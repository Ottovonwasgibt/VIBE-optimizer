"""Deterministic checkpoint policy for one long-running agent.

Research scaffold: NO background timer, no model calls, no tool interception,
no host integration. The host must supply trusted counters and must apply the
result at a safe boundary (between tasks/tool calls), not during a write.
A model self-report cannot suppress a checkpoint trigger.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Literal

Action = Literal["continue", "review", "handoff", "halt"]


@dataclass(frozen=True)
class CheckpointPolicy:
    max_elapsed_seconds: int = 1200
    max_tool_calls: int = 25
    max_failed_attempts: int = 3
    max_unverified_actions: int = 18
    max_fallback_tool_streak: int = 7
    handoff_context_fraction: float = 0.85

    def __post_init__(self) -> None:
        if min(self.max_elapsed_seconds, self.max_tool_calls,
               self.max_failed_attempts, self.max_unverified_actions,
               self.max_fallback_tool_streak) <= 0:
            raise ValueError("All trigger thresholds must be positive")
        if not 0 < self.handoff_context_fraction <= 1:
            raise ValueError("Context threshold must be in (0,1]")


@dataclass(frozen=True)
class SessionCounters:
    """All counts apply since the last externally acknowledged checkpoint.

    tool_fit_evidence is an independently observed reason that a specialized
    tool applies; don't infer merely from the presence of a tool.
    """
    elapsed_seconds: int = 0
    tool_calls: int = 0
    consecutive_failures: int = 0
    actions_without_verified_progress: int = 0
    fallback_tool_streak: int = 0
    tool_fit_evidence: bool = False
    context_fraction: float = 0.0
    unsafe_operation_detected: bool = False
    currently_in_critical_action: bool = False

    def __post_init__(self) -> None:
        if min(self.elapsed_seconds, self.tool_calls,
               self.consecutive_failures,
               self.actions_without_verified_progress,
               self.fallback_tool_streak) < 0:
            raise ValueError("Counters cannot be negative")
        if not 0 <= self.context_fraction <= 1:
            raise ValueError("Context fraction must be in [0,1]")


@dataclass(frozen=True)
class CheckpointDecision:
    action: Action
    reasons: tuple[str, ...]
    suggested_checks: tuple[str, ...]

    def as_dict(self) -> dict:
        return asdict(self)


REVIEW_CHECKS = (
    "Restate the original task objective and observable acceptance criteria.",
    "List independently verified outcomes with source/test evidence; mark hypotheses.",
    "Check whether the next operation requires a better or unused available tool.",
    "Identify repeated failures, drift from procedure and unresolved risks.",
    "Choose a minimal verified next action or propose a context handoff.",
)

HANDOFF_CHECKS = (
    "Save objective, acceptance criteria, evidence pointers and tested results.",
    "Record current tool versions, next permitted action and unresolved blockers.",
    "Verify the restart packet against the real task record; avoid invented facts.",
    "Resume only at a safe boundary with a fresh context and restored constraints.",
)


def decide(c: SessionCounters, p: CheckpointPolicy | None = None) -> CheckpointDecision:
    """Evaluate recorded signals. This function cannot stop a live agent itself."""
    p = p or CheckpointPolicy()
    if c.unsafe_operation_detected:
        return CheckpointDecision("halt", ("unsafe_operation_detected",),
                                  ("Stop sensitive actions and request authorized review.",))

    reasons = []
    if c.consecutive_failures >= p.max_failed_attempts:
        reasons.append("repeat_failure")
    if c.actions_without_verified_progress >= p.max_unverified_actions:
        reasons.append("unverified_progress_stall")
    if c.tool_fit_evidence and c.fallback_tool_streak >= p.max_fallback_tool_streak:
        reasons.append("suitable_tool_unused")
    if c.elapsed_seconds >= p.max_elapsed_seconds:
        reasons.append("time_interval")
    if c.tool_calls >= p.max_tool_calls:
        reasons.append("tool_call_interval")

    handoff = c.context_fraction >= p.handoff_context_fraction
    if handoff:
        reasons.append("context_pressure")

    # A host must finish/abort its critical operation first. The need for
    # review persists in the caller's counters; do not silently reset them.
    if c.currently_in_critical_action and (reasons or handoff):
        return CheckpointDecision("continue", ("defer_until_safe_boundary", *reasons),
                                  ("Finish or safely abort the in-flight operation.",))

    if handoff:
        return CheckpointDecision("handoff", tuple(reasons), HANDOFF_CHECKS)
    if reasons:
        return CheckpointDecision("review", tuple(reasons), REVIEW_CHECKS)
    return CheckpointDecision("continue", (), ())


def make_restart_packet(*, objective: str, acceptance: list[str],
                        verified: list[str], evidence_refs: list[str],
                        blockers: list[str], next_action: str,
                        tool_versions: dict[str, str]) -> dict:
    """Construct a compact handoff. Fields are caller-provided and NOT verified."""
    if not objective.strip() or not acceptance or not next_action.strip():
        raise ValueError("Objective, acceptance criteria and next action required")
    return {
        "format": "vibe-optimizer/restart-packet/v1",
        "objective": objective,
        "acceptance_criteria": list(acceptance),
        "claimed_verified_work": list(verified),
        "evidence_references": list(evidence_refs),
        "unresolved_blockers": list(blockers),
        "next_permitted_action": next_action,
        "tool_versions": dict(tool_versions),
        "evidence_reviewed_by_host": False,
    }
