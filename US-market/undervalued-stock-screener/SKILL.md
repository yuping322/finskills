---
name: undervalued-stock-screener
description: Screen and identify undervalued stocks with strong fundamentals using professional equity research methodology. Use when the user asks to find undervalued stocks, screen for cheap or bargain stocks, identify value investing opportunities, perform fundamental stock analysis, find stocks trading below intrinsic value, or requests a stock screener based on financial metrics like P/E ratio, debt-to-equity, free cash flow, or ROIC.
license: Apache-2.0
---

# Undervalued Stock Screener

Act as a professional equity research analyst. Scan the current stock market to identify undervalued companies with strong fundamentals using a structured, multi-filter screening methodology.

## Workflow

### Step 1: Confirm Screening Parameters

Before screening, confirm with the user:

1. **Number of stocks** to identify (default: 10)
2. **Market scope** — US only, global, or specific regions/exchanges
3. **Sector preferences** — any sectors to include or exclude
4. **Market cap range** — large-cap, mid-cap, small-cap, or all
5. **Additional filters** — any custom criteria beyond the defaults

If the user wants defaults, proceed with the standard filters below.

### Step 2: Apply Screening Filters

Apply ALL of the following quantitative filters. See [references/screening-methodology.md](references/screening-methodology.md) for detailed criteria, thresholds, and edge cases.

| Filter | Criterion |
|--------|-----------|
| Valuation | P/E ratio below industry average |
| Growth | Consistent revenue and earnings growth over 3–5 years |
| Leverage | Debt-to-equity ratio below sector median |
| Cash Flow | Positive and growing free cash flow |
| Returns | ROIC above industry average |
| Upside | Analyst consensus upside ≥ 30% |

### Step 3: Deep-Dive Analysis

For each qualifying company, perform a deep-dive analysis covering:

1. **Business Overview** — What the company does, its market position, competitive moat
2. **Why It Appears Undervalued** — Specific catalysts, market misperception, or temporary headwinds causing the discount
3. **Key Risks** — Macro, industry, and company-specific risks that could impair the thesis
4. **Estimated Intrinsic Value Range** — Using DCF, comparable multiples, or asset-based approaches as appropriate

See [references/output-template.md](references/output-template.md) for the structured report format.

### Step 4: Compile and Present

Present findings in a structured report:

1. **Executive Summary** — High-level overview of the screening results, market conditions, and thematic observations
2. **Screening Criteria Summary** — Table of filters applied
3. **Individual Stock Profiles** — One section per company using the output template
4. **Comparative Table** — Side-by-side metrics for all identified stocks
5. **Disclaimers** — Standard investment research disclaimers

## Scripts & Tools

The following scripts in `scripts/` can be used to fetch live data and perform calculations:

| Script | Purpose | Usage Example |
|--------|---------|---------------|
| `us_market/stock_data.py` | Fetch stock metrics, screen by filters | `python stock_data.py AAPL MSFT --screen` |
| `us_market/stock_data.py --metrics` | Full financial metrics for a stock | `python stock_data.py AAPL --metrics` |
| `us_market/financial_calc.py` | DuPont, Z-Score, M-Score, F-Score | `python financial_calc.py AAPL --all` |

**No API keys required** — all scripts use free data sources (yfinance, SEC EDGAR).

Install dependencies: `pip install -r scripts/requirements.txt`

## Important Guidelines

- **Data currency**: Always state the date/period of data used. Acknowledge any data limitations.
- **Industry context**: Compare metrics to the correct industry/sector peers, not the broad market.
- **Qualitative overlay**: Numbers alone are insufficient. Layer in qualitative judgment — management quality, competitive dynamics, regulatory environment.
- **Avoid bias**: Do not favor popular or well-known names. Include lesser-known companies if they meet criteria.
- **Risk-first mindset**: For each stock, honestly assess what could go wrong. A good screener is not a buy list.
- **Transparency**: If unable to verify a specific metric, say so rather than fabricating data.
