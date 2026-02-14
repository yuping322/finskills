from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

from .provider_akshare import AkshareProvider
from .tool_registry import ToolRegistry
from .view_runner import run_view
from .views_cn import ViewSpec, discover_custom_views, build_tool_views


def _json_dumps(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_json_dumps(payload), encoding="utf-8")


def _prev_weekday(d: date) -> date:
    while d.weekday() >= 5:
        d = d - timedelta(days=1)
    return d


def _yyyymmdd(d: date) -> str:
    return d.strftime("%Y%m%d")


def _classify_error(err_text: str) -> tuple[str, str | None]:
    t = (err_text or "").strip()
    if not t:
        return "unknown_error", None
    lo = t.lower()

    if "no module named" in lo or "modulenotfounderror" in lo or "importerror" in lo:
        return "missing_dependency", None

    # AKShare occasionally raises when the upstream returned no rows (empty DataFrame then renamed).
    if "length mismatch: expected axis has 0 elements" in lo:
        return "empty", "no_data"

    if (
        "missing required parameter" in lo
        or "invalid value for" in lo
        or "got an unexpected keyword argument" in lo
        or "unexpected keyword argument" in lo
        or "cannot convert" in lo
        or "invalid --set value" in lo
    ):
        return "param_mismatch", None

    if "429" in lo or "too many requests" in lo or "rate limit" in lo or "频繁" in t:
        return "network_error", "rate_limited"

    network_markers = [
        "connection aborted",
        "remotedisconnected",
        "max retries exceeded",
        "read timed out",
        "timed out",
        "name resolution",
        "failed to resolve",
        "proxyerror",
        "connection refused",
        "unexpected eof",
        "ssleoferror",
        "ssl",
        "handshake",
        "network request failed",
        "curl:",
    ]
    if any(m in lo for m in network_markers):
        return "network_error", None

    if "no tables found" in lo:
        return "network_error", "parse_error"

    return "unknown_error", None


def _rows_cols(data: Any) -> tuple[int | None, list[str] | None]:
    if data is None:
        return None, None
    if isinstance(data, list):
        if not data:
            return 0, []
        if isinstance(data[0], dict):
            cols: list[str] = []
            for k in data[0].keys():
                cols.append(str(k))
            return len(data), cols
        return len(data), None
    if isinstance(data, dict):
        return len(data), list(map(str, data.keys()))
    return None, None


def _build_views(cn_toolkit_root: Path, registry: ToolRegistry) -> dict[str, ViewSpec]:
    custom = discover_custom_views(cn_toolkit_root / "scripts" / "views")
    tools = build_tool_views(sorted(registry.tool_index.keys()))
    merged = dict(tools)
    merged.update(custom)

    # Fill tool view schema/desc from registry.
    for name, spec in list(merged.items()):
        if spec.kind != "tool_view":
            continue
        fn = registry.describe(name) or {}
        desc = fn.get("description") if isinstance(fn, dict) else ""
        schema = fn.get("parameters") if isinstance(fn, dict) else None
        if not isinstance(schema, dict):
            schema = {"type": "object", "properties": {}, "required": []}
        merged[name] = ViewSpec(
            name=name,
            kind="tool_view",
            description=str(desc or ""),
            params_schema=schema,
            module=None,
        )

    return merged


@dataclass(frozen=True)
class Check:
    view: str
    params: dict[str, Any]
    min_rows: int | None = None


def _default_checks(today: date) -> list[Check]:
    d = _prev_weekday(today)
    end = d
    # Some daily datasets (notably margin financing) are typically published with a 1-trading-day lag.
    margin_d = _prev_weekday(d - timedelta(days=1))
    start_30 = d - timedelta(days=30)
    start_60 = d - timedelta(days=60)

    return [
        # 行情
        Check(view="stock_zh_a_spot_em", params={}, min_rows=1000),
        # 历史K（短区间避免慢）
        Check(
            view="stock_zh_a_hist",
            params={
                "symbol": "000001",
                "period": "daily",
                "start_date": _yyyymmdd(start_60),
                "end_date": _yyyymmdd(end),
                "adjust": "qfq",
            },
            min_rows=10,
        ),
        # 融资融券（核心三项）
        Check(view="stock_margin_ratio_pa", params={"date": _yyyymmdd(margin_d)}, min_rows=1),
        Check(
            view="stock_margin_sse",
            params={"start_date": _yyyymmdd(margin_d), "end_date": _yyyymmdd(margin_d)},
            min_rows=1,
        ),
        Check(view="stock_margin_szse", params={"date": _yyyymmdd(margin_d)}, min_rows=1),
        # 回购
        Check(view="stock_repurchase_em", params={}, min_rows=1),
        # 大宗交易
        Check(view="stock_dzjy_sctj", params={}, min_rows=1),
        Check(view="stock_dzjy_mrtj", params={"start_date": _yyyymmdd(start_30), "end_date": _yyyymmdd(end)}, min_rows=1),
        Check(
            view="stock_dzjy_mrmx",
            params={"symbol": "A股", "start_date": _yyyymmdd(start_30), "end_date": _yyyymmdd(end)},
            min_rows=1,
        ),
    ]


