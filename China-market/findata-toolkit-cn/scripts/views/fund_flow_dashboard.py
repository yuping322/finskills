from __future__ import annotations

VIEW_NAME = "fund_flow_dashboard"
DESCRIPTION = "整合大盘/主力/板块资金流向与大单追踪（工具聚合视图）。"
PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "main_flow_scope": {
            "type": "string",
            "description": "stock_main_fund_flow 的 symbol；如：全部股票/沪深A股/沪市A股/科创板/深市A股/创业板 等",
        },
        "rank_indicator": {
            "type": "string",
            "description": "stock_individual_fund_flow_rank 的 indicator；今日/3日/5日/10日",
        },
        "sector_rank_indicator": {
            "type": "string",
            "description": "stock_sector_fund_flow_rank 的 indicator；今日/5日/10日",
        },
        "sector_type": {
            "type": "string",
            "description": "stock_sector_fund_flow_rank 的 sector_type；行业资金流/概念资金流/地域资金流",
        },
    },
    "required": [],
}


def plan(params: dict) -> list[dict]:
    main_flow_scope = params.get("main_flow_scope") or "全部股票"
    rank_indicator = params.get("rank_indicator") or "今日"
    sector_rank_indicator = params.get("sector_rank_indicator") or "今日"
    sector_type = params.get("sector_type") or "行业资金流"

    return [
        {"key": "market_fund_flow", "tool": "stock_market_fund_flow", "args": {}},
        {"key": "main_fund_flow_rank", "tool": "stock_main_fund_flow", "args": {"symbol": main_flow_scope}},
        {"key": "individual_fund_flow_rank", "tool": "stock_individual_fund_flow_rank", "args": {"indicator": rank_indicator}},
        {
            "key": "sector_fund_flow_rank",
            "tool": "stock_sector_fund_flow_rank",
            "args": {"indicator": sector_rank_indicator, "sector_type": sector_type},
        },
        {"key": "big_deal_tracker", "tool": "stock_fund_flow_big_deal", "args": {}},
    ]

