"""Smoke tests for the optional Vibe post_tool reminder hook."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples" / "checkpoint-watchdog"))
from vibe_post_tool_hook import handle_event  # noqa: E402


def event(sid="fixture-session", status="success", output=None):
    return {"hook_event_name": "post_tool", "session_id": sid,
            "tool_name": "file_system.read_file", "tool_status": status,
            "tool_output": {} if output is None else output}


class VibeHookTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.db = Path(self.tmp.name) / "test.sqlite"

    def test_no_nudge_before_threshold(self):
        for i in range(24):
            self.assertIsNone(handle_event(event(), database=self.db, now=10+i))
        self.assertIsNotNone(handle_event(event(), database=self.db, now=40))

    def test_one_nudge_not_every_subsequent_tool(self):
        for i in range(25):
            handle_event(event(), database=self.db, now=10+i)
        self.assertIsNone(handle_event(event(), database=self.db, now=100))

    def test_time_interval_on_next_tool_call(self):
        self.assertIsNone(handle_event(event(), database=self.db, now=100))
        result=handle_event(event(), database=self.db, now=1300)
        self.assertIn("time_interval",
                      result["hook_specific_output"]["additional_context"])

    def test_three_consecutive_failed_calls_trigger(self):
        self.assertIsNone(handle_event(event(status="failure"), database=self.db, now=1))
        self.assertIsNone(handle_event(event(status="failure"), database=self.db, now=2))
        result=handle_event(event(status="failure"), database=self.db, now=3)
        self.assertIn("repeat_failure", result["hook_specific_output"]["additional_context"])

    def test_shell_returncode_failure(self):
        for i in range(2):
            self.assertIsNone(handle_event(
                event(status="success", output={"returncode":1}),
                database=self.db, now=i))
        self.assertIsNotNone(handle_event(
            event(status="success", output={"returncode":2}),
            database=self.db, now=3))

    def test_success_resets_failure_streak(self):
        handle_event(event(status="failure"), database=self.db, now=1)
        handle_event(event(status="failure"), database=self.db, now=2)
        handle_event(event(status="success"), database=self.db, now=3)
        self.assertIsNone(handle_event(event(status="failure"), database=self.db, now=4))

    def test_separate_sessions(self):
        for i in range(24):
            handle_event(event("one"), database=self.db, now=10+i)
        self.assertIsNone(handle_event(event("two"), database=self.db, now=40))
        self.assertIsNotNone(handle_event(event("one"), database=self.db, now=41))

    def test_ignore_invalid_event(self):
        self.assertIsNone(handle_event({
            "hook_event_name":"post_agent","session_id":"fixture-session"
        }, database=self.db, now=0))
        self.assertIsNone(handle_event({
            "hook_event_name":"post_tool","session_id":""
        }, database=self.db, now=0))
        self.assertFalse(self.db.exists())


if __name__ == "__main__":
    unittest.main()
