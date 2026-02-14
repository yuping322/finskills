#!/usr/bin/env python3
"""
Portfolio Analytics Engine
==========================
Portfolio risk analysis: concentration, correlation clusters, factor exposure,
VaR/CVaR, stress testing, and health scoring.

Usage:
    python portfolio_analytics.py --holdings "AAPL:30,MSFT:25,GOOGL:20,AMZN:15,META:10"
    python portfolio_analytics.py --holdings "AAPL:30,MSFT:25,GOOGL:20" --benchmark SPY
    python portfolio_analytics.py --holdings-file portfolio.json
"""
import argparse
import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common.utils import output_json, safe_div, safe_float, error_exit, require_dependency


def _parse_holdings(holdings_str: str) -> dict[str, float]:
    """Parse 'AAPL:30,MSFT:25,GOOGL:20' into {ticker: weight%}."""
    holdings = {}
    for part in holdings_str.split(","):
        part = part.strip()
        if ":" in part:
            ticker, weight = part.split(":", 1)
            holdings[ticker.strip().upper()] = float(weight.strip())
        else:
            holdings[part.strip().upper()] = 0  # Equal weight later
    # Normalize if weights don't sum to 100
    total = sum(holdings.values())
    if total == 0:
        # Equal weight
        eq = 100.0 / len(holdings)
        holdings = {k: eq for k in holdings}
    elif abs(total - 100) > 0.5:
        # Normalize to 100%
        holdings = {k: v / total * 100 for k, v in holdings.items()}
    return holdings


def _fetch_returns(tickers: list[str], period_years: float = 3.0):
    """Fetch historical daily returns for a list of tickers."""
    import yfinance as yf
    import pandas as pd

    end = datetime.now()
    start = end - timedelta(days=int(period_years * 365))
    start_str = start.strftime("%Y-%m-%d")
    end_str = end.strftime("%Y-%m-%d")

    prices = yf.download(
        tickers, start=start_str, end=end_str,
        auto_adjust=True, progress=False
    )

    if isinstance(prices.columns, pd.MultiIndex):
        close = prices["Close"]
    else:
        close = prices[["Close"]]
        close.columns = tickers[:1]

    returns = close.pct_change().dropna()
    return returns, close


# ---------------------------------------------------------------------------
# Concentration Analysis
# ---------------------------------------------------------------------------

def concentration_analysis(holdings: dict[str, float]) -> dict:
    """Analyze portfolio concentration at multiple levels."""
    import yfinance as yf

    sorted_holdings = sorted(holdings.items(), key=lambda x: x[1], reverse=True)

    # Single-stock concentration
    single_stock = []
    for ticker, weight in sorted_holdings:
        severity = "safe"
        if weight > 25:
            severity = "critical"
        elif weight > 15:
            severity = "high"
        elif weight > 10:
            severity = "warning"
        elif weight > 5:
            severity = "monitor"
        single_stock.append({
            "ticker": ticker, "weight_pct": round(weight, 2), "severity": severity
        })

    # Top-5 concentration
    top5_weight = sum(w for _, w in sorted_holdings[:5])
    if top5_weight > 70:
        top5_severity = "critical"
    elif top5_weight > 50:
        top5_severity = "high"
    elif top5_weight > 30:
        top5_severity = "moderate"
    else:
        top5_severity = "well_diversified"

    # HHI (Herfindahl-Hirschman Index)
    hhi = sum((w / 100) ** 2 for _, w in sorted_holdings)

    # Sector concentration
    sector_weights = {}
    for ticker, weight in holdings.items():
        try:
            info = yf.Ticker(ticker).info
            sector = info.get("sector", "Unknown")
        except Exception:
            sector = "Unknown"
        sector_weights[sector] = sector_weights.get(sector, 0) + weight

    sector_analysis = []
    for sector, weight in sorted(sector_weights.items(), key=lambda x: x[1],
                                  reverse=True):
        severity = "critical" if weight > 40 else "high" if weight > 30 else "moderate" if weight > 20 else "ok"
        sector_analysis.append({
            "sector": sector, "weight_pct": round(weight, 2), "severity": severity
        })

    return {
        "single_stock": single_stock,
        "top_5": {
            "weight_pct": round(top5_weight, 2),
            "severity": top5_severity,
        },
        "hhi": round(hhi, 4),
        "hhi_interpretation": "concentrated" if hhi > 0.15 else "moderate" if hhi > 0.10 else "diversified",
        "sector_concentration": sector_analysis,
    }


