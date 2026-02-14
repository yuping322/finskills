from __future__ import annotations

from datetime import datetime

VIEW_NAME = "report_disclosure_calendar"
DESCRIPTION = "定期报告披露日历（交易所口径汇总；工具聚合视图）。"
PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "market": {"type": "string", "description": "沪深京/深市/深主板/创业板/沪市/沪主板/科创板/北交所"},
        "period": {"type": "string", "description": "报告期，如 2025年报 / 2025一季 / 2025半年报 / 2025三季（以接口实际可用为准）"},
    },
    "required": [],
}


def plan(params: dict) -> list[dict]:
    market = params.get("market") or "沪深京"
    default_period = f"{datetime.now().year - 1}年报"
    period = params.get("period") or default_period

    return [
        {"key": "report_disclosure", "tool": "stock_report_disclosure", "args": {"market": market, "period": period}},
    ]
