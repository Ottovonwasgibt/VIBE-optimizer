# Private Knowledge Boundary — public architecture, restricted documentation

**Status:** design and governance proposal; no private repositories, Osiris/Studielink installations, institution systems or restricted documents are connected to this project.

## Clarification of deployment scope

VIBE-optimizer may draw on **closed, licensed and institution-internal documentation** in an **explicitly authorized deployment**. This public ChatGPT/GitHub project has **no presumed access** to such materials. The absence of those documents here must not be mistaken for a prohibition on using them in a separate approved environment.

The public GitHub repository can contain:
- architecture, code, tests and manifests without proprietary content;
- references to public documentation and synthetic case fixtures;
- schemas for local-only source indexes and permission-aware retrieval;
- instructions for a private deployer to supply approved sources themselves.

It must **not** contain:
- copied licensed manuals or proprietary Studielink/Osiris documentation without redistribution rights;
- internal integration diagrams, private endpoint addresses, credentials or sensitive operational logs;
- student/personnel data, internal tickets with identifying details or derived private-data summaries.

## CRITICAL: Local CLI is not necessarily local inference

Running Vibe on a local Windows computer **does not imply that its language model runs locally**. If Vibe calls a remote model API, source excerpts and prompts may leave the device even when a retrieval MCP server and PDF files are local.

Before connecting closed docs to a model, determine:
1. Where inference is performed (local vs remote), including subprocesses, extensions, telemetry and logs.
2. Whether the institution authorizes sending this category of information to that model provider and endpoint.
3. The applicable contract, processor agreement, retention and security requirements.
4. Whether full excerpts, redacted excerpts, summaries, or **metadata only** may be sent.
5. Whether access is scoped to the acting user and the legitimate business purpose.

If these conditions are unknown, **default to no confidential document excerpts in model context**. A locally running, institution-approved model or a private approved endpoint is a possible alternative; neither is assumed present.

## Proposed deployment architecture

~~~text
PUBLIC PLANE (GitHub)
  workbench source, open docs, schema, synthetic fixtures
                         |
                         | code/config installed under approved governance
                         v
PRIVATE PLANE (institution / authorized workstation)
  approved closed manuals + local ticket/process notes
         |
    controlled document intake
    (rights, revision, effective date, owner, classification)
         |
    permission-aware private index
         |
    local/private retrieval gateway  <---- identity + user scope + audit
         |
    result policy
       +--> publicly shareable text
       +--> approved limited excerpts
       +--> on-prem inference only
       +--> metadata / refusal
         |
     task-solving agent (only allowed evidence for chosen model location)
         |
     advisory recommendation + sources + unknowns
         |
     approval for changes, messages, enrollment/finance/roles
~~~

**No public fallback:** if the private index is unavailable, do not silently upload a document to a public tool or paste it into an unapproved service.

## Classification and access model

| Tier | Examples | Retrieval/model policy |
| --- | --- | --- |
| PUBLIC | official public vendor marketing/docs, publicly published DUO guidance | normal citation and review |
| RESTRICTED | licensed vendor manuals, internal procedure guides, non-public schema specs | query only by entitled users and approved processing location |
| CONFIDENTIAL | incident timelines, tenant configs, staff notes, integration logs | narrowly scoped, logged, minimize output and retention |
| PERSONAL | student/student-finance/personnel records | separately authorized case-specific processing; not general memory or research index |
| SECRET | credentials, access tokens, signing materials | never place in model context or retriever results |

Document access is **not** a license to republish documents or index them for all colleagues. Access control must apply before retrieval results are returned, with tenant/role/record scope, and again to snippets sent to model inference.

## Proposed private source manifest

Project-specific schema example (not an Osiris/Studielink API):

~~~yaml
source_id: osiris-vendor-manual-local-example
status: staged
classification: RESTRICTED
storage_location: private-only
source_uri: "internal://approved-documents/source-id"
version: "verified-by-document-owner"
effective_from: null
last_reviewed_at: null
owner: "institution-designated-owner"
licensing_review: pending
approved_principals: []
external_model_excerpt_policy: deny
local_retrieval_permission: deny_until_approved
sha256: null
~~~

The source owner must explicitly approve the document, purpose, ingest/index location, scope and model endpoint **before** changing the retrieval policy.

## Engineering contracts to research

- **Source intake:** user-supplied file or authorized institution connector, SHA-256, approved classification, canonical version, source section locators; no arbitrary network crawler or scraping.
- **Permission-aware retrieval:** user/role/purpose context + query -> only authorized source IDs/chunks; denial reason should not expose document content.
- **Model egress guard:** policy evaluates destination model endpoint and result classification before assembling context. Redaction alone is not automatically adequate.
- **Citation and traceability:** source ID, applicable date, retrieved version, limited locator; avoid public URLs for private content.
- **Audit:** access reason, source IDs and policy decision; protect audit itself and apply retention limits.
- **Expiration/revocation:** removed entitlements, obsolete manuals or contract changes immediately invalidate relevant retrieval and cached excerpts.
- **Evidence distinction:** public explanation vs internal tenant fact vs hypothesis; prevent the model from inventing restricted schema fields.
- **Non-escalation:** informational access does not grant API write privileges, event replay or permission changes.

## Safe staged research plan

**Stage A (this public repo):** public and fictitious documentation, test ACL and egress decisions against synthetic data, benchmark process reasoning.

**Stage B (private authorized machine):** local metadata-only inventory and restricted keyword search after policy approval; test that forbidden sources never appear and that no retrieved text is sent to unapproved inference endpoints.

**Stage C (approved deployment):** selectively authorize excerpt-level access only where the institution/provider agreement permits, compare diagnosis accuracy and traceability, keep all real data out of public artifact uploads.

**Stage D (optional operations):** gated read-only status inquiries; any intervention requires separate owner permission, current vendor API contract and audited workflow.

**Research hypothesis H-16:** A permission-aware, versioned private domain library improves evidence-grounded functional-management performance while maintaining approved data boundaries, relative to a public-only generic assistant under identical case conditions. This cannot be measured here on real restricted sources.

## Related design
- [Cross-domain Capability Engine](DOMAIN-OPERATIONS-CAPABILITY-ENGINE.md)
- [Higher-education management pack](DOMAIN-DESIGNS/01-higher-education-functional-management.md)
- [General architecture and trust boundaries](ARCHITECTURE.md)

**Non-goal:** claiming an existing student-record integration or external-document permission solely because the agent is running on an authorized user's laptop.
