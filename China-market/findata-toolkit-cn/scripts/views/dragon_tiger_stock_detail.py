from __future__ import annotations

from ._helpers import ensure_yyyymmdd, today_yyyymmdd

VIEW_NAME = "dragon_tiger_stock_detail"
DESCRIPTION = "个股龙虎榜详情：按日期与上榜类型查询（工具聚合视图）。"
PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "symbol": {"type": "string", "description": "股票代码"},
        "date": {"type": "string", "description": "交易日 YYYYMMDD"},
        "flag": {"type": "string", "description": "上榜原因类型（见 stock_lhb_stock_detail_em 的 flag）"},
    },
    "required": ["symbol", "flag"],
}


def plan(params: dict) -> list[dict]:
    symbol = params.get("symbol")
    flag = params.get("flag")
    if not symbol:
        raise ValueError("symbol is required")
    if not flag:
        raise ValueError("flag is required")

    date = params.get("date") or today_yyyymmdd()
    date = ensure_yyyymmdd(str(date), field="date")

    return [
        {
            "key": "lhb_stock_detail",
            "tool": "stock_lhb_stock_detail_em",
            "args": {"symbol": str(symbol), "date": date, "flag": str(flag)},
        },
        {
            "key": "lhb_stock_statistic",
            "tool": "stock_lhb_stock_statistic_em",
            "args": {"symbol": str(symbol)},
        },
    ]

