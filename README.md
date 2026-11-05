# VIBE-optimizer

**Capability Maximization Engine — external cognitive augmentation for complex knowledge work**

A research-first project to unlock the maximum **effective capability of one task-solving agent**, initially using Mistral Vibe. External libraries, operational process models, verified knowledge, procedures, tools, memory and validation should improve **coding and non-coding work**—including functional management of student information systems. Multiple models are optional research tools, **not** the design goal.

> **Status:** research-backed design and bootstrap, **not** a working autonomous coding agent. The two external Deep Research reports discussed in the originating conversation have **not yet been imported or independently audited**. Do not mistake design sketches for implemented integrations.

## Primary mission: single-agent-first capability maximization

Start with [Capability Maximization Programme](docs/CAPABILITY-MAXIMIZATION.md). The informal 'Super Saiyan' ambition means *reliably solve harder previously unsolved tasks under measured budgets*, not a marketing performance label. Prioritize what one model plus well-designed infrastructure can accomplish; a second model or subagent must independently justify its extra cost.

## Why this repository exists

A model's weights are not the entire capability of the coding system. A well-designed environment can supply up-to-date repository context, relevant external knowledge, reliable procedures, test tooling and prior verified experience. We seek to **measure** gains over an unmodified Vibe baseline rather than assume that retrieval automatically improves reasoning.

## Project principles

1. Separate **model-intrinsic capability** from **system-level effective capability**.
2. Prefer verified, version-matched source material to large undifferentiated data dumps.
3. Use *progressive disclosure*: activate skills and retrieve evidence only when relevant.
4. Treat documents, repositories, and retrieval results as **untrusted data**, never higher-priority instructions.
5. Run small changes and focused checks; do not silently retry indefinitely.
6. Memory is **proposed, reviewed, verified, versioned, revoked**—not an unexamined transcript archive.
7. Benchmark each layer against a fixed-model baseline with cost, latency and safety metrics.
8. Keep secrets and local runtime data out of the public Git repository.

## Navigation

| Document | Purpose |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Operating instructions for a coding agent working on this repository |
| [docs/MASTER-BLUEPRINT.md](docs/MASTER-BLUEPRINT.md) | Overall architecture, milestones and requirements |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Interfaces, data flow, trust boundaries, design decisions |
| [docs/SOURCE-REGISTRY.md](docs/SOURCE-REGISTRY.md) | Primary technical specifications, scientific papers and audit status |
| [docs/TECHNICAL-DESIGNS/01-knowledge-brain.md](docs/TECHNICAL-DESIGNS/01-knowledge-brain.md) | Storage, retrieval, provenance and memory schema |
| [docs/TECHNICAL-DESIGNS/02-router-and-tools.md](docs/TECHNICAL-DESIGNS/02-router-and-tools.md) | Context router, skills, MCP and implementation contracts |
| [docs/EVALUATION.md](docs/EVALUATION.md) | Baselines, ablations, acceptance tests and safety evaluations |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Ordered delivery slices and definition of done |

## Minimal planned Vibe integration

A **project-scoped** Agent Plugins 1.0 plugin at `.vibe/plugins/cognitive-stack/`, containing a valid `plugin.json`, a small collection of `SKILL.md` files and reference knowledge. An MCP server will be enabled **only once its executable exists, is tested, and its runtime has been reviewed**. Experimental plugin interfaces may change across Vibe releases.

## Developer starting point

1. Read [AGENTS.md](AGENTS.md), the [source registry](docs/SOURCE-REGISTRY.md) and the architecture.
2. Inspect the local Vibe version and the *current* official documentation before running configuration snippets.
3. Implement an isolated SQLite FTS5 retrieval prototype, then tests.
4. Only after those tests pass, expose read-only `brain_search` / `brain_get` through MCP.
5. Measure an unmodified Vibe baseline before claiming any improvement.

**Non-goals:** extracting hidden prompts/weights, bypassing tool approvals, collecting secrets, asserting equivalence to proprietary coding models, self-approving memories or downloading arbitrary executable skill repositories.

## Core references

