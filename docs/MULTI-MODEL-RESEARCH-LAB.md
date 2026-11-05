# Multi-Model Research Laboratory — design v0.1

**Status:** research-operating protocol and technical concept; no external model connections are installed or configured in this repository. Version: 2026-11-05.

## Scope correction: optional research instrument

The **primary mission is single-agent capability maximization**, defined in [Capability Maximization Programme](CAPABILITY-MAXIMIZATION.md). This laboratory describes an *optional research protocol* for obtaining independent critiques, literature coverage or hypotheses. It is **not** a required multi-agent product architecture, and a single well-augmented Vibe instance is the default experimental system. Compare any additional model/subagent against equal-budget single-model scaling before concluding it helps.

## Mission

Use Mistral Vibe and one or more independent frontier models as **research instruments** to:
1. map public prior art and unknowns;
2. generate alternative causal explanations and *falsifiable* hypotheses;
3. design candidate tool/skill/memory architectures;
4. implement small discriminating prototypes;
5. independently test, challenge and replicate results;
6. update the working theory without falsely promoting model agreement to evidence.

The research question is **not** "how can ten AI agents agree?" It is "which combination of independent search paths, formal hypotheses, executable tests and rigorous adjudication produces more verified, transferable knowledge than a strong single-agent baseline at equal cost?"

## Guiding science

- The 2026 Nature Co-Scientist paper explores hypothesis generation, critique, tournament evolution and test-time compute. https://www.nature.com/articles/s41586-026-10644-y
- The Robin work demonstrates a research cycle combining literature agents, hypothesis design, experimental feedback and analysis in biological research. https://www.nature.com/articles/s41586-026-10652-y
- Negative evidence: HiddenBench identifies systematic failures to combine hidden/distributed information in multi-agent LLMs. https://proceedings.mlr.press/v306/li26ej.html
- Counter-evidence to naïve debate gains: compare against budget-matched repeated sampling, not just single-shot baseline. https://arxiv.org/abs/2609.35875
- Different models are **not guaranteed independent**: overlapping training, shared web evidence, copied prompts and correlated failures create dependence.

## Organization: a laboratory, not a chat group

### Research tracks

- **Track A — Harness mechanics**: agent runtimes, tools, context, execution, permissions, observability.
- **Track B — Cognitive augmentation theory**: retrieval, skill formation, metacognition, memory, epistemic reliability.
- **Track C — New mechanisms**: propose and disconfirm architecture ideas beyond current public implementations.
- **Track D — Benchmarks and causal measurement**: controlled reproducible experiments and independent replication.

### Roles (logical roles; may run on one or several models)

| Role | Input | Output | Prohibited shortcut |
| --- | --- | --- | --- |
| Scout | question + source access | evidence cards, prior art, uncertainty | unsupported citations or copied marketing |
| Theorist | evidence and unknowns | causal mechanism, prediction, rival theory | naming a hypothesis a proven theory |
| Architect | candidate mechanism | interface contract, data flow, cost/risk | "just add a vector database" |
| Skeptic | blinded candidate | failure scenarios, alternative explanations | vague subjective criticism |
| Experiment designer | hypotheses | preregistered task splits and ablations | tweaking rubric after results |
| Builder | frozen proposal | minimal prototype and tests | broad unsupervised project edits |
| Replicator | frozen artifact | independent rerun and discrepancy report | trusting builder self-report |
| Adjudicator | blinded results | decision, confidence level, next experiment | majority vote without evidence |

**One person or model may fulfill multiple roles for an MVP**, but do not pretend those roles are independent. For high-stakes or novel claims use a distinct reviewer model or human and external deterministic checks.

## Core workflow

1. **Question framing:** define task family, success criteria and one concrete bottleneck.
2. **Independent source mapping:** at least two distinct search strategies. Freeze citations and source versions.
3. **Blind proposal round:** candidate-generating models do not see each other's ideas yet.
4. **Structured hypothesis cards:** mechanism, predictions, competitors, expected cost, smallest discriminating experiment.
5. **Prior-art/novelty check:** search the open literature and code. Classify: already known, adaptation, novel combination, or plausible new mechanism. Uncertain novelty must remain uncertain.
6. **Critique by independent role:** identify counterexamples, data leaks, bad assumptions, security and licensing concerns.
7. **Selection:** select *diverse, testable* proposals; do not equate consensus, elo tournament score or judge preference with factual correctness.
8. **Prototype:** implement the smallest mechanism that could falsify the claim. Run in isolated worktree/fixture.
9. **Independent measurement:** blinded test cases, fixed model/version, budget matched best-of-N control, regression and cost reporting.
10. **Replication:** separate run/owner/model where possible; record disagreement and ambiguity, revise theory and retain failed hypotheses.

## Interaction protocol: avoid false consensus

- **Round 1** each model receives the same evidence snapshot and task question independently.
- **Round 2** reviewers see anonymized proposals; they must return strengths, falsifiers and missing evidence, **not** simply choose a winner.
- **Round 3** the proposer can respond to factual criticism while retaining old versions.
- **Round 4** experimental results, not debate persuasiveness, determine whether claims are supported.
- **Minority hypothesis preservation:** an apparently unpopular explanation may still be correct. Do not discard without an explicit test.
- **No infinite self-evolution:** cap rounds, context tokens and budget; prevent recursive self-invocation.

## Model collaboration without assuming proprietary details

Candidate configurations:
- **Vibe** as codebase-exploration and implementation worker, using its publicly documented tools.
- **Another frontier coding model** as an independent architecture challenger and test designer.
- **One separate model** for literature comparison and failure analysis.
- **Deterministic validators** for Git diff, schema, code tests and benchmark scores.

