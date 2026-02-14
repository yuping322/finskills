from __future__ import annotations

from ._helpers import days_ago_yyyymmdd, ensure_yyyymmdd, today_yyyymmdd

VIEW_NAME = "cninfo_disclosure_relation_search"
DESCRIPTION = "巨潮资讯信息披露调研查询（工具聚合视图）。"
PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "symbol": {"type": "string", "description": "股票代码，如 000001"},
        "market": {"type": "string", "description": "沪深京/港股/三板/基金/债券/监管/预披露"},
        "start_date": {"type": "string", "description": "YYYYMMDD"},
        "end_date": {"type": "string", "description": "YYYYMMDD"},
    },
    "required": ["symbol"],
}


def plan(params: dict) -> list[dict]:
    symbol = params.get("symbol")
    if not symbol:
        raise ValueError("symbol is required")

    market = params.get("market") or "沪深京"
    start_date = ensure_yyyymmdd(str(params.get("start_date") or days_ago_yyyymmdd(180)), field="start_date")
    end_date = ensure_yyyymmdd(str(params.get("end_date") or today_yyyymmdd()), field="end_date")

    return [
        {
            "key": "disclosure_relations",
            "tool": "stock_zh_a_disclosure_relation_cninfo",
            "args": {"symbol": str(symbol), "market": market, "start_date": start_date, "end_date": end_date},
        }
    ]

