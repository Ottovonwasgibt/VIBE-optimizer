"""One-shot demo of a host-provided checkpoint event (not an installed Vibe hook).

Run from repository root:
    python examples/checkpoint-watchdog/check.py --demo
    python examples/checkpoint-watchdog/check.py path/to/metrics.json

Input JSON is simulated, NOT authenticated model/session telemetry.
The output is a recommendation. A cooperating agent host must deliver it.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from vibe_optimizer.checkpoint_watchdog import SessionCounters, decide


DEMO = {
    "elapsed_seconds": 720,
    "tool_calls": 15,
    "consecutive_failures": 1,
    "actions_without_verified_progress": 10,
    "fallback_tool_streak": 8,
    "tool_fit_evidence": True,
    "context_fraction": 0.42,
    "unsafe_operation_detected": False,
    "currently_in_critical_action": False,
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("event_file", nargs="?", type=Path)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo and args.event_file:
        parser.error("Use --demo or event_file")
    if not args.demo and args.event_file is None:
        parser.error("Provide a JSON event file or --demo")
    raw = DEMO if args.demo else json.loads(
        args.event_file.read_text(encoding="utf-8")
    )
    counters = SessionCounters(**raw)
    result = decide(counters)
    print(json.dumps({
        "checkpoint": result.as_dict(),
        "metrics": asdict(counters),
        "warning": "Prototype only: does not interrupt or instruct live Vibe sessions"
    }, indent=2))


if __name__ == "__main__":
    main()
