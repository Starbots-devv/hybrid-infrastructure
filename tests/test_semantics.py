import copy
import json
from pathlib import Path
import unittest
from starbots_hybrid.contracts import validate
from starbots_hybrid.io import ValidationError

class SemanticTests(unittest.TestCase):
    def test_negative_resource_quantity_and_rate_are_invalid(self):
        r=Path(__file__).resolve().parents[1]/'examples/contracts'
        scenario=json.loads((r/'Scenario.json').read_text())
        scenario['payload']['resource_nodes'][0]['quantity']='-1'
        with self.assertRaises(ValidationError):validate(scenario)
        prices=json.loads((r/'CostSnapshot.json').read_text());prices['payload']['lines'][0]['unit_rate']='-1'
        with self.assertRaises(ValidationError):validate(prices)

if __name__=='__main__':unittest.main()
