from __future__ import annotations

from ._helpers import ensure_yyyymmdd, today_yyyymmdd

VIEW_NAME = "st_delist_dashboard"
DESCRIPTION = "ST/退市相关标的与停复牌提醒（工具聚合视图）。"
PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "suspend_date": {"type": "string", "description": "停复牌提醒日期 YYYYMMDD"},
    },
    "required": [],
}


def plan(params: dict) -> list[dict]:
    suspend_date = ensure_yyyymmdd(str(params.get("suspend_date") or today_yyyymmdd()), field="suspend_date")

    return [
        {"key": "risk_warning_board", "tool": "stock_zh_a_st_em", "args": {}},
        {"key": "stop_delist_board", "tool": "stock_zh_a_stop_em", "args": {}},
        {"key": "staq_net_stop", "tool": "stock_staq_net_stop", "args": {}},
        {"key": "trade_notify_suspend", "tool": "news_trade_notify_suspend_baidu", "args": {"date": suspend_date}},
    ]

