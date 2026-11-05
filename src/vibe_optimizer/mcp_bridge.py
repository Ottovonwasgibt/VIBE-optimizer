"""Optional public-only, read-only MCP v2 adapter for Capability Registry.

Uses official MCP Python SDK v2 import: from mcp.server import MCPServer.
No server starts during import. This is NOT a private-source connector or
a generalized execution gateway; tools only inspect synthetic/public cards.
Model-supplied version hints are unverified and explicitly marked as such.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from vibe_optimizer.capability_registry import CapabilityRegistry, TaskContext
from vibe_optimizer.task_router import Signals, route_task


def parse_version_hints(encoded: str) -> tuple[tuple[str, str], ...]:
    if not isinstance(encoded, str) or len(encoded) > 1000:
        raise ValueError("Version hint JSON must be a bounded string")
    mapping = json.loads(encoded)
    if not isinstance(mapping, dict) or len(mapping) > 10:
        raise ValueError("Version hints must be a small JSON object")
    if any(not isinstance(k, str) or not isinstance(v, str)
           or not k or not v or len(k)>100 or len(v)>100
           for k,v in mapping.items()):
        raise ValueError("Only short string version labels are accepted")
    return tuple(sorted(mapping.items()))


def create_public_server(catalog: str | Path, *, server_factory=None,
                         environment: str | None = None):
    """Create a public capability discovery MCP server (SDK not always installed).

    Test stub accepts server name and exposes .tool(). No permissions change.
    Real deployment must bind environment and versions to trusted project facts.
    """
    if server_factory is None:
        try:
            from mcp.server import MCPServer
        except ImportError as exc:
            raise RuntimeError("Install optional MCP Python SDK v2: pip install mcp>=2,<3") from exc
        server_factory = MCPServer

    registry = CapabilityRegistry.load(catalog)
    env = environment or ("windows" if os.name == "nt" else "linux")
    server = server_factory("vibe-optimizer-public-workbench")

    def context(query: str, encoded: str) -> TaskContext:
        return TaskContext(
            question=query, environment=env,
            versions=parse_version_hints(encoded),
            permissions=frozenset({"public_read"}),
            permitted_classifications=frozenset({"PUBLIC"}),
        )

    @server.tool()
    def workbench_search(query: str, version_hints_json: str = "{}") -> dict:
        """Search public, qualified capability metadata, never invoke a tool."""
        ctx = context(query, version_hints_json)
        found = registry.search(ctx, limit=5)
        return {
            "candidates": [dict(capability_id=s.capability_id, kind=s.kind,
                                score=s.score, source=s.source,
                                revision=s.revision) for s in found],
            "version_hints_verified": False,
            "status": "advisory_only",
            "scope": "public_metadata_no_execution",
        }

    @server.tool()
    def workbench_inspect(capability_id: str,
                          version_hints_json: str = "{}") -> dict:
        """Inspect one authorized public capability card; no script execution."""
        ctx = context("inspect capability", version_hints_json)
        info = registry.inspect(capability_id, ctx)
        return {
            "result": info,
            "version_hints_verified": False,
            "status": "not_found_or_not_authorized" if info is None else "advisory_only",
        }

    @server.tool()
    def workbench_plan(query: str, version_hints_json: str = "{}") -> dict:
        """Get a simple suggested first action; no model reasoning or execution."""
        ctx = context(query, version_hints_json)
        result = route_task(ctx, Signals(external_capability_needed=True), registry)
        return {
            "next_action": result.next_action,
            "reason": result.reason,
            "candidate_ids": result.candidate_ids,
            "version_hints_verified": False,
            "status": "advisory_only",
        }

    return server
