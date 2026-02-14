#!/usr/bin/env python3
"""
Generate per-skill `references/data-queries.md` with explicit data dependencies.

- China-market skills: prefer AKShare-backed views/tools (via findata-toolkit-cn).
- US-market skills: list shared scripts (yfinance / SEC EDGAR / FRED).

This script is deterministic and safe to run repeatedly.
"""

from __future__ import annotations

import re
import sys
import json
import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
CN_ROOT = REPO_ROOT / "China-market"
US_ROOT = REPO_ROOT / "US-market"
CN_TOOLKIT = CN_ROOT / "findata-toolkit-cn"
US_TOOLKIT = US_ROOT / "findata-toolkit"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _slug_tokens(s: str) -> list[str]:
    return [t for t in re.split(r"[^a-zA-Z0-9]+", (s or "").lower()) if t]


@dataclass(frozen=True)
class FrontMatter:
    name: str
    description: str


def _parse_frontmatter(md: str) -> FrontMatter:
    # Minimal YAML-frontmatter parser: only reads top-level "name:" and "description:".
    if not md.startswith("---"):
        return FrontMatter(name="", description="")
    parts = md.split("\n---\n", 1)
    if len(parts) != 2:
        return FrontMatter(name="", description="")
    fm = parts[0].strip().splitlines()[1:]
    name = ""
    description = ""
    for line in fm:
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        v = v.strip()
        if k == "name":
            name = v
        elif k == "description":
            description = v
    return FrontMatter(name=name, description=description)


def _md_code(cmds: str) -> str:
    return f"```bash\n{cmds.rstrip()}\n```\n"


def _md_table(rows: list[list[str]], headers: list[str]) -> str:
    def esc(cell: str) -> str:
        return (cell or "").replace("\n", "<br>").replace("|", "\\|")

    out = []
    out.append("| " + " | ".join(esc(h) for h in headers) + " |")
    out.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for r in rows:
        out.append("| " + " | ".join(esc(c) for c in r) + " |")
    return "\n".join(out) + "\n"


def _first_keys(d: dict[str, Any] | None, n: int) -> list[str]:
    if not isinstance(d, dict):
        return []
    keys = list(d.keys())
    return keys[:n]


def _schema_required(schema: dict[str, Any] | None) -> list[str]:
    if not isinstance(schema, dict):
        return []
    req = schema.get("required")
    if isinstance(req, list):
        return [str(x) for x in req]
    return []


