# Model portability — Astra, Claude and Mistral Vibe

**Date:** 2026-11-05  
**Status:** engineering design. A real MCP SDK v2 client has exercised the three read-only public workbench tools; no Astra, Claude or Vibe model has yet been A/B benchmarked with the integrated system.

## Core claim and limit

VIBE-optimizer is a **host-agnostic external capability layer**. It should work with any single-agent host that can provide a task contract, load relevant reference information and optionally expose the workbench through MCP or native function calls. It does not modify or train model parameters. Its gains depend on task, model, tool host, data permissions, retrieval relevance and budget.

### What is transferable?

| Mechanism | Portability | Caveat |
| --- | --- | --- |
| Versioned reference packs | High: any text-capable model can receive authorized excerpts | Need host-side source classification and model egress policies; no blanket context injection |
| Independent validators / scripts | High through *host* tool adapters or MCP | Script may be OS/environment-dependent; model must not self-authorize execution |
| Tool metadata search | High via MCP / function-call wrapper | Native tool search in Astra or Claude may already be better; don't duplicate blindly |
| Skills and conditional procedures | Medium–high: adapt packaging and trigger format | Native skill discovery and activation differ by product |
| Checkpoint/watchdog | Policy portable, **event binding host-specific** | Vibe post-tool hook != Claude hook != OpenAI/Codex integration |
| Verified reusable memory | Data/policy contract portable | Storage, permissions, retrieval and caching are host-owned |
| A/B benchmark grader | High (independent of model) | Equal *limits* do not mean equal price/time/tokens or actual reasoning effort |

Official interfaces:
- GPT-6 Astra supports tools, MCP, skills, function calling and tool search: https://developers.openai.com/api/docs/models/gpt-6-astra
- OpenAI MCP server and local Secure MCP Tunnel documentation: https://developers.openai.com/api/docs/guides/tools-connectors-mcp
- Claude tool-search and programmatic tool use: https://www.anthropic.com/research/advanced-tool-use
- Claude Code MCP: https://docs.anthropic.com/en/docs/mcp
- Mistral Vibe programmatic CLI (flags, exports, limits): https://docs.mistral.ai/vibe/code/cli/work-with-cli
- Claude Code headless CLI: https://docs.anthropic.com/en/docs/claude-code/cli-usage

**Name clarification:** the official OpenAI API model identifier in the reference is `gpt-6-astra`. A product UI selection like **Ultra/Ultrafast or maximum reasoning effort** should be documented separately as a setting or tier; do not assume it is a different publicly addressable model ID.

## Why stronger models could benefit (or not)

1. **Knowledge:** a newer model may know many APIs, but cannot reconstruct a private manual, an exact newly released API delta or unpublished institution procedures without authorized evidence. External versioned sources remain valuable.
2. **Precision:** validated templates and code execution may reduce unverified assumptions for *any* model.
3. **Efficiency:** targeted retrieval can save context compared to preloading hundreds of tool schemas. Reusable scripts can replace repeated conversational tool calls. But there are setup, tool-call and maintenance costs.
4. **Model complementarity:** a strong model may make **better use of advanced tools**, though its unaugmented baseline may be high and the absolute uplift smaller. Neither relationship is guaranteed or proven for this project.
5. **Native duplication:** OpenAI and Anthropic already provide built-in search, retrieval and tool capabilities. VIBE's external layer should first **inspect and reuse** them before adding a second bespoke tool.

Thus do not forecast a fixed percentage uplift for Astra/Claude from Vibe-only, synthetic or provider-internal experiments.

## Two-axis evaluation (do not mix claims)

**Within-model uplift** (scientifically primary):
- same exact model/version and host;
- baseline vs reference pack vs validated script vs targeted search vs checkpoints;
- fixed task and resource caps, log actual spend;
- verified safe success and regressions.

**Across-model efficiency** (secondary):
- run same tasks, oracle and external capability pack through a host-specific adapter for Vibe, Claude and Astra;
- show cost, latency, quality and their uncertainty separately;
- don't pretend a 1:1 call count or 1:1 token represents equal money or compute across different models;
- include native tools only where comparable, and explicitly document non-parity.

A valuable outcome could be **a cheaper model + strong external workbench achieving a quality threshold at lower cost**, or **a frontier model + workbench solving an otherwise unachievable corner case**. Both must be measured rather than assumed.

## Adapter contract

Each single-model provider/host adapter should supply:

```text
prepare(task, variant, authorized_sources)
run(prompt, sandbox, model_id, safe_limits)
observe(host_visible_tools, tool_invocations, resource_counters)
collect_output_and_artifacts()
grade_with_independent_oracle()
```

Controls:
- no unapproved auto-approval of shell or write tools;
- no confidential document export;
- task prompts and hidden verifier answers separated;
- fixed environment, versions and tool inventory;
- make clear whether requested tool permissions were actually granted;
- record provider/model and *host client* version;
- baseline and augmented prompts must not leak solutions from answer keys.

## Minimum useful next experiment

Use a small, safe public/synthetic task set (versioned API/documentation, multi-tool diagnosis and one noncoding process case). Execute the *same single model* at least once with no external source and once with relevant source, then repeat each pair. A third placebo or irrelevant-source condition helps test unnecessary retrieval. Start with Mistral Vibe because the repo already has an SDK v2 workbench adapter; then adapt Claude Code; then Astra via a verified supported API/host.

**Current code:** [paired outcome evaluator](../experiments/live_agent/paired_eval.py), [public MCP adapter](../src/vibe_optimizer/mcp_bridge.py) and [integrated synthetic smoke](../experiments/integration/smoke.py). **No live model outcomes yet.**
