# TDD-05 — Multi-model hypothesis laboratory: conceptual and technical blueprint

**Status:** technical proposal, interfaces are project-defined, not Mistral/OpenAI/Anthropic native contracts. **No live multi-provider runner exists yet.** Updated 2026-11-05.

## A. Separate scientific orchestration from the coding-agent harness

The Vibe plugin is *one implementation target and one research instrument*, not the entire scientific director. Avoid making Vibe the sole gatekeeper of evidence or judges.

    Study manifest  ---> Research Controller (offline state machine)
                                  |
                        +---------+---------+
                        |                   |
                 Model adapters      Evidence registry
                        |                   |
             Independent proposals   Sources + version
                        |                   |
                      Critique / novelty check
                                  |
                            Experiment plan
                                  |
                     Sandboxed implementation
                                  |
                       Independent evaluator
                                  |
                        Evidence + verdict
                                  |
                         Hypothesis registry

**Trust separation:**
- The controller owns experiment IDs, immutable records, budget, provider selection and task assignments.
- The coding model may propose code, schemas and methods, but cannot score its own hypothesis.
- Review models may supply criticisms, not promote source trust or determine test truth.
- A deterministic evaluator owns acceptance outcomes when executable.
- A human approves resource use, privileged commands and claims of scientific novelty.

## B. Minimal research-data contracts

### Study file (concept, not provider API)

~~~json
{
  "study_id": "X-H09-001",
  "hypothesis_id": "H-09",
  "status": "proposed",
  "questions": ["Does diagnosis of bottleneck help coding agent routing?"],
  "source_snapshot": "sources-2026-11-05",
  "budget": {"usd_max": 10, "tokens_max": 250000, "wallclock_minutes_max": 90},
  "model_assignments": [
    {"role": "theorist", "adapter": "manual", "model": "MODEL_A"},
    {"role": "skeptic", "adapter": "manual", "model": "MODEL_B"},
    {"role": "builder", "adapter": "local-vibe", "model": "PINNED_VIBE_MODEL"}
  ],
  "success_metric": "resolved_rate",
  "counterfactual_control": "same-model-equal-budget"
}
~~~