# ---------------------------------------------------------------------------
# Correlation Analysis
# ---------------------------------------------------------------------------

def correlation_analysis(holdings: dict[str, float]) -> dict:
    """Compute correlation matrix and detect correlation clusters."""
    import numpy as np

    tickers = list(holdings.keys())
    returns, _ = _fetch_returns(tickers)

    # Only include tickers with data
    available = [t for t in tickers if t in returns.columns]
    if len(available) < 2:
        return {"error": "Need at least 2 tickers with price data"}

    corr_matrix = returns[available].corr()

    # Detect clusters (groups with avg pairwise correlation > 0.7)
    clusters = []
    used = set()
    for i, t1 in enumerate(available):
        if t1 in used:
            continue
        cluster = [t1]
        for j, t2 in enumerate(available):
            if j <= i or t2 in used:
                continue
            if corr_matrix.loc[t1, t2] > 0.7:
                cluster.append(t2)
        if len(cluster) >= 2:
            cluster_weight = sum(holdings.get(t, 0) for t in cluster)
            avg_corr = np.mean([
                corr_matrix.loc[a, b]
                for ii, a in enumerate(cluster)
                for b in cluster[ii + 1:]
            ])
            clusters.append({
                "tickers": cluster,
                "avg_correlation": round(float(avg_corr), 4),
                "combined_weight_pct": round(cluster_weight, 2),
                "risk_level": (
                    "critical" if cluster_weight > 50
                    else "high" if cluster_weight > 30
                    else "moderate" if cluster_weight > 15
                    else "low"
                ),
            })
            used.update(cluster)

    # Effective Diversification Ratio
    weights = np.array([holdings.get(t, 0) / 100 for t in available])
    weights = weights / weights.sum()  # renormalize after filtering
    vols = returns[available].std() * np.sqrt(252)
    weighted_vol_sum = np.sum(weights * vols.values)
    cov_matrix = returns[available].cov() * 252
    port_var = np.dot(weights, np.dot(cov_matrix.values, weights))
    port_vol = np.sqrt(port_var)
    edr = float(weighted_vol_sum / port_vol) if port_vol > 0 else 1.0

    # Format correlation matrix
    corr_dict = {}
    for t1 in available:
        corr_dict[t1] = {t2: round(float(corr_matrix.loc[t1, t2]), 4)
                          for t2 in available}

    return {
        "correlation_matrix": corr_dict,
        "clusters": clusters,
        "effective_diversification_ratio": round(edr, 4),
        "edr_interpretation": (
            "good" if edr > 1.5
            else "moderate" if edr > 1.2
            else "weak" if edr > 1.0
            else "none"
        ),
    }


# ---------------------------------------------------------------------------
# Risk Metrics
# ---------------------------------------------------------------------------

