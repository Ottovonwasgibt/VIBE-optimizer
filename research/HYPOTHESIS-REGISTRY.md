# Hypothesis Registry — preregistration and failure retention

**Research phase:** 2026-11-05. Every hypothesis is **proposed**, not a VIBE-optimizer finding. This registry is deliberately distinct from implementation issues.

## Minimum research record

Each hypothesis has: identifier, falsifiable claim, causal mechanism, counter-theory, task subset, independent variable, controlled variables, outcome metric, negative outcome criteria, prototype, source support and status. A model's persuasive explanation is not an empirical result.

## H-01 — Task-conditional retrieval, rather than always retrieving

**Claim:** A router that retrieves only when evidence is plausibly missing improves verified success per unit cost compared with forced top-k knowledge injection.

**Mechanism:** Relevance selection reduces misleading context and token competition; simple tasks can avoid needless retrieval.

**Conditions:** Fix model, task, initial repository, and total token/time budget; task strata: local bug, unseen API, version-dependent bug, ambiguous request.

**Comparison:** (A) no retrieval, (B) mandatory lexical top-k, (C) task-conditioned lexical retrieval with abstention, (D) retrieval plus semantic reranking.

**Metrics:** resolved rate, retrieval/no-retrieval precision, calibration of no-evidence decisions, cost and latency.

**Refute or narrow if:** C has no higher utility or routinely misses essential evidence; or gains vanish with budget matching.

