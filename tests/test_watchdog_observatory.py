"""Tests for strict privacy-minimized event contract and offline replay."""
from __future__ import annotations
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "watchdog"))
from observatory import audit_trace, load_trace, metrics_from_events  # noqa: E402

EXAMPLE = ROOT / "experiments" / "watchdog" / "synthetic_trace.json"


def fixture():
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


class ObservatoryTests(unittest.TestCase):
    def test_example_processes_and_catches_drift(self):
        report = audit_trace(fixture())
        self.assertEqual(report["event_count"], 12)
        self.assertIn(10, [x["step"] for x in report["alerts"]])
        self.assertTrue(any("suitable_tool_unused" in x["reasons"]
                            for x in report["alerts"]))
        self.assertIn("offline analysis", report["status"])

    def test_exposure_is_metadata_only(self):
        report = audit_trace(fixture())
        serialized = json.dumps(report)
        for unexpected in ("tool_output", "tool_arguments", "student_number",
                           "system_prompt", "file_path"):
            self.assertNotIn(unexpected, serialized)

    def test_reject_unapproved_extra_document_text(self):
        payload = fixture()
        payload["events"][2]["tool_output"] = "Private student details"
        with self.assertRaisesRegex(ValueError, "exact approved keys"):
            audit_trace(payload)

    def test_reject_message_content_root(self):
        payload = fixture()
        payload["prompt"] = "private data"
        with self.assertRaisesRegex(ValueError, "exact approved keys"):
            audit_trace(payload)

    def test_reject_wrong_types(self):
        for key, value in (
            ("step", True), ("elapsed_seconds", -10),
            ("tool_class", ["generic"]), ("context_fraction", float("nan")),
            ("unsafe_operation", 1),
        ):
            payload = fixture()
            payload["events"][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                load_trace(payload)

    def test_reject_nonconsecutive_or_backward_clock(self):
        payload = fixture()
        payload["events"][1]["step"] = 7
        with self.assertRaises(ValueError):
            load_trace(payload)
        payload = fixture()
        payload["events"][2]["elapsed_seconds"] = 0
        with self.assertRaises(ValueError):
            load_trace(payload)

    def test_reject_invalid_event_enum(self):
        payload = fixture()
        payload["events"][0]["tool_fit"] = "invented high confidence"
        with self.assertRaises(ValueError):
            load_trace(payload)

    def test_reject_boolean_schema_version(self):
        payload = fixture()
        payload["schema_version"] = True
        with self.assertRaises(ValueError):
            load_trace(payload)

    def test_unknown_result_does_not_fabricate_progress(self):
        payload = fixture()
        payload["events"][0]["tool_result"] = "unknown"
        payload["events"][0]["progress"] = "unknown"
        payload["events"][0]["tool_fit"] = "unknown"
        _, events = load_trace(payload)
        first = metrics_from_events(events)[0]
        self.assertEqual(first.consecutive_failures, 0)
        self.assertEqual(first.actions_without_verified_progress, 0)
        self.assertFalse(first.tool_fit_evidence)

    def test_unsafe_event_is_preserved_as_halt(self):
        payload = fixture()
        payload["events"][2]["unsafe_operation"] = True
        report = audit_trace(payload)
        self.assertTrue(any(x["step"] == 3 and x["action"] == "halt"
                            for x in report["alerts"]))


if __name__ == "__main__":
    unittest.main()
