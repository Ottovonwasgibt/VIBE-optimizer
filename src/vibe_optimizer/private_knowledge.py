"""Fail-closed *prototype* of a permission-aware evidence gateway.

This module contains NO Osiris/Studielink integration, no remote model calls,
no real authentication and no production document parser. It is a testable
policy/retrieval scaffold using in-memory synthetic text. A real deployment
must supply verified identity, server-owned destination policy, durable audit
and an ACL-filtered private store. Never expose this as a public network API.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from hashlib import sha256
import re
from typing import Iterable, Protocol


CLASSIFICATIONS = frozenset({
    "PUBLIC", "RESTRICTED", "CONFIDENTIAL", "PERSONAL", "SECRET"
})
MAX_SNIPPET = 320


@dataclass(frozen=True)
class Principal:
    """Must be resolved by a trusted host authenticator, not from an LLM tool argument."""
    identifier: str
    tenant: str
    roles: frozenset[str]
    purposes: frozenset[str]


@dataclass(frozen=True)
class Request:
    """Destination and principal are trusted server context in any real deployment."""
    principal: Principal
    purpose: str
    destination: str
    as_of: date


@dataclass(frozen=True)
class Document:
    """A simulated indexed document plus provenance and policies."""
    source_id: str
    text: str
    title: str
    uri: str
    version: str
    owner: str
    tenant: str
    classification: str
    roles: frozenset[str]
    purposes: frozenset[str]
    destinations: frozenset[str]
    sha256_hex: str
    status: str = "staged"
    license_approved: bool = False
    valid_from: date | None = None
    valid_until: date | None = None

    def __post_init__(self) -> None:
        if not re.fullmatch(r"[a-zA-Z0-9_-]{1,100}", self.source_id):
            raise ValueError("Invalid source ID")
        if self.classification not in CLASSIFICATIONS:
            raise ValueError("Unrecognized classification")
        if self.status not in {"staged", "approved", "revoked"}:
            raise ValueError("Invalid status")
        if not all((self.title.strip(), self.uri.strip(),
                    self.owner.strip(), self.tenant.strip(), self.version.strip())):
            raise ValueError("Provenance is incomplete")
        if not self.purposes:
            raise ValueError("Source has no permitted purpose")
        if self.valid_from and self.valid_until and self.valid_until < self.valid_from:
            raise ValueError("Invalid validity period")
        digest = sha256(self.text.encode("utf-8")).hexdigest()
        if digest != self.sha256_hex:
            raise ValueError("Source content hash mismatch")


@dataclass(frozen=True)
class Evidence:
    source_id: str
    version: str
    locator: str
    text: str
    sha256_hex: str
    classification: str
    untrusted_content: bool = True


@dataclass(frozen=True)
class AuditEvent:
    """No queries, excerpts, document titles or restricted source IDs in prototype audit."""
    principal: str
    destination: str
    operation: str
    visible_result_count: int


class SourceStore(Protocol):
    """Prototype adapter contract; real store MUST enforce pre-search ACL itself."""
    def candidates(self) -> Iterable[Document]:
        ...


class InMemoryStore:
    """Only for synthetic fixtures. Never load production files here."""

    def __init__(self, docs: Iterable[Document] = ()) -> None:
        data = list(docs)
        if len({d.source_id for d in data}) != len(data):
            raise ValueError("Duplicate source IDs")
        self._docs = {doc.source_id: doc for doc in data}

    def candidates(self) -> Iterable[Document]:
        return self._docs.values()


class PrivateKnowledgeGateway:
    """Applies both user authorization and destination-specific model egress.

    destination_policy is administrator-owned; client/model-supplied policy
    overrides must never be allowed in a deployed server. This prototype
    exposes an in-memory event collection, not a production audit trail.
    """

    def __init__(self, store: SourceStore,
                 destination_policy: dict[str, frozenset[str]]) -> None:
        if any(not allowed.issubset(CLASSIFICATIONS - {"PERSONAL", "SECRET"})
               for allowed in destination_policy.values()):
            raise ValueError("Model destinations cannot receive PERSONAL/SECRET")
        self._store = store
        self._policy = {k: frozenset(v) for k, v in destination_policy.items()}
        self.events: list[AuditEvent] = []

    def _allows(self, doc: Document, req: Request) -> bool:
        allowed_classes = self._policy.get(req.destination, frozenset())
        if doc.classification not in allowed_classes:
            return False
        if doc.status != "approved" or not doc.license_approved:
            return False
        if req.destination not in doc.destinations:
            return False
        if req.purpose not in doc.purposes or req.purpose not in req.principal.purposes:
            return False
        if doc.valid_from and req.as_of < doc.valid_from:
            return False
        if doc.valid_until and req.as_of > doc.valid_until:
            return False
        if doc.classification != "PUBLIC":
            if not req.principal.identifier or req.principal.tenant != doc.tenant:
                return False
            if not doc.roles or not (req.principal.roles & doc.roles):
                return False
        return True

    def _audit(self, req: Request, op: str, count: int) -> None:
        self.events.append(AuditEvent(
            principal=req.principal.identifier,
            destination=req.destination,
            operation=op, visible_result_count=count
        ))

    def search(self, req: Request, query: str, limit: int = 5) -> list[Evidence]:
        if len(query) > 256:
            raise ValueError("Query too long")
        if not isinstance(limit, int):
            raise ValueError("Limit must be integer")
        limit = max(1, min(10, limit))
        tokens = [t.casefold() for t in re.findall(r"\w+", query)][:12]
        if not tokens:
            self._audit(req, "search", 0)
            return []
        results = []
        for doc in self._store.candidates():
            # Filter before lexical scoring and before constructing any output.
            if not self._allows(doc, req):
                continue
            body = doc.text.casefold()
            if not any(token in body for token in tokens):
                continue
            start = min(body.find(token) for token in tokens if token in body)
            excerpt = doc.text[max(0, start-40): min(len(doc.text), start+MAX_SNIPPET)]
            results.append(Evidence(
                doc.source_id, doc.version, "synthetic-excerpt",
                excerpt, doc.sha256_hex, doc.classification
            ))
            if len(results) >= limit:
                break
        self._audit(req, "search", len(results))
        return results

    def get_excerpt(self, req: Request, source_id: str, offset: int = 0,
                    length: int = MAX_SNIPPET) -> Evidence | None:
        if not isinstance(offset, int) or offset < 0 or not 1 <= length <= MAX_SNIPPET:
            raise ValueError("Invalid excerpt boundaries")
        # Does not distinguish unknown ID from unauthorized document.
        for doc in self._store.candidates():
            if doc.source_id == source_id and self._allows(doc, req):
                if offset >= len(doc.text):
                    break
                result = Evidence(
                    doc.source_id, doc.version, f"chars:{offset}-{offset+length}",
                    doc.text[offset:offset+length], doc.sha256_hex, doc.classification
                )
                self._audit(req, "get_excerpt", 1)
                return result
        self._audit(req, "get_excerpt", 0)
        return None
