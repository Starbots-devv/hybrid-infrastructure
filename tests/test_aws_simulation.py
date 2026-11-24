"""Rejection matrix for the synthetic, local SQS simulator."""
import base64
import copy
import cryptography
import importlib.util
from functools import lru_cache
import io
import multiprocessing
from datetime import datetime, timezone
import os
from pathlib import Path
import secrets
import socket
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import starbots_hybrid
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from starbots_hybrid.contracts import control_profile, envelope, readiness, validate
from starbots_hybrid.io import ValidationError, digest, json_bytes, parse_json, read_bytes, write_bytes
try:
    from starbots_hybrid.aws_sim import run_simulation, reconcile_simulation, InMemorySQS, policy_digest
    from starbots_hybrid.aws_sim.journal import canonical_state_dir
except ModuleNotFoundError:
    run_simulation = reconcile_simulation = InMemorySQS = policy_digest = canonical_state_dir = None


NOW = '2026-10-18T12:00:00Z'
LATER = '2026-10-18T12:10:00Z'
HASH = 'a' * 64
ROOT = Path(__file__).resolve().parents[1]


@lru_cache(maxsize=1)
def evaluation_template():
    from starbots_hybrid.engine import analyze
    return analyze(ROOT / 'examples/hybrid-saving/bundle.json', as_of='2026-10-17T00:00:00Z')


def b64(raw):
    return base64.urlsafe_b64encode(raw).rstrip(b'=').decode('ascii')


def hold_lock(state_dir, approval_id, ready, release):
    from starbots_hybrid.aws_sim.journal import locked_journal
    with locked_journal(state_dir,'000000000000','us-east-1',approval_id):
        ready.set()
        release.wait(10)


