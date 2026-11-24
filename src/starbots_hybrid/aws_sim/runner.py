"""Fail-closed state machine for one synthetic SQS CreateQueue."""
from datetime import datetime, timezone

from ..contracts import envelope, timestamp, validate
from ..io import ValidationError, digest, fail, parse_json, read_bytes
from .approval import verify_approval
from .journal import locked_journal
from .plan import policy_digest, verify_plan
from .transport import InMemorySQS, SimulatedTimeout


def _expected(plan, plan_digest, policy, transaction_id):
    name = plan['payload']['actions'][0]['queue_name']
    return name, policy['attributes'], {'starbots:plan-sha256':plan_digest,
                                        'starbots:client-id':plan['client_id'],
                                        'starbots:transaction-id':transaction_id}


def _matches(transport, name, attributes, tags):
    if transport.get_queue_url(name) is None:
        return False
    return transport.get_queue_attributes(name) == attributes and transport.list_queue_tags(name) == tags


def _record(plan, plan_digest, approval_digest, policy, *, state, transaction_id,
            as_of, attempt=None, partial_effects=None, reconciliation='', preflight_refs=None, postcondition_refs=None):
    p = plan['payload']
    attempt_list = [attempt] if attempt else []
    record = envelope('ExecutionRecord', transaction_id, {
        'execution_kind':'SIMULATED','plan_digest':plan_digest,'approval_digest':approval_digest,
        'verified_identity':p['account_id'] + '/' + p['region'],
        'scope':p['resources'][0],'runner_digest':p['runner_digest'],
        'policy_digest':p['action_policy_digest'],'transaction_id':transaction_id,
        'action_attempts':attempt_list,'preflight_evidence_refs':preflight_refs or [],
        'drift_evidence_refs':[],'postcondition_evidence_refs':postcondition_refs or [],
        'partial_effects':partial_effects or [],'reconciliation':reconciliation,'state':state},
        client_id=plan['client_id'],project_id=plan['project_id'],created_at=as_of)
    return validate(record, expected_kind='ExecutionRecord')


