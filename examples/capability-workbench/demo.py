"""Run advisory-only cross-domain demo with fictional evidence.

    python examples/capability-workbench/demo.py

Does not connect to Vibe, install skills or read restricted data.
"""
from __future__ import annotations

from datetime import date
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from vibe_optimizer.capability_registry import CapabilityRegistry, TaskContext
from vibe_optimizer.task_router import Signals
from vibe_optimizer.evidence_packets import evidence_from_text
from vibe_optimizer.capability_loop import advise
from vibe_optimizer.checkpoint_watchdog import SessionCounters

REGISTRY = ROOT / "examples" / "capability-workbench" / "catalog.json"


def main() -> None:
    reg = CapabilityRegistry.load(REGISTRY)
    today = date(2026, 11, 5)
    tasks = [
        (
            "SYNTHETIC-API",
            TaskContext(
                "Pydantic v2 model validation API", "windows",
                versions=(("pydantic", "2"),),
            ),
            "Exact v2 interface is requested. Legacy API examples are not "
            "automatically evidence of v2 suitability.",
        ),
        (
            "SYNTHETIC-HO",
            TaskContext(
                "Studielink Osiris enrollment status process", "windows"
            ),
            "Fictional workflow: a message is received but manual review is "
            "pending. This text is NOT a real institutional status mapping.",
        ),
    ]
    for task_id, ctx, text in tasks:
        evidence = [evidence_from_text(
            source_id=task_id.lower(), locator="fixture-1",
            revision="synthetic-v1", topic=task_id, excerpt=text,
            observed_at=today
        )]
        result = advise(
            task_id=task_id, context=ctx,
            signals=Signals(criteria_clear=True,
                            external_capability_needed=True,
                            target_version_known=True),
            registry=reg, evidence=evidence, date_of_use=today,
            checkpoint=SessionCounters(tool_calls=25 if task_id.endswith("HO") else 1),
        )
        print(json.dumps(result.as_dict(), indent=2))
    print("NO tools executed, models called, permissions added or memories approved.")


if __name__ == "__main__":
    main()
