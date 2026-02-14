#!/usr/bin/env python3
"""
AKShare tool runner (CN toolkit)
===============================

This script turns the `config/litellm_tools.json` registry into a usable CLI:

- List tools
- Show tool schema
- Call any AKShare function by tool name with validated arguments
- Optional file cache with TTL heuristics

Examples:
  python scripts/akshare_tools.py list --contains fund_flow
  python scripts/akshare_tools.py describe stock_zt_pool_em
  python scripts/akshare_tools.py stock_zh_a_spot_em
  python scripts/akshare_tools.py stock_individual_info_em --set symbol=000001
  python scripts/akshare_tools.py stock_zh_a_hist --args '{\"symbol\":\"000001\",\"period\":\"daily\",\"start_date\":\"20250101\",\"end_date\":\"20250201\",\"adjust\":\"qfq\"}'
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from common.cache import CacheManager  # noqa: E402
from common.akshare_runner import call_tool, describe_tool, list_tools, load_tool_index  # noqa: E402
from common.utils import error_exit, output_json  # noqa: E402


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
        # Best-effort parse for JSON literals and numbers.
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
    common.add_argument("--no-cache", action="store_true", help="Disable file cache")
    common.add_argument("--refresh", action="store_true", help="Bypass cache and refresh data")
    common.add_argument("--pretty", action="store_true", default=True, help="Pretty-print JSON (default)")
    common.add_argument("--no-pretty", action="store_false", dest="pretty", help="Minify JSON output")

    p = argparse.ArgumentParser(
        description="Run AKShare tools from litellm_tools.json",
        parents=[common],
    )

    sub = p.add_subparsers(dest="cmd")

    sp_list = sub.add_parser("list", help="List available tools", parents=[common])
    sp_list.add_argument("--contains", default="", help="Filter: substring")
    sp_list.add_argument("--prefix", default="", help="Filter: prefix")
    sp_list.add_argument("--limit", type=int, default=200, help="Max tools to print")

    sp_desc = sub.add_parser("describe", help="Show tool schema", parents=[common])
    sp_desc.add_argument("name")

    sp_call = sub.add_parser("call", help="Call a tool", parents=[common])
    sp_call.add_argument("name")
    sp_call.add_argument("--args", default="", help="JSON dict string for arguments")
    sp_call.add_argument("--set", action="append", default=[], help="Set argument: key=value (repeatable)")

    sub.add_parser("cache-stats", help="Show cache stats", parents=[common])
    sub.add_parser("cache-clear", help="Clear cache files", parents=[common])

    return p


def main(argv: list[str]) -> int:
    known_cmds = {"list", "describe", "call", "cache-stats", "cache-clear"}
    if len(argv) > 1 and not argv[1].startswith("-") and argv[1] not in known_cmds:
        argv = [argv[0], "call", *argv[1:]]

    parser = build_parser()
    args = parser.parse_args(argv[1:])

    tools_path = Path(args.tools_json).expanduser() if args.tools_json else None
    try:
        tool_index = load_tool_index(tools_path)
    except Exception as e:
        error_exit(f"Failed to load tools config: {e}")
        return 1

    cache = None if args.no_cache else CacheManager()

    if args.cmd == "list":
        names = list_tools(tool_index, prefix=args.prefix, contains=args.contains)
        output_json({"tools": names[: args.limit], "count": len(names)}, pretty=args.pretty)
        return 0

    if args.cmd == "describe":
        fn = describe_tool(tool_index, args.name)
        if not fn:
            error_exit(f"Unknown tool: {args.name}")
            return 1
        output_json(fn, pretty=args.pretty)
        return 0

    if args.cmd == "cache-stats":
        if not cache:
            output_json({"enabled": False}, pretty=args.pretty)
            return 0
        output_json(cache.stats(), pretty=args.pretty)
        return 0

    if args.cmd == "cache-clear":
        if not cache:
            output_json({"enabled": False, "cleared": 0}, pretty=args.pretty)
            return 0
        cleared = cache.clear()
        output_json({"enabled": True, "cleared": cleared, **cache.stats()}, pretty=args.pretty)
        return 0

    if args.cmd != "call":
        parser.print_help()
        return 0

    call_args: dict[str, Any] = {}
    if args.args:
        try:
            call_args.update(json.loads(args.args))
        except Exception as e:
            error_exit(f"Invalid --args JSON: {e}")
            return 1
    if args.set:
        try:
            call_args.update(_parse_set_kv(args.set))
        except Exception as e:
            error_exit(str(e))
            return 1

    try:
        result = call_tool(
            args.name,
            tool_index,
            call_args,
            cache=cache,
            refresh=args.refresh,
            meta_script="akshare_tools",
        )
    except Exception as e:
        error_exit(str(e))
        return 1

    output_json(result, pretty=args.pretty)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