class Fixture:
    def __init__(self, root):
        self.root = Path(root)
        self.key = Ed25519PrivateKey.generate()  # Ephemeral fixture key; never a real trust root.
        from cryptography.hazmat.primitives import serialization
        self.public = self.key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
        self.state = canonical_state_dir()
        self.transport = InMemorySQS(account_id='000000000000', region='us-east-1')
        self._artifacts()

    def put(self, path, obj):
        raw = json_bytes(obj)
        write_bytes(self.root, path, raw)
        return digest(raw)

    def _artifacts(self):
        profile, profile_raw = control_profile('starbots-local-review')
        write_bytes(self.root, 'control-profile.json', profile_raw)
        write_bytes(self.root, 'proposal.json', b'synthetic reviewed proposal\n')
        artifacts = [
            {'role':'proposal','path':'proposal.json','sha256':digest(b'synthetic reviewed proposal\n')},
            {'role':'security-control-profile','path':'control-profile.json','sha256':digest(profile_raw)},
        ]
        controls=[];evidence_refs=[];verified=set()
        for required in profile['required_controls']:
            control_id=required['id']
            observation={'state':'PASS','coverage':{'performed':True},'evidence':{}}
            if control_id in ('SB-AUTH','SB-RLS'):
                observation['evidence']={'probes':[{'passed':True}], 'fixture_sha256':HASH}
            if control_id=='SB-AGENT-BOUNDARY':
                observation['evidence']={'evaluation_type':'deterministic-policy-harness; no model invoked',
                    'cases':[{'allowed':True,'matched':True} for _ in range(12)],'mutating_calls':0}
            proof_path=f'proof/{control_id}.json'
            proof_hash=self.put(proof_path,{'control_id':control_id,'observation':observation})
            evidence_id=f'evidence-{control_id}'
            evidence_path=f'evidence/{control_id}.json'
            evidence=envelope('Evidence',evidence_id,{
                'evidence_type':'manual-review','source':'local','source_uri':'synthetic://sim',
                'observed_at':'2026-10-18T11:00:00Z','valid_until':'2026-10-19T12:00:00Z',
                'classification':'synthetic','evidence_level':'measured','artifact_path':proof_path,
                'artifact_sha256':proof_hash,'redaction_status':'no_sensitive_data','collector':'fixture',
                'tool_version':None,'rules_digest':None,'authorized_scope_id':'fixture-sim'},
                client_id='synthetic',project_id='sim',created_at='2026-10-18T11:00:00Z')
            evidence_hash=self.put(evidence_path,evidence)
            artifacts.extend([{'role':'observation','path':proof_path,'sha256':proof_hash},
                              {'role':'evidence','path':evidence_path,'sha256':evidence_hash}])
            evidence_refs.append({'path':evidence_path,'sha256':evidence_hash})
            controls.append({'id':control_id,'mandatory':True,'state':'PASS','evidence_refs':[evidence_id],
                             'rationale':'Synthetic local fixture check performed','external_refs':[]})
            verified.add(evidence_id)
        manifest = {'subject_id':'subject-sim','revision':'1','client_id':'synthetic','project_id':'sim','artifacts':artifacts}
        manifest_hash = self.put('manifest.json', manifest)
        self.subject = {'subject_id':'subject-sim','revision':'1','manifest_path':'manifest.json','manifest_sha256':manifest_hash,'artifacts':artifacts}
        coverage = {'performed':[c['id'] for c in controls],'missing':[],'excluded':[]}
        tool_runs=[{'tool':name,'tool_version':'fixture-1','rules_digest':None,'advisory_digest':None,
                    'status':'executed','output_ref':None} for name in profile['required_tools']]
        assessment = envelope('SecurityAssessment','assessment-sim',{
            'subject_ref':self.subject,'policy_id':profile['id'],'policy_version':profile['version'],
            'policy_digest':digest(profile_raw),'assessed_at':'2026-10-18T11:00:00Z',
            'expires_at':'2026-10-19T12:00:00Z','scope':'synthetic fixture',
            'evidence_refs':evidence_refs,'tool_runs':tool_runs,'controls':controls,'findings':[],'coverage':coverage,
            'readiness':readiness(controls,[],coverage,verified,tool_runs,policy_id='starbots-local-review')},
            client_id='synthetic',project_id='sim',created_at='2026-10-18T11:00:00Z')
        self.assessment_hash = self.put('assessment.json', assessment)
        evaluation = copy.deepcopy(evaluation_template())
        evaluation['client_id'] = 'synthetic'
        evaluation['project_id'] = 'sim'
        evaluation['created_at'] = '2026-10-18T11:59:00Z'
        evaluation['payload']['security_assessment_refs'] = [{'path':'assessment.json','sha256':self.assessment_hash}]
        evaluation['payload']['input_manifest'].append(artifacts[0])
        self.evaluation_hash = self.put('evaluation.json', evaluation)
        self.plan = envelope('ChangePlan','plan-sim',{
            'subject_ref':self.subject,'evaluation_digest':self.evaluation_hash,
            'security_assessment_digest':self.assessment_hash,'security_policy_digest':digest(profile_raw),
            'runner_version':'synthetic-1','runner_digest':HASH,'action_policy_digest':policy_digest(),
            'mode':'PLAN','environment':'sandbox','account_id':'000000000000','region':'us-east-1',
            'resources':['starbots-sandbox-sim'],'actions':[{'service':'sqs','operation':'CreateQueue','queue_name':'starbots-sandbox-sim','encrypted':True}],
            'preconditions':['queue absent'],'baseline_state_digest':self.transport.state_digest('starbots-sandbox-sim'),
            'baseline_observed_at':'2026-10-18T11:59:00Z',
            'diff':'Create one synthetic queue','incremental_cost':'0','currency':'USD',
            'cost_valid_until':'2026-10-19T12:00:00Z','query_budget':5,'blast_radius':'one synthetic queue',
            'backup_rollback':'manual synthetic cleanup review','stop_conditions':['drift'],
            'expected_postconditions':['queue matches fixed attributes and tags'],
            'idempotency_key':'sim','expires_at':LATER},
            client_id='synthetic',project_id='sim',created_at='2026-10-18T11:59:00Z')
        self.sign()

    def sign(self):
        self.plan_hash = self.put('plan.json', self.plan)
        p = self.plan['payload']
        signed = {'approval_id':'approval-'+secrets.token_hex(8),'plan_sha256':self.plan_hash,
                  'proposal_sha256':p['subject_ref']['manifest_sha256'],
                  'assessment_sha256':self.assessment_hash,'policy_sha256':p['action_policy_digest'],
                  'runner_sha256':p['runner_digest'],'account_id':p['account_id'],
                  'region':p['region'],'environment':p['environment'],
                  'resource_scope':p['resources'],'action_allowlist':['sqs:CreateQueue'],
                  'max_incremental_cost':'1','query_budget':5,
                  'issued_at':'2026-10-18T11:59:00Z','expires_at':LATER,'approver_id':'fixture-operator'}
        raw = json_bytes(signed)
        self.approval = envelope('ApprovalEnvelope','approval-envelope-sim',{
            **signed,'signed_payload_base64url':b64(raw),
            'signature':{'algorithm':'Ed25519','key_id':'fixture-key','value':b64(self.key.sign(raw))}},
            client_id='synthetic',project_id='sim',created_at='2026-10-18T11:59:00Z')
        self.put('approval.json', self.approval)

    def replace_assessment(self, assessment):
        self.assessment_hash=self.put('assessment.json',assessment)
        evaluation=parse_json(read_bytes(self.root,'evaluation.json'))
        evaluation['payload']['security_assessment_refs']=[{'path':'assessment.json','sha256':self.assessment_hash}]
        self.evaluation_hash=self.put('evaluation.json',evaluation)
        self.plan['payload']['security_assessment_digest']=self.assessment_hash
        self.plan['payload']['evaluation_digest']=self.evaluation_hash
        self.sign()

    def run(self, **kw):
        args = dict(root=self.root,plan_path='plan.json',approval_path='approval.json',
                    evaluation_path='evaluation.json',assessment_path='assessment.json',
                    trust_keys={'fixture-key':self.public},revoked_key_ids=set(),
                    runner_digest=HASH,as_of=NOW,transport=self.transport,state_dir=self.state,
                    trusted_assessment_digest=self.assessment_hash)
        args.update(kw)
        return run_simulation(**args)

    def journal_path(self):
        scope=digest(b'000000000000:us-east-1')[:24]
        approval_scope=digest(self.approval['payload']['approval_id'].encode('ascii'))[:24]
        return self.state/(scope+'-'+approval_scope+'.jsonl')

    def rejection_journal_path(self):
        scope=digest(b'LOCAL:SIMULATION')[:24]
        approval_scope=digest(b'rejections')[:24]
        return self.state/(scope+'-'+approval_scope+'.jsonl')


class SimulationTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('starbots_hybrid.aws_sim'), 'Simulator package is missing')
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.fx=Fixture(self.tmp.name)

    def test_success_is_simulated_and_single_mutation(self):
        with patch.object(socket,'socket',side_effect=AssertionError('network forbidden')), \
             patch.object(subprocess,'Popen',side_effect=AssertionError('subprocess forbidden')), \
             patch.dict(os.environ,{'AWS_ACCESS_KEY_ID':'FAKE_TEST_ONLY','AWS_SECRET_ACCESS_KEY':'FAKE_TEST_ONLY'}):
            record=self.fx.run()
        validate(record,expected_kind='ExecutionRecord')
        self.assertEqual(record['payload']['execution_kind'],'SIMULATED')
        self.assertEqual(record['payload']['state'],'succeeded')
        self.assertEqual(record['created_at'],NOW)
        self.assertEqual(self.fx.transport.mutations,['CreateQueue'])
        self.assertLessEqual(len(self.fx.transport.reads),5)
        for stage in ('preflight_evidence_refs','postcondition_evidence_refs'):
            self.assertEqual(len(record['payload'][stage]),1)
            ref=record['payload'][stage][0]
            self.assertEqual(digest(read_bytes(self.fx.state,ref['path'])),ref['sha256'])
        self.assertEqual(self.fx.transport.queues['starbots-sandbox-sim']['attributes']['SqsManagedSseEnabled'],'true')
        self.assertNotIn('KmsMasterKeyId',self.fx.transport.queues['starbots-sandbox-sim']['attributes'])

    def test_rejection_matrix_never_mutates(self):
        cases=[
            ('absent approval',lambda f:(f.root/'approval.json').unlink()),
            ('forged signature',lambda f:f.approval['payload']['signature'].__setitem__('value',b64(b'0'*64))),
            ('changed signed field',lambda f:f.approval['payload'].__setitem__('region','eu-west-1')),
            ('wrong client',lambda f:f.plan.__setitem__('client_id','another')),
            ('real mode',lambda f:f.plan['payload'].__setitem__('mode','APPLY_AWS')),
            ('delete',lambda f:f.plan['payload']['actions'][0].__setitem__('operation','DeleteQueue')),
            ('mixed action',lambda f:f.plan['payload']['actions'].append({'service':'iam','operation':'CreateRole','queue_name':'x','encrypted':True})),
            ('unknown cost',lambda f:f.plan['payload'].__setitem__('incremental_cost',None)),
            ('expired cost',lambda f:f.plan['payload'].__setitem__('cost_valid_until','2026-10-17T00:00:00Z')),
            ('zero query budget',lambda f:f.plan['payload'].__setitem__('query_budget',0)),
            ('malicious metadata',lambda f:f.plan['payload'].__setitem__('command','del C:\\*')),
        ]
        for name,change in cases:
            with self.subTest(name=name),tempfile.TemporaryDirectory() as t:
                f=Fixture(t);change(f)
                if (f.root/'plan.json').exists():f.put('plan.json',f.plan)
                if (f.root/'approval.json').exists():f.put('approval.json',f.approval)
                with self.assertRaises(ValidationError):f.run()
                self.assertEqual(f.transport.mutations,[])

    def test_tampered_artifact_revocation_and_expiry_reject(self):
        for action in ('proposal','assessment','evaluation','revoked','expired','missing key'):
            with self.subTest(action=action),tempfile.TemporaryDirectory() as t:
                f=Fixture(t);kw={}
                if action in ('proposal','assessment','evaluation'):(f.root/(action+'.json')).write_bytes(b'changed')
                if action=='revoked':kw['revoked_key_ids']={'fixture-key'}
                if action=='expired':kw['as_of']='2026-10-18T12:11:00Z'
                if action=='missing key':kw['trust_keys']={}
                with self.assertRaises(ValidationError):f.run(**kw)
                self.assertEqual(f.transport.mutations,[])

    def test_drift_and_foreign_queue_reject_before_create(self):
        self.fx.transport.queues['starbots-sandbox-sim']={'attributes':{},'tags':{'owner':'other'}}
        with self.assertRaises(ValidationError):self.fx.run()
        self.assertEqual(self.fx.transport.mutations,[])

    def test_plan_cannot_predate_bound_evaluation_or_assessment(self):
        for created_at in ('2026-10-18T11:58:59Z','2026-10-18T10:59:59Z'):
            with self.subTest(created_at=created_at),tempfile.TemporaryDirectory() as t:
                f=Fixture(t)
                f.plan['created_at']=created_at
                f.sign()
                with self.assertRaises(ValidationError) as caught:f.run()
                self.assertEqual(caught.exception.code,'EVIDENCE_STALE')
                self.assertEqual(f.transport.mutations,[])

    def test_approval_cannot_predate_change_plan(self):
        self.fx.plan['created_at']='2026-10-18T11:59:30Z'
        self.fx.sign()
        with self.assertRaises(ValidationError) as caught:self.fx.run()
        self.assertEqual(caught.exception.code,'EVIDENCE_STALE')
        self.assertEqual(self.fx.transport.mutations,[])

    def test_preflight_rejection_persists_redacted_execution_record(self):
        self.fx.plan['client_id']='sensitive_customer'
        self.fx.put('plan.json',self.fx.plan)
        with self.assertRaises(ValidationError):self.fx.run()
        from starbots_hybrid.aws_sim.journal import Journal
        journal=Journal(self.fx.rejection_journal_path())
        self.assertEqual(journal.entries[-1]['state'],'rejected')
        ref=journal.entries[-1]['evidence_ref']
        raw=read_bytes(self.fx.state,ref['path'])
        self.assertEqual(digest(raw),ref['sha256'])
        self.assertNotIn(b'sensitive_customer',raw)
        record=validate(parse_json(raw),expected_kind='ExecutionRecord')
        self.assertEqual(record['payload']['execution_kind'],'SIMULATED')
        self.assertEqual(record['payload']['state'],'rejected')
        self.assertEqual(record['payload']['verified_identity'],'unverified')
        self.assertEqual(record['created_at'],NOW)
        self.assertEqual(self.fx.transport.mutations,[])

    def test_replay_across_runner_instances_has_no_second_create(self):
        self.fx.run()
        with self.assertRaises(ValidationError):self.fx.run()
        self.assertEqual(self.fx.transport.mutations,['CreateQueue'])

    def test_timeout_after_effect_reconciles_without_repeat_mutation(self):
        self.fx.transport.fault='after_effect_timeout'
        first=self.fx.run()
        self.assertIn(first['payload']['state'],('partial','unknown'))
        self.assertEqual(self.fx.transport.mutations,['CreateQueue'])
        self.fx.transport.fault=None
        second=self.fx.run()
        self.assertEqual(second['payload']['state'],'succeeded')
        self.assertEqual(self.fx.transport.mutations,['CreateQueue'])

    def test_expired_approval_has_read_only_recovery(self):
        self.fx.transport.fault='after_effect_timeout'
        self.assertEqual(self.fx.run()['payload']['state'],'partial')
        with self.assertRaises(ValidationError):self.fx.run(as_of='2026-10-18T12:11:00Z')
        self.fx.transport.fault=None
        result=reconcile_simulation(root=self.fx.root,plan_path='plan.json',approval_path='approval.json',
            evaluation_path='evaluation.json',assessment_path='assessment.json',
            trust_keys={'fixture-key':self.fx.public},revoked_key_ids=set(),runner_digest=HASH,
            trusted_assessment_digest=self.fx.assessment_hash,as_of='2026-10-18T12:11:00Z',
            transport=self.fx.transport,state_dir=self.fx.state)
        self.assertEqual(result['payload']['state'],'succeeded')
        self.assertEqual(result['created_at'],'2026-10-18T12:11:00Z')
        self.assertEqual(self.fx.transport.mutations,['CreateQueue'])

    def test_reconciliation_requires_own_transaction_tag(self):
        self.fx.transport.fault='after_effect_timeout'
        self.assertEqual(self.fx.run()['payload']['state'],'partial')
        self.fx.transport.queues['starbots-sandbox-sim']['tags']['starbots:transaction-id']='foreign-transaction'
        self.fx.transport.fault=None
        result=self.fx.run()
        self.assertEqual(result['payload']['state'],'partial')
        self.assertEqual(self.fx.transport.mutations,['CreateQueue'])

    def test_queue_name_binds_signed_idempotency_key(self):
        self.fx.plan['payload']['idempotency_key']='another-action'
        self.fx.sign()
        with self.assertRaises(ValidationError):self.fx.run()
        self.assertEqual(self.fx.transport.mutations,[])

    def test_distinct_state_dirs_cannot_bypass_one_canonical_journal(self):
        with tempfile.TemporaryDirectory() as left,tempfile.TemporaryDirectory() as right:
            for candidate in (left,right):
                with self.assertRaises(ValidationError) as caught:self.fx.run(state_dir=candidate)
                self.assertEqual(caught.exception.code,'PATH_DENIED')
            self.assertEqual(self.fx.transport.mutations,[])
        self.fx.run()
        with self.assertRaises(ValidationError) as caught:self.fx.run()
        self.assertEqual(caught.exception.code,'REPLAY_DENIED')

    def test_apply_aws_argument_is_impossible(self):
        with self.assertRaises(ValidationError):self.fx.run(mode='APPLY_AWS')
        self.assertEqual(self.fx.transport.mutations,[])

    def test_stale_baseline_and_wrong_simulated_caller_reject(self):
        self.fx.plan['payload']['baseline_observed_at']='2026-10-18T11:00:00Z'
        self.fx.sign()
        with self.assertRaises(ValidationError):self.fx.run()
        self.assertEqual(self.fx.transport.mutations,[])
        with tempfile.TemporaryDirectory() as t:
            f=Fixture(t);f.transport.account_id='999999999999'
            with self.assertRaises(ValidationError):f.run()
            self.assertEqual(f.transport.mutations,[])

    def test_timeout_before_effect_and_postcondition_mismatch(self):
        for fault,expected in [('before_effect_timeout','unknown'),('postcondition_mismatch','partial')]:
            with self.subTest(fault=fault),tempfile.TemporaryDirectory() as t:
                f=Fixture(t);f.transport.fault=fault
                result=f.run()
                self.assertEqual(result['payload']['state'],expected)
                self.assertNotEqual(result['payload']['state'],'succeeded')
                if fault=='postcondition_mismatch':
                    replay=f.run()
                    self.assertEqual(replay['payload']['state'],'partial')
                    self.assertEqual(f.transport.mutations,['CreateQueue'])

    def test_journal_tamper_and_lock_contention_fail_closed(self):
        from starbots_hybrid.aws_sim.journal import locked_journal
        with locked_journal(self.fx.state,'000000000000','us-east-1',self.fx.approval['payload']['approval_id']):
            with self.assertRaises(ValidationError) as caught:self.fx.run()
            self.assertEqual(caught.exception.code,'LOCK_BUSY')
        self.fx.run()
        journal_path=self.fx.journal_path()
        journal_path.write_bytes(journal_path.read_bytes()+b'{"event":"forged"}\n')
        with self.assertRaises(ValidationError):self.fx.run()
        self.assertEqual(self.fx.transport.mutations,['CreateQueue'])

    def test_audit_snapshot_tamper_fails_closed(self):
        record=self.fx.run()
        ref=record['payload']['postcondition_evidence_refs'][0]
        (self.fx.state/ref['path']).write_bytes(b'changed')
        with self.assertRaises(ValidationError) as caught:self.fx.run()
        self.assertEqual(caught.exception.code,'JOURNAL_TAMPERED')
        self.assertEqual(self.fx.transport.mutations,['CreateQueue'])

    def test_reconciliation_snapshot_tamper_fails_after_restart(self):
        self.fx.transport.fault='after_effect_timeout'
        self.fx.run()
        self.fx.transport.fault=None
        reconciled=self.fx.run()
        ref=reconciled['payload']['postcondition_evidence_refs'][0]
        (self.fx.state/ref['path']).write_bytes(b'changed')
        with self.assertRaises(ValidationError) as caught:self.fx.run()
        self.assertEqual(caught.exception.code,'JOURNAL_TAMPERED')
        self.assertEqual(self.fx.transport.mutations,['CreateQueue'])

    def test_different_temp_environments_share_replay_journal(self):
        self.fx.run()
        key_path=self.fx.root/'test-public-key.bin'
        key_path.write_bytes(self.fx.public)
        with tempfile.TemporaryDirectory() as other_temp:
            env=dict(os.environ)
            env.update({'TEMP':other_temp,'TMP':other_temp,'TMPDIR':other_temp})
            # The child must import the same checkout or wheel as this process;
            # swapping installations would intentionally change journal scope.
            package_root=Path(starbots_hybrid.__file__).resolve().parents[1]
            env['PYTHONPATH']=os.pathsep.join((str(package_root),str(Path(cryptography.__file__).resolve().parents[1])))
            command=[sys.executable,'-m','starbots_hybrid.aws_sim','--root',str(self.fx.root),
                '--plan','plan.json','--approval','approval.json','--evaluation','evaluation.json',
                '--assessment','assessment.json','--trust-public-key',str(key_path),
                '--trust-key-id','fixture-key','--runner-digest',HASH,
                '--review-receipt-sha256',self.fx.assessment_hash,'--as-of',NOW]
            result=subprocess.run(command,env=env,capture_output=True,text=True,timeout=30)
        self.assertEqual(result.returncode,2,result.stdout+result.stderr)
        self.assertEqual(__import__('json').loads(result.stdout)['error'],'REPLAY_DENIED')

    def test_external_transport_subclass_is_rejected(self):
        class UnsafeTransport(InMemorySQS):
            pass
        with self.assertRaises(ValidationError):self.fx.run(transport=UnsafeTransport(account_id='000000000000',region='us-east-1'))
        self.assertEqual(self.fx.transport.mutations,[])

    def test_missing_mandatory_control_and_stale_assessment_reject(self):
        for condition in ('missing-control','stale-assessment'):
            with self.subTest(condition=condition),tempfile.TemporaryDirectory() as t:
                f=Fixture(t)
                assessment=parse_json(read_bytes(f.root,'assessment.json'))
                payload=assessment['payload']
                if condition=='missing-control':
                    payload['controls'][0]['state']='UNKNOWN'
                    payload['coverage']={'performed':[],'missing':['SB-AUTH'],'excluded':[]}
                    payload['readiness']=readiness(payload['controls'],[],payload['coverage'],
                        {c['evidence_refs'][0] for c in payload['controls']},payload['tool_runs'],
                        policy_id='starbots-local-review')
                else:
                    payload['assessed_at']='2026-10-17T10:00:00Z'
                f.replace_assessment(assessment)
                with self.assertRaises(ValidationError):f.run()
                self.assertEqual(f.transport.mutations,[])

    def test_two_processes_cannot_apply_same_scope_together(self):
        ctx=multiprocessing.get_context('spawn')
        ready=ctx.Event();release=ctx.Event()
        holder=ctx.Process(target=hold_lock,args=(str(self.fx.state),self.fx.approval['payload']['approval_id'],ready,release))
        holder.start()
        try:
            self.assertTrue(ready.wait(10),'lock holder did not start')
            with self.assertRaises(ValidationError) as caught:self.fx.run()
            self.assertEqual(caught.exception.code,'LOCK_BUSY')
            self.assertEqual(self.fx.transport.mutations,[])
        finally:
            release.set();holder.join(10)
            if holder.is_alive():holder.terminate();holder.join(5)
        self.assertEqual(holder.exitcode,0)

    def test_cli_explicit_apply_aws_is_rejected(self):
        from starbots_hybrid.aws_sim.__main__ import main
        output=io.StringIO()
        with redirect_stdout(output):
            status=main(['--root',str(self.fx.root),'--plan','plan.json','--approval','approval.json',
                         '--evaluation','evaluation.json','--assessment','assessment.json',
                         '--state-dir',str(self.fx.state),'--trust-public-key','unused',
                         '--trust-key-id','fixture-key','--runner-digest',HASH,
                         '--review-receipt-sha256',self.fx.assessment_hash,'--as-of',NOW,
                         '--mode','APPLY_AWS'])
        self.assertEqual(status,2)
        self.assertEqual(__import__('json').loads(output.getvalue())['error'],'MODE_DENIED')
        self.assertEqual(self.fx.transport.mutations,[])
        from starbots_hybrid.aws_sim.journal import Journal
        self.assertEqual(Journal(self.fx.rejection_journal_path()).entries[-1]['error_code'],'MODE_DENIED')


if __name__=='__main__':unittest.main()
