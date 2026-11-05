# TDD-08 — External Capability Library & Software Stack Atlas

**Date:** 2026-11-05  
**Status:** research-stage architecture proposal; no capability packs in this repository are certified production tools.  
**Mission:** extend one fixed coding agent's *effective* ability by making external versioned knowledge, tested snippets, reusable scripts, complete stack patterns and known failure modes discoverable and usable on demand.

## Hypothesis

Technical competence is not just recalling API syntax. A useful agent needs (1) correct **version-specific facts**, (2) **worked implementations**, (3) **executable operations** and (4) **verification evidence**. Even when a model knows component libraries, it can miss compatibility constraints, undocumented interactions and subtle environmental preconditions. A **Capability Pack** joins these types without injecting everything into context.

Do not pretend a pack changes model parameters. A source, worked example or script must be *selected, understood and successfully applied*. The causal prediction is that *version-matched, independently verified capability packs* outperform either raw documentation retrieval alone or generic standing instructions on relevant held-out tasks.

## Research grounding: actual published findings

| ID | Primary research | Evidence and caveat |
| --- | --- | --- |
| DOC-PROMPT | https://arxiv.org/abs/2207.05987 | ICLR 2023: retrieving library docs improved code generation; CodeT5 +2.85 pp pass@1 (52% relative) on CoNaLa, other results on Bash. Task-specific, not full software agent. |
| REPOCODER | https://aclanthology.org/2023.emnlp-main.151/ | EMNLP 2023: iterative repo retrieval/generation outperformed in-file completion by over 10% in reported scenarios. |
| REPOFORMER | https://proceedings.mlr.press/v235/wu24a.html | ICML 2024: selective repo retrieval yielded up to ~70% inference speedup without hurting studied completion quality. Uses trained/selective model; do not assume a generic runtime router replicates this. |
| CODERAG | https://aclanthology.org/2025.findings-naacl.176/ | NAACL 2025: 10 retrievers × 10 LMs and heterogeneous corpora; gold docs can improve code, but real retrieval and integration often underperform. |
| GORILLA | https://proceedings.neurips.cc/paper_files/paper/2024/hash/e4c61f578ff07830f5c37378dd3ecb0d-Abstract-Conference.html | NeurIPS 2024: retrieval-aware API use and updates reduced hallucination; model is fine-tuned, so not pure fixed-model proof. |
| LIBEVO | https://research.google/pubs/libevobench-probing-temporal-knowledge-startification-in-code-generation-models/ | NeurIPS 2026: models often confuse evolving library API versions; specifying target version alone failed to help, relevant docs improved accuracy. |
| EVOLVING-API | https://arxiv.org/abs/2604.09515 | 2026: 270 real API changes from 8 Python libs; authors report executable generated examples 42.55% without comprehensive documentation and only 66.36% even with more favorable structured-documentation/model settings. Not clean single-variable causal estimates. |
| INCOMPATIBLE-API | https://doi.org/10.1145/3830085 | ACM TOSEM 2026: 10,867 versioned library completion tasks across six LMs; incompatible API usages common; detection + repair investigated. |
| SKILLSBENCH | https://www.skillsbench.ai/blogs/skillsbench-1-1 | 2026 v1.1: curated skills raised average resolution from 33.9% to 50.5% in reported 18 configurations, but task and domain specificity matter. |
| SWE-SKILLS | https://arxiv.org/abs/2603.15401 | 2026 software-focused: 39/49 tested public skills no pass-rate gain, average +1.2 pp, some version-mismatched skills harmful. Essential counter-evidence. |
| VOYAGER | https://mlanthology.org/tmlr/2024/wang2024tmlr-voyager/ | TMLR 2024: black-box GPT-4 agent accumulates an executable skill library in Minecraft without weight training; significant domain-specific learning. Not a code-agent benchmark. |
| LATM | https://proceedings.iclr.cc/paper_files/paper/2024/hash/ed91353f700d113e5d848c7e04a858b0-Abstract-Conference.html | ICLR 2024: LLMs can make reusable Python tools and amortize creation cost across use cases; tool writer and user may be same or different models. |
| TOOLSMITH | https://aclanthology.org/2026.findings-emnlp.1699/ | 2026 failure-driven reusable Python tool generation for multimodal search; evaluated partly with VLM-as-judge, not deterministic coding tests. |

