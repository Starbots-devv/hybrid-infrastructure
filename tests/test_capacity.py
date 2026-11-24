"""Capacity and local worker recovery checks for the synthetic examples."""

from pathlib import Path
import json
import unittest

from starbots_hybrid.capacity import assess
from starbots_hybrid.worker_recovery import LocalRecoveryDrill


ROOT = Path(__file__).resolve().parents[1] / "examples" / "flows" / "flow-01"


def fixture(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


class CapacityChecks(unittest.TestCase):
    def setUp(self):
        self.profile = fixture("profile.json")
        self.scenario = fixture("scenario-hybrid.json")

    def test_analytical_ceiling_respects_memory_connections_and_network(self):
        inputs = self.scenario["payload"]["capacity_inputs"]
        inputs.update(parallel_slots="8", available_memory_gib="2", required_memory_per_job_gib="1", service_time_seconds="2", max_db_connections="8", required_connections="10", network_capacity_mbps="9", target_network_mbps="10")
        result = assess(self.profile, self.scenario, "0" * 64, "offline-demo-1.0.0")
        self.assertEqual(result["estimated_capacity_rps"], "1")
        self.assertEqual(result["headroom_percent"], "0")
        self.assertEqual([(item["id"], item["state"]) for item in result["constraint_results"]], [
            ("model-throughput", "PASS"), ("model-db-connections", "FAIL"), ("model-network", "FAIL")])
        self.assertEqual(result["measured_or_estimated"], "estimated")
        strict = assess(self.profile, self.scenario, "0" * 64, "strict-analysis-1.0.0")
        self.assertEqual([item["state"] for item in strict["constraint_results"]], ["UNKNOWN"] * 3)

    def test_missing_service_inputs_are_unknown(self):
        self.scenario["payload"]["capacity_inputs"]["service_time_seconds"] = None
        result = assess(self.profile, self.scenario, "0" * 64, "offline-demo-1.0.0")
        self.assertIsNone(result["estimated_capacity_rps"])
        self.assertEqual(result["constraint_results"][0]["state"], "UNKNOWN")


class WorkerRecoveryChecks(unittest.TestCase):
    def test_lease_loss_retry_idempotency_backpressure_and_cloud_fallback(self):
        drill = LocalRecoveryDrill(queue_limit=2, lease_seconds=5, fallback_enabled=True)
        self.assertTrue(drill.submit("job-1", "one"))
        self.assertTrue(drill.submit("job-2", "two"))
        self.assertFalse(drill.submit("job-3", "three"))
        first = drill.lease("local")
        self.assertEqual(first.job_id, "job-1")
        self.assertTrue(drill.commit(first, "side-effect-1"))
        drill.fail_local()
        self.assertIsNone(drill.lease("local"))
        drill.advance(5)
        retry = drill.lease("cloud")
        self.assertEqual(retry.job_id, "job-1")
        self.assertEqual(retry.attempt, 2)
        self.assertFalse(drill.commit(retry, "duplicate-side-effect"))
        drill.ack(retry)
        second = drill.lease("cloud")
        self.assertEqual(second.job_id, "job-2")
        self.assertTrue(drill.commit(second, "side-effect-2"))
        drill.ack(second)
        self.assertEqual(drill.effects, {"job-1": "side-effect-1", "job-2": "side-effect-2"})
        self.assertEqual(drill.queue_depth, 0)
        self.assertEqual(drill.backpressure_rejections, 1)

    def test_fallback_must_be_explicitly_enabled(self):
        drill = LocalRecoveryDrill(queue_limit=1, lease_seconds=1, fallback_enabled=False)
        self.assertTrue(drill.submit("job-1", "one"))
        drill.fail_local()
        self.assertIsNone(drill.lease("cloud"))
        self.assertEqual(drill.queue_depth, 1)


if __name__ == "__main__":
    unittest.main()
