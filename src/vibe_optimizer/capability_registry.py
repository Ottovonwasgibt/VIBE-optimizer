"""Advisory, read-only capability registry for one task-solving agent.

A qualified card is discoverable metadata, NOT executable authority.
The registry does not install packages, read private docs, execute scripts,
invoke arbitrary MCP tools or grant permissions. Inputs are a small,
explicitly approved local JSON catalog; no remote downloads.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any

KINDS = frozenset({"manual", "procedure", "script", "function", "stack",
                   "tool", "verifier", "memory"})
STATUSES = frozenset({"candidate", "tested", "qualified", "revoked"})
PERMISSIONS = frozenset({"public_read", "approved_read", "execute", "write"})
CLASSIFICATIONS = frozenset({"PUBLIC", "RESTRICTED", "CONFIDENTIAL"})
HEALTH = frozenset({"healthy", "unknown", "unreachable", "not_applicable"})
WORD = re.compile(r"[a-zA-Z0-9_]+")
KEY = re.compile(r"[a-zA-Z0-9_.-]{1,100}")
CARD_FIELDS = frozenset({
    "capability_id", "kind", "description", "keywords", "triggers",
    "exclusions", "requires_versions", "environment", "status",
    "permission", "classification", "health", "source", "revision",
    "tests", "license_review",
})


def _terms(text: str) -> frozenset[str]:
    return frozenset(x.lower() for x in WORD.findall(text))


def _strings(value: Any, *, label: str) -> tuple[str, ...]:
    if not isinstance(value, list) or any(
        not isinstance(x, str) or not 1 <= len(x) <= 240 for x in value
    ):
        raise ValueError(f"{label} must be a list of bounded strings")
    return tuple(value)


@dataclass(frozen=True)
class CapabilityCard:
    capability_id: str
    kind: str
    description: str
    keywords: tuple[str, ...]
    triggers: tuple[str, ...]
    exclusions: tuple[str, ...]
    requires_versions: tuple[tuple[str, str], ...]
    environment: tuple[str, ...]
    status: str
    permission: str
    classification: str
    health: str
    source: str
    revision: str
    tests: tuple[str, ...]
    license_review: str

    @classmethod
    def from_dict(cls, d: dict) -> "CapabilityCard":
        if not isinstance(d, dict) or set(d) != CARD_FIELDS:
            raise ValueError("Capability card fields do not match v1 schema")
        if not isinstance(d["capability_id"], str) or not KEY.fullmatch(
            d["capability_id"]
        ):
            raise ValueError("Invalid capability ID")
        if d["kind"] not in KINDS or d["status"] not in STATUSES:
            raise ValueError("Invalid kind or qualification status")
        if d["permission"] not in PERMISSIONS or d["classification"] not in CLASSIFICATIONS:
            raise ValueError("Invalid permission or classification")
        if d["health"] not in HEALTH:
            raise ValueError("Invalid health state")
        for k in ("description", "source", "revision"):
            if not isinstance(d[k], str) or not d[k].strip() or len(d[k]) > 1024:
                raise ValueError(f"Missing or oversized {k}")
        for k in ("keywords", "triggers", "exclusions", "environment", "tests"):
            _strings(d[k], label=k)
        versions = d["requires_versions"]
        if not isinstance(versions, dict) or any(
            not isinstance(k, str) or not KEY.fullmatch(k) or
            not isinstance(v, str) or not 1 <= len(v) <= 100
            for k, v in versions.items()
        ):
            raise ValueError("Invalid exact-version requirements")
        if d["license_review"] not in ("approved", "pending", "denied"):
            raise ValueError("Unreviewed license status")
        return cls(
            capability_id=d["capability_id"], kind=d["kind"],
            description=d["description"],
            keywords=_strings(d["keywords"], label="keywords"),
            triggers=_strings(d["triggers"], label="triggers"),
            exclusions=_strings(d["exclusions"], label="exclusions"),
            requires_versions=tuple(sorted(versions.items())),
            environment=_strings(d["environment"], label="environment"),
            status=d["status"], permission=d["permission"],
            classification=d["classification"], health=d["health"],
            source=d["source"], revision=d["revision"],
            tests=_strings(d["tests"], label="tests"),
            license_review=d["license_review"],
        )

    def to_dict(self) -> dict:
        return {
            "capability_id": self.capability_id, "kind": self.kind,
            "description": self.description, "keywords": list(self.keywords),
            "triggers": list(self.triggers), "exclusions": list(self.exclusions),
            "requires_versions": dict(self.requires_versions),
            "environment": list(self.environment), "status": self.status,
            "permission": self.permission,
            "classification": self.classification,
            "health": self.health, "source": self.source,
            "revision": self.revision, "tests": list(self.tests),
            "license_review": self.license_review,
        }


@dataclass(frozen=True)
class TaskContext:
    """The model does NOT get to invent auth or environment properties.

    Model destination and permissions must come from a trusted host. This
    class merely records them, it does not authenticate the caller.
    """
    question: str
    environment: str
    versions: tuple[tuple[str, str], ...] = ()
    permissions: frozenset[str] = frozenset({"public_read"})
    permitted_classifications: frozenset[str] = frozenset({"PUBLIC"})
    allowed_kinds: frozenset[str] = KINDS
    externally_verified_tool_need: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.question, str) or len(self.question) > 2048:
            raise ValueError("Invalid task text")
        if not self.environment or len(self.environment) > 80:
            raise ValueError("Invalid environment")
        if not set(self.permissions).issubset(PERMISSIONS):
            raise ValueError("Invalid requested permission")
        if not set(self.permitted_classifications).issubset(CLASSIFICATIONS):
            raise ValueError("Invalid permitted classification")


@dataclass(frozen=True)
class Suggestion:
    capability_id: str
    kind: str
    score: int
    reason: str
    source: str
    revision: str
    permission: str


class CapabilityRegistry:
    def __init__(self, cards: tuple[CapabilityCard, ...]) -> None:
        if len(cards) > 10000:
            raise ValueError("Registry exceeds research maximum")
        ids = [c.capability_id for c in cards]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate capability IDs")
        self._cards = {c.capability_id: c for c in cards}

    @classmethod
    def load(cls, path: str | Path) -> "CapabilityRegistry":
        p = Path(path)
        if p.stat().st_size > 4_000_000:
            raise ValueError("Catalog too large")
        raw = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(raw, dict) or set(raw) != {"schema_version", "cards"}:
            raise ValueError("Invalid catalog envelope")
        if type(raw["schema_version"]) is not int or raw["schema_version"] != 1:
            raise ValueError("Unsupported catalog version")
        if not isinstance(raw["cards"], list):
            raise ValueError("Catalog cards must be an array")
        return cls(tuple(CapabilityCard.from_dict(x) for x in raw["cards"]))

    @staticmethod
    def _authorized(card: CapabilityCard, ctx: TaskContext) -> bool:
        return (card.status == "qualified" and card.license_review == "approved"
                and card.classification in ctx.permitted_classifications
                and card.permission in ctx.permissions
                and card.kind in ctx.allowed_kinds)

    @staticmethod
    def _fits(card: CapabilityCard, ctx: TaskContext) -> bool:
        # Version UNKNOWN does not silently match a version-pinned recipe.
        known = dict(ctx.versions)
        if any(known.get(k) != v for k, v in card.requires_versions):
            return False
        if card.environment and ctx.environment not in card.environment:
            return False
        if card.health in ("unknown", "unreachable"):
            return False
        query = _terms(ctx.question)
        if any(_terms(x).issubset(query) for x in card.exclusions if _terms(x)):
            return False
        return True

    def search(self, ctx: TaskContext, *, limit: int = 5) -> list[Suggestion]:
        if not isinstance(limit, int) or not 1 <= limit <= 10:
            raise ValueError("Search limit must be 1..10")
        query = _terms(ctx.question)
        if not query:
            return []
        found = []
        for card in self._cards.values():
            if not self._authorized(card, ctx) or not self._fits(card, ctx):
                continue
            overlap = query & _terms(" ".join(card.keywords))
            triggers = sum(1 for phrase in card.triggers
                           if _terms(phrase) and _terms(phrase).issubset(query))
            score = 3 * len(overlap) + 6 * triggers
            if score == 0:
                continue
            found.append(Suggestion(
                card.capability_id, card.kind, score,
                "keyword overlap and declared task trigger",
                card.source, card.revision, card.permission
            ))
        return sorted(found, key=lambda x: (-x.score, x.capability_id))[:limit]

    def inspect(self, capability_id: str, ctx: TaskContext) -> dict | None:
        card = self._cards.get(capability_id)
        if card is None or not self._authorized(card, ctx):
            return None
        # Requires version/scope suitability check before using the card.
        return {"card": card.to_dict(), "suitable_for_context": self._fits(card, ctx),
                "requires_review_before_execution": card.permission != "public_read"}

    def visible_ids(self, ctx: TaskContext) -> list[str]:
        """For an independently trusted catalog/delivery audit."""
        return sorted(c.capability_id for c in self._cards.values()
                      if self._authorized(c, ctx))
