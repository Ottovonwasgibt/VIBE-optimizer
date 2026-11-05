# Capability Maximization Programme — "Super Saiyan" objective

**Date:** 2026-11-05
**Status:** project mission and research programme, **not** a claim of superhuman model intelligence or an implemented mode.

## Mission: unlock maximum *effective* capacity

The project's ultimate goal is to push **one chosen task-solving model, initially Mistral Vibe**, as close as practical to its **system-level capability frontier** through external cognitive infrastructure. The goal is *not* to assemble as many agents as possible. Additional models or subagents are **optional tools**, evaluated only against equivalent single-model alternatives.

The ambition can be colloquially called *Super Saiyan mode*. Engineering term: **Capability Maximization Engine (CME)**.

A useful unit of progress is a task—whether coding, investigation, functional management or knowledge work—that the unaugmented model cannot reliably complete, but an augmented configuration **can complete and independently verify** under a clearly stated budget, without unacceptable safety regression.

## What is maximized?

No single scalar captures intelligence. Research a **multi-objective capability frontier**:

- **Competence:** probability of correctly resolving unseen, varied tasks.
- **Reach:** complexity/depth of task families reachable (versions, repository size, long-horizon integration, formal requirements).
- **Reliability:** consistency across reruns; success not based on lucky samples.
- **Autonomy within bounded permissions:** number of useful steps requiring no human intervention, without permission bypass.
- **Learning through external state:** transfer of *verified* experience and reusable procedures to different tasks.
- **Efficiency:** verified successes per time, token, cost and tool invocation.
- **Grounding and safety:** provenance, resistance to injection, no confidential leaks, ability to abstain, minimal destructive actions.

The system should expose the **Pareto frontier** of these objectives rather than hide trade-offs behind a marketing "IQ" number. Some modes optimize resource cost; a deliberate deep mode may spend more inference or verification budget to solve previously inaccessible tasks.

## Baselines are mandatory

For the same pinned model and held-out tasks:

A. **Naked baseline:** model + standard Vibe functionality, no project enhancements.
B. **Budget-matched single-agent scaling:** same model allowed more reasoning / retries / sampling, no new cognitive library.
C. **Augmented single agent:** targeted knowledge, skills, memory, tools and verification, with the same total budget as B when feasible.
D. **Augmented high-budget mode:** adaptive resource use, explicitly disclose extra cost.
E. **Optional diverse-model system:** independent specialist/reviewer only if it outperforms C/D on objective outcomes or cost.

This isolates *real external augmentation* from just paying for more model calls. Multi-agent is not a default rung or a milestone.

## The six capability levers

### L1 — External knowledge: know more, more accurately

Versioned documentation, algorithms, domain theory, project architecture, dependency contracts, evidence. Retrieval must select relevant snippets, not flood context.

**Research lever:** coverage × retrievability × compatibility × application reliability.

### L2 — External methods: know *how* to attack a problem

Conditional procedures, checklists, diagnosis, heuristics, algorithm templates, counterexample-driven methods, task decomposition. Use short skills with applicability criteria and proof of transfer.

**Research lever:** reusable procedure with tested boundaries; automatically generated skills are only candidates until validated.

### L3 — External computation: do things text generation cannot establish

Run precise tools: compilers, typecheckers, unit/integration tests, static analyzers, parsers, search, formatters, symbolic solvers, profilers and simulations. The external system can generate **new observations**, not merely add context.

**Research lever:** choose highest-information tool for the current uncertainty, under privileges/budget.

### L4 — External memory: retain usable experience

Store task episodes, hypotheses, failed attempts, repairs, test evidence, lesson conditions, versions, and conflicting observations. Promote only reviewed transferable insights; expire or scope invalidated knowledge.

**Research lever:** verified transfer and prevention of repeated failure, not infinite transcript accumulation.

### L5 — Meta-cognition: direct effort to the bottleneck

Diagnose capability deficit before choosing next action:
- unavailable technical knowledge;
- missing repo localization;
- missing executable/permission environment;
- absence of test oracle;
- underspecified requirement.

Use selective retrieval, dynamically adjusted verification, and abstention when evidence is insufficient. The best upgrade may be **not** using a tool.

**Research lever:** adaptive, cost-aware action selection with explicit uncertainty and fallback.

### L6 — Deliberate reasoning / adaptive inference

Allow the *same model* to explore competing hypotheses, simulate consequences, use search/branching when helpful, compare candidate patches, and spend more inference budget only on difficult tasks. This lever is not equivalent to multi-agent architecture.

**Research lever:** compare sequential reasoning, budget-matched candidate search and structured verification before considering a second model.

## Performance modes (research taxonomy, not currently implemented CLI flags)

| Mode | Purpose | Selection approach | Constraints |
| --- | --- | --- | --- |
| Foundation | Correct minimal model/tool interface | Current Vibe baseline | No extra retrieval |
| Informed | Relevant facts and repository context | Targeted evidence | Provenance, version |
| Deliberate | Better plans and checked alternatives | Procedural skills + test loop | Bounded retries |
| Adaptive | Choose tools and effort by measured deficit | Router + verified memory | Confidence/budget gates |
| Frontier ("Super Saiyan") | Attempt difficult tasks beyond baseline reach | Selective deep reasoning + active solvers + all *validated* levers | Explicit budget, safety controls, rollback |

