# Roadmap and first coding-agent assignments

**Status:** planning. Work from narrow verifiable vertical slices, not by implementing all subsystems at once.

## Day 0 — bootstrap (done)

- [x] Public repository initialized.
- [x] README, AGENTS.md, architecture, primary source registry, technical designs and evaluation contract.
- [ ] Import/reconcile both full external Deep Research reports when available.

## Phase 1 — source and Vibe compatibility audit

- [ ] Capture `vibe --version`; inspect `vibe config schema`; record OS, Python version, `uv` presence.
- [ ] Validate Agent Plugins 1.0 and `SKILL.md` against installed Vibe.
- [ ] Document any mismatch between current docs and executable behavior.
- [ ] Create a baseline task set and run vanilla Vibe.
- [ ] Define source license, confidentiality and approval gate.

**Deliverable:** `docs/compatibility-report.md`, reproducible baseline task/results references, numbered architecture decisions.

## Phase 2 — first retrieval vertical slice

- [ ] Implement and test SQLite FTS5 schema and migrations.
- [ ] Implement offline ingestion from *locally provided, reviewed* example documents first.
- [ ] Add source/version/hash/locator checks, approved-only filters and query token limits.
- [ ] Unit test hostile query syntax, revoked sources and no-source behavior.
- [ ] Benchmark retrieval relevance against baseline.

**Deliverable:** pure Python retrieval service and tests; no MCP dependency required yet.

## Phase 3 — Vibe integration

- [ ] Pick and pin MCP Python SDK v2 release.
- [ ] Wrap read-only search/get functions as narrow MCP tools.
- [ ] Implement launch command that **actually works on target Windows machine**.
- [ ] Only then add a validated `mcp.json` to project plugin.
- [ ] Test `/plugins`, `/mcp`, `/reload-plugins` and clean shutdown.
- [ ] Implement `repo-intelligence` skill and a minimal commit-aware map.

**Deliverable:** demonstrably working end-to-end task with cited retrieval and successful test run.

## Phase 4 — feedback and experiments

- [ ] Introduce small patch → verify → diagnose workflow and evidence logs.
- [ ] Separate memory proposal from approval and retrieval.
- [ ] Evaluate on held-out tasks with fixed model/budget.
- [ ] Do ablations B–F, measure latency, tokens, security and failure types.
- [ ] Investigate embeddings and graph retrieval only if benchmark indicates a gap.

**Deliverable:** `experiments/` reports, accepted/rejected architectural decisions.

## Suggested issues for next contributor agent

**ISSUE-001 Source and environment audit**
- Verify each `VIBE-*`, `MCP-*` reference and capture installed versions.
- Acceptance: no unverified CLI flag or config key in executable examples.

**ISSUE-002 SQLite knowledge prototype**
- Build schema, source catalog importer, read-only `search`.
- Acceptance: source allow-list filter, revision provenance and tests for malicious FTS syntax.

**ISSUE-003 Minimal MCP bridge**
- Only after ISSUE-002: expose `brain_search` and `brain_get`.
- Acceptance: works in Vibe on Windows using pinned SDK, no unexpected shell/tool access.

**ISSUE-004 Evaluation harness**
- Freeze task cases; compare vanilla against skills/retrieval.
- Acceptance: deterministic run metadata and isolation of solution keys.

**ISSUE-005 Repository intelligence**
- Index checked-out commit's symbols using parser, not stale file summaries.
- Acceptance: correct symbol and file locations, invalidation after Git commit switch.

## Definition of done for every slice

- Source references and dependency versions.
- Minimal implementation and automated tests.
- Actual run evidence (or explicit 'not executed').
- Trust/security analysis, at least one adversarial case.
- Change log/ADR, rollback path and public/private data check.

## Deliberately deferred

No private-data indexing, remote scraping without rights, autonomous memory approval, self-modifying agent loops, global plugin installation, complex multiactor agent delegation or knowledge-graph platform until simple components show measurable gains.

## Updated priority — scientific development before feature parity

**R0 — Conceptual foundation:** maintain a live source/claim registry, establish TECA constructs and counter-theories, distinguish prior art from a candidate contribution.

**R1 — Hypothesis design:** preregister 3–4 discriminating studies with positive, negative, and budget-matched controls. Prioritize H-01 (selective retrieval), H-03 (verified procedural skills), H-06 (active verification) and H-09 (capability-deficit routing). H-07 (multi-model research) is optional, not foundational.

**R2 — Single-model capability frontier:** compare bare Vibe, budget-matched repeated inference, augmented Vibe, and optional high-budget deliberate mode. Identify which previously unsolved task classes become reliably solvable. Multi-model research is a secondary controlled experiment only when valuable.

**R3 — Minimal scientific instruments:** build only tools/scripts needed to test claims—hypothesis linter, evidence provenance graph, prompt snapshot, read-only retrieval, AST map, simple verifier/evaluator.

**R4 — Theory revision:** record supported, refuted, mixed and unresolved propositions; refine architectural choice only when results justify it.

The older implementation phases below remain **candidate engineering work**, not commitments. Avoid optimising directly for a large feature count.

## Mission correction: capability maximization first

The main goal is the [Capability Maximization Programme](CAPABILITY-MAXIMIZATION.md): unlock the maximum verified coding/problem-solving ability from **one** fixed model using external knowledge, procedures, tools, verified experience, adaptive context and deliberate inference. Extra agents/models are not a milestone. Evaluate them only when a specific gap warrants the comparison. Use this as the priority order for future work; older roadmap entries are subordinate.
