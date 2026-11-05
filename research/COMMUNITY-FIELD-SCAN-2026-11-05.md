# Community field scan — agent capability engineering (5 November 2026)

**Scope:** firsthand GitHub projects, issue threads, Reddit discussions and Hacker News posts about improving one tool-using agent with external procedures, context, memory, scripts and tools. **Status:** desk research and technical ideas; no packages were installed or run in VIBE-optimizer. Citation is to public source, *not* empirical replication.

## How to read the evidence

- **I — inspectable implementation:** actual source, config, script or manual can be read; does not mean it beats an alternative.
- **E — author-run evaluation:** the project shows a methodology/outcome; claims may be self-evaluation and lack independent replication.
- **U — user account:** report of one person's experience or issue, useful for failure modes; not controlled evidence.
- **R — observational research:** systematic public-repository analysis; often static and not an agent task benchmark.
- **C — contested:** other users report serious downside or contradict the benefit.

No links below constitute an installation or an endorsement. Review licenses, dependencies, shell and network effects and secret handling before using third-party skills/hooks.

## A. Provenance-linked implementation and community lessons

### F01 — Superpowers: skills as tested procedures; **ceremony and overreach** (I, C)
Source: https://github.com/obra/superpowers
Community opposition: https://www.reddit.com/r/ClaudeCode/comments/1rmi6pr/anyone_else_not_a_fan_of_the_superpowers_plugin/
Other users positive: https://www.reddit.com/r/ClaudeCode/comments/1u2tqud/are_you_guys_still_using_the_superpowers_skill/

Implementation has structured skills for brainstorming, systematic debugging, TDD and verification; its recent releases add task-class-sensitive workflows and diagnosis of failed sessions. Some users say this reduces missed steps; others report excessive questions, worktrees, commits and inference cost even for small jobs.

**VIBE idea:** graduated procedures: lightweight/standard/deep. Measure the false-positive skill activation rate, unnecessary rituals and result correctness, not just number of completed checks. Prevent scripts committing or altering files without authorized workflow.

### F02 — gstack browser-skills: successful exploratory action -> tested deterministic script (I, E)
Source: https://github.com/garrytan/gstack/blob/main/docs/designs/BROWSER_SKILLS_V1.md
Docs: https://github.com/garrytan/gstack/blob/main/docs/skills.md

