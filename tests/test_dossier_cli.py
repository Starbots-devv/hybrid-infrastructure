import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from starbots_hybrid.cli import main
from starbots_hybrid.io import load_json,read_bytes,verify_ref

ROOT=Path(__file__).resolve().parents[1]
class DossierCliTests(unittest.TestCase):
    def test_custom_bundle_filename_is_preserved_for_regeneration(self):
        import shutil
        with tempfile.TemporaryDirectory() as t:
            inputs=Path(t)/'inputs';shutil.copytree(ROOT/'examples/hybrid-saving',inputs)
            (inputs/'bundle.json').rename(inputs/'fictional-company.json')
            a=Path(t)/'a';b=Path(t)/'b'
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(['analyze','--bundle',str(inputs/'fictional-company.json'),'--as-of','2026-10-17T00:00:00Z','--output-dir',str(a)]),0)
                self.assertEqual(main(['dossier','--evaluation',str(a/'evaluation.json'),'--output-dir',str(b)]),0)
    def test_proposal_subject_identity_does_not_depend_on_result_identity(self):
        import copy
        from starbots_hybrid.engine import analyze
        from starbots_hybrid.intake import load_bundle
        from starbots_hybrid.output import export_analysis
        bundle=ROOT/'examples/hybrid-saving/bundle.json';data=load_bundle(bundle)
        result=analyze(bundle,as_of='2026-10-17T00:00:00Z');changed=copy.deepcopy(result);changed['id']='a-different-report'
        with tempfile.TemporaryDirectory() as t:
            a=Path(t)/'a';b=Path(t)/'b';export_analysis(data,result,a);export_analysis(data,changed,b)
            self.assertEqual(read_bytes(a,'subject-manifest.json'),read_bytes(b,'subject-manifest.json'))
            self.assertEqual(read_bytes(a,'subject.json'),read_bytes(b,'subject.json'))
    def test_regeneration_preserves_result_and_all_manifest_bytes_without_reanalysis(self):
        with tempfile.TemporaryDirectory() as t:
            first=Path(t)/'first';second=Path(t)/'second'
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(['analyze','--bundle',str(ROOT/'examples/hybrid-saving/bundle.json'),'--as-of','2026-10-17T00:00:00Z','--output-dir',str(first)]),0)
                with patch('starbots_hybrid.engine.analyze',side_effect=AssertionError('Dossier must not reanalyze')):
                    self.assertEqual(main(['dossier','--evaluation',str(first/'evaluation.json'),'--output-dir',str(second),'--audience','both']),0)
            for ref in load_json(first,'artifact-manifest.json')['artifacts']:
                verify_ref(second,ref)
            self.assertEqual(read_bytes(first,'artifact-manifest.json'),read_bytes(second,'artifact-manifest.json'))
            (first/'dossier.html').write_text('tampered')
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(['dossier','--evaluation',str(first/'evaluation.json'),'--output-dir',str(Path(t)/'third')]),2)
            self.assertFalse((Path(t)/'third').exists())
if __name__=='__main__':unittest.main()
