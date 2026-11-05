# Master Blueprint v1.0 — External Cognitive Augmentation

**Status:** architecture proposal synthesized from the present conversation; external Deep Research reports not yet imported. **Date:** 2026-11-05.

## Mission

Build a maintainable extension to Mistral Vibe Code that improves real software-engineering outcomes by supplying relevant external evidence, procedural skills, trusted code tools, verifiers, and reviewed memory **without modifying model weights**.

### Taxonomy of capability

| Layer | What changes | What cannot be inferred |
| --- | --- | --- |
| Intrinsic model | Only through model/training changes | Retrieval does not alter learned weights |
| External knowledge | Coverage, accuracy, freshness when retrieved well | More tokens do not necessarily improve reasoning |
| Procedural skills | Decomposition, heuristics, verification policies | Instructions are not an enforceable sandbox |
| Tool augmentation | Executable search, tests, parsers, solvers | Tools do not guarantee correct interpretation |
| Memory & feedback | Reuse of validated past experience | Unverified self-reflection is not learning evidence |
| Meta-control | Choice of tools, skills, evidence and budget | Complex routing may make performance worse |

## Target outcomes

- Better repository-specific localization and edits.
- Reliable citations to source files, API docs and versions.
- More reproducible patch → focused test → diagnosis cycles.
- Reduction in repeated failures when previously *verified* solutions apply.
- Empirical evidence of improvement in task success, without unacceptable cost or security regression.

## Five main capability layers

1. **Knowledge Brain** — source catalog, provenance, ingestion, SQLite FTS5, later semantic retrieval.
2. **Procedural Intelligence** — small, discoverable `SKILL.md` playbooks; project `AGENTS.md` governs development.
3. **Tool Fabric** — MCP read-only knowledge tools, repository map; gated execution is the host's responsibility.
4. **Episodic Memory** — proposed → reviewed → verified/revoked; scoped to project/version/commit.
5. **Cognitive Router and Evaluator** — task classification, evidence budgets, tool selection, test metrics.

## Architecture principles

- **Progressive disclosure:** discover lightweight skill metadata first; load full procedure and sources only on demand.
- **Evidence-first:** attach source ID, URL, revision, chunk locator, license status and content hash.
- **Version aware:** code context tied to commit; library knowledge tied to version and date.
- **Independent verification:** unit/integration tests and static checks outrank model self-rating.
- **Conservative autonomy:** read-only by default, bounded retries, permission boundaries and review on promotion.
- **Ablation driven:** add a module only when it improves controlled measurements.

## Phases

**P0 — Reproducible baseline:** inspect installed Vibe; validate official plugin/skill formats; create blind internal tasks and vanilla metrics.

**P1 — Knowledge MVP:** approved-source ingestion, FTS5/BM25, `brain_search`/`brain_get`, provenance and adversarial retrieval tests.

**P2 — Repository and procedures:** Git-aware map, targeted skill activation, deterministic routing and verifier integration.

**P3 — Memory:** proposed experiences and reviewed verified lessons, expiry/invalidation and retrieval policies.

**P4 — Research options:** semantic reranking, dependency graphs, symbolic solvers, multiagent experiments and model-based routing—only through measured incremental value.

See technical designs and evaluation contract.

## Explicit unknowns / gates

- Locally installed Vibe version and admin-imposed permissions: **not checked**.
- MCP server launch on Windows: **must be tested on the target machine**.
- The two Deep Research reports: **not yet attached**; their findings must be reconciled with sources, not guessed.
- Performance uplift: **unknown** until experiments.
- Security of external skills and proprietary source licensing: review before ingestion.

## Open decisions

See `docs/ARCHITECTURE.md` and `docs/ROADMAP.md`; file architecture decisions in `docs/decisions/` once experiments establish evidence.

## Research-first addendum — theory, not just infrastructure

The overarching goal is to build and test a **working causal theory** of how external knowledge, procedure, tools, episodic experience, validation and task-aware routing interact to change a fixed model's effective capability. Read [TECA](THEORY-OF-EXTERNAL-COGNITION.md), the [hypothesis registry](../research/HYPOTHESIS-REGISTRY.md), the [frontier dossier](../research/FRONTIER-EVIDENCE-DOSSIER.md) and the [multi-model laboratory protocol](MULTI-MODEL-RESEARCH-LAB.md) before prioritizing an architectural component.

Our primary deliverables are **explanatory models, falsifiable hypotheses, alternative mechanism designs, technical specifications, and discriminating experiments**. Production-grade implementation is a later consequence of surviving experiments. The small SQLite/CLI implementation is only an initial instrumentation scaffold.

The project's original five-layer architecture remains a proposal, not a conclusion. New components should emerge from the research cycle `evidence → theory → rival explanation → hypothesis → small test → revision`, not from architectural fashion or model consensus. Multi-model research can expand the candidate search space, but independent measurement and budget-matched controls are required before claims of improvement.
