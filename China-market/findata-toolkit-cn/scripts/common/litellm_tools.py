"""
Tool registry loader for litellm-style tool definitions.

The skill ships with `config/litellm_tools.json` which enumerates AKShare-backed
functions and their JSON schemas. We use it to:
- list available tools
- show per-tool schemas
- validate/cast arguments before calling akshare
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def default_tools_json_path() -> Path:
    project_dir = Path(__file__).resolve().parent.parent.parent
    return project_dir / "config" / "litellm_tools.json"


def load_tools_config(path: Path | None = None) -> list[dict[str, Any]]:
    tools_path = (path or default_tools_json_path()).resolve()
    raw = json.loads(tools_path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("litellm_tools.json must be a list")
    return raw


def build_tool_index(tools_config: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for tool in tools_config:
        fn = tool.get("function") if isinstance(tool, dict) else None
        if not isinstance(fn, dict):
            continue
        name = fn.get("name")
        if not isinstance(name, str) or not name:
            continue
        index[name] = tool
    return index

