# Source Registry — primary sources and evidence status

**Last checked:** 2026-11-05. **Scope:** public specifications and reproducible research; verify again at implementation time. The reports from separately initiated Deep Research sessions have not been imported.

## Evidence labels

- **[SPEC]** Current public vendor/protocol documentation; verify against installed version.
- **[CODE]** Public source code or reference implementation; check commit/release before reuse.
- **[PAPER]** Published research; experimental claim is not automatically reproducible for our stack.
- **[DESIGN]** Our architectural hypothesis; not a vendor-supported feature until verified.
- **[PENDING]** Claim not yet verified against environment or linked source.

## Official integration specifications

| ID | Type | Source | Intended use | Review notes |
| --- | --- | --- | --- | --- |
| VIBE-PLUGIN | SPEC | https://docs.mistral.ai/vibe/code/cli/plugins | Agent Plugins 1.0 `plugin.json`; `mcp.json`; Vibe extension; plugin data and skill namespaces | Support described as *experimental*; only plugin root `plugin.json` required |
| VIBE-SKILL | SPEC | https://docs.mistral.ai/vibe/code/cli/skills | `skills/<name>/SKILL.md`, frontmatter, slash commands, loading | `allowed-tools` not an enforced permission mechanism |
| VIBE-CONFIG | SPEC | https://docs.mistral.ai/vibe/code/cli/configuration-reference | `config.toml` schema, agent/tool security | Confirm by running installed `vibe config schema` |
| VIBE-MCP | SPEC | https://docs.mistral.ai/vibe/code/cli/mcp-servers | Server configuration and supported tool transports | Use stdio initially; verify Windows executable resolution |
| VIBE-CODE | CODE | https://github.com/mistralai/mistral-vibe | Observe agent/CLI architecture and versioned behavior | Record exact inspected Git SHA before making claims about internals |
| AGENT-PLUGIN | SPEC | https://agent-plugins.org/ | Agent Plugins 1.0 schema & format | Schema for `plugin.json` and `mcp.json` must match exactly |
| AGENT-SKILLS | SPEC | https://agentskills.io/specification | Portable procedural skill format | Progressive discovery/activation; inspect individual skill provenance |
| MCP-SPEC | SPEC | https://modelcontextprotocol.io/specification | Tool, resource, prompt, transport semantics | Tool output is lower-trust content; implement narrow schemas |
| MCP-PY | SPEC/CODE | https://py.sdk.modelcontextprotocol.io/ | MCP Python SDK v2 `from mcp.server import MCPServer` | SDK v2 docs describe Python 3.11+; pin exact tested dependency |
| MCP-PY-SOURCE | CODE | https://github.com/modelcontextprotocol/python-sdk | Working server and test patterns | Do not mix v1 `FastMCP` examples with v2 without migration |
| SQLITE-FTS5 | SPEC | https://www.sqlite.org/fts5.html | BM25, FTS query syntax, snippets, tokenizers | BM25 is rank, **not probability**; sanitize FTS syntax |
| TREE-SITTER | SPEC/CODE | https://tree-sitter.github.io/tree-sitter/ | Incremental syntax trees and symbol extraction | Per-language parsers require versioning |
| AIDER-REPOMAP | CODE/DOC | https://aider.chat/docs/repomap.html | Repository-map design, symbol relevance, token budgets | Use ideas; do not copy implementation without license review |

## Research mapped to engineering questions

| ID | Type | Primary source | Hypothesis to test |
| --- | --- | --- | --- |
| RAG-2020 | PAPER | https://arxiv.org/abs/2005.11401 | Retrieval may improve knowledge-grounded output if evidence selection works |
| REACT-2022 | PAPER | https://arxiv.org/abs/2210.03629 | Interleaving reasoning and tool interaction can aid multistep tasks |
| REFLEXION-2023 | PAPER | https://arxiv.org/abs/2303.11366 | Verbal feedback and past episode memories may improve repeated attempts |
| SELF-REFINE-2023 | PAPER | https://arxiv.org/abs/2303.17651 | Iterated feedback/refinement may improve candidate outputs under some tasks |
| GRAPH-RAG-2024 | PAPER | https://arxiv.org/abs/2404.16130 | Relationship structure can help certain global/connected queries beyond plain chunks |
| SWE-BENCH-2023 | PAPER | https://arxiv.org/abs/2310.06770 | Repository-level tasks need executable test-based evaluation |
| SWE-BENCH-DATA | CODE | https://github.com/SWE-bench/SWE-bench | Benchmark harness reference; contamination and policy review required |

