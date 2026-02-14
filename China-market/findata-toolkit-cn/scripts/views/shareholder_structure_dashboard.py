from __future__ import annotations

from ._helpers import ensure_yyyymmdd, latest_quarter_end_yyyymmdd

VIEW_NAME = "shareholder_structure_dashboard"
DESCRIPTION = "股东结构/筹码聚合：股东户数、主要股东、流通股东、持股变动与监管披露（工具聚合视图）。"
PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "symbol": {"type": "string", "description": "股票代码（6位）"},
        "gdhs_quarter": {"type": "string", "description": "股东户数查询季度：最新 或 YYYYMMDD（季度末）"},
        "cninfo_date": {"type": "string", "description": "巨潮口径股东人数/集中度季度末 YYYYMMDD"},
        "cninfo_hold_change_scope": {"type": "string", "description": "股本变动市场范围：深市主板/沪市/创业板/科创板/北交所/全部"},
        "cninfo_control_scope": {"type": "string", "description": "控制人持股变动范围：单独控制/实际控制人/一致行动人/家族控制/全部"},
    },
    "required": ["symbol"],
}


def plan(params: dict) -> list[dict]:
    symbol = params.get("symbol")
    if not symbol:
        raise ValueError("symbol is required")
    sym6 = str(symbol).strip()[-6:]

    gdhs_quarter = params.get("gdhs_quarter") or "最新"
    cninfo_date = ensure_yyyymmdd(str(params.get("cninfo_date") or latest_quarter_end_yyyymmdd()), field="cninfo_date")
    hold_change_scope = params.get("cninfo_hold_change_scope") or "全部"
    control_scope = params.get("cninfo_control_scope") or "全部"

    return [
        {"key": "gdhs_quarter_list", "tool": "stock_zh_a_gdhs", "args": {"symbol": str(gdhs_quarter)}},
        {"key": "gdhs_detail", "tool": "stock_zh_a_gdhs_detail_em", "args": {"symbol": sym6}},
        {"key": "main_stock_holder", "tool": "stock_main_stock_holder", "args": {"stock": sym6}},
        {"key": "circulate_stock_holder", "tool": "stock_circulate_stock_holder", "args": {"symbol": sym6}},
        {"key": "shareholder_change_ths", "tool": "stock_shareholder_change_ths", "args": {"symbol": sym6}},
        {"key": "share_hold_change_sse", "tool": "stock_share_hold_change_sse", "args": {"symbol": sym6}},
        {"key": "share_hold_change_szse", "tool": "stock_share_hold_change_szse", "args": {"symbol": sym6}},
        {"key": "share_hold_change_bse", "tool": "stock_share_hold_change_bse", "args": {"symbol": sym6}},
        {"key": "hold_num_cninfo", "tool": "stock_hold_num_cninfo", "args": {"date": cninfo_date}},
        {"key": "hold_change_cninfo", "tool": "stock_hold_change_cninfo", "args": {"symbol": hold_change_scope}},
        {"key": "hold_control_cninfo", "tool": "stock_hold_control_cninfo", "args": {"symbol": control_scope}},
    ]

