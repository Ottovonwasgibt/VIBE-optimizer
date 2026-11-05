"""Checkpoint-watchdog policy tests, no host/model integration."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from vibe_optimizer.checkpoint_watchdog import (
    CheckpointPolicy, SessionCounters, decide, make_restart_packet,
)


class CheckpointPolicyTests(unittest.TestCase):
    def test_default_continue(self):
        d = decide(SessionCounters())
        self.assertEqual(d.action, "continue")
        self.assertEqual(d.reasons, ())

    def test_clock_interval(self):
        d = decide(SessionCounters(elapsed_seconds=1200))
        self.assertEqual(d.action, "review")
        self.assertIn("time_interval", d.reasons)

    def test_tool_interval(self):
        d = decide(SessionCounters(tool_calls=25))
        self.assertEqual(d.action, "review")
        self.assertIn("tool_call_interval", d.reasons)

    def test_repeat_failure(self):
        d = decide(SessionCounters(consecutive_failures=3))
        self.assertEqual(d.action, "review")
        self.assertIn("repeat_failure", d.reasons)

    def test_no_progress(self):
        d = decide(SessionCounters(actions_without_verified_progress=18))
        self.assertEqual(d.action, "review")
        self.assertIn("unverified_progress_stall", d.reasons)

    def test_tool_drift_only_when_tool_fits(self):
        self.assertEqual(decide(SessionCounters(fallback_tool_streak=7)).action,
                         "continue")
        d = decide(SessionCounters(fallback_tool_streak=7, tool_fit_evidence=True))
        self.assertEqual(d.action, "review")
        self.assertIn("suitable_tool_unused", d.reasons)

    def test_handoff_context_pressure(self):
        d = decide(SessionCounters(context_fraction=0.86))
        self.assertEqual(d.action, "handoff")
        self.assertIn("context_pressure", d.reasons)

    def test_safety_halt_takes_precedence(self):
        d = decide(SessionCounters(
            unsafe_operation_detected=True, context_fraction=0.99))
        self.assertEqual(d.action, "halt")

    def test_defer_in_critical_action(self):
        d = decide(SessionCounters(
            tool_calls=25, currently_in_critical_action=True))
        self.assertEqual(d.action, "continue")
        self.assertIn("defer_until_safe_boundary", d.reasons)
        self.assertIn("tool_call_interval", d.reasons)

    def test_custom_thresholds(self):
        p = CheckpointPolicy(max_elapsed_seconds=10, max_tool_calls=2)
        self.assertEqual(decide(SessionCounters(tool_calls=2), p).action, "review")

    def test_invalid_policy_and_metrics(self):
        with self.assertRaises(ValueError):
            CheckpointPolicy(max_tool_calls=0)
        with self.assertRaises(ValueError):
            CheckpointPolicy(handoff_context_fraction=2)
        with self.assertRaises(ValueError):
            SessionCounters(tool_calls=-1)
        with self.assertRaises(ValueError):
            SessionCounters(context_fraction=1.3)

    def test_restart_packet_explicit_evidence(self):
        packet = make_restart_packet(
            objective="Fix a synthetic bug",
            acceptance=["typecheck green"],
            verified=["typecheck passed"],
            evidence_refs=["ci-run-123"],
            blockers=["integration not yet verified"],
            next_action="run integration fixture",
            tool_versions={"python": "3.12"},
        )
        self.assertFalse(packet["evidence_reviewed_by_host"])
        self.assertEqual(packet["evidence_references"], ["ci-run-123"])
        self.assertEqual(packet["unresolved_blockers"],
                         ["integration not yet verified"])

    def test_empty_restart_packet_rejected(self):
        with self.assertRaises(ValueError):
            make_restart_packet(
                objective="", acceptance=["a"], verified=[], evidence_refs=[],
                blockers=[], next_action="step", tool_versions={}
            )


if __name__ == "__main__":
    unittest.main()
