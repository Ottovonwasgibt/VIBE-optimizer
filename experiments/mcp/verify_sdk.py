"""SDK v2 in-memory integration smoke test (real MCP protocol, no Vibe model).

Install optional SDK v2 first: python -m pip install "mcp>=2,<3".
Use only the fictional catalog in examples/capability-workbench/catalog.json.
"""
from __future__ import annotations

import asyncio
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"src"))
from vibe_optimizer.mcp_bridge import create_public_server


async def main() -> None:
    from mcp import Client
    server=create_public_server(
        ROOT/"examples"/"capability-workbench"/"catalog.json",
        environment="windows",
    )
    async with Client(server,raise_exceptions=True) as client:
        response=await client.call_tool(
            "workbench_search",
            {"query":"Pydantic v2 model validation API",
             "version_hints_json":'{"pydantic":"2"}'},
        )
        if response.is_error:
            raise AssertionError("MCP tool reported error")
        print("synthetic structured_content:", repr(response.structured_content))
        print("synthetic content:", repr(response.content))
        payload=json.dumps(response.structured_content)
        if "api_pydantic_2" not in payload or "api_pydantic_1" in payload:
            raise AssertionError("Version mismatch in MCP result")
        if "restricted_vendor_manual" in payload:
            raise AssertionError("Private metadata was exposed")
        inspected=await client.call_tool(
            "workbench_inspect", {"capability_id":"restricted_vendor_manual"})
        if inspected.is_error:
            raise AssertionError("Inspect tool unexpectedly failed")
        inspect_payload=json.dumps(inspected.structured_content)
        if "Invented operations manual" in inspect_payload:
            raise AssertionError("Restricted content leaked")
        plan=await client.call_tool(
            "workbench_plan", {"query":"Studielink Osiris enrollment status process"})
        if plan.is_error or "higher_ed_process" not in json.dumps(plan.structured_content):
            raise AssertionError("Planner failed on fictional domain task")
    print("PASS: in-memory MCP v2 client exercised 3 public advisory tools")
    print("NO real Vibe session, private document, model inference or executable tool used")


if __name__=="__main__":
    asyncio.run(main())
