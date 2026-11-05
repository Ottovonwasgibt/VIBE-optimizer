# Domain Pack 01 — Higher-Education Functional Management (Osiris, Studielink, DUO)

**Status:** research design with public-source grounding; **not** an implementation, certified training guide or statement about any institution's actual configuration.  
**Date:** 2026-11-05. **Data classification:** public, synthetic examples only.

## Purpose

Build a VIBE-optimizer domain workbench for a functional manager in Dutch higher education. The agent must reason across organizational procedures, student information systems, enrollment and tuition processes, event/message exchanges, identity administration, reporting and authorization.

This should support **human work**: finding the right documentation, diagnosing likely root causes, preparing safe checks, comparing configurations, writing support responses and planning/validating changes. It must not presume full rights to access a vendor's SaaS infrastructure or student records.

## Source-of-truth hierarchy

1. **Observed current institutional tenant facts** — only if explicitly supplied under authorized private scope; configurations vary, and observed data can still be incomplete.
2. **Current contracts, vendor manuals and release notes** — accessible only where rights permit; distinguish supported API from locally enabled interface.
3. **Current approved institution policies and change procedures** — approval owner and effective date necessary.
4. **Official sector documents and regulations** — DUO, Studielink, SURF/HORA, official governmental sources; check study year and implementation date.
5. **Public vendor overview and training descriptions** — describes general capabilities, not exact local implementation.
6. **Prior troubleshooting episodes** — usable only when reviewed, anonymized, and matching current version/scope.

A model-generated SQL statement, guessed field name or undocumented event code is never authoritative evidence.

## Institutional process model (conceptual)

~~~text
Prospective student
       |
       v
Studielink: request/identification/education background
       |
       v
Institution: admission and enrollment decision
       |
       v
Student Information System (Osiris or other SIS)
       |            |
       |            +--> internal admissions / education / reporting
       |            +--> identity / communications / payments (implementation-specific)
       |
       v
Institutional reporting / DUO registration (ROD HO)
       |
       v
Acknowledgements, reconciliation, regulatory and operational checks
~~~

The exact physical routing, message structure and which component initiates what **must be verified** against current Studielink/DUO specifications and the institution's installed interfaces. The diagram is conceptual, not a claim of one universal direct API path.

**Grounding:** DUO explains Studielink identification and the institution's subsequent obligation to supply enrollment data to ROD HO. CACI's product documentation describes Osiris modules and its integration options. SURF's HORA provides the sector's reference vocabulary.

## Workbench shelves

| Shelf | Sample capability | Allowed initial access |
| --- | --- | --- |
| Process atlas | lifecycle from request to enrollment, study progress, diploma and termination | public/read-only |
| Regulation library | current DUO requirements, effective date, exception and validation sources | public/read-only |
| Vendor manual library | current Osiris user/help instructions and event/authorization documentation | licensed/internal, approval-gated |
| Integration atlas | Studielink/SIS/DUO message and acknowledgement stages | public conceptual; private schemas only with rights |
| Configuration library | reference tables, institutional workflows, forms, status mappings | private only, read-only by default |
| Diagnostic tool shelf | anonymized message comparison, XML/JSON validation, state reconciliation | approved local/test inputs |
| Reporting workshop | safe report specification, field lineage, BI queries and output validation | synthetic first |
| Operational memory | resolved incident patterns, known mismatches and rollback steps | reviewed, scoped and privacy-clean |

## Specific research tasks for the assistant

### A. Enrollment state inconsistency

**User-like request:** "Studielink shows an enrollment-related status that doesn't match what an authorized operator sees in the SIS. What should we check?"

The agent should:
- identify the exact status, timestamps and **different status semantics** before assuming a synchronization failure;
- reconstruct the expected process and last independently observed event;
- differentiate request, decision, financial conditions and final administrative registration;
- propose authorized read-only checks for source-of-truth and acknowledgements;
- ask for institution-specific mapping when it is not documented;
- recommend escalation to the relevant service owner, without fabricating a status mapping.

