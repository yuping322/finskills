from __future__ import annotations

import importlib
import pkgutil
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any


@dataclass(frozen=True)
class ViewSpec:
    name: str
    kind: str  # "tool_view" | "custom_view"
    description: str
    params_schema: dict[str, Any]
    module: ModuleType | None


def discover_custom_views(views_dir: Path) -> dict[str, ViewSpec]:
    """
    Discover custom views from `China-market/findata-toolkit-cn/scripts/views/*.py`.
    """
    views_dir = views_dir.resolve()
    if not views_dir.exists():
        raise FileNotFoundError(f"views_dir not found: {views_dir}")

    out: dict[str, ViewSpec] = {}

    scripts_dir = views_dir.parent  # .../scripts
    sys.path.insert(0, str(scripts_dir))

    pkg = importlib.import_module("views")
    for m in pkgutil.walk_packages(pkg.__path__, prefix="views."):
        if m.ispkg:
            continue
        leaf = m.name.rsplit(".", 1)[-1]
        if leaf.startswith("_") or leaf in {"registry"}:
            continue
        mod = importlib.import_module(m.name)

        view_name = getattr(mod, "VIEW_NAME", None) or leaf
        if not isinstance(view_name, str) or not view_name:
            continue
        if not hasattr(mod, "plan") or not callable(getattr(mod, "plan")):
            continue

        description = getattr(mod, "DESCRIPTION", "") or ""
        schema = getattr(mod, "PARAMS_SCHEMA", None) or {"type": "object", "properties": {}, "required": []}
        if not isinstance(schema, dict):
            schema = {"type": "object", "properties": {}, "required": []}

        if view_name in out:
            raise ValueError(f"Duplicate view name: {view_name!r}")

        out[view_name] = ViewSpec(
            name=view_name,
            kind="custom_view",
            description=str(description),
            params_schema=schema,
            module=mod,
        )

    return out


def build_tool_views(tool_names: list[str]) -> dict[str, ViewSpec]:
    """
    Tool view: 1:1 mapping. Plan is implicit (call tool with params as args).
    """
    out: dict[str, ViewSpec] = {}
    for name in tool_names:
        out[name] = ViewSpec(
            name=name,
            kind="tool_view",
            description="",
            params_schema={"type": "object", "properties": {}, "required": []},
            module=None,
        )
    return out
