"""Capability delivery and utilization audit from trusted host observations.

Differentiates four states often conflated in agent discussions:
qualified/allowed catalog entry, actually advertised tool, actually invoked,
and independently demonstrated usefulness for the task.

No LLM, hook or tool is executed. Do not use model statements like
'I had a tool' as the source of tool-delivery telemetry.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class DeliveryAudit:
    expected: tuple[str, ...]
    visible: tuple[str, ...]
    invoked: tuple[str, ...]
    relevant: tuple[str, ...]
    missing_from_host: tuple[str, ...]
    visible_but_unused_when_relevant: tuple[str, ...]
    invoked_without_observed_relevance: tuple[str, ...]
    relevant_invoked: tuple[str, ...]
    unexpected_exposure: tuple[str, ...]

    def as_dict(self) -> dict:
        return asdict(self)


def audit_delivery(*, qualified_ids: list[str], host_visible_ids: list[str],
                   host_invocation_ids: list[str],
                   independently_relevant_ids: list[str]) -> DeliveryAudit:
    """All lists should come from an independent instrumentation boundary.

    'Relevant' is externally judged, not model-assigned. Absence from
    independently_relevant_ids is unknown without complete annotations.
    This prototype treats it as not demonstrated, not necessarily useless.
    """
    for xs in (qualified_ids, host_visible_ids,
               host_invocation_ids, independently_relevant_ids):
        if any(not isinstance(x, str) or not x or len(x) > 100 for x in xs):
            raise ValueError("Invalid tool ID")
        if len(xs) > 10000:
            raise ValueError("Oversized tool inventory")
    q, v, i, r = (set(xs) for xs in
                   (qualified_ids, host_visible_ids,
                    host_invocation_ids, independently_relevant_ids))
    return DeliveryAudit(
        tuple(sorted(q)), tuple(sorted(v)), tuple(sorted(i)), tuple(sorted(r)),
        tuple(sorted(q - v)),
        tuple(sorted((r & v) - i)),
        tuple(sorted(i - r)),
        tuple(sorted(r & i)),
        tuple(sorted(v - q)),
    )
