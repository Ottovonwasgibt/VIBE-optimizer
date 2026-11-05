# Capability Maximization Beyond Coding — a Domain-Agnostic Workbench

**Date:** 2026-11-05  
**Status:** architectural mission correction, not evidence of higher task-performance.

## Core mission

VIBE-optimizer is **not only a coding-agent optimizer**. Its objective is to extend the effective competence of **one general task-solving agent** through curated evidence, operational procedures, software tools, simulations, verifiers and reviewed experience. Programming is one experimental domain, not the sole product.

We begin with Mistral Vibe as a practical agent runtime, but must not assume that every valuable task involves writing code or that every source can be accessed programmatically.

**First additional proving ground:** functional management of higher-education information systems, including **Osiris, Studielink**, and the surrounding Dutch institutional and public-sector information chain.

## What changes when we move beyond coding?

A code editor's success test (a passing unit test) is insufficient for many operational tasks. A functional-management assistant must often:

1. Diagnose inconsistencies across systems from partial and sometimes contradictory observations.
2. Trace business processes, message chains, identities, statuses, and timing.
3. Apply the *correct version and scope* of vendor documentation, institution policy, security procedures, and applicable regulations.
4. Understand who owns an action and whether it is permitted at each step.
5. Produce understandable operational artifacts: incident analysis, change impact, test plans, SQL/report specifications, ticket notes, runbooks, stakeholder communication.
6. Stop or escalate when necessary evidence or authority is missing.

**Do not treat a plausible explanation as a confirmed incident diagnosis.** Distinguish observed system evidence from hypotheses, policy and proposed interventions.

## Generalized Cognitive Workbench

~~~text
Task + user role + authorized environment
                 |
          Situation model
     (process, systems, facts, risks)
                 |
           Capability gap
                 |
  Domain-aware workbench discovery
  +-------------------------------+
  | Verified knowledge pack       |
  | Process/state-machine manual  |
  | API & schema contract         |
  | Data-quality and report tools |
  | Diagnostic queries / parsers  |
  | Approved procedures/checklists|
  | Simulation or test harness    |
  +-------------------------------+
                 |
         Evidence acquisition
                 |
    Explanation / decision proposal
                 |
      Independent cross-check
                 |
    Human confirmation or approval
                 |
    Audit trace and verified lesson
~~~

The same agent can use this architecture for higher education, finance, publishing, creative software, production management and other domains. Domain-specific packs supply vocabulary and checks; the workbench core stays reusable.

## Knowledge types — separate rather than blending into a single search index

| Knowledge type | Example in functional management | Required metadata |
| --- | --- | --- |
| **Domain concepts** | application, enrollment request, student registration, financial status | source, exact meaning, scope |
| **Process models** | expected handoffs and status transitions | owner, versions, exceptions |
| **Interface contracts** | supported integration or message formats | vendor release, schema, rights |
| **Configuration recipes** | how to configure a role, template or event route | environment, prerequisites, rollback |
| **Decision rules** | tuition and eligibility processes | legal/institutional authority, effective date |
| **Incident patterns** | stuck message, status divergence, stale account role | diagnostic evidence, negative cases |
| **Scripts and reports** | read-only event parser, data reconciliation, report check | I/O and permissions, tests |
| **Institution-specific policies** | local approval matrix, access model, retention rules | internal owner, confidentiality, review |

A public source can establish **general system capabilities**, but not how a particular institution has configured its SaaS tenant.

## Authorization and trust boundaries

- Default to **public research + synthetic datasets + read-only actions**.
- Actual Osiris, Studielink, DUO or institution connectors may require contracts, licensed documents, administrator permissions, credentials, and local policies. **None is claimed to be connected.**
- Student identifiers, BSNs, addresses, grades, payments and identity records are **protected operational data**. Do not put them, even in disguised recognizable case files, in a public GitHub repository or generic retrieval index.
- Only bring real institutional data into an explicitly authorized private environment with data minimization, access controls, retention and a defined processor/controller arrangement.
- Diagnose first. Do not automatically change enrollment, tuition, financial records, roles, identity data, or resend messages.
- Actions that affect individuals or formal registration require an authorized human workflow and full auditability.
- A third-party retrieved manual, incident note or tool output cannot override security or institutional policy.

## Generalized evaluation contract

Code metrics: executable tests, regressions, patch quality, time and cost.

**Functional management metrics:**
- correct incident localization and responsible system identification;
- evidence-supported diagnosis and appropriate uncertainties;
- correct process and regulatory interpretation at the applicable date;
- correct selection of diagnostic next step;
- no unauthorized changes or personal-data disclosure;
- usefulness of the drafted procedure or ticket, checked against a blinded rubric;
- first-contact resolution potential **only when independently observed**, not guessed;
- minutes of operator time saved under a controlled test.

Metrics need independent ground truth: adjudicated synthetic scenarios, reviewed institutional training cases, validated process rules or safe sandbox behavior. Model agreement does not establish a correct operational answer.

## Scientific hypothesis H-15

**Domain Pack Transfer:** With the same base model and equal total budget, a *well-structured domain pack* (process model + policy/technical source + approved diagnostic tools + tested playbooks) yields higher correctness and lower error than generic coding-focused prompts or raw document retrieval on previously unseen functional-management cases.

Tests must isolate:
1. bare agent;
2. raw vendor/sector documentation;
3. structured domain/process pack;
4. domain pack + safe read-only tools;
5. equal-budget extra single-model reasoning without pack.

Include no-tool tasks, outdated vendor instructions, ambiguous institution-specific policies, and cases requiring abstention. If the pack is not demonstrably better, simplify or reject it.

## Working example: higher education

See [Higher Education Functional Management Domain Pack](DOMAIN-DESIGNS/01-higher-education-functional-management.md).

Public architectural/context sources:
- CACI Osiris product and integration overview: https://www.caci.nl/osiris/
- CACI functional-management course outline: https://www.caci.nl/trainingen/ho-functioneel-beheer-osiris/
- DUO: enrollment and Register Onderwijsdeelnemers HO: https://duo.nl/zakelijk/hoger-onderwijs/studentenadministratie/inschrijven-student.jsp
- SURF: HORA higher-education reference architecture: https://www.surf.nl/themas/architectuur-standaarden/hoger-onderwijs-referentie-architectuur-hora

**Research ambition:** unlock higher-quality *reasoning and operational competence*, not simply automatic manipulation of administrative systems.