def main() -> int:
    p = argparse.ArgumentParser(description="Healthcheck: run key CN primitive views with real data fetching")
    p.add_argument("--repo-root", default=".", help="Repo root (default: .)")
    p.add_argument("--cn-toolkit-root", default="China-market/findata-toolkit-cn")
    p.add_argument("--out-json", default="", help="Write JSON report to path")
    p.add_argument("--refresh", action="store_true", help="Bypass cache (if provider supports)")
    p.add_argument("--only", action="append", default=[], help="Only run these views (repeatable)")
    args = p.parse_args()

    # Ensure we're not in smoke mode.
    os.environ.pop("FINSKILLS_SMOKE", None)

    repo_root = Path(args.repo_root).resolve()
    cn_root = (repo_root / args.cn_toolkit_root).resolve()
    tools_json = cn_root / "config" / "litellm_tools.json"

    registry = ToolRegistry.load(tools_json)
    provider = AkshareProvider(registry=registry)
    views = _build_views(cn_root, registry)

    checks = _default_checks(date.today())
    if args.only:
        allow = set(str(x).strip() for x in args.only if str(x).strip())
        checks = [c for c in checks if c.view in allow]

    results: list[dict[str, Any]] = []
    failures = 0

    started = datetime.now()
    for c in checks:
        spec = views.get(c.view)
        if not spec:
            failures += 1
            results.append(
                {
                    "view": c.view,
                    "ok": False,
                    "category": "param_mismatch",
                    "subcategory": None,
                    "error": f"Unknown view: {c.view}",
                    "params": c.params,
                }
            )
            continue

        out = run_view(spec, params=c.params, provider=provider, refresh=bool(args.refresh))
        env = out.data.get(c.view) if isinstance(out.data, dict) else None
        env_data = env.get("data") if isinstance(env, dict) else None
        env_meta = env.get("meta") if isinstance(env, dict) else None
        env_errs = env.get("errors") if isinstance(env, dict) else None
        env_errs_list = env_errs if isinstance(env_errs, list) else []

        rows, cols = _rows_cols(env_data)

        error_text = ""
        if out.errors:
            error_text = "; ".join(str(e) for e in out.errors)
        elif env_errs_list:
            error_text = "; ".join(str(e) for e in env_errs_list)

        provider_name = None
        backend = None
        if isinstance(env_meta, dict):
            provider_name = env_meta.get("provider") or env_meta.get("tool") or None
            backend = env_meta.get("backend") or None

        ok = True
        category = "ok"
        subcategory = None

        if error_text:
            ok = False
            category, subcategory = _classify_error(error_text)
        else:
            # Treat stubbed results as not "real fetching".
            if str(provider_name or "").lower() in {"fallback", "smoke_stub"} or "stub" in str(backend or "").lower():
                ok = False
                category = "empty"
                subcategory = "stubbed"
                error_text = "Result produced by stub/fallback backend (not real fetching)"
            else:
                # Empty/insufficient rows is a failure category for healthcheck.
                if rows is None:
                    ok = False
                    category = "empty"
                    error_text = "No tabular data returned"
                elif c.min_rows is not None and rows < c.min_rows:
                    ok = False
                    category = "empty"
                    error_text = f"Too few rows: {rows} < {c.min_rows}"

        if not ok:
            failures += 1

        results.append(
            {
                "view": c.view,
                "ok": ok,
                "category": category,
                "subcategory": subcategory,
                "error": error_text or None,
                "params": c.params,
                "provider": provider_name,
                "backend": backend,
                "rows": rows,
                "columns": cols,
                "meta": env_meta,
            }
        )

    ended = datetime.now()
    payload: dict[str, Any] = {
        "meta": {
            "tool": "view-service",
            "kind": "healthcheck",
            "as_of": ended.isoformat(timespec="seconds"),
            "elapsed_seconds": round((ended - started).total_seconds(), 3),
            "python": sys.version.split()[0],
        },
        "checks": results,
        "failures": failures,
    }

    if args.out_json:
        _write_json(Path(args.out_json).expanduser().resolve(), payload)

    # Human-readable summary
    if failures:
        print(f"FAIL ({failures}/{len(results)} failed)")
        for r in results:
            if r.get("ok"):
                continue
            print(f"- {r['view']}: {r.get('category')}" + (f"/{r.get('subcategory')}" if r.get("subcategory") else ""))
            if r.get("error"):
                print(f"  {r['error']}")
    else:
        print(f"OK ({len(results)} checks)")

    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
