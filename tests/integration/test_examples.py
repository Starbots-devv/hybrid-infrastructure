"""Reproducible CLI checks for the three explicitly synthetic flows."""

import json
import os
from hashlib import sha256
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
import starbots_hybrid


ROOT = Path(__file__).resolve().parents[2]
FLOWS = ROOT / "examples" / "flows"
AS_OF = "2026-10-17T00:00:00Z"


def _run(*args):
    return subprocess.run(
        [sys.executable, "-m", "starbots_hybrid.cli", *map(str, args)],
        capture_output=True,
        text=True,
        cwd=ROOT,
        env={**os.environ, "PYTHONPATH": str(Path(starbots_hybrid.__file__).resolve().parents[1])},
        check=False,
    )


def _analyze(flow, output):
    bundle = FLOWS / flow / "bundle.json"
    result = _run("validate", "--bundle", bundle)
    assert result.returncode == 0, result.stdout + result.stderr
    result = _run("analyze", "--bundle", bundle, "--as-of", AS_OF, "--output-dir", output)
    assert result.returncode == 0, result.stdout + result.stderr
    required = {"evaluation.json", "subject.json", "subject-manifest.json", "artifact-manifest.json", "dossier.md", "dossier.html", "costs.csv", "cashflow.csv", "executive-summary.md", "implementation-guide.md"}
    assert required.issubset({item.name for item in output.iterdir()})
    manifest = json.loads((output / "artifact-manifest.json").read_text(encoding="utf-8"))
    for artifact in manifest["artifacts"]:
        assert sha256((output / artifact["path"]).read_bytes()).hexdigest() == artifact["sha256"]
    return json.loads((output / "evaluation.json").read_text(encoding="utf-8"))["payload"]


def _comparison(payload, scenario, view):
    return next(
        item for item in payload["comparable_economics"]
        if item["scenario_id"] == scenario and item["view"] == view
    )


def _cost(payload, scenario, view):
    return next(
        item for item in payload["costs"]
        if item["scenario_id"] == scenario and item["view"] == view
    )


