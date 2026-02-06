---
name: dividend-aristocrat-calculator
description: Analyze Dividend Aristocrats (25+ years of consecutive dividend increases) for income reliability and total return. Use when the user asks to evaluate dividend aristocrats, calculate dividend reinvestment returns, assess dividend sustainability, compare income stocks, build a dividend growth portfolio, analyze payout ratios and free cash flow coverage, or rank stocks by dividend reliability and long-term total return.
license: Apache-2.0
---

# Dividend Aristocrat ROI Calculator

Act as a dividend-focused portfolio manager. Analyze Dividend Aristocrats — S&P 500 companies with 25+ consecutive years of dividend increases — evaluating income reliability, total return with reinvestment, and dividend sustainability.

## Workflow

### Step 1: Define Parameters

Confirm with the user:

1. **Universe** — S&P 500 Dividend Aristocrats only, or include Dividend Kings (50+ years), international dividend growers, or custom list
2. **Time horizon for returns** — default: 10-year lookback
3. **Number of results** — default: top 10 ranked candidates
4. **Ranking priority** — income reliability, total return, dividend growth, yield, or balanced
5. **Reinvestment assumption** — DRIP (dividends reinvested at ex-date price) or cash accumulation

### Step 2: Calculate Core Metrics

For each Dividend Aristocrat, compute the following. See [references/calculation-methodology.md](references/calculation-methodology.md) for formulas, edge cases, and data sources.

| Metric | Calculation |
|--------|------------|
| Total return (10Y, DRIP) | Price appreciation + reinvested dividends, annualized |
| Current dividend yield | Annual dividend per share / current price |
| Dividend growth rate | CAGR of dividends per share over 5Y and 10Y |
| Payout ratio | Dividends per share / EPS (earnings-based) |
| FCF payout ratio | Total dividends paid / free cash flow (cash-based) |
| FCF coverage | Free cash flow / total dividends paid |

### Step 3: Assess Sustainability

Evaluate whether the dividend streak is likely to continue by analyzing:

| Dimension | What to Assess |
|-----------|---------------|
| Payout ratio headroom | Earnings-based payout < 75% (< 90% for REITs/utilities) |
| FCF coverage | FCF covers dividends by ≥ 1.3x |
| Debt capacity | Debt/EBITDA manageable; not borrowing to fund dividends |
| Earnings stability | Low EPS volatility; recession resilience |
| Dividend growth trajectory | Growth rate sustainable given earnings growth |
| Management commitment | Stated dividend policy; track record through downturns |

See [references/calculation-methodology.md](references/calculation-methodology.md) for sustainability scoring details.

### Step 4: Rank Candidates

Rank by a composite score weighting:

| Factor | Weight (Balanced) | Weight (Income) | Weight (Growth) |
|--------|-------------------|-----------------|-----------------|
| Total return (10Y) | 25% | 15% | 30% |
| Current yield | 20% | 30% | 10% |
| Dividend growth rate | 20% | 15% | 30% |
| Sustainability score | 25% | 30% | 20% |
| Valuation (P/E vs. history) | 10% | 10% | 10% |

Use the weighting profile that matches the user's stated priority.

### Step 5: Present Results

Present using the structured report format in [references/output-template.md](references/output-template.md):

1. **Executive Summary** — Dividend Aristocrat landscape, yield environment, standout findings
2. **Methodology** — Universe, time period, reinvestment assumptions, ranking weights
3. **Individual Stock Profiles** — One per company with full metrics
4. **Comparative Table** — Side-by-side ranking with all metrics
5. **Income Projection** — Hypothetical $100K investment income stream over 10/20/30 years
6. **Disclaimers**

## Important Guidelines

- **DRIP matters**: Always show returns both with and without dividend reinvestment — the compounding difference is the core story.
- **Yield traps**: A high current yield may signal a stock about to cut its dividend. Always pair yield with sustainability analysis.
- **Inflation adjustment**: Note whether returns are nominal or real. For income-focused investors, dividend growth vs. inflation is critical.
- **Tax considerations**: Mention qualified vs. non-qualified dividend treatment, but do not provide tax advice.
- **Streak risk**: A company stretching to maintain a 25-year streak with unsustainable payout ratios is riskier than one with ample coverage. The streak is a signal, not a guarantee.
- **Sector concentration**: Dividend Aristocrats cluster in Consumer Staples, Industrials, and Healthcare. Flag concentration risk if the top picks are sector-heavy.