def risk_metrics(holdings: dict[str, float], benchmark: str = "SPY") -> dict:
    """
    Calculate portfolio-level risk metrics:
    volatility, beta, VaR, CVaR, Sharpe, Sortino, max drawdown.
    """
    import numpy as np

    tickers = list(holdings.keys())
    all_tickers = tickers + ([benchmark] if benchmark not in tickers else [])
    returns, prices = _fetch_returns(all_tickers)

    available = [t for t in tickers if t in returns.columns]
    if not available:
        return {"error": "No price data available"}

    weights = np.array([holdings.get(t, 0) / 100 for t in available])
    weights = weights / weights.sum()  # renormalize

    # Portfolio daily returns
    port_returns = (returns[available] * weights).sum(axis=1)

    # Annualized metrics
    ann_return = float(port_returns.mean() * 252)
    ann_vol = float(port_returns.std() * np.sqrt(252))
    risk_free = 0.045  # approximate current rate

    sharpe = (ann_return - risk_free) / ann_vol if ann_vol > 0 else 0

    # Sortino (downside deviation)
    downside = port_returns[port_returns < 0]
    downside_dev = float(downside.std() * np.sqrt(252)) if len(downside) > 0 else ann_vol
    sortino = (ann_return - risk_free) / downside_dev if downside_dev > 0 else 0

    # VaR and CVaR (historical simulation)
    var_95 = float(np.percentile(port_returns, 5)) * np.sqrt(252)
    var_99 = float(np.percentile(port_returns, 1)) * np.sqrt(252)
    cvar_95 = float(port_returns[port_returns <= np.percentile(port_returns, 5)].mean()) * np.sqrt(252)

    # Max drawdown
    cumulative = (1 + port_returns).cumprod()
    rolling_max = cumulative.cummax()
    drawdowns = (cumulative - rolling_max) / rolling_max
    max_dd = float(drawdowns.min())

    # Beta vs benchmark
    beta = None
    tracking_error = None
    active_share_note = "Requires full benchmark holdings to calculate"
    if benchmark in returns.columns:
        cov = np.cov(port_returns.values, returns[benchmark].values)
        beta = float(cov[0, 1] / cov[1, 1]) if cov[1, 1] > 0 else None

        active_returns = port_returns - returns[benchmark]
        tracking_error = float(active_returns.std() * np.sqrt(252))

    return {
        "annualized_return": round(ann_return, 4),
        "annualized_volatility": round(ann_vol, 4),
        "sharpe_ratio": round(sharpe, 4),
        "sortino_ratio": round(sortino, 4),
        "beta": round(beta, 4) if beta else None,
        "tracking_error": round(tracking_error, 4) if tracking_error else None,
        "var_95_annual": round(var_95, 4),
        "var_99_annual": round(var_99, 4),
        "cvar_95_annual": round(cvar_95, 4),
        "max_drawdown": round(max_dd, 4),
        "risk_free_rate_assumed": risk_free,
        "benchmark": benchmark,
    }


# ---------------------------------------------------------------------------
# Stress Testing
# ---------------------------------------------------------------------------

