# TDD-10 — Checkpoint Watchdog, Agent Reorientation and Fresh-Context Handoffs

**Date:** 2026-11-05 · **Status:** design and tested policy prototype, **not** an active Mistral Vibe hook or background reminder.

## Insight

Humans sometimes return to familiar work habits during long, uninterrupted tasks, and a fresh pause can help them reconsider the goal and work methods. Tool-using agents exhibit **related operational failure patterns**: long-session instruction drift, overreliance on generic tools, lost constraints, stalls, premature completion and stale context.

Do **not** anthropomorphize the mechanism. An AI agent does not need biological rest. Its equivalent is an external, auditable **reorientation checkpoint**, followed when justified by a structured context handoff and fresh model session.

## Research grounding

- Serena maintainers explicitly describe agent drift: Claude Code can revert to generic search tools and neglect the Serena symbolic toolset as a session grows; hooks can remind the agent after repeated fallback calls: https://github.com/oraios/serena/blob/main/docs/02-usage/030_clients.md
- Ralph (community harness) starts each small story in fresh context, carrying Git state, a compact progress file and a task manifest: https://github.com/snarktank/ralph
- Anthropic, November 2025, discusses initializer/continuation routines and explicit progress state for long-running coding agents: https://www.anthropic.com/research/effective-harnesses-for-long-running-agents
- Anthropic, April 2026, describes prior context-reset adaptations against premature completion at context limits: https://www.anthropic.com/research/managed-agents
- Microsoft Research, October 2026, analyzes **13.5 million** GitHub Copilot sessions; its CompactionBench/APEC work finds a significant minority of sessions trigger expensive repeated context compaction and reports up to 25.4% lower cost and 9.6% shorter execution in measured settings: https://www.microsoft.com/en-us/research/publication/benchmarking-long-horizon-agent-context-compaction-with-compactionbench/
- Practitioners warn against continuously appending full progress history; index into task-relevant evidence rather than injecting entire logs: https://github.com/snarktank/ralph/issues/166

**Evidence caveat:** these are different tools and research environments, not direct validation that a periodic Vibe reminder improves its success rate. The preferred checkpoint interval is unknown and should be measured.

## Three mechanisms

**1. Interval-based inspection (external timer/counter).** Check after a configured number of minutes or tool calls. This catches slow drift when no obvious errors are emitted.

**2. Event-triggered inspection (independent signal).** Trigger sooner after consecutive failed attempts, long periods with no independently verified progress, or repeated fallback to generic tools **when a suitable specialized tool has independently been identified**. Security/scope issues always take precedence.

**3. Fresh-context handoff (not simply compaction).** Preserve original task, acceptance criteria, verified evidence and source pointers, changed files/configuration, tool versions, blockers and next safe action. An independent host checks the packet and restarts the agent only after an appropriate safe boundary.

## Decision states

| State | Meaning | External host behavior |
| --- | --- | --- |
| CONTINUE | no checkpoint needed | keep ordinary task execution |
| REVIEW | check goal, workbench, evidence, progression | inject compact prompt after safe tool boundary |
| HANDOFF | context pressure / scheduled restart | prepare an independently reviewed restart packet; new session by host |
| HALT | explicitly unsafe operation detected | stop sensitive action and request authorized review |

**Default proof-of-concept settings (not scientifically optimized):** 20 minutes or 25 tool calls, three consecutive failures, 18 actions without verified progress, seven fallback calls with evidence that another suitable tool exists, or 85% context utilization prompting handoff. Different tasks will need different thresholds.

Do not reset watchdog counters merely because the model says "I reviewed it." Use a trusted host acknowledgement of a completed checkpoint. A periodic prompt alone without a host integration will not interrupt an autonomous session.

## Proposed working model

~~~text
Host event / completed tool call
      |
Collect observed counters, progress and suitability evidence
      |
[deterministic checkpoint policy]
  | CONTINUE        -> normal step
  | REVIEW          -> compact reorientation prompt
  | HANDOFF         -> safe snapshot and source-backed restart packet
  | HALT            -> stop and authorized human review
      |
Checkpoint receipt with timestamp and reason
      |
Resume from validated objective, tools and sources
~~~

The watchdog **must not interrupt an in-flight write, production transaction, migration or file operation**. At such a boundary, defer until the host can safely finish or abort. A genuine safety violation is treated specially and should block further sensitive operations.

## Concrete implementation

- [Policy module](../../src/vibe_optimizer/checkpoint_watchdog.py): pure deterministic policy with typed counters, reason codes, and restart packet helper.
- [Unit tests](../../tests/test_checkpoint_watchdog.py): intervals, stalls, observed tool drift, context pressure, safe-boundary deferral, priority, invalid configuration and packet shape.
- [Host-agnostic example script](../../examples/checkpoint-watchdog/check.py): consumes JSON event input, prints JSON outcome; **not** an installed Vibe hook.

**Integration still required:** Mistral Vibe must expose or permit a reliable tool-completion/session event source or a controlling external harness. The actual event and plug-in APIs need to be verified against the installed Vibe version. We cannot assume every agent host supports arbitrary periodic hook injection. A supervisor process can evaluate a policy, but only a cooperating host can display or act on the result.

## Reorientation questions to ask the agent

