from __future__ import annotations

VIEW_NAME = "ipo_newlist_dashboard"
DESCRIPTION = "IPO/新股/次新聚合：申报、新股发行、新股列表、首日与受益股（工具聚合视图）。"
PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "symbol": {"type": "string", "description": "股票代码（可选；用于查询个股上市相关信息）"},
    },
    "required": [],
}


def plan(params: dict) -> list[dict]:
    calls: list[dict] = [
        {"key": "ipo_declare", "tool": "stock_ipo_declare", "args": {}},
        {"key": "new_ipo_cninfo", "tool": "stock_new_ipo_cninfo", "args": {}},
        {"key": "new_stock_list_em", "tool": "stock_zh_a_new_em", "args": {}},
        {"key": "sub_new_list_sina", "tool": "stock_zh_a_new", "args": {}},
        {"key": "new_list_first_day_ths", "tool": "stock_xgsr_ths", "args": {}},
        {"key": "ipo_benefit_ths", "tool": "stock_ipo_benefit_ths", "args": {}},
    ]

    symbol = params.get("symbol")
    if symbol:
        calls.append({"key": "ipo_summary_cninfo", "tool": "stock_ipo_summary_cninfo", "args": {"symbol": str(symbol)}})
        # Some APIs accept 'stock' instead of 'symbol'.
        calls.append({"key": "ipo_info_sina", "tool": "stock_ipo_info", "args": {"stock": str(symbol)}})

    return calls

