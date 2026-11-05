"""Synthetic proof of the restricted-source gateway. NOT a connection to SIS."""
from __future__ import annotations

from datetime import date
from hashlib import sha256
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from vibe_optimizer.private_knowledge import (
    Document, InMemoryStore, Principal, PrivateKnowledgeGateway, Request,
)


def make_source():
    fake_text = (
        "SYNTHETIC ONLY. A fictional enrollment request is received and "
        "placed in a review queue. A missing final decision is not proof "
        "that message transport failed."
    )
    return Document(
        source_id="fake-operations-guide",
        title="Synthetic enrollment workflow",
        uri="synthetic://fictional-workflow",
        version="fixture-v1",
        owner="fictional-owner",
        tenant="fictional-university",
        classification="RESTRICTED",
        roles=frozenset({"functional_manager"}),
        purposes=frozenset({"incident_analysis"}),
        destinations=frozenset({"approved-demo-model"}),
        text=fake_text,
        sha256_hex=sha256(fake_text.encode("utf-8")).hexdigest(),
        status="approved",
        license_approved=True,  # Only a test fixture, not real approval.
    )


def main():
    gateway = PrivateKnowledgeGateway(
        InMemoryStore([make_source()]),
        destination_policy={
            "public-remote-model": frozenset({"PUBLIC"}),
            "approved-demo-model": frozenset({"PUBLIC", "RESTRICTED"}),
        },
    )
    actor = Principal("fictional-user", "fictional-university",
                      frozenset({"functional_manager"}),
                      frozenset({"incident_analysis"}))
    for endpoint in ("public-remote-model", "approved-demo-model"):
        query = Request(actor, "incident_analysis", endpoint, date(2026, 11, 5))
        results = gateway.search(query, "review")
        print(f"{endpoint}: {len(results)} permitted evidence fragment(s)")
        for item in results:
            print(f"  {item.source_id}: {item.text[:90]}...")
    print("No real documents, actual identity or live systems accessed.")


if __name__ == "__main__":
    main()
