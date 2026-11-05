import sqlite3
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))
from capability_calculator import (  # noqa: E402
    funnel, completeness_independent, probe_value, reuse_breakeven, context_budget
)


class CalculatorTests(unittest.TestCase):
    def test_funnel_chain(self):
        self.assertAlmostEqual(funnel([.7, .65, .85, .8, .9]), .27846)
        self.assertAlmostEqual(funnel([.9, .85, .85, .8, .9]), .46818)

    def test_bad_probabilities(self):
        with self.assertRaises(ValueError):
            funnel([1.01])
        with self.assertRaises(ValueError):
            funnel([])

    def test_completeness_independent(self):
        self.assertAlmostEqual(completeness_independent(.85, 4), .52200625)
        with self.assertRaises(ValueError):
            completeness_independent(.5, 0)

    def test_probe(self):
        x = probe_value(.35, .25, 120, 4, 3)
        self.assertAlmostEqual(x["net_expected_utility"], 3.5)
        self.assertAlmostEqual(x["minimum_p_gap_to_justify_probe"], 7/30)

    def test_probe_uninformative(self):
        x = probe_value(.35, 0, 120, 4, 3)
        self.assertIsNone(x["minimum_p_gap_to_justify_probe"])
        self.assertFalse(x["probe_positive_utility"])

    def test_reuse(self):
        self.assertEqual(reuse_breakeven(120, 60, 30, .8, 12), 22)
        self.assertIsNone(reuse_breakeven(120, 60, 30, 0, 12))

    def test_context(self):
        x = context_budget(60, 600, 4, 500)
        self.assertEqual(x["saved_tokens"], 33100)
        self.assertAlmostEqual(x["saved_fraction"], 33100/36000)

    def test_context_bad(self):
        with self.assertRaises(ValueError):
            context_budget(10, 400, 11, 300)


if __name__ == "__main__":
    unittest.main()
