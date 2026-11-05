# Empirical Evidence and Replication Shortlist (2026-11-05)

**Purpose:** distill published *observed* outcomes relevant to a single fixed-weight coding agent and its external workbench. **All values below are authors' reports or vendor internal measurements. None are VIBE-optimizer reruns.**

## Directly relevant trials

| Study | Evaluation and reported result | Evidence strength / portability |
| --- | --- | --- |
| Anthropic Advanced Tool Use (2025) | Internal MCP tool-search evaluation: Opus 4 **49% to 74%**, Opus 4.5 **79.5% to 88.1%**; large-tool context token saving ~85% | Vendor internal, not coding task resolution; reproduce on Vibe |
| SWE-agent (NeurIPS 2024) | Purpose-designed agent-computer interface; benchmark results **12.5% SWE-bench**, **87.7% HumanEvalFix** | Peer-reviewed; absolute scores on different tests, not a before/after delta |
| ACE (ICLR 2026) | Evolving procedure/memory context: reported avg **+10.6% agent tasks**, **+8.6% finance** | Paper with [open-source code](https://github.com/ace-agent/ace); not directly coding tasks |
| Apple Plan or Retrieve First? (EMNLP 2026) | **46,984 APIs**, 50 categories; retrieve-first wins on single-tool tasks, abstract-plan-first on multi-tool; extra plan roughly doubles inference overhead on retrieval step | Peer-reviewed, highly relevant for adaptive workbench routing |
| ToolSmith (Findings EMNLP 2026) | Failure-driven reusable Python tool creation; **36/39** model × benchmark cells improve. Qwen3-VL-32B out-of-domain **31.27 to 34.25**, GPT-5 **39.80 to 42.20** | Peer-reviewed; multimodal searching, **VLM-as-a-judge** rather than deterministic coding grader. [Paper](https://aclanthology.org/2026.findings-emnlp.1699/) / [project](https://threesr.github.io/toolsmith/) |
| SMITH (NeurIPS 2026) | Co-trained creator/user; frozen 350M consumer held-out accuracy **11.6 to 42.9** when using SMITH-written tools | Strong evidence tools can transfer; **tool-writer uses RL training**, unlike fixed-weight goal. [Code](https://github.com/appier-research/smith) |
| CodeGrep (ACL 2026) | Fixed downstream coding agent: solve **25.8% to 27.0%**, **19% fewer tokens**, **15% fewer rounds** on resolved tasks | Peer-reviewed; retrieval helper trained with RL; SWE-bench Verified has contamination/scorer concerns |
| Agent Retrieval Bench (2026) | **427 samples**, 25 repos; no universal best retriever, logged trajectories missed all gold files **27–35%** of cases | Preprint and [benchmark code](https://github.com/eyuansu62/agent-retrieval-bench); measures context acquisition, not patch correctness |
| AGENTS.md (ICLR 2026 workshop) | Context files had **no overall task success improvement**, >**20%** cost increase | Peer-reviewed workshop negative finding; [code](https://github.com/eth-sri/agentbench) |
| CrossCoder (Findings EMNLP 2026) | Dependency-version-aware cross-repo graph retrieval improves pass@1 by **up to 6.3% in reported settings** | Peer-reviewed; benchmark-specific and context-dependent |

## Primary sources

- https://www.anthropic.com/research/advanced-tool-use
- https://papers.nips.cc/paper/2024/hash/5a7c947568c1b1328ccc5230172e1e7c-Abstract-Conference.html
- https://arxiv.org/abs/2510.04618
- https://github.com/ace-agent/ace
- https://aclanthology.org/2026.emnlp-industry.19/
- https://aclanthology.org/2026.findings-emnlp.1699/
- https://threesr.github.io/toolsmith/
- https://tool-use-smith.github.io/
- https://aclanthology.org/2026.realm-1.80/
- https://arxiv.org/abs/2607.24882
- https://www.sri.inf.ethz.ch/publications/gloaguen2026agentsmd
- https://aclanthology.org/2026.findings-emnlp.433/
- https://epoch.ai/benchmarks/swe-bench-verified/review

## Reproduction strategy for VIBE-optimizer

**First (small, no model training):** reproduce a fixed-model *tool registry* trial with 30–50 newly authored tasks and identical token/tool budgets: static schemas vs lazy tool search vs complexity-adaptive tool discovery. Split single-tool, multi-tool, and no-tool cases. Track correct tool selection, independent task resolution, latency, and tool false-positive rate.

**Second:** port ToolSmith's failure-mining → reuse-or-grow → test → quarantine sequence to a coding-task fixture, with generated tools run in a reviewable isolated environment. Compare fixed tools, proposed tools and validated promoted tools; hold out new repositories/tasks.

**Third:** compare static standing instructions vs ACE-style reviewed context/skill updates, including negative transfer and costs. A proposed skill should be **tested with and without itself on the same task instances**, not only evaluated on its successes.

**Interpretation:** Report observed tasks, model version, control budget, full tool registry snapshot, source/repo commits, counterexamples, and whether success uses deterministic test outcomes or model judges. Never add percentage gains from different studies.

## Benchmark warning

Epoch AI's **2026-09-03 review** labels SWE-bench Verified *Flawed*, citing contamination and scoring defects. Public leaderboard scores should not serve as sole proof that an augmented agent became more capable. Prioritize new, held-out project tasks, executable grading and replicated same-model ablations.

**Conclusion:** The workbench/capability-maximization research direction has substantial prior evidence; claims of an integrated 'Super Saiyan' uplift remain **untested**.
