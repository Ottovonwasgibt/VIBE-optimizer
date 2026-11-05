"""Deterministic sensitivity test for watchdog policy thresholds.

Vary pacing and noisy observations across *synthetic*, hand-authored cases.
No LLM is run, and alerts never change future events. This is a stress test
of the policy/measurement harness, NOT evidence of better agent outcomes.
"""
from __future__ import annotations

from dataclasses import replace
import argparse
import json
import random
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from replay import Scenario, scenarios, replay_one
from vibe_optimizer.checkpoint_watchdog import CheckpointPolicy


def perturb(base: Scenario, rng: random.Random, repeat: int) -> Scenario:
    """Inject variability into counters without using hidden anomaly label.

    The fixture's onset and class are evaluator-only and never used in the
    mutation decisions. We preserve trusted unsafe-operation and critical
    action signals; noise concerns timing, context and imperfect diagnostics.
    """
    pace = rng.uniform(0.7, 1.4)
    last_elapsed = 0
    changed = []
    for event in base.events:
        elapsed = max(last_elapsed + 1,
                      round(event.elapsed_seconds * pace + rng.uniform(-8, 8)))
        last_elapsed = elapsed
        # An external fit signal may be intermittent (not present) even when
        # a specialized tool would be useful.
        tool_fit = event.tool_fit_evidence and rng.random() >= .15
        stall = max(0, event.actions_without_verified_progress +
                    rng.choice((-2, -1, 0, 0, 1, 2)))
        fallback = max(0, event.fallback_tool_streak +
                       rng.choice((-2, -1, 0, 0, 1, 2)))
        failures = event.consecutive_failures
        if failures and rng.random() < .1:
            failures = max(0, failures - rng.randint(1, 2))
        context = max(0.0, min(1.0,
                     event.context_fraction + rng.uniform(-.035, .035)))
        changed.append(replace(
            event,
            elapsed_seconds=elapsed,
            consecutive_failures=failures,
            actions_without_verified_progress=stall,
            fallback_tool_streak=fallback,
            tool_fit_evidence=tool_fit,
            context_fraction=context,
        ))
    return replace(base, name=f"{base.name}_j{repeat:03d}", events=tuple(changed))


def fixture_family(seed: int, repeats: int) -> tuple[Scenario, ...]:
    if repeats < 1 or repeats > 300:
        raise ValueError("repeats must be 1..300")
    rng = random.Random(seed)
    return tuple(perturb(base, rng, repeat)
                 for base in scenarios() for repeat in range(repeats))


def candidate_policies() -> dict[str, CheckpointPolicy]:
    """Predeclared variants, not tuned against data from this experiment."""
    huge = 10**9
    return {
        "events_only": CheckpointPolicy(
            max_elapsed_seconds=huge, max_tool_calls=huge),
        "frequent_10m_12calls": CheckpointPolicy(
            max_elapsed_seconds=600, max_tool_calls=12),
        "balanced_20m_25calls": CheckpointPolicy(
            max_elapsed_seconds=1200, max_tool_calls=25),
        "relaxed_30m_40calls": CheckpointPolicy(
            max_elapsed_seconds=1800, max_tool_calls=40),
        "noisy_signal_tolerant": CheckpointPolicy(
            max_elapsed_seconds=1200, max_tool_calls=25,
            max_failed_attempts=4, max_unverified_actions=22,
            max_fallback_tool_streak=9),
    }


def measure(fixture: tuple[Scenario, ...], policy: CheckpointPolicy) -> dict:
    # The replay runner's special name invokes the same gated reminder policy
    # for every threshold variant. In-flight critical actions are deferred.
    rows = [replay_one(s, "hybrid_gated", policy) for s in fixture]
    positives = [r for r in rows if r["category"] != "negative"]
    negatives = [r for r in rows if r["category"] == "negative"]
    delays = [r["delay_steps"] for r in positives if
              r["detected_after_onset"] and r["delay_steps"] is not None]
    return {
        "positive_traces": len(positives),
        "detected_traces": sum(r["detected_after_onset"] for r in positives),
        "negative_traces": len(negatives),
        "negative_traces_with_alert": sum(r["alert_count"] > 0 for r in negatives),
        "false_alerts_on_negative_traces": sum(r["alert_count"] for r in negatives),
        "total_alerts": sum(r["alert_count"] for r in rows),
        "mean_detection_delay_steps": (
            round(sum(delays)/len(delays), 2) if delays else None),
        # A diagnostic alert during healthy long work is not an established
        # error: it is counted as an interruption for comparison.
    }


def evaluate(repeats: int = 20, development_seed: int = 2026,
             holdout_seed: int = 2027) -> dict:
    policies = candidate_policies()
    if development_seed == holdout_seed:
        raise ValueError("Development and holdout perturbations must differ")
    out = {}
    for split, seed in (("development", development_seed),
                        ("holdout", holdout_seed)):
        fixture = fixture_family(seed, repeats)
        out[split] = {label: measure(fixture, policy)
                      for label, policy in policies.items()}
    return {
        "status": "policy stress test on simulated traces; not an LLM experiment",
        "randomization": "seeded pacing and measurement noise; base case templates shared",
        "repeats_per_base_scenario": repeats,
        "base_scenarios": len(scenarios()),
        "caveat": ("Development and holdout differ only in random perturbations "
                   "of the SAME author-designed base cases; no independent task "
                   "distribution, causal policy benefit or statistical generality."),
        "results": out,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeats", type=int, default=20)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = evaluate(repeats=args.repeats)
    print(json.dumps(output["results"], indent=2))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(output, indent=2) + "\n",
                               encoding="utf-8")


if __name__ == "__main__":
    main()
