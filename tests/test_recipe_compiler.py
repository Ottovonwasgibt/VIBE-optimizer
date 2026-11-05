"""Tests of safe declarative recipe workshop and verified promotion boundary."""
from __future__ import annotations

from dataclasses import replace
from datetime import date
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from vibe_optimizer.recipe_compiler import Recipe, apply, evaluate_fixtures
from vibe_optimizer.candidate_governance import propose,adjudicate,ReviewReceipt,applicable


class RecipeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture=json.loads(
            (ROOT/"examples"/"script-workshop"/"synthetic-recipe.json").read_text(
                encoding="utf-8"))
        cls.recipe=Recipe.parse(cls.fixture["recipe"])

    def test_synthetic_fixtures_pass(self):
        result=evaluate_fixtures(self.recipe,self.fixture["fixtures"])
        self.assertTrue(result["all_passed"])
        self.assertEqual(result["fixture_passed"],3)
        self.assertIn("not_independent_approval",result["status"])

    def test_same_recipe_same_bytes(self):
        self.assertEqual(self.recipe.manifest_bytes(),self.recipe.manifest_bytes())

    def test_arbitrary_code_never_accepted_as_step(self):
        invalid=dict(self.fixture["recipe"])
        invalid["steps"]=["__import__('os').system('whoami')"]
        with self.assertRaises(ValueError):
            Recipe.parse(invalid)

    def test_unknown_fields_rejected(self):
        invalid=dict(self.fixture["recipe"])
        invalid["shell"]="rm -rf /"
        with self.assertRaises(ValueError):
            Recipe.parse(invalid)

    def test_bounded_input(self):
        with self.assertRaises(ValueError):
            apply(self.recipe,"X"*200001)

    def test_empty_or_overlong_recipe(self):
        for steps in ([], ["lowercase"]*13):
            bad=dict(self.fixture["recipe"])
            bad["steps"]=steps
            with self.subTest(steps=steps),self.assertRaises(ValueError):
                Recipe.parse(bad)

    def test_candidate_requires_separate_review(self):
        c=propose(
            candidate_id="synthetic_line_normalizer",
            kind="function",proposer="candidate-agent",
            candidate_bytes=self.recipe.manifest_bytes(),
            scope={"workshop":"synthetic-v1"},
            source_refs=["synthetic-recipe.json"]
        )
        self.assertFalse(applicable(c,{"workshop":"synthetic-v1"}))
        receipt=ReviewReceipt(
            reviewer="independent-test-runner",
            observed_content_sha256=c.content_sha256,
            validation_refs=("tests/test_recipe_compiler.py",),
            tests_passed=True,independently_reproduced=True,
            applicability_confirmed=True,reviewed_at=date(2026,11,5)
        )
        with self.assertRaises(PermissionError):
            adjudicate(c,receipt)
        approved=adjudicate(c,receipt,trusted_admin_process=True)
        self.assertTrue(applicable(approved,{"workshop":"synthetic-v1"}))
        self.assertFalse(applicable(approved,{"workshop":"production"}))


if __name__=="__main__":
    unittest.main()
