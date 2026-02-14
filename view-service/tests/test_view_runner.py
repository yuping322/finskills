from __future__ import annotations

import sys
import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Ensure `view-service/` is importable when running from repo root.
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "view-service"))

from view_service.provider_base import ToolProvider, ToolResult  # noqa: E402
from view_service.view_runner import run_view  # noqa: E402
from view_service.views_cn import ViewSpec  # noqa: E402


@dataclass
class FakeProvider(ToolProvider):
    calls: list[tuple[str, dict[str, Any]]]

    def call_tool(self, name: str, args: dict[str, Any], *, refresh: bool, meta_script: str) -> ToolResult:
        _ = refresh, meta_script
        self.calls.append((name, dict(args)))
        return ToolResult(meta={"function": name}, data={"ok": True, "args": args}, warnings=[], errors=[])


class _Mod:
    @staticmethod
    def plan(params: dict) -> list[dict]:
        return [
            {"key": "a", "tool": "t1", "args": {"x": params.get("x", 1)}},
            {"key": "b", "tool": "t2", "args": {}},
        ]


class ViewRunnerTests(unittest.TestCase):
    def test_tool_view_executes_single_call(self) -> None:
        provider = FakeProvider(calls=[])
        spec = ViewSpec(
            name="stock_zh_a_spot_em",
            kind="tool_view",
            description="",
            params_schema={"type": "object", "properties": {}, "required": []},
            module=None,
        )
        out = run_view(spec, params={"k": "v"}, provider=provider, refresh=False)
        self.assertEqual(out.errors, [])
        self.assertEqual(provider.calls, [("stock_zh_a_spot_em", {"k": "v"})])
        self.assertIn("stock_zh_a_spot_em", out.data)

    def test_custom_view_executes_plan_tools(self) -> None:
        provider = FakeProvider(calls=[])
        spec = ViewSpec(
            name="demo_custom",
            kind="custom_view",
            description="",
            params_schema={"type": "object", "properties": {}, "required": []},
            module=_Mod,
        )
        out = run_view(spec, params={"x": 9}, provider=provider, refresh=True)
        self.assertEqual(out.errors, [])
        self.assertEqual(provider.calls, [("t1", {"x": 9}), ("t2", {})])
        self.assertEqual(set(out.data.keys()), {"a", "b"})
