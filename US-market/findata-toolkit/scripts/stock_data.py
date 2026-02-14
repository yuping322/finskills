#!/usr/bin/env python3
"""
US Market Stock Data Fetcher
============================
Fetch stock fundamentals, price history, and financial metrics using yfinance.
No API key required.

Usage:
    python stock_data.py AAPL MSFT GOOGL              # Basic info
    python stock_data.py AAPL --metrics                # Full financial metrics
    python stock_data.py AAPL --history --period 1y    # Price history
    python stock_data.py AAPL MSFT --screen            # Screen with filters
"""
import argparse
import sys
from pathlib import Path

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common.utils import output_json, safe_div, safe_float, error_exit, require_dependency


def _get_ticker(symbol: str):
    """Return a yfinance Ticker object."""
    import yfinance as yf
    return yf.Ticker(symbol)


def fetch_basic_info(symbols: list[str]) -> list[dict]:
    """Fetch basic company info for a list of tickers."""
    import yfinance as yf

    results = []
    for sym in symbols:
        try:
            t = yf.Ticker(sym)
            info = t.info
            results.append({
                "symbol": sym,
                "name": info.get("longName") or info.get("shortName", sym),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "market_cap": info.get("marketCap"),
                "currency": info.get("currency", "USD"),
                "exchange": info.get("exchange"),
                "country": info.get("country"),
                "website": info.get("website"),
                "description": info.get("longBusinessSummary", "")[:300],
            })
        except Exception as e:
            results.append({"symbol": sym, "error": str(e)})
    return results


def fetch_financial_metrics(symbol: str) -> dict:
    """
    Fetch comprehensive financial metrics for a single stock.
    Covers valuation, profitability, leverage, growth, and cash flow.
    """
    import yfinance as yf

    t = yf.Ticker(symbol)
    info = t.info

    # --- Valuation ---
    pe_trailing = safe_float(info.get("trailingPE"))
    pe_forward = safe_float(info.get("forwardPE"))
    pb = safe_float(info.get("priceToBook"))
    ps = safe_float(info.get("priceToSalesTrailing12Months"))
    ev_ebitda = safe_float(info.get("enterpriseToEbitda"))
    ev_revenue = safe_float(info.get("enterpriseToRevenue"))
    peg = safe_float(info.get("pegRatio"))
    dividend_yield = safe_float(info.get("dividendYield"))

    # --- Profitability ---
    gross_margin = safe_float(info.get("grossMargins"))
    operating_margin = safe_float(info.get("operatingMargins"))
    profit_margin = safe_float(info.get("profitMargins"))
    roe = safe_float(info.get("returnOnEquity"))
    roa = safe_float(info.get("returnOnAssets"))

    # --- Leverage ---
    debt_to_equity = safe_float(info.get("debtToEquity"))
    current_ratio = safe_float(info.get("currentRatio"))
    quick_ratio = safe_float(info.get("quickRatio"))

    # --- Cash flow ---
    fcf = safe_float(info.get("freeCashflow"))
    operating_cf = safe_float(info.get("operatingCashflow"))
    market_cap = safe_float(info.get("marketCap"))
    fcf_yield = safe_div(fcf, market_cap)

    # --- Growth ---
    revenue_growth = safe_float(info.get("revenueGrowth"))
    earnings_growth = safe_float(info.get("earningsGrowth"))
    earnings_quarterly_growth = safe_float(info.get("earningsQuarterlyGrowth"))

    # --- Analyst consensus ---
    target_mean = safe_float(info.get("targetMeanPrice"))
    target_high = safe_float(info.get("targetHighPrice"))
    target_low = safe_float(info.get("targetLowPrice"))
    current_price = safe_float(info.get("currentPrice"))
    recommendation = info.get("recommendationKey")
    num_analysts = safe_float(info.get("numberOfAnalystOpinions"))
    upside = safe_div(
        (target_mean - current_price) if target_mean and current_price else None,
        current_price,
    )

    # --- Enterprise value ---
    enterprise_value = safe_float(info.get("enterpriseValue"))
    total_revenue = safe_float(info.get("totalRevenue"))
    ebitda = safe_float(info.get("ebitda"))
    total_debt = safe_float(info.get("totalDebt"))
    total_cash = safe_float(info.get("totalCash"))

    # --- ROIC (approximate) ---
    net_income = safe_float(info.get("netIncomeToCommon"))
    book_value = safe_float(info.get("bookValue"))
    shares = safe_float(info.get("sharesOutstanding"))
    total_equity = book_value * shares if book_value and shares else None
    invested_capital = (
        (total_equity + (total_debt or 0) - (total_cash or 0))
        if total_equity is not None
        else None
    )
    roic = safe_div(net_income, invested_capital)

    return {
        "symbol": symbol,
        "name": info.get("longName") or info.get("shortName", symbol),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "current_price": current_price,
        "market_cap": market_cap,
        "valuation": {
            "pe_trailing": pe_trailing,
            "pe_forward": pe_forward,
            "pb": pb,
            "ps": ps,
            "ev_ebitda": ev_ebitda,
            "ev_revenue": ev_revenue,
            "peg": peg,
            "fcf_yield": fcf_yield,
            "dividend_yield": dividend_yield,
        },
        "profitability": {
            "gross_margin": gross_margin,
            "operating_margin": operating_margin,
            "profit_margin": profit_margin,
            "roe": roe,
            "roa": roa,
            "roic": roic,
        },
        "leverage": {
            "debt_to_equity": debt_to_equity,
            "current_ratio": current_ratio,
            "quick_ratio": quick_ratio,
            "total_debt": total_debt,
            "total_cash": total_cash,
        },
        "cash_flow": {
            "free_cash_flow": fcf,
            "operating_cash_flow": operating_cf,
        },
        "growth": {
            "revenue_growth_yoy": revenue_growth,
            "earnings_growth_yoy": earnings_growth,
            "earnings_quarterly_growth": earnings_quarterly_growth,
        },
        "analyst_consensus": {
            "recommendation": recommendation,
            "target_mean": target_mean,
            "target_high": target_high,
            "target_low": target_low,
            "upside_pct": upside,
            "num_analysts": num_analysts,
        },
        "enterprise": {
            "enterprise_value": enterprise_value,
            "total_revenue": total_revenue,
            "ebitda": ebitda,
        },
    }


