"""Strict paired evaluation report for the same fixed agent/model.

Consumes externally graded task OUTCOMES only. It does not launch Vibe,
read private prompts, execute candidate tools or independently verify a
claimed verifier. Keep private task keys and restricted evidence off GitHub.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


_ROOT = frozenset({
    "schema_version", "study_id", "evidence_status",
    "model", "model_version", "budget_tokens", "budget_tool_calls",
    "results"
})
_ROW = frozenset({
    "task_id", "repetition", "variant", "solved", "safety_violation",
    "tokens_used", "tool_calls", "elapsed_seconds", "verifier_ref"
})


def _validate(data: dict) -> dict[str, dict[tuple[str, int], dict]]:
    if not isinstance(data, dict) or set(data) != _ROOT:
        raise ValueError("Study has unknown or missing fields")
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise ValueError("Unsupported evaluation schema")
    if data["evidence_status"] not in ("synthetic", "externally_graded_claim"):
        raise ValueError("Evidence status must be explicit")
    if not all(isinstance(data[k], str) and 1 <= len(data[k]) <= 120
               for k in ("study_id", "model", "model_version")):
        raise ValueError("Pinned model and study IDs required")
    for k in ("budget_tokens", "budget_tool_calls"):
        if type(data[k]) is not int or data[k] <= 0:
            raise ValueError("Fixed positive per-run budget required")
    rows = data["results"]
    if not isinstance(rows, list) or not rows or len(rows) > 100000:
        raise ValueError("Invalid result list")
    variants: dict[str, dict[tuple[str, int], dict]] = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != _ROW:
            raise ValueError("Result row has unknown or missing fields")
        if not all(isinstance(row[k], str) and 1 <= len(row[k]) <= 160
                   for k in ("task_id", "variant", "verifier_ref")):
            raise ValueError("Missing task/variant/verifier provenance")
        if type(row["repetition"]) is not int or row["repetition"] < 0:
            raise ValueError("Invalid repetition number")
        if type(row["solved"]) is not bool or type(row["safety_violation"]) is not bool:
            raise ValueError("Solved/safety flags must be boolean")
        if not all(type(row[k]) is int and row[k] >= 0
                   for k in ("tokens_used", "tool_calls")):
            raise ValueError("Invalid usage counters")
        if type(row["elapsed_seconds"]) not in (int, float):
            raise ValueError("Elapsed must be a number")
        if not math.isfinite(row["elapsed_seconds"]) or row["elapsed_seconds"] < 0:
            raise ValueError("Invalid elapsed time")
        if row["tokens_used"] > data["budget_tokens"] or row["tool_calls"] > data["budget_tool_calls"]:
            raise ValueError("Run exceeded declared comparison budget")
        if row["solved"] and row["safety_violation"]:
            # Retain this as unsafe success, never score it as a safe solution.
            pass
        key = (row["task_id"], row["repetition"])
        group = variants.setdefault(row["variant"], {})
        if key in group:
            raise ValueError("Duplicate task/repetition/variant")
        group[key] = row
    if "baseline" not in variants or len(variants) < 2:
        raise ValueError("Baseline and at least one intervention required")
    keys = set(variants["baseline"])
    if any(set(v) != keys for v in variants.values()):
        raise ValueError("Strict matched-task/repetition comparisons only")
    return variants


def _p_sign_test(gains: int, losses: int) -> float | None:
    """Exact paired sign-test p-value for discordant binary outcomes.

    Descriptive exploratory test; no adjustment for multiple hypotheses,
    benchmark selection or repeated correlated trials. No p if tied only.
    """
    n = gains + losses
    if n == 0:
        return None
    k = min(gains, losses)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / (2**n))


def report(data: dict) -> dict:
    variants = _validate(data)
    keys = sorted(variants["baseline"])
    n = len(keys)
    base = variants["baseline"]

    def good(row: dict) -> bool:
        return row["solved"] and not row["safety_violation"]

    def summary(group: dict) -> dict:
        runs = list(group.values())
        return {
            "runs": len(runs),
            "safe_solved": sum(good(x) for x in runs),
            "safe_solved_rate": round(sum(good(x) for x in runs) / len(runs), 6),
            "safety_incidents": sum(x["safety_violation"] for x in runs),
            "mean_tokens_used": round(sum(x["tokens_used"] for x in runs)/len(runs),1),
            "mean_tool_calls": round(sum(x["tool_calls"] for x in runs)/len(runs),2),
            "mean_elapsed_seconds": round(sum(x["elapsed_seconds"] for x in runs)/len(runs),2),
        }

    comparisons = {}
    for name, current in variants.items():
        if name == "baseline":
            continue
        gains = sum(not good(base[k]) and good(current[k]) for k in keys)
        losses = sum(good(base[k]) and not good(current[k]) for k in keys)
        comparisons[name] = {
            "matched_pairs": n, "baseline_only_failures_fixed": gains,
            "baseline_successes_lost": losses,
            "net_difference_pp": round((gains-losses) * 100 / n, 3),
            "paired_sign_test_p_unadjusted": _p_sign_test(gains, losses),
            "warning": "Descriptive exploratory statistic; not proof of causation"
        }
    return {
        "study_id": data["study_id"],
        "evidence_status": data["evidence_status"],
        "model": data["model"],
        "model_version": data["model_version"],
        "fixed_per_run_budgets": {
            "tokens": data["budget_tokens"],
            "tool_calls": data["budget_tool_calls"],
        },
        "variants": {name: summary(g) for name, g in variants.items()},
        "paired_comparisons": comparisons,
        "interpretation": (
            "Synthetic records or unverified external-grader claims only. "
            "Actual task verification, model identity and treatment assignment "
            "must be audited outside this program."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results_json", type=Path)
    args = parser.parse_args()
    data = json.loads(args.results_json.read_text(encoding="utf-8"))
    print(json.dumps(report(data), indent=2))


if __name__ == "__main__":
    main()