**Important:** This is a classification for controlled experiments; it does not promise a performance increase, and every proposed layer may be removed if measurements show negative transfer.

## A concrete example: unfamiliar large-codebase bug

**Without augmentation:** agent reads a few files, guesses at a patch, may run a test.

**CME hypothesis:** the agent first identifies whether the obstacle is unknown API semantics, code location or missing tests; retrieves the exact dependency version and a Git-aware symbol map; formulates multiple hypotheses; asks a relevant verifier to produce counterevidence; patches the smallest surface; tests regressions; records verified applicability and known failed strategies for future tasks. Optionally spends more time on high-impact failures, but does not automatically call another model.

**What counts as an actual breakthrough?** A held-out issue repeatedly unresolved by baseline and equal-budget single-model retries becomes reliably solvable with the cognitive stack, under reproducible conditions.

## Capability frontier research questions

1. What task classes remain impossible even with perfect documentation retrieval? What active computation would change the limit?
2. Can we diagnose *why* an agent is stuck before choosing evidence or tools?
3. Can the agent compile new, verified procedural strategies from experience rather than just replay transcripts?
4. Under what conditions does external memory reduce rather than amplify error?
5. How should resource allocation scale with task complexity and uncertainty?
6. Can we make context **reversible**: compact active window, raw evidence available on demand?
7. What is gained by several candidates from **one model** compared with a second independent model?
8. Where does environment complexity hurt: tool latency, failure modes, prompt contamination and maintenance?

## Prototype candidates aligned with the levers

| Candidate | Function | First experiment | Dependencies |
| --- | --- | --- | --- |
| Evidence compiler | Build cited, bounded task context | Retrieval on/off; selective vs top-k | L1, L5 |
| Repository intelligence | Git-aware symbols, dependency versions and tests | Correct-file localization vs lexical | L1, L3 |
| Procedure evaluator | Execute and score targeted skill intervention | Skilled vs unskilled held-out tasks | L2, L3 |
| Verification selector | Choose test/typecheck/solver based on failure | Same-model extra sample vs external checker | L3, L6 |
| Memory curator | Distinguish episodic/semantic/procedural and failures | Transfer and negative-transfer set | L4 |
| Adaptive controller | Diagnose deficits and allocate budget | Static workflow vs adaptive, budget matched | L5, L6 |
| Optional model reviewer | Challenge or diversify hypotheses | Same-model best-of-N vs reviewer | Optional |

## How new theoretical knowledge enters the project

For every candidate: source/prior art → explicit mechanism → counter-theory → falsifiable prediction → minimal prototype → independent evaluation → replication → revision or rejection.

A model can invent an architecture candidate; it cannot independently certify the scientific novelty or real effectiveness of its own proposal. Store failed or contradictory findings.

## Evidence and required distinctions

- **Established fact:** public specifications and independently checked code/evaluation.
- **Supported research finding:** cited study's reported observation with task/method limits.
- **Working hypothesis:** concrete predicted improvement with a plausible mechanism.
- **Prototype:** implemented and tested module; not proof of general performance.
- **Measured improvement:** controlled experiment with pinned model, task and budget.
- **Theoretical contribution:** explanation of why/when improvements occur, tested against plausible alternatives.

A big tool list is *not* proof of capability. A benchmark score is *not* proof of generalized intelligence.

## What is out of scope unless justified

- Multiagent swarms as an architectural objective.
- Copying proprietary model weights, training data or hidden prompts.
- Automatically trusting third-party skills, code or tool output.
- Self-approving memories, modifying authorization policy, autonomous permission escalation.
- Expensive knowledge graphs before they beat simpler retrieval.
- Benchmark-result claims without rigorous leakage and budget controls.

## Where the optional multi-model lab fits

The [Multi-Model Research Lab](MULTI-MODEL-RESEARCH-LAB.md) is a **research method**, not CME's product architecture. Use a second model only for an independently useful task (e.g. novel prior-art search or adversarial review) and always compare against running the principal model multiple times with the same budget.

## Related documents

- [Working causal theory](THEORY-OF-EXTERNAL-COGNITION.md)
- [Hypothesis registry](../research/HYPOTHESIS-REGISTRY.md)
- [Knowledge and tools architecture](ARCHITECTURE.md)
- [Frontier evidence dossier](../research/FRONTIER-EVIDENCE-DOSSIER.md)
- [Ablation evaluation](EVALUATION.md)
- [Roadmap](ROADMAP.md)

## Domain-independent capability frontier

The workbench is not a code-only product. In higher-education functional management the objective includes solving previously difficult **Osiris/Studielink process and integration questions** with documented evidence and the correct procedural judgment. Tools may be documentation search, process/state reconstruction, log correlation, report-definition comparison or tested scripts; the best next action may be to seek authorized confirmation rather than write code.

See [Domain-Agnostic Capability Engine](DOMAIN-OPERATIONS-CAPABILITY-ENGINE.md) and the [higher-education example](DOMAIN-DESIGNS/01-higher-education-functional-management.md). Reevaluate the current evaluation metric: independently verified operational correctness, safe escalation, source fidelity and actual time savings are as important as benchmark patch resolution.