def _execute_simulation(*, root, plan_path, approval_path, evaluation_path, assessment_path,
                        trust_keys, revoked_key_ids, runner_digest, as_of, transport, state_dir,
                        trusted_assessment_digest, mode='PLAN', _recovery_only=False):
    """Verify exact local artifacts then simulate at most one CreateQueue.

    All trust inputs are explicitly synthetic. No environment variables or credentials are read.
    """
    if mode != 'PLAN':
        fail('MODE_DENIED', 'APPLY_AWS is unavailable in this package')
    if type(transport) is not InMemorySQS:
        fail('TRANSPORT_DENIED', 'Only the in-memory SQS transport is accepted')
    timestamp(as_of)
    verification_clock = as_of
    if _recovery_only:
        claimed = parse_json(read_bytes(root,approval_path))
        try: verification_clock = claimed['payload']['issued_at']
        except (KeyError,TypeError): fail('INVALID_SCHEMA','Recovery approval is malformed')
        if timestamp(as_of) < timestamp(verification_clock):
            fail('APPROVAL_EXPIRED','Recovery cannot precede approval issue time')
    plan, plan_hash, policy = verify_plan(root, plan_path, evaluation_path, assessment_path,
                                         as_of=verification_clock, runner_digest=runner_digest,
                                         trusted_assessment_digest=trusted_assessment_digest)
    approval, approval_hash = verify_approval(root, approval_path, plan, plan_hash,
                                              trust_keys=trust_keys, revoked_key_ids=revoked_key_ids,
                                              as_of=verification_clock)
    p = plan['payload']
    signed = approval['payload']
    transaction_id = digest((signed['approval_id'] + ':' + plan_hash + ':' + p['idempotency_key']).encode('ascii'))[:32]
    name, attributes, tags = _expected(plan, plan_hash, policy, transaction_id)
    with locked_journal(state_dir, p['account_id'], p['region'], signed['approval_id']) as journal:
        transport.begin_read_budget(p['query_budget'])
        identity = transport.get_caller_identity()
        if identity != {'account_id':p['account_id']} or transport.region != p['region']:
            fail('IDENTITY_MISMATCH', 'Simulated caller identity differs')
        prior = journal.last_for(signed['approval_id'])
        if prior:
            if prior['plan_digest'] != plan_hash:
                fail('REPLAY_DENIED', 'Approval ID was consumed by another plan')
            if prior['state'] not in ('partial','unknown','applying'):
                fail('REPLAY_DENIED', 'Approval ID was already consumed')
            matches = _matches(transport, name, attributes, tags)
            state = 'succeeded' if matches else ('partial' if transport.get_queue_url(name) is not None else 'unknown')
            post_ref = journal.evidence('reconciliation',
                {'queue_state_sha256':transport.state_digest(name),'matches_expected':matches,'state':state})
            journal.append({'approval_id':signed['approval_id'],'plan_digest':plan_hash,
                            'state':state,'transaction_id':transaction_id,'detail':'read-only reconciliation',
                            'evidence_ref':post_ref})
            return _record(plan,plan_hash,approval_hash,policy,state=state,
                           transaction_id=transaction_id,as_of=as_of,
                           partial_effects=['queue exists with mismatched state'] if state == 'partial' else [],
                           reconciliation='read-only reconciliation',postcondition_refs=[post_ref])
        if _recovery_only:
            fail('RECOVERY_NOT_FOUND','Read-only recovery requires a consumed approval')
        journal.append({'approval_id':signed['approval_id'],'plan_digest':plan_hash,
                        'state':'authorized','transaction_id':transaction_id,'detail':'signature verified'})
        try:
            # Check a scoped read as well as the exact baseline digest; existing foreign queues never reconcile.
            existing = transport.get_queue_url(name)
            if existing is not None or transport.state_digest(name) != p['baseline_state_digest']:
                drift_ref = journal.evidence('drift',
                    {'expected_state_sha256':p['baseline_state_digest'],
                     'observed_state_sha256':transport.state_digest(name),'queue_exists':existing is not None})
                journal.append({'approval_id':signed['approval_id'],'plan_digest':plan_hash,
                                'state':'rejected','transaction_id':transaction_id,'detail':'drift',
                                'evidence_ref':drift_ref})
                fail('DRIFT_DETECTED', 'Queue state differs from the reviewed baseline')
            preflight_ref = journal.evidence('preflight',
                {'account_id':p['account_id'],'region':p['region'],'queue_name':name,
                 'baseline_state_sha256':p['baseline_state_digest'],'observed_at':as_of})
            journal.append({'approval_id':signed['approval_id'],'plan_digest':plan_hash,
                            'state':'preflight_verified','transaction_id':transaction_id,
                            'detail':'identity and absent queue match baseline','evidence_ref':preflight_ref})
            journal.append({'approval_id':signed['approval_id'],'plan_digest':plan_hash,
                            'state':'applying','transaction_id':transaction_id,'detail':'CreateQueue pending'})
            attempt = {'operation':'sqs:CreateQueue','started_at':as_of,'ended_at':as_of,
                       'request_id':transaction_id[:24],'result':'synthetic result','state':'applying'}
            try:
                transport.create_queue(name=name,attributes=attributes,tags=tags)
            except SimulatedTimeout:
                # A timeout is never success on the first attempt, even if the effect happened.
                effect = transport.get_queue_url(name) is not None
                state = 'partial' if effect else 'unknown'
                attempt['state'] = state
                attempt['result'] = 'synthetic timeout; effect requires reconciliation'
                post_ref = journal.evidence('timeout',
                    {'queue_state_sha256':transport.state_digest(name),'queue_exists':effect,'state':state})
                journal.append({'approval_id':signed['approval_id'],'plan_digest':plan_hash,
                                'state':state,'transaction_id':transaction_id,
                                'detail':'effect observed' if effect else 'effect not observed',
                                'evidence_ref':post_ref})
                return _record(plan,plan_hash,approval_hash,policy,state=state,
                               transaction_id=transaction_id,as_of=as_of,attempt=attempt,
                               partial_effects=['queue may exist'] if effect else [],
                               reconciliation='Read-only retry required',preflight_refs=[preflight_ref],
                               postcondition_refs=[post_ref])
            state = 'succeeded' if _matches(transport,name,attributes,tags) else 'partial'
            attempt['state'] = state
            attempt['result'] = 'synthetic postconditions match' if state == 'succeeded' else 'synthetic postcondition mismatch'
            post_ref = journal.evidence('postcondition',
                {'queue_state_sha256':transport.state_digest(name),'matches_expected':state == 'succeeded','state':state})
            journal.append({'approval_id':signed['approval_id'],'plan_digest':plan_hash,
                            'state':state,'transaction_id':transaction_id,'detail':attempt['result'],
                            'evidence_ref':post_ref})
            return _record(plan,plan_hash,approval_hash,policy,state=state,
                           transaction_id=transaction_id,as_of=as_of,attempt=attempt,
                           partial_effects=[] if state == 'succeeded' else ['queue exists with mismatched state'],
                           reconciliation='postconditions checked by read-only transport',
                           preflight_refs=[preflight_ref],postcondition_refs=[post_ref])
        except ValidationError as exc:
            journal.append({'approval_id':signed['approval_id'],'plan_digest':plan_hash,
                            'state':'rejected','transaction_id':transaction_id,'detail':exc.code})
            raise


