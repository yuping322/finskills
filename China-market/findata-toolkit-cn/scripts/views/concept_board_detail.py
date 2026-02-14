from __future__ import annotations

from ._helpers import days_ago_yyyymmdd, ensure_yyyymmdd, today_yyyymmdd

VIEW_NAME = "concept_board_detail"
DESCRIPTION = "概念板块详情：成分股 + 历史行情（工具聚合视图）。"
PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "symbol": {"type": "string", "description": "概念名称或代码（如 绿色电力）"},
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
        # Note: some tool schemas are incomplete; passing symbol still works via signature filtering.
        {"key": "constituents", "tool": "stock_board_concept_cons_em", "args": {"symbol": symbol}},
        {
            "key": "history",
            "tool": "stock_board_concept_hist_em",
            "args": {
                "symbol": symbol,
                "period": period,
                "start_date": start_date,
                "end_date": end_date,
                "adjust": adjust,
            },
        },
    ]

