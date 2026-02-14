#!/usr/bin/env python3
"""
Views runner (CN toolkit)
========================

Views compose multiple AKShare tools (from `config/litellm_tools.json`) into
stable, higher-level datasets.

Examples:
  python scripts/views_runner.py list
  python scripts/views_runner.py describe fund_flow_dashboard
  python scripts/views_runner.py fund_flow_dashboard
  python scripts/views_runner.py stock_zh_a_spot_em  # tool view (view name == tool name)
  python scripts/views_runner.py limit_up_pool_daily --set date=20241008
  python scripts/views_runner.py dragon_tiger_daily --set date=20250211 --dry-run
  FINSKILLS_VIEW_API_URL=http://127.0.0.1:8808 python scripts/views_runner.py list
  python scripts/views_runner.py --remote-url http://127.0.0.1:8808 repurchase_dashboard --set symbol=000001
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib import error as urllib_error
from urllib import parse as urllib_parse
from urllib import request as urllib_request

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from common.akshare_runner import call_tool, load_tool_index  # noqa: E402
from common.cache import CacheManager  # noqa: E402
from common.utils import error_exit, output_json  # noqa: E402
from views._helpers import view_envelope  # noqa: E402
from views.registry import discover_views  # noqa: E402


def _parse_set_kv(pairs: list[str]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for p in pairs:
        if "=" not in p:
            raise ValueError(f"Invalid --set value: {p!r} (expected key=value)")
        k, v = p.split("=", 1)
        k = k.strip()
        v = v.strip()
        if not k:
            raise ValueError(f"Invalid --set value: {p!r} (empty key)")
        if v.lower() in {"none", "null"}:
            out[k] = None
            continue
        if v and v[0] in "[{\"":
            try:
                out[k] = json.loads(v)
                continue
            except Exception:
                pass
        # Preserve strings with leading zeros (common for stock codes like 000001).
        if v.isdigit() and len(v) > 1 and v.startswith("0"):
            out[k] = v
            continue
        try:
            if "." in v:
                out[k] = float(v)
            else:
                out[k] = int(v)
            continue
        except Exception:
            pass
        out[k] = v
    return out


def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--tools-json", default="", help="Override tools json path")
    common.add_argument(
        "--remote-url",
        default="",
        help="Remote View API base URL (or set FINSKILLS_VIEW_API_URL)",
    )
    common.add_argument("--no-cache", action="store_true", help="Disable file cache")
    common.add_argument("--refresh", action="store_true", help="Bypass cache and refresh data")
    common.add_argument("--dry-run", action="store_true", help="Print planned tool calls without executing")
    common.add_argument("--pretty", action="store_true", default=True, help="Pretty-print JSON (default)")
    common.add_argument("--no-pretty", action="store_false", dest="pretty", help="Minify JSON output")

    p = argparse.ArgumentParser(description="Run FinSkills views", parents=[common])
    sub = p.add_subparsers(dest="cmd")

    sp_list = sub.add_parser("list", help="List available views", parents=[common])
    sp_list.add_argument("--contains", default="", help="Filter: substring")
    sp_list.add_argument("--prefix", default="", help="Filter: prefix")

    sp_desc = sub.add_parser("describe", help="Describe a view", parents=[common])
    sp_desc.add_argument("name")

    sp_run = sub.add_parser("run", help="Run a view", parents=[common])
    sp_run.add_argument("name")
    sp_run.add_argument("--args", default="", help="JSON dict string for view parameters")
    sp_run.add_argument("--set", action="append", default=[], help="Set parameter: key=value (repeatable)")

    return p


def _resolve_view_name(views: dict[str, Any], name: str) -> str | None:
    if name in views:
        return name
    alt = name.replace("-", "_")
    if alt in views:
        return alt
    return None


def _remote_base_url(cli_url: str) -> str | None:
    url = (cli_url or "").strip() or (os.getenv("FINSKILLS_VIEW_API_URL") or "").strip()
    if not url:
        return None
    return url.rstrip("/")


def _remote_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "finskills-views-runner/remote",
    }
    token = (os.getenv("FINSKILLS_VIEW_API_TOKEN") or "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
        return headers
    api_key = (os.getenv("FINSKILLS_VIEW_API_KEY") or "").strip()
    if api_key:
        headers["X-API-Key"] = api_key
    return headers


def _remote_timeout_seconds() -> float:
    raw = (os.getenv("FINSKILLS_VIEW_API_TIMEOUT") or "").strip()
    if not raw:
        return 30.0
    try:
        return float(raw)
    except Exception:
        return 30.0


def _remote_request_json(method: str, url: str, *, body: dict[str, Any] | None) -> tuple[int, Any]:
    data = None
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib_request.Request(url, data=data, method=method, headers=_remote_headers())
    timeout = _remote_timeout_seconds()
    try:
        with urllib_request.urlopen(req, timeout=timeout) as resp:
            status = int(getattr(resp, "status", 200))
            raw = resp.read().decode("utf-8", errors="replace")
    except urllib_error.HTTPError as e:
        status = int(getattr(e, "code", 500) or 500)
        try:
            raw = e.read().decode("utf-8", errors="replace")
        except Exception:
            raw = ""
    except urllib_error.URLError as e:
        raise RuntimeError(f"Remote request failed: {e}") from e

    if not raw:
        return status, None
    try:
        return status, json.loads(raw)
    except Exception:
        return status, {"error": raw}


def _remote_try_names(name: str) -> list[str]:
    candidates = [name]
    alt = name.replace("-", "_")
    if alt != name:
        candidates.append(alt)
    alt2 = name.replace("_", "-")
    if alt2 != name and alt2 not in candidates:
        candidates.append(alt2)
    # Keep order, de-dup.
    out: list[str] = []
    for c in candidates:
        if c and c not in out:
            out.append(c)
    return out


def main(argv: list[str]) -> int:
    known_cmds = {"list", "describe", "run"}
    if len(argv) > 1 and not argv[1].startswith("-") and argv[1] not in known_cmds:
        argv = [argv[0], "run", *argv[1:]]

    parser = build_parser()
    args = parser.parse_args(argv[1:])

    remote_url = _remote_base_url(args.remote_url)
    if remote_url:
        try:
            if args.cmd == "list":
                q: dict[str, str] = {}
                if args.contains:
                    q["contains"] = str(args.contains)
                if args.prefix:
                    q["prefix"] = str(args.prefix)
                url = f"{remote_url}/views"
                if q:
                    url = f"{url}?{urllib_parse.urlencode(q)}"
                status, payload = _remote_request_json("GET", url, body=None)
                if status >= 400:
                    output_json(payload, pretty=args.pretty)
                    return 1
                output_json(payload, pretty=args.pretty)
                return 0

            if args.cmd == "describe":
                last_payload: Any = None
                for candidate in _remote_try_names(args.name):
                    status, payload = _remote_request_json("GET", f"{remote_url}/views/{candidate}", body=None)
                    last_payload = payload
                    if status == 404:
                        continue
                    if status >= 400:
                        output_json(payload, pretty=args.pretty)
                        return 1
                    output_json(payload, pretty=args.pretty)
                    return 0
                output_json(last_payload or {"error": f"Unknown view: {args.name}"}, pretty=args.pretty)
                return 1

            if args.cmd != "run":
                parser.print_help()
                return 0

            if args.dry_run:
                error_exit("--dry-run is not supported in remote mode (remote API does not expose plans)")
                return 1

            params: dict[str, Any] = {}
            if args.args:
                try:
                    params.update(json.loads(args.args))
                except Exception as e:
                    error_exit(f"Invalid --args JSON: {e}")
                    return 1
            if args.set:
                try:
                    params.update(_parse_set_kv(args.set))
                except Exception as e:
                    error_exit(str(e))
                    return 1

            last_payload = None
            for candidate in _remote_try_names(args.name):
                status, payload = _remote_request_json(
                    "POST",
                    f"{remote_url}/run",
                    body={"name": candidate, "params": params, "refresh": bool(args.refresh)},
                )
                last_payload = payload
                if status == 404:
                    # Unknown view - try alternate name mappings.
                    continue
                if status >= 400:
                    output_json(payload, pretty=args.pretty)
                    return 1
                output_json(payload, pretty=args.pretty)
                return 0

            output_json(last_payload or {"error": f"Unknown view: {args.name}"}, pretty=args.pretty)
            return 1
        except Exception as e:
            error_exit(str(e))
            return 1

    tools_path = Path(args.tools_json).expanduser() if args.tools_json else None
    try:
        tool_index = load_tool_index(tools_path)
    except Exception as e:
        error_exit(f"Failed to load tools config: {e}")
        return 1

    views = discover_views(tool_index)

    if args.cmd == "list":
        names = sorted(views.keys())
        if args.prefix:
            names = [n for n in names if n.startswith(args.prefix)]
        if args.contains:
            names = [n for n in names if args.contains in n]
        output_json(
            {
                "views": [
                    {"name": n, "description": views[n].description}
                    for n in names
                ],
                "count": len(names),
            },
            pretty=args.pretty,
        )
        return 0

    if args.cmd == "describe":
        resolved = _resolve_view_name(views, args.name)
        if not resolved:
            error_exit(f"Unknown view: {args.name}")
            return 1
        spec = views[resolved]
        output_json(
            {
                "name": spec.name,
                "description": spec.description,
                "params_schema": spec.params_schema,
            },
            pretty=args.pretty,
        )
        return 0

    if args.cmd != "run":
        parser.print_help()
        return 0

    resolved = _resolve_view_name(views, args.name)
    if not resolved:
        error_exit(f"Unknown view: {args.name}")
        return 1
    spec = views[resolved]

    params: dict[str, Any] = {}
    if args.args:
        try:
            params.update(json.loads(args.args))
        except Exception as e:
            error_exit(f"Invalid --args JSON: {e}")
            return 1
    if args.set:
        try:
            params.update(_parse_set_kv(args.set))
        except Exception as e:
            error_exit(str(e))
            return 1

    cache = None if args.no_cache else CacheManager()

    started = time.time()
    try:
        plan = spec.module.plan(params)
    except Exception as e:
        error_exit(f"Failed to build view plan: {e}")
        return 1

    if args.dry_run:
        output_json(
            {
                "view": spec.name,
                "params": params,
                "plan": plan,
            },
            pretty=args.pretty,
        )
        return 0

    results: dict[str, Any] = {}
    errors: list[str] = []
    warnings: list[str] = []

    for call in plan:
        key = call.get("key") or call.get("tool") or "result"
        tool = call.get("tool")
        tool_args = call.get("args", {}) or {}
        if not tool:
            errors.append(f"Invalid plan item (missing tool): {call}")
            continue

        try:
            res = call_tool(
                tool,
                tool_index,
                tool_args,
                cache=cache,
                refresh=args.refresh,
                meta_script=f"view:{spec.name}",
            )
        except Exception as e:
            tool_def = tool_index.get(tool) if isinstance(tool_index, dict) else None
            tool_desc = ""
            if isinstance(tool_def, dict):
                tool_desc = str((tool_def.get("function") or {}).get("description") or "")
            res = {
                "meta": {
                    "tool": "findata-toolkit-cn",
                    "script": f"view:{spec.name}",
                    "function": tool,
                    "description": tool_desc,
                    "as_of": datetime.now().isoformat(timespec="seconds"),
                    "elapsed_seconds": None,
                    "params": tool_args,
                    "cache": {"hit": None, "ttl_seconds": None},
                },
                "data": None,
                "warnings": [],
                "errors": [str(e)],
            }

        results[str(key)] = res
        for err in res.get("errors") or []:
            errors.append(f"{tool}: {err}")
        for warn in res.get("warnings") or []:
            warnings.append(f"{tool}: {warn}")

    elapsed = time.time() - started
    out = view_envelope(
        view=spec.name,
        params=params,
        data=results,
        errors=errors,
        warnings=warnings,
        elapsed_seconds=elapsed,
    )
    output_json(out, pretty=args.pretty)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
