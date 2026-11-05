"""Tests for synthetic watchdog replay and reminder debounce semantics.

These tests evaluate detection policies, not actual LLM behavior.
"""
from __future__ import annotations
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "watchdog"))

from replay import run, scenarios, policies, replay_one  # noqa: E402
from vibe_optimizer.watchdog_gate import (
    GateState, gate_alert, acknowledge_handoff, acknowledge_safety_hold
)
from vibe_optimizer.checkpoint_watchdog import CheckpointDecision  # noqa: E402


def decision(action="review", *reasons):
    return CheckpointDecision(action, tuple(reasons), ())


class WatchdogReplayTests(unittest.TestCase):
    def test_fixture_and_policy_counts(self):
        report = run()
        self.assertEqual(report["scenarios"], 10)
        self.assertEqual(report["positive_scenarios"], 6)
        self.assertEqual(report["negative_scenarios"], 4)
        self.assertEqual(set(report["summary"]), set(policies()))

    def test_baseline_never_alerts(self):
        x = run()["summary"]["baseline"]
        self.assertEqual(x["total_alerts"], 0)
        self.assertEqual(x["synthetic_positive_detected"], 0)

    def test_hybrid_detects_at_least_as_many_as_interval(self):
        s = run()["summary"]
        self.assertGreaterEqual(s["hybrid"]["synthetic_positive_detected"],
                                s["interval_only"]["synthetic_positive_detected"])
        self.assertGreater(s["hybrid"]["total_alerts"], 0)

    def test_rate_limit_reduces_spam_not_detection_on_these_fixtures(self):
        s = run()["summary"]
        self.assertLess(s["hybrid_gated"]["total_alerts"],
                        s["hybrid"]["total_alerts"])
        self.assertEqual(s["hybrid_gated"]["synthetic_positive_detected"],
                         s["hybrid"]["synthetic_positive_detected"])

    def test_halt_takes_priority(self):
        scenario = next(x for x in scenarios() if x.name == "unsafe_operation")
        row = replay_one(scenario, "hybrid_gated", policies()["hybrid_gated"])
        self.assertEqual(row["first_detected_step"], 8)
        self.assertEqual(row["alerts"][0]["action"], "halt")

    def test_critical_action_not_interrupted(self):
        scenario = next(x for x in scenarios() if x.name == "safe_boundary_deferral")
        row = replay_one(scenario, "hybrid_gated", policies()["hybrid_gated"])
        self.assertFalse(any(a["step"] in (24, 25, 26) for a in row["alerts"]))
        self.assertGreaterEqual(row["first_detected_step"], 27)

    def test_no_specialized_tool_drift_when_no_tool_fits(self):
        s = next(x for x in scenarios() if x.name == "generic_tool_appropriate")
        row = replay_one(s, "event_only", policies()["event_only"])
        self.assertEqual(row["alert_count"], 0)

    def test_gate_interval_and_distinct_reason(self):
        st = GateState()
        emit, st = gate_alert(decision("review", "time_interval"), 2, st)
        self.assertTrue(emit)
        emit, st = gate_alert(decision("review", "time_interval"), 3, st)
        self.assertFalse(emit)
        emit, st = gate_alert(decision("review", "repeat_failure"), 4, st)
        self.assertTrue(emit)
        emit, st = gate_alert(decision("review", "repeat_failure"), 12, st)
        self.assertTrue(emit)

    def test_gate_rearms_on_normal_step(self):
        _, st = gate_alert(decision("review", "repeat_failure"), 1, GateState())
        emitted, st = gate_alert(decision("continue"), 2, st)
        self.assertFalse(emitted)
        emitted, _ = gate_alert(decision("review", "repeat_failure"), 3, st)
        self.assertTrue(emitted)

    def test_pending_handoff_requires_host_ack(self):
        st = GateState()
        emitted, st = gate_alert(decision("handoff", "context_pressure"), 1, st)
        self.assertTrue(emitted)
        emitted, st = gate_alert(decision("handoff", "context_pressure"), 2, st)
        self.assertFalse(emitted)
        self.assertTrue(acknowledge_handoff(st, host_reviewed=False).handoff_pending)
        cleared = acknowledge_handoff(st, host_reviewed=True)
        self.assertFalse(cleared.handoff_pending)
        emitted, st = gate_alert(decision("handoff", "context_pressure"), 3, cleared)
        self.assertTrue(emitted)

    def test_halt_ignores_reminder_cooldown(self):
        _, st = gate_alert(decision("review", "time_interval"), 1, GateState())
        emitted, _ = gate_alert(decision("halt", "unsafe_operation_detected"), 2, st)
        self.assertTrue(emitted)

    def test_safety_latch_survives_transient_signal_and_handoff_ack(self):
        state = GateState()
        emitted, state = gate_alert(
            decision("halt", "unsafe_operation_detected"), 1, state)
        self.assertTrue(emitted)
        self.assertTrue(state.safety_hold)
        emitted, state = gate_alert(decision("continue"), 2, state)
        self.assertFalse(emitted)
        self.assertTrue(state.safety_hold)
        state = acknowledge_handoff(state, host_reviewed=True)
        self.assertTrue(state.safety_hold)
        self.assertTrue(acknowledge_safety_hold(
            state, authorized_host_release=False).safety_hold)
        restored = acknowledge_safety_hold(state, authorized_host_release=True)
        self.assertFalse(restored.safety_hold)
        emitted, restored = gate_alert(
            decision("review", "time_interval"), 3, restored)
        self.assertTrue(emitted)

    def test_out_of_order_host_counter_rejected(self):
        _, st = gate_alert(decision("review", "time_interval"), 5, GateState())
        with self.assertRaises(ValueError):
            gate_alert(decision("review", "time_interval"), 5, st)


if __name__ == "__main__":
    unittest.main()
