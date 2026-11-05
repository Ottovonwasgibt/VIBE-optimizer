# Capability Workbench — runnable research scaffold

**Status (2026-11-05):** functional Python modules, unit tests, fictional catalog, synthetic integration smoke and an optional **real MCP Python SDK v2** server. The model has **not** been benchmarked with these capabilities in a Vibe session.

## Simple offline demo (no dependencies)

Run from the repository root:

~~~powershell
python examples/capability-workbench/demo.py
python experiments/integration/smoke.py
python experiments/live_agent/paired_eval.py experiments/live_agent/synthetic_results.json
python -m unittest discover -s tests -v
~~~

What you should observe:
- Pydantic v2 task selects a v2-matched manual rather than v1;
- synthetic Studielink/Osiris process task selects a public fictional domain card;
- proposed scripts and restricted manual metadata do not appear in the public search;
- evidence retains source/revision, and the checkpoint policy can recommend a review;
- a controlled synthetic line-normalizer passes three test fixtures;
- the A/B scorer reports **fictional** matched-task outcomes, not observed Vibe gains.

## Optional MCP SDK v2 integration (public metadata only)

Official source: https://py.sdk.modelcontextprotocol.io/ and https://docs.mistral.ai/vibe/code/cli/mcp-servers

1. In a disposable Python 3.11+ environment, install the optional SDK:
   ~~~powershell
   python -m pip install "mcp>=2,<3"
   ~~~
   For a pinned deployment, freeze the exact resolved version before use.
2. Test the three read-only tools against a real in-memory MCP v2 client:
   ~~~powershell
   python experiments/mcp/verify_sdk.py
   ~~~
3. Inspect [public_mcp_server.py](public_mcp_server.py) and [mcp_bridge.py](../../src/vibe_optimizer/mcp_bridge.py). The launcher hosts only:
   - workbench_search
   - workbench_inspect
   - workbench_plan
4. To start the stdio server manually, run:
   ~~~powershell
   python examples/capability-workbench/public_mcp_server.py
   ~~~
   It will wait for an MCP client; no interactive prompt is expected. Terminate it yourself.
5. **Only if you explicitly choose to test this in Vibe:** inspect the active Vibe version and permissions, then use a manually configured stdio MCP server with an **absolute** path to the script. Example syntax from official Vibe docs:
   ~~~text
   vibe mcp add optimizer_public --transport stdio --command python --arg ABSOLUTE_PATH_TO_PUBLIC_MCP_SERVER_PY
   ~~~
   This is an installation action in the user's Vibe configuration; **it has not been executed by this repository or ChatGPT**. Check /mcp status and the actual tool list before a task. Removing this entry is a separate user action.

**Do not** put this optional server in a project plugin's mcp.json until the real launch path and host behavior are verified. The current public catalog contains no credentials or real manuals.

## On-demand skills (project plugin)

This repo already has a project-scoped Agent Plugins 1.0 manifest under .vibe/plugins/cognitive-stack. The new procedural skills are:
- /cognitive:capability-check — inspect a missing capability or repeated tool mismatch;
- /cognitive:checkpoint-review — brief reorientation after repeated errors, no blanket ritual;
- /cognitive:implement-verify — existing code-change procedure.

Vibe only loads project plugins from a trusted working directory. The plugin does **not** automatically enable MCP here. Verify actual visibility using /plugins and, if needed, /reload-plugins. Skill text does not change permissions.

## Technical controls and caveats

- The public MCP bridge is advice-only. It cannot invoke shell, write files, install tools, connect to Osiris/Studielink or query private documents.
- Version hints passed by a model are **not independently verified**. Use host-observed versions for any real execution decision.
- The catalog is fictional; its qualification flags represent test fixtures, not certified external products.
- No raw URL fetch, remote package download, subprocess execution or direct credential access is performed by these tools.
- Private source access belongs to a separate approved server with authentication and egress policy (see docs/PRIVATE-KNOWLEDGE-BOUNDARY.md).
- The mock admin reviewer in synthetic tests is **not** a security mechanism. Production qualification/revocation requires an independently authenticated process.

## What to measure next

Run actual tasks on the same pinned Vibe model with and without the public workbench, keeping budgets and task verifiers constant. Track whether the MCP tools were really visible, called, appropriate and linked to a correct result. Do not infer outcome improvement from successful metadata lookups or from a green test suite.

See [Integrated Capability Cycle](../../docs/INTEGRATED-CAPABILITY-CYCLE.md).
