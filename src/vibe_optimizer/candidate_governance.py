"""Governance for reusable lessons, skill and script proposals.

This module only handles metadata and verification receipts; it neither
executes candidate code nor distributes skills to an agent. A signed/verified
identity and source-of-truth for test evidence must be supplied by an
external trusted host. A Python reviewer string is NOT authentication.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date
import hashlib
import re


_KINDS = frozenset({"lesson", "procedure", "skill", "script", "function"})
_STATES = frozenset({"proposed", "qualified", "rejected", "revoked"})


@dataclass(frozen=True)
class Candidate:
    candidate_id: str
    kind: str
    proposer: str
    content_sha256: str
    scope: tuple[tuple[str, str], ...]
    source_refs: tuple[str, ...]
    status: str = "proposed"
    approved_by: str | None = None
    validation_refs: tuple[str, ...] = ()
    reviewed_at: date | None = None

    def __post_init__(self) -> None:
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,100}", self.candidate_id):
            raise ValueError("Invalid candidate ID")
        if self.kind not in _KINDS or self.status not in _STATES:
            raise ValueError("Unknown kind or state")
        if not self.proposer.strip() or len(self.content_sha256) != 64:
            raise ValueError("Missing proposer or content digest")
        if any(not k or not v for k, v in self.scope):
            raise ValueError("Applicability keys and values required")


@dataclass(frozen=True)
class ReviewReceipt:
    """Independent test proof *claimed* by host; host must validate it."""
    reviewer: str
    observed_content_sha256: str
    validation_refs: tuple[str, ...]
    tests_passed: bool
    independently_reproduced: bool
    applicability_confirmed: bool
    reviewed_at: date


def propose(*, candidate_id: str, kind: str, proposer: str,
            candidate_bytes: bytes, scope: dict[str, str],
            source_refs: list[str]) -> Candidate:
    """Do not include candidate bytes in public or model memory by default."""
    if not candidate_bytes:
        raise ValueError("Empty skill/lesson/script")
    if not isinstance(candidate_bytes, bytes):
        raise TypeError("Candidate must be bytes")
    if not source_refs:
        raise ValueError("Candidate requires at least one provenance reference")
    return Candidate(
        candidate_id, kind, proposer,
        hashlib.sha256(candidate_bytes).hexdigest(),
        tuple(sorted(scope.items())), tuple(source_refs)
    )


def adjudicate(candidate: Candidate, receipt: ReviewReceipt,
               *, trusted_admin_process: bool = False) -> Candidate:
    """Stage-to-qualified transition, never from model self-report.

    trusted_admin_process is only an explicit caller acknowledgement.
    Production authentication MUST be an independent process boundary; never
    expose this routine via agent-accessible tools or MCP.
    """
    if not trusted_admin_process:
        raise PermissionError("Only an external trusted review process may adjudicate")
    if candidate.status != "proposed":
        raise ValueError("Only proposed candidates are reviewable")
    if not receipt.reviewer.strip() or receipt.reviewer == candidate.proposer:
        raise ValueError("Independent reviewer required")
    if receipt.observed_content_sha256 != candidate.content_sha256:
        raise ValueError("Candidate changed since testing")
    if not receipt.validation_refs:
        raise ValueError("No independently checkable test references")
    approved = (receipt.tests_passed and receipt.independently_reproduced
                and receipt.applicability_confirmed)
    return replace(
        candidate, status="qualified" if approved else "rejected",
        approved_by=receipt.reviewer, validation_refs=receipt.validation_refs,
        reviewed_at=receipt.reviewed_at
    )


def revoke(candidate: Candidate, *, trusted_admin_process: bool = False) -> Candidate:
    if not trusted_admin_process:
        raise PermissionError("Revocation uses independent administrative path")
    if candidate.status == "revoked":
        raise ValueError("Already revoked")
    return replace(candidate, status="revoked")


def applicable(candidate: Candidate, context_versions: dict[str, str]) -> bool:
    """Only exact, reviewed applicability; unknown versions are not matches."""
    return (candidate.status == "qualified"
            and all(context_versions.get(k) == v for k, v in candidate.scope))
