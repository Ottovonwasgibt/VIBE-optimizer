# Theory of External Cognitive Augmentation (TECA) — working theory v0.1

**Date:** 2026-11-05  
**Status:** original **proposed explanatory theory**, not a validated scientific theory.  
**Scope:** fixed-weight tool-using language models, initially software-engineering agents.

## Abstract

A fixed language model may achieve higher *effective* competence when a surrounding system supplies appropriate evidence, procedures, computation, state and verification at the right time. Mere access to more information is not sufficient. We propose that external cognitive augmentation is best understood as a **causal, budget-constrained process of transforming latent problem-solving possibilities into verified actions**.

This distinguishes **parametric capabilities** (what the model can produce without added infrastructure), **environmental affordances** (what knowledge and computation it can access), **orchestration quality** (when and how affordances are used), and **epistemic control** (how wrong outputs are detected and corrected). The key observable is *independently verified task success*, not self-rated reasoning quality.

The goal of TECA is to generate **testable, potentially false predictions** about these relations. It must be revised or abandoned when measurements contradict it.

## Theory building blocks

### Construct 1 — Capability is task-conditional, not a single intelligence score

Let:
- **m** = fixed model configuration and inference settings;
- **t** = held-out task and repository snapshot;
- **a** = agent architecture/policy;
- **e** = environment and available libraries/tools;
- **b** = bounded budget (tokens, money, wall-clock, tool calls);
- **Y(m,t,a,e,b)** = externally assessed outcome: resolved=1, not resolved=0.

Effective capability in a task distribution **D** is:

    Q(m, a, e, b, D) = E[t ~ D][Y(m,t,a,e,b)]

This is an **operational outcome definition**, not a psychometric measure of intelligence. A library changes e; skills, routing and validation change a; none of these modifies the weights of m.

The causal effect of component **c** at matched budget:

    Delta(c | m, D, b, a) =
        E[Y | do(c = on), m, D, b, a]
      - E[Y | do(c = off), m, D, b, a]

Report confidence intervals, failures and negative effects; uncontrolled benchmark differences are *not* causal estimates.

### Construct 2 — The augmentation chain has several failure gates

For a given task, a useful source or procedure must be:

1. **available**: the needed evidence/tool exists and can be legally accessed;
2. **discoverable**: the router/retriever can identify it;
3. **compatible**: it matches code revision, library version and problem context;
4. **interpretable**: the model can apply it correctly;
5. **actionable**: the environment permits execution within budget;
6. **verifiable**: independent checks can distinguish valid from invalid results.

These gates are **not assumed statistically independent**. A rough diagnostic decomposition may estimate the *conditional* success frequencies at each gate. It is **not** a justified claim that their raw probabilities may be multiplied as a universal formula.

Interpretation: a huge corpus may raise availability but reduce discoverability, compatibility or interpretability. Under some tasks a modest, curated corpus could outperform a much larger one.

### Construct 3 — Meta-control is an allocation problem

A useful agent should decide among:
- answer using present context;
- look up one targeted source;
- inspect local repository symbols;
- call a specialized tool/solver;
- activate a procedure/skill;
- request clarification or human approval;
- test a candidate;
- abstain/stop.

A policy should maximize expected *verified* task utility subject to **budget, privilege and risk constraints**. Its most important function may be deciding **not** to retrieve, or knowing when evidence is insufficient.

### Construct 4 — External memory needs epistemic types

Do not flatten all knowledge into a vector collection.

- **Semantic claims:** general facts from versioned sources;
- **Repository claims:** symbol/behavior statements tied to Git + dirty state;
- **Procedural skills:** instructions with preconditions and acceptance tests;
- **Episodic traces:** particular prior runs with evidence and outcomes;
- **Normative policies:** permissions and user instructions; not retrievable documentation;
- **Counterexamples:** known failed strategies and boundary conditions.

A memory promotion process may transform a sequence of episodes into a candidate skill **only if** independent evidence supports transfer beyond the original task and exposes applicability constraints.

### Construct 5 — Verified action is a source of new information

Independent execution, unit tests, counterexamples and formal solvers can provide evidence not present in language-model parameters or retrieved text. This is **active computation**, not passive context enrichment. New reliable information should update the system's *external* state while preserving the original observation and provenance.

## A causal graph of a coding-agent episode

    Task + repository state
           |
           v
    Task diagnosis ----------------> Retrieval/skill decision
           |                                 |
           |                                 v
           |                         Evidence / tool affordances
           |                                 |
           +-------------> Plan <------------+
                                |
                                v
                       Patch / action proposal
                                |
                                v
                     Independent verification
                                |
                        outcome + failure cause
                                |
                           reviewed trace
                                |
                           typed memory
                                |
                                +--> future decisions

