import sqlite3
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from vibe_optimizer.knowledge import (  # noqa: E402
    chunk_text, compile_fts_query, get_chunk, init_database,
    review_source, search, stage_document,
)


class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = Path(self.temp.name) / "knowledge.sqlite"
        init_database(self.db)
        self.content = "# Async\n\nPython asyncio cancellation and shutdown cleanup."
        self.sha = stage_document(
            self.db, source_id="python", uri="https://example.org/python",
            title="Async docs", content=self.content, license="test-fixture",
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_staged_is_invisible(self):
        self.assertEqual(search(self.db, "asyncio"), [])
        with closing(sqlite3.connect(self.db)) as con:
            chunk_id = con.execute("SELECT rowid FROM chunks LIMIT 1").fetchone()[0]
        self.assertIsNone(get_chunk(self.db, chunk_id))

    def test_digest_matches_exact_text(self):
        import hashlib
        self.assertEqual(self.sha, hashlib.sha256(self.content.encode()).hexdigest())

    def test_review_and_revoke_gate_search_and_get(self):
        review_source(self.db, source_id="python", reviewer="test-reviewer", action="approve")
        results = search(self.db, "asyncio")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["sha256"], self.sha)
        self.assertIn("asyncio", get_chunk(self.db, results[0]["chunk_id"])["body"])
        review_source(self.db, source_id="python", reviewer="test-reviewer", action="revoke")
        self.assertEqual(search(self.db, "asyncio"), [])
        self.assertIsNone(get_chunk(self.db, results[0]["chunk_id"]))

    def test_unknown_license_not_approvable(self):
        stage_document(self.db, source_id="unknown", uri="file://example",
                       title="Unknown", content="testing", license="review-required")
        with self.assertRaises(ValueError):
            review_source(self.db, source_id="unknown", reviewer="reviewer", action="approve")

    def test_empty_reviewer_fails(self):
        with self.assertRaises(ValueError):
            review_source(self.db, source_id="python", reviewer="", action="approve")

    def test_duplicate_is_atomic(self):
        with self.assertRaises(sqlite3.IntegrityError):
            stage_document(self.db, source_id="python", uri="file://x",
                           title="Dup", content="duplicate", license="fixture")
        with closing(sqlite3.connect(self.db)) as con:
            self.assertEqual(con.execute("SELECT COUNT(*) FROM chunks").fetchone()[0], 1)

    def test_hostile_fts_tokens_are_quoted(self):
        self.assertEqual(compile_fts_query('asyncio " OR * - ^'), '"asyncio" OR "OR"')
        with self.assertRaises(ValueError):
            compile_fts_query("z" * 2050)
        review_source(self.db, source_id="python", reviewer="reviewer", action="approve")
        self.assertEqual(search(self.db, 'asdf " OR * - ^'), [])

    def test_reject_missing_data(self):
        with self.assertRaises(ValueError):
            stage_document(self.db, source_id="bad/id", uri="file://x", title="A",
                           content="some data", license="fixture")
        with self.assertRaises(ValueError):
            stage_document(self.db, source_id="valid", uri="file://x", title="A",
                           content=" ", license="fixture")

    def test_chunk_bounding(self):
        chunks = chunk_text("alpha " * 1000, max_chars=100)
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(0 < len(c) <= 100 for c in chunks))

    def test_review_audit(self):
        review_source(self.db, source_id="python", reviewer="reviewer", action="approve")
        with closing(sqlite3.connect(self.db)) as con:
            self.assertEqual(con.execute("SELECT reviewer FROM source_reviews").fetchone()[0], "reviewer")


if __name__ == "__main__":
    unittest.main()
