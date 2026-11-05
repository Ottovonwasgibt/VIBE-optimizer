# VIBE-optimizer

**Capability Maximization Engine for Mistral Vibe Code — external cognitive augmentation**

A research-first project to unlock the maximum **effective capability of a single coding agent**, initially Mistral Vibe, using knowledge, skills, specialized computation, verified memory, adaptive inference and controlled verification. Multiple models are optional research tools, **not** the design goal.

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
