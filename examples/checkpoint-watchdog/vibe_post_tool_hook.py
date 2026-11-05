"""Optional Mistral Vibe post_tool hook: periodically nudge agent reorientation.

Not installed automatically. Uses only validated session ID, tool outcome and
call counters; does NOT store prompts, arguments, response bodies, paths or
identifying source data. Emits model-visible additional_context when due.
A Vibe hook is not an independent timer: it fires only after executed tools.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from vibe_optimizer.checkpoint_watchdog import SessionCounters, decide


MESSAGE = (
    "[VIBE-optimizer checkpoint — host-triggered] "
    "Check the original objective and acceptance criteria. "
    "Separate verified progress from assumptions; identify repeated failures. "
    "Ask whether a suitable tool/skill is available but unused, and whether "
    "your next step is the most informative safe action. "
    "If context or strategy needs a reset, prepare an evidence-linked handoff. "
    "Do not claim a check passed without actual test evidence."
)


def _storage_path() -> Path:
    # The environment value must be configured by the trusted host, never by model output.
    override = os.environ.get("VIBE_OPTIMIZER_WATCHDOG_DB")
    return (Path(override).expanduser() if override
            else Path.cwd() / ".vibe" / "data" / "checkpoint-watchdog.sqlite")


def _failed_tool(payload: dict) -> bool:
    if payload.get("tool_status") == "failure":
        return True
    # A shell tool can report tool_status=success even on a nonzero process returncode.
    output = payload.get("tool_output")
    if isinstance(output, dict):
        returncode = output.get("returncode")
        if isinstance(returncode, int) and not isinstance(returncode, bool):
            return returncode != 0
    return False


def handle_event(payload: dict, *, database: Path | None = None,
                 now: float | None = None) -> dict | None:
    """Parse a Vibe event; return protocol JSON or None for empty passthrough.

    Intended to be called only from a trusted Vibe post_tool lifecycle hook;
    session ID must come from the host. The model cannot directly pass a trusted
    session ID in this command's arguments.
    """
    if payload.get("hook_event_name") not in ("post_tool", "post_tool_use"):
        return None
    sid = payload.get("session_id")
    if not isinstance(sid, str) or not 1 <= len(sid) <= 256:
        return None
    current = time.time() if now is None else float(now)
    sid_hash = hashlib.sha256(sid.encode("utf-8")).hexdigest()
    db = database or _storage_path()
    db.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db, timeout=5) as con:
        con.execute("PRAGMA busy_timeout=5000")
        con.execute(
            "CREATE TABLE IF NOT EXISTS sessions "
            "(sid TEXT PRIMARY KEY, last_nudge REAL NOT NULL, "
            "tool_calls INTEGER NOT NULL, failed_streak INTEGER NOT NULL)"
        )
        con.execute("BEGIN IMMEDIATE")
        row = con.execute(
            "SELECT last_nudge, tool_calls, failed_streak FROM sessions WHERE sid=?",
            (sid_hash,),
        ).fetchone()
        last_nudge, calls, failures = row if row else (current, 0, 0)
        calls += 1
        failures = failures + 1 if _failed_tool(payload) else 0

        # A nudge is not proof of completed review or true verified progress;
        # counters measure time and calls since last emitted reminder only.
        counters = SessionCounters(
            elapsed_seconds=max(0, int(current - last_nudge)),
            tool_calls=calls,
            consecutive_failures=failures,
        )
        decision = decide(counters)
        if decision.action == "review":
            con.execute(
                "INSERT INTO sessions(sid,last_nudge,tool_calls,failed_streak) "
                "VALUES(?,?,?,?) ON CONFLICT(sid) DO UPDATE SET "
                "last_nudge=excluded.last_nudge,tool_calls=excluded.tool_calls,"
                "failed_streak=excluded.failed_streak",
                (sid_hash, current, 0, 0),
            )
        else:
            con.execute(
                "INSERT INTO sessions(sid,last_nudge,tool_calls,failed_streak) "
                "VALUES(?,?,?,?) ON CONFLICT(sid) DO UPDATE SET "
                "last_nudge=excluded.last_nudge,tool_calls=excluded.tool_calls,"
                "failed_streak=excluded.failed_streak",
                (sid_hash, last_nudge, calls, failures),
            )

    if decision.action == "review":
        return {
            "hook_specific_output": {
                "additional_context": MESSAGE + " Trigger: " + ", ".join(decision.reasons)
            }
        }
    return None


def main() -> None:
    payload = json.load(sys.stdin)
    result = handle_event(payload)
    if result is not None:
        print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
