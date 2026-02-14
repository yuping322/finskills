"""
AKShare tool runner (shared library).

This module powers:
- `scripts/akshare_tools.py` (generic CLI for 356 tools)
- view layer scripts that compose multiple tools into stable views

It relies on `config/litellm_tools.json` as the tool registry.
"""

from __future__ import annotations

import inspect
import os
import time
from datetime import datetime
from typing import Any

from .cache import CacheManager
from .litellm_tools import build_tool_index, load_tools_config


def _is_pseudo_optional(param_name: str, param_schema: dict[str, Any] | None) -> bool:
    if param_name in {"timeout", "token"}:
        return True
    if not param_schema:
        return False
    desc = str(param_schema.get("description", "")).lower()
    # Many schemas mark these as required even though they default to None.
    return "none" in desc or ("默认" in desc and "不设置" in desc)


def _to_bool(val: Any) -> bool:
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        return bool(val)
    if isinstance(val, str):
        v = val.strip().lower()
        if v in {"true", "1", "yes", "y"}:
            return True
        if v in {"false", "0", "no", "n"}:
            return False
    raise ValueError(f"Cannot convert to boolean: {val!r}")


def validate_and_convert_parameters(
    tool_name: str,
    tool_index: dict[str, dict[str, Any]],
    arguments: dict[str, Any],
) -> dict[str, Any]:
    tool = tool_index.get(tool_name)
    if not tool:
        raise ValueError(f"Unknown tool: {tool_name}")

    params = tool.get("function", {}).get("parameters", {}) if isinstance(tool, dict) else {}
    properties = params.get("properties", {}) if isinstance(params, dict) else {}
    required = params.get("required", []) if isinstance(params, dict) else []

    # Auto-fill common env-based defaults.
    if "token" in properties and ("token" not in arguments or arguments.get("token") is None):
        env_token = os.getenv("XUEQIU_TOKEN")
        if env_token:
            arguments["token"] = env_token

    # Validate required parameters (with pseudo-optional exceptions).
    for param_name in required:
        if param_name in arguments and arguments[param_name] is not None:
            continue
        if _is_pseudo_optional(param_name, properties.get(param_name)):
            arguments[param_name] = None
            continue
        raise ValueError(f"Missing required parameter: {param_name}")

    converted: dict[str, Any] = {}
    for param_name, param_value in arguments.items():
        schema = properties.get(param_name, {}) if isinstance(properties, dict) else {}
        if param_value is None:
            converted[param_name] = None
            continue

        # Treat placeholder strings as None for compatibility with some schemas.
        if isinstance(param_value, str) and param_value.strip().lower() in {"timeout", "token", "none", "null"}:
            converted[param_name] = None
            continue

        typ = schema.get("type")
        enum = schema.get("enum")

        try:
            if typ == "string" or typ is None:
                value = str(param_value)
            elif typ == "integer":
                value = int(param_value)
            elif typ == "number":
                value = float(param_value)
            elif typ == "boolean":
                value = _to_bool(param_value)
            elif typ == "array":
                if isinstance(param_value, str):
                    import json

                    pv = param_value.strip()
                    if pv.startswith("["):
                        value = json.loads(pv)
                    else:
                        value = [s for s in pv.split(",") if s]
                else:
                    value = list(param_value)
            elif typ == "object":
                if isinstance(param_value, str):
                    import json

                    value = json.loads(param_value)
                else:
                    value = dict(param_value)
            else:
                value = param_value
        except Exception as e:
            raise ValueError(f"Failed to convert parameter {param_name} to {typ}: {e}") from e

        if enum is not None and value not in enum:
            raise ValueError(f"Invalid value for {param_name}: {value!r}; allowed: {enum}")

        converted[param_name] = value

    return converted


def _filter_kwargs(func, kwargs: dict[str, Any]) -> dict[str, Any]:
    try:
        sig = inspect.signature(func)
    except Exception:
        return kwargs

    accepts_kwargs = any(p.kind == p.VAR_KEYWORD for p in sig.parameters.values())
    if accepts_kwargs:
        return kwargs
    allowed = set(sig.parameters.keys())
    return {k: v for k, v in kwargs.items() if k in allowed}


def _normalize_result(result: Any) -> Any:
    try:
        import pandas as pd

        if isinstance(result, pd.DataFrame):
            return result.to_dict(orient="records")
        if isinstance(result, pd.Series):
            return result.to_dict()
    except Exception:
        pass

    return result