class ExampleFlows(unittest.TestCase):
    def test_flow_01_exact_cash_and_tco_oracles(self):
        with tempfile.TemporaryDirectory() as directory:
            payload = _analyze("flow-01", Path(directory) / "flow-01")
        self.assertTrue(payload["synthetic"])
        self.assertEqual(_cost(payload, "current", "incremental_cash")["monthly_total"], "720")
        self.assertEqual(_cost(payload, "hybrid", "incremental_cash")["monthly_total"], "500")
        self.assertEqual(_cost(payload, "hybrid", "allocated_tco")["monthly_total"], "540")
        for view, expected in {
            "incremental_cash": ("1440", "6720", 6),
            "allocated_tco": ("960", "5280", 7),
        }.items():
            row = _comparison(payload, "hybrid", view)
            self.assertEqual((row["incremental_investment"], row["net_12_months"], row["net_36_months"], row["break_even_month"]), ("1200", *expected))
            self.assertEqual(len(row["monthly_series"]), 36)
        self.assertEqual(payload["recommendation"]["scenario_id"], "hybrid")
        self.assertEqual(payload["recommendation"]["status"], "CONDITIONAL")
        self.assertFalse(payload["execution_eligibility"]["eligible"])
        local_only = next(item for item in payload["feasibility"] if item["scenario_id"] == "local-only")
        self.assertEqual(local_only["state"], "INFEASIBLE")

    def test_flow_02_hidden_costs_reverse_the_apparent_saving(self):
        with tempfile.TemporaryDirectory() as directory:
            payload = _analyze("flow-02", Path(directory) / "flow-02")
        baseline = _cost(payload, "current", "incremental_cash")
        proposed = _cost(payload, "hidden-costs", "incremental_cash")
        self.assertEqual(baseline["monthly_total"], "520")
        self.assertEqual(proposed["monthly_total"], "620")
        amounts = {item["id"]: item["amount"] for item in proposed["lines"]}
        self.assertEqual(sum(int(amounts[key]) for key in ("compute", "db", "network", "observability")), 290)
        self.assertEqual(tuple(amounts[key] for key in ("transfer", "operations", "power", "fallback")), ("110", "80", "65", "75"))
        row = _comparison(payload, "hidden-costs", "incremental_cash")
        self.assertEqual((row["incremental_investment"], row["net_12_months"], row["net_36_months"], row["break_even_month"]), ("400", "-1600", "-4000", None))
        self.assertEqual(len(row["monthly_series"]), 36)
        self.assertEqual(payload["recommendation"]["scenario_id"], "current")

    def test_flow_03_stay_on_managed_service(self):
        with tempfile.TemporaryDirectory() as directory:
            payload = _analyze("flow-03", Path(directory) / "flow-03")
        self.assertEqual(_cost(payload, "current", "incremental_cash")["monthly_total"], "260")
        proposed = _cost(payload, "vm", "incremental_cash")
        self.assertEqual(proposed["monthly_total"], "305")
        self.assertEqual(tuple(item["amount"] for item in proposed["lines"] if item["period"] == "monthly"), ("120", "60", "125"))
        row = _comparison(payload, "vm", "incremental_cash")
        self.assertEqual((row["incremental_investment"], row["net_12_months"], row["net_36_months"], row["break_even_month"]), ("600", "-1140", "-2220", None))
        self.assertEqual(payload["recommendation"]["scenario_id"], "current")

    def test_capacity_and_residency_failures_remove_hybrid_from_shortlist(self):
        for change, expected in (("capacity", "model-throughput"), ("residency", "eu-residency")):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as directory:
                bundle_root = Path(directory) / "input"
                shutil.copytree(FLOWS / "flow-01", bundle_root)
                scenario_path = bundle_root / "scenario-hybrid.json"
                scenario = json.loads(scenario_path.read_text(encoding="utf-8"))
                if change == "capacity":
                    scenario["payload"]["capacity_inputs"]["parallel_slots"] = "1"
                else:
                    residency = next(item for item in scenario["payload"]["constraint_requirements"] if item["id"] == "eu-residency")
                    residency["observation"]["value"] = "Outside EU"
                scenario_path.write_text(json.dumps(scenario), encoding="utf-8")
                sealed = _run("seal-bundle", "--bundle", bundle_root / "bundle.json")
                self.assertEqual(sealed.returncode, 0, sealed.stdout + sealed.stderr)
                result = _run("analyze", "--bundle", bundle_root / "bundle.json", "--as-of", AS_OF, "--output-dir", Path(directory) / "output")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                payload = json.loads((Path(directory) / "output" / "evaluation.json").read_text(encoding="utf-8"))["payload"]
                feasibility = next(item for item in payload["feasibility"] if item["scenario_id"] == "hybrid")
                self.assertEqual(feasibility["state"], "INFEASIBLE")
                self.assertTrue(any(item["id"] == expected and item["state"] == "FAIL" for item in feasibility["constraints"]))
                self.assertNotEqual(payload["recommendation"]["scenario_id"], "hybrid")

    def test_strict_policy_keeps_unmeasured_capacity_unknown(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "strict"
            result = _run("analyze", "--bundle", FLOWS / "flow-01" / "bundle.json", "--as-of", AS_OF, "--output-dir", output, "--policy", "strict-analysis-1.0.0")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads((output / "evaluation.json").read_text(encoding="utf-8"))["payload"]
            self.assertEqual(payload["recommendation"]["status"], "NONE")
            self.assertIsNone(payload["recommendation"]["scenario_id"])
            self.assertTrue(all(item["state"] == "UNKNOWN" for row in payload["capacities"] for item in row["constraint_results"]))


if __name__ == "__main__":
    unittest.main()
