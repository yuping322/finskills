from __future__ import annotations

from ._helpers import days_ago_yyyymmdd, ensure_yyyymmdd, today_yyyymmdd

VIEW_NAME = "block_deal_dashboard"
DESCRIPTION = "大宗交易聚合视图：市场统计、区间每日统计/明细、活跃个股与活跃营业部（工具聚合视图）。"
PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "market": {
            "type": "string",
            "description": "每日明细口径；A股/B股/基金/债券",
        },
        "start_date": {"type": "string", "description": "YYYYMMDD；区间起始日期（用于每日统计/每日明细）"},
        "end_date": {"type": "string", "description": "YYYYMMDD；区间结束日期（用于每日统计/每日明细）"},
        "active_stock_window": {
            "type": "string",
            "description": "活跃A股统计窗口；近一月/近三月/近六月/近一年",
        },
        "active_broker_window": {
            "type": "string",
            "description": "活跃营业部统计窗口；当前交易日/近3日/近5日/近10日/近30日",
        },
        "broker_rank_window": {
            "type": "string",
            "description": "营业部排行窗口；近一月/近三月/近六月/近一年",
        },
    },
    "required": [],
}


def plan(params: dict) -> list[dict]:
    market = params.get("market") or "A股"

    default_end = today_yyyymmdd()
    default_start = days_ago_yyyymmdd(30)
    start_date = ensure_yyyymmdd(str(params.get("start_date") or default_start), field="start_date")
    end_date = ensure_yyyymmdd(str(params.get("end_date") or default_end), field="end_date")

    active_stock_window = params.get("active_stock_window") or "近三月"
    active_broker_window = params.get("active_broker_window") or "近30日"
    broker_rank_window = params.get("broker_rank_window") or "近三月"

    return [
        {"key": "market_stats", "tool": "stock_dzjy_sctj", "args": {}},
        {"key": "daily_stats", "tool": "stock_dzjy_mrtj", "args": {"start_date": start_date, "end_date": end_date}},
        {"key": "daily_detail", "tool": "stock_dzjy_mrmx", "args": {"symbol": market, "start_date": start_date, "end_date": end_date}},
        {"key": "active_stocks", "tool": "stock_dzjy_hygtj", "args": {"symbol": active_stock_window}},
        {"key": "active_brokers", "tool": "stock_dzjy_hyyybtj", "args": {"symbol": active_broker_window}},
        {"key": "broker_ranking", "tool": "stock_dzjy_yybph", "args": {"symbol": broker_rank_window}},
    ]

