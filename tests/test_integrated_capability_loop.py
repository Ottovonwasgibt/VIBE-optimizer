"""Tests integrated advisory loop and host tool delivery audit."""
from __future__ import annotations

from datetime import date
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from vibe_optimizer.capability_registry import CapabilityRegistry, TaskContext
from vibe_optimizer.task_router import Signals
from vibe_optimizer.capability_loop import advise
from vibe_optimizer.evidence_packets import evidence_from_text
from vibe_optimizer.checkpoint_watchdog import SessionCounters
from vibe_optimizer.capability_delivery import audit_delivery


class IntegratedLoopTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = CapabilityRegistry.load(
            ROOT / "examples/capability-workbench/catalog.json")

    def test_api_context_produces_qualified_recommendation_not_execution(self):
        result = advise(
            task_id="fake-api-001",
            context=TaskContext(
                "Pydantic v2 model validation API", "windows",
                versions=(("pydantic", "2"),)),
            signals=Signals(criteria_clear=True, external_capability_needed=True,
                            target_version_known=True),
            registry=self.registry,
            evidence=[evidence_from_text(
                source_id="synthetic-v2",locator="part-1",revision="v2",
                topic="pydantic",excerpt="Synthetic Pydantic v2 manual",
                observed_at=date(2026,11,5))],
            date_of_use=date(2026,11,5),
        )
        self.assertEqual(result.next_action,"search_workbench")
        self.assertIn("api_pydantic_2",result.candidates)
        self.assertNotIn("api_pydantic_1",result.candidates)
        self.assertEqual(result.execution_status,"advisory_only_not_executed")
        self.assertEqual(result.evidence_packet["status"],"evidence_available")

    def test_checkpoint_is_observational_not_authority(self):
        result=advise(
            task_id="fake-ho",
            context=TaskContext("Studielink Osiris enrollment status process","linux"),
            signals=Signals(external_capability_needed=True),
            registry=self.registry,evidence=[],date_of_use=date(2026,11,5),
            checkpoint=SessionCounters(tool_calls=25),
        )
        self.assertIn("higher_ed_process",result.candidates)
        self.assertEqual(result.checkpoint["action"],"review")
        self.assertEqual(result.evidence_packet["status"],
                         "abstain_no_authorized_evidence")
        self.assertEqual(result.execution_status,"advisory_only_not_executed")

    def test_delivery_audit_separates_catalog_from_real_visibility(self):
        audit=audit_delivery(
            qualified_ids=["documentation","repo_symbols","xml_validator"],
            host_visible_ids=["documentation","xml_validator","unexpected"],
            host_invocation_ids=["documentation","unexpected"],
            independently_relevant_ids=["repo_symbols","xml_validator"],
        )
        self.assertEqual(audit.missing_from_host,("repo_symbols",))
        self.assertEqual(audit.visible_but_unused_when_relevant,("xml_validator",))
        self.assertEqual(audit.invoked_without_observed_relevance,
                         ("documentation","unexpected"))
        self.assertEqual(audit.unexpected_exposure,("unexpected",))

    def test_delivery_audit_validates_ids(self):
        with self.assertRaises(ValueError):
            audit_delivery(
                qualified_ids=[""],host_visible_ids=[],
                host_invocation_ids=[],independently_relevant_ids=[])


if __name__ == "__main__":
    unittest.main()
