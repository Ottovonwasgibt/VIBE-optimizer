# TDD-09 — Private Source Method and Executable Scaffold

**Date:** 2026-11-05  
**Scope:** *methodology and reusable scaffold only*. No closed manuals, student records, vendor credentials, institution APIs or tenant configurations live in this repository.

## User requirement

This public project develops **how** VIBE-optimizer would consult authorized restricted documentation in an institutional environment, **not the documents themselves**. The domain pack should be deployable to Osiris/Studielink functional management and also to unrelated authorized knowledge-intensive tasks.

## Architecture (planned deployment)

~~~text
Public GitHub scaffolding
  data contracts, domain pack schemas, tests and synthetic fixtures
                      |
                approved deploy
                      v
Institution-private installation
  authorized provider/local file adapters
       -> controlled intake and hashing
       -> version, license and owner review
       -> classified local search index
       -> identity + role + purpose + tenant ACL
       -> destination/LLM egress policy
       -> cited, minimal, untrusted evidence packet
       -> task-solving model and advisory workflow
       -> evidence review and protected operational audit
~~~

No assumptions that CLI-on-desktop implies on-device model inference. Inference location, provider contracts and allowed information classes must be evaluated **before** any production document snippet reaches the model.

## Working scaffold in this repository

| Component | Current state | Purpose |
| --- | --- | --- |
| [Private gateway](../../src/vibe_optimizer/private_knowledge.py) | **Executable prototype** | Source classification, policy checks and bounded retrieval over fictional in-memory docs |
| [Synthetic demo](../../examples/private-knowledge/demo.py) | **Executable prototype** | Show that a restricted snippet is blocked for public destination and visible for a simulated approved one |
| [Policy tests](../../tests/test_private_knowledge.py) | **Executable tests** | Class, role, purpose, tenant, staged/revoked, date range, digest, bypass resistance |
| [General knowledge base](../../src/vibe_optimizer/knowledge.py) | Existing unrelated public-source SQLite prototype | Source staging, review and FTS5 retrieval; **NOT permission-aware for private sources** |
| [Private Knowledge Boundary](../PRIVATE-KNOWLEDGE-BOUNDARY.md) | Architectural design | Confidentiality, authorization, egress, retention and source type policy |

