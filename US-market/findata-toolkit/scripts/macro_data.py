#!/usr/bin/env python3
"""
US Macro Economic Data Fetcher
================================
Fetch macro indicators from FRED (Federal Reserve Economic Data).
No API key required for basic usage.

Covers: interest rates, inflation, GDP, employment, yield curve, PMI.

Usage:
    python macro_data.py --dashboard                  # All key indicators
    python macro_data.py --rates                      # Interest rate data
    python macro_data.py --inflation                  # Inflation data
    python macro_data.py --gdp                        # GDP data
    python macro_data.py --employment                 # Employment data
    python macro_data.py --cycle                      # Business cycle assessment
"""
import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common.utils import output_json, safe_float, error_exit


def _fetch_fred_series(series_id: str, start: str | None = None,
                        periods: int = 24) -> list[dict]:
    """Fetch a FRED series. Returns list of {date, value} dicts."""
    try:
        import pandas_datareader.data as web
        if start is None:
            start = (datetime.now() - timedelta(days=periods * 31)).strftime("%Y-%m-%d")
        df = web.DataReader(series_id, "fred", start=start)
        records = []
        for dt, row in df.iterrows():
            val = safe_float(row.iloc[0])
            if val is not None:
                records.append({
                    "date": dt.strftime("%Y-%m-%d"),
                    "value": val,
                })
        return records
    except Exception as e:
        return [{"error": str(e)}]


def _latest_value(series: list[dict]) -> float | None:
    """Get the latest value from a FRED series."""
    for entry in reversed(series):
        if "value" in entry:
            return entry["value"]
    return None


def _direction(series: list[dict], lookback: int = 6) -> str:
    """Determine if a series is rising, falling, or stable."""
    values = [e["value"] for e in series if "value" in e]
    if len(values) < 2:
        return "insufficient_data"
    recent = values[-lookback:] if len(values) >= lookback else values
    if len(recent) < 2:
        return "insufficient_data"
    first = recent[0]
    last = recent[-1]
    change = (last - first) / abs(first) if first != 0 else 0
    if change > 0.05:
        return "rising"
    elif change < -0.05:
        return "falling"
    return "stable"


# ---------------------------------------------------------------------------
# Interest Rates
# ---------------------------------------------------------------------------

def fetch_rates() -> dict:
    """Fetch key interest rate data."""
    fed_funds = _fetch_fred_series("FEDFUNDS")
    t2y = _fetch_fred_series("DGS2")
    t10y = _fetch_fred_series("DGS10")
    t30y = _fetch_fred_series("DGS30")
    t3m = _fetch_fred_series("DGS3MO")

    # Yield curve spread
    t10y_val = _latest_value(t10y)
    t2y_val = _latest_value(t2y)
    t3m_val = _latest_value(t3m)
    spread_10_2 = round(t10y_val - t2y_val, 4) if t10y_val and t2y_val else None
    spread_10_3m = round(t10y_val - t3m_val, 4) if t10y_val and t3m_val else None

    return {
        "fed_funds_rate": {
            "latest": _latest_value(fed_funds),
            "direction": _direction(fed_funds),
            "series": fed_funds[-12:],
        },
        "treasury_2y": {
            "latest": _latest_value(t2y),
            "direction": _direction(t2y),
        },
        "treasury_10y": {
            "latest": _latest_value(t10y),
            "direction": _direction(t10y),
        },
        "treasury_30y": {
            "latest": _latest_value(t30y),
            "direction": _direction(t30y),
        },
        "yield_curve": {
            "spread_10y_2y": spread_10_2,
            "spread_10y_3m": spread_10_3m,
            "inverted": spread_10_2 is not None and spread_10_2 < 0,
            "interpretation": (
                "Inverted — historically signals recession within 12-24 months"
                if spread_10_2 and spread_10_2 < 0
                else "Normal — economy likely expanding"
                if spread_10_2 and spread_10_2 > 0.5
                else "Flat — transition period, uncertainty"
            ),
        },
    }


# ---------------------------------------------------------------------------
# Inflation
# ---------------------------------------------------------------------------

