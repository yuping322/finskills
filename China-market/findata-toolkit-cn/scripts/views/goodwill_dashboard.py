from __future__ import annotations

from ._helpers import ensure_yyyymmdd, latest_quarter_end_yyyymmdd

VIEW_NAME = "goodwill_dashboard"
DESCRIPTION = "商誉聚合：公司/行业商誉、减值明细与预期（工具聚合视图）。"
PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "date": {"type": "string", "description": "报告期/日期 YYYYMMDD（通常为季度末，如 20251231）"},
    },
    "required": [],
}


def plan(params: dict) -> list[dict]:
    date = ensure_yyyymmdd(str(params.get("date") or latest_quarter_end_yyyymmdd()), field="date")

    return [
        {"key": "profile", "tool": "stock_sy_profile_em", "args": {}},
        {"key": "goodwill_company", "tool": "stock_sy_em", "args": {"date": date}},
        {"key": "goodwill_industry", "tool": "stock_sy_hy_em", "args": {"date": date}},
        {"key": "impairment_detail", "tool": "stock_sy_jz_em", "args": {"date": date}},
        {"key": "impairment_expectation", "tool": "stock_sy_yq_em", "args": {"date": date}},
    ]

