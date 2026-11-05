"""Policy tests using fictional documents only; no real institution data."""
import hashlib
import sys
import unittest
from dataclasses import replace
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from vibe_optimizer.private_knowledge import (
    AuditEvent, Document, InMemoryStore, Principal,
    PrivateKnowledgeGateway, Request,
)


def fake_doc(id="example", classification="RESTRICTED", status="approved",
             text="SYNTHETIC: a received message awaits review", **changes):
    defaults = dict(
        source_id=id, text=text, title="Invented operations manual",
        uri="synthetic://example", version="draft-v1", owner="fixture-owner",
        tenant="demo-university", classification=classification,
        roles=frozenset({"functional_manager"}),
        purposes=frozenset({"incident_analysis"}),
        destinations=frozenset({"approved-private-model"}),
        sha256_hex=hashlib.sha256(text.encode()).hexdigest(),
        status=status, license_approved=True,
    )
    defaults.update(changes)
    return Document(**defaults)


def request(destination="approved-private-model", tenant="demo-university",
            roles=frozenset({"functional_manager"}), purpose="incident_analysis",
            permitted_purposes=frozenset({"incident_analysis"}),
            as_of=date(2026, 11, 5)):
    return Request(Principal("fictional-operator", tenant, roles, permitted_purposes),
                   purpose, destination, as_of)


class PrivateKnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.restricted = fake_doc()
        self.public = fake_doc(
            id="public", classification="PUBLIC",
            text="SYNTHETIC PUBLIC documentation for report matching",
            destinations=frozenset({"approved-private-model", "public-model"}),
        )
        self.gateway = PrivateKnowledgeGateway(InMemoryStore(
            [self.restricted, self.public]
        ), {
            "public-model": frozenset({"PUBLIC"}),
            "approved-private-model": frozenset({"PUBLIC", "RESTRICTED"}),
        })

    def test_private_source_is_visible_in_approved_scope(self):
        matches = self.gateway.search(request(), "received")
        self.assertEqual([m.source_id for m in matches], ["example"])
        self.assertTrue(matches[0].untrusted_content)
        self.assertEqual(matches[0].version, "draft-v1")

    def test_restricted_content_never_egresses_to_public_model(self):
        self.assertEqual(
            self.gateway.search(request(destination="public-model"), "received"), []
        )
        self.assertIsNone(self.gateway.get_excerpt(
            request(destination="public-model"), "example"
        ))

    def test_public_evidence_remains_available(self):
        hits = self.gateway.search(request(destination="public-model"), "report")
        self.assertEqual([h.source_id for h in hits], ["public"])

    def test_wrong_role_denied(self):
        self.assertEqual(self.gateway.search(
            request(roles=frozenset({"researcher"})), "received"
        ), [])

    def test_wrong_tenant_denied(self):
        self.assertEqual(self.gateway.search(
            request(tenant="different-campus"), "received"
        ), [])

    def test_wrong_purpose_denied(self):
        self.assertEqual(self.gateway.search(
            request(purpose="marketing"), "received"
        ), [])

    def test_principal_purpose_denied(self):
        self.assertEqual(self.gateway.search(
            request(permitted_purposes=frozenset({"training"})), "received"
        ), [])

    def test_staged_revoked_and_unlicensed_sources_denied(self):
        for doc in (
            replace(self.restricted, status="staged"),
            replace(self.restricted, status="revoked"),
            replace(self.restricted, license_approved=False),
        ):
            gw = PrivateKnowledgeGateway(
                InMemoryStore([doc]), {"approved-private-model": frozenset({"RESTRICTED"})}
            )
            self.assertEqual(gw.search(request(), "received"), [])
            self.assertIsNone(gw.get_excerpt(request(), "example"))

    def test_personal_and_secret_are_always_blocked(self):
        for kind in ("PERSONAL", "SECRET"):
            with self.assertRaises(ValueError):
                PrivateKnowledgeGateway(InMemoryStore([]), {
                    "any-model": frozenset({kind})
                })

    def test_empty_policy_fails_closed(self):
        gw = PrivateKnowledgeGateway(InMemoryStore([self.restricted]), {})
        self.assertEqual(gw.search(request(), "received"), [])

    def test_version_effective_date(self):
        timebound = replace(self.restricted,
                            valid_from=date(2026, 1, 1),
                            valid_until=date(2026, 10, 31))
        gw = PrivateKnowledgeGateway(InMemoryStore([timebound]), {
            "approved-private-model": frozenset({"RESTRICTED"})
        })
        self.assertEqual(gw.search(request(), "received"), [])
        self.assertEqual(len(gw.search(
            request(as_of=date(2026, 9, 1)), "received")), 1)

    def test_hash_integrity(self):
        with self.assertRaises(ValueError):
            replace(self.restricted, text="tampered without new review")

    def test_no_direct_id_bypass(self):
        self.assertIsNone(self.gateway.get_excerpt(
            request(roles=frozenset()), "example"
        ))
        self.assertIsNone(self.gateway.get_excerpt(request(), "nonexistent"))

    def test_excerpt_is_bounded(self):
        d = fake_doc(text="received " + "X" * 700)
        gw = PrivateKnowledgeGateway(InMemoryStore([d]), {
            "approved-private-model": frozenset({"RESTRICTED"})
        })
        excerpt = gw.get_excerpt(request(), "example")
        self.assertIsNotNone(excerpt)
        self.assertLessEqual(len(excerpt.text), 320)
        with self.assertRaises(ValueError):
            gw.get_excerpt(request(), "example", length=1000)

    def test_query_and_audit_no_private_contents(self):
        self.gateway.search(request(), 'received " OR * ;')
        logged = repr(self.gateway.events)
        self.assertNotIn("received", logged)
        self.assertNotIn("SYNTHETIC:", logged)
        self.assertNotIn("example", logged)
        self.assertTrue(all(isinstance(e, AuditEvent) for e in self.gateway.events))

    def test_duplicate_ids_rejected(self):
        with self.assertRaises(ValueError):
            InMemoryStore([self.restricted, self.restricted])


if __name__ == "__main__":
    unittest.main()
