"""Reproducibility and sensitivity stress test — policy only, no model inference."""
from __future__ import annotations
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "watchdog"))
from sensitivity import evaluate, fixture_family, candidate_policies  # noqa: E402


class SensitivityTests(unittest.TestCase):
    def test_deterministic_given_seed(self):
        a = fixture_family(2026, 2)
        b = fixture_family(2026, 2)
        self.assertEqual(a, b)

    def test_different_seeds_change_observations(self):
        a = fixture_family(2026, 1)
        b = fixture_family(2027, 1)
        self.assertNotEqual(a, b)

    def test_timing_always_increases(self):
        for scenario in fixture_family(2026, 4):
            times = [e.elapsed_seconds for e in scenario.events]
            self.assertEqual(times, sorted(set(times)))

    def test_no_anomaly_labels_leak_to_model_inputs(self):
        # The input to replay_one is SessionCounters; hidden oracle fields
        # are only on Scenario and must not enter the policy's decide().
        case = fixture_family(2026, 1)[0]
        self.assertFalse(hasattr(case.events[0], "anomaly_onset"))
        self.assertFalse(hasattr(case.events[0], "category"))

    def test_splits_and_counting(self):
        summary = evaluate(repeats=2)
        self.assertEqual(set(summary["results"]), {"development", "holdout"})
        self.assertEqual(summary["base_scenarios"], 10)
        self.assertEqual(summary["repeats_per_base_scenario"], 2)
        for split in summary["results"].values():
            self.assertEqual(set(split), set(candidate_policies()))
            for row in split.values():
                self.assertEqual(row["positive_traces"], 12)
                self.assertEqual(row["negative_traces"], 8)
                self.assertLessEqual(row["detected_traces"], row["positive_traces"])
                self.assertLessEqual(row["negative_traces_with_alert"], row["negative_traces"])

    def test_policy_not_claimed_as_agent_result(self):
        summary = evaluate(repeats=1)
        self.assertIn("not an LLM", summary["status"])
        self.assertIn("SAME author-designed", summary["caveat"])

    def test_safety_signal_not_suppressed(self):
        for split in evaluate(repeats=3)["results"].values():
            # All 3 'unsafe_operation' fixtures trigger a halt regardless
            # of ordinary interval thresholds; all detected >=3.
            for row in split.values():
                self.assertGreaterEqual(row["detected_traces"], 3)

    def test_invalid_repeats(self):
        with self.assertRaises(ValueError):
            evaluate(repeats=0)
        with self.assertRaises(ValueError):
            evaluate(repeats=301)

    def test_holdout_seed_must_be_distinct(self):
        with self.assertRaises(ValueError):
            evaluate(repeats=1, development_seed=3, holdout_seed=3)


if __name__ == "__main__":
    unittest.main()
