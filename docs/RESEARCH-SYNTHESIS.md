# Research synthesis: what we established in conversation

**Source:** design conversation on 2026-11-05. This is a reconstruction of decisions stated in the conversation, **not** an import of the full results from two separately initiated Deep Research reports.

## Track A — Harness / workflow capability parity

Research question: Which observable engineering layers give coding agents their practical performance, beyond the base model?

Architecture decomposition:
1. Model and reasoning/training (intrinsic, only partially changeable through model selection).
2. Agent runtime/harness (planning, tool schemas, permissions, shell/filesystem actions).
3. Context engineering (selection, compaction, retrieval, repository mapping).
4. Procedures and skills (AGENTS.md, SKILL.md, subagents and optional hooks).
5. Tool fabric (MCP servers, specialized analyzers, tests and static checks).
6. Execution and feedback (patch-test-diagnose with human approval).
7. Measurement (fixed tasks, failure analysis, cost/latency and safety evaluation).

**Explicit correction:** We cannot copy proprietary models, hidden weights or private prompts by installing a plugin. We can reproduce **observable workflow patterns** within public specifications. Claims like 'automatically loaded all skills', 'hidden repo mapper', 'universal 1M context', or a particular `plugin.json` format need independent verification.

## Track B — External Cognitive Augmentation

Research question: Can a fixed model's **effective** coding and problem-solving capability be significantly extended using external knowledge, procedure, tools and accumulated evidence?

Separate these capabilities:

| Layer | Mechanism | Design target |
| --- | --- | --- |
| Semantic knowledge | Versioned documentation and concepts | Knowledge Brain |
| Repository knowledge | Current symbols, imports and tests | Git-aware code map |
| Procedural knowledge | Task-specific heuristics, checklists | Skills |
| Active reasoning tools | Parsers, external solvers, test frameworks | Tool Fabric |
| Episodic memory | Past tasks, failures, validated patches | Reviewed memory |
| Meta-control | Choose when to retrieve, invoke, verify or abstain | Router |

The strongest practical idea is **selective, verified augmentation**, not dumping large libraries into a prompt. Retrieval noise, stale documents and self-confirming memories can **reduce** correctness; effectiveness must be shown empirically.

### Examples

- Concurrency bug: retrieve version-matched runtime docs and related symbols; run focused tests and cancellation-specific checks.
- Unknown compiler error: retrieve exact error/version documentation and current build configuration, not generic troubleshooting advice.
- Architecture refactor: create a commit-scoped symbol map, patch in small slices and verify regressions.
- Previously solved bug: retrieve verified history only if signature and dependency scope still match.

## Decisions made

- Build as a **separate public repository** named `VIBE-optimizer`.
- Use current official Vibe plugin/skill interfaces where possible, not a speculative generic plugin manifest.
- Ship a minimal **project-scoped** plugin first; do not turn on an MCP server until it exists and runs on target OS.
- Start with **SQLite FTS5 + provenance**; embeddings, graph DBs and metacognition are later experiments.
- Build an **evaluation harness before sophisticated memory**, to measure actual usefulness.
- Explicitly separate source claims, own designs, and independently tested behavior.
- Keep the public repo free of secrets, local snapshots and private data.

## Unresolved integration tasks

1. Retrieve both Deep Research reports, compare evidence and create a citation-to-component matrix.
2. Check exact installed Vibe version, Python toolchain, security policy and Windows compatibility.
3. Verify whether new standards or better implementations supersede any initial proposed tools.
4. Collect real task examples/benchmark baselines before claiming gains.
5. Test the first end-to-end MCP integration and measure tool-call reliability.

## Sources

Primary specifications and research references are listed in [SOURCE-REGISTRY.md](SOURCE-REGISTRY.md). Any numerical advantage attributed to the external brain requires a cited benchmark and independent reproduction.
