from __future__ import annotations

import importlib
import pkgutil
from dataclasses import dataclass
from types import ModuleType
from typing import Any


@dataclass(frozen=True)
class ViewSpec:
    name: str
    description: str
    params_schema: dict[str, Any]
    module: ModuleType


def _build_tool_view_module(tool_name: str, tool: dict[str, Any]) -> ModuleType:
    pkg_name = __name__.rsplit(".", 1)[0]  # scripts.views
    mod = ModuleType(f"{pkg_name}._tool_view_{tool_name}")

    fn = tool.get("function", {}) if isinstance(tool, dict) else {}
    description = fn.get("description", "") if isinstance(fn, dict) else ""
    params_schema = fn.get("parameters") if isinstance(fn, dict) else None
    if not isinstance(params_schema, dict):
        params_schema = {"type": "object", "properties": {}, "required": []}

    def plan(params: dict, _tool: str = tool_name) -> list[dict]:
        if params is None:
            params = {}
        if not isinstance(params, dict):
            raise ValueError("View params must be a dict")
        return [{"key": _tool, "tool": _tool, "args": params}]

    mod.VIEW_NAME = tool_name
    mod.DESCRIPTION = description
    mod.PARAMS_SCHEMA = params_schema
    mod.plan = plan
    return mod


def discover_views(tool_index: dict[str, dict[str, Any]] | None = None) -> dict[str, ViewSpec]:
    """
    Discover views from python modules under `scripts/views/` and optionally
    auto-expose every AKShare tool as a 1:1 "tool view" (view name == tool name).

    Custom views take precedence: if a view module declares `VIEW_NAME` that
    matches a tool name, the tool view is skipped.
    """
    views: dict[str, ViewSpec] = {}
    pkg_name = __name__.rsplit(".", 1)[0]  # scripts.views

    pkg = importlib.import_module(pkg_name)
    for m in pkgutil.walk_packages(pkg.__path__, prefix=f"{pkg_name}."):
        if m.ispkg:
            continue
        leaf = m.name.rsplit(".", 1)[-1]
        if leaf.startswith("_") or leaf in {"registry"}:
            continue

        mod = importlib.import_module(m.name)

        view_name = getattr(mod, "VIEW_NAME", None) or leaf
        description = getattr(mod, "DESCRIPTION", "") or ""
        schema = getattr(mod, "PARAMS_SCHEMA", None) or {"type": "object", "properties": {}, "required": []}

        if not hasattr(mod, "plan") or not callable(getattr(mod, "plan")):
            continue

        if view_name in views:
            raise ValueError(
                f"Duplicate view name: {view_name!r} ({views[view_name].module.__name__} vs {m.name})"
            )

        views[view_name] = ViewSpec(
            name=view_name,
            description=description,
            params_schema=schema,
            module=mod,
        )

    if tool_index:
        for tool_name in sorted(tool_index.keys()):
            if tool_name in views:
                continue
            tool = tool_index.get(tool_name) or {}
            mod = _build_tool_view_module(tool_name, tool)
            views[tool_name] = ViewSpec(
                name=tool_name,
                description=getattr(mod, "DESCRIPTION", "") or "",
                params_schema=getattr(mod, "PARAMS_SCHEMA", None)
                or {"type": "object", "properties": {}, "required": []},
                module=mod,
            )

    return views