def load_tool_index(tools_json_path=None) -> dict[str, dict[str, Any]]:
    tools_cfg = load_tools_config(tools_json_path)
    return build_tool_index(tools_cfg)


def list_tools(
    tool_index: dict[str, dict[str, Any]],
    *,
    prefix: str = "",
    contains: str = "",
) -> list[str]:
    names = sorted(tool_index.keys())
    if prefix:
        names = [n for n in names if n.startswith(prefix)]
    if contains:
        names = [n for n in names if contains in n]
    return names


def describe_tool(tool_index: dict[str, dict[str, Any]], name: str) -> dict[str, Any] | None:
    tool = tool_index.get(name)
    if not tool:
        return None
    return tool.get("function", {})


def call_tool(
    tool_name: str,
    tool_index: dict[str, dict[str, Any]],
    arguments: dict[str, Any],
    *,
    cache: CacheManager | None,
    refresh: bool,
    meta_script: str,
) -> dict[str, Any]:
    try:
        import akshare as ak
    except ImportError as e:
        raise ImportError(
            "Missing dependency: 'akshare'. Install toolkit deps first (from repo root): "
            "pip install -r China-market/findata-toolkit-cn/requirements.txt"
        ) from e

    tool = tool_index.get(tool_name)
    if not tool:
        raise ValueError(f"Unknown tool: {tool_name}")

    converted = validate_and_convert_parameters(tool_name, tool_index, dict(arguments))

    func = getattr(ak, tool_name, None)
    if func is None:
        raise ValueError(f"akshare has no attribute {tool_name!r}")

    call_kwargs = _filter_kwargs(func, converted)

    ttl = cache.get_ttl(tool_name) if cache else 0
    cache_key = cache.get_cache_key(tool_name, call_kwargs) if cache else ""
    if cache and not refresh:
        cached = cache.load(cache_key, ttl)
        if cached and isinstance(cached, dict) and "result" in cached:
            payload = cached.get("result")
            age = time.time() - float(cached.get("timestamp", 0))
            if isinstance(payload, dict) and isinstance(payload.get("meta"), dict):
                payload["meta"]["cache"] = {
                    "hit": True,
                    "ttl_seconds": ttl,
                    "age_seconds": round(age, 3),
                }
            return payload if isinstance(payload, dict) else {
                "meta": {"function": tool_name, "cache": {"hit": True}},
                "data": payload,
                "warnings": [],
                "errors": [],
            }

    started = time.time()
    raw: Any = None
    try:
        raw = func(**call_kwargs)
        data = _normalize_result(raw)
        errors: list[str] = []
    except Exception as e:
        data = None
        errors = [str(e)]

    elapsed = time.time() - started

    warnings: list[str] = []
    result_meta: dict[str, Any] = {}
    if not errors:
        try:
            import pandas as pd

            if isinstance(raw, pd.DataFrame):
                result_meta["type"] = "dataframe"
                result_meta["rows"] = int(raw.shape[0])
                result_meta["columns"] = [str(c) for c in raw.columns]
                if raw.empty:
                    warnings.append("Empty DataFrame result")
            elif isinstance(raw, pd.Series):
                result_meta["type"] = "series"
                result_meta["rows"] = int(raw.shape[0])
                if raw.empty:
                    warnings.append("Empty Series result")
        except Exception:
            # Pandas may not be available or raw is not a pandas object.
            pass

        if not result_meta:
            if data is None:
                result_meta["type"] = "none"
                warnings.append("Tool returned null/None result")
            elif isinstance(data, list):
                result_meta["type"] = "list"
                result_meta["rows"] = len(data)
                if not data:
                    warnings.append("Empty list result")
            elif isinstance(data, dict):
                result_meta["type"] = "dict"
                result_meta["keys"] = len(data)
                if not data:
                    warnings.append("Empty dict result")
            else:
                result_meta["type"] = type(data).__name__

    envelope: dict[str, Any] = {
        "meta": {
            "tool": "findata-toolkit-cn",
            "script": meta_script,
            "function": tool_name,
            "description": tool.get("function", {}).get("description", ""),
            "as_of": datetime.now().isoformat(timespec="seconds"),
            "elapsed_seconds": round(elapsed, 3),
            "params": call_kwargs,
            "cache": {
                "hit": False if cache else None,
                "ttl_seconds": ttl if cache else None,
            },
            "result": result_meta,
        },
        "data": data,
        "warnings": warnings,
        "errors": errors,
    }

    if cache and not errors:
        try:
            cache.save(cache_key, envelope)
        except Exception:
            pass

    return envelope
