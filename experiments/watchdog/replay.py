"""Deterministic replay experiment for checkpoint strategies.

NOT an agent evaluation: sessions and anomaly labels are synthetic and
hand-designed. The replay does not alter model behavior after a reminder.
Use it to examine notification sensitivity/cost and regression-test thresholds,
not to infer task completion or causal performance improvement.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from vibe_optimizer.checkpoint_watchdog import (
    CheckpointPolicy, SessionCounters, decide
)


@dataclass(frozen=True)
class Scenario:
    name: str
    category: str
    events: tuple[SessionCounters, ...]
    anomaly_onset: int | None = None  # 1-indexed, independently assigned in fixture
    note: str = ""


def timeline(n: int, seconds_per_step: int = 35) -> list[SessionCounters]:
    """Synthetic completed-tool events; the clock doesn't fire between events."""
    return [
        SessionCounters(elapsed_seconds=i * seconds_per_step, tool_calls=i)
        for i in range(1, n + 1)
    ]


def scenarios() -> tuple[Scenario, ...]:
    s = []
    s.append(Scenario("healthy_short", "negative", tuple(timeline(12)),
                      note="Brief productive session; no checkpoint warranted"))
    s.append(Scenario("healthy_long", "negative", tuple(timeline(38, 55)),
                      note="Long productive session, potential interval false alarms"))
    s.append(Scenario("generic_tool_appropriate", "negative",
                      tuple(replace(x, fallback_tool_streak=i,
                                    tool_fit_evidence=False)
                            for i, x in enumerate(timeline(30, 30), 1)),
                      note="Generic search is suitable; no specialized tool needed"))
    s.append(Scenario("slow_legitimate_review", "negative",
                      tuple(replace(x, actions_without_verified_progress=i)
                            for i, x in enumerate(timeline(15, 90), 1)),
                      note="Thought-intensive investigation without fast test oracle"))
    s.append(Scenario("repeat_failures", "positive",
                      tuple(replace(x, consecutive_failures=max(0, i - 8))
                            for i, x in enumerate(timeline(18), 1)),
                      anomaly_onset=9,
                      note="Several repeated failures after step 8"))
    s.append(Scenario("specialized_tool_ignored", "positive",
                      tuple(replace(x,
                                    fallback_tool_streak=max(0, i - 4),
                                    tool_fit_evidence=i >= 5)
                            for i, x in enumerate(timeline(22), 1)),
                      anomaly_onset=5,
                      note="Confirmed appropriate tool, yet generic fallback continues"))
    s.append(Scenario("verified_progress_stall", "positive",
                      tuple(replace(x,
                                    actions_without_verified_progress=max(0, i - 3))
                            for i, x in enumerate(timeline(28, 25), 1)),
                      anomaly_onset=11,
                      note="Independent checks cease producing verifiable progress"))
    s.append(Scenario("context_pressure", "positive",
                      tuple(replace(x, context_fraction=min(.99, .06*i))
                            for i, x in enumerate(timeline(19), 1)),
                      anomaly_onset=13,
                      note="Estimated active context reaches high utilization"))
    s.append(Scenario("safe_boundary_deferral", "positive",
                      tuple(replace(x, currently_in_critical_action=(i in (24,25,26)))
                            for i, x in enumerate(timeline(29, 30), 1)),
                      anomaly_onset=25,
                      note="Threshold occurs while an operation is in flight"))
    s.append(Scenario("unsafe_operation", "safety",
                      tuple(replace(x, unsafe_operation_detected=(i == 8))
                            for i, x in enumerate(timeline(10), 1)),
                      anomaly_onset=8,
                      note="Trusted external signal of unsafe operation"))
    return tuple(s)


def policies() -> dict[str, CheckpointPolicy | None]:
    huge = 10**9
    return {
        "baseline": None,
        "interval_only": CheckpointPolicy(
            max_elapsed_seconds=1200, max_tool_calls=25,
            max_failed_attempts=huge, max_unverified_actions=huge,
            max_fallback_tool_streak=huge, handoff_context_fraction=1.0),
        "event_only": CheckpointPolicy(
            max_elapsed_seconds=huge, max_tool_calls=huge,
            max_failed_attempts=3, max_unverified_actions=18,
            max_fallback_tool_streak=7, handoff_context_fraction=.85),
        "hybrid": CheckpointPolicy(),
    }


def replay_one(s: Scenario, name: str, policy: CheckpointPolicy | None) -> dict:
    alerts: list[dict] = []
    # Records are deliberately immutable synthetic observations. The replay
    # cannot assume a model responds to reminders or changes course.
    # An in-progress critical action postpones a review until the next safe event.
    for step, metrics in enumerate(s.events, start=1):
        if policy is None:
            continue
        decision = decide(metrics, policy)
        if decision.action == "continue":
            continue
        alerts.append({
            "step": step, "action": decision.action,
            "reasons": list(decision.reasons)
        })

    eligible = s.category in {"positive", "safety"}
    post_onset = ([a for a in alerts if a["step"] >= s.anomaly_onset]
                  if eligible else [])
    first = post_onset[0]["step"] if post_onset else None
    correct_type = (not eligible or
                    any(a["action"] == "halt" for a in post_onset)
                    if s.category == "safety" else
                    any(a["action"] in ("review","handoff","halt") for a in post_onset))
    return {
        "scenario": s.name,
        "category": s.category,
        "onset_step": s.anomaly_onset,
        "strategy": name,
        "alert_count": len(alerts),
        "false_alert_count": len(alerts) if not eligible else
                             sum(a["step"] < s.anomaly_onset for a in alerts),
        "detected_after_onset": bool(post_onset) and correct_type,
        "first_detected_step": first,
        "delay_steps": first - s.anomaly_onset if first is not None else None,
        "alerts": alerts,
    }


def run() -> dict:
    testcases = scenarios()
    configs = policies()
    rows = [replay_one(s, name, policy)
            for name, policy in configs.items() for s in testcases]
    summaries = {}
    for name in configs:
        subset = [r for r in rows if r["strategy"] == name]
        positives = [r for r in subset if r["category"] != "negative"]
        negatives = [r for r in subset if r["category"] == "negative"]
        delays = [r["delay_steps"] for r in positives
                  if r["delay_steps"] is not None and r["detected_after_onset"]]
        summaries[name] = {
            "synthetic_positive_detected": sum(r["detected_after_onset"] for r in positives),
            "synthetic_positive_total": len(positives),
            "false_alarms_on_negative_traces": sum(r["alert_count"] for r in negatives),
            "negative_traces_with_any_alert": sum(r["alert_count"] > 0 for r in negatives),
            "negative_traces_total": len(negatives),
            "total_alerts": sum(r["alert_count"] for r in subset),
            "mean_detection_delay_steps": round(sum(delays)/len(delays), 2) if delays else None,
        }
    return {
        "status": "synthetic-policy-only; no Vibe or LLM run, no causal inference",
        "scenarios": len(testcases),
        "positive_scenarios": sum(s.category in ("positive","safety") for s in testcases),
        "negative_scenarios": sum(s.category == "negative" for s in testcases),
        "summary": summaries,
        "details": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    args = parser.parse_args()
    result = run()
    print(json.dumps(result["summary"], indent=2))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
