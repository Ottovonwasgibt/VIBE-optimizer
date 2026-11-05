"""No-model tests of the integrated capability workbench foundations.

The fixture catalog is fictional. Passing tests establish only deterministic
registry, routing, evidence and qualification policy behavior.
"""
from __future__ import annotations

from dataclasses import replace
from datetime import date
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from vibe_optimizer.capability_registry import (  # noqa: E402
    CapabilityRegistry, CapabilityCard, TaskContext,
)
from vibe_optimizer.task_router import Signals, route_task
from vibe_optimizer.evidence_packets import evidence_from_text, compile_packet
from vibe_optimizer.candidate_governance import (
    propose, adjudicate, ReviewReceipt, revoke, applicable,
)

CATALOG = ROOT / "examples" / "capability-workbench" / "catalog.json"


class RegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = CapabilityRegistry.load(CATALOG)

    def test_pinned_version_chooses_only_matching_manual(self):
        ctx = TaskContext("Pydantic v2 model validation API", "windows",
                          versions=(("pydantic", "2"),))
        matches = self.registry.search(ctx)
        ids = [x.capability_id for x in matches]
        self.assertIn("api_pydantic_2", ids)
        self.assertNotIn("api_pydantic_1", ids)
        self.assertEqual(matches[0].permission, "public_read")

    def test_unknown_version_does_not_match_either_api(self):
        ctx = TaskContext("Pydantic model validation API", "linux")
        ids = [x.capability_id for x in self.registry.search(ctx)]
        self.assertNotIn("api_pydantic_1", ids)
        self.assertNotIn("api_pydantic_2", ids)

    def test_unapproved_candidate_and_unknown_health_not_recommended(self):
        ctx = TaskContext("convert csv into json with parser script", "linux",
                          permissions=frozenset({"execute", "public_read"}))
        ids = [x.capability_id for x in self.registry.search(ctx)]
        self.assertNotIn("tested_conversion", ids)
        self.assertNotIn("tested_conversion", self.registry.visible_ids(ctx))

    def test_execution_permission_is_not_implied_by_discovery(self):
        task = TaskContext("find symbols and callers repository", "windows")
        self.assertNotIn("repo_symbol_lookup",
                         [x.capability_id for x in self.registry.search(task)])
        elevated = replace(task, permissions=frozenset({"public_read","execute"}))
        self.assertIn("repo_symbol_lookup",
                      [x.capability_id for x in self.registry.search(elevated)])

    def test_restricted_metadata_not_leaked_in_public_search(self):
        task = TaskContext("osiris manual authorization", "linux")
        self.assertIsNone(self.registry.inspect("restricted_vendor_manual", task))
        self.assertNotIn("restricted_vendor_manual",
                         [x.capability_id for x in self.registry.search(task)])

    def test_restricted_access_requires_both_permission_and_classification(self):
        task = TaskContext(
            "osiris manual authorization", "linux",
            permissions=frozenset({"public_read","approved_read"}),
            permitted_classifications=frozenset({"PUBLIC","RESTRICTED"})
        )
        self.assertIsNotNone(self.registry.inspect("restricted_vendor_manual",task))

    def test_no_write_capability_with_default_permissions(self):
        task = TaskContext("update enrollment student register", "linux")
        self.assertNotIn("unsafe_admin_write",
                         [x.capability_id for x in self.registry.search(task)])

    def test_qualified_card_can_still_be_unsuitable(self):
        task = TaskContext("production mutation enrollment process", "linux")
        self.assertFalse(self.registry.inspect(
            "higher_ed_process", task)["suitable_for_context"])

    def test_invalid_duplicate_and_unexpected_card_field(self):
        raw = json.loads(CATALOG.read_text(encoding="utf-8"))["cards"][0]
        with self.assertRaises(ValueError):
            CapabilityRegistry((CapabilityCard.from_dict(raw),
                                CapabilityCard.from_dict(raw)))
        bad = dict(raw)
        bad["eval"] = "__import__('os').system('...')"
        with self.assertRaises(ValueError):
            CapabilityCard.from_dict(bad)

    def test_search_limit_and_empty(self):
        with self.assertRaises(ValueError):
            self.registry.search(TaskContext("foo","linux"),limit=11)
        self.assertEqual(self.registry.search(TaskContext("","linux")),[])


class RouterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = CapabilityRegistry.load(CATALOG)

    def test_unclear_criteria_before_tool_search(self):
        t = TaskContext("Pydantic model", "linux")
        r = route_task(t, Signals(criteria_clear=False), self.registry)
        self.assertEqual(r.next_action, "clarify_specification")
        self.assertFalse(r.executed)

    def test_reproduce_before_knowledge_fetch(self):
        t = TaskContext("Find error in Python", "linux")
        r = route_task(t, Signals(error_observed=True,
                                  failure_reproduced=False), self.registry)
        self.assertEqual(r.next_action, "reproduce_error")

    def test_unknown_version_requests_observation(self):
        t = TaskContext("Pydantic model validation API", "linux")
        r = route_task(t, Signals(target_version_known=False), self.registry)
        self.assertEqual(r.next_action, "check_version")

    def test_missing_verifier_first(self):
        t = TaskContext("validate XML schema", "linux")
        r = route_task(t, Signals(verifier_available=False), self.registry)
        self.assertEqual(r.next_action, "design_verifier")

    def test_negative_control_avoids_external_tool(self):
        t = TaskContext("Explain a general concept", "linux")
        r = route_task(t, Signals(external_capability_needed=False), self.registry)
        self.assertEqual(r.next_action, "no_external_capability_needed")

    def test_workbench_recommendation_is_advice_not_execution(self):
        t = TaskContext("Studielink Osiris enrollment status process", "windows")
        r = route_task(t, Signals(external_capability_needed=True), self.registry)
        self.assertEqual(r.next_action, "search_workbench")
        self.assertIn("higher_ed_process", r.candidate_ids)
        self.assertFalse(r.executed)

    def test_blocked_need_abstains_instead_of_fabricating_tool(self):
        t = TaskContext("convert csv into json using parser script", "linux")
        r = route_task(t, Signals(external_capability_needed=True), self.registry)
        self.assertEqual(r.next_action, "abstain")

    def test_signals_must_not_guess_unknowns(self):
        with self.assertRaises(ValueError):
            Signals(target_version_known="false")


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.d = date(2026, 11, 5)
        self.a = evidence_from_text(
            source_id="manual-v1", locator="part-1", revision="v1",
            topic="pydantic API", excerpt="Use parse_obj in v1",
            observed_at=self.d)
        self.b = evidence_from_text(
            source_id="manual-v2", locator="part-2", revision="v2",
            topic="pydantic API", excerpt="Use model_validate in v2",
            observed_at=self.d)

    def test_conflicting_version_evidence_marked_not_silently_resolved(self):
        p = compile_packet(task_id="test", purpose="API migration",
                           items=[self.a, self.b], as_of=self.d)
        self.assertEqual(p["conflicts_to_investigate"], ["pydantic API"])
        self.assertTrue(all(x["trust"].startswith("lower_trust")
                            for x in p["evidence"]))

    def test_default_rejects_private(self):
        private = replace(self.b, classification="RESTRICTED")
        p = compile_packet(task_id="t", purpose="check", items=[private],
                           as_of=self.d)
        self.assertEqual(p["status"], "abstain_no_authorized_evidence")
        self.assertEqual(p["omitted"]["forbidden"], 1)

    def test_expired_and_duplicate(self):
        p = compile_packet(task_id="t", purpose="check",
                           items=[replace(self.a, expires_at=date(2025,1,1)),
                                  self.b,self.b], as_of=self.d)
        self.assertEqual(len(p["evidence"]), 1)
        self.assertEqual(p["omitted"]["expired"],1)

    def test_small_packet_respects_bound(self):
        p = compile_packet(task_id="t", purpose="check",
                           items=[replace(self.a,excerpt="x"*200),
                                  replace(self.b,excerpt="y"*200)],
                           as_of=self.d,max_chars=100)
        self.assertLessEqual(sum(len(x["excerpt"]) for x in p["evidence"]),100)


class CandidateGovernanceTests(unittest.TestCase):
    def setUp(self):
        self.c = propose(candidate_id="parser",kind="script",proposer="agent",
                         candidate_bytes=b"print('synthetic')",
                         scope={"python":"3.12"},source_refs=["fixture-001"])
        self.review = ReviewReceipt(
            reviewer="independent-reviewer",
            observed_content_sha256=self.c.content_sha256,
            validation_refs=("ci/test/123",), tests_passed=True,
            independently_reproduced=True, applicability_confirmed=True,
            reviewed_at=date(2026,11,5))

    def test_candidate_not_usable_before_review(self):
        self.assertFalse(applicable(self.c,{"python":"3.12"}))
        self.assertEqual(self.c.status,"proposed")

    def test_review_requires_trusted_process(self):
        with self.assertRaises(PermissionError):
            adjudicate(self.c,self.review)

    def test_self_review_forbidden(self):
        with self.assertRaises(ValueError):
            adjudicate(self.c,replace(self.review,reviewer="agent"),
                       trusted_admin_process=True)

    def test_candidate_changed_since_test(self):
        with self.assertRaises(ValueError):
            adjudicate(self.c,replace(self.review,observed_content_sha256="0"*64),
                       trusted_admin_process=True)

    def test_verified_candidate_has_scope_limits(self):
        c = adjudicate(self.c,self.review,trusted_admin_process=True)
        self.assertEqual(c.status,"qualified")
        self.assertTrue(applicable(c,{"python":"3.12"}))
        self.assertFalse(applicable(c,{"python":"3.13"}))

    def test_failed_review_is_rejected(self):
        c = adjudicate(self.c,replace(self.review,tests_passed=False),
                       trusted_admin_process=True)
        self.assertEqual(c.status,"rejected")
        self.assertFalse(applicable(c,{"python":"3.12"}))

    def test_revocation_removes_reuse(self):
        c = adjudicate(self.c,self.review,trusted_admin_process=True)
        revoked = revoke(c,trusted_admin_process=True)
        self.assertFalse(applicable(revoked,{"python":"3.12"}))
        with self.assertRaises(ValueError):
            revoke(revoked,trusted_admin_process=True)


if __name__ == "__main__":
    unittest.main()