def stress_test(holdings: dict[str, float]) -> dict:
    """
    Simulate portfolio performance under historical stress scenarios.
    Uses actual sector-level drawdowns as proxy.
    """
    import numpy as np

    # Historical scenario drawdowns by sector (approximate)
    scenarios = {
        "Global Financial Crisis (2007-2009)": {
            "description": "Credit freeze, bank failures, housing collapse",
            "period": "Oct 2007 – Mar 2009",
            "sp500_drawdown": -0.55,
            "sector_drawdowns": {
                "Financial Services": -0.83, "Real Estate": -0.70,
                "Consumer Cyclical": -0.60, "Technology": -0.50,
                "Industrials": -0.55, "Energy": -0.52,
                "Basic Materials": -0.55, "Communication Services": -0.50,
                "Consumer Defensive": -0.28, "Healthcare": -0.35,
                "Utilities": -0.35,
            },
        },
        "COVID Crash (Feb-Mar 2020)": {
            "description": "Pandemic shock, rapid -34% decline, V-shaped recovery",
            "period": "Feb 2020 – Mar 2020",
            "sp500_drawdown": -0.34,
            "sector_drawdowns": {
                "Energy": -0.58, "Financial Services": -0.42,
                "Industrials": -0.38, "Real Estate": -0.35,
                "Consumer Cyclical": -0.35, "Technology": -0.28,
                "Communication Services": -0.30, "Basic Materials": -0.33,
                "Healthcare": -0.25, "Consumer Defensive": -0.18,
                "Utilities": -0.28,
            },
        },
        "2022 Rate Shock": {
            "description": "Aggressive Fed hiking, bonds & stocks down together",
            "period": "Jan 2022 – Oct 2022",
            "sp500_drawdown": -0.25,
            "sector_drawdowns": {
                "Technology": -0.35, "Communication Services": -0.40,
                "Consumer Cyclical": -0.35, "Real Estate": -0.30,
                "Financial Services": -0.20, "Industrials": -0.18,
                "Healthcare": -0.12, "Energy": 0.45,
                "Utilities": -0.05, "Consumer Defensive": -0.05,
                "Basic Materials": -0.10,
            },
        },
        "Dot-Com Bust (2000-2002)": {
            "description": "Tech bubble burst, Nasdaq -78%",
            "period": "Mar 2000 – Oct 2002",
            "sp500_drawdown": -0.49,
            "sector_drawdowns": {
                "Technology": -0.78, "Communication Services": -0.70,
                "Consumer Cyclical": -0.45, "Industrials": -0.40,
                "Financial Services": -0.30, "Healthcare": -0.30,
                "Energy": -0.15, "Consumer Defensive": -0.10,
                "Utilities": -0.40, "Real Estate": -0.15,
                "Basic Materials": -0.25,
            },
        },
        "Inflation Shock (1973-1974)": {
            "description": "Oil embargo, stagflation, broad equity -45%",
            "period": "Jan 1973 – Oct 1974",
            "sp500_drawdown": -0.45,
            "sector_drawdowns": {
                "Consumer Cyclical": -0.50, "Technology": -0.50,
                "Industrials": -0.45, "Financial Services": -0.45,
                "Real Estate": -0.40, "Healthcare": -0.30,
                "Consumer Defensive": -0.25, "Energy": -0.10,
                "Utilities": -0.30, "Basic Materials": -0.35,
                "Communication Services": -0.40,
            },
        },
    }

    # Get sector for each holding
    import yfinance as yf
    holding_sectors = {}
    for ticker in holdings:
        try:
            info = yf.Ticker(ticker).info
            holding_sectors[ticker] = info.get("sector", "Unknown")
        except Exception:
            holding_sectors[ticker] = "Unknown"

    # Simulate each scenario
    results = []
    for name, scenario in scenarios.items():
        sector_dd = scenario["sector_drawdowns"]
        estimated_loss = 0
        holding_impacts = []

        for ticker, weight in holdings.items():
            sector = holding_sectors.get(ticker, "Unknown")
            dd = sector_dd.get(sector, scenario["sp500_drawdown"])
            impact = (weight / 100) * dd
            estimated_loss += impact
            holding_impacts.append({
                "ticker": ticker,
                "sector": sector,
                "weight_pct": round(weight, 2),
                "estimated_drawdown": round(dd, 4),
                "contribution_to_loss": round(impact, 4),
            })

        results.append({
            "scenario": name,
            "description": scenario["description"],
            "period": scenario["period"],
            "sp500_drawdown": scenario["sp500_drawdown"],
            "estimated_portfolio_loss": round(estimated_loss, 4),
            "relative_to_sp500": round(estimated_loss - scenario["sp500_drawdown"], 4),
            "holding_impacts": holding_impacts,
        })

    return {
        "stress_tests": results,
        "worst_case": min(results, key=lambda x: x["estimated_portfolio_loss"]),
        "note": "Estimates based on sector-level drawdowns; actual results may vary",
    }


# ---------------------------------------------------------------------------
# Health Score
# ---------------------------------------------------------------------------

