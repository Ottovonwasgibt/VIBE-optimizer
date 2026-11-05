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


def decode_tool_response(result) -> dict:
    """SDK v2 may return a JSON text block instead of structured_content."""
    if result.is_error:
        raise AssertionError("MCP tool returned an error")
    if result.structured_content is not None:
        return result.structured_content
    if not result.content or not hasattr(result.content[0], "text"):
        raise AssertionError("MCP did not return JSON text")
    value = json.loads(result.content[0].text)
    if not isinstance(value, dict):
        raise AssertionError("Expected result object")
    return value


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
        result=decode_tool_response(response)
        ids=[x["capability_id"] for x in result["candidates"]]
        if "api_pydantic_2" not in ids or "api_pydantic_1" in ids:
            raise AssertionError("Version mismatch in MCP result")
        if "restricted_vendor_manual" in ids:
            raise AssertionError("Private metadata was exposed")
        inspected=await client.call_tool(
            "workbench_inspect", {"capability_id":"restricted_vendor_manual"})
        if inspected.is_error:
            raise AssertionError("Inspect tool unexpectedly failed")
        inspected_result=decode_tool_response(inspected)
        if inspected_result.get("result") is not None:
            raise AssertionError("Restricted content leaked")
        plan=await client.call_tool(
            "workbench_plan", {"query":"Studielink Osiris enrollment status process"})
        plan_result=decode_tool_response(plan)
        if "higher_ed_process" not in plan_result["candidate_ids"]:
            raise AssertionError("Planner failed on fictional domain task")
    print("PASS: in-memory MCP v2 client exercised 3 public advisory tools")
    print("NO real Vibe session, private document, model inference or executable tool used")


if __name__=="__main__":
    asyncio.run(main())