def fetch_price_history(symbol: str, period: str = "1y",
                        interval: str = "1d") -> dict:
    """Fetch historical OHLCV data."""
    import yfinance as yf

    t = yf.Ticker(symbol)
    hist = t.history(period=period, interval=interval)

    if hist.empty:
        return {"symbol": symbol, "error": "No price data found"}

    records = []
    for dt, row in hist.iterrows():
        records.append({
            "date": dt.strftime("%Y-%m-%d"),
            "open": round(float(row["Open"]), 2),
            "high": round(float(row["High"]), 2),
            "low": round(float(row["Low"]), 2),
            "close": round(float(row["Close"]), 2),
            "volume": int(row["Volume"]),
        })

    return {
        "symbol": symbol,
        "period": period,
        "interval": interval,
        "data_points": len(records),
        "start_date": records[0]["date"],
        "end_date": records[-1]["date"],
        "prices": records,
    }


def fetch_financial_statements(symbol: str) -> dict:
    """Fetch income statement, balance sheet, and cash flow statement."""
    import yfinance as yf

    t = yf.Ticker(symbol)

    def _df_to_records(df):
        if df is None or df.empty:
            return []
        records = []
        for col in df.columns:
            period_data = {"period": col.strftime("%Y-%m-%d")}
            for idx in df.index:
                val = df.loc[idx, col]
                period_data[str(idx)] = safe_float(val)
            records.append(period_data)
        return records

    return {
        "symbol": symbol,
        "income_statement": _df_to_records(t.income_stmt),
        "balance_sheet": _df_to_records(t.balance_sheet),
        "cash_flow": _df_to_records(t.cashflow),
    }


