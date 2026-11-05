import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from vibe_optimizer.cli import main  # noqa: E402


class CliTests(unittest.TestCase):
    def test_stage_review_search_revoke(self):
        with tempfile.TemporaryDirectory() as temp:
            d = Path(temp)
            db = d / "brain.sqlite"
            file = d / "fixture.md"
            file.write_text("Async Python code needs cancellation handling.", encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(main(["--db", str(db), "init"]), 0)
                self.assertEqual(main([
                    "--db", str(db), "stage", "--file", str(file),
                    "--id", "fixture", "--uri", "file://fixture.md",
                    "--title", "fixture", "--license", "test-fixture",
                ]), 0)
                self.assertEqual(main([
                    "--db", str(db), "review", "--id", "fixture",
                    "--reviewer", "tester", "--action", "approve",
                ]), 0)
            out = io.StringIO()
            with redirect_stdout(out):
                main(["--db", str(db), "search", "cancellation"])
            self.assertEqual(len(json.loads(out.getvalue())), 1)
            with redirect_stdout(io.StringIO()):
                main(["--db", str(db), "review", "--id", "fixture",
                      "--reviewer", "tester", "--action", "revoke"])
            out = io.StringIO()
            with redirect_stdout(out):
                main(["--db", str(db), "search", "cancellation"])
            self.assertEqual(json.loads(out.getvalue()), [])
