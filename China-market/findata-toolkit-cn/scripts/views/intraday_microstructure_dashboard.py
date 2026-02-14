from __future__ import annotations

from ._helpers import ensure_yyyymmdd, today_yyyymmdd

VIEW_NAME = "intraday_microstructure_dashboard"
DESCRIPTION = "日内微观结构聚合：盘口/分时/分钟线（工具聚合视图）。"
PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "symbol": {"type": "string", "description": "股票代码（6位）"},
        "date": {"type": "string", "description": "交易日 YYYYMMDD（可选；用于新浪日内分时）"},
        "minute_period": {"type": "string", "description": "分钟频率：1/5/15/30/60（可选）"},
        "minute_adjust": {"type": "string", "description": "复权：''/qfq/hfq（可选）"},
    },
    "required": ["symbol"],
}


def _infer_market_prefix(symbol_6d: str) -> str:
    s = symbol_6d.strip()[-6:]
    if s.startswith("6"):
        return "sh"
    if s.startswith(("0", "3")):
        return "sz"
    if s.startswith(("4", "8")):
        return "bj"
    return "sz"


def plan(params: dict) -> list[dict]:
    symbol = params.get("symbol")
    if not symbol:
        raise ValueError("symbol is required")
    sym6 = str(symbol).strip()[-6:]
    market = _infer_market_prefix(sym6)

    calls: list[dict] = [
        {"key": "bid_ask", "tool": "stock_bid_ask_em", "args": {"symbol": sym6}},
        {"key": "intraday_em", "tool": "stock_intraday_em", "args": {"symbol": sym6}},
    ]

    date = params.get("date")
    if date:
        d = ensure_yyyymmdd(str(date), field="date")
        calls.append({"key": "intraday_sina", "tool": "stock_intraday_sina", "args": {"symbol": f"{market}{sym6}", "date": d}})

    minute_period = params.get("minute_period")
    if minute_period:
        calls.append(
            {
                "key": "minute_bars",
                "tool": "stock_zh_a_minute",
                "args": {"symbol": f"{market}{sym6}", "period": str(minute_period), "adjust": params.get("minute_adjust") or ""},
            }
        )

    return calls