def _schema_properties(schema: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(schema, dict):
        return {}
    props = schema.get("properties")
    return props if isinstance(props, dict) else {}


def _render_required_and_common(schema: dict[str, Any] | None, *, common: Iterable[str] = ()) -> str:
    req = [r for r in _schema_required(schema) if r not in {"timeout", "token"}]
    props = _schema_properties(schema)
    common = list(common)
    # Always treat these as pseudo-optional if present.
    for k in ("timeout", "token"):
        if k in props and k not in common:
            common.append(k)
    common = [c for c in common if c in props and c not in req]
    parts = []
    if req:
        parts.append("required: " + ", ".join(req))
    if common:
        parts.append("common: " + ", ".join(common))
    return "; ".join(parts) if parts else "-"


def _load_cn_views_and_tools() -> tuple[dict[str, Any], dict[str, Any]]:
    """
    Returns (tool_index, views) where:
      - tool_index: name -> full tool dict from litellm_tools.json
      - views: view_name -> ViewSpec (from toolkit registry)
    """
    sys.path.insert(0, str(CN_TOOLKIT / "scripts"))
    from common.litellm_tools import build_tool_index, load_tools_config  # type: ignore
    from views.registry import discover_views  # type: ignore

    tools_cfg = load_tools_config(None)
    tool_index = build_tool_index(tools_cfg)
    views = discover_views(tool_index)
    return tool_index, views


def _cn_sample_params(schema: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(schema, dict):
        return {}
    props = _schema_properties(schema)
    req = _schema_required(schema)
    out: dict[str, Any] = {}
    for k in req:
        ks = str(k)
        p = props.get(ks) if isinstance(props, dict) else None
        typ = (p or {}).get("type") if isinstance(p, dict) else None
        kl = ks.lower()
        if typ == "boolean":
            out[ks] = False
        elif typ == "integer":
            out[ks] = 0
        elif typ == "number":
            out[ks] = 0.0
        else:
            if "symbol" in kl:
                out[ks] = "000001"
            elif "date" in kl:
                out[ks] = "20250101"
            elif "flag" in kl:
                out[ks] = "default"
            else:
                out[ks] = "demo"
    return out


def _cn_custom_view_plan(view_spec: Any) -> list[dict[str, Any]]:
    mod = getattr(view_spec, "module", None)
    if not mod:
        return []
    plan_fn = getattr(mod, "plan", None)
    if not callable(plan_fn):
        return []
    view_name = str(getattr(view_spec, "name", "") or "")
    try:
        base = plan_fn({}) or []
    except Exception:
        # Retry with minimal sample params for views that require inputs.
        schema = getattr(view_spec, "params_schema", None)
        try:
            sample = _cn_sample_params(schema)
            return plan_fn(sample) or []
        except Exception:
            return []

    # Some views have useful optional branches; prefer a plan that reveals them.
    if view_name == "repurchase_dashboard":
        try:
            enriched = plan_fn({"symbol": "000001"}) or []
            if len(enriched) > len(base):
                return enriched
        except Exception:
            pass

    return base


def _cn_is_tool_view(view_spec: Any) -> bool:
    mod = getattr(view_spec, "module", None)
    mod_name = getattr(mod, "__name__", "") if mod else ""
    return "._tool_view_" in mod_name


def _cn_view_spec_to_json(*, name: str, view_spec: Any, tool_index: dict[str, Any]) -> dict[str, Any]:
    schema = getattr(view_spec, "params_schema", None)
    description = getattr(view_spec, "description", "") or ""

    if _cn_is_tool_view(view_spec):
        tool = _cn_tool_def(tool_index, name) or {}
        fn = tool.get("function") or {}
        extra = tool.get("extra") or {}
        return {
            "name": name,
            "kind": "tool_view",
            "description": description or str(fn.get("description") or ""),
            "params_schema": schema if isinstance(schema, dict) else {"type": "object", "properties": {}, "required": []},
            "tool": {"function": fn, "extra": extra},
        }

    plan = _cn_custom_view_plan(view_spec)
    deps: list[str] = []
    for c in plan:
        if isinstance(c, dict) and c.get("tool"):
            deps.append(str(c.get("tool")))
    deps = [d for i, d in enumerate(deps) if d and d not in deps[:i]]

    return {
        "name": name,
        "kind": "custom_view",
        "description": description,
        "params_schema": schema if isinstance(schema, dict) else {"type": "object", "properties": {}, "required": []},
        "plan": plan,
        "depends_on": deps,
    }


def _cn_tool_def(tool_index: dict[str, Any], tool_name: str) -> dict[str, Any] | None:
    tool = tool_index.get(tool_name)
    return tool if isinstance(tool, dict) else None


def _cn_tool_row(tool_index: dict[str, Any], tool_name: str) -> list[str]:
    tool = _cn_tool_def(tool_index, tool_name) or {}
    fn = tool.get("function") or {}
    extra = tool.get("extra") or {}
    params = fn.get("parameters") if isinstance(fn, dict) else None
    output = extra.get("output") if isinstance(extra, dict) else None
    key_fields = _first_keys(output if isinstance(output, dict) else None, 10)
    return [
        tool_name,
        str(fn.get("description") or "-"),
        _render_required_and_common(params, common=("symbol", "date", "start_date", "end_date", "period", "adjust")),
        ", ".join(key_fields) if key_fields else "(columns as-is)",
    ]


def _cn_skill_dependencies(skill_dir: str) -> dict[str, Any]:
    """
    Returns a structured dependency spec with:
      - views: list[str]   (includes both custom views and tool-views)
      - notes: list[str]
    """
    s = skill_dir
    tokens = set(_slug_tokens(s))
    out: dict[str, Any] = {"views": [], "tools": [], "notes": []}

    custom_map: dict[str, list[str]] = {
        "ab-ah-premium-monitor": ["ab_ah_premium_dashboard"],
        "block-deal-monitor": ["block_deal_dashboard"],
        "bse-selection-analyzer": ["stock_info_bj_name_code", "stock_bj_a_spot_em", "stock_zcfz_bj_em", "stock_zh_a_hist"],
        "concept-board-analyzer": ["concept_board_snapshot", "concept_board_detail"],
        "disclosure-notice-monitor": ["notice_daily_dashboard", "cninfo_disclosure_search", "cninfo_disclosure_relation_search"],
        "dividend-corporate-action-tracker": ["dividend_actions_dashboard"],
        "dragon-tiger-list-analyzer": ["dragon_tiger_daily", "dragon_tiger_stock_detail"],
        "equity-pledge-risk-monitor": ["equity_pledge_dashboard"],
        "fund-flow-monitor": ["fund_flow_dashboard"],
        "goodwill-risk-monitor": ["goodwill_dashboard"],
        "hot-rank-sentiment-monitor": ["hot_rank_sentiment_dashboard"],
        "hsgt-holdings-monitor": ["hsgt_dashboard"],
        "industry-board-analyzer": ["industry_board_snapshot", "industry_board_detail"],
        "intraday-microstructure-analyzer": ["intraday_microstructure_dashboard"],
        "ipo-lockup-risk-monitor": ["restricted_release_dashboard"],
        "ipo-newlist-monitor": ["ipo_newlist_dashboard"],
        "limit-up-pool-analyzer": ["limit_up_pool_daily"],
        "margin-risk-monitor": ["margin_dashboard"],
        "market-overview-dashboard": ["market_overview_dashboard"],
        "share-repurchase-monitor": ["repurchase_dashboard"],
        "shareholder-structure-monitor": ["shareholder_structure_dashboard"],
        "st-delist-risk-scanner": ["st_delist_dashboard"],
    }
    if s in custom_map:
        out["views"].extend(custom_map[s])

    # Category tool dependencies.
    if "undervalued" in tokens or "screener" in tokens or "small" in tokens or "growth" in tokens:
        out["tools"].extend(["stock_zh_a_spot_em", "stock_a_indicator_lg", "stock_financial_abstract_ths"])

    if "financial" in tokens or "statement" in tokens:
        out["tools"].extend(
            [
                "stock_financial_abstract_ths",
                "stock_financial_analysis_indicator",
                "stock_balance_sheet_by_report_em",
                "stock_profit_sheet_by_report_em",
                "stock_cash_flow_sheet_by_report_em",
            ]
        )

    if "esg" in tokens:
        out["tools"].extend(
            [
                "stock_esg_rate_sina",
                "stock_esg_msci_sina",
                "stock_esg_rft_sina",
                "stock_esg_zd_sina",
                "stock_esg_hz_sina",
            ]
        )

    if "insider" in tokens or "trading" in tokens:
        out["tools"].extend(["stock_ggcg_em", "stock_inner_trade_xq", "stock_shareholder_change_ths"])

    if "northbound" in tokens or "hsgt" in tokens:
        out["views"].append("hsgt_dashboard")
        out["tools"].extend(["stock_hsgt_fund_flow_summary_em", "stock_hsgt_hold_stock_em"])

    if "margin" in tokens:
        out["views"].append("margin_dashboard")

    if "pledge" in tokens:
        out["views"].append("equity_pledge_dashboard")
        out["tools"].extend(["stock_gpzy_pledge_ratio_em", "stock_gpzy_pledge_ratio_detail_em"])

    if "dividend" in tokens:
        out["views"].append("dividend_actions_dashboard")
        out["tools"].extend(["stock_history_dividend", "stock_history_dividend_detail", "stock_dividend_cninfo"])

    if "ipo" in tokens and "newlist" not in tokens and "lockup" not in tokens:
        out["tools"].extend(["stock_ipo_info", "stock_ipo_declare", "stock_new_ipo_cninfo"])

    if "lockup" in tokens or "restricted" in tokens:
        out["views"].append("restricted_release_dashboard")
        out["tools"].extend(
            [
                "stock_restricted_release_summary_em",
                "stock_restricted_release_detail_em",
                "stock_restricted_release_stockholder_em",
            ]
        )

    if "valuation" in tokens and "regime" in tokens:
        out["tools"].extend(["stock_buffett_index_lg", "stock_index_pe_lg", "stock_index_pb_lg"])

    if "volatility" in tokens:
        out["tools"].append("stock_zh_a_hist")

    if "sector" in tokens or "rotation" in tokens or "industry" in tokens:
        out["tools"].extend(
            [
                "stock_board_industry_name_em",
                "stock_board_industry_spot_em",
                "stock_board_industry_index_ths",
                "stock_fund_flow_industry",
            ]
        )

    if "concept" in tokens:
        out["views"].extend(["concept_board_snapshot", "concept_board_detail"])
        out["tools"].extend(["stock_board_concept_name_em", "stock_board_concept_spot_em", "stock_board_concept_cons_em"])

    if "fund" in tokens and "flow" in tokens:
        out["views"].append("fund_flow_dashboard")
        out["tools"].extend(["stock_market_fund_flow", "stock_sector_fund_flow_rank", "stock_fund_flow_big_deal"])

    if "sentiment" in tokens or "hot" in tokens:
        out["views"].append("hot_rank_sentiment_dashboard")
        out["tools"].extend(["stock_hot_rank_em", "stock_hot_rank_detail_em", "stock_hot_keyword_em"])

    if "disclosure" in tokens or "notice" in tokens:
        out["views"].extend(["notice_daily_dashboard", "cninfo_disclosure_search", "report_disclosure_calendar"])

    if "event" in tokens:
        out["tools"].extend(["stock_zh_a_hist", "stock_bid_ask_em"])

    if "portfolio" in tokens or "optimizer" in tokens or "rebalancing" in tokens:
        out["tools"].append("stock_zh_a_hist")

    if "etf" in tokens:
        out["notes"].append("当前 A股工具注册表未包含 ETF 专用接口；如需 ETF 数据可后续扩展 litellm_tools.json 或添加自定义 view。")

    if "macro" in tokens or "policy" in tokens or "liquidity" in tokens or "yield" in tokens:
        out["views"].append("macro_china_dashboard")

    # Baseline (avoid empty docs).
    if not out["views"] and not out["tools"]:
        out["tools"].extend(["stock_individual_info_em", "stock_zh_a_hist"])

    # De-dup while preserving order.
    def dedup(seq: list[str]) -> list[str]:
        seen = set()
        out2 = []
        for x in seq:
            if x in seen:
                continue
            seen.add(x)
            out2.append(x)
        return out2

    out["views"] = dedup([v for v in out["views"] if v])
    out["tools"] = dedup([t for t in out["tools"] if t])
    # Treat tool names as tool-views (view name == tool name).
    out["views"] = dedup(out["views"] + out["tools"])
    return out


def _render_cn_data_queries(
    *,
    skill_dir_name: str,
    fm: FrontMatter,
    tool_index: dict[str, Any],
    views: dict[str, Any],
) -> str:
    deps = _cn_skill_dependencies(skill_dir_name)

    view_rows: list[list[str]] = []
    custom_view_details: list[str] = []
    for view_name in deps["views"]:
        spec = views.get(view_name)
        if not spec:
            view_rows.append([view_name, "(missing)", "-", "-", "-", ""])
            continue

        is_tool_view = _cn_is_tool_view(spec)
        schema = getattr(spec, "params_schema", None)
        required = _render_required_and_common(schema, common=("symbol", "date", "start_date", "end_date", "period", "adjust"))

        if is_tool_view:
            tool = _cn_tool_def(tool_index, view_name) or {}
            fn = tool.get("function") or {}
            extra = tool.get("extra") or {}
            output = extra.get("output") if isinstance(extra, dict) else None
            key_fields = _first_keys(output if isinstance(output, dict) else None, 10)
            view_rows.append(
                [
                    view_name,
                    "tool",
                    "tool view (1:1)",
                    getattr(spec, "description", "") or str(fn.get("description") or "-"),
                    required,
                    ", ".join(key_fields) if key_fields else "tool envelope: {meta,data,warnings,errors}",
                ]
            )
            continue

        plan = _cn_custom_view_plan(spec)
        keys = []
        tools = []
        for c in plan:
            if isinstance(c, dict):
                if c.get("key"):
                    keys.append(str(c.get("key")))
                if c.get("tool"):
                    tools.append(str(c.get("tool")))
        keys = [k for i, k in enumerate(keys) if k and k not in keys[:i]]
        tools = [t for i, t in enumerate(tools) if t and t not in tools[:i]]
        view_rows.append(
            [
                view_name,
                "custom",
                "composed view",
                getattr(spec, "description", "") or "-",
                required,
                f"data keys: {', '.join(keys[:10])}" if keys else "view envelope: {meta,data,warnings,errors}",
            ]
        )

        # Add per-view underlying tool dependency table.
        if plan:
            rows: list[list[str]] = []
            for c in plan[:25]:
                if not isinstance(c, dict):
                    continue
                k = str(c.get("key") or "")
                t = str(c.get("tool") or "")
                if not t:
                    continue
                if t in tool_index:
                    tool = _cn_tool_def(tool_index, t) or {}
                    fn = tool.get("function") or {}
                    extra = tool.get("extra") or {}
                    params = fn.get("parameters") if isinstance(fn, dict) else None
                    output = extra.get("output") if isinstance(extra, dict) else None
                    key_fields = _first_keys(output if isinstance(output, dict) else None, 10)
                    rows.append(
                        [
                            k or "-",
                            t,
                            str(fn.get("description") or "-"),
                            _render_required_and_common(params, common=("symbol", "date", "start_date", "end_date", "period", "adjust")),
                            ", ".join(key_fields) if key_fields else "(columns as-is)",
                        ]
                    )
                else:
                    rows.append([k or "-", t, "(missing)", "-", "-"])

            if rows:
                custom_view_details.append(f"#### `{view_name}` 底层工具（plan 展开）\n\n")
                custom_view_details.append(
                    _md_table(
                        rows,
                        headers=["key", "tool", "说明", "入参（必填/常用）", "关键输出字段（示例）"],
                    )
                )

    tool_rows: list[list[str]] = []
    notes = deps.get("notes") or []

    title_hint = f"（{fm.description}）" if fm.description else ""
    header = "# 数据获取命令（共享脚本）\n\n"
    header += "运行时约定：仅支持 Python 3.10–3.12，并使用仓库根目录统一虚拟环境 `.venv`。\n\n"
    header += f"从本技能目录运行。共享数据脚本位于 `../findata-toolkit-cn/`。{title_hint}\n"

    setup = "## 一次性环境准备\n\n" + _md_code(
        "\n".join(
            [
                "# 激活仓库根目录虚拟环境（统一 .venv）",
                "source ../../.venv/bin/activate",
                "",
                "# 安装 A股工具包依赖",
                "python -m pip install -r ../findata-toolkit-cn/requirements.txt",
            ]
        )
    )

    deps_md = "## 本技能依赖的数据（views / tools）\n\n"
    deps_md += "口径约定：\n\n"
    deps_md += "- `views_runner.py` 输出统一为 JSON：`{meta, data, warnings, errors}`。\n"
    deps_md += "- tool view 的 `data` 字段保持底层实现的原始字段名/单位（不做二次清洗）。\n"
    deps_md += "- 自定义 view 的 `data` 是多个 tool view 调用结果的聚合字典（每个 value 仍是 tool envelope）。\n\n"

    if view_rows:
        deps_md += "### Views（建议）\n\n"
        deps_md += _md_table(
            view_rows,
            headers=["view 名称", "类型", "定位", "用途", "入参（必填/常用）", "产出/口径"],
        )
        if custom_view_details:
            deps_md += "\n".join(custom_view_details) + "\n"

    if notes:
        deps_md += "### 备注\n\n"
        for n in notes:
            deps_md += f"- {n}\n"
        deps_md += "\n"

    common = "## 常用命令\n\n" + _md_code(
        "\n".join(
            [
                "# 确保已激活虚拟环境（统一 .venv）",
                "source ../../.venv/bin/activate",
                "",
                "# 发现可用 view（包含 tool views 与组合 views）",
                "python ../findata-toolkit-cn/scripts/views_runner.py list --contains <keyword>",
                "",
                "# 查看 view 的入参 schema",
                "python ../findata-toolkit-cn/scripts/views_runner.py describe <view_or_tool_name>",
                "",
                "# 只生成调用计划（不执行真实抓取；便于写分析/复现）",
                "python ../findata-toolkit-cn/scripts/views_runner.py <view_or_tool_name> --dry-run --set key=value",
                "",
                "# 示例：A股实时行情 / 历史K线",
                "python ../findata-toolkit-cn/scripts/views_runner.py stock_zh_a_spot_em",
                "python ../findata-toolkit-cn/scripts/views_runner.py stock_zh_a_hist --set symbol=000001 --set period=daily --set start_date=20250101 --set end_date=20250201 --set adjust=qfq",
            ]
        )
    )

    optional = "## 可选\n\n" + "\n".join(
        [
            "- 缓存目录：`FINSKILLS_CACHE_DIR=/tmp/finskills-cache`",
            "- 若某些接口需要雪球 token：设置 `XUEQIU_TOKEN` 环境变量（当工具入参包含 `token` 时）",
            "",
        ]
    )

    return header + "\n\n" + setup + "\n" + deps_md + "\n" + common + "\n" + optional


def _us_skill_dependencies(skill_dir: str) -> dict[str, Any]:
    tokens = set(_slug_tokens(skill_dir))
    out: dict[str, Any] = {"scripts": [], "notes": []}

    def add(script: str, why: str) -> None:
        out["scripts"].append({"script": script, "why": why})

    if "macro" in tokens or "policy" in tokens or "yield" in tokens or "credit" in tokens or "breadth" in tokens:
        add("macro_data.py", "FRED macro dashboard (rates, inflation, credit proxies).")

    if "insider" in tokens or "edgar" in tokens or "buyback" in tokens or "earnings" in tokens or "event" in tokens:
        add("sec_edgar.py", "SEC EDGAR filings / insider trades (Form 4) / corporate events.")

    if "options" in tokens or "volatility" in tokens:
        add("stock_data.py", "Underlying price history / volatility inputs via yfinance.")

    if "factor" in tokens or "quant" in tokens:
        add("factor_screener.py", "Factor scoring / screening engine.")

    if "portfolio" in tokens or "optimizer" in tokens or "rebalancing" in tokens or "tax" in tokens:
        add("portfolio_analytics.py", "Portfolio analytics (risk, drawdown, stress, basic optimization helpers).")

    if "financial" in tokens or "statement" in tokens or "undervalued" in tokens or "peer" in tokens or "tech" in tokens or "growth" in tokens or "dividend" in tokens:
        add("stock_data.py", "Fundamentals / metrics / history via yfinance.")
        add("financial_calc.py", "Quality metrics (Z/M/F scores, DuPont-style helpers).")

    if "etf" in tokens:
        add("stock_data.py", "ETF quotes / holdings proxy data available via yfinance fields when present.")
        out["notes"].append("ETF constituents may be incomplete in yfinance for some tickers; consider extending toolkit if needed.")

    if not out["scripts"]:
        add("stock_data.py", "Basic quotes / fundamentals / history via yfinance.")

    # De-dup while preserving order.
    seen = set()
    dedup = []
    for item in out["scripts"]:
        if item["script"] in seen:
            continue
        seen.add(item["script"])
        dedup.append(item)
    out["scripts"] = dedup
    return out


def _render_us_data_queries(*, skill_dir_name: str, fm: FrontMatter) -> str:
    deps = _us_skill_dependencies(skill_dir_name)
    header = "# Data Queries (Shared Scripts)\n\n"
    header += f"Run commands from this skill directory. Shared scripts live in `../findata-toolkit/`."
    if fm.description:
        header += f" ({fm.description})"
    header += "\n"

    setup = "## Setup (One-Time)\n\n" + _md_code(
        "\n".join(
            [
                "# Activate repo-root venv (single .venv)",
                "source ../../.venv/bin/activate",
                "",
                "# Install US toolkit deps",
                "python -m pip install -r ../findata-toolkit/requirements.txt",
            ]
        )
    )

    dep_rows = [[d["script"], d["why"]] for d in deps["scripts"]]
    deps_md = "## Data Dependencies (What this skill uses)\n\n"
    deps_md += _md_table(dep_rows, headers=["Script", "Primary use"])
    if deps.get("notes"):
        deps_md += "\nNotes:\n\n"
        for n in deps["notes"]:
            deps_md += f"- {n}\n"
        deps_md += "\n"

    common = "## Common Recipes\n\n" + _md_code(
        "\n".join(
            [
                "# Ensure venv is active",
                "source ../../.venv/bin/activate",
                "",
                "# Quotes / fundamentals / history",
                "python ../findata-toolkit/scripts/stock_data.py AAPL",
                "python ../findata-toolkit/scripts/stock_data.py AAPL --metrics",
                "python ../findata-toolkit/scripts/stock_data.py AAPL --history --period 1y",
                "",
                "# SEC EDGAR (insider trades / filings)",
                "python ../findata-toolkit/scripts/sec_edgar.py insider AAPL --days 90",
                "python ../findata-toolkit/scripts/sec_edgar.py filings AAPL --form-type 10-K",
                "",
                "# Macro (FRED)",
                "python ../findata-toolkit/scripts/macro_data.py --dashboard",
                "",
                "# Financial calculators",
                "python ../findata-toolkit/scripts/financial_calc.py AAPL --all",
            ]
        )
    )

    more = "## Discover More\n\n" + _md_code(
        "\n".join(
            [
                "python ../findata-toolkit/scripts/stock_data.py --help",
                "python ../findata-toolkit/scripts/sec_edgar.py --help",
                "python ../findata-toolkit/scripts/macro_data.py --help",
                "python ../findata-toolkit/scripts/financial_calc.py --help",
                "python ../findata-toolkit/scripts/portfolio_analytics.py --help",
                "python ../findata-toolkit/scripts/factor_screener.py --help",
            ]
        )
    )

    return header + "\n\n" + setup + "\n" + deps_md + "\n" + common + "\n" + more


def _iter_skill_dirs(root: Path, toolkit_dirname: str) -> list[Path]:
    out = []
    for p in sorted(root.iterdir()):
        if not p.is_dir():
            continue
        if p.name == toolkit_dirname:
            continue
        if not (p / "SKILL.md").exists():
            continue
        if not (p / "references" / "data-queries.md").exists():
            continue
        out.append(p)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate per-skill references/data-queries.md")
    parser.add_argument(
        "--emit-deps-json",
        default="",
        help="Write a machine-readable dependency index JSON (views/scripts per skill).",
    )
    parser.add_argument(
        "--emit-view-specs-dir",
        default="",
        help="Write per-view JSON specs for all required China-market views into this directory.",
    )
    args = parser.parse_args()

    tool_index, views = _load_cn_views_and_tools()

    cn_skills = _iter_skill_dirs(CN_ROOT, "findata-toolkit-cn")
    us_skills = _iter_skill_dirs(US_ROOT, "findata-toolkit")

    changed = 0
    deps_index: dict[str, Any] = {"china": {}, "us": {}}

    for skill in cn_skills:
        fm = _parse_frontmatter(_read_text(skill / "SKILL.md"))
        out = _render_cn_data_queries(skill_dir_name=skill.name, fm=fm, tool_index=tool_index, views=views)
        dest = skill / "references" / "data-queries.md"
        if _read_text(dest) != out:
            _write_text(dest, out)
            changed += 1
        deps_index["china"][skill.name] = {"views": _cn_skill_dependencies(skill.name)["views"]}

    for skill in us_skills:
        fm = _parse_frontmatter(_read_text(skill / "SKILL.md"))
        out = _render_us_data_queries(skill_dir_name=skill.name, fm=fm)
        dest = skill / "references" / "data-queries.md"
        if _read_text(dest) != out:
            _write_text(dest, out)
            changed += 1
        deps_index["us"][skill.name] = {"scripts": [d["script"] for d in _us_skill_dependencies(skill.name)["scripts"]]}

    # Add a flattened view list for convenience.
    all_cn_views: list[str] = []
    for v in deps_index["china"].values():
        all_cn_views.extend(v.get("views") or [])
    deps_index["china_all_views"] = sorted({x for x in all_cn_views if isinstance(x, str) and x})

    if args.emit_deps_json:
        out_path = Path(args.emit_deps_json).expanduser()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(deps_index, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.emit_view_specs_dir:
        out_dir = Path(args.emit_view_specs_dir).expanduser()
        out_dir.mkdir(parents=True, exist_ok=True)

        required = set(deps_index["china_all_views"])
        # Closure: include underlying tool views used by custom views.
        queue = list(required)
        while queue:
            vname = queue.pop()
            spec = views.get(vname)
            if not spec or _cn_is_tool_view(spec):
                continue
            for c in _cn_custom_view_plan(spec):
                if isinstance(c, dict) and c.get("tool"):
                    dep = str(c.get("tool"))
                    if dep and dep not in required:
                        required.add(dep)
                        queue.append(dep)

        index: dict[str, Any] = {"views": []}
        for vname in sorted(required):
            spec = views.get(vname)
            if not spec:
                continue
            payload = _cn_view_spec_to_json(name=vname, view_spec=spec, tool_index=tool_index)
            (out_dir / f"{vname}.json").write_text(
                json.dumps(payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            index["views"].append({"name": vname, "kind": payload.get("kind")})

        (out_dir / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Updated {changed} data-queries.md files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
