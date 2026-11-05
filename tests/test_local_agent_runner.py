"""Tests for the manual, opt-in local single-model evaluation launcher."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
import json
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "live_agent"))
from run_local import load_suite, build_prompt, cli_command, run


def args(folder: Path, adapter: str = "vibe", execute: bool = False):
    return SimpleNamespace(
        suite=ROOT / "experiments" / "live_agent" / "public_synthetic_suite.json",
        adapter=adapter, model=None if not execute else "explicit-test-model",
        task=None, variants="baseline,reference", max_turns=5,
        max_tokens=8000, time_limit=180, executable=None,
        output=folder, execute=execute,
    )


class RunnerTests(unittest.TestCase):
    def test_fixture_has_versioned_and_noncoding_cases(self):
        suite=load_suite(ROOT/"experiments/live_agent/public_synthetic_suite.json")
        self.assertEqual(len(suite["tasks"]),4)
        self.assertIn("functional_management",
                      {x["category"] for x in suite["tasks"]})

    def test_only_reference_variant_receives_reference_facts(self):
        case=load_suite(ROOT/"experiments/live_agent/public_synthetic_suite.json")["tasks"][1]
        baseline=build_prompt(case,"baseline")
        enriched=build_prompt(case,"reference")
        self.assertNotIn("ReceivedBySIS_AwaitingLocalApproval",baseline)
        self.assertIn("ReceivedBySIS_AwaitingLocalApproval",enriched)
        self.assertIn("lower-trust facts",enriched)

    def test_dry_run_never_executes_cli(self):
        with tempfile.TemporaryDirectory() as dirname:
            folder=Path(dirname)/"runtime"
            result=run(args(folder))
            self.assertEqual(result["mode"],"DRY_RUN")
            self.assertEqual(len(result["sessions"]),8)
            self.assertTrue(all(x["status"]=="dry_run_not_executed"
                                for x in result["sessions"]))
            self.assertTrue((folder/"manifest.json").exists())
            self.assertFalse(list(folder.glob("**/stdout.txt")))

    def test_claude_dry_run_does_not_contact_provider(self):
        with tempfile.TemporaryDirectory() as dirname:
            result=run(args(Path(dirname)/"runtime",adapter="claude"))
            self.assertEqual(len(result["sessions"]),8)
            self.assertEqual(result["mode"],"DRY_RUN")

    def test_automation_must_pin_a_model(self):
        with tempfile.TemporaryDirectory() as dirname:
            a=args(Path(dirname),execute=True)
            with self.assertRaises(ValueError):
                run(SimpleNamespace(**{**vars(a),"model":None}))

    def test_real_cli_not_accidentally_autoapproved(self):
        prompt=Path("test-prompt.txt")
        cmd=cli_command("vibe","vibe","model",prompt,
                        Path("export"),5,8000,180)
        self.assertIn("--agent",cmd)
        self.assertIn("ask",cmd)
        self.assertNotIn("--auto-approve",cmd)
        self.assertNotIn("--yolo",cmd)

    def test_invalid_or_duplicate_suite_ids_rejected(self):
        source=load_suite(ROOT/"experiments/live_agent/public_synthetic_suite.json")
        source["tasks"].append(dict(source["tasks"][0]))
        with tempfile.TemporaryDirectory() as dirname:
            p=Path(dirname)/"suite.json"
            p.write_text(json.dumps(source),encoding="utf-8")
            with self.assertRaises(ValueError):
                load_suite(p)

    def test_claude_adapter_is_plan_mode(self):
        with tempfile.TemporaryDirectory() as dirname:
            p=Path(dirname)/"prompt.txt"
            p.write_text("Synthetic test only",encoding="utf-8")
            cmd=cli_command("claude","claude","model",p,
                            Path("export"),4,5000,60)
            self.assertIn("--permission-mode",cmd)
            self.assertIn("plan",cmd)
            self.assertNotIn("--dangerously-skip-permissions",cmd)


if __name__ == "__main__":
    unittest.main()
