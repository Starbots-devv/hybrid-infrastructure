import copy
import importlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]

class DecisionTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('starbots_hybrid.economics'),'Offline economics is not implemented')
        self.e=importlib.import_module('starbots_hybrid.economics')
        self.engine=importlib.import_module('starbots_hybrid.engine')
        self.intake=importlib.import_module('starbots_hybrid.intake')
        self.io=importlib.import_module('starbots_hybrid.io')

    def result(self,**kw):
        return self.engine.analyze(ROOT/'examples/hybrid-saving/bundle.json',as_of='2026-10-17T00:00:00Z',**kw)

    def test_hybrid_golden_cash_tco_and_recovery(self):
        r=self.result();p=r['payload']
        self.assertEqual(p['recommendation']['scenario_id'],'hybrid')
        self.assertEqual(p['recommendation']['status'],'CONDITIONAL')
        self.assertFalse(p['execution_eligibility']['eligible'])
        golden={'incremental_cash':('220','1440','6720',6),'allocated_tco':('180','960','5280',7)}
        for view,expected in golden.items():
            row=next(x for x in p['comparable_economics'] if x['scenario_id']=='hybrid' and x['view']==view)
            self.assertEqual((row['monthly_saving'],row['net_12_months'],row['net_36_months'],row['break_even_month']),expected)

    def test_sensitivity_uses_horizon_net_results_instead_of_fixed_prose(self):
        saving=self.result()['payload']['sensitivity']
        cash12=next(x for x in saving if x['variable']=='hybrid / incremental_cash / 12 months')
        cash36=next(x for x in saving if x['variable']=='hybrid / incremental_cash / 36 months')
        tco12=next(x for x in saving if x['variable']=='hybrid / allocated_tco / 12 months')
        self.assertIn('USD 1440',cash12['condition'])
        self.assertIn('increases',cash12['condition'])
        self.assertIn('USD 6720',cash36['condition'])
        self.assertIn('USD 960',tco12['condition'])
        losing=self.engine.analyze(ROOT/'examples/flows/flow-02/bundle.json',as_of='2026-10-17T00:00:00Z')['payload']['sensitivity']
        loss12=next(x for x in losing if x['variable']=='hidden-costs / incremental_cash / 12 months')
        self.assertIn('USD 1600',loss12['condition'])
        self.assertIn('decreases',loss12['condition'])

    def test_cheaper_infeasible_alternative_cannot_win(self):
        p=self.result()['payload']
        bad=next(x for x in p['feasibility'] if x['scenario_id']=='local-only')
        self.assertEqual(bad['state'],'INFEASIBLE')
        self.assertNotEqual(p['recommendation']['scenario_id'],'local-only')

    def test_strict_policy_does_not_convert_synthetic_capacity_to_measurement(self):
        p=self.result(policy='strict-analysis-1.0.0')['payload']
        self.assertEqual(p['recommendation']['status'],'NONE')
        self.assertTrue(any(x['state']=='UNDEMONSTRATED' for x in p['feasibility']))

    def test_deterministic_without_network(self):
        with patch('socket.socket',side_effect=AssertionError('Offline means no network')):
            first=self.result();second=self.result()
        self.assertEqual(self.io.json_bytes(first),self.io.json_bytes(second))

    def test_capacity_is_service_rate_hypothesis_not_users(self):
        p=self.result()['payload'];c=next(x for x in p['capacities'] if x['scenario_id']=='hybrid')
        self.assertEqual(c['estimated_capacity_rps'],'2')
        self.assertEqual(c['headroom_percent'],'50')
        self.assertEqual(c['measured_or_estimated'],'estimated')
        self.assertTrue(c['assumptions'])

    def test_input_tamper_is_detected_before_evaluation(self):
        with tempfile.TemporaryDirectory() as t:
            d=Path(t)/'demo';shutil.copytree(ROOT/'examples/hybrid-saving',d)
            profile=json.loads((d/'profile.json').read_text());profile['payload']['company_name']='Changed requirements'
            (d/'profile.json').write_text(json.dumps(profile))
            with self.assertRaises(self.io.ValidationError):self.engine.analyze(d/'bundle.json',as_of='2026-10-17T00:00:00Z')
            self.intake.seal_bundle(d/'bundle.json')
            self.assertEqual(self.engine.analyze(d/'bundle.json',as_of='2026-10-17T00:00:00Z')['payload']['profile']['payload']['company_name'],'Changed requirements')

    def test_other_client_cannot_be_sealed_as_current_client(self):
        with tempfile.TemporaryDirectory() as t:
            d=Path(t)/'demo';shutil.copytree(ROOT/'examples/hybrid-saving',d)
            p=json.loads((d/'profile.json').read_text());p['client_id']='other-client';(d/'profile.json').write_text(json.dumps(p))
            with self.assertRaises(self.io.ValidationError):self.intake.seal_bundle(d/'bundle.json')

    def test_unknown_and_stale_prices_are_never_zero(self):
        snapshot=json.loads((ROOT/'examples/hybrid-saving/prices-hybrid.json').read_text())
        snapshot['payload']['lines'][0]['unit_rate']=None
        r=self.e.calculate_cost(snapshot,'hybrid','incremental_cash','2026-10-17T00:00:00Z')
        self.assertFalse(r['complete']);self.assertIsNone(r['monthly_total']);self.assertTrue(r['unknown_line_ids'])
        snapshot=json.loads((ROOT/'examples/hybrid-saving/prices-hybrid.json').read_text())
        r=self.e.calculate_cost(snapshot,'hybrid','incremental_cash','2026-12-01T00:00:00Z')
        self.assertFalse(r['complete']);self.assertIsNone(r['monthly_total']);self.assertTrue(r['stale_line_ids'])

    def test_negative_saving_zero_reference_and_incompatible_currencies(self):
        def cost(monthly,one_time='0',currency='USD'):
            return {'scenario_id':'x','view':'incremental_cash','currency':currency,'accounting_basis':'list','complete':True,'monthly_total':monthly,'one_time_total':one_time}
        r=self.e.compare(cost('260'),cost('305','600'),baseline_id='baseline',scenario_id='stay')
        self.assertEqual((r['monthly_saving'],r['net_12_months'],r['net_36_months'],r['break_even_month']),('-45','-1140','-2220',None))
        self.assertIsNone(self.e.compare(cost('0'),cost('10'),baseline_id='b',scenario_id='p')['saving_percent'])
        self.assertFalse(self.e.compare(cost('10'),cost('10',currency='EUR'),baseline_id='b',scenario_id='p')['comparable'])

    def test_currency_line_rounding_reconciles_without_float(self):
        snapshot=json.loads((ROOT/'examples/hybrid-saving/prices-hybrid.json').read_text())
        first=copy.deepcopy(snapshot['payload']['lines'][0]);first.update(id='tiny-1',allocation_id='tiny-1',quantity='1',unit_rate='0.005',period='monthly',view='both')
        second=copy.deepcopy(first);second.update(id='tiny-2',allocation_id='tiny-2')
        snapshot['payload']['lines']=[first,second]
        r=self.e.calculate_cost(snapshot,'tiny','incremental_cash','2026-10-17T00:00:00Z')
        self.assertEqual((r['monthly_total'],r['unrounded_monthly_total'],r['rounding_delta']),('0.02','0.01','0.01'))

    def test_hourly_rate_uses_declared_730_hour_month(self):
        snapshot=json.loads((ROOT/'examples/hybrid-saving/prices-hybrid.json').read_text())
        snapshot['payload']['period_definition']['kind']='fixed_730_hours'
        line=snapshot['payload']['lines'][0];line.update(quantity='2',unit='hour',unit_rate='0.1',period='hourly')
        snapshot['payload']['lines']=[line]
        self.assertEqual(self.e.calculate_cost(snapshot,'x','incremental_cash','2026-10-17T00:00:00Z')['monthly_total'],'146')

    def test_mandatory_profile_objective_cannot_be_relaxed_by_scenario(self):
        with tempfile.TemporaryDirectory() as t:
            d=Path(t)/'demo';shutil.copytree(ROOT/'examples/hybrid-saving',d)
            p=json.loads((d/'scenario-hybrid.json').read_text());p['payload']['constraint_requirements'][0]['mandatory']=False
            (d/'scenario-hybrid.json').write_text(json.dumps(p));self.intake.seal_bundle(d/'bundle.json')
            with self.assertRaises(self.io.ValidationError):self.engine.analyze(d/'bundle.json',as_of='2026-10-17T00:00:00Z')

    def test_bound_capacity_profile_cannot_be_reused_after_input_change(self):
        with tempfile.TemporaryDirectory() as t:
            d=Path(t)/'demo';shutil.copytree(ROOT/'examples/hybrid-saving',d)
            p=json.loads((d/'scenario-hybrid.json').read_text());p['payload']['required_capacity_profile_digest']='0'*64
            (d/'scenario-hybrid.json').write_bytes(self.io.json_bytes(p))
            b=json.loads((d/'bundle.json').read_text());b['scenarios'][1]['sha256']=self.io.digest(self.io.json_bytes(p));(d/'bundle.json').write_bytes(self.io.json_bytes(b))
            with self.assertRaises(self.io.ValidationError):self.engine.analyze(d/'bundle.json',as_of='2026-10-17T00:00:00Z')

    def test_failed_mandatory_security_cannot_enter_conditional_shortlist(self):
        with tempfile.TemporaryDirectory() as t:
            d=Path(t)/'demo';shutil.copytree(ROOT/'examples/hybrid-saving',d)
            p=json.loads((d/'scenario-hybrid.json').read_text());p['payload']['constraint_requirements'].append(dict(id='encryption',dimension='security',mandatory=True,rule='equals',threshold=True,observation=dict(value=False,evidence_level='synthetic',evidence_refs=[]),rationale='Required encryption'))
            (d/'scenario-hybrid.json').write_bytes(self.io.json_bytes(p));self.intake.seal_bundle(d/'bundle.json')
            result=self.engine.analyze(d/'bundle.json',as_of='2026-10-17T00:00:00Z')
            self.assertNotEqual(result['payload']['recommendation']['scenario_id'],'hybrid')

    def test_repeated_resource_action_groups_cannot_hide_conflicts(self):
        with tempfile.TemporaryDirectory() as t:
            d=Path(t)/'demo';shutil.copytree(ROOT/'examples/hybrid-saving',d)
            p=json.loads((d/'scenario-hybrid.json').read_text());p['payload']['action_groups'].append(dict(resource_id='compute',actions=['stop']))
            (d/'scenario-hybrid.json').write_bytes(self.io.json_bytes(p));self.intake.seal_bundle(d/'bundle.json')
            with self.assertRaises(self.io.ValidationError):self.engine.analyze(d/'bundle.json',as_of='2026-10-17T00:00:00Z')

    def test_bundle_transport_types_fail_closed(self):
        with tempfile.TemporaryDirectory() as t:
            d=Path(t)/'demo';shutil.copytree(ROOT/'examples/hybrid-saving',d)
            b=json.loads((d/'bundle.json').read_text());b['security_assessments']={}
            (d/'bundle.json').write_bytes(self.io.json_bytes(b))
            with self.assertRaises(self.io.ValidationError):self.intake.load_bundle(d/'bundle.json')

    def test_different_price_periods_are_not_comparable(self):
        with tempfile.TemporaryDirectory() as t:
            d=Path(t)/'demo';shutil.copytree(ROOT/'examples/hybrid-saving',d)
            p=json.loads((d/'prices-hybrid.json').read_text());p['payload']['period_definition']['start_month']='2026-11'
            (d/'prices-hybrid.json').write_bytes(self.io.json_bytes(p));self.intake.seal_bundle(d/'bundle.json')
            with self.assertRaises(self.io.ValidationError):self.engine.analyze(d/'bundle.json',as_of='2026-10-17T00:00:00Z')

if __name__=='__main__':unittest.main()
