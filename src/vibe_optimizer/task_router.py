"""Transparent first-step decision policy for single-agent capability selection.

An advisory baseline, not a trained reasoning layer. Model-generated signals
must be cross-checked against observed test/doc/environment facts. The router
never executes tools or treats a missing source as a license to fabricate one.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Literal

from vibe_optimizer.capability_registry import CapabilityRegistry, TaskContext


Action = Literal[
    "clarify_specification", "reproduce_error", "locate_symbols",
    "check_version", "design_verifier", "search_workbench",
    "inspect_available_evidence", "no_external_capability_needed",
    "request_authorization", "abstain"
]


@dataclass(frozen=True)
class Signals:
    """Only explicitly known booleans should be True/False; unknown is None."""
    criteria_clear: bool | None = None
    error_observed: bool | None = None
    failure_reproduced: bool | None = None
    location_known: bool | None = None
    target_version_known: bool | None = None
    verifier_available: bool | None = None
    external_capability_needed: bool | None = None
    evidence_sufficient: bool | None = None

    def __post_init__(self) -> None:
        if any(x is not None and type(x) is not bool for x in asdict(self).values()):
            raise ValueError("Signals must be boolean or unknown")


@dataclass(frozen=True)
class Route:
    next_action: Action
    reason: str
    candidate_ids: tuple[str, ...] = ()
    missing_observations: tuple[str, ...] = ()
    authorization_needed: bool = False
    executed: bool = False


def route_task(task: TaskContext, signals: Signals,
               registry: CapabilityRegistry) -> Route:
    """Deterministic, easily falsified rule baseline.

    Signals remain independent of model choice in a real experiment.
    Unknown signals must not be silently read as false.
    """
    if signals.criteria_clear is False:
        return Route("clarify_specification", "Task contract is ambiguous",
                     missing_observations=("acceptance_criteria",))
    if signals.error_observed is True and signals.failure_reproduced is False:
        return Route("reproduce_error", "Observed failure not independently reproduced",
                     missing_observations=("reproducible_fixture",))
    if signals.location_known is False and signals.error_observed is True:
        return Route("locate_symbols", "Fault location has not been established")
    if signals.target_version_known is False:
        return Route("check_version", "Version-specific evidence may be incompatible",
                     missing_observations=("exact_target_version",))
    if signals.verifier_available is False:
        return Route("design_verifier", "No independent success criterion exists",
                     missing_observations=("verification_method",))
    if signals.external_capability_needed is False:
        return Route("no_external_capability_needed",
                     "No external capability is justified by current evidence")

    if signals.external_capability_needed is None and signals.evidence_sufficient is True:
        return Route("no_external_capability_needed",
                     "Existing evidence appears sufficient; don't add context by default")

    suggestions = registry.search(task, limit=5)
    if suggestions:
        # No privilege escalation: suggestions are metadata, not invocations.
        return Route("search_workbench",
                     "Task terms match qualified, version-compatible visible cards",
                     candidate_ids=tuple(s.capability_id for s in suggestions))
    if signals.external_capability_needed is True:
        return Route("abstain", "Needed capability was not found among permitted, "
                     "qualified and compatible cards",
                     missing_observations=("approved_alternative_or_owner",))
    if signals.evidence_sufficient is False:
        return Route("inspect_available_evidence",
                     "Evidence gap reported but missing capability not established",
                     missing_observations=("source_or_observation_needed",))
    return Route("no_external_capability_needed",
                 "No demonstrated benefit of a new capability")


def as_json_dict(route: Route) -> dict:
    return asdict(route)
