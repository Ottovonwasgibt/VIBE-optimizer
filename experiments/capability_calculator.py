"""Illustrative cost and capability calculations; never measured agent performance.

The chained probabilities are nested conditional stage rates. Completeness
assumes independence and is only a toy reference. Utility values must use
consistent units; do not treat model confidence as calibrated probabilities.
"""
from __future__ import annotations

import argparse
import json
import math
from typing import Sequence


def _prob(x: float) -> float:
    if not math.isfinite(x) or not 0 <= x <= 1:
        raise ValueError(f"Expected probability in [0,1], got {x!r}")
    return x


def funnel(rates: Sequence[float]) -> float:
    """Joint event probability from nested conditional stage frequencies."""
    if not rates:
        raise ValueError("At least one stage required")
    return math.prod(_prob(float(r)) for r in rates)


def completeness_independent(recall_per_tool: float, required_tools: int) -> float:
    """Toy formula; assumes independent, identical retrieval events."""
    if required_tools < 1:
        raise ValueError("Must require at least one tool")
    return _prob(recall_per_tool) ** required_tools


def probe_value(p_gap: float, conditional_lift: float, task_value: float,
                probe_cost: float, risk_cost: float) -> dict:
    for value in (conditional_lift, task_value, probe_cost, risk_cost):
        if not math.isfinite(value) or value < 0:
            raise ValueError("Lift/value/costs must be nonnegative and finite")
    _prob(p_gap)
    _prob(conditional_lift)
    ev = p_gap * conditional_lift * task_value - probe_cost - risk_cost
    denom = conditional_lift * task_value
    threshold = (probe_cost + risk_cost) / denom if denom else None
    return {"net_expected_utility": ev,
            "minimum_p_gap_to_justify_probe": threshold,
            "probe_positive_utility": ev > 0}


def reuse_breakeven(build_cost: float, validation_cost: float,
                    maintenance_cost: float, applicability: float,
                    savings_per_use: float) -> int | None:
    for value in (build_cost, validation_cost, maintenance_cost, savings_per_use):
        if not math.isfinite(value) or value < 0:
            raise ValueError("Time/costs must be nonnegative and finite")
    _prob(applicability)
    gain = applicability * savings_per_use
    return math.ceil((build_cost + validation_cost + maintenance_cost) / gain) if gain else None


def context_budget(total_tools: int, average_tokens: int,
                   active_tools: int, search_tokens: int) -> dict:
    if min(total_tools, average_tokens, active_tools, search_tokens) < 0 or active_tools > total_tools:
        raise ValueError("Invalid tool/token counts")
    static = total_tools * average_tokens
    dynamic = search_tokens + active_tools * average_tokens
    return {"static_tokens": static, "dynamic_tokens": dynamic,
            "saved_tokens": static - dynamic,
            "saved_fraction": (static - dynamic) / static if static else None}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="model", required=True)
    f = sub.add_parser("funnel")
    f.add_argument("--baseline", nargs="+", type=float, required=True)
    f.add_argument("--enhanced", nargs="+", type=float, required=True)
    c = sub.add_parser("completeness")
    c.add_argument("--recall", type=float, required=True)
    c.add_argument("--tools", type=int, required=True)
    p = sub.add_parser("probe")
    for n in ("p-gap", "lift", "value", "probe-cost", "risk-cost"):
        p.add_argument("--" + n, type=float, required=True)
    r = sub.add_parser("reuse")
    for n in ("build", "validation", "maintenance", "applicability", "saved-per-use"):
        r.add_argument("--" + n, type=float, required=True)
    x = sub.add_parser("context")
    for n in ("total", "schema-tokens", "active", "search-tokens"):
        x.add_argument("--" + n, type=int, required=True)
    a = parser.parse_args()
    if a.model == "funnel":
        if len(a.baseline) != len(a.enhanced):
            parser.error("Baseline and enhanced must have the same number of stages")
        b, e = funnel(a.baseline), funnel(a.enhanced)
        out = {"baseline": b, "enhanced": e, "difference_pp": (e-b)*100,
               "note": "synthetic conditional funnel, not empirical performance"}
    elif a.model == "completeness":
        out = {"joint_coverage": completeness_independent(a.recall, a.tools),
               "assumption": "independent, identically distributed discovery events"}
    elif a.model == "probe":
        out = probe_value(a.p_gap, a.lift, a.value, a.probe_cost, a.risk_cost)
    elif a.model == "reuse":
        out = {"minimum_future_uses": reuse_breakeven(a.build, a.validation,
            a.maintenance, a.applicability, a.saved_per_use)}
    else:
        out = context_budget(a.total, a.schema_tokens, a.active, a.search_tokens)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
