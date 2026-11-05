"""Regression tests for synthetic paired agent-evaluation metadata."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"experiments"/"live_agent"))
from paired_eval import report, _p_sign_test


def fixture():
    return json.loads((ROOT/"experiments"/"live_agent"/"synthetic_results.json").read_text(
        encoding="utf-8"))


class PairedAgentEvalTests(unittest.TestCase):
    def test_fixture_is_paired_and_explicitly_synthetic(self):
        r=report(fixture())
        self.assertEqual(r["evidence_status"],"synthetic")
        self.assertEqual(r["variants"]["baseline"]["runs"],8)
        self.assertEqual(r["paired_comparisons"]["docs"]["matched_pairs"],8)
        self.assertEqual(r["paired_comparisons"]["capability_pack"]["matched_pairs"],8)
        self.assertIn("not proof",r["paired_comparisons"]["docs"]["warning"])

    def test_paired_gain_and_loss_counts(self):
        r=report(fixture())
        self.assertEqual(r["paired_comparisons"]["docs"]["baseline_only_failures_fixed"],2)
        self.assertEqual(r["paired_comparisons"]["docs"]["baseline_successes_lost"],0)
        self.assertEqual(r["paired_comparisons"]["capability_pack"]["baseline_only_failures_fixed"],4)
        self.assertAlmostEqual(r["paired_comparisons"]["capability_pack"]["net_difference_pp"],50)

    def test_unpaired_comparison_rejected(self):
        f=fixture()
        f["results"].pop()
        with self.assertRaises(ValueError):
            report(f)

    def test_duplicate_comparison_rejected(self):
        f=fixture()
        f["results"].append(deepcopy(f["results"][0]))
        with self.assertRaises(ValueError):
            report(f)

    def test_unknown_fields_rejected_to_avoid_prompt_upload(self):
        f=fixture()
        f["results"][0]["prompt"]="private data"
        with self.assertRaises(ValueError):
            report(f)

    def test_over_budget_rejected(self):
        f=fixture()
        f["results"][0]["tokens_used"]=10000
        with self.assertRaises(ValueError):
            report(f)

    def test_failure_does_not_become_safe_success(self):
        f=fixture()
        f["results"][0]["solved"]=True
        f["results"][0]["safety_violation"]=True
        r=report(f)
        self.assertLess(r["variants"]["baseline"]["safe_solved"],
                        r["variants"]["baseline"]["runs"])

    def test_unadjusted_sign_test(self):
        self.assertAlmostEqual(_p_sign_test(3,0),0.25)
        self.assertIsNone(_p_sign_test(0,0))


if __name__=="__main__":
    unittest.main()
