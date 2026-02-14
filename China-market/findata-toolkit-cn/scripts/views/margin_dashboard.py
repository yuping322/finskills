from __future__ import annotations

from ._helpers import ensure_yyyymmdd, today_yyyymmdd

VIEW_NAME = "margin_dashboard"
DESCRIPTION = "两融汇总视图：沪深两融汇总、明细与账户信息（工具聚合视图）。"
PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "date": {"type": "string", "description": "交易日 YYYYMMDD"},
        "start_date": {"type": "string", "description": "YYYYMMDD（可选；上交所汇总使用）"},
        "end_date": {"type": "string", "description": "YYYYMMDD（可选；上交所汇总使用）"},
    },
    "required": [],
}


def plan(params: dict) -> list[dict]:
    date = ensure_yyyymmdd(str(params.get("date") or today_yyyymmdd()), field="date")
    start_date = params.get("start_date")
    end_date = params.get("end_date")
    sd = ensure_yyyymmdd(str(start_date or date), field="start_date")
    ed = ensure_yyyymmdd(str(end_date or date), field="end_date")

    return [
        {"key": "margin_ratio_pa", "tool": "stock_margin_ratio_pa", "args": {"date": date}},
        {"key": "margin_account_info", "tool": "stock_margin_account_info", "args": {}},
        {"key": "margin_sse_summary", "tool": "stock_margin_sse", "args": {"start_date": sd, "end_date": ed}},
        {"key": "margin_sse_detail", "tool": "stock_margin_detail_sse", "args": {"date": date}},
        {"key": "margin_szse_summary", "tool": "stock_margin_szse", "args": {"date": date}},
        {"key": "margin_szse_detail", "tool": "stock_margin_detail_szse", "args": {"date": date}},
        {"key": "margin_underlying_szse", "tool": "stock_margin_underlying_info_szse", "args": {"date": date}},
    ]