- [Mistral Vibe plugins](https://docs.mistral.ai/vibe/code/cli/plugins)
- [Mistral Vibe skills](https://docs.mistral.ai/vibe/code/cli/skills)
- [Vibe configuration reference](https://docs.mistral.ai/vibe/code/cli/configuration-reference)
- [Agent Skills specification](https://agentskills.io/specification)
- [MCP Python SDK v2](https://py.sdk.modelcontextprotocol.io/)
- [SQLite FTS5](https://www.sqlite.org/fts5.html)

See the source registry for source-to-component traceability.

## Research-first programme (2026-11-05)

The priority is now **frontier concept development and theory building**—not immediately shipping a big plugin. The local SQLite prototype is a research scaffold, not the main scientific result.

- [Working theory of external cognitive augmentation](docs/THEORY-OF-EXTERNAL-COGNITION.md) — causal constructs, competing explanations and falsifiable predictions.
- [Hypothesis registry](research/HYPOTHESIS-REGISTRY.md) — ten preregistration-ready candidate mechanisms and ways to disprove them.
- [Frontier evidence dossier](research/FRONTIER-EVIDENCE-DOSSIER.md) — current 2025–2026 literature, positive and negative evidence, open gaps.
- [Optional multi-model research laboratory](docs/MULTI-MODEL-RESEARCH-LAB.md) — one possible validation/discovery method, not the primary architecture.
- [Research orchestrator technical blueprint](docs/TECHNICAL-DESIGNS/03-research-orchestrator.md) — project-owned data contracts, model adapters, prompts and evaluator boundaries.

Treat proposed novelty as **unverified** until a primary-literature search and independent experiment establish what is actually new. Do not equate multiple-model agreement with scientific validation.

- [Research council runbook](research/RESEARCH-COUNCIL-RUNBOOK.md) — ready-to-use prompts and read-only Vibe agent example.
- [Deficit-aware router and evidence compiler](docs/TECHNICAL-DESIGNS/04-deficit-router-evidence-compiler.md) — detailed candidate mechanism, contracts and falsifiers.


## Quantitative research and reproducible thought experiments

The workbench now has a mathematical research programme, with **synthetic examples rather than measured Vibe improvements**:

- [Quantitative Capability Models](research/QUANTITATIVE-CAPABILITY-MODELS.md): conditional tool-use failure funnel, multi-tool completeness, expected value of discovery/probing, tool-making break-even, context savings, budget-sensitive task frontier, Bayesian tool adequacy.
- [Capability calculator](experiments/capability_calculator.py): dependency-free CLI for varying the hypothetical parameters.
- [Calculator unit tests](tests/test_capability_calculator.py): deterministic numerical checks; the script was tested locally before uploading.
- [Research pilot / Issue #7](https://github.com/Ottovonwasgibt/VIBE-optimizer/issues/7): replace assumed probabilities with measured task outcomes.

Example:

~~~powershell
python experiments/capability_calculator.py funnel --baseline .70 .65 .85 .80 .90 --enhanced .90 .85 .85 .80 .90
python experiments/capability_calculator.py probe --p-gap .35 --lift .25 --value 120 --probe-cost 4 --risk-cost 3
python -m unittest discover -s tests -v
~~~

The formulas and thresholds describe **assumptions and research questions**, not certified scientific findings or numerical guarantees of improved coding-agent intelligence.

## Capability Library & Stack Atlas (research direction)

A structured external library goes beyond RAG text chunks: it combines **version-matched API manuals**, **tested function patterns**, **reviewed scripts**, **complete stack recipes**, **conditional skills**, and **known failures**. These are progressively discovered on demand, not globally injected into context.

- [Technical design TDD-08: Capability Library & Software Stack Atlas](docs/TECHNICAL-DESIGNS/06-capability-library-stack-atlas.md)
- [Research issue #8: benchmark capability packs against docs, skills and scripts](https://github.com/Ottovonwasgibt/VIBE-optimizer/issues/8)

Grounding: DocPrompting, RepoCoder, Repoformer, CodeRAG-Bench, LibEvoBench, SkillsBench and SWE-Skills-Bench. Published work supports individual interventions but **does not yet prove a combined uplift** for this project. Pack manifests and example stack versions are only drafts until actual source/lockfile verification.


## First executed research pilots — 2026-11-05

Two **actual executable infrastructure tests** have now been run and independently reproduced in GitHub Actions. These are **not Vibe/LLM benchmark runs**.

- [Experimental report and observed outcomes](research/EXPERIMENT-REPORT-2026-11-05.md)
- [Reproducible pilot scripts, instructions and summary](experiments/pilots/README.md)
- [GitHub Actions reproduction: success](https://github.com/Ottovonwasgibt/VIBE-optimizer/actions/runs/42038453644)

Tool-workbench proxy: 24 synthetic tools, 28 hand-authored tasks; scoped/decomposed selection selected the correct compatible slate on **26/28** cases at top-3 versus **18/28** for plain lexical search. Real Pydantic compatibility smoke test: **v2-only methods 0/7 on v1 compatibility API** versus **7/7 on v2 API**. These observations support pursuing real model A/B experiments; they **do not** establish improved Vibe task-solving performance.

## Beyond coding: functional management and higher education

The same workbench is intended for process analysis, operational diagnostics, application/authorization configuration review, integration troubleshooting, reporting and change management—not only writing scripts.

- [Domain-agnostic operational capability architecture](docs/DOMAIN-OPERATIONS-CAPABILITY-ENGINE.md)
- [Higher education functional management domain pack: Osiris, Studielink and DUO](docs/DOMAIN-DESIGNS/01-higher-education-functional-management.md)
- [Synthetic higher education research tasks](experiments/domains/higher-education/synthetic-cases.json)

**No live Osiris or Studielink connection is assumed.** Public system descriptions and synthetic tasks do not authorize use of student data, administrative mutations or resubmitting messages. In operational domains the evaluation must test correctness of decisions, evidence, dates, process understanding and safe escalation as well as any generated code.

## Restricted documentation in an authorized deployment

Closed vendor manuals and institution-internal Osiris/Studielink documentation **may be consulted in a separately authorized environment**; they are not accessible from this public GitHub/ChatGPT project. [Private Knowledge Boundary](docs/PRIVATE-KNOWLEDGE-BOUNDARY.md) describes permission-aware local indexes, source classification, model data egress and safe retrieval. **A local Vibe CLI does not necessarily mean local model inference:** do not send restricted excerpts to an external model endpoint until that processing is expressly approved.


## Restricted documentation: the method and scaffold, not the documents

The public repository includes a **runnable, fail-closed synthetic prototype** of permission-aware retrieval and destination-based data release. It contains **no closed Osiris/Studielink manuals or real student data**.

- [Technical implementation method](docs/TECHNICAL-DESIGNS/07-private-source-scaffold.md) — source staging, classification, rights, access, egress, source revision, evidence and approval.
- [Policy-aware Python gateway](src/vibe_optimizer/private_knowledge.py) — prototype code (no real identity or private storage integration).
- [Unit tests](tests/test_private_knowledge.py) — role, tenant, purpose, date, status, content hash and model destination checks.
- [Synthetic runnable demonstration](examples/private-knowledge/demo.py) — shows a simulated private snippet blocked to public model destination.
- [Source manifest JSON Schema](schemas/private-source-manifest.schema.json) and [fictional staged manifest](examples/private-knowledge/synthetic-manifest.json) — data contracts, **not proof of approved rights**.

Run \`python examples/private-knowledge/demo.py\` and \`python -m unittest discover -s tests -v\` from the repository root. The prototype is not an Osiris connector, production authentication service, protected persistent index or model-network security boundary. A real deployment still requires institution-approved authorization and infrastructure.

## Community practice and frontier-forum evidence (2026-11-05)

[Community Field Scan](research/COMMUNITY-FIELD-SCAN-2026-11-05.md) examines twelve practice patterns and counterexamples from Reddit, Hacker News, GitHub projects and issue trackers: Superpowers, gstack browser scriptification, Ralph, Beads, claude-mem, Serena, Context7, hooks, silent skill activation, underused LSP tools and skill supply-chain findings. It separates inspectable implementations, author evaluations, user anecdotes and observational research; **no community code was automatically installed**.


## Agent drift, periodic checkpoints and fresh-context recovery

[Checkpoint Watchdog design and research](docs/TECHNICAL-DESIGNS/08-checkpoint-watchdog.md): a single agent should periodically **reorient**, verify observable progress, reconsider available tools and, when justified, resume with an evidence-linked fresh-context handoff.

- [Deterministic checkpoint policy](src/vibe_optimizer/checkpoint_watchdog.py): time/tool-call, repeated failures, stalled progress, observed underuse of suitable tools and context-pressure gates.
- [Opt-in native Vibe post-tool hook](examples/checkpoint-watchdog/vibe_post_tool_hook.py): an actual Mistral Vibe hooks-compatible example that adds a short reminder after 20 minutes, 25 tool calls or repeated tool errors; no conversation or tool contents are stored.
- [Example hooks.toml](examples/checkpoint-watchdog/hooks.toml.example): **not automatically installed**.
- [One-shot policy demo](examples/checkpoint-watchdog/check.py) and [tests](tests/test_checkpoint_watchdog.py).

The Vibe hook can only nudge the agent at **the next tool event**, not while the model is idle; it cannot independently verify that the agent followed the reminder or forcibly create a fresh session. It must be evaluated against a Vibe task-success baseline before declaring a benefit. Current thresholds are research defaults, **not scientifically optimized**. Relevant public Vibe hook contract: https://docs.mistral.ai/vibe/code/cli/hooks


## Checkpoint watchdog: executed sensitivity study and trace instrumentation

- [Research report — Watchdog Sensitivity](research/CHECKPOINT-WATCHDOG-SENSITIVITY-2026-11-05.md): 400 perturbed **synthetic** sessions in two splits; compares event-only, frequent, balanced, relaxed and stricter policies. Not a model evaluation.
- [Sensitivity experiment](experiments/watchdog/sensitivity.py) and [replay](experiments/watchdog/replay.py): deterministic synthetic traces and reminder-rate tradeoffs.
- [Privacy-minimized observatory adapter](experiments/watchdog/observatory.py) and [fictional trace](experiments/watchdog/synthetic_trace.json): accepts only allowlisted host-event metrics for later live-session A/B evaluations.
- [Watchdog safety gate](src/vibe_optimizer/watchdog_gate.py): remembers a safety hold until an **externally authorized** release; enforcement in the real agent host is still pending.

**Important:** Detection of a simulated anomaly is not a demonstrated improvement in task success. The live Vibe hook is opt-in and has not been proven to change outcomes.

## Integrated capability system v0.2 — runnable research scaffolds

The architecture is now linked into a **synthetic, advisory-only end-to-end cycle** rather than just independent proposals. It is **not** yet an autonomous agent or evidence of improved real Vibe task performance.

- [Integrated Capability Cycle](docs/INTEGRATED-CAPABILITY-CYCLE.md): architecture, implementation status, host permissions and release gates.
- [Workbench getting started](examples/capability-workbench/README.md): offline cross-domain demo, the public synthetic catalog, a tested optional MCP Python SDK v2 bridge, and on-demand Vibe skills.
- [Integrated CI smoke (synthetic)](https://github.com/Ottovonwasgibt/VIBE-optimizer/actions/workflows/integrated-cycle.yml): public SQLite source -> search -> task triage -> evidence packet -> checkpoint -> safe recipe -> simulated review -> paired evaluation.
- [MCP v2 SDK smoke](https://github.com/Ottovonwasgibt/VIBE-optimizer/actions/runs/42053782097): real in-memory MCP client invoked three public advisory tools; **not** an installed Vibe session.
- [Function/Script Workshop](src/vibe_optimizer/recipe_compiler.py): declarative, bounded pure transformations with [synthetic fixtures](examples/script-workshop/synthetic-recipe.json), not arbitrary program execution.
- [Paired evaluator](experiments/live_agent/paired_eval.py) and [explicitly fictional scores](experiments/live_agent/synthetic_results.json): a reporting contract for future fixed-model A/B trials.

The project-skills `/cognitive:capability-check` and `/cognitive:checkpoint-review` are available for manual Vibe discovery after trusting/reloading this repo's existing plugin. They do not install servers or change tool permissions. Actual model evaluation remains an open milestone.


## Model-portable capability packs and first opt-in A/B launcher

The workbench is intentionally model-agnostic: it should serve Mistral Vibe, Claude and GPT-6 Astra (or other tool-capable models) through **host-specific adapters**. The same external reference, validated recipe or checkpoint may help different models, but task success, cost and latency must be measured independently; the system does **not** change base model weights.

- [Cross-model architecture and Astra/Claude portability](docs/MODEL-PORTABILITY.md)
- [Dry-run-first local Vibe/Claude A/B runner](experiments/live_agent/run_local.py) and [instructions](experiments/live_agent/README.md)
- [Public/synthetic cross-domain task suite](experiments/live_agent/public_synthetic_suite.json)
- [CI: dry run only, no model or API calls](https://github.com/Ottovonwasgibt/VIBE-optimizer/actions/runs/42059658685)
- [Issue #12: actual pinned Vibe A/B task evaluation](https://github.com/Ottovonwasgibt/VIBE-optimizer/issues/12)

**No actual model was run by this research launcher yet.** All generated benchmark prompts and model traces default to ignored `runtime/`. Use `--execute` only after checking the installed agent CLI, provider fees, permissions and exact model. Astra integration is documented, not implemented in this CLI runner.
