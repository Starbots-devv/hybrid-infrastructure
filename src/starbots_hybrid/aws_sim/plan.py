"""Pinned data-only simulation policy and exact artifact checks."""
from decimal import Decimal
from importlib.resources import files

from ..contracts import envelope, timestamp, validate, verify_assessment
from ..io import digest, fail, parse_json, read_bytes, verify_subject

POLICY_FILE = files('starbots_hybrid').joinpath('data/sqs-simulation-policy.json')


def policy_bytes():
    return POLICY_FILE.read_bytes()


def policy_digest():
    return digest(policy_bytes())


def verify_plan(root, plan_path, evaluation_path, assessment_path, *, as_of, runner_digest,
                trusted_assessment_digest):
    plan_raw = read_bytes(root, plan_path)
    plan = validate(parse_json(plan_raw), expected_kind='ChangePlan', as_of=as_of)
    p = plan['payload']
    policy = parse_json(policy_bytes())
    if p['mode'] != 'PLAN' or p['environment'] != policy['environment']:
        fail('MODE_DENIED', 'Only a synthetic PLAN is supported')
    if p['account_id'] != policy['account_id'] or p['region'] != policy['region']:
        fail('IDENTITY_MISMATCH', 'Simulation identity must match pinned synthetic policy')
    if p['action_policy_digest'] != policy_digest() or p['runner_digest'] != runner_digest:
        fail('HASH_MISMATCH', 'Policy or runner digest differs')
    if len(p['actions']) != 1 or len(p['resources']) != 1:
        fail('ACTION_DENIED', 'Exactly one SQS action and resource are required')
    action = p['actions'][0]
    if (action != {'service':'sqs','operation':'CreateQueue','queue_name':p['resources'][0],'encrypted':True}
            or not action['queue_name'].startswith(policy['queue_prefix'])):
        fail('ACTION_DENIED', 'Only one fixed CreateQueue action is supported')
    if action['queue_name'] != policy['queue_prefix'] + p['idempotency_key']:
        fail('ACTION_DENIED', 'Queue name must derive from the signed idempotency key')
    if p['incremental_cost'] is None or Decimal(p['incremental_cost']) < 0 or p['currency'] != 'USD':
        fail('COST_UNKNOWN', 'A bounded synthetic USD incremental cost is required')
    if p['query_budget'] < 5:
        fail('QUERY_BUDGET', 'The identity and SQS verification budget is insufficient')
    now = timestamp(as_of)
    if not p.get('baseline_observed_at'):
        fail('EVIDENCE_STALE', 'A timed queue baseline is required for simulation')
    baseline_time = timestamp(p['baseline_observed_at'])
    if baseline_time > now or (now - baseline_time).total_seconds() > 300:
        fail('EVIDENCE_STALE', 'Reviewed queue baseline is older than five minutes')
    if now >= timestamp(p['expires_at']) or now >= timestamp(p['cost_valid_until']):
        fail('EVIDENCE_STALE', 'Plan or cost evidence expired')
    subject = envelope('SubjectRef', 'subject-for-simulation', p['subject_ref'],
                       client_id=plan['client_id'], project_id=plan['project_id'], created_at=plan['created_at'])
    validate(subject, expected_kind='SubjectRef', client_id=plan['client_id'], project_id=plan['project_id'])
    verify_subject(root, subject, client_id=plan['client_id'], project_id=plan['project_id'])
    evaluation_raw = read_bytes(root, evaluation_path)
    assessment_raw = read_bytes(root, assessment_path)
    if (digest(evaluation_raw) != p['evaluation_digest'] or digest(assessment_raw) != p['security_assessment_digest']
            or trusted_assessment_digest != p['security_assessment_digest']):
        fail('HASH_MISMATCH', 'Evaluation or assessment bytes differ from the plan')
    evaluation = validate(parse_json(evaluation_raw), expected_kind='EvaluationResult',
                          client_id=plan['client_id'], project_id=plan['project_id'], as_of=as_of)
    assessment_ref = {'path':assessment_path,'sha256':p['security_assessment_digest']}
    proposal_refs = [a for a in p['subject_ref']['artifacts'] if a['role'] == 'proposal']
    if (assessment_ref not in evaluation['payload']['security_assessment_refs']
            or len(proposal_refs) != 1 or proposal_refs[0] not in evaluation['payload']['input_manifest']):
        fail('HASH_MISMATCH', 'Evaluation does not bind the exact proposal and assessment')
    assessment = verify_assessment(root, {'path':assessment_path,'sha256':p['security_assessment_digest']},
                                   subject, as_of=as_of, expected_policy_id='starbots-local-review')
    plan_time = timestamp(plan['created_at'])
    if (timestamp(evaluation['created_at']) > plan_time
            or timestamp(assessment['created_at']) > plan_time
            or timestamp(assessment['payload']['assessed_at']) > plan_time
            or baseline_time > plan_time):
        fail('EVIDENCE_STALE', 'Change plan predates the evidence or queue baseline it reviews')
    if assessment['payload']['readiness']['state'] != 'READY':
        fail('INCOMPLETE_COVERAGE', 'Mandatory security controls are not ready')
    if p['security_policy_digest'] != assessment['payload']['policy_digest']:
        fail('HASH_MISMATCH', 'Security policy digest differs')
    if (now - timestamp(assessment['payload']['assessed_at'])).total_seconds() > policy['max_security_age_seconds']:
        fail('EVIDENCE_STALE', 'Security assessment is older than the simulation policy allows')
    return plan, digest(plan_raw), policy