## Six complementary shelves (avoid one undifferentiated corpus)

1. **API Manuals** — version-specific signatures, overloads, deprecations, behavior, error conditions, official examples, migration deltas.
2. **Function Patterns** — small tested algorithms, idiomatic code transformations, adapters with explicit pre/postconditions and negative examples.
3. **Script Workshop** — executable CLI analyzers, parsers, converters, test generators, setup/repair utilities; always with contracts, tests, permission scopes.
4. **Stack Atlas** — combinations of libraries/frameworks, lockfiles, runtime versions, container manifests, integration boundaries, minimal reproducible stacks and end-to-end smoke tests.
5. **Procedural Skills** — conditional diagnosis and workflows, task triggers, contraindications, explicit verifiers; should *reference* relevant documents and scripts rather than repeat entire manuals.
6. **Failure & Compatibility Cases** — bug signatures, migration incompatibilities, known wrong patterns, version-specific counterexamples, revoked guidance.

**Separate a source fact, a recommended method, and an executable effect.** A model may read a manual without acquiring execution permissions; a script may pass a smoke test without proving global applicability.

## Proposed layout (not yet populated)

~~~text
capabilities/
  catalog.jsonl                        # light searchable metadata, source of discovery
  api/
    <library>/<version>/
      INDEX.md                         # brief indexed guide, anchors to sources
      signatures.json                  # extracted API contracts, checked
      compatibility.yaml               # introduced/deprecated/breaks rules
      examples/                        # independently executed small calls
  functions/
    <pattern>/
      manifest.yaml                    # applicability + signature + provenance
      implementation.py                # only after review and qualification
      tests/
      counterexamples/
  scripts/
    <operation>/
      SKILL.md                         # only if procedural loading is useful
      scripts/                         # locally reviewed executables
      tests/
      fixtures/
      manifest.yaml
  stacks/
    <stack-name>/<stack-revision>/
      STACK.md                         # architecture, boundaries, operations
      manifest.yaml                    # compatibility constraints
      lockfiles/                       # frozen dependencies
      recipes/                         # version-matched implementation slices
      tests/                           # integration and migration smoke tests
      failure-cases.md                 # constraints and known bad versions
  skills/
    <task-procedure>/
      SKILL.md
      references/
      scripts/
      tests/
  failures/
    cases.jsonl
  evaluations/
    heldout-manifests/                  # no secret or answer-key inclusion
~~~

Conforms conceptually to Agent Skills optional `references/`, `scripts/`, `assets/` folders; actual support of a given agent host and executable permissions must be validated. https://agentskills.io/specification

## Capability Pack manifest — proposed project-owned format

~~~yaml
schema_version: 1
pack_id: python-fastapi-postgres-integration
kind: stack_recipe
status: staged
purpose: "Version-constrained integration of Python API, ORM and Postgres"
scope:
  languages: [python]
  target_os: [linux, windows]
  package_versions: {}   # fill ONLY after inspecting actual lockfiles
  git_revision: null
sources:
  - url: "https://fastapi.tiangolo.com/"
    revision: null
    license_review: pending
artifacts:
  guide: STACK.md
  examples: recipes/
  tests: tests/
fitness:
  applicable_when: ["known stack constraints and testable API contract"]
  not_applicable_when: ["dependency versions unknown"]
verification:
  environment_hash: null
  tests_passed: null
  independently_reviewed: false
security:
  network: disabled_by_default
  filesystem: read_only_by_default
  authorization: host_controlled
~~~

This manifest is illustrative, **not** a demonstrated working compatibility matrix or a vendor API.

## Stack Atlas design: go beyond isolated library descriptions

