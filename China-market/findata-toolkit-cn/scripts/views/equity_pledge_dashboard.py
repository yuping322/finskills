from __future__ import annotations

from ._helpers import ensure_yyyymmdd, today_yyyymmdd

VIEW_NAME = "equity_pledge_dashboard"
DESCRIPTION = "股权质押风险聚合：质押概览、行业分布、质押比例（工具聚合视图）。"
PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "date": {"type": "string", "description": "交易日 YYYYMMDD（部分接口需要可用交易日）"},
    },
    "required": [],
}


def plan(params: dict) -> list[dict]:
    date = ensure_yyyymmdd(str(params.get("date") or today_yyyymmdd()), field="date")

    return [
        {"key": "profile", "tool": "stock_gpzy_profile_em", "args": {}},
        {"key": "industry_data", "tool": "stock_gpzy_industry_data_em", "args": {}},
        {"key": "distribute_company", "tool": "stock_gpzy_distribute_statistics_company_em", "args": {}},
        {"key": "distribute_bank", "tool": "stock_gpzy_distribute_statistics_bank_em", "args": {}},
        {"key": "pledge_ratio", "tool": "stock_gpzy_pledge_ratio_em", "args": {"date": date}},
        # Schema may be incomplete; still try passing date.
        {"key": "pledge_ratio_detail", "tool": "stock_gpzy_pledge_ratio_detail_em", "args": {"date": date}},
    ]

