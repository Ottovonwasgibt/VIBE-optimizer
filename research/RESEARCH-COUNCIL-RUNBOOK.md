# Research Council Runbook — prompts and concrete Vibe configurations

**Status:** experimental research handoff; not automatically executed. 2026-11-05.

## Operational caveat

Official Vibe documentation: https://docs.mistral.ai/vibe/code/cli/agents

- User-facing custom agents can be configured in project \`.vibe/agents/<name>.toml\`.
- A custom agent \`instructions\` value can provide its role-specific directives.
- A subagent uses only its permitted **built-in** tools and does **not** inherit MCP, connector or plugin tools. Therefore, do **not** design a Vibe subagent as though it can call the Knowledge Brain MCP.
- Agent safety labels are visual hints, not enforcement.
- The \`ask\` agent requires approval for tools; \`auto-approve\` is inappropriate for unreviewed research source packages.
- Use an external research controller/manual exchange for cross-provider coordination; Vibe's local subagents are not automatically interfaces to other model providers.
- Validate these instructions against the installed Vibe version before trying to load them.

## Option A — read-only conceptual agent configuration (proposed file)

\`.vibe/agents/theory-lab.toml\`

~~~toml
agent_type = "agent"
display_name = "Theory Lab"
description = "Researches and challenges externally augmented coding-agent theories without modifying files."
safety = "safe"
disabled_tools = ["edit", "write_file"]

instructions = """
Study the project's working theory, hypothesis register and source registry.
Do not invent factual citations or pretend designs are implemented.
Generate competing causal mechanisms and falsifiable predictions.
For each proposal: identify existing prior art, counterexamples,
budget-matched controls, minimum runnable experiment, and expected failure.
Do not edit code. Return a structured research note only.
"""

[tools.bash]
permission = "ask"

[tools.read_file]
permission = "always"
~~~

This is an **example to audit**, not a file installed in the repo's active agent directory. The explicit \`disabled_tools\` setting is stronger than a plain request not to edit but does not replace host/filesystem controls.

Run conceptually after checking environment:

~~~powershell
vibe --agent theory-lab
~~~

Use \`/clear\` when switching to an agent that needs to apply a different system prompt mid-session, following documented Vibe behavior.

## Option B — independent model research prompts (no API required)

### Prompt 1: Literature scout

> Research question: [INSERT HYPOTHESIS ID AND CAUSAL MECHANISM]. Search primary research publications, public code and versioned tool specifications through 2026-11-05. Return 8–15 evidence cards with exact URLs, publication date, mechanism, tested task setting, key limitations, contradictory results and a clear distinction between verified source claims and your own conjectures. Identify which code implementations need inspection and which potential 'novelties' are already known. Do not invent citations. If a source cannot be opened, mark it unverified rather than relying on its title.

Required structured output:
\`[{source_id, url, source_type, year, claim, method, limitations, relevance, verification_status}]\`.

### Prompt 2: Theorist

> You are given a frozen evidence pack and a working theory for fixed-weight coding-agent augmentation. Propose exactly three genuinely different **mechanistic explanations** for the observed limitation: [INSERT LIMITATION]. For each, state assumptions, causal chain, what the model/environment must do, two distinct predictions, one counter-theory, a task where the idea should fail, and the cheapest independent experiment that distinguishes it from its rival. Do not assert scientific novelty without a detailed prior-art comparison. Treat extra context and extra compute as separate confounds.

Required structured output:
\`[{title, mechanism, assumptions, predictions, rival, falsifier, experiment, sources, novelty_status}]\`.

### Prompt 3: Independent skeptical reviewer

> Review this anonymized theory and proposed experiment *as though it is wrong*. Identify hidden assumptions, causal confounds, source mismatch, benchmark contamination, API/version incompatibilities, false independence between model agents, and neglected negative results. Construct at least one counterexample in which the intervention should **decrease** task performance. Propose the single cheapest experiment that could refute it. Do not optimize for rhetorical balance or agreement.

Required output:
\`{weaknesses, alternative_mechanism, counterexample, discriminating_test, literature_gap, verdict_pretest}\`.

### Prompt 4: Architecture inventor

> Given this frozen hypothesis and critic feedback, design **two competing architectures** that could implement the same causal mechanism. Specify module contracts, data types, tool schemas, exact trust boundaries, source/provenance model, context/token budgets, rollback plan, and one minimum viable experiment. Identify which parts already exist natively in the target Vibe version, what a plugin can supply, and which parts require a separate Python service. Mark all unsupported syntax as pseudocode.

Required output:
\`{architectures: [{modules, interfaces, state, permissions, failure_modes, expected_cost, prototype_plan, verifiers}]}\`.

### Prompt 5: Experiment preregistration / adversarial test designer

> Produce a preregistration for [INSERT HYPOTHESIS] that differentiates the intervention from a no-augmentation baseline, an equal-budget self-consistency control, and an alternative simpler mechanism. Use blinded held-out tasks, fixed repository snapshots, versioned source corpora, and independent executable graders. Define primary/secondary metrics, negative transfer, stopping criteria, and what result would cause you to reject the claim. Do not change the evaluation after seeing outputs.

Required output:
\`{study, task_splits, controls, metric, acceptance, falsifier, sample_size_rationale, cost_ceiling, security_tests}\`.

## Frozen evidence workflow

Before collecting model responses, store:
1. Source snapshot date and links.
2. Task question and exact prompt version.
3. Model/provider/version, setting and inference budget.
4. Anonymized candidate IDs.
5. Independent test design and test answer locations.
6. An explicit record of which models received which evidence.

Do **not** send the output from Model A to Model B before the blind proposal round. Later critic rounds can see proposals but should preserve the first answers in an immutable record.

## Integration options

1. **Manual first:** run Vibe and a second model separately, paste only the same public/non-sensitive evidence pack, and save their JSON outputs locally. Zero orchestration dependencies.
2. **Open-file exchange:** controller writes input JSON under a local ignored directory; model workers return structured JSON. Can be independently inspected.
3. **Adapter layer later:** interface based on \`ResearchRequest\` / \`ResearchResponse\` in TDD-05. Add provider-specific implementations only after version and user permissions are checked.
4. **Codex optional:** official SDK/app-server documentation https://learn.chatgpt.com/docs/codex-sdk ; actual user entitlement and SDK operation need verification.
5. **Vibe:** official custom agents and subagents docs above, plus plugins https://docs.mistral.ai/vibe/code/cli/plugins .

## When research has gone beyond the existing literature

Not when a model says "novel," nor when two models agree. Require:
- specific source-based gap;
- a distinct mechanistic contribution;
- at least one reproducible independent test;
- a control that rules out simpler known mechanisms;
- transfer to an unseen repository or task;
- an honest negative-results audit.

A result may remain an **engineering invention, conditional mechanism or conjecture** even if useful. This is an acceptable research outcome.
