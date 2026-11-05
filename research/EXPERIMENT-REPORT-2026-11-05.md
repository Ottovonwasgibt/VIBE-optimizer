# First Executed Pilot — Workbench Retrieval and Versioned API Recipes

**Date:** 2026-11-05  
**Status:** experiments **executed**, with successful local and GitHub Actions reproduction.  
**CI:** https://github.com/Ottovonwasgibt/VIBE-optimizer/actions/runs/42038453644  
**Important limitation:** **NO Mistral Vibe model, frontier LLM, agent-generated code, or actual task-solving agent was executed.** This report evaluates two *supporting mechanisms* using synthetic catalog retrieval and real Pydantic API smoke tests. No general agent-capability gain is established.

## Motivation

The Capability Maximization Engine proposes version-aware knowledge packs, an Adaptive Tool Workbench, and selective tool discovery. Before funding an expensive Vibe A/B trial, test whether these mechanisms are executable, produce diagnostic data, and reveal meaningful failure cases.

## Environment and reproducibility

| Component | Observed environment |
| --- | --- |
| Local test Python | 3.13.5 |
| Local search | SQLite FTS5, in-memory database |
| API dependency | Pydantic 2.13.5 |
| API v1 behavior | \`pydantic.v1\` compatibility namespace **inside Pydantic 2**, not separate old install |
| Vibe CLI / local model | Not present in experiment container |
| Independent rerun | GitHub Actions Ubuntu / Python 3.13, 4 tests passed, both scripts executed successfully |

Source and reproducibility:
- [Workbench retrieval script](../experiments/pilots/workbench_pilot.py)
- [Pydantic API script](../experiments/pilots/pydantic_packs_pilot.py)
- [Pilot regression tests](../experiments/pilots/test_pilots.py)
- [Pilot README and methods](../experiments/pilots/README.md)
- [Results summary JSON](../experiments/pilots/results-summary.json)

## Experiment 1 — Can a searchable workbench select the right instruments?

### Method

Manually author **24 tool metadata cards** and **28 task queries**:
- 15 single-tool tasks,
- 9 multi-tool tasks,
- 4 no-tool negative controls.

Keep required gold tool IDs in task records only for evaluator scoring; the selection policy receives task text and scope. Each strategy selects a maximum of three tools.

Four policies:
1. \`static\`: fixed three popular tools (a deliberately weak control, **not a faithful Vibe baseline**).
2. \`bm25\`: FTS5 lexical search using tool title/description.
3. \`filtered\`: BM25 plus scope/version and known usability filters.
4. \`plan\`: simple split on conjunctive clauses, filtered BM25 and simple no-tool abstention.

Metric: **usable tool slate** = all gold required tools included AND none of the selected tools is explicitly incompatible/unavailable; a no-tool task must receive no tools. This is *not* actual tool invocation correctness or task resolution.

### Observations (executed)

| Policy | Usable slate /28 | Single /15 | Multi /9 | No-tool /4 | Incompatible tool selections |
| --- | ---: | ---: | ---: | ---: | ---: |
| Static top-3 | **3** | 3 | 0 | 0 | 0 |
| BM25 | **18** | 8 | 7 | 3 | 10 |
| BM25 + compatibility filters | **25** | 14 | 8 | 3 | 0 |
| Text-clause plan + filters | **26** | 14 | 8 | 4 | 0 |

**Sensitivity:** raw BM25 at k=5 falls to **14/28** under this strict slate-validity metric, as extra inappropriate tools enter the slate. Filtering + splitting at k=5 reaches **27/28**. This is a study-specific observation, not an inference about all agent toolboxes.

### Failure analysis / actual finding

- Initial metadata scope filter had a bug: when task scope was \`any\`, version-specific tools slipped into the output. During pilot development this was caught, corrected to require exact matching for scoped tools, and regression tested.
- \`t01\` (Python symbol definition) still misses target with lexical ranking.
- \`t19\` (SQLite performance + migration safety) misses one required tool at k=3.
- The no-tool detection heuristic helps one task but may be overfitted to phrases like \`explain\` or \`describe\`.

Interpretation: version and reachability metadata make the **selection slate** cleaner; both good and bad choices become visible. The experiment does **not** establish that actual coding agents solve more programming tasks with this setup.

## Experiment 2 — Do tested API recipes detect real version mismatch?

### Method

Use **real installed Pydantic** interfaces:
- \`pydantic.v1.BaseModel\` compatibility API (legacy methods);
- \`pydantic.BaseModel\` v2 API (modern methods).

For each target × recipe combination execute **seven operations**: validate, serialize to dict, serialize JSON, produce JSON schema, copy model, construct model and inspect fields. Independently compare return values to expected outputs and collect deprecation warnings.

### Observations (executed)

| Target | Legacy recipe | Modern recipe |
| --- | --- | --- |
| Pydantic v1 compatibility API | **7/7 passed**, 0 deprecations | **0/7 passed** |
| Pydantic v2 API | **7/7 passed**, 7 deprecations | **7/7 passed**, 0 deprecations |

Interpretation:
- A correct-version API recipe can be necessary: modern Pydantic v2 method calls are not automatically compatible with the older API.
- Compatibility can be **asymmetric**: older method names still worked with Pydantic v2 but emitted deprecation warnings.
- A **Capability Pack** should store both exact-version method contracts and known migration/deprecation paths, not simply latest examples.

**Important:** this experiment **manually applied** specific method recipes and tested API behavior. It did not evaluate whether a model would choose or synthesize them with or without retrieved manuals.

## What we know — and what we do not know

**Directly observed in this pilot:** the ranking/filter/splitting programs have measurable behavior on our handmade task set; a scope-filter bug was corrected; seven legacy and seven modern method calls behaved asymmetrically on Pydantic 2.13.5; four pilot unit tests and a GitHub Actions rerun passed.

**Not established:** Vibe pass@1 uplift; a model's capacity to learn from Capability Packs; validity on unrelated software stacks; transfer to other task formulations; real-world tool discovery quality; meaningful statistical generalization. The 28 tool-query prompts were crafted for the pilot and are not an unbiased sample.

## The minimum credible next study with Vibe

1. Pin a specific Mistral Vibe version/model, system prompt, total inference/tool budget and runtime.
2. Design fresh **12–20** issue-level software tasks with hidden executable tests. Include multiple real library versions in **separate pinned environments**, not only a compatibility namespace.
3. Compare model runs for: **(A) no supplied docs**, **(B) raw official docs**, **(C) exact-version reference pack**, **(D) version pack + tested recipes**, and **(E) budget-matched extra reasoning without pack**.
4. Include no-retrieval controls and deliberately outdated doc examples; ensure the test-answer code is not in the retrieval corpus.
5. Measure independently verified resolution, API contract violations, tool calls, tokens, latency, cost and security or leakage.
6. Pre-register analysis and retain failed/negative cases. Do not call small pilot differences statistically conclusive.

The goal is to discover **whether external libraries cause measurable improvement in the model**, not merely show that a version-aware program can select correct functions.

## Follow-ups

- [Issue #8: Capability Pack benchmark](https://github.com/Ottovonwasgibt/VIBE-optimizer/issues/8)
- [Issue #7: Quantitative capability frontier](https://github.com/Ottovonwasgibt/VIBE-optimizer/issues/7)
- [TDD-08: Capability Library and Stack Atlas](../docs/TECHNICAL-DESIGNS/06-capability-library-stack-atlas.md)
- [TDD-07: Adaptive Tool Workbench](../docs/TECHNICAL-DESIGNS/05-adaptive-tool-workbench.md)

**Research verdict:** Two real infrastructure hypotheses have been operationalized, measured and reproduced; **no claim of Vibe cognitive uplift is justified yet**.
