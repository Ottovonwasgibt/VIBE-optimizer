"""Offline MCP bridge contract tests without external SDK or an agent host."""
from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from vibe_optimizer.mcp_bridge import create_public_server, parse_version_hints


class FakeServer:
    def __init__(self,name):
        self.name=name
        self.tools={}
    def tool(self):
        def decorate(f):
            self.tools[f.__name__]=f
            return f
        return decorate


class McpBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=create_public_server(
            ROOT/"examples"/"capability-workbench"/"catalog.json",
            server_factory=FakeServer, environment="windows"
        )

    def test_narrow_read_only_tools_only(self):
        self.assertEqual(set(self.server.tools),
                         {"workbench_search","workbench_inspect","workbench_plan"})

    def test_version_aware_tool_search_is_advisory(self):
        response=self.server.tools["workbench_search"](
            "Pydantic v2 model validation API", '{"pydantic":"2"}'
        )
        ids=[x["capability_id"] for x in response["candidates"]]
        self.assertIn("api_pydantic_2",ids)
        self.assertNotIn("api_pydantic_1",ids)
        self.assertEqual(response["status"],"advisory_only")
        self.assertFalse(response["version_hints_verified"])

    def test_no_private_or_unqualified_exposure(self):
        result=self.server.tools["workbench_search"](
            "osiris manual authorization", "{}")
        self.assertNotIn("restricted_vendor_manual",
                         [x["capability_id"] for x in result["candidates"]])
        self.assertIsNone(self.server.tools["workbench_inspect"](
            "restricted_vendor_manual")["result"])
        self.assertIsNone(self.server.tools["workbench_inspect"](
            "tested_conversion")["result"])

    def test_only_host_environment_from_factory(self):
        result=self.server.tools["workbench_search"](
            "find symbols callers repository", "{}")
        # The tool exists in the catalog but has execute permission, not read.
        self.assertNotIn("repo_symbol_lookup",
                         [x["capability_id"] for x in result["candidates"]])

    def test_plan_is_not_execution(self):
        result=self.server.tools["workbench_plan"](
            "Studielink Osiris enrollment status process")
        self.assertEqual(result["next_action"],"search_workbench")
        self.assertIn("higher_ed_process",result["candidate_ids"])
        self.assertEqual(result["status"],"advisory_only")

    def test_untrusted_version_hints_are_strictly_bounded(self):
        for invalid in ('[]','{"pydantic":[]}','{"a":"'+("x"*101)+'"}',
                        '{"x":1}','not-json'):
            with self.subTest(invalid=invalid),self.assertRaises(
                    (ValueError,TypeError)):
                parse_version_hints(invalid)

    def test_valid_versions_are_sorted(self):
        self.assertEqual(parse_version_hints('{"z":"2","a":"1"}'),
                         (("a","1"),("z","2")))


if __name__=="__main__":
    unittest.main()
