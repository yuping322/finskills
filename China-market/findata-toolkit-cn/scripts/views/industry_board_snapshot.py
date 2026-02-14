from __future__ import annotations

VIEW_NAME = "industry_board_snapshot"
DESCRIPTION = "行业板块快照：行业一览表/行业代码列表（工具聚合视图）。"
PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "sector_rank_indicator": {"type": "string", "description": "stock_sector_fund_flow_rank 的 indicator；今日/5日/10日"},
        "include_sector_fund_flow_rank": {"type": "boolean", "description": "是否附带行业资金流排名"},
    },
    "required": [],
}


def plan(params: dict) -> list[dict]:
    include_rank = params.get("include_sector_fund_flow_rank")
    if include_rank is None:
        include_rank = True

    indicator = params.get("sector_rank_indicator") or "今日"

    calls = [
        {"key": "industry_summary_ths", "tool": "stock_board_industry_summary_ths", "args": {}},
        # Some registries omit schema; still callable.
        {"key": "industry_name_em", "tool": "stock_board_industry_name_em", "args": {}},
    ]

    if include_rank:
        calls.append(
            {
                "key": "sector_fund_flow_rank",
                "tool": "stock_sector_fund_flow_rank",
                "args": {"indicator": indicator, "sector_type": "行业资金流"},
            }
        )

    return calls