**Critical boundary:** The existing \`knowledge.search\` and \`knowledge.get_chunk\` have only an approval-status gate, **not role/tenant/purpose/egress ACLs**. Never put confidential documents into that generic database or connect it directly to a model. This new gateway is a separated research prototype until the private storage adapter enforces ACLs *inside the retrieval query*.

## Approved-source workflow

1. **Inventory:** institution owner supplies a list of permitted source families, not full document uploads to public GitHub.
2. **Legal/contract classification:** source owner checks whether indexing, retention, excerpt use and remote inference are permitted. One permission does not imply the others.
3. **Version record:** capture title, owner, system/application version, publication/effective date, revision, SHA-256 and location URI.
4. **Controlled ingestion:** a private adapter reads only approved files or authenticated services under minimal scope. Documents remain in an institution-private location.
5. **Index and query:** index only after approval; filter tenant/role/purpose **before** scoring and assembling result snippets.
6. **Egress decision:** evaluate destination model endpoint, classification and source-specific allowlist before building any prompt.
7. **Evidence packet:** limited fragment and locator, version and content digest, explicit marker that source content is *untrusted data*, uncertainty and conflicting versions.
8. **Use and verify:** the agent analyses and proposes; factual/procedural checks and relevant human review remain external.
9. **Revoke or expire:** immediately invalidate index results and caches when permissions/documents change. Audit without echoing confidential text.

## Proposed private metadata contract

~~~json
{
  "source_id": "institution-internal-doc-id",
  "classification": "RESTRICTED",
  "status": "staged",
  "owner": "assigned-by-institution",
  "tenant": "internal-tenant-id",
  "effective_from": null,
  "effective_to": null,
  "version": "specified-by-document-owner",
  "sha256": "computed-from-locally-approved-bytes",
  "uri": "internal://document-ref",
  "access": {
    "allowed_roles": [],
    "allowed_purposes": [],
    "allowed_model_destinations": []
  },
  "rights": {
    "index_permission": "review-required",
    "model_excerpt_permission": "deny-by-default"
  }
}
~~~

This is a **project-defined manifest**, not a field mapping to Osiris or Studielink. All approvals must originate from a trusted administrative process, not source text or a model suggestion.

## Workbench tools to implement, in order

1. \`private_source_inventory()\` — authorized human/admin UI, metadata only.
2. \`private_source_stage(source, policy)\` — admin-only, local source acquisition + hash + rights review.
3. \`private_source_approve(source_id, owner_approval)\` — admin process, not agent-accessible.
4. \`private_search(query, purpose)\` — safe read-only tool receiving **server-derived principal and model destination**, returning only authorized excerpts.
5. \`private_get(source_id, locator)\` — the same authorization boundary as search, bounded by chunk.
6. \`private_source_revoke(source_id)\` — admin process that purges relevant index/caches.
7. \`private_audit_report()\` — secured operational diagnostics, never a public trace.

**MCP caution:** Do not expose actor identity, roles, desired classification or model endpoint as editable arguments to the model, and do not let the model choose what it is authorized to view. The MCP server must derive them from a trusted session. Prefer separate processes/credentials for admin intake and read-only agent retrieval.

## Security and validation details for deployment

This initial prototype is **not** a safe production security boundary. It intentionally omits:
- actual authentication, trusted role resolution and institution SSO;
- transport TLS, OS-level ACL and process isolation;
- real private storage, at-rest encryption, secure key management;
- query-time database RLS, multi-tenant index isolation;
- reliable immutable audit trail and operational retention policy;
- scanning/parsing of PDF/Word/HTML, embedded instructions and malicious files;
- model endpoint identity attestation, network egress enforcement and vendor data processing agreements;
- license/contract checks beyond fixture flags;
- automatic invalidation of prompt caches, stale sessions or embeddings.

The real deployment must address these before confidential sources are indexed or sent to any model. A safe interim capability is **metadata-only** or purely synthetic demonstrations.

## Current scaffold run

With Python 3.11+ from the repository root:

~~~powershell
python examples/private-knowledge/demo.py
python -m unittest discover -s tests -v
~~~

Expected demo pattern: the \`public-remote-model\` receives **0** fictional restricted fragments; the \`approved-demo-model\` receives **1**. This is a *policy unit test*, not authorization against a real model endpoint.

## First realistic but private-domain-independent experiments

- **D01 Permission isolation:** two fictional tenants with overlapping keywords; searching one tenant must not return any source from the other.
- **D02 Model egress:** same user and document, changed destination policy; public endpoint never receives restricted bytes.
- **D03 Version staleness:** expired source or revoked source must disappear immediately; negative cache tests pending.
- **D04 Retrieval quality:** compare generic source chunks, structured process knowledge and verified procedures with a fixed inference budget and synthetic cases.
- **D05 Failure reporting:** distinguish unavailable documentation from unsupported claims, without leaking source titles or metadata.
- **D06 Integration boundary:** validate that a deployed read-only MCP server cannot call admin approval/mutation endpoints.

The first three can run without documents or external networks. D04 requires access to a model runtime and an independent case evaluation. D06 needs the target Vibe host version and institution-approved environment.

## Recommended work sequence

**P0:** Run prototype tests and fix policy/shape errors.  
**P1:** Make a private source-manifest JSON Schema and fixtures; add a source-adapter protocol with explicit security assumptions.  
**P2:** Build a separate, encrypted institution-only index with identity-aware filtered retrieval and protected audit.  
**P3:** Expose only the read-only search/get MCP interface after host permission and egress validation.  
**P4:** Reproduce synthetic domain evaluations comparing public-only vs authorized knowledge packs.  
**P5:** Consider real data/workflow integration only with institution approval.

**Success criterion:** a general method to attach *any* authorized knowledge base to one agent, not a one-off Osiris integration or a demand to transfer confidential documents into this conversation.
