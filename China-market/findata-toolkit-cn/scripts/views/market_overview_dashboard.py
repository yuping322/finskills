from __future__ import annotations

from ._helpers import ensure_yyyymmdd, today_yyyymmdd

VIEW_NAME = "market_overview_dashboard"
DESCRIPTION = "汇总上交所/深交所市场总貌与成交概况（工具聚合视图）。"
PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "date": {"type": "string", "description": "交易日 YYYYMMDD；深交所/上交所部分统计需收盘后可得"},
    },
    "required": [],
}


def plan(params: dict) -> list[dict]:
    date = params.get("date") or today_yyyymmdd()
    date = ensure_yyyymmdd(str(date), field="date")

    return [
        {"key": "sse_summary", "tool": "stock_sse_summary", "args": {}},
        {"key": "szse_summary", "tool": "stock_szse_summary", "args": {"date": date}},
        {"key": "sse_deal_daily", "tool": "stock_sse_deal_daily", "args": {"date": date}},
    ]

