# TDD-01 — Knowledge Brain: source ingestion, retrieval and memory

**Status:** proposed implementation contract; not deployed. **First target:** Python 3.11+, SQLite FTS5, local offline/explicitly approved ingestion.

## Goals and explicit exclusions

MVP: find bounded relevant text from **approved** sources, preserve source/version/hash and reject revoked content. Do not add a vector DB before a benchmark shows that lexical retrieval is a bottleneck. Do not index confidential files, API keys or benchmark answer keys.

## Database v0.1

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE sources (
  source_id TEXT PRIMARY KEY,
  uri TEXT NOT NULL,
  title TEXT NOT NULL,
  publisher TEXT,
  version TEXT,
  license TEXT NOT NULL,
  sha256 TEXT NOT NULL,
  retrieved_at TEXT NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('staged','approved','revoked'))
);

CREATE VIRTUAL TABLE chunks USING fts5(
  source_id UNINDEXED,
  locator UNINDEXED,
  body,
  tokenize='unicode61'
);

CREATE TABLE memory (
  memory_id TEXT PRIMARY KEY,
  status TEXT NOT NULL CHECK(status IN ('proposed','verified','rejected','expired')),
  repository TEXT,
  git_commit TEXT,
  problem_signature TEXT NOT NULL,
  lesson TEXT NOT NULL,
  evidence_json TEXT NOT NULL,
  created_at TEXT NOT NULL
);
```

`chunks` is a virtual table and cannot enforce a conventional foreign key on `source_id`. **Ingestion must enforce referential integrity**, and tests must check for orphan chunks. For a later robust version consider a normal content table plus an external-content FTS index and triggers; follow SQLite docs carefully on rebuild semantics.

## Source catalog example

```json
{
  "source_id": "sqlite-fts5",
  "uri": "https://www.sqlite.org/fts5.html",
  "title": "SQLite FTS5",
  "publisher": "SQLite",
  "version": "retrieved-2026-11-05",
  "license": "review-required",
  "status": "staged",
  "sha256": "FULL_SHA256_AFTER_FETCH",
  "retrieved_at": "2026-11-05T00:00:00Z"
}
```

The above is **illustrative**, not a source to insert unchanged. Do not mark approved unless the ingestion job actually fetched, hashed, checked rights and reviewed the material. Timestamps must be actual observation times.

## Retrieval v0.1

```sql
SELECT
  chunks.rowid AS chunk_id,
  chunks.source_id,
  chunks.locator,
  sources.uri,
  sources.version,
  sources.sha256,
  snippet(chunks, 2, '[', ']', '…', 24) AS excerpt,
  bm25(chunks) AS rank
FROM chunks
JOIN sources USING (source_id)
WHERE chunks MATCH ?
  AND sources.status = 'approved'
ORDER BY rank
LIMIT ?;
```

The FTS5 query syntax is **not** a plain string syntax; untrusted input must be converted to quoted, bounded search tokens with parameter binding rather than passed as arbitrary FTS expressions. BM25 produces a **ranking score**, not a confidence probability. Avoid presenting arbitrary rank magnitudes as calibrated confidence.

### Safe query compilation sketch (Python)

```python
import re

def to_fts_match(text: str) -> str:
    tokens = re.findall(r"\w+", text, flags=re.UNICODE)[:12]
    if not tokens:
        raise ValueError("No searchable terms")
    return " OR ".join('"' + t.replace('"', '""') + '"' for t in tokens)
```

### Read-only database opening

```python
import sqlite3
from pathlib import Path

def connect_readonly(database_path: str):
    path = Path(database_path).resolve(strict=True)
    return sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
```

Enforce path limits and runtime service privileges **outside** SQLite. A read-only SQLite connection is not a complete OS sandbox.

## Ingestion steps

1. Parse a curated `resources/catalog` entry; permit only approved source domains and file types.
2. Fetch into a staging area; record exact bytes, timestamp, canonical URL and SHA-256.
3. Run a license/privacy/PII/secret check and quarantine suspicious content.
4. Parse headings, code fences, version banners and page anchors.
5. Chunk at semantic boundaries (sections/functions); retain `source_id`, heading and locator.
6. Stage in a temporary database; run schema checks, deduplication and retrieval tests.
7. After review, promote source status to `approved` atomically.
8. On revocation or superseded versions, purge from active retrieval (including auxiliary indexes).

No automatic running of code snippets from documentation during ingestion.

## Episodic memory contract

```yaml
memory_id: mem-000001
status: proposed
repository: example/project
git_commit: FULL_GIT_SHA
problem_signature: "async shutdown timeout"
lesson: "Check task cancellation paths before increasing timeout"
evidence:
  test_report: tests/run-001
  diff_review: review-001
proposed_by: agent
reviewed_by: null
```

The memory record must be reviewed and **independently validated** before the `verified` state is assigned. Store reviews and state transitions in an append-only audit trail in a later schema. Do not let the search service itself promote memory.

## MVP acceptance tests

- A known approved source is returned with stable source/locator/hash.
- Staged/revoked sources are never returned.
- Hostile FTS input cannot change SQL structure or bypass source filters.
- Too-long queries and result limits are bounded.
- Reindexing after source removal does not retain stale results.
- A newly proposed memory is not searchable as verified.
- Secret scanning and license review are mandatory ingest gates.

## Research questions

- Does +FTS5 improve correct-file localization vs Vibe baseline?
- Which chunk size and result budget minimizes context pollution?
- Does query expansion improve recall more than it harms precision?
- Is vector retrieval worth its embedding cost for unseen tasks?

## Primary references

- https://www.sqlite.org/fts5.html
- https://arxiv.org/abs/2005.11401
- https://modelcontextprotocol.io/specification
- https://py.sdk.modelcontextprotocol.io/
