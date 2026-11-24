import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from starbots_hybrid.cli import main
from starbots_hybrid.io import load_json,verify_subject

ROOT=Path(__file__).resolve().parents[1]
class AnalysisCliTests(unittest.TestCase):
    def test_cli_exports_independent_verified_bundle_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as t:
            output=Path(t)/'Result with spaces á'
            args=['analyze','--bundle',str(ROOT/'examples/hybrid-saving/bundle.json'),'--as-of','2026-10-17T00:00:00Z','--output-dir',str(output)]
            with contextlib.redirect_stdout(io.StringIO()):self.assertEqual(main(args),0)
            evaluation=load_json(output,'evaluation.json');subject=load_json(output,'subject.json')
            verify_subject(output,subject,client_id=evaluation['client_id'],project_id=evaluation['project_id'])
            self.assertNotIn('evaluation.json',[x['path'] for x in subject['payload']['artifacts']])
            self.assertTrue(any(x['role']=='capacity' for x in subject['payload']['artifacts']))
            with contextlib.redirect_stdout(io.StringIO()):self.assertEqual(main(args),2)
            self.assertEqual(load_json(output,'evaluation.json'),evaluation)
    def test_validate_bundle_rejects_other_identity(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(['validate','--bundle',str(ROOT/'examples/hybrid-saving/bundle.json'),'--client-id','other']),2)
if __name__=='__main__':unittest.main()
