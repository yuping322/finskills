from __future__ import annotations

from ._helpers import days_ago_yyyymmdd, ensure_yyyymmdd, today_yyyymmdd

VIEW_NAME = "repurchase_dashboard"
DESCRIPTION = "股票回购聚合视图：回购清单 + 个股股本变动（可选；工具聚合视图）。"
PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "symbol": {"type": "string", "description": "股票代码（6位，可选；用于股本变动查询）"},
        "start_date": {"type": "string", "description": "YYYYMMDD（可选；用于股本变动查询）"},
        "end_date": {"type": "string", "description": "YYYYMMDD（可选；用于股本变动查询）"},
    },
    "required": [],
}


def plan(params: dict) -> list[dict]:
    calls: list[dict] = [
        {"key": "repurchase_list", "tool": "stock_repurchase_em", "args": {}},
    ]

    symbol = params.get("symbol")
    if symbol:
        default_end = today_yyyymmdd()
        default_start = days_ago_yyyymmdd(365 * 5)
        start_date = ensure_yyyymmdd(str(params.get("start_date") or default_start), field="start_date")
        end_date = ensure_yyyymmdd(str(params.get("end_date") or default_end), field="end_date")
        calls.append(
            {
                "key": "share_change",
                "tool": "stock_share_change_cninfo",
                "args": {"symbol": str(symbol).strip()[-6:], "start_date": start_date, "end_date": end_date},
            }
        )

    return calls