**Test oracle:** a synthetic event timeline with a known missing acknowledgement or delayed processing, distinct from actual vendor event codes.

### B. Integration/event failure

**User-like request:** "A message appears to have been produced but the receiving system has not updated."

The agent should separate generation, transmission, reception, validation, business-rule processing and user-facing publication. It should propose verifying the last confirmed stage, available logs/correlation IDs, retry policy and idempotency.

Vendor CACI publicly describes Osiris Event Broker logging and the possibility of re-offering messages. **That does not authorize an agent to resend events**, and the tenant-specific controls must be confirmed. Source: https://www.caci.nl/osiris/

### C. Reporting discrepancy

**User-like request:** "A study-progress or enrollment report doesn't agree with the administrator's screen."

Compare definitions of inclusion/exclusion, effective dates, joins and aggregations, authorization filters, refresh latency, report-template selection and SQL/run-time environment. Generate a **read-only** query design or test plan only after a real schema is supplied, otherwise avoid hallucinating tables or columns.

### D. Role/identity mismatch

**User-like request:** "A staff member can log in but lacks the expected function."

Map identity, authentication, attribute provisioning, group/role assignment, Osiris authorization profile, propagation and session/cache behavior. Treat every step as hypothesis pending actual identity/provider documentation. No privilege changes without institution approval.

### E. Tuition and enrollment eligibility

Use current **DUO rules for the applicable academic year** as public context, but distinguish government indicators from formal institution decisions. Escalate ambiguous nationality/residency/previous degree cases to an authorized operator. Do not issue definitive financial or legal eligibility determinations from incomplete data. Source: https://www.duo.nl/zakelijk/hoger-onderwijs/studentenadministratie/soort-collegegeld.jsp

### F. Change management

**User-like request:** "We need to adapt a registration process."

Produce a requirements matrix, impacted process map, permissions, integration contracts, release dependencies, sandbox tests, rollback/communication plan and approval list. Never apply production changes from a generated plan without authorized workflow.

## A safe incident-analysis output contract

*Project-owned example, not a vendor API.*

~~~json
{
  "case_id": "SYNTHETIC-001",
  "systems": ["Studielink", "SIS", "DUO registration"],
  "reported_symptom": "Status mismatch",
  "facts": [
    {"source": "synthetic event log", "observation": "event created at T1"}
  ],
  "hypotheses": [
    {"cause": "Receiver business validation pending", "status": "unverified"}
  ],
  "missing_evidence": ["Acknowledgement status", "current local status mapping"],
  "safe_next_checks": ["Compare timestamp and correlation ID in authorized logs"],
  "recommended_owner": "institution service owner",
  "proposed_actions": [],
  "requires_human_approval": true
}
~~~

Retain citations per claim, event timestamps and source scope. The agent should be allowed to say: "The available evidence cannot yet distinguish between two failure stages."

## Example safe synthetic timeline

These are **invented fixture labels**, never actual Studielink/Osiris protocol codes.

| Time | Component | Synthetic observation |
| --- | --- | --- |
| 09:00 | Portal | APPLICATION_REQUESTED |
| 09:01 | Exchange | REQUEST_EMITTED, correlation TEST-42 |
| 09:03 | SIS intake | REQUEST_RECEIVED, correlation TEST-42 |
| 09:04 | SIS workflow | AWAITING_MANUAL_REVIEW |
| 09:12 | Operator | "Why is registration not finalized?" |

Correct diagnostic behavior: distinguish a pending institutional review from failed message transport, identify no evidence of final enrollment, request authorized review/status mapping; **do not resubmit or register the student**.

## Prototype packs

