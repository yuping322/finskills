from __future__ import annotations

from datetime import datetime

from ._helpers import ensure_yyyymmdd, today_yyyymmdd

VIEW_NAME = "dividend_actions_dashboard"
DESCRIPTION = "分红/配股聚合：分红配送、交易提醒、个股历史分红与配股方案（工具聚合视图）。"
PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "fhps_date": {"type": "string", "description": "分红配送报告期 YYYYMMDD（通常为 XXXX0630 或 XXXX1231）"},
        "calendar_date": {"type": "string", "description": "交易提醒日期 YYYYMMDD"},
        "symbol": {"type": "string", "description": "股票代码（可选；用于个股分红/配股详情）"},
        "allotment_start_date": {"type": "string", "description": "配股方案查询起始 YYYYMMDD"},
        "allotment_end_date": {"type": "string", "description": "配股方案查询结束 YYYYMMDD"},
    },
    "required": [],
}


def plan(params: dict) -> list[dict]:
    default_fhps_date = f"{datetime.now().year - 1}1231"
    fhps_date = ensure_yyyymmdd(str(params.get("fhps_date") or default_fhps_date), field="fhps_date")
    calendar_date = ensure_yyyymmdd(str(params.get("calendar_date") or today_yyyymmdd()), field="calendar_date")

    calls: list[dict] = [
        {"key": "fhps_by_period", "tool": "stock_fhps_em", "args": {"date": fhps_date}},
        {"key": "trade_notify_dividend", "tool": "news_trade_notify_dividend_baidu", "args": {"date": calendar_date}},
    ]

    symbol = params.get("symbol")
    if symbol:
        calls.append({"key": "dividend_cninfo", "tool": "stock_dividend_cninfo", "args": {"symbol": str(symbol)}})
        calls.append({"key": "fhps_detail_em", "tool": "stock_fhps_detail_em", "args": {"symbol": str(symbol)}})
        calls.append({"key": "fhps_detail_ths", "tool": "stock_fhps_detail_ths", "args": {"symbol": str(symbol)}})

        asd = ensure_yyyymmdd(str(params.get("allotment_start_date") or "19700101"), field="allotment_start_date")
        aed = ensure_yyyymmdd(str(params.get("allotment_end_date") or "22220222"), field="allotment_end_date")
        calls.append(
            {
                "key": "allotment_plan",
                "tool": "stock_allotment_cninfo",
                "args": {"symbol": str(symbol), "start_date": asd, "end_date": aed},
            }
        )

    return calls