def _available_digest(root, path):
    try:
        return digest(read_bytes(root, path))
    except ValidationError:
        return digest(b'')


def _persist_rejection(*, root, plan_path, approval_path, as_of, error):
    """Keep a contract-valid denial without trusting or disclosing rejected input fields."""
    try:
        timestamp(as_of)
        recorded_at = as_of
    except ValidationError:
        recorded_at = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    plan_hash = _available_digest(root, plan_path)
    approval_hash = _available_digest(root, approval_path)
    transaction_id = digest((plan_hash + approval_hash + recorded_at + error.code).encode('ascii'))[:32]
    record = envelope('ExecutionRecord', transaction_id, {
        'execution_kind':'SIMULATED','plan_digest':plan_hash,'approval_digest':approval_hash,
        'verified_identity':'unverified','scope':'unverified',
        'runner_digest':digest(b'UNVERIFIED_RUNNER'),'policy_digest':policy_digest(),
        'transaction_id':transaction_id,'action_attempts':[],
        'preflight_evidence_refs':[],'drift_evidence_refs':[],'postcondition_evidence_refs':[],
        'partial_effects':[],'reconciliation':error.code,'state':'rejected'},
        client_id='simulation',project_id='local',created_at=recorded_at)
    validate(record, expected_kind='ExecutionRecord')
    with locked_journal(None, 'LOCAL', 'SIMULATION', 'rejections') as journal:
        ref = journal.evidence('rejected', record)
        journal.append({'approval_id':approval_hash,'plan_digest':plan_hash,
                        'execution_kind':'SIMULATED','state':'rejected',
                        'error_code':error.code,'evidence_ref':ref})


def run_simulation(*, root, plan_path, approval_path, evaluation_path, assessment_path,
                   trust_keys, revoked_key_ids, runner_digest, as_of, transport, state_dir,
                   trusted_assessment_digest, mode='PLAN', _recovery_only=False):
    try:
        return _execute_simulation(root=root,plan_path=plan_path,approval_path=approval_path,
            evaluation_path=evaluation_path,assessment_path=assessment_path,
            trust_keys=trust_keys,revoked_key_ids=revoked_key_ids,runner_digest=runner_digest,
            as_of=as_of,transport=transport,state_dir=state_dir,
            trusted_assessment_digest=trusted_assessment_digest,mode=mode,
            _recovery_only=_recovery_only)
    except ValidationError as exc:
        _persist_rejection(root=root,plan_path=plan_path,approval_path=approval_path,
                           as_of=as_of,error=exc)
        raise


def reconcile_simulation(**kwargs):
    """After a partial/unknown transaction, reconcile read-only even after expiry.

    This entry point cannot create a queue or grant new mutation authority.
    """
    if '_recovery_only' in kwargs:
        fail('MODE_DENIED','Recovery mode is reserved')
    return run_simulation(**kwargs, _recovery_only=True)