## Assertions to audit before any implementation

1. **Mistral Vibe plugin namespace and commands:** check supported version and manifest. Current docs describe `extensions["ai.mistral.vibe"].toolNamespace` and `/plugins` / `/reload-plugins`; do not infer behavior across versions.
2. **MCP server launch:** in plugin `mcp.json`, `command` must be a bare executable or start `./`; variables expand in `args`, `env`, `cwd`, not `command` (per Vibe docs).
3. **Runtime data:** `PLUGIN_DATA` belongs to plugin runtime; never store local indexes in Git.
4. **Autonomy/approval:** a skill's `allowed-tools` field is descriptive rather than enforcement in Vibe.
5. **SDK compatibility:** MCP Python SDK v2 uses `MCPServer`; confirm dependency in lockfile and test execution, including Windows.
6. **Model parity:** an external library can expand effective problem-solving resources but does not copy private model weights or training.
7. **Benchmark performance:** no measured improvement has been established for this repository.

## Resource intake contract

Each ingested source needs: `source_id`, `uri`, `title`, `publisher`, `retrieved_at`, `version_or_revision`, `sha256`, `license_review`, `trust_tier`, `status`, `section_locator` and `embedding_model` if applicable.

Statuses: `staged -> approved -> revoked`. Only `approved` enters live retrieval. Do not mirror restricted content without rights. Cite original sources rather than treating the cache as authoritative.

## Pending research report reconciliation

On receiving either Deep Research report:
1. Inventory every claim and citation.
2. Match to the sources above or add new primary sources.
3. Mark `SUPPORTED`, `PARTIAL`, `UNVERIFIED`, `CONTRADICTED`.
4. Convert only supported claims into architecture decisions or implementation issues.
5. Keep a dated changelog of corrections.

## Additional current 2026 primary research — research-first programme

The following source pages were inspected on 2026-11-05. **Full evaluation code, paper methods and licenses still require an independent audit**. For mechanisms, caveats and research implications see `research/FRONTIER-EVIDENCE-DOSSIER.md`.

| ID | Primary source | Relevance |
| --- | --- | --- |
| SKILLGEN-2026 | https://www.microsoft.com/en-us/research/publication/skillgen-verified-inference-time-agent-skill-synthesis/ | Skill induction from positive/negative traces and intervention-based evaluation |
| MSCE-2026 | https://aclanthology.org/2026.findings-emnlp.1637/ | Evidence-governed memory-to-skill transformations |
| UCE-2026 | https://aclanthology.org/2026.emnlp-main.2188/ | Typed memory/strategy/workflow/skill evolution |
| CROSSCODER-2026 | https://aclanthology.org/2026.findings-emnlp.433/ | Cross-repository dependency-version-aware retrieval |
| ARB-2026 | https://arxiv.org/abs/2607.24882 | Selective repository retrieval and no-evidence cases |
| AGENTS-NEGATIVE-2026 | https://www.sri.inf.ethz.ch/publications/gloaguen2026agentsmd | Context-file null-result and cost overhead in evaluated tasks |
| CO-SCIENTIST-2026 | https://www.nature.com/articles/s41586-026-10644-y | Multi-agent hypothesis evolution with critique and testing |
| ROBIN-2026 | https://www.nature.com/articles/s41586-026-10652-y | Experiment-driven multi-agent scientific discovery |
| HIDDENBENCH-2026 | https://proceedings.mlr.press/v306/li26ej.html | Distributed evidence integration failure modes |
| DEBATE-ACL-2026 | https://aclanthology.org/2026.findings-acl.1694/ | Confidence and diversity as conditional debate mechanisms |
| DEBATE-COUNTER-2026 | https://arxiv.org/abs/2609.35875 | Debate may underperform budget-matched sampling |
| EVOAGENTBENCH-2026 | https://aclanthology.org/2026.findings-emnlp.2344/ | Procedural ability transfer benchmark |

Research contribution statuses: `known-prior-art`, `adaptation`, `candidate-novel-combination`, `unverified-novelty`, `supported-novelty`. The last category requires a broad prior-art audit, not merely independent LLM agreement.
