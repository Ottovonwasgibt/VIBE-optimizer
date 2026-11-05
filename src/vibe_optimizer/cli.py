"""Local admin/debug CLI. Review actions are NOT an authorization boundary.

Production deployment needs OS-level separation between the staging/review
process and read-only MCP process. Do not expose review commands to agents.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .knowledge import (
    get_chunk, init_database, review_source, search, stage_document,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="vibe-brain")
    parser.add_argument("--db", required=True, type=Path, help="Local SQLite file")
    subs = parser.add_subparsers(dest="command", required=True)
    subs.add_parser("init", help="Initialize empty SQLite database")
    stage = subs.add_parser("stage", help="Stage a local UTF-8 document")
    stage.add_argument("--file", required=True, type=Path)
    stage.add_argument("--id", required=True)
    stage.add_argument("--uri", required=True)
    stage.add_argument("--title", required=True)
    stage.add_argument("--license", required=True)
    stage.add_argument("--version", default="")
    stage.add_argument("--publisher", default="")
    review = subs.add_parser("review", help="Administrative, manual review operation")
    review.add_argument("--id", required=True)
    review.add_argument("--reviewer", required=True)
    review.add_argument("--action", required=True, choices=["approve", "revoke"])
    lookup = subs.add_parser("search", help="Search only approved source chunks")
    lookup.add_argument("query")
    lookup.add_argument("--limit", type=int, default=5)
    get = subs.add_parser("get", help="Get approved chunk by row ID")
    get.add_argument("chunk_id", type=int)
    args = parser.parse_args(argv)

    if args.command == "init":
        init_database(args.db)
        print(f"Initialized {args.db}")
    elif args.command == "stage":
        source = args.file.read_text(encoding="utf-8")
        digest = stage_document(
            args.db, source_id=args.id, uri=args.uri, title=args.title,
            content=source, license=args.license, publisher=args.publisher,
            version=args.version,
        )
        print(json.dumps({"status": "staged", "sha256": digest}))
    elif args.command == "review":
        review_source(args.db, source_id=args.id,
                      reviewer=args.reviewer, action=args.action)
        print(json.dumps({"source_id": args.id, "action": args.action}))
    elif args.command == "search":
        print(json.dumps(search(args.db, args.query, limit=args.limit), indent=2))
    elif args.command == "get":
        print(json.dumps(get_chunk(args.db, args.chunk_id), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
