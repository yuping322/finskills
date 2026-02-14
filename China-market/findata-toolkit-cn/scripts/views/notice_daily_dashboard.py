from __future__ import annotations

from ._helpers import ensure_yyyymmdd, today_yyyymmdd

VIEW_NAME = "notice_daily_dashboard"
DESCRIPTION = "公告类别-按日汇总（stock_notice_report；工具聚合视图）。"
PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "category": {"type": "string", "description": "全部/重大事项/财务报告/融资公告/风险提示/资产重组/信息变更/持股变动"},
        "date": {"type": "string", "description": "YYYYMMDD"},
    },
    "required": [],
}


def plan(params: dict) -> list[dict]:
    category = params.get("category") or "重大事项"
    date = ensure_yyyymmdd(str(params.get("date") or today_yyyymmdd()), field="date")

    return [
        {"key": "notice_report", "tool": "stock_notice_report", "args": {"symbol": category, "date": date}},
    ]

