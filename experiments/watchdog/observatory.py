"""Sanitized host-event trace contract and offline checkpoint replay.

This is a measurement adapter, NOT a Vibe hook or real-time enforcement.
The allowlist deliberately rejects free-text prompts, tool parameters, output,
document paths and personal/student information fields. Trace authors still
must use opaque IDs and ensure the source is permitted for analysis.

Only independently trusted observer labels may claim "verified" progress or
"suitable_tool_available"; a model's own self-report is insufficient.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from vibe_optimizer.checkpoint_watchdog import CheckpointPolicy, SessionCounters, decide
from vibe_optimizer.watchdog_gate import GateState, gate_alert


EVENT_KEYS = frozenset({
    "step", "elapsed_seconds", "tool_class", "tool_result",
    "progress", "tool_fit", "context_fraction", "critical_action",
    "unsafe_operation"
})
TOOL_CLASSES = frozenset({
    "generic", "specialized", "test", "read", "write", "other"
})
TOOL_RESULTS = frozenset({"success", "failure", "unknown"})
PROGRESS_RESULTS = frozenset({"verified", "not_verified", "unknown"})
TOOL_FIT_RESULTS = frozenset({"confirmed", "not_applicable", "unknown"})
MAX_EVENTS = 10000


def _expect_exact_keys(obj: dict, expected: frozenset[str], label: str) -> None:
    if not isinstance(obj, dict) or frozenset(obj.keys()) != expected:
        raise ValueError(f"{label} must contain only exact approved keys")


@dataclass(frozen=True)
class TraceEvent:
    step: int
    elapsed_seconds: int
    tool_class: str
    tool_result: str
    progress: str
    tool_fit: str
    context_fraction: float | None
    critical_action: bool
    unsafe_operation: bool


def load_trace(payload: dict) -> tuple[str, tuple[TraceEvent, ...]]:
    _expect_exact_keys(payload, frozenset({"schema_version", "trace_id", "events"}),
                       "trace")
    if type(payload["schema_version"]) is not int or payload["schema_version"] != 1:
        raise ValueError("Unsupported trace version")
    trace_id = payload["trace_id"]
    if not isinstance(trace_id, str) or not re.fullmatch(
            r"[A-Za-z0-9_-]{1,64}", trace_id):
        raise ValueError("Trace ID must be opaque and bounded")
    inputs = payload["events"]
    if not isinstance(inputs, list) or not 1 <= len(inputs) <= MAX_EVENTS:
        raise ValueError("Invalid event list size")
    events = []
    last_time = -1
    for i, entry in enumerate(inputs, 1):
        _expect_exact_keys(entry, EVENT_KEYS, f"event {i}")
        e = TraceEvent(**entry)
        if type(e.step) is not int or e.step != i:
            raise ValueError("Nonconsecutive event steps")
        if type(e.elapsed_seconds) is not int or e.elapsed_seconds < 0 or e.elapsed_seconds < last_time:
            raise ValueError("Non-monotonic event time")
        last_time = e.elapsed_seconds
        if (type(e.tool_class) is not str or type(e.tool_result) is not str or
            type(e.progress) is not str or type(e.tool_fit) is not str or
            e.tool_class not in TOOL_CLASSES or
            e.tool_result not in TOOL_RESULTS or
            e.progress not in PROGRESS_RESULTS or
            e.tool_fit not in TOOL_FIT_RESULTS):
            raise ValueError("Unknown event classification")
        if type(e.critical_action) is not bool or type(e.unsafe_operation) is not bool:
            raise ValueError("Invalid boolean")
        if e.context_fraction is not None and (
            type(e.context_fraction) not in (int, float) or
            not 0 <= e.context_fraction <= 1):
            raise ValueError("Context fraction must be 0..1 or null")
        events.append(e)
    return trace_id, tuple(events)


def metrics_from_events(events: tuple[TraceEvent, ...]) -> tuple[SessionCounters, ...]:
    failures = 0
    unverified = 0
    fallbacks = 0
    counters = []
    for i, e in enumerate(events, 1):
        # 'unknown' is NOT silently interpreted as a verified outcome.
        failures = failures + 1 if e.tool_result == "failure" else 0
        unverified = unverified + 1 if e.progress == "not_verified" else 0
        available = e.tool_fit == "confirmed"
        fallbacks = fallbacks + 1 if available and e.tool_class == "generic" else 0
        counters.append(SessionCounters(
            elapsed_seconds=e.elapsed_seconds,
            tool_calls=i,
            consecutive_failures=failures,
            actions_without_verified_progress=unverified,
            fallback_tool_streak=fallbacks,
            tool_fit_evidence=available,
            context_fraction=e.context_fraction if e.context_fraction is not None else 0.0,
            currently_in_critical_action=e.critical_action,
            unsafe_operation_detected=e.unsafe_operation,
        ))
    return tuple(counters)


def audit_trace(payload: dict, policy: CheckpointPolicy | None = None) -> dict:
    trace_id, events = load_trace(payload)
    state = GateState()
    alerts = []
    for step, metrics in enumerate(metrics_from_events(events), 1):
        decision = decide(metrics, policy)
        emit, state = gate_alert(decision, step, state)
        if emit:
            alerts.append({
                "step": step, "action": decision.action,
                "reasons": list(decision.reasons)
            })
    return {
        "trace_id": trace_id,
        "event_count": len(events),
        "alerts": alerts,
        "status": "offline analysis only; did not change a model's behavior",
        "provenance_note": "Progress and tool-fit labels require external verification",
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python observatory.py synthetic_trace.json")
    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(json.dumps(audit_trace(payload), indent=2))


if __name__ == "__main__":
    main()