1. \`enrollment-lifecycle\`: source-dated diagrams and terminology.
2. \`message-troubleshooting\`: generic message-state reasoning and safe correlation tools.
3. \`sis-report-validation\`: report definition, data lineage and test templates.
4. \`identity-role-diagnosis\`: authentication vs role/authorization separation.
5. \`tuition-rule-references\`: source-dated rule bibliography and escalation boundaries.
6. \`change-impact-review\`: impact, approval and rollback plan.

Each pack must indicate **public vs internal**, applicable system versions, task triggers, contraindications, required permissions, evidence sources, and whether a diagnostic tool is tested or only planned.

## Evaluation program

Do not start by uploading live production tickets or user-identifiable student cases to a public repository. Instead:

- build 12-20 synthetic, independently reviewed incident cases with event timelines and unambiguous or deliberately ambiguous facts;
- split into message failure, reporting difference, authorization problem, process/eligibility question and change request;
- compare one pinned model with (A) no domain pack, (B) raw public docs, (C) dated structured process pack, (D) pack plus read-only diagnostics;
- measure correct next investigative step, correct known/unknown separation, factual/procedural accuracy, risk of inappropriate mutation, cited source/date, completeness of handover;
- budget-match inference; use blinded human rubric plus deterministic checks where feasible;
- hold out institution-specific information and include cases where the right answer is "verify with authorized staff".

**Research hypothesis:** retrieval of *process relationships and evidence requirements* may help more than retrieving isolated snippets, especially where status labels differ across systems. Do not claim this without testing.

## Non-negotiable data and authorization rules

- No student IDs, BSNs, bank details, grades, correspondence, exports, or actual event payloads in public repo or unapproved external AI.
- No direct production mutations, resends, tuition decisions, access grants or enrollment decisions.
- Consent to use an AI tool is not equivalent to organizational permission to share personal data or vendor materials.
- Admin-disabled capabilities in SaaS are not bypassed by constructing an unofficial API. Public Osiris S2S descriptions **do not prove entitlement** to any endpoint.
- For a future private deployment, define data owner, processor arrangement, lawful basis, retention, DPIA as appropriate, incident audit and permission boundaries.

## Current authoritative public sources (verify effective dates on each use)

- CACI Osiris product modules, integration, Event Broker, S2S and gateway overview: https://www.caci.nl/osiris/
- CACI HO functional management curriculum; Studielink/Osiris processes and authorization: https://www.caci.nl/trainingen/ho-functioneel-beheer-osiris/
- DUO higher education registration and ROD HO: https://duo.nl/zakelijk/hoger-onderwijs/studentenadministratie/inschrijven-student.jsp
- DUO tuition category rules: https://www.duo.nl/zakelijk/hoger-onderwijs/studentenadministratie/soort-collegegeld.jsp
- SURF HORA reference architecture: https://www.surf.nl/themas/architectuur-standaarden/hoger-onderwijs-referentie-architectuur-hora
- SURF SURFeduhub/OOAPI information: https://servicedesk.surf.nl/wiki/pages/viewpage.action?pageId=128920594
- DUO RIO education registry: https://rio-kennisbank.duo.nl/6-ho/aa-wat-is-rio-ho.jsp

**Next testable engineering slice:** a *synthetic* read-only event-timeline reconciler plus a human-scored incident response benchmark. The model should explain why it proposes each check and what observation would refute the diagnosis.

## Practical deployment correction: closed manuals are useful, but accessed elsewhere

The target institutional agent **can use approved restricted Osiris/Studielink documentation** in a separate permissioned environment. That source material is not available in this public ChatGPT session or repository; no license-restricted manuals need to be uploaded here. Public research outputs should provide schemas and methods for an internal implementation rather than the documents themselves.

See [Private Knowledge Boundary](../PRIVATE-KNOWLEDGE-BOUNDARY.md). In particular: access to a local document does not mean permission to transmit it to a remote model API. Before using a private source, check institution rights, endpoint processing authorization, principal scope, logging/retention and whether only metadata or approved excerpts may enter the model context.
