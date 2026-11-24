import copy
import csv
import importlib
import importlib.util
import io
import html
from pathlib import Path
import unittest
from starbots_hybrid.engine import analyze
from starbots_hybrid.io import json_bytes

ROOT=Path(__file__).resolve().parents[1]
class DossierTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('starbots_hybrid.dossier'),'Dossier is not implemented')
        self.d=importlib.import_module('starbots_hybrid.dossier')
        self.result=analyze(ROOT/'examples/hybrid-saving/bundle.json',as_of='2026-10-17T00:00:00Z')
    def test_complete_outputs_and_thirteen_populated_sections(self):
        r=self.d.populate(self.result);out=self.d.render(r)
        expected={'dossier.md','dossier.html','costs.csv','cashflow.csv','executive-summary.md','implementation-guide.md','architecture-current.svg','architecture-proposed.svg','shareable-summary.html','redaction-manifest.json'}
        self.assertEqual(set(out),expected)
        self.assertEqual([x['id'] for x in r['payload']['dossier_sections']],list(range(1,14)))
        self.assertTrue(all(x['paragraphs'] for x in r['payload']['dossier_sections']))
        self.assertEqual(json_bytes(self.result),json_bytes(analyze(ROOT/'examples/hybrid-saving/bundle.json',as_of='2026-10-17T00:00:00Z')))
    def test_every_line_amount_is_identical_across_formats(self):
        r=self.d.populate(self.result);out=self.d.render(r)
        rows=list(csv.DictReader(io.StringIO(out['costs.csv'].decode())))
        mdrows={}
        for raw in out['dossier.md'].decode().splitlines():
            if raw.startswith('| '):
                cells=[html.unescape(x.strip()) for x in raw.strip('|').split('|')]
                if len(cells)==5:mdrows[cells[0]]=cells
        for cost in r['payload']['costs']:
            for line in cost['lines']:
                key='|'.join([cost['scenario_id'],cost['view'],line['id'],line['period']])
                row=next(x for x in rows if x['row_id']==key)
                self.assertEqual(row['amount'],line['amount'] or 'UNKNOWN')
                self.assertEqual(mdrows[key][3],(line['amount'] if line['amount'] is not None else 'UNKNOWN — required input or evidence')+' / '+cost['currency'])
                self.assertIn(key.encode(),out['dossier.md']);self.assertIn(key.encode(),out['dossier.html'])
        self.assertIn(b'1440',out['executive-summary.md']);self.assertIn(b'6720',out['dossier.html'])
        self.assertIn(b'1200',out['implementation-guide.md'])
    def test_imported_markup_never_becomes_active_html_or_svg(self):
        r=copy.deepcopy(self.result);attack='<script>fetch("https://invalid.example")</script><img src=x onerror=alert(1)>'
        r['payload']['profile']['payload']['company_name']=attack
        r['payload']['scenarios'][1]['payload']['resource_nodes'][0]['service']=attack
        out=self.d.render(self.d.populate(r))
        for name in ('dossier.html','architecture-proposed.svg'):
            self.assertNotIn(b'<script',out[name]);self.assertNotIn(b'<img src=x',out[name]);self.assertIn(b'&lt;',out[name])
        self.assertNotIn(b'<script',out['dossier.md'])
    def test_csv_formula_payloads_with_hidden_prefix_are_neutralized(self):
        module=importlib.import_module('starbots_hybrid.renderers.csv')
        for value in ('=1+1','+SUM(1,1)','-1+2','@SUM(A1)',' \t=cmd','\ufeff\u200b=1','\r\n@cmd'):
            self.assertTrue(module.safe_cell(value).startswith("'"),repr(value))
    def test_shareable_allowlist_removes_identifiers_and_free_text(self):
        r=copy.deepcopy(self.result);r['client_id']='confidential-client';r['payload']['profile']['payload']['company_name']='CONFIDENTIAL_COMPANY'
        out=self.d.render(self.d.populate(r))
        for name in ('shareable-summary.html','redaction-manifest.json'):
            self.assertNotIn(b'confidential-client',out[name]);self.assertNotIn(b'CONFIDENTIAL_COMPANY',out[name])
        self.assertIn(b'SYNTHETIC DEMONSTRATION',out['shareable-summary.html'])
    def test_steps_keep_owner_parameters_validation_stop_and_required_inputs(self):
        out=self.d.render(self.d.populate(self.result))['implementation-guide.md'].decode()
        for step in self.result['payload']['scenarios'][1]['payload']['implementation_steps']:
            for key in ('owner','validation','stop_condition'):
                self.assertIn(step[key],out)
        self.assertIn('Required inputs',out);self.assertIn('Prerequisites',out)
        self.assertIn('Database hostname',out);self.assertIn('verify-full',out);self.assertIn('Queue visibility timeout seconds',out)
if __name__=='__main__':unittest.main()
