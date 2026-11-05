# TDD-02 — Cognitive Router, Skills, MCP and verifiers

**Status:** proposed, interfaces are **project-owned** JSON/Python sketches, not native Vibe APIs.

## Control responsibilities

- **Vibe host:** agent/model loop and enforcement of tool permissions.
- **Router:** select source scopes, context budget, procedure and verifier policy.
- **MCP server:** expose limited data-oriented tools; do not own security decisions that belong to the host.
- **Skills:** supply procedures/checklists through `SKILL.md`, not unbounded autonomy or privileged execution.
- **Verifier:** inspect an execution report and test result; never declare correctness solely from model opinion.

## Task contract

```json
{
  "intent": "debug",
  "repository": "example/project",
  "git_commit": "FULL_GIT_SHA",
  "language": "python",
  "risk": "medium",
  "acceptance": ["focused_test_passes", "no_unrelated_diff"],
  "retrieval_budget_tokens": 4500
}
```

## Router output contract

```json
{
  "skill": "implement-verify",
  "retrieval": {
    "sources": ["repository", "official_docs", "verified_memory"],
    "limit": 8,
    "max_tokens": 4500
  },
  "verification": {
    "required": true,
    "run_focused_tests": true,
    "max_materially_different_retries": 3
  }
}
```

These schemas need actual JSON Schema definitions and unit tests before integration.

## Initial deterministic routing rules

```python
def choose_policy(task):
    # Illustrative pseudocode, not executable module.
    if task.risk == "high":
        return "review-first"
    if task.intent in {"debug", "refactor", "implement"}:
        return "implement-verify"
    if task.intent == "investigate":
        return "repo-intelligence"
    return "task-triage"
```

Evidence ranking order: current target repository/test behavior > matching-version official docs > reviewed memory > verified third-party sources. Use score heuristics only after documenting failure cases. Fall back gracefully when indexing is unavailable.

## Vibe plugin: verified format

`.vibe/plugins/cognitive-stack/plugin.json`

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "cognitive-stack",
  "version": "0.1.0",
  "description": "Procedural skills and reviewed technical knowledge for Vibe Code.",
  "extensions": {
    "ai.mistral.vibe": {
      "schemaVersion": 1,
      "displayName": "Cognitive Stack",
      "toolNamespace": "cognitive"
    }
  }
}
```

Vibe documents namespaced `/cognitive:skill-name` command exposure for plugin skills. Plugin support is **experimental**; reload via `/reload-plugins`.

### MCP registration (EXAMPLE ONLY — do not enable before server exists)

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
  "mcpServers": {
    "cognitive-brain": {
      "type": "stdio",
      "command": "./bin/brain-server",
      "env": { "BRAIN_DB": "${PLUGIN_DATA}/brain.sqlite" }
    }
  }
}
```

Mistral plugin `mcp.json`: top-level `$schema` must exactly match; only additional top-level field is `mcpServers`; `command` must be a bare executable or start `./`. `PLUGIN_DATA` expands in env/args, **not command**. Windows-specific packaging and dependencies are not solved by this snippet.

## MCP Python v2 server sketch

```python
from mcp.server import MCPServer

mcp = MCPServer("Cognitive Brain")

@mcp.tool()
def brain_search(query: str, limit: int = 5) -> list[dict]:
    """Search approved technical knowledge; return source provenance."""
    raise NotImplementedError("Wire read-only SQLite backend")
```

The official SDK v2 uses `MCPServer` and Python 3.11+. No `mcp.json` is active in this bootstrap because the server executable has not yet been implemented and tested.

## MCP interface policy

Proposed minimal tools:
- `brain_search(query, limit, scope)`: verified sources only; bounded results and input.
- `brain_get(chunk_id)`: full chunk plus URL/version/content hash, with hard size limit.
- `repo_map(repository_commit, query)`: current commit symbols and paths; no shell commands.
- `memory_propose(problem, evidence, lesson)`: write **proposed only**, separate permissions required.

Avoid `execute_shell`, `fetch_any_url`, `approve_memory` in the initial read-only knowledge server.

## Executable procedure: implement → verify

1. Capture acceptance criteria and git status.
2. Collect bounded code evidence; load skill only if task matches.
3. Draft a minimal plan; require additional approval for higher-risk operations.
4. Apply a small patch under host permissions.
5. Run specified focused tests/typechecks, capture exact exit code and logs.
6. Diagnose whether failure is code, environment, flaky test or bad requirements.
7. Retry only when the hypothesis changes; cap at three material attempts.
8. Report diff, passes/failures, evidence and unresolved risk.
9. Propose (not auto-approve) an episodic memory.

## Risks

- Prompt injection via retrieved files or pasted terminal output.
- Model treating rank as certainty.
- Stale commit maps.
- A skill gaining implied authority despite host permissions.
- Third-party MCP package supply-chain compromise.
- Model-based router overshadowing a simple deterministic baseline.

## References

- https://docs.mistral.ai/vibe/code/cli/plugins
- https://docs.mistral.ai/vibe/code/cli/skills
- https://docs.mistral.ai/vibe/code/cli/configuration-reference
- https://py.sdk.modelcontextprotocol.io/
- https://arxiv.org/abs/2210.03629
- https://arxiv.org/abs/2303.11366