1. What is the original task, including constraints and desired outcome?
2. What has actually been verified? Link tool/test output, don't rely on a narrative.
3. Have I changed objectives or fallen back to familiar but unsuitable tools?
4. Does the next action need a different tool, updated source, or extra verification?
5. What would falsify my current diagnosis or planned solution?
6. Should I continue, reduce scope, escalate, or create a fresh-context handoff?

Keep the nudge **brief** (a few hundred tokens). Ask for observable state, not hidden thought transcripts or a long self-analysis.

## H-17: checkpoint policy reduces long-horizon drift

**Prediction:** an event-triggered watchdog supplemented by a moderate interval and evidence-based restart improves *independently verified task completion* over fixed no-checkpoint sessions under matched total inference/tool budget.

**Alternatives:** checkpoints may simply waste context, disrupt useful flow, produce untrusted summaries or force unnecessary tool usage. A lightweight one-time planning prompt might perform as well. Long sessions can perform better on tasks requiring continuous state.

**Comparative conditions:**
- A: uninterrupted agent (standard context handling);
- B: fixed-interval reorientation prompts;
- C: event-triggered prompts;
- D: hybrid event+interval policy;
- E: hybrid+fresh-context restart with evidence packet.

**Measurements:** task resolution, skipped constraints, inappropriate tool choices, repeated failed calls, usable source evidence, cost, latency, human interventions, recovery after context reset and observed safety decisions. Compare across short, long and high-ambiguity tasks; include controls in which no checkpoint is needed. Randomize and hold out prompts and task solutions.

**Critical attribution:** if a checkpoint improves performance, determine whether the gain came from renewed instruction visibility, compaction, an extra inference pass, a better tool choice or a different solution plan. Budget matching and ablation are essential.

## Useful additional engineering investigations

1. Trigger policy conditioned on work phase (exploration, execution, verification).
2. Count *verified progress*, not arbitrary completed tool calls.
3. Use a contextual tool-fit signal; don't demand a specialized tool when ordinary grep is suitable.
4. Measure when a clean restart is better than preserving the working session.
5. Build a small indexed evidence ledger to avoid unbounded progress.txt loading.
6. Add human-requested break/resume interfaces without pretending the machine needs rest.
7. Track "checkpoint effectiveness" separately: prevented error, time cost and false alarms.


## Concrete opt-in Vibe integration confirmed in official documentation

Mistral Vibe Code now documents native lifecycle hooks, including post-tool hooks and a JSON \`hook_specific_output.additional_context\` field that is appended to the tool result the agent receives. This makes **actual reorientation nudges possible**, without inventing a proprietary API.

- Specification: https://docs.mistral.ai/vibe/code/cli/hooks
- [Opt-in hook script](../../examples/checkpoint-watchdog/vibe_post_tool_hook.py)
- [Example hooks.toml](../../examples/checkpoint-watchdog/hooks.toml.example)
- [Hook tests](../../tests/test_vibe_post_tool_hook.py)

The example hook is **NOT active automatically**. The project owner can inspect the script and copy the hook definition into a trusted working directory's \`.vibe/hooks.toml\`, then ensure the command points to the script. Running a hook may require Vibe to restart or create a new session to pick up configuration. Verify behavior with installed \`vibe --version\`.

### Implementation boundaries

- Hook reads only event/session identifier, tool outcome and time. It **never stores prompts, student data, tool arguments or tool output**; an SQLite file under ignored \`.vibe/data/\` stores a hashed session ID and counters.
- The hook offers a short reminder **after** the 25th completed tool call, after ~20 minutes elapsed **as observed at the next tool event**, or after three observed tool failures. A process returning nonzero may still be reported as tool success by Vibe, so the sample checks \`returncode\` where available.
- It does **not** run a timer in a currently idle model session. It has no access to independent context-utilization signals, structured verified-progress certificates, or a strong tool-suitability oracle.
- It does not assert that the model acknowledged the checkpoint. Counter resets are *reminder-rate-limiting*, not proof of a review. A trusted host must later record completed reviews and source-backed handoffs.
- The example deliberately does not inject a context reset or force another model turn, does not bypass permissions and does not deny ordinary tool calls.
- Invocations may overlap; SQLite transactions protect counter updates, but host-specific installation and concurrent tool ordering require further testing.

**Research status:** we can now test whether the prompt is really delivered to a compatible Vibe version. We still cannot claim that actual long-horizon task completion improves until a controlled Vibe A/B experiment measures it.


## Executed sensitivity study and observational instrumentation

See [Checkpoint Watchdog Sensitivity — 2026-11-05](../../research/CHECKPOINT-WATCHDOG-SENSITIVITY-2026-11-05.md). It replays ten synthetic session families with twenty seeded perturbations per family in two splits. Event-driven policies produced fewer notifications on healthy traces; shorter interval policies produced more broad warnings. These are **policy outputs**, not demonstrated agent-task improvement.

A new [strict sanitized observatory](../../experiments/watchdog/observatory.py) rejects prompt/tool-output/path fields and is intended to receive independently observed host telemetry in a later actual Vibe evaluation. Unknown progress or tool-fit information must remain unknown, not model-hallucinated.

The [external reminder gate](../../src/vibe_optimizer/watchdog_gate.py) also retains a \`safety_hold\` after a trusted unsafe signal; only a host-authenticated clearance may release it. The library alone does **not** interrupt Vibe or enforce that hold.

Do not optimize the 20-minute/25-call thresholds based on synthetic alerts alone: controlled fixed-model task evaluations and false-interruption costs remain necessary.