**Implementation sketch:** deterministic task-signal classifier + \`retrieve / do-not-retrieve / seek-version\` action, with routing decisions logged.

**References:** https://arxiv.org/abs/2607.24882 ; https://arxiv.org/abs/2005.11401

## H-02 — Repository plus dependency version graph

**Claim:** Linking local symbols to version-matched external library interfaces improves diagnosis and correctness on dependency-breaking tasks compared with unversioned repository-only search.

**Mechanism:** API compatibility is conditional on dependency versions, not just symbol-name similarity.

**Comparison:** (A) ripgrep/path search, (B) Git-scoped AST symbol map, (C) B plus dependency lockfile and docs, (D) C plus graph-neighbor expansion.

**Metrics:** correct-file/symbol localization, version-incompatible calls, patch pass@1, context tokens.

**Refute or narrow if:** D adds cost and errors with no improvement on version-sensitive tasks. Evaluate simple local bug tasks separately.

**References:** https://aclanthology.org/2026.findings-emnlp.433/ ; https://aider.chat/docs/repomap.html

## H-03 — Evidence-compiled procedures beat verbose standing instructions

**Claim:** A small skill assembled from contrasting verified successful and failed traces, and activated only in matching situations, improves held-out outcomes relative to a large always-on AGENTS.md or plain trajectory summaries.

**Mechanism:** Procedures compress actionable decision rules and boundary conditions, rather than transferring narrative artifacts.

**Comparison:** (A) no added instruction, (B) generic AGENTS.md, (C) manually designed skill, (D) evidence-derived skill with applicability checks.

**Metrics:** paired resolved-rate difference, rescued vs regressed tasks, skill false-activation rate, per-task cost.

**Refute or narrow if:** no held-out gain or negative transfer outweighs rescues.

**References:** https://www.microsoft.com/en-us/research/publication/skillgen-verified-inference-time-agent-skill-synthesis/ ; https://www.sri.inf.ethz.ch/publications/gloaguen2026agentsmd

## H-04 — Typed memory with external verification

**Claim:** Episodic memories, environmental facts, failures and procedures stored separately with explicit proof and scope reduce false reuse compared with untyped free-form chat memories.

**Mechanism:** Evidence and version applicability prevent incorrect generalization and self-reinforcing memory mistakes.

**Comparison:** (A) no memory, (B) raw summaries, (C) typed memories, (D) typed + independent approval/invalidation.

**Metrics:** future-task transfer, false-memory-induced regression, stale-memory retrieval, cost.

**Refute or narrow if:** typed governance increases cost without reducing harmful reuse; tests must deliberately introduce conflicting/stale records.

**References:** https://aclanthology.org/2026.emnlp-main.2188/ ; https://aclanthology.org/2026.findings-emnlp.1637/

## H-05 — Reversible context beats irreversible compression on long tasks

**Claim:** A three-tier record (raw trace + typed condensed state + cited active window) improves long-horizon correctness under equal context budgets.

**Mechanism:** Reconstructing source detail when needed preserves evidence lost in successive summaries.

**Comparison:** (A) rolling summary, (B) truncated recent window, (C) selective raw-trace retrieval, (D) reversible context hierarchy.

**Metrics:** fact recovery, missed constraints, rework, task success and prompt tokens.

**Refute or narrow if:** overhead exceeds benefit or raw-history selection cannot reliably restore needed context.

**References:** https://arxiv.org/abs/2510.04618 ; https://aclanthology.org/2026.emnlp-main.2188/

## H-06 — Verification converts uncertainty into actionable external cognition

**Claim:** Syntax parsers, formal analyzers, tests and bounded experiments produce more robust gains than a similarly expensive additional free-form reasoning pass for a subset of checkable coding problems.

**Mechanism:** Independent tools reveal facts/counterexamples unavailable from pure self-evaluation.

**Comparison:** (A) first attempt, (B) same-model second attempt, (C) independent typecheck/unit test, (D) property-based or symbolic verification as appropriate.

**Metrics:** resolved rate, regressions, correctly diagnosed failures, total budget, verifier false-positive and false-negative rates.

**Refute or narrow if:** tool signals are too noisy or too expensive, or tests are inadequate to distinguish correctness.

**References:** https://arxiv.org/abs/2210.03629 ; https://arxiv.org/abs/2310.06770

## H-07 — Multi-model research council improves discoveries only if independently evaluated

**Claim:** Independent literature mapping, divergent candidate architectures and adversarial critique can generate a better **verified** research portfolio than a single model *at matched total inference budget*, provided candidate selection uses external evidence and blind tests.

**Mechanism:** Variation in assumptions and information paths may increase useful search-space coverage; cross-model consensus itself is not a correctness guarantee.

**Comparison:** (A) one model with repeated samples, (B) one model self-critique, (C) multiple models with blind independent submissions + independent checks, (D) unconstrained debate.

**Metrics:** independently replicated novel useful propositions, cross-model transfer, evaluation cost, redundancy, spurious novelty, minority-correct-hypothesis suppression.

**Refute or narrow if:** C performs no better than equal-cost repeated sampling; errors are correlated; independent tests fail.

**References:** https://www.nature.com/articles/s41586-026-10644-y ; https://aclanthology.org/2026.findings-acl.1694/ ; https://proceedings.mlr.press/v306/li26ej.html ; https://arxiv.org/abs/2609.35875

## H-08 — Budget-aware information acquisition (value-of-information)

**Claim:** A router that chooses next actions based on estimated uncertainty reduction per cost is more effective than a static fixed sequence of search → plan → code → test.

**Mechanism:** Different coding failures benefit from different observation actions; active choice economizes limited tokens and executions.

**Comparison:** (A) fixed workflow, (B) rules by task type, (C) calibrated heuristic information value, (D) learned policy (only after sufficient log data).

**Metrics:** resolved tasks per dollar/time, unnecessary tool calls, rate of early correct abstention, security incidents.

**Refute or narrow if:** prediction overhead and calibration errors offset observed savings.

**References:** https://arxiv.org/abs/2607.24882 ; https://www.nature.com/articles/s41586-026-10652-y

## H-09 — Separate capability deficit diagnosis before retrieval

**Claim:** A deficit taxonomy (**knowledge gap**, **localization gap**, **execution gap**, **verification gap**, **specification gap**) reduces wasted tool calls and increases resolution on heterogeneous task sets.

**Mechanism:** Retrieval does not fix missing test coverage; another model call does not fix unavailable dependencies. First identifying the bottleneck improves action selection.

**Comparison:** (A) standard one-size-fits-all agent, (B) rules-based deficit classifier, (C) model-suggested deficit + independent supporting signals.

**Metrics:** error type confusion matrix vs human labels, effective time to first useful action, task resolution.

**Refute or narrow if:** classifier misdiagnoses cases so often that it degrades outcomes.

**References:** Synthesized working proposal, requires targeted literature review and pre-registered tests.

## H-10 — Counterexample memory as a non-useful-action filter

**Claim:** A curated bank of known failed procedures with version/context boundary constraints can prevent repeated mistakes, but only when the task matches sufficiently closely.

**Mechanism:** Negative procedural knowledge changes exploration choices, not just facts retrieved.

**Comparison:** (A) verified success memory, (B) success + failure traces, (C) explicit contraindications + task-scoped matching.

**Metrics:** repeated error frequency, harmful over-generalization, missed positive alternatives, cost.

**Refute or narrow if:** counterexample memory suppresses correct approaches more than it prevents repeated failures.

**References:** https://www.microsoft.com/en-us/research/publication/skillgen-verified-inference-time-agent-skill-synthesis/ ; https://aclanthology.org/2026.findings-emnlp.1637/

## Experimental discipline

Every experiment must predeclare:
- task population and excluded tasks;
- base model(s), fixed versions, tool/build environment;
- independent blind validator;
- metric hierarchy and cost allowance;
- train/dev/evaluation separation;
- stopping rules and multiple-comparison caution;
- expected counterexample conditions;
- status from \`proposed\` → \`pre_registered\` → \`tested\` → \`replicated\` or \`rejected\`.

**Novelty** is a *research question*, not a label earned by phrasing differently. Compare candidate against this registry, primary literature, open-source code and known prior art, then solicit an independent literature check.

## Research-to-component matrix

| Hypothesis | Component idea | First executable artifact |
| --- | --- | --- |
| H-01 | task-conditioned evidence router | policy function + abstention tests |
| H-02 | versioned cross-repo index | lockfile/link graph schema + probe |
| H-03 | trace-to-skill compiler | evidence-based SKILL.md candidate & A/B |
| H-04 | typed memory governance | candidate/approval/revocation state machine |
| H-05 | reversible context store | raw event log + attributed compact view |
| H-06 | verifier tool fabric | executable test/counterexample adaptor |
| H-07 | research council | model-independent proposal/review workflow |
| H-08 | cost-aware action policy | logged action-value heuristic |
| H-09 | bottleneck triage | task-deficit classifier + labeled cases |
| H-10 | contraindication memory | negative lesson schema with applicability |


## H-17 — A checkpoint watchdog reduces long-session agent drift

**Claim (untested on a model):** Under equal total inference/tool/time budget, periodic reorientation combined with externally detected mistakes and verified restarts improves independently validated task outcomes compared with an unmodified uninterrupted agent.

**Mechanism:** A model can lose priority constraints or persist with a poor tool choice during long trajectories. A trusted host can recover the task contract and objective evidence, remind it to reconsider tool suitability, and when needed provide a source-linked restart packet. This is not biological rest or guaranteed cognitive recovery.

**Comparison:** (A) no watchdog; (B) fixed interval; (C) event-triggered; (D) hybrid with reminder gate; (E) hybrid plus independently reviewed fresh-context handoff. Task types include long coding and non-coding diagnosis plus short negative controls. Record actual delivered/acknowledged prompts, not only a logged trigger.

**Metrics:** held-out verified resolution, missed constraints, inappropriate tool selection, repeated tool failures, corrected-error rate after checkpoint, alert precision, interruptions on productive tasks, token/time cost and unauthorized actions. Stratify by task length and tool count.

**Refute or narrow if:** improvements vanish when controlling extra inference budget; alerts cause disruptive over-checking; false checks interrupt good work; source-backed handoff loses essential constraints; model ignores the hook; or a static initial instruction works as well.

**Evidence and actual status (2026-11-05):** **policy mechanics tested; model-level causal hypothesis NOT tested**. Two synthetic replay phases found (i) the need for reminder-rate limiting and (ii) a tradeoff between broad interval detection and unnecessary notifications on healthy sessions. Seeded variations share the same hand-authored ten families and do not establish population validity. A metadata-only offline trace contract and a safety-hold latch have passed automated tests. See [report](CHECKPOINT-WATCHDOG-SENSITIVITY-2026-11-05.md) and [TDD-10](../docs/TECHNICAL-DESIGNS/08-checkpoint-watchdog.md).

**Prior art:** https://github.com/oraios/serena ; https://github.com/snarktank/ralph ; https://www.anthropic.com/research/effective-harnesses-for-long-running-agents ; https://www.microsoft.com/en-us/research/publication/benchmarking-long-horizon-agent-context-compaction-with-compactionbench/

**Research warning:** Creating warnings and detecting synthetic conditions does not demonstrate that a model notices, acknowledges, obeys, or benefits from them. Do not label H-17 as empirically confirmed.


## H-11 — Tool discovery and real host delivery

**Claim:** A qualified, searchable catalog increases correct use of available capabilities versus static/global tool lists at matched budget, **provided that discovered tools are actually delivered to the agent**.

**Competing explanation:** naming/description quality or prompt token differences, rather than discovery itself, cause gains.

**Evaluation:** same pinned model on held-out multi-tool and no-tool tasks: static tools, searchable catalog, search+host-delivery audit. Measure set completeness, actual host-visible tool list, calls, safe task resolution and cost.

**Status:** synthetic catalog search and MCP v2 in-memory delivery tests only; no actual Vibe-task uplift demonstrated. See [TDD-07](../docs/TECHNICAL-DESIGNS/05-adaptive-tool-workbench.md) and [catalog](../src/vibe_optimizer/capability_registry.py).

## H-12 — Tool adequacy probing

**Claim:** Version/health/permission/suitability checks reduce incompatible calls and wasted attempts, more than an equal-budget extra-reasoning control.

**Refutation:** filters discard useful tools or their overhead exceeds time saved.

**Status:** toy search policy and versioned Pydantic API smoke tests executed; no agent causal experiment. See [pilot](EXPERIMENT-REPORT-2026-11-05.md).

## H-13 — Tool reuse and safe composition

**Claim:** A single agent using a verified composition of existing tools resolves more new tasks, at the same budget, than reasoning longer or selecting a new untested tool.

**Refutation:** unnecessary complexity, hidden dependency side effects, or no transfer to unseen tasks.

**Status:** proposed; only pure allowlisted declarative recipe transformations and tests exist. See [recipe compiler](../src/vibe_optimizer/recipe_compiler.py).

## H-14 — Script/skill synthesis transfer

**Claim:** A reviewed tool made from a previously solved task transfers to a new task family, and future savings outweigh development, testing and maintenance costs.

**Comparisons:** no script vs plain instructions vs synthesized candidate vs independently qualified/pinned script.

**Safety:** staged script text has no permission to run; independent review required.

**Status:** candidate metadata and pure recipe fixture tested; general sandboxed program synthesis and real agent transfer not implemented. See [candidate governance](../src/vibe_optimizer/candidate_governance.py).

## H-15 — Domain pack transfer beyond coding

**Claim:** A process/state/technical evidence pack improves an agent's independent resolution of unseen *noncoding* operational tasks compared with baseline and raw public docs.

**Refutation:** fabricated tenant configuration, incorrect regulatory date, overconfidence or no outcome gain.

**Status:** eight fictional higher education cases and public domain-pack design; no actual model/domain-expert grading. See [domain pack](../docs/DOMAIN-DESIGNS/01-higher-education-functional-management.md).

## H-16 — Permission-aware institutional knowledge

**Claim:** In a separately approved deployment, a versioned, properly authorized private knowledge store improves operational diagnosis without prohibited data egress.

**Safety requirement:** identity- and purpose-scoped retrieval, model endpoint policy, licensed document rights, revocation, audit and human approval for operations.

**Status:** fictional access-control policy tests only; no real Osiris/Studielink documentation or connector and no approved production deployment. See [Private Knowledge Boundary](../docs/PRIVATE-KNOWLEDGE-BOUNDARY.md).

## H-18 — Capability utilization observatory

**Claim:** Monitoring the difference between tools configured, actually delivered, invoked and independently relevant makes adaptive tool selection/retirement more effective than maintaining every tool permanently.

**Alternative:** most tools are naturally seldom used; retiring them can harm rare but important tasks.

**Comparisons:** stable catalog vs usage-based nudging vs qualified hot/cold shelf; include very rare-task negative controls and memory/latency measurements.

**Status:** deterministic [delivery audit](../src/vibe_optimizer/capability_delivery.py) and sanitized [watchdog trace](../experiments/watchdog/observatory.py) tested on fictional data; no actual agent host usage traces.

## Cross-hypothesis integration rule

H-11 through H-18 are **not cumulative percentage bonuses**. The interaction terms may be positive or negative: search may add overhead, skills may override task plans, memories may become stale, and checkpoints may interrupt productive work. Compare each intervention, simpler alternatives and the *combined* stack on the same fixed model, matched budget and genuinely held-out tasks. For current component status see [Integrated Capability Cycle](../docs/INTEGRATED-CAPABILITY-CYCLE.md).
