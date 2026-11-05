"""Offline, provenance-preserving SQLite FTS5 knowledge prototype.

All input is untrusted. Staging does not confer approval. Approval and
revocation are separate administrative actions, never exposed by read-only MCP.
"""
from __future__ import annotations

import hashlib
from contextlib import contextmanager
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "database" / "schema.sql"
MAX_DOCUMENT_CHARS = 256_000
MAX_CHUNK_CHARS = 1_200


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def _write_conn(path: str | Path):
    con = sqlite3.connect(Path(path).expanduser().resolve())
    try:
        with con:
            yield con
    finally:
        con.close()


def init_database(path: str | Path) -> None:
    db = Path(path).expanduser().resolve()
    db.parent.mkdir(parents=True, exist_ok=True)
    with _write_conn(db) as con:
        con.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


@contextmanager
def _read_only(path: str | Path):
    db = Path(path).expanduser().resolve(strict=True)
    # file: URI is created by pathlib, not user-controlled URL composition.
    con = sqlite3.connect(db.as_uri() + "?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA query_only = ON")
    try:
        yield con
    finally:
        con.close()


def chunk_text(text: str, *, max_chars: int = MAX_CHUNK_CHARS) -> list[str]:
    """Deterministic, bounded paragraphs/chunks; preserve source order."""
    if not 100 <= max_chars <= 10_000:
        raise ValueError("Invalid chunk bound")
    paragraphs = re.split(r"\n\s*\n", text.replace("\r\n", "\n"))
    pieces: list[str] = []
    current = ""
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        while paragraph:
            room = max_chars - len(current) - (2 if current else 0)
            if room <= 0:
                pieces.append(current)
                current = ""
                continue
            if len(paragraph) <= room:
                current += ("\n\n" if current else "") + paragraph
                break
            if current:
                pieces.append(current)
                current = ""
                continue
            pieces.append(paragraph[:max_chars])
            paragraph = paragraph[max_chars:]
    if current:
        pieces.append(current)
    return pieces


def stage_document(
    path: str | Path, *, source_id: str, uri: str, title: str,
    content: str, license: str, publisher: str = "", version: str = "",
    retrieved_at: str | None = None,
) -> str:
    """Stage a local text document; returns SHA256 of exactly supplied UTF-8."""
    if not re.fullmatch(r"[a-zA-Z0-9_-]{1,120}", source_id):
        raise ValueError("Invalid source identifier")
    if not uri or not title.strip() or not license.strip():
        raise ValueError("URI, title and license must be supplied")
    if not content.strip() or len(content) > MAX_DOCUMENT_CHARS:
        raise ValueError("Empty or oversized document")
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    pieces = chunk_text(content)
    with _write_conn(path) as con:
        con.execute("PRAGMA foreign_keys = ON")
        con.execute(
            """INSERT INTO sources
            (source_id, uri, title, publisher, version, license, sha256,
             retrieved_at, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'staged')""",
            (source_id, uri, title, publisher, version, license,
             digest, retrieved_at or _now()),
        )
        con.executemany(
            "INSERT INTO chunks(source_id, locator, body) VALUES (?, ?, ?)",
            ((source_id, f"part-{i:04d}", piece)
             for i, piece in enumerate(pieces, start=1)),
        )
    return digest


def review_source(path: str | Path, *, source_id: str, reviewer: str,
                  action: str) -> None:
    """Administrative action only. Never expose via agent-accessible MCP."""
    if action not in {"approve", "revoke"}:
        raise ValueError("Invalid review action")
    if not reviewer.strip():
        raise ValueError("Reviewer is required")
    with _write_conn(path) as con:
        con.execute("PRAGMA foreign_keys = ON")
        record = con.execute(
            "SELECT status, license FROM sources WHERE source_id = ?",
            (source_id,),
        ).fetchone()
        if record is None:
            raise ValueError("Unknown source")
        status, license_name = record
        if action == "approve":
            if status != "staged":
                raise ValueError("Only staged sources can be approved")
            if license_name.lower() in {"review-required", "unknown", ""}:
                raise ValueError("License review required")
            if not con.execute("SELECT 1 FROM chunks WHERE source_id=? LIMIT 1",
                               (source_id,)).fetchone():
                raise ValueError("Source has no content")
            new_status = "approved"
        else:
            if status == "revoked":
                raise ValueError("Already revoked")
            new_status = "revoked"
        con.execute("UPDATE sources SET status = ? WHERE source_id = ?",
                    (new_status, source_id))
        con.execute(
            "INSERT INTO source_reviews(source_id, action, reviewer, reviewed_at) "
            "VALUES (?, ?, ?, ?)",
            (source_id, action, reviewer.strip(), _now()),
        )


def compile_fts_query(query: str) -> str:
    """Quote individual tokens instead of passing untrusted FTS grammar."""
    if len(query) > 2048:
        raise ValueError("Query too long")
    terms = [x[:64] for x in re.findall(r"\w+", query, re.UNICODE)[:12]]
    if not terms:
        raise ValueError("Query contains no searchable terms")
    return " OR ".join('"' + token + '"' for token in terms)


def search(path: str | Path, query: str, *, limit: int = 5) -> list[dict]:
    safe_limit = max(1, min(int(limit), 10))
    expression = compile_fts_query(query)
    sql = """
        SELECT chunks.rowid AS chunk_id, chunks.source_id,
               chunks.locator, sources.uri, sources.title,
               sources.version, sources.license, sources.sha256,
               snippet(chunks, 2, '[', ']', '…', 24) AS excerpt,
               bm25(chunks) AS rank
        FROM chunks JOIN sources ON sources.source_id = chunks.source_id
        WHERE chunks MATCH ? AND sources.status = 'approved'
        ORDER BY rank LIMIT ?
    """
    with _read_only(path) as con:
        return [dict(row) for row in con.execute(sql, (expression, safe_limit))]


def get_chunk(path: str | Path, chunk_id: int) -> dict | None:
    """Get content and provenance, never bypassing approval or size limits."""
    sql = """
        SELECT chunks.rowid AS chunk_id, chunks.source_id,
               chunks.locator, chunks.body, sources.uri, sources.title,
               sources.version, sources.license, sources.sha256
        FROM chunks JOIN sources ON sources.source_id = chunks.source_id
        WHERE chunks.rowid = ? AND sources.status = 'approved'
    """
    with _read_only(path) as con:
        row = con.execute(sql, (int(chunk_id),)).fetchone()
        return dict(row) if row else None
