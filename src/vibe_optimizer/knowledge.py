"""Local SQLite FTS5 knowledge prototype. Not an MCP service.

Sources and chunks can only be written by the explicit ingestion interface;
search always opens the database read-only and only returns approved sources.
"""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "database" / "schema.sql"


def init_database(path: str | Path) -> None:
    db_path = Path(path).resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as connection:
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


def ingest_source(
    path: str | Path, *, source_id: str, uri: str, title: str,
    license: str, sha256: str, retrieved_at: str, version: str = "",
    publisher: str = "", status: str = "staged",
) -> None:
    """Stage source metadata; source approval is a separate review step."""
    if status != "staged":
        raise ValueError("New sources must be staged for review")
    if not re.fullmatch(r"[a-zA-Z0-9_-]{1,120}", source_id):
        raise ValueError("Invalid source identifier")
    if not re.fullmatch(r"[a-fA-F0-9]{64}", sha256):
        raise ValueError("SHA-256 must be a full hexadecimal digest")
    with sqlite3.connect(Path(path).resolve()) as connection:
        connection.execute(
            """INSERT INTO sources
               (source_id, uri, title, publisher, version, license, sha256,
                retrieved_at, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (source_id, uri, title, publisher, version, license,
             sha256, retrieved_at, status),
        )


def ingest_chunk(path: str | Path, *, source_id: str, locator: str, body: str) -> None:
    """Index a chunk only for a registered source."""
    if not body.strip():
        raise ValueError("Chunk body is empty")
    with sqlite3.connect(Path(path).resolve()) as connection:
        source = connection.execute(
            "SELECT 1 FROM sources WHERE source_id = ?", (source_id,)
        ).fetchone()
        if not source:
            raise ValueError("Unknown source")
        connection.execute(
            "INSERT INTO chunks(source_id, locator, body) VALUES (?, ?, ?)",
            (source_id, locator, body),
        )


def compile_fts_query(query: str) -> str:
    """Produce a bounded phrase-only FTS expression from untrusted text."""
    terms = re.findall(r"\w+", query, re.UNICODE)
    terms = [term[:64] for term in terms[:12]]
    if not terms:
        raise ValueError("Query contains no searchable terms")
    return " OR ".join('"' + term.replace('"', '""') + '"' for term in terms)


def search(path: str | Path, query: str, *, limit: int = 5) -> list[dict]:
    """Return approved-only results; scores are ranks, not confidence."""
    db_path = Path(path).resolve(strict=True)
    expression = compile_fts_query(query)
    safe_limit = max(1, min(10, int(limit)))
    sql = """
        SELECT chunks.rowid AS chunk_id, chunks.source_id,
               chunks.locator, sources.uri, sources.title,
               sources.version, sources.sha256,
               snippet(chunks, 2, '[', ']', '…', 24) AS excerpt,
               bm25(chunks) AS rank
        FROM chunks JOIN sources ON sources.source_id = chunks.source_id
        WHERE chunks MATCH ? AND sources.status = 'approved'
        ORDER BY rank LIMIT ?
    """
    with sqlite3.connect(db_path.as_uri() + "?mode=ro", uri=True) as connection:
        connection.row_factory = sqlite3.Row
        return [dict(row) for row in connection.execute(sql, (expression, safe_limit))]