Store outcomes in separate append-only JSONL files with \`study_id\` and \`artifact_sha256\` fields. Never overwrite historical proposals after critique.

### Typed artifacts

\`EvidenceCard\`:
- source ID, exact URL, publication date, retrieved date, version/commit and rights status;
- one paraphrased claim supported by a short locator;
- caveat and source reliability category.

\`TheoryCard\`:
- constructs, causal arrows, assumptions, conditional predictions, strongest rival theory;
- links to registered studies and contradiction log.

\`HypothesisCard\`:
- independent variable, expected mechanism and affected task strata;
- baseline, interventions, predicted sign, falsification criterion;
- smallest testable prototype.

\`DesignCard\`:
- interface JSON Schema, boundary diagram, required tests, security model;
- reversible fallback and comparative cost.

\`ExperimentRun\`:
- task/repo hash, source corpus hash, model/version, role and prompt hash;
- tool trace pointer, explicit test commands and outputs, wall time/cost/tokens;
- resolved and regression status from independent checker.

## C. Provider-neutral adapter (future code sketch)

~~~python
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class ResearchRequest:
    study_id: str
    role: str
    evidence_bundle: str
    instructions: str
    max_output_tokens: int

@dataclass(frozen=True)
class ResearchResponse:
    provider: str
    model_id: str
    content: str
    input_tokens: int | None
    output_tokens: int | None
    raw_trace_path: str | None

class ResearchModel(Protocol):
    def generate(self, request: ResearchRequest) -> ResearchResponse:
        ...

# Implement adapters only for endpoints the user has connected and
# explicitly authorized; validate the provider's current API and usage policy.
# An initial "manual" adapter can import model-generated JSON from disk.
~~~

No assumption that Vibe exposes a stable server API or that every proprietary frontier model supports the same features. Model outputs should be converted into **one internal typed format** by a schema validator and errors logged.

## D. Initial human-in-the-loop protocol requiring no API integrations

1. Pick an ID and create \`research/studies/<id>/manifest.json\` locally.
2. Generate identical frozen evidence packs for two models (prompt hash + source URLs).
3. Submit proposal prompts independently via authorized UI/CLI interactions.
4. Import each candidate as \`proposals/model-a.json\`, \`proposals/model-b.json\` after schema validation.
5. Remove model identity before passing candidate to an independent reviewer, where practical.
6. Obtain one adversarial critique per proposal; import as distinct artifacts.
7. Freeze a discriminating test design *before* implementing the favored candidate.
8. Have the coding agent implement on disposable branches/worktrees with host approvals.
9. Score with deterministic executable tests or a human-blinded rubric.
10. Update hypothesis as \`supported\`, \`mixed\`, \`unsupported\`, or \`unresolved\`, with links to raw artifacts.

## E. Prompt recipes (not system-prompt impersonation)

**Theory creator — input fields:** study question, known primary evidence, source limitations, fixed model/tool budget.

**Required output keys:**
\`mechanism\`, \`assumptions\`, \`predictions\`, \`counter_theories\`, \`falsifier\`, \`minimal_experiment\`, \`novelty_search_terms\`, \`citations\`.

**Independent skeptic — input fields:** anonymized proposal and original evidence, but not preferred candidate or experimental results.

**Required output keys:**
\`strongest_counterexample\`, \`alternative_mechanism\`, \`unjustified_leaps\`, \`missing_prior_art\`, \`information_needed\`, \`test_to_discriminate\`.

**Architecture builder — input fields:** frozen experiment design, project constraints, relevant source specs.

**Required output keys:**
\`module_boundaries\`, \`interface_schema\`, \`minimal_patch_plan\`, \`test_plan\`, \`security_gates\`, \`rollback\`, \`uncertainties\`.

**Adjudicator — input fields:** independent experimental results and preregistered metric (preferably blinded model identity).

**Required output keys:**
\`observed_metric\`, \`uncertainty\`, \`confounds\`, \`claim_status\`, \`required_replication\`.

## F. Selection protocols and anti-consensus measures

Choose among candidates using reproducibility and *expected discriminating power*, rather than elo-style persuasiveness. When two proposals disagree, **preserve the conflict** and design a task that makes their predictions diverge.

Controls:
- match total tokens/time/cost against single-model repeated sampling;
- blind identity and preferred hypothesis where possible;
- include negative controls and benchmarks without gold retrieval;
- record each original first answer before debate or critique;
- forbid the selector from reading hidden tests;
- compare changes across different model families but avoid asserting independence;
- report near misses, negative transfer, and hypotheses rejected.

### A cost-aware candidate selection heuristic (proposal, not validated)

~~~python
def rank_candidate(candidate: dict) -> tuple:
    # Transparent triage, NOT a scientific truth function.
    return (
        int(candidate["has_falsifier"]),
        int(candidate["test_is_executable"]),
        int(candidate["novelty_check_started"]),
        -float(candidate["estimated_cost"]),
    )
~~~

This ranks candidates for *research convenience*, not likelihood of correctness. Replace only with a calibrated policy after collecting data.

## G. Research artifact graph

A relational schema or triples may represent:

    (Source) --supports/contradicts--> (Claim)
    (Claim) --motivates--> (Hypothesis)
    (Hypothesis) --predicts--> (Outcome)
    (Experiment) --tests--> (Hypothesis)
    (Run) --implements--> (Intervention)
    (Run) --observes--> (Outcome)
    (Outcome) --updates--> (Theory)
    (Design) --operationalizes--> (Hypothesis)

**Source of truth:** immutable artifact records and explicit reviewer events. A vector embedding is an *index*, not the database of record.

## H. Proposed tooling backlog

| Tool/script | Interface | Input | Output | Purpose | Priority |
| --- | --- | --- | --- | --- | --- |
| \`source-scout\` | local script / optional connected research tool | search questions | staged evidence cards | Prior art audit | P0 |
| \`hypothesis-lint\` | Python CLI | JSON card | errors and missing falsifier | Reject vague claims | P0 |
| \`prompt-freeze\` | CLI | prompts, sources, models | hash-stamped manifest | Reproducibility | P0 |
| \`research-import\` | CLI | model artifact JSON | validated typed record | Manual multi-model round | P0 |
| \`experiment-maker\` | CLI | hypothesis card | preregistered YAML | Specify discriminating test | P1 |
| \`run-control\` | local orchestrator | experiment + tasks | attempt traces | Budget-controlled execution | P1 |
| \`code-evidence\` | read-only MCP | git snapshot + symbol | source locations | Repo observations | P1 |
| \`evidence-compiler\` | read-only MCP | task + budget | cited evidence packet | Task-conditional context | P2 |
| \`skill-mutator\` | offline candidate generator | verified traces | staged SKILL.md candidate | Procedure evolution | P2 |
| \`memory-curator\` | gated administrative service | evidence and test report | verified/rejected event | Controlled memory learning | P2 |
| \`theory-diff\` | audit script | theory versions | changed predictions / contradictions | Avoid moving goalposts | P2 |

## I. Non-functional requirements

- Must run in read-only / dry-run mode before any side effects.
- No credentials in task prompts or Git.
- External model access only through user-approved connections and data scopes.
- Store private raw traces locally; publish only redacted result summaries.
- Cap model calls, tool calls, wall time and cost at the controller level.
- Optional model adapters cannot disable security gates.
- No automated scientific claim promotion without independent evaluation.

## First discriminatory pilot

Research H-09 (capability-deficit triage):
- 40–60 new issue-style tasks with hand-labeled deficit categories and hidden acceptance tests;
- baseline: direct agent, plus equal-budget repeat;
- intervention: rule-based deficit classifier before first tool call;
- experimental intervention: model-suggested deficit plus independent evidence check;
- record correct tool choice, retrieval/no-retrieval choice, first useful action, patch result, cost;
- identify cases where classification helped vs introduced a false frame;
- stop without conclusion if sample too small to separate conditions meaningfully.

**A research conclusion must be supported by actual study records.** The pilot design is not a claim that TECA or the classifier works.
