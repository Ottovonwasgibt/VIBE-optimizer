# Quantitative Capability Frontier — research and calculation notes v0.1

**Date:** 2026-11-05. **Status:** hypothetical mathematical models, NOT measured VIBE-optimizer results. All numerical probabilities below are synthetic examples. The user-facing mission is in [Capability Maximization](../docs/CAPABILITY-MAXIMIZATION.md).

## The research question

Which marginal change—better gap recognition, tool discovery, tool fit, correct use, independent verification, longer model reasoning, or a reusable tool—moves the independently verified task-solving frontier most, **per unit total budget**, for one fixed coding model?

## Model A — A capability chain, not a single model-quality number

On tasks where a specific external capability is necessary, track a nested chain of events:

- G: agent recognizes the capability gap;
- D: it discovers a candidate tool **conditional on G**;
- F: it confirms that the candidate is compatible/reachable **conditional on D**;
- U: it invokes or adapts the tool correctly **conditional on F**;
- S: it completes the task correctly according to independent tests **conditional on U**.

By the probability chain rule (NOT an assumption of independence):

    P(G∩D∩F∩U∩S)
      = P(G) × P(D|G) × P(F|G,D)
        × P(U|G,D,F) × P(S|G,D,F,U)

The one-number product is a **diagnostic proxy for completion along this chosen path**, not a general model success probability: fallback paths, changing tools, retries and tasks not needing tools also exist.

Synthetic illustration:
- Baseline conditional fractions: 0.70 × 0.65 × 0.85 × 0.80 × 0.90 = **0.27846**.
- Enhanced diagnosis and discovery only: 0.90 × 0.85 × 0.85 × 0.80 × 0.90 = **0.46818**.
- Difference: **+18.972 percentage points along the idealized path**; relative gain about **68%**. This is NOT a predicted performance uplift for Vibe.

Interpretation: when gap recognition and tool search are the bottleneck, increasing context size without improving those two stages may deliver little benefit. Conversely, improving only discovery fails if the tool is unusable.

Research tasks should label the stage at which each real attempt fails. Otherwise a failed overall result is not informative about the architecture.

## Model B — Tool *set completeness* rather than single-tool recall

For a workflow requiring several dependent tools, finding a single correct tool is insufficient. Define:

    completeness@k =
      number of tasks where ALL required tools are in top-k
      / number of evaluated tasks

If a toy retriever finds each of four needed tools with 85% probability and the events were **independent**, then the probability of discovering all four would be:

    0.85^4 = 0.52200625 (~52.2%).

