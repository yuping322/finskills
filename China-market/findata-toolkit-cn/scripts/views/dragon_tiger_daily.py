from __future__ import annotations

from ._helpers import ensure_yyyymmdd, today_yyyymmdd

VIEW_NAME = "dragon_tiger_daily"
DESCRIPTION = "龙虎榜日度聚合：上榜明细 + 机构买卖统计 + 活跃营业部（工具聚合视图）。"
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

    return [
        {"key": "lhb_detail_daily_sina", "tool": "stock_lhb_detail_daily_sina", "args": {"date": date}},
        {"key": "lhb_detail_em", "tool": "stock_lhb_detail_em", "args": {"start_date": date, "end_date": date}},
        {"key": "lhb_institution_buy_sell_stat", "tool": "stock_lhb_jgmmtj_em", "args": {"start_date": date, "end_date": date}},
        {"key": "lhb_active_yyb", "tool": "stock_lhb_hyyyb_em", "args": {"start_date": date, "end_date": date}},
    ]

