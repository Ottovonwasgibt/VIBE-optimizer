"""Reminder delivery gate for an external agent supervisor.

Distinguishes a checkpoint *decision* from sending a reminder. Repeated
identical warnings are rate-limited; new reasons and safety halts are not.
The state is process-owned, never agent-self-reported. It does not prove that
the review was completed; only a trusted host can acknowledge one.
"""
from __future__ import annotations

from dataclasses import dataclass
from vibe_optimizer.checkpoint_watchdog import CheckpointDecision


@dataclass(frozen=True)
class GateState:
    last_emitted_step: int | None = None
    last_reasons: frozenset[str] = frozenset()
    handoff_pending: bool = False


def gate_alert(decision: CheckpointDecision, step: int, state: GateState,
               *, cooldown_steps: int = 8) -> tuple[bool, GateState]:
    """Returns (emit, updated state); one step is one observed host event."""
    if step < 1 or cooldown_steps < 1:
        raise ValueError("Step/cooldown must be positive")
    if state.last_emitted_step is not None and step <= state.last_emitted_step:
        raise ValueError("Host events must be monotonically numbered")
    if decision.action == "halt":
        return True, state
    if decision.action == "continue":
        # Re-arm after a successful normal, condition-free observation. A
        # deferred critical action is different: preserve the pending state.
        if not decision.reasons:
            return False, GateState(handoff_pending=state.handoff_pending)
        return False, state
    if decision.action == "handoff":
        if state.handoff_pending:
            return False, state
        return True, GateState(step, frozenset(decision.reasons), True)

    reasons = frozenset(decision.reasons)
    new_cause = bool(reasons - state.last_reasons)
    eligible = (state.last_emitted_step is None or new_cause or
                step - state.last_emitted_step >= cooldown_steps)
    if eligible:
        return True, GateState(step, reasons, state.handoff_pending)
    return False, state


def acknowledge_handoff(state: GateState, *, host_reviewed: bool) -> GateState:
    """Only a trusted host may confirm handoff completion.

    This function itself cannot verify a model claim; caller enforcement
    is a deployment requirement.
    """
    if not host_reviewed:
        return state
    return GateState()