Independence usually fails in practice; workflows have shared APIs, dependency order, correlated misses, and repeated discovery. Use this number **only** to illustrate compounding failure, and evaluate real \`set-completeness@k\` on labeled workflows.

2026 primary study about multi-tool retrieval:
https://arxiv.org/abs/2610.41905

## Model C — Expected value of checking the workbench

When should Vibe search or probe another tool instead of continuing to reason?

Let:
- \`p_gap\` = estimated probability that extra capability is actually needed;
- \`delta_p\` = additional task success probability *if it is needed and suitable*;
- \`V\` = value of resolving task, expressed in one consistent utility unit;
- \`C_probe\` = retrieval/probe/time/token cost in same units;
- \`C_risk\` = expected cost of inappropriate choice or security/recovery impact.

Expected incremental utility (simplifying approximation):

    EV_probe = p_gap × delta_p × V - C_probe - C_risk

Choose the probe only if \`EV_probe > 0\` and authorization constraints are satisfied.

Toy values in human-minute-equivalent units:
\`p_gap=0.35\`, \`delta_p=0.25\`, \`V=120\`, \`C_probe=4\`, \`C_risk=3\`.

    EV_probe = 0.35×0.25×120 - 4 - 3 = +3.5 minutes equivalent.

Indifference threshold:

    p_gap* = (C_probe + C_risk)/(delta_p × V)
           = 7/(0.25×120) = 0.2333...

If the estimated capability need is below ~23.3% **under these toy assumptions**, a probe has negative expected value. If \`V\` is high, the threshold decreases. These probabilities **must be calibrated**, not hallucinated by a model. Risk constraints may veto an action regardless of positive utility.

A more principled later design compares **Expected Value of Sample Information (EVSI)** after a diagnostic probe against not probing, using empirical outcome distributions and explicit opportunity cost. The simple equation above is an initial heuristic only.

## Model D — When is writing a reusable tool worth it?

A newly created tool should have a nontrivial *future reuse horizon*, unless it enables a one-off otherwise unsolvable high-value task.

Let:
- \`C_build\` = design and implementation time;
- \`C_validate\` = independently qualifying the tool;
- \`C_maintain\` = expected support/maintenance cost;
- \`p_usable\` = chance it works and is applicable at future use;
- \`s\` = human-minute-equivalent savings per valid reuse;
- \`N\` = number of future eligible tasks.

Break-even:

    N ≥ (C_build+C_validate+C_maintain)/(p_usable×s)

Toy numbers: 120 + 60 + 30 = 210 minutes; \`p_usable=.8\`; \`s=12\` minutes.
\`N ≥ 210/(.8×12)=21.875\`; break-even at **22 eligible reuses**.

If the tool creates a new capability rather than only saving time, additionally model the value of otherwise unsolved tasks. Always track tool regressions and maintenance drift.

## Model E — Context carrying cost of tool definitions

With 60 tools averaging 600 tokens of schema, a static list uses **36,000 tokens** before the model solves the task.

A hypothetical dynamically searched workbench with a 500-token discovery interface and four loaded tool schemas would use:

    500 + 4×600 = 2,900 tokens.

Difference: **33,100 tokens** (~91.9% of the 36,000-token static overhead). This excludes search query/results, extra inference turns and cache behavior; it is not a Vibe benchmark.

Anthropic (2025) reported major context savings and improved accuracy with tool search:
https://www.anthropic.com/research/advanced-tool-use
Microsoft Foundry similarly documents searchable toolboxes:
https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/tool-search

**Research extension:** don't optimize context savings alone. Measure if the required tools were *actually discovered*, and whether the extra search steps delayed or worsened the task.

## Model F — Capability frontier as a function of budget and difficulty

Define for a fixed model, task family, architecture and total budget:

    P_solve(d, b, a) = P(independent checks pass | difficulty d, budget b, architecture a)

Vary \`b\` (token, tool-call, wall-time, optionally dollar) and \`d\` (predeclared task difficulty, repository size, task human-time horizon). Estimate curves from repeated task runs; compare:
1. unmodified Vibe at budget B;
2. same Vibe with additional reasoning/search attempts and **equal budget**;
3. Vibe + external cognitive stack, equal budget;
4. stack with adaptively allocated budget, reported separately.

Potential metrics:
- area under success-vs-budget curve;
- cost to reach fixed success rate on a task stratum;
- longest task difficulty/horizon reliably solved at predeclared confidence level;
- tool call and token usage per independently verified success;
- safety/recovery risk at each budget.

Do **not** infer general intelligence from a single benchmark score. AISI reports strong test-time-compute dependence and warns that evaluation budgets can hide capability:
https://www.aisi.gov.uk/blog/more-compute-more-capability-why-ai-agent-evals-need-to-account-for-test-time-compute

Budget-aware search work:
https://research.google/pubs/cost-effective-agent-test-time-scaling/

## Six competing engineering experiments, in priority order

**Q1 / failure-stage attribution (first):** instrument 30-50 realistic tasks and label G/D/F/U/S; diagnose which weak gate to target. Do not call the labeler's guess ground truth without independent review.

**Q2 / discoverability and completeness:** compare hot-only tools, all static tools, searchable tool catalog, searchable catalog plus dependency-set coverage. Introduce tasks that require 2–5 tools and *negative controls needing no extra tool*.

**Q3 / adequacy probing:** add version/permission/health validation before tool invocation; compare tool contract errors, wasted calls and verified task success to Q2.

**Q4 / tool composition:** test whether sequencing or combining two already-approved tools solves tasks without new installations; measure correctness and additional costs.

**Q5 / tool making and transfer:** permit isolated proposals for small scripts; require tests and human/admin approval before reuse; compare unseen tasks and maintenance cost.

**Q6 / adaptive compute allocation:** compare static token/tool-call limits against a budget policy guided by observed progress and independent test feedback.

### Existing literature that narrows novelty claims

- ICML 2026 AutoTool learns dynamic tool selection **with model training** (not same as our fixed-weight runtime): https://proceedings.mlr.press/v306/zou26p.html
- 2026 SkillCraft explores learning and reusing tool compositions: https://arxiv.org/abs/2603.00718
- 2026 retrieval study exposes set-completeness failures: https://arxiv.org/abs/2610.41905
- 2026 tool-use diagnostic TRIDENT separates judgment, planning and execution: https://aclanthology.org/2026.findings-emnlp.1862/
- 2026 CATS explores budget-aware test-time scaling: https://research.google/pubs/cost-effective-agent-test-time-scaling/

**Possible research contribution, unproven:** in-execution capability-gap diagnosis + tool set completeness + suitability probing + validated tool adaptation, with a single fixed-weight model and a measured task/cost frontier.

## Falsification and scientific discipline

Record failed and negative results, tasks solved without tools, false-positive tool creation, unsafe upgrade requests and degradation from extra context. Experimental thresholds and protocols must be chosen *before* seeing results. Use task-distribution stratification and blind grading. This document offers quantitative reasoning and experimental design, **not** evidence that VIBE-optimizer currently raises performance.