Examples of eligible model providers in principle: Mistral, OpenAI, Anthropic, Google and local open-weight models. **No adapters, credentials, model versions or provider availability are asserted to be present.** Select models by tested API and cost/performance, not brand loyalty.

Different models can challenge one another's assumptions, but a *single* model sampled several times is a required budget-matched control. Model diversity without independent checking is not a scientific method.

## Research record schemas (project-owned, not provider APIs)

Each study has immutable:
- study_id, hypothesis_id, source_snapshot and date;
- role/model/provider/model-version, temperature, context budget;
- proposed architecture and rationale;
- blinded test case manifest and environment hash;
- attempted actions with tool outputs and errors;
- result metrics with null for unmeasured values;
- red-team/novelty/reproducibility verdicts;
- rights and security review;
- raw trace pointer stored *outside* public repository.

### Proposal example

~~~json
{
  "proposal_id": "P-H01-001",
  "hypothesis_id": "H-01",
  "creator": {"role": "theorist", "model": "PINNED_MODEL"},
  "mechanism": "Retrieve only when current task uncertainty requires external evidence.",
  "novelty_status": "unverified",
  "predictions": ["Better resolution-per-cost on mixed coding tasks"],
  "rival_explanations": ["The gains come only from extra inference time"],
  "minimum_experiment": "Compare forced top-k against abstaining retrieval at matched budget.",
  "required_sources": ["https://arxiv.org/abs/2607.24882"],
  "confidence": "hypothesis-only"
}
~~~

### Experiment manifest example

~~~yaml
experiment_id: X-H01-001
hypothesis_id: H-01
preregistered: false
model: PINNED_MODEL
repository_snapshot: FULL_COMMIT_SHA
variants:
  - no_retrieval
  - mandatory_topk
  - selective_retrieval
  - equal_budget_resampling
primary_metric: independent_resolved_rate
secondary_metrics:
  - correct_file_recall_at_10
  - tokens_total
  - wallclock_seconds
  - adverse_tool_events
task_source: HELD_OUT_TASK_MANIFEST
answer_keys_access: evaluator_only
~~~

## Quality gates for a 'frontier hypothesis'

1. **Mechanism:** a precise causal explanation, not a relabeled feature.
2. **Novelty search:** explicit adjacent prior art, similarities and differences.
3. **Counterexample:** at least one situation expected to make the mechanism fail.
4. **Discriminating test:** a cheap experiment where two theories predict different outcomes.
5. **Transfer:** distinguish memorization from generalization to new repos/languages/models.
6. **Risk:** model hallucination, adversarial retrieval, prompt injection, privacy/license and supply-chain.
7. **Honest limits:** no guaranteed improvement and no assumption of model-internal parity.

## Beyond known techniques: three high-potential concept families

### C1 — Capability-deficit diagnosis

Before retrieval, classify whether a task is blocked by:
- knowledge gap,
- local code localization gap,
- executable-environment gap,
- verification gap,
- unclear specification.

**Novel combination hypothesis:** routing based on *diagnosed deficit* can outperform task-type routing, because two bugs of the same nominal category may need radically different tools.

Proposed tests: manually labeled deficit dataset, routing confusion analysis, equal-budget evaluation.

### C2 — Evidence-linked skill gene pool

Each verified procedural unit carries:
- preconditions and applicability boundaries,
- actual positive/negative task evidence,
- implementation-independent steps,
- dependency/version scope,
- estimated transfer gain vs no-skill baseline,
- counterexamples and sunset/review rule.

A research agent may **mutate or recombine candidate skills** to create novel candidates, but candidates remain quarantined until independent tests show benefit. This is not biological evolution; "gene pool" is an explanatory metaphor.

Proposed tests: learned vs hand-authored vs no-skill, including negative transfer.

### C3 — Epistemic context compiler

Rather than indiscriminately inserting documents, compile a *bounded evidence pack* for each action:
- current repo state and exact symbols,
- version-matched technical facts,
- relevant procedure plus its preconditions,
- disconfirming evidence,
- what is still unknown,
- independent verifier choice.

The compiler may choose to provide **no external context** when the evidence is irrelevant. The task records point back to raw sources rather than copying entire histories into prompts.

Proposed tests: compare top-k chunks, coherent summaries and compiler-produced evidence packs on novel tasks, with equal token budgets.

## Research independence and privacy

- Keep private repository content and full agent traces off public GitHub.
- Do not feed confidential user/company code or personal information to external provider APIs without authorization.
- Do not assume provider outputs can be trained on or re-published; review Terms and source licenses.
- Agents cannot approve their own experiments, merge unreviewed code or overwrite authoritative source registries.
- Do not use test answers, hidden patches or known benchmarks as retrieval resources when evaluating the same tasks.

## What VIBE-optimizer should deliver from this laboratory

- A living **theory** with mechanistic explanations and counter-theories.
- A **hypothesis registry** with preregistration and negative results.
- A **source/evidence graph** linking claim → paper → mechanism → prototype → test.
- Detailed **Technical Design Documents** for candidate scripts, schemas and MCP tools.
- Small reference implementations only when they can discriminate between hypotheses.
- A reproducible multi-model research protocol that does not conflate confidence, consensus and truth.

See:
- [Theory](THEORY-OF-EXTERNAL-COGNITION.md)
- [Hypothesis Registry](../research/HYPOTHESIS-REGISTRY.md)
- [Evaluation](EVALUATION.md)
- [Source Registry](SOURCE-REGISTRY.md)
