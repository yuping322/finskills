from __future__ import annotations

from ._helpers import days_from_now_yyyymmdd, ensure_yyyymmdd, today_yyyymmdd

VIEW_NAME = "restricted_release_dashboard"
DESCRIPTION = "限售解禁聚合：解禁汇总/明细/个股解禁队列与股东信息（工具聚合视图）。"
PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "market_scope": {"type": "string", "description": "全部股票/沪市A股/科创板/深市A股/创业板/京市A股"},
        "start_date": {"type": "string", "description": "YYYYMMDD"},
        "end_date": {"type": "string", "description": "YYYYMMDD"},
        "symbol": {"type": "string", "description": "股票代码（可选；用于个股队列/股东信息）"},
        "queue_date": {"type": "string", "description": "YYYYMMDD（可选；用于股东解禁明细）"},
    },
    "required": [],
}


def plan(params: dict) -> list[dict]:
    market_scope = params.get("market_scope") or "全部股票"
    start_date = ensure_yyyymmdd(str(params.get("start_date") or today_yyyymmdd()), field="start_date")
    end_date = ensure_yyyymmdd(str(params.get("end_date") or days_from_now_yyyymmdd(30)), field="end_date")

    calls: list[dict] = [
        {
            "key": "release_summary",
            "tool": "stock_restricted_release_summary_em",
            "args": {"symbol": market_scope, "start_date": start_date, "end_date": end_date},
        },
        {"key": "release_detail", "tool": "stock_restricted_release_detail_em", "args": {"start_date": start_date, "end_date": end_date}},
    ]

    symbol = params.get("symbol")
    if symbol:
        calls.append({"key": "queue_em", "tool": "stock_restricted_release_queue_em", "args": {"symbol": str(symbol)}})
        calls.append({"key": "queue_sina", "tool": "stock_restricted_release_queue_sina", "args": {"symbol": str(symbol)}})

        queue_date = params.get("queue_date")
        if queue_date:
            qd = ensure_yyyymmdd(str(queue_date), field="queue_date")
            calls.append(
                {
                    "key": "stockholder_release",
                    "tool": "stock_restricted_release_stockholder_em",
                    "args": {"symbol": str(symbol), "date": qd},
                }
            )

    return calls

