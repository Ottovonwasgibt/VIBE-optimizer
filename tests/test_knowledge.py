import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from vibe_optimizer.knowledge import (  # noqa: E402
    init_database, ingest_chunk, ingest_source, search, compile_fts_query,
)


class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / "brain.sqlite"
        init_database(self.db)
        ingest_source(
            self.db, source_id="official", uri="https://example.org/docs",
            title="Demo official docs", license="test-only",
            sha256="a" * 64, retrieved_at="2026-11-05T00:00:00Z",
        )
        ingest_chunk(
            self.db, source_id="official", locator="section1",
            body="asyncio cancellation shutdown cleanup task",
        )

    def tearDown(self):
        self.tmp.cleanup()

    def test_staged_sources_hidden(self):
        self.assertEqual(search(self.db, "asyncio cancellation"), [])

    def test_approved_source_visible_with_provenance(self):
        with sqlite3.connect(self.db) as conn:
            conn.execute("UPDATE sources SET status='approved' WHERE source_id='official'")
        matches = search(self.db, "asyncio cancellation")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["source_id"], "official")
        self.assertEqual(matches[0]["locator"], "section1")
        self.assertEqual(matches[0]["uri"], "https://example.org/docs")

    def test_revoked_sources_hidden(self):
        with sqlite3.connect(self.db) as conn:
            conn.execute("UPDATE sources SET status='revoked' WHERE source_id='official'")
        self.assertEqual(search(self.db, "asyncio"), [])

    def test_fts_query_metacharacters_are_bounded(self):
        compiled = compile_fts_query('asyncio " OR * - ^')
        self.assertEqual(compiled, '"asyncio" OR "OR"')
        self.assertLessEqual(len(compile_fts_query("word " * 100).split(" OR ")), 12)

    def test_unknown_source_rejected(self):
        with self.assertRaises(ValueError):
            ingest_chunk(self.db, source_id="unknown", locator="x", body="text")

    def test_new_source_cannot_self_approve(self):
        with self.assertRaises(ValueError):
            ingest_source(
                self.db, source_id="trusted", uri="https://example.org",
                title="Trusted", license="test-only", sha256="b" * 64,
                retrieved_at="2026-11-05T00:00:00Z", status="approved",
            )


if __name__ == "__main__":
    unittest.main()
