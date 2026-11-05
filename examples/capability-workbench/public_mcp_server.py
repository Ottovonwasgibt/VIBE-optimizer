"""Optional real MCP SDK v2 stdio server for a public synthetic catalog.

Install locally: python -m pip install "mcp>=2,<3"
Start:          python examples/capability-workbench/public_mcp_server.py

Does NOT run until explicitly launched. Do NOT install into Vibe
automatically; verify the installed Vibe and SDK versions and inspect the
server's three read-only metadata tools before opting in.
"""
from __future__ import annotations

from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"src"))
from vibe_optimizer.mcp_bridge import create_public_server


def main() -> None:
    catalog=ROOT/"examples"/"capability-workbench"/"catalog.json"
    server=create_public_server(catalog)
    server.run()  # official MCPServer v2 stdio loop


if __name__=="__main__":
    main()
