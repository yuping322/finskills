from __future__ import annotations

from ._helpers import days_ago_yyyymmdd, ensure_yyyymmdd, today_yyyymmdd

VIEW_NAME = "industry_board_detail"
DESCRIPTION = "行业板块详情：实时行情/成分股/历史行情（工具聚合视图）。"
PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "symbol": {"type": "string", "description": "行业名称或板块代码（如 小金属 或 BK1027）"},
        "start_date": {"type": "string", "description": "YYYYMMDD"},
        "end_date": {"type": "string", "description": "YYYYMMDD"},
        "period": {"type": "string", "description": "daily/weekly/monthly"},
        "adjust": {"type": "string", "description": "''/qfq/hfq"},
    },
    "required": ["symbol"],
}


def plan(params: dict) -> list[dict]:
    symbol = params.get("symbol")
    if not symbol:
        raise ValueError("symbol is required")

    start_date = ensure_yyyymmdd(str(params.get("start_date") or days_ago_yyyymmdd(90)), field="start_date")
    end_date = ensure_yyyymmdd(str(params.get("end_date") or today_yyyymmdd()), field="end_date")
    period = params.get("period") or "daily"
    adjust = params.get("adjust") or ""

    return [
        {"key": "spot", "tool": "stock_board_industry_spot_em", "args": {"symbol": symbol}},
        {"key": "constituents", "tool": "stock_board_industry_cons_em", "args": {"symbol": symbol}},
        {
            "key": "history",
            "tool": "stock_board_industry_hist_em",
            "args": {"symbol": symbol, "start_date": start_date, "end_date": end_date, "period": period, "adjust": adjust},
        },
    ]

