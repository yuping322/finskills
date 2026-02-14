from __future__ import annotations

from ._helpers import ensure_yyyymmdd, today_yyyymmdd

VIEW_NAME = "hsgt_dashboard"
DESCRIPTION = "沪深港通/北向资金聚合：资金流、历史序列、持股排行、板块增持排行（工具聚合视图）。"
PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "hist_symbol": {"type": "string", "description": "北向资金/沪股通/深股通/南向资金/港股通沪/港股通深"},
        "hold_market": {"type": "string", "description": "北向/沪股通/深股通"},
        "hold_indicator": {"type": "string", "description": "今日排行/3日排行/5日排行/10日排行/月排行/季排行/年排行"},
        "board_rank_symbol": {"type": "string", "description": "北向资金增持行业板块排行/概念板块排行/地域板块排行"},
        "board_rank_indicator": {"type": "string", "description": "今日/3日/5日/10日/1月/1季/1年"},
        "individual_symbol": {"type": "string", "description": "个股代码（可选；用于查询单股持仓明细）"},
        "start_date": {"type": "string", "description": "YYYYMMDD（可选；用于统计/明细）"},
        "end_date": {"type": "string", "description": "YYYYMMDD（可选；用于统计/明细）"},
    },
    "required": [],
}


def plan(params: dict) -> list[dict]:
    hist_symbol = params.get("hist_symbol") or "北向资金"
    hold_market = params.get("hold_market") or "北向"
    hold_indicator = params.get("hold_indicator") or "今日排行"
    board_rank_symbol = params.get("board_rank_symbol") or "北向资金增持行业板块排行"
    board_rank_indicator = params.get("board_rank_indicator") or "今日"

    calls: list[dict] = [
        {"key": "fund_flow_summary", "tool": "stock_hsgt_fund_flow_summary_em", "args": {}},
        {"key": "hist", "tool": "stock_hsgt_hist_em", "args": {"symbol": hist_symbol}},
        {"key": "hold_stock_rank", "tool": "stock_hsgt_hold_stock_em", "args": {"market": hold_market, "indicator": hold_indicator}},
        {"key": "board_rank", "tool": "stock_hsgt_board_rank_em", "args": {"symbol": board_rank_symbol, "indicator": board_rank_indicator}},
        {"key": "fund_min", "tool": "stock_hsgt_fund_min_em", "args": {"symbol": "北向资金"}},
    ]

    individual_symbol = params.get("individual_symbol")
    if individual_symbol:
        calls.append({"key": "individual", "tool": "stock_hsgt_individual_em", "args": {"symbol": str(individual_symbol)}})

        start_date = params.get("start_date")
        end_date = params.get("end_date")
        if start_date or end_date:
            sd = ensure_yyyymmdd(str(start_date or today_yyyymmdd()), field="start_date")
            ed = ensure_yyyymmdd(str(end_date or today_yyyymmdd()), field="end_date")
            calls.append(
                {
                    "key": "individual_detail",
                    "tool": "stock_hsgt_individual_detail_em",
                    "args": {"symbol": str(individual_symbol), "start_date": sd, "end_date": ed},
                }
            )

    start_date = params.get("start_date")
    end_date = params.get("end_date")
    if start_date and end_date:
        sd = ensure_yyyymmdd(str(start_date), field="start_date")
        ed = ensure_yyyymmdd(str(end_date), field="end_date")
        calls.append(
            {"key": "stock_statistics", "tool": "stock_hsgt_stock_statistics_em", "args": {"symbol": "北向持股", "start_date": sd, "end_date": ed}}
        )
        calls.append(
            {"key": "institution_statistics", "tool": "stock_hsgt_institution_statistics_em", "args": {"market": "北向持股", "start_date": sd, "end_date": ed}}
        )

    return calls

