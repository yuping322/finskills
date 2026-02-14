from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ToolRegistry:
    tools_path: Path
    tool_index: dict[str, dict[str, Any]]  # name -> full tool dict

    @staticmethod
    def load(tools_path: Path) -> "ToolRegistry":
        tools_path = tools_path.resolve()
        raw = json.loads(tools_path.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            raise ValueError("tools json must be a list")

        index: dict[str, dict[str, Any]] = {}
        for item in raw:
            if not isinstance(item, dict):
                continue
            fn = item.get("function")
            if not isinstance(fn, dict):
                continue
            name = fn.get("name")
            if not isinstance(name, str) or not name:
                continue
            index[name] = item

        if not index:
            raise ValueError("tool registry is empty")

        return ToolRegistry(tools_path=tools_path, tool_index=index)

    def describe(self, name: str) -> dict[str, Any] | None:
        tool = self.tool_index.get(name)
        if not tool:
            return None
        fn = tool.get("function")
        return fn if isinstance(fn, dict) else None

