"""Independent arithmetic oracles for the 36-month decision series."""
import unittest
import copy
import json
from pathlib import Path
import shutil
import tempfile

from starbots_hybrid.economics import compare
from starbots_hybrid.finops import calculate_series
from starbots_hybrid import dossier, engine, intake
from starbots_hybrid.io import json_bytes

FIXTURE = Path(__file__).resolve().parents[1] / "examples/hybrid-saving/prices-hybrid.json"


def row(monthly, one_time="0"):
    return {
        "scenario_id": "example", "view": "incremental_cash", "currency": "USD",
        "accounting_basis": "list", "complete": True,
        "monthly_total": monthly, "one_time_total": one_time,
    }


class FinOpsSeriesTests(unittest.TestCase):
    def test_malformed_identifiers_fail_with_validation_error(self):
        from starbots_hybrid.io import ValidationError
        snapshot = json.loads(FIXTURE.read_text())
        base = {
            'format': 'starbots-finops-1', 'scenario_id': 'p',
            'client_id': snapshot['client_id'], 'project_id': snapshot['project_id'],
            'observed_at': '2026-10-17T00:00:00Z',
            'valid_until': '2026-11-01T00:00:00Z', 'currency': 'USD',
            'start_month': '2026-10', 'tax_status': 'pre_tax_unknown',
            'source_uri': 'synthetic://bad-input', 'line_rules': [], 'promotions': [],
        }
        cases = [
            {'line_rules': [{'line_id': ['compute'], 'segments': [{'first': 1, 'last': 1}]}]},
            {'asset_rules': [{'resource_id': ['hardware'], 'purchase_line_id': None,
                              'depreciation_line_id': 'hardware', 'purchase_cost': '1440',
                              'residual_value': '0', 'life_months': 36}]},
            {'promotions': [{'id': 'credit', 'pool_id': 'pool', 'first': 1, 'last': 1,
                             'monthly_cap': '1', 'pool_total': '1',
                             'eligible_line_ids': [['compute']]}]},
        ]
        for changed in cases:
            with self.subTest(changed=changed), self.assertRaises(ValidationError):
                calculate_series(snapshot, 'p', 'incremental_cash',
                                 '2026-10-17T00:00:00Z', {**base, **changed})

    def test_owned_asset_depreciation_is_checked_and_purchase_cannot_be_recounted(self):
        snapshot=copy.deepcopy(json.loads(FIXTURE.read_text()))
        plan={'format':'starbots-finops-1','scenario_id':'p','client_id':snapshot['client_id'],
              'project_id':snapshot['project_id'],'observed_at':'2026-10-17T00:00:00Z',
              'valid_until':'2026-11-01T00:00:00Z','currency':'USD','start_month':'2026-10',
              'tax_status':'pre_tax_unknown','source_uri':'synthetic://asset','line_rules':[],
              'promotions':[], 'asset_rules':[{'resource_id':'hardware','purchase_line_id':None,
                  'depreciation_line_id':'hardware','purchase_cost':'1440','residual_value':'0','life_months':36}]}
        cost,_=calculate_series(snapshot,'p','allocated_tco','2026-10-17T00:00:00Z',plan)
        self.assertEqual(cost['monthly_total'],'540')
        purchase=copy.deepcopy(next(x for x in snapshot['payload']['lines'] if x['id']=='hardware'))
        purchase.update(id='hardware-purchase',allocation_id='hardware-purchase',view='both',
                        period='one_time',unit='one_time',unit_rate='1440')
        snapshot['payload']['lines'].append(purchase)
        plan['asset_rules'][0]['purchase_line_id']='hardware-purchase'
        from starbots_hybrid.io import ValidationError
        with self.assertRaises(ValidationError):
            calculate_series(snapshot,'p','allocated_tco','2026-10-17T00:00:00Z',plan)

    def test_declared_dated_fx_pair_converts_only_matching_lines(self):
        snapshot=copy.deepcopy(json.loads(FIXTURE.read_text()))
        line=snapshot['payload']['lines'][0]
        line.update(currency='EUR',unit_rate='100',quantity='1',period='monthly',view='both')
        snapshot['payload']['lines']=[line]
        plan={'format':'starbots-finops-1','scenario_id':'p','client_id':snapshot['client_id'],
              'project_id':snapshot['project_id'],'observed_at':'2026-10-17T00:00:00Z',
              'valid_until':'2026-11-01T00:00:00Z','currency':'USD','start_month':'2026-10',
              'tax_status':'pre_tax_unknown','source_uri':'synthetic://fx-plan','line_rules':[],
              'promotions':[], 'fx':{'version':'1.0.0','from_currency':'EUR','to_currency':'USD',
               'direction':'multiply','rate':'1.1','spread_percent':'0',
               'observed_at':'2026-10-17T00:00:00Z','valid_until':'2026-11-01T00:00:00Z',
               'source_uri':'synthetic://fx-rate'}}
        cost,months=calculate_series(snapshot,'p','incremental_cash','2026-10-17T00:00:00Z',plan)
        self.assertEqual((cost['currency'],cost['monthly_total'],months[35]),('USD','110','110'))
        plan['fx']['valid_until']='2026-10-17T00:00:00Z'
        from starbots_hybrid.io import ValidationError
        with self.assertRaises(ValidationError):calculate_series(snapshot,'p','incremental_cash','2026-10-17T00:00:00Z',plan)

    def test_overlapping_promotion_pools_cannot_discount_twice(self):
        snapshot = copy.deepcopy(json.loads(FIXTURE.read_text()))
        line=snapshot['payload']['lines'][0]
        line.update(unit_rate='100', quantity='1', period='monthly', view='both')
        snapshot['payload']['lines']=[line]
        plan={'format':'starbots-finops-1','scenario_id':'p','client_id':snapshot['client_id'],
              'project_id':snapshot['project_id'],'observed_at':'2026-10-17T00:00:00Z',
              'valid_until':'2026-11-01T00:00:00Z','currency':'USD','start_month':'2026-10',
              'tax_status':'pre_tax_unknown','source_uri':'synthetic://credits','line_rules':[],
              'promotions':[{'id':name,'pool_id':name,'first':1,'last':1,'monthly_cap':'100',
                             'pool_total':'100','eligible_line_ids':[line['id']]} for name in ('a','b')]}
        _,months=calculate_series(snapshot,'p','incremental_cash','2026-10-17T00:00:00Z',plan)
        self.assertEqual(months[0],'0')

    def test_calendar_month_hourly_rate_uses_actual_days(self):
        snapshot=copy.deepcopy(json.loads(FIXTURE.read_text()))
        snapshot['payload']['period_definition']['kind']='calendar_month'
        line=snapshot['payload']['lines'][0]
        line.update(quantity='2',unit='hour',unit_rate='0.1',period='hourly')
        snapshot['payload']['lines']=[line]
        plan={'format':'starbots-finops-1','scenario_id':'p','client_id':snapshot['client_id'],
              'project_id':snapshot['project_id'],'observed_at':'2026-10-17T00:00:00Z',
              'valid_until':'2026-11-01T00:00:00Z','currency':'USD','start_month':'2026-10',
              'tax_status':'pre_tax_unknown','source_uri':'synthetic://hours','line_rules':[],
              'promotions':[]}
        cost,months=calculate_series(snapshot,'p','incremental_cash','2026-10-17T00:00:00Z',plan)
        self.assertEqual((cost['monthly_total'],months[1]),('148.8','144'))

    def test_shared_promotion_pool_exhausts_and_cannot_make_cost_negative(self):
        snapshot = copy.deepcopy(json.loads(FIXTURE.read_text()))
        line = snapshot['payload']['lines'][0]
        line.update(unit_rate='100', quantity='1', period='monthly', view='both')
        snapshot['payload']['lines'] = [line]
        plan = {
            'format': 'starbots-finops-1', 'scenario_id': 'p',
            'client_id': snapshot['client_id'], 'project_id': snapshot['project_id'],
            'observed_at': '2026-10-17T00:00:00Z', 'valid_until': '2026-11-01T00:00:00Z',
            'currency': 'USD', 'start_month': '2026-10', 'tax_status': 'pre_tax_unknown',
            'source_uri': 'synthetic://pool', 'line_rules': [],
            'promotions': [{'id': 'intro', 'pool_id': 'account-credit', 'first': 1, 'last': 3,
                            'monthly_cap': '60', 'pool_total': '100', 'eligible_line_ids': [line['id']]}],
        }
        cost, months = calculate_series(snapshot, 'p', 'incremental_cash', '2026-10-17T00:00:00Z', plan)
        self.assertEqual(months[:4], ['40', '60', '100', '100'])
        self.assertEqual(cost['monthly_total'], '40')

    def test_marginal_tiers_growth_and_minimum_are_explicit(self):
        snapshot = copy.deepcopy(json.loads(FIXTURE.read_text()))
        line = snapshot['payload']['lines'][0]
        line.update(unit_rate='1', quantity='10', period='monthly', view='both')
        snapshot['payload']['lines'] = [line]
        plan = {
            'format': 'starbots-finops-1', 'scenario_id': 'p',
            'client_id': snapshot['client_id'], 'project_id': snapshot['project_id'],
            'observed_at': '2026-10-17T00:00:00Z', 'valid_until': '2026-11-01T00:00:00Z',
            'currency': 'USD', 'start_month': '2026-10', 'tax_status': 'pre_tax_unknown',
            'source_uri': 'synthetic://tier', 'promotions': [],
            'line_rules': [{'line_id': line['id'], 'segments': [
                {'first': 1, 'last': 2, 'quantity': '10', 'growth_percent': '10',
                 'tiers': [{'through': '5', 'unit_rate': '2'}, {'through': None, 'unit_rate': '1'}],
                 'minimum': '12'}]}],
        }
        cost, months = calculate_series(snapshot, 'p', 'incremental_cash', '2026-10-17T00:00:00Z', plan)
        self.assertEqual(months[:3], ['15', '16', '10'])
        self.assertEqual(cost['lines'][0]['amount'], '15')

    def test_versioned_bundle_binds_finops_plans_and_uses_monthly_series(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / 'demo'
            shutil.copytree(FIXTURE.parent, destination)
            bundle = json.loads((destination / 'bundle.json').read_text())
            bundle['schema_version'] = '1.1.0'
            bundle['finops'] = {}
            for scenario in ('current', 'hybrid', 'local-only'):
                snapshot = json.loads((destination / ('prices-' + scenario + '.json')).read_text())
                rules = ([{'line_id': 'compute', 'segments': [{'first': 1, 'last': 3, 'unit_rate': '40'}]}]
                         if scenario == 'hybrid' else [])
                plan = {
                    'format': 'starbots-finops-1', 'scenario_id': scenario,
                    'client_id': snapshot['client_id'], 'project_id': snapshot['project_id'],
                    'observed_at': '2026-10-17T00:00:00Z', 'valid_until': '2026-11-01T00:00:00Z',
                    'currency': 'USD', 'start_month': '2026-10', 'tax_status': 'pre_tax_unknown',
                    'source_uri': 'synthetic://finops/' + scenario, 'line_rules': rules, 'promotions': [],
                }
                name = 'finops-' + scenario + '.json'
                (destination / name).write_bytes(json_bytes(plan))
                bundle['finops'][scenario] = {'path': name, 'sha256': '0' * 64}
            (destination / 'bundle.json').write_bytes(json_bytes(bundle))
            intake.seal_bundle(destination / 'bundle.json')
            result = engine.analyze(destination / 'bundle.json', as_of='2026-10-17T00:00:00Z')
            self.assertEqual(len([x for x in result['payload']['input_manifest'] if x['role'] == 'finops-plan']), 3)
            cash = next(x for x in result['payload']['comparable_economics'] if x['scenario_id'] == 'hybrid' and x['view'] == 'incremental_cash')
            self.assertEqual(cash['monthly_series'][0]['proposed'], '440')
            self.assertEqual(cash['monthly_series'][3]['proposed'], '500')
            rendered=dossier.render(result)
            self.assertIn('cashflow.csv',rendered)
            self.assertIn('hybrid,incremental_cash,4,720,500,220',rendered['cashflow.csv'].decode())
            self.assertIn('Month 36',rendered['dossier.md'].decode())
            self.assertIn('Month 36',rendered['dossier.html'].decode())

    def test_expiring_promotion_is_calculated_from_hashable_inputs(self):
        snapshot = copy.deepcopy(json.loads(FIXTURE.read_text()))
        line = snapshot["payload"]["lines"][0]
        line.update(unit_rate="110", quantity="1", period="monthly", view="both")
        snapshot["payload"]["lines"] = [line]
        plan = {
            "format": "starbots-finops-1", "scenario_id": "proposed",
            "client_id": snapshot["client_id"], "project_id": snapshot["project_id"],
            "observed_at": "2026-10-17T00:00:00Z", "valid_until": "2026-11-01T00:00:00Z",
            "currency": "USD", "start_month": "2026-10", "tax_status": "pre_tax_unknown",
            "source_uri": "synthetic://finops/promotion", "line_rules": [
                {"line_id": line["id"], "segments": [
                    {"first": 1, "last": 3, "unit_rate": "40"}
                ]}
            ], "promotions": []
        }
        cost, months = calculate_series(snapshot, "proposed", "incremental_cash", "2026-10-17T00:00:00Z", plan)
        self.assertEqual((cost["monthly_total"], months[:4]), ("40", ["40", "40", "40", "110"]))

    def test_promotion_expires_and_reverses_earlier_saving(self):
        result = compare(
            row("100"), row("40", "60"), baseline_id="current", scenario_id="proposed",
            baseline_series=["100"] * 36,
            proposed_series=["40"] * 3 + ["110"] * 33,
        )
        self.assertEqual(result["net_12_months"], "30")
        self.assertEqual(result["net_36_months"], "-210")
        self.assertEqual(result["break_even_month"], 1)
        self.assertEqual(result["monthly_series"][3]["saving"], "-10")
        self.assertEqual(result["monthly_series"][35]["cumulative_net"], "-210")

    def test_growth_reverses_twelve_month_winner(self):
        result = compare(
            row("600"), row("450", "600"), baseline_id="current", scenario_id="proposed",
            baseline_series=["600"] * 36,
            proposed_series=["450"] * 12 + ["750"] * 24,
        )
        self.assertEqual((result["net_12_months"], result["net_36_months"]), ("1200", "-2400"))

    def test_residual_commitment_is_paid_even_after_replacement(self):
        result = compare(
            row("100"), row("160"), baseline_id="current", scenario_id="proposed",
            baseline_series=["100"] * 36,
            proposed_series=["160"] * 6 + ["60"] * 30,
        )
        self.assertEqual(result["monthly_series"][0]["saving"], "-60")
        self.assertEqual(result["monthly_series"][6]["saving"], "40")

    def test_incomplete_or_wrong_length_series_cannot_rank(self):
        result = compare(row("100"), row("60"), baseline_id="current", scenario_id="proposed",
                         baseline_series=["100"] * 36, proposed_series=["60"] * 35)
        self.assertFalse(result["comparable"])
        self.assertIsNone(result["net_36_months"])
        sensitivity=engine._sensitivity([result], 'current')
        self.assertEqual(len(sensitivity), 3)
        self.assertTrue(all('No numeric' in entry['effect'] for entry in sensitivity[:2]))

    def test_zero_net_has_no_fake_positive_sensitivity(self):
        result=compare(row("100"),row("100"),baseline_id="current",scenario_id="proposed")
        sensitivity=engine._sensitivity([result], 'current')
        self.assertIn('net result is zero',sensitivity[0]['condition'])
        self.assertIn('net loss',sensitivity[0]['effect'])


if __name__ == "__main__":
    unittest.main()
