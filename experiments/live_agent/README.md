# First real model trial — controlled local launcher

**Status:** ready-to-run **dry-run-first** tooling, not a completed model trial. No Vibe, Claude or Astra inference was run by GitHub Actions or ChatGPT.

## Main idea

First compare **the same exact model** on the exact same public/synthetic tasks in two conditions: baseline (no supplied reference) and reference (short version- or domain-specific documentation). This identifies the causal value of having the right external facts before testing the full workbench, scripts and watchdog.

Do not compare a Claude result with a Vibe result and call the difference an augmentation effect. Cross-model comparisons are a separate question requiring task/host/price controls. See [Model Portability](../../docs/MODEL-PORTABILITY.md).

## Preview without model calls

From a local clone of the repository:

~~~powershell
python experiments/live_agent/run_local.py --suite experiments/live_agent/public_synthetic_suite.json
~~~

By default this **only writes a local dry-run manifest and eight prompt files** under ignored `runtime/first-live-trial/`. No model is contacted. The generated prompts are strictly public or fictional.

## Explicitly start Vibe when ready

First check `vibe --version` and inspect the current model ID/alias in the installed CLI. Then manually choose:

~~~powershell
python experiments/live_agent/run_local.py --suite experiments/live_agent/public_synthetic_suite.json --adapter vibe --model YOUR_EXACT_VIBE_MODEL --task python_api_version --execute
~~~

This invokes two separate **billable** Vibe CLI sessions (baseline/reference) using documented `--prompt-file`, `--max-turns`, `--max-tokens`, `--time-limit` and `--agent ask` flags. It deliberately does **not** use `--auto-approve`, `--yolo`, or a project worktree. Sessions work from isolated `runtime/` directories and are forbidden to execute commands or modify files by the benchmark prompt. However, the runner is **not a security sandbox**; the host and its actual tool permissions remain authoritative.

## Optional Claude Code CLI comparison

~~~powershell
python experiments/live_agent/run_local.py --suite experiments/live_agent/public_synthetic_suite.json --adapter claude --model YOUR_EXACT_CLAUDE_MODEL --task python_api_version --execute
~~~

The Claude adapter uses its documented print mode with `--permission-mode plan`. It does **not** enforce the same token cap as Vibe; record actual cost, model revision and latency before cross-provider comparisons. This command is optional and should only be executed after inspecting the installed CLI.

## What about GPT-6 Astra?

OpenAI's `gpt-6-astra` supports function calling, tools, skills, tool search and MCP. It can consume the same **public capability cards and evidence packets**, via an appropriate API/Codex host adapter. **This repository does not yet have an Astra runner**, and no installed OpenAI model access or cost entitlement is assumed. Do not mistake a ChatGPT UI 'ultra' mode for a portable CLI model ID.

Official references: [GPT-6 Astra](https://developers.openai.com/api/docs/models/gpt-6-astra), [OpenAI MCP](https://developers.openai.com/api/docs/guides/tools-connectors-mcp), [Vibe programmatic CLI](https://docs.mistral.ai/vibe/code/cli/work-with-cli), [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code/cli-usage).

## Evidence and scoring

- Generated `manifest.json` records execution or dry-run **but cannot mark a task solved**.
- Raw model stdout/stderr and exported Vibe sessions remain **local under ignored runtime/**; review them before sharing or uploading anywhere.
- Independent hidden answer keys, source requirements and policy checks must be assessed outside the model prompt. The public suite is a feasibility pilot, not a blinded statistically powered benchmark.
- For a formal study, convert verified outcome rows to the strict [paired evaluator](paired_eval.py) format, including per-condition real cost, time, tool calls and safety labels. Never map a zero exit code to `solved=true`.
- Equal resource caps do not imply equal actual inference effort or dollars; inspect exports and provider billing.

## Research next steps

1. Run one dry-run and inspect prompts and host flags.
2. Pin actual Vibe model and confirm the public MCP catalog is visible and safe.
3. Run baseline/reference on a small task and independently score correctness.
4. Expand to controlled multi-tool, skills, checkpoint and no-tool cases.
5. Replicate within the same Claude and Astra model configurations (when independently authorized and implemented).

**No private Osiris or Studielink documentation, student data, production actions or secrets belong in this public experiment.**
