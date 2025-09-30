import json
import os
import shutil
import subprocess
from typing import Any, Dict, List

import pytest

pytestmark = pytest.mark.skipif(
    shutil.which("node") is None or shutil.which("npx") is None,
    reason="Node/npx not present; skipping Inspector CLI smoke test.",
)


def _inspector_enabled() -> bool:
    return os.getenv("ENABLE_SMOKE_INSPECTOR", "0") == "1"


@pytest.mark.skipif(
    not _inspector_enabled(),
    reason="Inspector smoke test disabled by default; set ENABLE_SMOKE_INSPECTOR=1 to enable",
)
def test_tools_list_returns_tools() -> None:
    cmd = [
        "npx",
        "--yes",
        "@modelcontextprotocol/inspector",
        "--cli",
        "--",
        "uvx",
        "--from",
        "awslabs.openapi-mcp-server@latest",
        "awslabs.openapi-mcp-server",
        "--api-name",
        "petstore",
        "--api-url",
        "https://petstore3.swagger.io/api/v3",
        "--spec-url",
        "https://petstore3.swagger.io/api/v3/openapi.json",
        "--method",
        "tools/list",
    ]
    env = {"ENABLE_OPERATION_PROMPTS": "true"}
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env, check=False)
    stdout = proc.stdout.strip()
    assert proc.returncode == 0, (
        f"Inspector CLI failed: {proc.returncode}\n{proc.stderr}\n{stdout}"
    )

    last_json = None
    for line in stdout.splitlines()[::-1]:
        line = line.strip()
        if not line:
            continue
        try:
            last_json = json.loads(line)
            break
        except Exception:
            continue

    assert isinstance(last_json, dict), f"Unexpected output format:\n{stdout}"
    tools: List[Dict[str, Any]] = last_json.get("tools") or last_json.get("result") or []
    assert isinstance(tools, list) and len(tools) >= 1, "No tools returned"
    names = [t.get("name", "") for t in tools if isinstance(t, dict)]
    assert any("pet" in n.lower() or "store" in n.lower() for n in names), f"Tool names: {names}"