An unusually concrete implementation of *tool-making*: capture successful browsing procedure; generate per-task SKILL.md, script.ts, fixtures and test; future runs call deterministic script instead of re-exploring via agent tool calls. Project claims one repeat intent around 200ms vs 30 seconds of interactive tool exploration. It also separates a read-only \`/scrape\` from proposed or gated mutating automation, and describes isolation as an unresolved engineering boundary.

**VIBE idea:** workbench *scriptifier*—record successful human-reviewed tool action sequence -> propose test and fixture -> stage script -> independent review -> promote to reusable tool catalog. Test speed, transfer and drift on unseen pages/task variants.

### F03 — Ralph: fresh context per small task + file-based durable state (I)
Source: https://github.com/snarktank/ralph
Independent experimentation: https://news.ycombinator.com/item?id=46632445

Minimal shell loop starts a new agent for each small story and stores progress in Git history, \`prd.json\` and \`progress.txt\`. Demonstrates that a durable task contract is often more useful than keeping all prior tokens in context. A user reports long autonomous runs but also intermittent intervention and goal drift; not a quality benchmark.

**VIBE idea:** short-lived task sessions with *evidence-linked restart packet*, verified progress, unresolved blockers and reproducible stopping conditions. Compare with compaction alone and an uninterrupted long conversation.

### F04 — Beads: dependency-aware task graph instead of transcript memory (I)
Source: https://github.com/gastownhall/beads
Evidence of scaling problems: https://github.com/gastownhall/beads/issues/7982

Structured tasks, dependencies and readiness query (\`bd ready\`) define which work can proceed. This is external state/memory, not language-model weight training. User issues also report performance degradation at large memory scales; do not assume every graph should live in persistent storage.

**VIBE idea:** store durable *task dependencies and outcomes*, separate from semantically searched evidence and episodic memories. Benchmark ready-state correctness and restart fidelity; compare to plain JSONL.

### F05 — Claude-Mem: observations -> compressed searchable memory; relevance and stale-state failures (I, U)
Source: https://github.com/thedotmack/claude-mem
23-day user case: https://github.com/thedotmack/claude-mem/issues/1573
Community question on conflicting memories: https://github.com/thedotmack/claude-mem/discussions

A user reported 3,469 observations over 23 days, and improved injection of relevant evidence when moving from last-eight-recency to semantic retrieval; approximate per-turn context claimed reduced from ~1,800 to ~800–1,200 tokens. Issue threads identify orphan sessions, stale warnings and resource-consuming background behavior.

**VIBE idea:** event log + short active state + selective retrieval; store contradictory evidence, version scope and source path; inspect memory worker health and cost. No indiscriminate automatic promotion of model summaries.

### F06 — Serena: semantic source tools, but the agent may forget to use them (I, E, U)
Source: https://github.com/oraios/serena
Project evaluation: https://github.com/oraios/serena/blob/main/docs/04-evaluation/010_methodology.md
User issue: https://github.com/oraios/serena/issues/1201

Serena provides LSP-backed symbol/refactor/navigation tools and repository memory. Its maintainers compare hands-on tasks for precision, call count and payload size; for tiny edits or config, built-in tools can remain simpler. One issue documents long-session drift from semantic tools back to grep/read, suggesting that *tool visibility is not tool utilization*.

**VIBE idea:** capability-targeted discovery and explicit observable usage telemetry. A workbench should monitor whether a recommended tool is ever called, and measure fallback quality; do not force semantic tools where grep suffices.

### F07 — Context7: current versioned manuals with narrow task triggers (I)
Source: https://github.com/upstash/context7
Usage rule: https://github.com/upstash/context7/blob/master/rules/context7-mcp.md

A practical documentation MCP integration: resolve library ID/version, ask targeted documentation queries, avoid using it for ordinary coding logic or unrelated review. Separate topic queries reduce shallow retrieval on mixed topics. This is a shipped capability, **not an independently demonstrated accuracy gain for Vibe**.

**VIBE idea:** external API/stack atlas with explicit "use / do not use" applicability rules, source versions and a mechanism to retrieve only relevant detail.

### F08 — Hooks: text instruction vs deterministic enforceable event gate (I, U)
Official classification: https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more
User with 19 hooks and incident-driven fixes: https://www.reddit.com/r/ClaudeCode/comments/1w666so/my_claude_code_setup_after_7_months_of_daily_use/
Other community practice: https://www.reddit.com/r/ClaudeAI/comments/1sv852q/claude_code_cheat_sheet_after_6_months_of_daily/

A user reports replacing ineffectual generic prompting ("batch tool calls") with an executable hook and creating rules after accidents, not preemptively. Some hooks add ~2 seconds to every call. Procedural *skills* are for judgment; event hooks are for safe deterministic checks. Hooks are host-specific; do not assume identical events exist in Mistral Vibe.

**VIBE idea:** incident-driven reusable guard/action scripts behind a minimal stable interface. Only enforce checks backed by observed failure and test their cost. Never give installed community hooks unconditional access.

### F09 — Skill trigger misses and context delivery failures (U)
Claude issue: https://github.com/anthropics/claude-code/issues/100813
Other issue: https://github.com/anthropics/claude-code/issues/30387
Hacker News: https://news.ycombinator.com/item?id=48137164

Developers documented skills registered in settings but missing from model-delivered skill listings; auto-invocation may fail on tasks already resembling the model's built-in behavior. Other users prefer explicit short AGENTS.md instructions as a dependable entry point. These are reported versions/contexts, not proof all modern hosts share the bug.

**VIBE idea:** *capability-delivery audit*: compare expected tool/skill inventory with actual agent-visible inventory, log skill trigger precision/recall and provide explicit fallback/diagnostics. This is distinct from tool registration.

### F10 — LSP tools left unused; adding tools can reduce system utility (U, C)
Hacker News discussion: https://news.ycombinator.com/item?id=48289950

A developer installed several language servers, then audited hundreds of sessions and found near-zero actual tool invocation alongside memory pressure. Other posts dispute universal prescriptions such as "always install an LSP." Anecdote, but a perfect negative control for our Tool Workbench.

**VIBE idea:** retire underused/expensive tools or expose only when tool-fit predicts a benefit. Measure actual calls, task correctness, resident memory, latency and cost.

### F11 — Current public skill ecosystem has maintenance and supply-chain gaps (R)
GitHub skill-evolution empirical preprint, **2026-11-03**: https://arxiv.org/abs/2611.04456
Static public sample by community author, **2026-10-13**:
https://dev.to/basitalisandhu/the-state-of-public-agent-skills-and-mcp-servers-ii2

The new preprint analyzed **84,200 skills and 750,898 commits**, finding weak explicit reliability/recovery practices, project-coupled changes and redundant skills. A separate author scanned static config files from **2,999 repos**, reporting 82% without SECURITY.md and many very young projects. Neither directly measures benchmark capability of the installed skill.

**VIBE idea:** every imported skill is a versioned candidate with source/license verification, behavioral fixture, negative control, regression test and quarantine/revocation path. Stars are not quality scores.

### F12 — Inference-cost and effort adaptation: don't force heavyweight pipelines (U, C)
Pro-Superpowers user: https://www.reddit.com/r/ClaudeCode/comments/1u2tqud/are_you_guys_still_using_the_superpowers_skill/
Against: https://www.reddit.com/r/ClaudeCode/comments/1rmi6pr/anyone_else_not_a_fan_of_the_superpowers_plugin/
Issue: https://github.com/obra/superpowers/issues/1120
Hacker News: https://news.ycombinator.com/item?id=48289950

Users disagree on whether prescriptive planning/review frameworks help: some credit them with reliability, while others experience latency, unnecessary interruptions and invasive behavior. An actionable experiment compares adaptive "minimal/standard/deep" escalation against always-heavy and always-light.

## Candidate prompt/skill patterns to test, NOT validated universal incantations

**Tool gap check (triggered, not always-on):**
> When blocked, when evidence conflicts, or before declaring inability: specify the next needed observation; look for already authorized tools; confirm reachability, version and suitability; prefer reuse/composition over new tools; run the smallest safe test; record tool result. Do not silently acquire privileges.

**Small skill activation contract:**
> Use this skill when [observable symptom] AND [specific context]. Don't use it when [known exclusion]. First gather [required evidence]. Execute [bounded check], then produce [verifiable artifact]. On failure [fallback and diagnostic].

**Restart packet contract:**
> Preserve task objective, latest verified facts with source pointers, repository/base version, finished acceptance checks, unresolved questions, tool versions and next allowable read-only step. Reconstruct from records, not assumed conversation memory.

**Script promotion contract:**
> A one-off script is only a candidate. Record input/output contract, approved scope, fixture, test result, version, source and contraindications before promoting to the reusable tool catalogue.

## Frontier candidate experiments for one fixed Vibe model

| Priority | Test | Control and outcome |
| --- | --- | --- |
| P1 | Tool discovery vs **tool use**: does a hidden/registered tool become invoked? | Static, searchable, visible-with-trigger; measure actual calls and resolution |
| P1 | Prompt instruction vs deterministic hook on repeatable failure | Equal budget; block rate, cost and false positives |
| P1 | Fresh task session + evidence packet | Uninterrupted/compacted baseline; restart accuracy, missed constraints |
| P2 | Semantic memory vs recency memory vs no memory | Hold-out tasks, stale/conflict negative controls, tokens per useful fact |
| P2 | Procedure -> executable scriptifier | One-off vs replay script; per-task reliability, drift, break-even reuse |
| P2 | Skill selection and validation | Short skill, long global rules, injected full text, no-skill controls |
| P3 | Full procedural frameworks vs adaptive minimal flow | Resolved tasks per time/cost, unnecessary user questions and edits |
| P3 | Tool retirement/pruning | Always-on all tools vs usage-governed shelf; RAM, latency and task success |

## Preliminary assessment

The highest-value community signals for VIBE-optimizer are **(a) codify repeated successful actions as tested scripts, (b) audit capability delivery and actual utilization, (c) persist task state and memory independently of chat context, and (d) keep procedures proportional to the task**.

The community also supplies clear **negative evidence**: silent skill loading failures, stale memories, over-engineering due to large frameworks, never-invoked LSP tools and unsafe unreviewed skill distributions. Treat every source as a hypothesis lead, not proof of system-wide uplift.

**No code, model, plugin or community script was installed from this scan.**
