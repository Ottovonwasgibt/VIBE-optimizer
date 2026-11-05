---
name: checkpoint-review
description: Use after repeated tool errors, loss of verified progress, unexpectedly long sessions, or when a host checkpoint prompts reorientation. Do not run at every small successful action.
user-invocable: true
---

# Brief evidence-based reorientation

This procedure is a checkpoint, not a new objective or a reason to restart unnecessarily.

1. Re-read the original objective, known constraints and acceptance checks from source-of-truth records.
2. Record what is independently established (tests, files, timestamps, authorized observations). Label model-generated explanations as hypotheses.
3. Look for drift: abandoned constraints, repeated errors, unnecessary calls, a more suitable available tool or stale/version-mismatched evidence.
4. Decide: continue with one concrete next observation; switch approved tool; escalate; or prepare a fresh-context handoff. Avoid speculative tool installation.
5. If restarting, provide objective, acceptance checks, verified progress with pointers, blockers, revisions, environment, pending approvals and the next safe action. No sensitive transcripts in public logs.
6. A reminder is **not proof** this review was done. Do not mark a test passed or memory verified without independently observed evidence.

**Return:** at most a brief checkpoint summary, a single next action and any genuine approval blockers.

Related: docs/TECHNICAL-DESIGNS/08-checkpoint-watchdog.md. This skill does not activate the watchdog hook or itself interrupt a running tool.