For each meaningful combination, store:
- **Compatibility matrix**: interpreter/runtime, exact dependency versions and constraints, OS/architecture, known ABI breaks.
- **Integration map**: modules, interface boundaries, data contracts, configuration points, interaction diagrams.
- **Minimal working project**: a tiny reproducible build from an authorized package source and pin/lock files.
- **Smoke tests**: start service, open DB safely, exercise one endpoint, verify migration/rollback.
- **Troubleshooting and counterexamples**: wrong APIs for previous versions, imports/deprecations, silent behavior changes.
- **Provenance**: exact documentation source, retrieval time, license status, source code commit.

Never treat popular StackOverflow examples or synthetic generated snippets as verified just because they compile.

## Retrieval and execution flow

~~~text
Task -> detect gap -> decide: facts / pattern / executable / full stack
     -> search only matching shelf and current version
     -> check source quality, applicability, permission, health
     -> return compact evidence packet with explicit provenance
     -> select: read; adapt example; run pre-approved script; stage new tool
     -> independent tests; record failures and scope
     -> approved candidate becomes discoverable for future tasks
~~~

The model's context receives a small **index** of capability cards, not every manual and tool schema. Keep raw source and full fixtures addressable on demand. Existing models already have a lot of general knowledge; use a pack only when it plausibly adds missing or uncertain information.

## Candidate experiments

- **E-L1 Versioned API**: no docs vs version mentioned only vs latest docs vs *exact version docs* vs version-specific tested examples. Hidden tests run against two incompatible library versions.
- **E-L2 Function Patterns**: documentation snippet vs tested function template vs generated code; control for total inference and code exposure.
- **E-L3 Script Workshop**: no script vs manual recipe vs tested script with same API scope; include timeouts, bad inputs and mismatched OS.
- **E-L4 Stack Atlas**: library docs separately vs integrated pinned stack recipe vs reference implementation with smoke tests. Hold out different repository layouts.
- **E-L5 Skill vs Pack**: long global AGENTS.md vs brief conditional SKILL.md vs SKILL.md + scripts + verified references, all budget matched.
- **E-L6 Recency/negative knowledge**: injected stale API doc vs correct migration notes vs negative counterexample; test when agent incorrectly applies old parameters.

Every design needs exact model ID/version, context/token/tool budget, corpus snapshot/hash, code snapshot, independent verifier and 3 conditions: simpler baseline, helpful intervention, deliberately harmful/unneeded context.

## Closest existing implementations to inspect, not copy blindly

- **Context7**: https://github.com/upstash/context7 — current API/library documentation and examples through MCP; practical product, not independently proved benchmark superiority.
- **Aider repository map**: https://aider.chat/docs/repomap.html — graph-ranked symbol map within token budget.
- **Google ADK Recipes**: https://github.com/google/adk-recipes — machine-readable manifest, validated recipe, instructions and runnability tests; production fitness varies by recipe.
- **CodeRAG-Bench**: https://code-rag-bench.github.io/ — heterogeneous retrieved docs and coding outcome benchmark.
- **SkillsBench**: https://www.skillsbench.ai/ — controlled with/without skills with deterministic verifiers.
- **SWE-Skills-Bench**: https://github.com/GeniusHTX/SWE-Skills-Bench — software-only countercheck.
- **Voyager**: https://github.com/MineDojo/Voyager — reusable executable skill library, black-box model.
- **Agent Skills**: https://agentskills.io/specification — packaging format, not security enforcement.

## Crucial research caution

The performance of an agent given a code snippet cannot be compared with no-snippet accuracy if the snippet secretly contains the target answer. Use unseen, independent tasks with controlled access to ground-truth code; vary source version and include misleading but realistic historical examples. **There is no scientific basis yet for combining all library effects into one percentage improvement.**

## Proposed research result

A **versioned, evidence-linked, executable Capability Pack** is a hypothesis of a better external "cognitive unit" than a raw text chunk, static skill or arbitrary reusable script. This specific combination's novelty and actual effectiveness are **unproven**, and should be tested against each simpler mechanism before being adopted as architecture.