def fetch_inflation() -> dict:
    """Fetch inflation indicators."""
    cpi = _fetch_fred_series("CPIAUCSL")
    core_cpi = _fetch_fred_series("CPILFESL")
    pce = _fetch_fred_series("PCEPI")
    core_pce = _fetch_fred_series("PCEPILFE")
    breakeven_5y = _fetch_fred_series("T5YIE")
    breakeven_10y = _fetch_fred_series("T10YIE")

    # Calculate YoY CPI
    cpi_values = [e for e in cpi if "value" in e]
    cpi_yoy = None
    if len(cpi_values) >= 13:
        latest = cpi_values[-1]["value"]
        year_ago = cpi_values[-13]["value"]
        if year_ago:
            cpi_yoy = round((latest / year_ago - 1) * 100, 2)

    return {
        "cpi_yoy": {
            "latest": cpi_yoy,
            "direction": _direction(cpi),
            "interpretation": (
                f"CPI YoY: {cpi_yoy}%" if cpi_yoy else "N/A"
            ),
        },
        "core_pce": {
            "latest": _latest_value(core_pce),
            "direction": _direction(core_pce),
            "fed_target": "2.0%",
        },
        "breakeven_inflation": {
            "5y": _latest_value(breakeven_5y),
            "10y": _latest_value(breakeven_10y),
            "interpretation": "Market-implied inflation expectations",
        },
    }


# ---------------------------------------------------------------------------
# GDP
# ---------------------------------------------------------------------------

def fetch_gdp() -> dict:
    """Fetch GDP and growth indicators."""
    gdp = _fetch_fred_series("GDP", periods=20)
    gdp_growth = _fetch_fred_series("A191RL1Q225SBEA", periods=20)  # Real GDP growth
    lei = _fetch_fred_series("USSLIND")  # Leading Economic Index
    ism_pmi = _fetch_fred_series("MANEMP")  # Manufacturing employment as proxy

    return {
        "real_gdp_growth": {
            "latest_quarterly": _latest_value(gdp_growth),
            "direction": _direction(gdp_growth),
            "series": gdp_growth[-8:],
        },
        "leading_economic_index": {
            "latest": _latest_value(lei),
            "direction": _direction(lei),
            "interpretation": (
                "Declining LEI — potential recession signal"
                if _direction(lei) == "falling"
                else "Rising LEI — expansion likely continues"
                if _direction(lei) == "rising"
                else "Stable LEI"
            ),
        },
    }


# ---------------------------------------------------------------------------
# Employment
# ---------------------------------------------------------------------------

def fetch_employment() -> dict:
    """Fetch employment indicators."""
    unemployment = _fetch_fred_series("UNRATE")
    nfp = _fetch_fred_series("PAYEMS")
    claims = _fetch_fred_series("ICSA")
    participation = _fetch_fred_series("CIVPART")
    jolts = _fetch_fred_series("JTSJOL")

    return {
        "unemployment_rate": {
            "latest": _latest_value(unemployment),
            "direction": _direction(unemployment),
            "series": unemployment[-12:],
        },
        "nonfarm_payrolls": {
            "latest": _latest_value(nfp),
            "direction": _direction(nfp),
        },
        "initial_claims": {
            "latest": _latest_value(claims),
            "direction": _direction(claims),
            "interpretation": (
                "Rising claims — labor market weakening"
                if _direction(claims) == "rising"
                else "Falling claims — labor market strengthening"
                if _direction(claims) == "falling"
                else "Stable claims"
            ),
        },
        "labor_participation": {
            "latest": _latest_value(participation),
            "direction": _direction(participation),
        },
        "job_openings_jolts": {
            "latest": _latest_value(jolts),
            "direction": _direction(jolts),
        },
    }


# ---------------------------------------------------------------------------
# Business Cycle Assessment
# ---------------------------------------------------------------------------

