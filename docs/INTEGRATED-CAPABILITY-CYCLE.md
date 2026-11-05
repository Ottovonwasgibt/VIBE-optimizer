# Integrated Capability Cycle — Single-Agent System v0.2

**Date:** 2026-11-05  
**Status:** integrated research blueprint plus **executable advisory prototypes**. No claims of measured increases in Vibe model intelligence or an autonomous operational agent.

## Mission: one task-solving agent, better external cognition

Maximize **independently verified task outcomes at a specified budget** for one fixed-weight model. Coding is one application; diagnosis, functional management, research, documentation, process analysis and other knowledge work are equally valid. The workbench can supply missing facts, version-specific manuals, reusable procedures, verified scripts, tests, memory, solvers and task controls. Additional models are optional comparison instruments, not the target architecture.

## Closed-loop design

~~~text
User objective + authorized context + independent acceptance criteria
                           |
                    Observe task state
                           |
             Detect deficit and uncertainty
            (knowledge, scope, tool, test, policy)
                           |
         Inspect available capability inventory
         (qualified / visible / reachable / suitable)
                           |
      Choose next information-producing SAFE action
     (no tool, evidence, procedure, tool, test, human)
                           |
     Host authorizes execution; agent receives result
                           |
           Independent verification / evidence ledger
                           |
                 Watchdog checkpoint
        (continue, review, safe handoff, halt)
                           |
        Candidate lesson / function / script/skill
                           |
          Separate test and qualification path
                           |
       Approved reusable asset returns to catalog
~~~

**The host remains the only authority to call tools, modify files, change roles, run scripts, approve memory or transmit private material.** Metadata discovery cannot grant new permissions.

## What is currently implemented vs not

| Capability | Current artifact | What has actually been validated | Still missing |
| --- | --- | --- | --- |
| Public knowledge retrieval | [knowledge.py](../src/vibe_optimizer/knowledge.py) | SQLite FTS5 staging, approval/revocation and retrieval tests | License workflow beyond simple flags; classification and real source adapters |
| Versioned capability registry | [capability_registry.py](../src/vibe_optimizer/capability_registry.py) | Synthetic catalog suitability, qualification, permission filters | Real catalog, source discovery, operating-system and API probe fixtures |
| First-step deficit router | [task_router.py](../src/vibe_optimizer/task_router.py) | Transparent deterministic rules and negative controls | Task-state observation and calibrated value-of-information policy |
| Evidence compiler | [evidence_packets.py](../src/vibe_optimizer/evidence_packets.py) | Size, provenance, expiry, deduplication and conflicting versions | Independently checked source integrity, live private policy gateway |
| Integrated advisory loop | [capability_loop.py](../src/vibe_optimizer/capability_loop.py) | Registry, router, evidence and checkpoint wired together | Agent invocation, actual tool execution, persistent evidence state |
| Candidate skill/function/script governance | [candidate_governance.py](../src/vibe_optimizer/candidate_governance.py) | Source/digest scope, independent review receipts, revocation state | Authenticated reviewer, isolated execution, scriptifier and version migration |
| Delivery and actual utilization distinction | [capability_delivery.py](../src/vibe_optimizer/capability_delivery.py) | Expected / visible / invoked / externally relevant classifications | Actual host telemetry and observed impact on task success |
| Session watchdog | [checkpoint_watchdog.py](../src/vibe_optimizer/checkpoint_watchdog.py) + [hook](../examples/checkpoint-watchdog/vibe_post_tool_hook.py) | Synthetic replay, threshold stress tests and hook unit tests | Live session delivery, independent review acknowledgement, verified outcome gain |
| MCP public workbench bridge | [mcp_bridge.py](../src/vibe_optimizer/mcp_bridge.py) | Fake-server contract and optional MCP v2 integration CI (check latest run) | Actual installed Vibe integration and supported host permissions |
| Restricted source governance | [private_knowledge.py](../src/vibe_optimizer/private_knowledge.py) | Fictional tenant/role/purpose/egress tests | Institution-approved authentication, storage, contract and network enforcement |
| Domain pack prototype | [Higher Education](DOMAIN-DESIGNS/01-higher-education-functional-management.md) | Fictional scenarios and general public-source architecture | Domain-expert grading, real authorized docs in separate private deployment |
| Paired model experiment scorer | [paired_eval.py](../experiments/live_agent/paired_eval.py) | Strict task pairing, budget, safety and synthetic fixture metadata tests | Real pinned model runs and independently collected verifier outputs |

**Status rule:** a green unit test indicates deterministic code behavior, not a general capability improvement. A successful MCP SDK test is not an installed Vibe interaction. A qualified synthetic card is not operational permission.

## Minimal capability card (project-defined)

A card records kind, purpose, explicit trigger and contraindication, exact required versions, target environment, source and revision, license, health, qualification status and permission. Search returns only matching **qualified** cards that are visible under caller policy. Read-only inspection reports suitability without running the associated tool.

What is explicitly separate:
1. Exists in catalog.
2. Is visible to this host/session.
3. Is reachable and healthy.
4. Is authorized for the current user and action.
5. Is actually suitable for this task/version.
6. Is invoked successfully and produces relevant evidence.
7. Improves the independently verified final task outcome.

Do not collapse these into a single model confidence score.

