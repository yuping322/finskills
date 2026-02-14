from __future__ import annotations

from ._helpers import ensure_yyyymmdd, today_yyyymmdd

VIEW_NAME = "limit_up_pool_daily"
DESCRIPTION = "涨停池/强势股池聚合：涨停股池、昨日涨停、强势股、次新、炸板、跌停等（工具聚合视图）。"
PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "date": {"type": "string", "description": "交易日 YYYYMMDD"},
    },
    "required": [],
}


def plan(params: dict) -> list[dict]:
    date = params.get("date") or today_yyyymmdd()
    date = ensure_yyyymmdd(str(date), field="date")

    tools = [
        ("zt_pool", "stock_zt_pool_em"),
        ("zt_pool_previous", "stock_zt_pool_previous_em"),
        ("zt_pool_strong", "stock_zt_pool_strong_em"),
        ("zt_pool_sub_new", "stock_zt_pool_sub_new_em"),
        ("zt_pool_zbgc", "stock_zt_pool_zbgc_em"),
        ("zt_pool_dtgc", "stock_zt_pool_dtgc_em"),
    ]

    return [{"key": key, "tool": tool, "args": {"date": date}} for key, tool in tools]