def assess_business_cycle() -> dict:
    """
    Determine current business cycle phase based on macro indicators.
    Phases: early_expansion, mid_expansion, late_expansion, contraction.
    """
    rates = fetch_rates()
    inflation = fetch_inflation()
    gdp = fetch_gdp()
    employment = fetch_employment()

    signals = {
        "gdp_direction": gdp["real_gdp_growth"]["direction"],
        "rate_direction": rates["fed_funds_rate"]["direction"],
        "inflation_direction": inflation["cpi_yoy"]["direction"],
        "unemployment_direction": employment["unemployment_rate"]["direction"],
        "yield_curve_inverted": rates["yield_curve"]["inverted"],
        "lei_direction": gdp["leading_economic_index"]["direction"],
    }

    # Simple heuristic for cycle phase
    gdp_dir = signals["gdp_direction"]
    rate_dir = signals["rate_direction"]
    unemp_dir = signals["unemployment_direction"]
    inverted = signals["yield_curve_inverted"]
    lei_dir = signals["lei_direction"]

    if gdp_dir == "falling" or (inverted and lei_dir == "falling"):
        phase = "contraction"
        description = "Economic contraction or recession risk is elevated"
        favored_sectors = ["Consumer Defensive", "Healthcare", "Utilities"]
        disfavored_sectors = ["Consumer Cyclical", "Technology", "Industrials"]
    elif gdp_dir == "rising" and unemp_dir == "falling" and rate_dir != "rising":
        phase = "early_expansion"
        description = "Economy accelerating from trough, rates still low"
        favored_sectors = ["Technology", "Consumer Cyclical", "Industrials", "Financial Services"]
        disfavored_sectors = ["Utilities", "Consumer Defensive"]
    elif gdp_dir in ("rising", "stable") and rate_dir == "rising":
        if inverted or lei_dir == "falling":
            phase = "late_expansion"
            description = "Growth slowing, rates high, cycle nearing peak"
            favored_sectors = ["Energy", "Healthcare", "Consumer Defensive"]
            disfavored_sectors = ["Technology", "Real Estate", "Consumer Cyclical"]
        else:
            phase = "mid_expansion"
            description = "Steady growth, rates rising moderately"
            favored_sectors = ["Technology", "Industrials", "Financial Services"]
            disfavored_sectors = ["Utilities"]
    else:
        phase = "mid_expansion"
        description = "Mixed signals — likely mid-cycle"
        favored_sectors = ["Technology", "Healthcare", "Industrials"]
        disfavored_sectors = []

    return {
        "phase": phase,
        "description": description,
        "confidence": "moderate",
        "signals": signals,
        "sector_implications": {
            "favored": favored_sectors,
            "disfavored": disfavored_sectors,
        },
        "factor_implications": {
            "early_expansion": "Size, Momentum favored",
            "mid_expansion": "Quality, Growth favored",
            "late_expansion": "Value, Low Volatility favored",
            "contraction": "Low Volatility, Quality, Value (deep) favored",
        }.get(phase, ""),
    }


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

def macro_dashboard() -> dict:
    """Comprehensive macro dashboard with all indicators."""
    return {
        "timestamp": datetime.now().isoformat(),
        "rates": fetch_rates(),
        "inflation": fetch_inflation(),
        "gdp": fetch_gdp(),
        "employment": fetch_employment(),
        "business_cycle": assess_business_cycle(),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="US Macro Data Fetcher (FRED, no API key)"
    )
    parser.add_argument("--dashboard", action="store_true",
                        help="Full macro dashboard")
    parser.add_argument("--rates", action="store_true",
                        help="Interest rates")
    parser.add_argument("--inflation", action="store_true",
                        help="Inflation indicators")
    parser.add_argument("--gdp", action="store_true",
                        help="GDP and growth")
    parser.add_argument("--employment", action="store_true",
                        help="Employment data")
    parser.add_argument("--cycle", action="store_true",
                        help="Business cycle assessment")
    args = parser.parse_args()

    try:
        if args.rates:
            data = fetch_rates()
        elif args.inflation:
            data = fetch_inflation()
        elif args.gdp:
            data = fetch_gdp()
        elif args.employment:
            data = fetch_employment()
        elif args.cycle:
            data = assess_business_cycle()
        else:
            data = macro_dashboard()

        output_json(data)

    except ImportError:
        error_exit("pandas-datareader is required. Install: pip install pandas-datareader")
    except Exception as e:
        error_exit(f"Error: {e}")


if __name__ == "__main__":
    main()
