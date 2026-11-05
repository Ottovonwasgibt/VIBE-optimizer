"""First integrated advisory loop for VIBE-optimizer.

Connects deficit triage, capability catalog, authorized evidence packets and
a checkpoint signal. It does NOT call an LLM, execute tools, install skills,
write to memory or authenticate users. The host retains ALL execution authority.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date

from vibe_optimizer.capability_registry import CapabilityRegistry, TaskContext
from vibe_optimizer.task_router import Signals, route_task
from vibe_optimizer.evidence_packets import Evidence, compile_packet
from vibe_optimizer.checkpoint_watchdog import SessionCounters, decide


@dataclass(frozen=True)
class AdvisoryResult:
    task: str
    next_action: str
    reason: str
    candidates: tuple[str, ...]
    evidence_packet: dict
    checkpoint: dict
    execution_status: str = "advisory_only_not_executed"

    def as_dict(self) -> dict:
        return asdict(self)


def advise(*, task_id: str, context: TaskContext, signals: Signals,
           registry: CapabilityRegistry, evidence: list[Evidence],
           date_of_use: date, checkpoint: SessionCounters | None = None,
           evidence_budget_chars: int = 1600) -> AdvisoryResult:
    route = route_task(context, signals, registry)
    packet = compile_packet(
        task_id=task_id, purpose=context.question, items=evidence,
        as_of=date_of_use,
        allowed_classes=context.permitted_classifications,
        max_chars=evidence_budget_chars,
    )
    status = decide(checkpoint or SessionCounters())
    return AdvisoryResult(
        task_id, route.next_action, route.reason, route.candidate_ids,
        packet, status.as_dict(),
    )
