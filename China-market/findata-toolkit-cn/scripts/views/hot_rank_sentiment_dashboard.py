from __future__ import annotations

import re

VIEW_NAME = "hot_rank_sentiment_dashboard"
DESCRIPTION = "人气/热度与情绪代理聚合：人气榜、相关股票、关注指数、投票等（工具聚合视图）。"
PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "symbol": {"type": "string", "description": "东方财富人气榜股票标识（如 SZ000665），可选"},
        "comment_symbol": {"type": "string", "description": "千股千评/关注指数用股票代码（如 600000），可选"},
        "xq_hot_deal_symbol": {"type": "string", "description": "雪球交易热度榜：最热门/本周新增"},
        "include_vote": {"type": "boolean", "description": "是否附带百度股评投票"},
        "vote_indicator": {"type": "string", "description": "指数/股票"},
    },
    "required": [],
}


def _extract_6d(code: str) -> str | None:
    m = re.search(r"(\\d{6})", code or "")
    return m.group(1) if m else None


def plan(params: dict) -> list[dict]:
    calls: list[dict] = [
        {"key": "hot_rank_list", "tool": "stock_hot_rank_em", "args": {}},
        {"key": "xq_hot_deal", "tool": "stock_hot_deal_xq", "args": {"symbol": params.get("xq_hot_deal_symbol") or "最热门"}},
    ]

    symbol = params.get("symbol")
    if symbol:
        calls.extend(
            [
                {"key": "hot_rank_latest", "tool": "stock_hot_rank_latest_em", "args": {"symbol": str(symbol)}},
                {"key": "hot_rank_detail", "tool": "stock_hot_rank_detail_em", "args": {"symbol": str(symbol)}},
                {"key": "hot_rank_relate", "tool": "stock_hot_rank_relate_em", "args": {"symbol": str(symbol)}},
            ]
        )

    comment_symbol = params.get("comment_symbol") or (_extract_6d(str(symbol)) if symbol else None)
    if comment_symbol:
        calls.append({"key": "comment_focus", "tool": "stock_comment_detail_scrd_focus_em", "args": {"symbol": str(comment_symbol)}})
        calls.append({"key": "comment_desire", "tool": "stock_comment_detail_scrd_desire_em", "args": {"symbol": str(comment_symbol)}})
        calls.append({"key": "comment_score", "tool": "stock_comment_detail_zhpj_lspf_em", "args": {"symbol": str(comment_symbol)}})

        if params.get("include_vote"):
            calls.append(
                {
                    "key": "baidu_vote",
                    "tool": "stock_zh_vote_baidu",
                    "args": {"symbol": str(comment_symbol), "indicator": params.get("vote_indicator") or "股票"},
                }
            )

    return calls

