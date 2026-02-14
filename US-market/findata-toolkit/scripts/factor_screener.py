#!/usr/bin/env python3
"""
Multi-Factor Stock Screener
============================
Systematic multi-factor scoring engine: value, momentum, quality,
low volatility, size, growth. Score, rank, and screen stocks.

Usage:
    python factor_screener.py --universe "AAPL,MSFT,GOOGL,AMZN,META,NVDA,TSLA,JPM,JNJ,PG"
    python factor_screener.py --universe "AAPL,MSFT,GOOGL" --factors value,quality --top 5
    python factor_screener.py --sp500-sample --top 10
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common.utils import output_json, safe_div, safe_float, error_exit, require_dependency


# ---------------------------------------------------------------------------
# Factor Calculation
# ---------------------------------------------------------------------------

def _get_factor_data(ticker: str) -> dict | None:
    """Fetch all data needed for factor scoring."""
    import yfinance as yf

    try:
        t = yf.Ticker(ticker)
        info = t.info

        # Price data for momentum and volatility
        hist = t.history(period="1y")
        if hist.empty:
            return None

        # 12-month return (skip most recent month for momentum)
        prices = hist["Close"]
        if len(prices) < 22:
            return None

        price_12m_ago = prices.iloc[0] if len(prices) > 252 else prices.iloc[0]
        price_1m_ago = prices.iloc[-22] if len(prices) > 22 else prices.iloc[0]
        price_now = prices.iloc[-1]

        # Momentum: 12-1 month return (skip most recent month)
        mom_12_1 = (price_1m_ago / price_12m_ago - 1) if price_12m_ago > 0 else None

        # Volatility: annualized std of daily returns
        daily_returns = prices.pct_change().dropna()
        volatility = float(daily_returns.std() * (252 ** 0.5)) if len(daily_returns) > 20 else None

        # Beta (approximate)
        beta = safe_float(info.get("beta"))

        # Downside deviation
        neg_returns = daily_returns[daily_returns < 0]
        downside_dev = float(neg_returns.std() * (252 ** 0.5)) if len(neg_returns) > 10 else None

        return {
            "ticker": ticker,
            "name": info.get("longName") or info.get("shortName", ticker),
            "sector": info.get("sector", "Unknown"),
            "market_cap": safe_float(info.get("marketCap")),
            # Value
            "pe_trailing": safe_float(info.get("trailingPE")),
            "pb": safe_float(info.get("priceToBook")),
            "ps": safe_float(info.get("priceToSalesTrailing12Months")),
            "ev_ebitda": safe_float(info.get("enterpriseToEbitda")),
            "dividend_yield": safe_float(info.get("dividendYield")),
            "fcf_yield": safe_div(
                safe_float(info.get("freeCashflow")),
                safe_float(info.get("marketCap"))
            ),
            # Momentum
            "momentum_12_1": mom_12_1,
            "earnings_growth": safe_float(info.get("earningsGrowth")),
            # Quality
            "roe": safe_float(info.get("returnOnEquity")),
            "roa": safe_float(info.get("returnOnAssets")),
            "debt_to_equity": safe_float(info.get("debtToEquity")),
            "current_ratio": safe_float(info.get("currentRatio")),
            "profit_margin": safe_float(info.get("profitMargins")),
            "operating_margin": safe_float(info.get("operatingMargins")),
            # Volatility
            "volatility_1y": volatility,
            "beta": beta,
            "downside_deviation": downside_dev,
            # Size
            # (market_cap already above)
            # Growth
            "revenue_growth": safe_float(info.get("revenueGrowth")),
            "earnings_quarterly_growth": safe_float(info.get("earningsQuarterlyGrowth")),
            "gross_margins": safe_float(info.get("grossMargins")),
        }
    except Exception:
        return None


def _percentile_rank(values: list[float | None], higher_is_better: bool = True) -> list[float | None]:
    """Convert values to percentile ranks (0-100). None values stay None."""
    import numpy as np

    valid = [(i, v) for i, v in enumerate(values) if v is not None]
    if not valid:
        return [None] * len(values)

    indices, vals = zip(*valid)
    sorted_vals = sorted(vals, reverse=not higher_is_better)
    ranks = {v: r for r, v in enumerate(sorted_vals)}

    result = [None] * len(values)
    n = len(valid)
    for idx, val in zip(indices, vals):
        rank = sorted_vals.index(val)
        result[idx] = round((1 - rank / max(n - 1, 1)) * 100, 2)

    return result


def calculate_factor_scores(stock_data: list[dict],
                             factors: list[str] | None = None,
                             weights: dict[str, float] | None = None) -> list[dict]:
    """
    Calculate factor scores for a list of stocks.
    Returns scored and ranked results.
    """
    all_factors = ["value", "momentum", "quality", "low_volatility", "size", "growth"]
    active_factors = factors or all_factors

    if weights is None:
        w = {f: 1.0 / len(active_factors) for f in active_factors}
    else:
        total_w = sum(weights.values())
        w = {f: weights.get(f, 0) / total_w for f in active_factors}

    n = len(stock_data)

    # --- Calculate raw factor scores ---

    # Value: earnings yield (1/PE), book/price (1/PB), FCF yield
    # Higher value = cheaper = better
    val_scores = []
    for d in stock_data:
        pe = d.get("pe_trailing")
        earnings_yield = 1.0 / pe if pe and pe > 0 else None
        pb = d.get("pb")
        bp = 1.0 / pb if pb and pb > 0 else None
        fcf_y = d.get("fcf_yield")
        # Composite
        parts = [x for x in [earnings_yield, bp, fcf_y] if x is not None]
        val_scores.append(sum(parts) / len(parts) if parts else None)

    # Momentum: 12-1 month return + earnings growth
    mom_scores = []
    for d in stock_data:
        m = d.get("momentum_12_1")
        eg = d.get("earnings_growth")
        parts = [x for x in [m, eg] if x is not None]
        mom_scores.append(sum(parts) / len(parts) if parts else None)

    # Quality: ROE, profit margin, low debt
    qual_scores = []
    for d in stock_data:
        roe = d.get("roe")
        pm = d.get("profit_margin")
        de = d.get("debt_to_equity")
        inv_de = 1.0 / (1 + de / 100) if de is not None and de >= 0 else None
        parts = [x for x in [roe, pm, inv_de] if x is not None]
        qual_scores.append(sum(parts) / len(parts) if parts else None)

    # Low Volatility: inverse of volatility + inverse of beta
    lvol_scores = []
    for d in stock_data:
        vol = d.get("volatility_1y")
        inv_vol = 1.0 / vol if vol and vol > 0 else None
        beta = d.get("beta")
        inv_beta = 1.0 / beta if beta and beta > 0 else None
        parts = [x for x in [inv_vol, inv_beta] if x is not None]
        lvol_scores.append(sum(parts) / len(parts) if parts else None)

    # Size: inverse of market cap (smaller = higher score)
    size_scores = []
    for d in stock_data:
        mc = d.get("market_cap")
        size_scores.append(1.0 / (mc / 1e9) if mc and mc > 0 else None)

    # Growth: revenue growth + earnings growth + margin expansion
    growth_scores = []
    for d in stock_data:
        rg = d.get("revenue_growth")
        eg = d.get("earnings_quarterly_growth")
        parts = [x for x in [rg, eg] if x is not None]
        growth_scores.append(sum(parts) / len(parts) if parts else None)

    # --- Percentile rank each factor ---
    factor_percentiles = {
        "value": _percentile_rank(val_scores, higher_is_better=True),
        "momentum": _percentile_rank(mom_scores, higher_is_better=True),
        "quality": _percentile_rank(qual_scores, higher_is_better=True),
        "low_volatility": _percentile_rank(lvol_scores, higher_is_better=True),
        "size": _percentile_rank(size_scores, higher_is_better=True),
        "growth": _percentile_rank(growth_scores, higher_is_better=True),
    }

    # --- Composite score ---
    results = []
    for i, d in enumerate(stock_data):
        scores = {}
        composite = 0
        for f in active_factors:
            pct = factor_percentiles.get(f, [None] * n)[i]
            scores[f] = pct
            if pct is not None:
                composite += w.get(f, 0) * pct

        results.append({
            "ticker": d["ticker"],
            "name": d.get("name", ""),
            "sector": d.get("sector", ""),
            "market_cap": d.get("market_cap"),
            "factor_scores": scores,
            "composite_score": round(composite, 2),
        })

    # Sort by composite score
    results.sort(key=lambda x: x["composite_score"], reverse=True)

    # Add rank
    for i, r in enumerate(results):
        r["rank"] = i + 1

    return results


# ---------------------------------------------------------------------------
# Factor Crowding Assessment
# ---------------------------------------------------------------------------

def assess_factor_crowding(scored_stocks: list[dict],
                            active_factors: list[str]) -> dict:
    """Assess whether selected factors appear crowded."""
    crowding = {}
    for factor in active_factors:
        scores = [s["factor_scores"].get(factor) for s in scored_stocks
                  if s["factor_scores"].get(factor) is not None]
        if not scores:
            continue

        import numpy as np
        spread = np.std(scores)
        # Low spread = more stocks cluster around same score = more crowded
        if spread < 15:
            level = "crowded"
            note = "Low dispersion — many stocks scoring similarly"
        elif spread < 25:
            level = "moderate"
            note = "Normal dispersion"
        else:
            level = "uncrowded"
            note = "High dispersion — opportunity for differentiation"

        crowding[factor] = {
            "dispersion": round(float(spread), 2),
            "level": level,
            "note": note,
        }

    return crowding


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Multi-Factor Stock Screener"
    )
    parser.add_argument("--universe", type=str,
                        help="Comma-separated tickers")
    parser.add_argument("--sp500-sample", action="store_true",
                        help="Use a sample of S&P 500 stocks")
    parser.add_argument("--factors", type=str, default=None,
                        help="Comma-separated factors (value,momentum,quality,low_volatility,size,growth)")
    parser.add_argument("--top", type=int, default=10,
                        help="Number of top stocks to return")
    args = parser.parse_args()

    require_dependency("pandas", requirements_path="US-market/findata-toolkit/requirements.txt")
    require_dependency("yfinance", requirements_path="US-market/findata-toolkit/requirements.txt")

    if args.sp500_sample:
        tickers = [
            "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA",
            "JPM", "JNJ", "PG", "UNH", "V", "MA", "HD", "DIS",
            "COST", "PEP", "ABBV", "MRK", "KO", "WMT", "CSCO",
            "CRM", "ABT", "AVGO", "LLY", "TMO", "NKE", "ORCL", "ACN",
        ]
    elif args.universe:
        tickers = [t.strip().upper() for t in args.universe.split(",")]
    else:
        error_exit("Provide --universe or --sp500-sample")
        return

    factors = args.factors.split(",") if args.factors else None

    print(f"Fetching data for {len(tickers)} stocks...", file=sys.stderr)

    # Fetch data
    stock_data = []
    for ticker in tickers:
        d = _get_factor_data(ticker)
        if d:
            stock_data.append(d)
        else:
            print(f"  Warning: Could not fetch data for {ticker}", file=sys.stderr)

    if not stock_data:
        error_exit("No stock data retrieved")
        return

    # Calculate scores
    scored = calculate_factor_scores(stock_data, factors=factors)
    top = scored[:args.top]

    # Crowding
    active = factors or ["value", "momentum", "quality", "low_volatility", "size", "growth"]
    crowding = assess_factor_crowding(scored, active)

    result = {
        "universe_size": len(tickers),
        "stocks_analyzed": len(stock_data),
        "factors_used": active,
        "factor_weights": {f: round(1 / len(active), 4) for f in active},
        "top_picks": top,
        "factor_crowding": crowding,
    }

    output_json(result)


if __name__ == "__main__":
    main()
