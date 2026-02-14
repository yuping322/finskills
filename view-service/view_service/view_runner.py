from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .provider_base import ToolProvider
from .views_cn import ViewSpec


@dataclass(frozen=True)
class ViewResult:
    meta: dict[str, Any]
    data: dict[str, Any]
    warnings: list[str]
    errors: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {"meta": self.meta, "data": self.data, "warnings": self.warnings, "errors": self.errors}


def run_view(
    spec: ViewSpec,
    *,
    params: dict[str, Any] | None,
    provider: ToolProvider,
    refresh: bool,
) -> ViewResult:
    params = params or {}
    started = time.time()

    errors: list[str] = []
    warnings: list[str] = []
    data: dict[str, Any] = {}

    if spec.kind == "tool_view":
        try:
            res = provider.call_tool(spec.name, params, refresh=refresh, meta_script=f"view:{spec.name}")
            data[spec.name] = res.to_dict()
            errors.extend(res.errors)
        except Exception as e:
            errors.append(str(e))
            data[spec.name] = {"meta": {"function": spec.name}, "data": None, "warnings": [], "errors": [str(e)]}

    elif spec.kind == "custom_view":
        if not spec.module or not hasattr(spec.module, "plan"):
            errors.append(f"Invalid custom view module for {spec.name}")
        else:
            try:
                plan = spec.module.plan(params)  # type: ignore[attr-defined]
            except Exception as e:
                errors.append(f"Failed to build view plan: {e}")
                plan = []

            if not isinstance(plan, list):
                errors.append("View plan must be a list")
                plan = []

            for call in plan:
                if not isinstance(call, dict):
                    errors.append(f"Invalid plan item: {call!r}")
                    continue
                key = str(call.get("key") or call.get("tool") or "result")
                tool = call.get("tool")
                tool_args = call.get("args", {}) or {}
                if not isinstance(tool, str) or not tool:
                    errors.append(f"Invalid plan item (missing tool): {call!r}")
                    continue
                if not isinstance(tool_args, dict):
                    errors.append(f"Invalid plan item args for {tool}: must be dict")
                    tool_args = {}

                try:
                    res = provider.call_tool(tool, tool_args, refresh=refresh, meta_script=f"view:{spec.name}")
                    data[key] = res.to_dict()
                    for err in res.errors:
                        errors.append(f"{tool}: {err}")
                except Exception as e:
                    data[key] = {"meta": {"function": tool}, "data": None, "warnings": [], "errors": [str(e)]}
                    errors.append(f"{tool}: {e}")
    else:
        errors.append(f"Unknown view kind: {spec.kind}")

    elapsed = time.time() - started
    meta = {
        "layer": "views",
        "view": spec.name,
        "as_of": datetime.now().isoformat(timespec="seconds"),
        "elapsed_seconds": round(elapsed, 3),
        "params": params,
    }
    return ViewResult(meta=meta, data=data, warnings=warnings, errors=errors)