def screen_stocks(symbols: list[str], filters: dict | None = None) -> dict:
    """
    Screen a list of stocks against financial filters.

    Default filters (can be overridden):
        pe_below_industry: True   (P/E below sector average)
        min_revenue_growth: 0.0   (positive revenue growth)
        max_debt_to_equity: 200   (D/E below 200%)
        min_fcf: 0                (positive free cash flow)
        min_roic: 0               (positive ROIC)
        min_upside: 0.30          (30% analyst upside)
    """
    defaults = {
        "min_revenue_growth": 0.0,
        "max_debt_to_equity": 200.0,
        "min_fcf": 0,
        "min_roic": 0.0,
        "min_upside": 0.30,
    }
    if filters:
        defaults.update(filters)

    passing = []
    failing = []

    for sym in symbols:
        try:
            m = fetch_financial_metrics(sym)
            if "error" in m:
                failing.append({"symbol": sym, "reason": m["error"]})
                continue

            reasons = []
            rev_g = m["growth"]["revenue_growth_yoy"]
            if rev_g is not None and rev_g < defaults["min_revenue_growth"]:
                reasons.append(f"revenue_growth {rev_g:.2%} < {defaults['min_revenue_growth']:.2%}")

            de = m["leverage"]["debt_to_equity"]
            if de is not None and de > defaults["max_debt_to_equity"]:
                reasons.append(f"debt_to_equity {de:.1f} > {defaults['max_debt_to_equity']:.1f}")

            fcf = m["cash_flow"]["free_cash_flow"]
            if fcf is not None and fcf < defaults["min_fcf"]:
                reasons.append(f"free_cash_flow {fcf:,.0f} < {defaults['min_fcf']}")

            roic = m["profitability"]["roic"]
            if roic is not None and roic < defaults["min_roic"]:
                reasons.append(f"roic {roic:.2%} < {defaults['min_roic']:.2%}")

            upside = m["analyst_consensus"]["upside_pct"]
            if upside is not None and upside < defaults["min_upside"]:
                reasons.append(f"upside {upside:.2%} < {defaults['min_upside']:.2%}")

            if reasons:
                failing.append({"symbol": sym, "reasons": reasons})
            else:
                passing.append(m)

        except Exception as e:
            failing.append({"symbol": sym, "reason": str(e)})

    return {
        "filters_applied": defaults,
        "total_screened": len(symbols),
        "passed": len(passing),
        "failed": len(failing),
        "results": passing,
        "rejected": failing,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="US Market Stock Data Fetcher (yfinance, no API key)"
    )
    parser.add_argument("symbols", nargs="+", help="Stock ticker(s)")
    parser.add_argument("--metrics", action="store_true",
                        help="Full financial metrics")
    parser.add_argument("--history", action="store_true",
                        help="Price history")
    parser.add_argument("--financials", action="store_true",
                        help="Financial statements (income, balance, cash flow)")
    parser.add_argument("--screen", action="store_true",
                        help="Screen against default value filters")
    parser.add_argument("--period", default="1y",
                        help="History period (1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max)")
    parser.add_argument("--min-upside", type=float, default=0.30,
                        help="Minimum analyst upside for screening (default 0.30)")
    args = parser.parse_args()

    require_dependency("pandas", requirements_path="US-market/findata-toolkit/requirements.txt")
    require_dependency("yfinance", requirements_path="US-market/findata-toolkit/requirements.txt")

    try:
        if args.screen:
            data = screen_stocks(args.symbols,
                                 {"min_upside": args.min_upside})
        elif args.metrics:
            if len(args.symbols) == 1:
                data = fetch_financial_metrics(args.symbols[0])
            else:
                data = [fetch_financial_metrics(s) for s in args.symbols]
        elif args.history:
            data = fetch_price_history(args.symbols[0], period=args.period)
        elif args.financials:
            data = fetch_financial_statements(args.symbols[0])
        else:
            data = fetch_basic_info(args.symbols)

        output_json(data)

    except Exception as e:
        error_exit(f"Error fetching data: {e}")


if __name__ == "__main__":
    main()