Potential confounds: model differences, task selection, budget drift, retrieval answer contamination, version drift, cross-agent copying, grader quality and human intervention. Explicitly log these.

## Theoretical predictions (all prospective, not observed in VIBE-optimizer)

- **P1: Retrieval conditionality.** Targeted evidence retrieval helps version-specific API tasks more than tasks solved from current repo/tests alone; over-retrieval may hurt simpler tasks.
- **P2: Verification interactions.** A diagnostic/test tool can increase the value of a procedure or retrieved source because failure is observable; without checking it may propagate bad guidance.
- **P3: Procedural transfer.** A small evidence-backed skill with applicability rules outperforms a generic instruction dump on related but unseen task families at matched cost.
- **P4: Typed memory.** Separating prior failure traces from verified reusable procedures reduces self-confirming or stale memory errors relative to untyped replay, all else equal.
- **P5: Version-aware knowledge.** Version-linked local/external API relationships beat unversioned retrieval on tasks whose solution depends on changing dependencies; may be inferior for simple local edits.
- **P6: Abstention.** A decision policy permitted to return no retrieval result should reduce harmful irrelevant context compared with compulsory top-k, without sacrificing too much relevant recall.
- **P7: Independent adjudication.** Multi-model idea generation can improve hypothesis coverage but **not necessarily result accuracy**; test-time diversity must be paired with independent checks and budget-matched sampling baselines.
- **P8: Reversible context.** Keeping evidence-addressable raw traces plus compact views may outperform irreversible summarization on long-horizon diagnosis when old details become relevant again.

## Crucial counter-theories to distinguish experimentally

1. **All benefit is compute:** better results arise merely from more tokens/attempts rather than external cognition. Compare equal token/time/cost budgets, including same-model best-of-N.
2. **All benefit is answer leakage:** external corpora contain task fixes or test answers. Use private, fresh, time-sliced held-out tasks and corpus exclusion.
3. **All benefit is model quality:** strong models use any context equally well. Fix model and vary augmentation, then test interactions across multiple models.
4. **Complexity tax:** additional routers/tools add latency and error points, hurting task completion. Measure negative transfer and maintenance.
5. **Selection bottleneck:** generating more hypotheses is useless without independent effective selection; compare selection strategies and calibration.
6. **Instruction overhang:** long AGENTS.md files worsen performance; compare minimal AGENTS.md vs conditional skills vs no added instructions.

## What would falsify TECA?

TECA is a *family of propositions*, not a single easily falsified numerical law. Reject or narrow an individual prediction when:
- controlled equal-budget ablations show no useful improvement or consistent regression;
- an apparently useful skill fails on independent unseen tasks;
- performance vanishes when leaked answer artifacts are removed;
- gains cannot be separated from model/model-budget changes;
- verification reliability is too low to support claimed memory improvements.

Keep failed predictions and explanations in the research register rather than rewriting history.

## Link to operational components

| Theory construct | Proposed component | Observable artifact |
| --- | --- | --- |
| Evidence availability | Curated source registry | Source provenance records |
| Discoverability | Retrieval/router | Query/results and retrieval recall |
| Compatibility | Version-aware code index | Snapshot and dependency-version IDs |
| Procedural transfer | Conditional skill catalog | Skill version + applicability gates |
| Active computation | Test/solver tools | Signed-or-hashed execution report |
| Epistemic learning | Typed memory curator | Proposed/reviewed/verified transition |
| Budget and meta-control | Decision router | Selection reasons and costs |
| Causal evidence | Paired experiment harness | Pre-registered ablations and run traces |

## Research foundations / conflicting evidence

- ACE — evolving contexts: https://arxiv.org/abs/2510.04618
- CrossCoder — dependency-aware cross-repository graph: https://aclanthology.org/2026.findings-emnlp.433/
- MSCE — evidence-grounded memory-to-skill: https://aclanthology.org/2026.findings-emnlp.1637/
- Unified Context Evolution — typed evolving units: https://aclanthology.org/2026.emnlp-main.2188/
- SkillGen — skill intervention measured on same instances: https://www.microsoft.com/en-us/research/publication/skillgen-verified-inference-time-agent-skill-synthesis/
- Agent Retrieval Bench — no-gold and context-selection failures: https://arxiv.org/abs/2607.24882
- AGENTS.md negative results: https://www.sri.inf.ethz.ch/publications/gloaguen2026agentsmd
- Multi-agent scientific research: https://www.nature.com/articles/s41586-026-10644-y
- Multi-agent hidden information failures: https://proceedings.mlr.press/v306/li26ej.html
- Multi-agent debate alternative explanations: https://arxiv.org/abs/2609.35875

**Do not call TECA a published or peer-reviewed theory.** Its distinct predictions and mechanisms need empirical evaluation, novelty checks and independent critique.
