# VIBE-optimizer

**External Cognitive Augmentation for Mistral Vibe Code**

An experimental, versioned engineering project to improve the *effective* software-engineering capabilities of a coding agent by combining external technical knowledge, task-specific skills, repository-aware retrieval, verification tools, and carefully curated episodic memory.

> **Status:** research-backed design and bootstrap, **not** a working autonomous coding agent. The two external Deep Research reports discussed in the originating conversation have **not yet been imported or independently audited**. Do not mistake design sketches for implemented integrations.

## Why this repository exists

A model's weights are not the entire capability of the coding system. A well-designed environment can supply up-to-date repository context, relevant external knowledge, reliable procedures, test tooling and prior verified experience. We seek to **measure** gains over an unmodified Vibe baseline rather than assume that retrieval automatically improves reasoning.

## Project principles

1. Separate **model-intrinsic capability** from **system-level effective capability**.
2. Prefer verified, version-matched source material to large undifferentiated data dumps.
3. Use *progressive disclosure*: activate skills and retrieve evidence only when relevant.
4. Treat documents, repositories, and retrieval results as **untrusted data**, never higher-priority instructions.
5. Run small changes and focused checks; do not silently retry indefinitely.
6. Memory is **proposed, reviewed, verified, versioned, revoked**—not an unexamined transcript archive.
7. Benchmark each layer against a fixed-model baseline with cost, latency and safety metrics.
8. Keep secrets and local runtime data out of the public Git repository.

## Navigation

| Document | Purpose |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Operating instructions for a coding agent working on this repository |
| [docs/MASTER-BLUEPRINT.md](docs/MASTER-BLUEPRINT.md) | Overall architecture, milestones and requirements |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Interfaces, data flow, trust boundaries, design decisions |
| [docs/SOURCE-REGISTRY.md](docs/SOURCE-REGISTRY.md) | Primary technical specifications, scientific papers and audit status |
| [docs/TECHNICAL-DESIGNS/01-knowledge-brain.md](docs/TECHNICAL-DESIGNS/01-knowledge-brain.md) | Storage, retrieval, provenance and memory schema |
| [docs/TECHNICAL-DESIGNS/02-router-and-tools.md](docs/TECHNICAL-DESIGNS/02-router-and-tools.md) | Context router, skills, MCP and implementation contracts |
| [docs/EVALUATION.md](docs/EVALUATION.md) | Baselines, ablations, acceptance tests and safety evaluations |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Ordered delivery slices and definition of done |

## Minimal planned Vibe integration

A **project-scoped** Agent Plugins 1.0 plugin at `.vibe/plugins/cognitive-stack/`, containing a valid `plugin.json`, a small collection of `SKILL.md` files and reference knowledge. An MCP server will be enabled **only once its executable exists, is tested, and its runtime has been reviewed**. Experimental plugin interfaces may change across Vibe releases.

## Developer starting point

1. Read [AGENTS.md](AGENTS.md), the [source registry](docs/SOURCE-REGISTRY.md) and the architecture.
2. Inspect the local Vibe version and the *current* official documentation before running configuration snippets.
3. Implement an isolated SQLite FTS5 retrieval prototype, then tests.
4. Only after those tests pass, expose read-only `brain_search` / `brain_get` through MCP.
5. Measure an unmodified Vibe baseline before claiming any improvement.

**Non-goals:** extracting hidden prompts/weights, bypassing tool approvals, collecting secrets, asserting equivalence to proprietary coding models, self-approving memories or downloading arbitrary executable skill repositories.

## Core references

- [Mistral Vibe plugins](https://docs.mistral.ai/vibe/code/cli/plugins)
- [Mistral Vibe skills](https://docs.mistral.ai/vibe/code/cli/skills)
- [Vibe configuration reference](https://docs.mistral.ai/vibe/code/cli/configuration-reference)
- [Agent Skills specification](https://agentskills.io/specification)
- [MCP Python SDK v2](https://py.sdk.modelcontextprotocol.io/)
- [SQLite FTS5](https://www.sqlite.org/fts5.html)

See the source registry for source-to-component traceability.