## Knowledge, skills, functions, scripts and software stacks

- **Knowledge:** source-dated facts, exact API/manual versions, institutional workflow semantics, counterexamples. Retrieval on demand, no large blanket prompt.
- **Procedures/skills:** conditional triggers, contraindications and verification steps, small enough to load at task time; no automatic elevation of host permissions.
- **Functions:** typed input/output, test fixtures and version constraints; a function is only reusable after qualification.
- **Scripts:** capabilities proposed from successful task sequences, then independently tested and separately approved; no automatic execution of generated script.
- **Stack Atlas:** pinned combinations of software packages/services, tested integration recipes, failure cases and migration paths; no claim that one popular setup works everywhere.
- **Operational process atlas:** state transitions, responsibility, rule versions and evidence chains in non-coding domains, with strict confidentiality boundaries.

**Promotion rule:** candidate -> independent tests -> reviewed provenance/applicability -> qualified/revocable artifact. A model's own explanation cannot act as the verifier. If an artifact becomes stale, revoke or stage a new version; never silently rewrite an old approved receipt.

## Independent evidence and "do nothing" control

An agent can be better off doing no additional retrieval. Every action policy should consider:
- whether task criteria and target versions are known;
- what next observation would materially reduce uncertainty;
- what exact independent check would distinguish the hypotheses;
- tool cost, risk and permissions;
- whether existing evidence is already enough.

When the required tool is absent or forbidden, **abstain or escalate** instead of inventing an API or a temporary authorization bypass.

## Memory as verified experience, not transcript accumulation

Retain only source-scoped lessons with task signatures, accepted/rejected evidence, environment and relevant versions. Proposal metadata is separate from private text; retrieval must honor scope, version and revocation. A large raw transcript or a model-written summary is not verified memory.

## Meta-control: watch for drift and tool underuse

Track whether the model has stopped using suitable tools or is repeating the same failed approach. Event triggers can cause brief checkpoints; a longer interval is a fallback. Prefer a quiet, rate-limited supervisor; do not interrupt critical operations. A fresh-context handoff carries objective, acceptance criteria and independently verified facts, not all previous chat.

## Security boundaries

- PUBLIC and qualified metadata may be shown by the public workbench.
- RESTRICTED institution/vendor sources stay in a separately authorized deployment; never mirror them to public GitHub.
- OS-local CLI does not imply local model inference; check remote model egress.
- A tool-search result is not an authorization token. Scripts, financial/enrollment changes, role updates and message replay require independent host approval.
- Skills, retrieved documents and tool output are lower-trust data, not instructions with authority.
- Candidate code is never downloaded or executed based solely on its existence in a catalog.

## Next engineering gates, in order

**G0 — Deterministic integration (underway):** demonstrate public synthetic registry -> route -> evidence -> checkpoint -> advisory result; preserve negative controls and revision filtering; complete repeatable test suite.

**G1 — Actual public MCP host compatibility:** check exact installed Vibe version, SDK v2 server launch, the three public advisory tools, tool visibility and permission behavior. Do not load private docs or executable tools.

**G2 — Outcome observatory:** capture sanitized host-delivered tools, invocations, verified actions and actual checkpoint outcomes. Never depend on model self-reported success. Ensure reviewer/source separation.

**G3 — Controlled one-model experiments:** same pinned Vibe model, same unseen tasks and budgets, randomize baseline vs versioned evidence packs, relevant skills, tool discovery and checkpoint strategies. Include no-tool/no-skill negative controls.

**G4 — Script/skill compiler:** turn one independently successful procedure into a candidate with inputs, fixtures, tests, permission and revision constraints. Evaluate transfer to unseen tasks and amortized cost.

**G5 — Full external packs:** exercise versioned API and stack integration on separate isolated environments, with real package constraints and independently executed tests; ensure licensed/private source boundaries.

**G6 — Verified memory and adaptive budgets:** only after observed repeated needs and measured costs. Benchmark retrieval usefulness, negative transfer and candidate revocation.

**G7 — Optional restricted deployment:** only with institution-specific information security, license and model-processing approvals. Separate private storage and trusted identity—not a new public connector.

## R&D scoring

First metric: **independently verified safe task success**, stratified by task type and task horizon.

Secondaries: time/token/tool-call costs; first useful observation; unsupported claims; wrong-version suggestions; inappropriate tool use; false-positive skills; time to recover from errors; checkpoint interruption overhead; safety issues; human intervention required.

A proposed improvement is retained only if it beats (i) unmodified model and (ii) same-model **budget-matched extra reasoning** or simple standard tooling. Negative findings remain recorded. See [paired evaluator](../experiments/live_agent/paired_eval.py), [evaluation contract](EVALUATION.md) and [hypothesis registry](../research/HYPOTHESIS-REGISTRY.md).

## Current immediate constraints

- The project is not an autonomous full-stack agent yet.
- SDK-level MCP and manual skills do not prove actual host delivery or a solved task.
- No Vibe model version and real baseline runs have yet been measured here.
- Full original external Deep Research documents were not included in this repo.
- Unrestricted self-modification, remote retrieval of private sources and real admin/financial operations remain out of scope.

The desired end state is **a single agent that knows how to recognize missing competence, acquire the right authorized external capability, test its own output, learn verified reusable methods and periodically correct its course**.
