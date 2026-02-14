from __future__ import annotations

from ._helpers import days_ago_yyyymmdd, ensure_yyyymmdd, today_yyyymmdd

VIEW_NAME = "cninfo_disclosure_search"
DESCRIPTION = "巨潮资讯信息披露公告查询（按股票/类别/关键词/时间窗；工具聚合视图）。"
PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "symbol": {"type": "string", "description": "股票代码，如 000001"},
        "market": {"type": "string", "description": "沪深京/港股/三板/基金/债券/监管/预披露"},
        "keyword": {"type": "string", "description": "关键词（可选）"},
        "category": {"type": "string", "description": "公告类别（见接口枚举，如 年报/业绩预告/解禁/可转债/风险提示 等）"},
        "start_date": {"type": "string", "description": "YYYYMMDD"},
        "end_date": {"type": "string", "description": "YYYYMMDD"},
    },
    "required": ["symbol", "category"],
}


def plan(params: dict) -> list[dict]:
    symbol = params.get("symbol")
    category = params.get("category")
    if not symbol:
        raise ValueError("symbol is required")
    if not category:
        raise ValueError("category is required")

    market = params.get("market") or "沪深京"
    keyword = params.get("keyword") or ""
    start_date = ensure_yyyymmdd(str(params.get("start_date") or days_ago_yyyymmdd(180)), field="start_date")
    end_date = ensure_yyyymmdd(str(params.get("end_date") or today_yyyymmdd()), field="end_date")

    return [
        {
            "key": "disclosure_reports",
            "tool": "stock_zh_a_disclosure_report_cninfo",
            "args": {
                "symbol": str(symbol),
                "market": market,
                "keyword": keyword,
                "category": str(category),
                "start_date": start_date,
                "end_date": end_date,
            },
        }
    ]

