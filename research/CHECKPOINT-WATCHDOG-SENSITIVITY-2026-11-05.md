# Checkpoint Watchdog — Sensitivity, Alert Noise and Telemetry Contracts

**Date:** 2026-11-05  
**Stage:** second *executed* infrastructure experiment. No Vibe/model trajectories or human task outcomes measured.

## The question

Can external reorientation checkpoints notice long-running work-pattern drift without repeatedly interrupting productive work? The previous 10-case replay found a simple hybrid triggered many redundant alerts, motivating a gated alert policy.

This follow-up:
1. Compares event-only and interval+event thresholds on timing/measurement-perturbed synthetic traces.
2. Separates *alert detection* from actual correction of model behavior.
3. Introduces a strict whitelist format for later session telemetry and an offline auditor.
4. Makes the host-side safety-stop flag persistent until externally released.

## How to reproduce

~~~powershell
python experiments/watchdog/replay.py --output experiments/watchdog/replay-results.json
python experiments/watchdog/sensitivity.py --repeats 20 --output experiments/watchdog/sensitivity-results.json
python experiments/watchdog/observatory.py experiments/watchdog/synthetic_trace.json
python -m unittest discover -s tests -p 'test_watchdog_*.py' -v
~~~

GitHub Actions [watchdog workflow](https://github.com/Ottovonwasgibt/VIBE-optimizer/actions/workflows/watchdog-replay.yml) performs replay, sensitivity, strict trace audit and tests; provides downloadable *synthetic* JSON artifacts.

## Dataset: 200 perturbed sessions per split

Ten **hand-authored** base-case families:
- 4 labeled negative / no known problem (short productive, long productive, suitable generic tool, slow legitimate investigation);
- 5 labeled non-safety problems (repeated failures, specialist-tool neglect, stalled verification, context pressure, critical-operation-safe-boundary);
- 1 labeled safety problem (an externally asserted unsafe operation).

Each base family is randomly perturbed 20 times with a fixed seed, yielding **80 negative and 120 positive synthetic traces** per split, 200 total. The development and holdout splits use different random seeds but **the same underlying ten templates**. This is NOT a truly independent holdout population.

Perturbations cover pacing (0.7×–1.4×), small counter noise, occasional missing tool-fit evidence, noisy failure counters and context-utilization estimates. Hidden anomaly labels do not enter policy decision inputs.

## Observed holdout-split outcomes

| Policy | Detected synthetic problem traces /120 | Alerts in healthy traces /80 | All alerts /200 | Mean detection lag, steps |
| --- | ---: | ---: | ---: | ---: |
| Event signals only | **100** | **0** | **150** | 3.87 |
| Frequent: 10 minutes /12 tools + signals | **119** | **221** | **541** | 2.12 |
| Balanced: 20 minutes /25 tools + signals | **120** | **92** | **279** | 3.56 |
| Relaxed: 30 minutes /40 tools + signals | **100** | **33** | **183** | 3.87 |
| Balanced + stricter anomaly thresholds | **120** | **92** | **255** | 4.78 |

Development split gave similar qualitative patterns:
- event only 100/120, 0 notifications in healthy traces;
- frequent 115/120, 217 healthy notifications;
- balanced 120/120, 99 healthy notifications;
- relaxed 100/120, 31 healthy notifications;
- stricter 120/120, 99 healthy notifications.

**Interpretation:**
- Event-only policy avoids interruptions in explicitly healthy fixture families; it misses at least one problem family where the synthetic event signals never cross threshold.
- A moderate interval catches additional situations but warns during long **healthy** sessions, too. These are not objectively proven "false alarms" from a real task; we count them as potential interruption costs.
- Frequent intervals overproduce alerts in this fixture. A stricter anomaly threshold reduces total alerts somewhat at the cost of delayed detection.
- The 120/120 score **must not** be described as perfect anomaly diagnosis: a generic time-based warning occurring after an event counts as detecting the *session*, not correctly inferring its cause.
- **There is no basis for declaring a winning threshold** or predicting Vibe task-resolution gains.

## Important simulation mismatch

Synthetic observations continue **unchanged** after a warning. The replay's interval counters are cumulative; the gated policy rate-limits duplicate reminders, but does not emulate a real agent changing behavior, a human acting on a reminder, or confirmed review resetting observation counters. The optional Vibe hook separately resets its reminder rate-limit counters, but cannot verify that a review happened.

Consequently the large alert counts are useful to identify pathological policy settings, **not forecasts of notifications during actual Vibe sessions**.

## Security/control correction

The [watchdog gate](../src/vibe_optimizer/watchdog_gate.py) now retains a **safety_hold** once an externally signaled unsafe operation is observed. Later normal observations or acknowledgment of a regular handoff must not clear this state. An explicit trusted host authorization is required to release it.

**It is a data-model guarantee only**: the offline module cannot stop a real agent or enforce permissions. The eventual agent host must enforce the hold before further sensitive operations.

## New bridge toward real measurements

A metadata-only JSON trace protocol and validation script are now available:

- [observatory.py](../experiments/watchdog/observatory.py)
- [fictional JSON trace](../experiments/watchdog/synthetic_trace.json)
- [tests](../tests/test_watchdog_observatory.py)

Only these approved fields are accepted per event: monotonic step/time, generic tool class (not tool name/path), observed success/failure/unknown, externally assessed verified progress, independent suitable-tool signal, optional context usage, critical-operation and safety flags. Unknown extra fields such as prompts, tool outputs and file paths are rejected. The auditor produces only alert reasons and step numbers.

**Privacy reminder:** a whitelist is not a replacement for host authentication, proper institutional permission, reviewed identifier conventions or protected logging. Do not collect content from private Osiris/Studielink sessions in this public experiment.

### Why this improves the next experiment

We can obtain **observable traces** for real agent runs without archiving task prompts, code, documents or student data. Separately retained private answer keys and independent outcome checks can evaluate whether a checkpoint actually improves task completion.

## Next real Vibe experiment

Run at least two pre-registered task types with the **same pinned model, tools and comparable budgets**:
- long software-repository investigation requiring sustained attention and tool switching;
- lengthy non-coding, public/synthetic administrative process analysis requiring evidence tracing.

Randomize a no-checkpoint baseline vs event-only vs balanced-gated in isolated, reproducible environments. Record only sanitized events and external task outcomes; checkpoint messages and delivered tool inventory must be logged separately and reviewed. Include short productive negative controls.

Success metric is **independently verified solved tasks with acceptable safety**, not the number of reminders or how many model phrases mention a tool.

## Engineering next steps

1. Integrate read-only, trusted session event counters from a pinned Vibe version.
2. Verify native post-tool hook delivery semantics in a real session.
3. Distinguish a reminder being emitted, actually delivered, acknowledged and followed by a verified action.
4. Replace context/progress estimates with trustworthy host observations or leave fields unknown.
5. Test notification cooldown with evidence of actual task progression, not merely repeated thresholds.
6. Compare adaptive/event-triggered vs fixed-interval interventions under matched total model effort.

This report establishes a reproducible **watchdog policy stress test and telemetry scaffold**, not improved agent competence.
