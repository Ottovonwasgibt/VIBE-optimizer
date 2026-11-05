# Frontier Evidence Dossier — 2026-11-05

**Status:** research source mapping, not a systematic review or independent replication. Publicly accessible pages inspected; paper findings are **authors' reported results**, not results from VIBE-optimizer. Where source code, licenses, effect sizes or conditions remain unverified, mark them explicitly.

## 2026 frontier: empirical findings and design implications

### S-01 — Agentic Context Engineering (ACE)

- **Primary:** https://arxiv.org/abs/2510.04618
- **Claim in paper:** generator–reflector–curator improves evolving procedural playbooks via incremental updates and natural execution feedback, with reported gains in its selected domains.
- **Mechanism:** experience is consolidated as a structured, revisable playbook rather than compressed into a brittle summary.
- **VIBE proposal:** candidate memory/skill evolution pipeline with evidence citations and independent verification gates.
- **Blind spot:** reported task distribution is not our coding benchmark; cannot transfer numerical gains without reproduction.
- **Counter-hypothesis:** improvements are from additional test-time tokens or preexisting answers in memory.

### S-02 — SkillGen (May 2026)

- **Primary:** https://www.microsoft.com/en-us/research/publication/skillgen-verified-inference-time-agent-skill-synthesis/
- **Claim in paper:** induces readable skills from both success and failure trajectories; checks skill effect through matched task-level interventions, including rescues and regressions; reported cross-model transfer.
- **Mechanism:** contrastive execution patterns become a localized, reusable procedure.
- **VIBE proposal:** "skill candidate laboratory" with a separate \`SKILL.md\` template, version scope, negative cases and preregistered paired A/B tests.
- **Blind spot:** skill extraction may favor benchmark-specific patterns; positive evidence may not generalize to new repositories or unseen languages.

### S-03 — Memory–Skill Co-Evolution (EMNLP 2026)

- **Primary:** https://aclanthology.org/2026.findings-emnlp.1637/
- **Claim in paper:** evidence-grounded, training-free memory-to-skill governance with applicability boundaries and reliability estimates.
- **Mechanism:** episodic traces and reusable procedures are represented at different levels and promoted under policies.
- **VIBE proposal:** typed memory and explicit skill promotion graph.
- **Blind spot:** need to independently validate whether reported reliability estimates calibrate well under distribution shift.

### S-04 — Unified Context Evolution (EMNLP 2026)

- **Primary:** https://aclanthology.org/2026.emnlp-main.2188/
- **Claim in paper:** typed Evolvable Context Units (Memory, Strategy, Workflow, Skill) are retrieved, evaluated through outcomes, and pruned.
- **Mechanism:** untyped accumulation is replaced by typed, outcome-aware adaptive context.
- **VIBE proposal:** typed knowledge ecology and memory shelf life; avoid a flat indiscriminate vector store.
- **Blind spot:** inference cost and reproducibility under constrained local toolchains.

### S-05 — CrossCoder (EMNLP 2026)

- **Primary:** https://aclanthology.org/2026.findings-emnlp.433/
- **Claim in paper:** unified repo + external library knowledge graph retrieves multi-hop context and tests dependency version compatibility; authors report improvements including up to 6.3% pass@1 in specified settings.
- **Mechanism:** relationships across local and external APIs constrain context; static docs alone lack version dependencies.
- **VIBE proposal:** lockfile-aware repository graph, selective neighbor expansion and version-compatible citations.
- **Blind spot:** graph construction and maintenance cost; compare against simple symbol map and BM25, not only naïve RAG.

### S-06 — Agent Retrieval Bench (2026)

- **Primary:** https://arxiv.org/abs/2607.24882
- **Project:** https://agent-retrieval-bench.github.io/
- **Claim in paper:** different retrievers win on different coding signals; correct evidence selection and **no-gold/abstention** are hard; more retrieval is not always better.
- **Mechanism:** useful context depends on workflow need, not just semantic query similarity.
- **VIBE proposal:** task-conditional context compiler with selective abstention, exact Git snapshot and budget-aware retrieval.
- **Blind spot:** task-set dependence; measure actual patch outcomes alongside recall and MRR.

### S-07 — Evaluating AGENTS.md (ICLR workshop 2026)

- **Primary:** https://www.sri.inf.ethz.ch/publications/gloaguen2026agentsmd
- **Claim in paper:** the evaluated repository-level context files had no aggregate success improvement while increasing inference cost by over 20%.
- **Mechanism:** verbose generalized instructions may induce unnecessary exploration and operational overhead.
- **VIBE proposal:** minimal standing AGENTS.md plus selective procedure loading; A/B-test this choice rather than assume it helps.
- **Blind spot:** study conditions may differ from high-quality hand-written project rules or specialized safety instructions.

### S-08 — Co-Scientist (Nature 2026)

- **Primary:** https://www.nature.com/articles/s41586-026-10644-y
- **Claim in paper:** multiple agent roles create, critique and refine research hypotheses, including a tournament-style evolution process and test-time scaling.
- **Mechanism:** independent hypothesis search plus structured criticism may discover promising candidates.
- **VIBE proposal:** model-independent research council and explicit hypothesis records.
- **Blind spot:** persuasive judging, cost scaling and scientific novelty claims all require human and independent test verification.

### S-09 — Robin (Nature 2026)

- **Primary:** https://www.nature.com/articles/s41586-026-10652-y
- **Claim in paper:** multi-agent scientific exploration with literature, hypothesis design, external experiments and data analysis in a lab-in-the-loop cycle.
- **Mechanism:** experimental outcome supplies information unavailable to prompt-only generation.
- **VIBE proposal:** tools and verifiers as *active sources of new evidence*, not just ways to execute suggestions.
- **Blind spot:** biology lab workflows do not transfer automatically to engineering; focus on programmable validators.

### S-10 — HiddenBench (ICML 2026)

- **Primary:** https://proceedings.mlr.press/v306/li26ej.html
- **Claim in paper:** groups can fail badly to integrate distributed/private evidence, leading to premature consensus even with strong individual models.
- **Mechanism:** latent information asymmetry is not recognized; critical minority knowledge goes unmentioned.
- **VIBE proposal:** explicit evidence inventory, role-specific knowledge gaps and minority signal retention.
- **Blind spot:** what works in synthetic distributed-information tasks may not extrapolate to coding-agent architectural design.

### S-11 — Multi-agent debate: competing evidence (2026)

- **Positive mechanism case:** https://aclanthology.org/2026.findings-acl.1694/ reports that diversity-aware initialization and calibrated confidence can help in some QA settings.
- **Challenging preprint:** https://arxiv.org/abs/2609.35875 reports heterogeneous debate did not beat matched sampling controls across its evaluated small-model tasks and incurred extra cost.
- **VIBE proposal:** compare blind multi-model proposals against best-of-N sampling at *matched budgets*, and assess with external executable outcomes.
- **Takeaway:** "more models" is not an outcome metric; evidence from different settings can conflict without any being universally wrong.

### S-12 — Scientific discovery workflow bottleneck (Patterns 2026)

- **Primary:** https://pmc.ncbi.nlm.nih.gov/articles/PMC13674306/
- **Claim in review:** systems show progress in retrieval and hypothesis generation, while execution and experimental feedback remain central bottlenecks.
- **VIBE proposal:** prioritize experiment compilation, test harnesses, and theory revision over infinite ideation loops.
- **Blind spot:** review is cross-domain, not specific to our tools.

### S-13 — EvoAgentBench (EMNLP 2026)

- **Primary:** https://aclanthology.org/2026.findings-emnlp.2344/
- **Claim in paper:** distinguishes procedural ability transfer from isolated task solving and proposes domain-spanning evaluation.
- **VIBE proposal:** evaluate skills on distinct tasks that reuse the **procedure** but not the same code patch.
- **Blind spot:** benchmark validity, leakage and ability-graph construction need local review.

## Proposed synthesis: where a new research contribution might live

| Mechanism | Existing closest prior art | Candidate extension | How to determine if novel |
| --- | --- | --- | --- |
| Deficit-conditioned retrieval | Agent Retrieval Bench, task-conditioned retrieval | Classify *what kind of capability is missing*, not just what text is relevant | Search for adaptive deficit routers and compare interventions |
| Evidence-backed skill evolution | ACE, SkillGen, MSCE, UCE | Separate success skill, contraindication memory and versioned scope; falsify transfer | Compare documented variants and run negative-transfer tasks |
| Cross-repo context | CrossCoder | Build exact dependency version + test coverage + failure-cause links | Search code graph provenance and version-aware verification work |
| Meta-research across models | Co-Scientist, Robin, debate research | Independent blind proposal, causal test design, falsification-focused selection | Run equal-budget best-of-N and blind objective grading |
| Context restoration | ACE and evolving context work | Reconstruct minimal *disconfirming* evidence and original sources after compaction | Test long-horizon tasks where forgotten constraints matter |

**These ideas are *candidate novel combinations*, not patentability/priority assertions or proven scientific novelties.** Novelty must be established by a broader systematic search and primary code inspection.

## What to investigate next

1. Find and read code implementations for ACE, SkillGen, MSCE, UCE, CrossCoder, Agent Retrieval Bench and research agents. Pin exact commit/release and examine evaluation scripts, data splits and licenses.
2. Inventory skill/library/memory failure modes and trace which are mitigated by *verification* versus prompt instructions alone.
3. Build a versioned claim-to-citation registry and a falsifiability matrix.
4. Draft 3–4 minimal experimental interventions with neutral controls.
5. Choose one high-information pilot with at least one negative-control task category and a fixed evaluation budget.
6. Report negative results and cases of improvement at the task level rather than only aggregates.
