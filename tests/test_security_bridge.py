import importlib.util
from pathlib import Path
import tempfile
import unittest
from starbots_hybrid.io import ValidationError, digest, json_bytes, write_bytes
from starbots_hybrid.contracts import envelope

class BridgeTests(unittest.TestCase):
    def test_security_export_roundtrip_and_forged_readiness_rejection(self):
        import shutil
        from starbots_hybrid.security_bridge import verify_security
        from starbots_hybrid.io import load_json
        source=Path(__file__).parent/'fixtures/security-review'
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)/'review';shutil.copytree(source,root)
            receipt=digest((root/'security-assessment.json').read_bytes())
            args=dict(client_id='synthetic',project_id='bridge-test',as_of='2026-10-18T21:33:00Z')
            result=verify_security(root,root/'proposal/subject.json',receipt,**args)
            self.assertTrue(result['valid']);self.assertEqual(result['readiness'],'BLOCKED');self.assertFalse(result['execution_eligible'])
            for changed in [dict(client_id='other'),dict(project_id='other'),dict(as_of='2026-10-20T21:33:00Z')]:
                with self.subTest(changed=changed),self.assertRaises(ValidationError):verify_security(root,root/'proposal/subject.json',receipt,**{**args,**changed})
            a=load_json(root,'security-assessment.json');a['payload']['controls'][0]['state']='PASS';a['payload']['readiness']={'state':'READY','reasons':[]}
            raw=json_bytes(a);write_bytes(root,'security-assessment.json',raw)
            # Even a newly supplied hash cannot make contradictory control proof valid.
            with self.assertRaises(ValidationError):verify_security(root,root/'proposal/subject.json',digest(raw),**args)

    def test_explicit_external_digest_and_missing_review_fail_closed(self):
        self.assertIsNotNone(importlib.util.find_spec('starbots_hybrid.security_bridge'),'Independent security verifier missing')
        from starbots_hybrid.security_bridge import verify_security
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(ValidationError):verify_security(t,Path(t)/'subject.json','0'*64,client_id='synthetic',project_id='fixture',as_of='2026-10-18T22:00:00Z')

    def test_wrong_proposal_cannot_be_accepted_without_original_bytes(self):
        self.assertIsNotNone(importlib.util.find_spec('starbots_hybrid.security_bridge'))
        from starbots_hybrid.security_bridge import verify_security
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);artifacts=[dict(path='proposal.json',role='proposal',sha256=digest(b'original'))]
            manifest=dict(subject_id='fixture',revision='1',client_id='synthetic',project_id='fixture',artifacts=artifacts)
            raw=json_bytes(manifest);write_bytes(root,'manifest.json',raw)
            s=envelope('SubjectRef','subject-fixture',dict(subject_id='fixture',revision='1',manifest_path='manifest.json',manifest_sha256=digest(raw),artifacts=artifacts),client_id='synthetic',project_id='fixture',created_at='2026-10-18T22:00:00Z')
            write_bytes(root,'subject.json',json_bytes(s));write_bytes(root,'proposal.json',b'modified')
            with self.assertRaises(ValidationError):verify_security(root/'review',root/'subject.json','0'*64,client_id='synthetic',project_id='fixture',as_of='2026-10-18T22:00:00Z')