def health_score(holdings: dict[str, float], benchmark: str = "SPY") -> dict:
    """
    Compute a composite 0–100 health score across all dimensions.
    """
    conc = concentration_analysis(holdings)
    corr = correlation_analysis(holdings)
    risk = risk_metrics(holdings, benchmark)
    stress = stress_test(holdings)

    score = 100
    issues = []
    warnings = []
    strengths = []

    # Concentration scoring
    hhi = conc.get("hhi", 0)
    if hhi > 0.25:
        score -= 25
        issues.append(f"Extreme concentration (HHI={hhi:.3f})")
    elif hhi > 0.15:
        score -= 15
        warnings.append(f"High concentration (HHI={hhi:.3f})")
    elif hhi < 0.08:
        strengths.append(f"Well diversified (HHI={hhi:.3f})")

    top5 = conc.get("top_5", {}).get("weight_pct", 0)
    if top5 > 70:
        score -= 15
        issues.append(f"Top 5 positions = {top5:.0f}% of portfolio")
    elif top5 > 50:
        score -= 8
        warnings.append(f"Top 5 positions = {top5:.0f}% of portfolio")

    # Correlation scoring
    edr = corr.get("effective_diversification_ratio", 1)
    if edr < 1.1:
        score -= 15
        issues.append(f"Poor diversification benefit (EDR={edr:.2f})")
    elif edr < 1.3:
        score -= 8
        warnings.append(f"Moderate diversification (EDR={edr:.2f})")
    elif edr > 1.5:
        strengths.append(f"Good diversification benefit (EDR={edr:.2f})")

    clusters = corr.get("clusters", [])
    critical_clusters = [c for c in clusters if c.get("risk_level") in ("critical", "high")]
    if critical_clusters:
        score -= 10
        issues.append(f"{len(critical_clusters)} high-correlation cluster(s) detected")

    # Risk scoring
    vol = risk.get("annualized_volatility", 0)
    if vol > 0.30:
        score -= 10
        warnings.append(f"High volatility ({vol:.1%})")

    max_dd = abs(risk.get("max_drawdown", 0))
    if max_dd > 0.40:
        score -= 10
        issues.append(f"Large historical max drawdown ({max_dd:.1%})")
    elif max_dd > 0.25:
        score -= 5
        warnings.append(f"Moderate historical max drawdown ({max_dd:.1%})")

    sharpe = risk.get("sharpe_ratio", 0)
    if sharpe > 1.0:
        strengths.append(f"Strong risk-adjusted returns (Sharpe={sharpe:.2f})")
    elif sharpe < 0:
        score -= 10
        issues.append(f"Negative risk-adjusted returns (Sharpe={sharpe:.2f})")

    # Stress test scoring
    worst = stress.get("worst_case", {})
    worst_loss = abs(worst.get("estimated_portfolio_loss", 0))
    if worst_loss > 0.60:
        score -= 10
        issues.append(f"Severe stress test loss ({worst_loss:.0%} in {worst.get('scenario', 'N/A')})")

    score = max(0, min(100, score))

    if score >= 80:
        overall = "Healthy"
    elif score >= 60:
        overall = "Needs Attention"
    elif score >= 40:
        overall = "At Risk"
    else:
        overall = "Critical"

    return {
        "health_score": score,
        "overall_assessment": overall,
        "critical_issues": issues,
        "warnings": warnings,
        "strengths": strengths,
        "concentration": conc,
        "correlation": corr,
        "risk_metrics": risk,
        "stress_tests": stress,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Portfolio Analytics Engine"
    )
    parser.add_argument("--holdings", type=str, required=True,
                        help='Holdings string "AAPL:30,MSFT:25,GOOGL:20,..."')
    parser.add_argument("--benchmark", default="SPY",
                        help="Benchmark ticker (default: SPY)")
    parser.add_argument("--concentration", action="store_true",
                        help="Concentration analysis only")
    parser.add_argument("--correlation", action="store_true",
                        help="Correlation analysis only")
    parser.add_argument("--risk", action="store_true",
                        help="Risk metrics only")
    parser.add_argument("--stress", action="store_true",
                        help="Stress testing only")
    parser.add_argument("--health", action="store_true",
                        help="Full health score (default)")
    args = parser.parse_args()

    require_dependency("pandas", requirements_path="US-market/findata-toolkit/requirements.txt")
    require_dependency("numpy", requirements_path="US-market/findata-toolkit/requirements.txt")
    require_dependency("scipy", requirements_path="US-market/findata-toolkit/requirements.txt")
    require_dependency("yfinance", requirements_path="US-market/findata-toolkit/requirements.txt")

    holdings = _parse_holdings(args.holdings)

    try:
        if args.concentration:
            data = concentration_analysis(holdings)
        elif args.correlation:
            data = correlation_analysis(holdings)
        elif args.risk:
            data = risk_metrics(holdings, args.benchmark)
        elif args.stress:
            data = stress_test(holdings)
        else:
            data = health_score(holdings, args.benchmark)

        output_json(data)

    except Exception as e:
        error_exit(f"Error: {e}")


if __name__ == "__main__":
    main()
