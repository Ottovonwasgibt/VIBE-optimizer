# TDD-06 — Deficit-aware Cognitive Router and Evidence Compiler

**Status:** conceptual R&D design, not implemented. All input/output contracts below are project-owned, not native Vibe APIs.

## Mechanism under test

**Hypothesis:** A coding agent should first diagnose which *capability is missing* (knowledge, localization, execution, verification, specification), then select the appropriate form of evidence or computation, rather than always retrieving the most similar chunks.

This is a candidate **new combination** of existing ideas, not an established novel scientific discovery. Source backdrop:
- https://arxiv.org/abs/2607.24882 (selective agentic retrieval)
- https://aclanthology.org/2026.findings-emnlp.433/ (dependency-aware graph retrieval)
- https://www.sri.inf.ethz.ch/publications/gloaguen2026agentsmd (extra context can hurt)

## Deficit ontology and action mapping

| Deficit | Diagnostic clue | First useful observation | Wrong default |
| --- | --- | --- | --- |
| Knowledge | API/version concept not known | Versioned official documentation | Broad search without version |
| Localization | Unknown function, caller or failure site | Commit-aware code symbols and tests | Web search |
| Execution | Environment/build tool unavailable | Reproduce environment and inspect dependencies | Edit code blindly |
| Verification | No reliable behavioral oracle | Design a test/property/checker | Declare success from self-review |
| Specification | Behavior ambiguous or conflicting | Clarify constraints and state assumptions | Implement arbitrary reading |

The categories may overlap. A model may suggest a deficit; it must back the diagnosis with observable signals. Keep missing information as unknown, not false.

## Project-owned input contract

~~~json
{
  "task_id": "T001",
  "repo": {"revision": "GIT_SHA", "dirty": false},
  "signals": {
    "error_trace_present": true,
    "api_version_unknown": false,
    "symbol_location_missing": true,
    "failure_reproduces": false,
    "criteria_clear": true
  },
  "budget": {"max_context_tokens": 4000, "max_tool_calls": 6}
}
~~~

## Proposed router output

~~~json
{
  "diagnoses": [
    {"kind": "localization", "reason": "Unknown failing callsite"},
    {"kind": "execution", "reason": "Failure not reproduced"}
  ],
  "next_action": {"tool": "reproduce_failure", "args": {"task_id": "T001"}},
  "fallback": {"kind": "repo_map", "condition": "Reproduction still inconclusive"},
  "external_retrieval": "skip_for_now",
  "confidence_calibration": "not_measured"
}
~~~

## Deterministic first control algorithm

~~~python
def next_action(s: dict) -> str:
    """Baseline for an experiment, not a validated routing strategy."""
    if s.get("criteria_clear") is False:
        return "clarify"
    if s.get("error_trace_present") and s.get("failure_reproduces") is False:
        return "reproduce_failure"
    if s.get("symbol_location_missing"):
        return "repo_map"
    if s.get("api_version_unknown"):
        return "versioned_docs_search"
    if s.get("tests_available") is False:
        return "design_verifier"
    return "inspect_repo"
~~~

## Evidence compiler

Compile only the evidence needed by the selected action, with source locators and contradictory information.

~~~yaml
packet_id: E-T001-01
task_revision: GIT_SHA
purpose: locate_shutdown_caller
evidence:
  - type: repository_symbol
    source: src/worker.py
    revision: GIT_SHA
    locator: "lines 30-64"
    sha256: PLACEHOLDER
  - type: verified_procedure
    name: diagnose_async_shutdown
    version: 2
    applicability: "python >=3.11"
    evidence_ids: ["RUN-001"]
counterevidence:
  - "Increasing timeout failed in a different dependency version"
unknowns:
  - "Shutdown failure not yet reproduced"
max_context_tokens: 4000
~~~

No source content should become system instructions; evidence is lower-trust data. If no evidence is relevant, return an explicit abstention. Never fabricate calibrated confidence numbers.

## Value-of-information policy (theory only)

The router's long-run goal is to pick the **next observation** with highest estimated increase in independently verified success per cost/risk, rather than maximizing retrieval similarity.

Candidate actions: read exact source, retrieve docs, inspect symbol graph, run test, ask human, call solver, abstain. Start with transparent rules; only fit statistical scoring after real action–outcome data. Compare against an equally expensive repeated-reasoning baseline.

## Discriminating experiments

- **E01 mixed tasks:** unmodified agent vs rules-based deficit router vs same-model extra inference.
- **E02 versioned API:** lexical top-k vs version-matched retrieval vs graph-augmented evidence packet.
- **E03 negative control:** trivial rename/syntax tasks; see whether the router correctly avoids external context.
- **E04 weak verifier:** ambiguous behavior with no test; see whether the agent first constructs a verifier rather than selecting a plausible-looking fix.

Outcomes: resolved rate, first-useful-tool accuracy, retrieval precision, wasted tokens, latency, regressions and security events. Preserve alternative hypotheses in every experiment.

## Possible R&D tools

| Proposed tool | Contract | Status |
| --- | --- | --- |
| \`diagnose_capability_gap\` | TaskSnapshot -> Diagnoses | Speculative |
| \`compile_evidence_packet\` | Task + Diagnoses + Budget -> EvidencePacket | Speculative |
| \`check_provenance\` | Packet -> ValidationReport | Speculative |
| \`record_action_outcome\` | Action + TestReport -> EpisodeRecord | Speculative |
| \`propose_skill_revision\` | Verified traces -> CandidateSkill | Speculative |

Implement independently testable pure functions before exposing them via MCP. Re-evaluate the mechanism if the diagnostic layer causes more errors or greater costs than it saves.
