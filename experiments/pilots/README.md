# Research pilots — executed 2026-11-05

**Scope:** first executable **infrastructure** experiments. They do **not** execute or benchmark Mistral Vibe, model generations, or scientific task-resolution accuracy. Tools and tool-selection queries are synthetic and researcher-authored; the API test uses real installed Pydantic interfaces.

## Environment used

- Python **3.13.5**
- SQLite **FTS5 available** (stdlib sqlite3)
- Pydantic **2.13.5**, including \`pydantic.v1\` compatibility namespace
- No Vibe CLI / Ollama available in the test container; no model-inference comparison performed.

## Reproduce locally

From this directory:

~~~powershell
python -m pip install pydantic==2.13.5
python -m unittest -v test_pilots
python workbench_pilot.py
python pydantic_packs_pilot.py
~~~

The first experiment needs no dependencies beyond Python+SQLite FTS5. The Pydantic test uses the \`pydantic.v1\` namespace shipped with v2; it does not install a separate v1 distribution. The scripts write detailed JSON result files into this folder. Those generated files should not be confused with model-performance metrics.

## Pilot A — Tool discovery, catalog fitness, task decomposition

- 24 metadata-only tool cards (including 3 version/engine-specific domains and one deliberately unavailable tool).
- 28 hand-authored task queries: **15 single-tool**, **9 multi-tool**, **4 no-tool**.
- Evaluation gold includes required tool IDs per task, never passed into the selection functions.
- Four simple policies, each limited to top-3 selected tools:
  - \`static\`: fixed three tool IDs (deliberately weak reference).
  - \`bm25\`: FTS5 lexical ranking over title and description.
  - \`filtered\`: same BM25 + environment/version and reachability filters.
  - \`plan\`: heuristic splitting on 'and/then', filtered BM25, simple no-tool detection.

**"Usable"** means the chosen tool IDs cover the manually assigned required set **without selecting any explicitly incompatible/unavailable tool** (for no-tool tasks, choose none). It is **not an executed tool-call outcome**, nor correctness on software tasks.

| Policy | Usable selection / 28 | Single /15 | Multi /9 | No-tool /4 | Incompatible selections |
| --- | ---: | ---: | ---: | ---: | ---: |
| Static top three | 3 | 3 | 0 | 0 | 0 |
| BM25 alone | 18 | 8 | 7 | 3 | 10 |
| BM25 + metadata filters | 25 | 14 | 8 | 3 | 0 |
| Heuristic plan + filters | 26 | 14 | 8 | 4 | 0 |

Notable unsolved selection cases:
- \`t01\`: Python symbol lookup; BM25 favors unrelated technical descriptions.
- \`t19\`: joint SQLite query-plan and migration safety; top-3 misses migration tool.
- \`t25\`: plain explanatory question; BM25 unnecessarily offers SQL tools, resolved by heuristic abstention.

**Sensitivity:** at \`k=5\`, raw BM25 selection fitness falls to **14/28**, because additional bad/incompatible suggestions enter the selected list. Metadata filtering + decomposition reaches **27/28** at \`k=5\`. This is an artifact of the deliberately strict slate-level compatibility metric but illustrates the tradeoff: exposing more candidates can increase irrelevant or unsafe suggestions.

**Internal engineering failure detected:** first version of the metadata filter mistakenly allowed version-scoped tools when task scope was 'any'. Regression tests and revised implementation removed that loophole. This is a concrete result of actually running the experiment.

## Pilot B — Real Pydantic API recipe contracts

Seven operations: validation, serialization to dict and JSON, schema, copy, construction and field introspection. Compare legacy method names versus v2 method names on Pydantic's v1 compatibility namespace and modern BaseModel.

| Target API | Legacy recipe | Modern recipe |
| --- | ---: | ---: |
| Pydantic v1 compatibility | 7/7 pass, 0 warnings | 0/7 pass |
| Pydantic v2 | 7/7 pass, **7 deprecation warnings** | 7/7 pass, 0 warnings |

This demonstrates **API fit and asymmetric compatibility** for this example. It does *not* demonstrate that an LLM given a Capability Pack chooses the correct recipe or generates better code. The modern-v2 recipe fails on v1; the legacy recipe still works on v2 through deprecated methods (as observed on installed Pydantic 2.13.5).

## Methods limitations / next real model experiment

- All tool prompts, descriptions and gold sets were authored by one investigator; likely optimistic overlap and potential bias.
- Only a tiny number of cases; no inferential confidence intervals or causal performance claims.
- The query splitter is hand-coded and exploits explicit conjunctions in task descriptions.
- The API task uses a v1 compatibility layer inside v2, not separate isolated environments.
- No independent coding-model attempts, task traces or tests of synthesized patches.
- No security penetration or supply-chain testing.

### What to test next **with a Vibe runtime**

1. Choose 12–20 unseen version-sensitive coding tasks and independently test their outputs on actual pinned library versions (in separate environments).
2. Run the **same pinned Vibe model** with: no external docs; raw docs; version-matched API pack; version-matched pack with tested examples/recipes. Match total token+tool budgets where possible.
3. Freeze tasks, source references, manifest versions, acceptance tests, prompts, and model configuration *before* running.
4. Add tasks requiring multiple tools, and no-tool negative controls. Compare task-resolved rates, invalid API use, number of tool calls, cost/latency and negative transfer.
5. Only declare a capability uplift after the paired experiment runs; retain failed tasks and counterexamples.

See [full pilot report](../../research/EXPERIMENT-REPORT-2026-11-05.md).
