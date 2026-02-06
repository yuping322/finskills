# Calculation Methodology

Formulas, data sources, and sustainability scoring for Dividend Aristocrat analysis.

## Table of Contents

1. [Total Return Calculation](#total-return-calculation)
2. [Dividend Metrics](#dividend-metrics)
3. [Sustainability Scoring](#sustainability-scoring)
4. [Sector-Specific Adjustments](#sector-specific-adjustments)
5. [Data Sources](#data-sources)

## Total Return Calculation

### DRIP (Dividend Reinvestment) Return

Calculate as if all dividends are reinvested at the closing price on the ex-dividend date:

1. Start with initial investment and share count
2. For each dividend payment, compute additional shares: `Dividend Amount / Price on Ex-Date`
3. Accumulate share count over the period
4. Final value = Total shares × Current price
5. Annualized return = `(Final Value / Initial Value)^(1/Years) − 1`

### Non-DRIP Return

Price return + cumulative cash dividends received (not reinvested):
- Total return = `(Price Change + Cumulative Dividends) / Initial Investment`

### Always Present Both

The compounding gap between DRIP and non-DRIP is often the most powerful illustration of dividend investing.

## Dividend Metrics

### Current Dividend Yield

```
Yield = (Annual Dividend Per Share / Current Stock Price) × 100
```

- Use the **indicated annual dividend** (most recent quarterly × 4) unless the company pays variable/special dividends
- For variable payers, use trailing 12-month actual dividends

### Dividend Growth Rate

```
CAGR = (Latest Annual DPS / DPS N Years Ago)^(1/N) − 1
```

Calculate for both 5-year and 10-year periods. Note:
- If there was a stock split, use split-adjusted DPS
- Special/one-time dividends should be excluded from the growth rate calculation
- If the company has a pattern of large annual increases followed by small ones, note the inconsistency

### Dividend Growth Consistency

| Pattern | Assessment |
|---------|-----------|
| Increase every year, ≥ inflation | Excellent — true compounder |
| Increase every year, < inflation | Good — streak intact but real value eroding |
| Increase most years, occasional flat | Adequate — monitoring warranted |
| Token $0.01 increases to maintain streak | Poor — streak is artificial |

### Payout Ratios

**Earnings-based payout ratio**:
```
Payout Ratio = DPS / EPS
```

**FCF-based payout ratio** (preferred):
```
FCF Payout = Total Dividends Paid / Free Cash Flow
```

**Why FCF payout is preferred**: Earnings include non-cash items (depreciation, amortization, SBC). FCF shows actual cash available to pay dividends.

| Payout Ratio (Earnings) | Assessment |
|-------------------------|-----------|
| < 40% | Very safe — ample room for growth and downturns |
| 40–60% | Healthy — balanced between payout and retention |
| 60–75% | Moderate risk — limited buffer for earnings dips |
| 75–90% | Elevated risk — sustainable only for very stable businesses (utilities, staples) |
| > 90% | High risk — dividend cut probable if earnings soften |

### FCF Coverage Ratio

```
FCF Coverage = Free Cash Flow / Total Dividends Paid
```

| Coverage | Assessment |
|----------|-----------|
| > 2.0x | Excellent — dividend well-covered with room for growth |
| 1.5–2.0x | Strong — healthy buffer |
| 1.2–1.5x | Adequate — slim margin of safety |
| 1.0–1.2x | Thin — any FCF weakness threatens the dividend |
| < 1.0x | Danger — dividend exceeds FCF; funded by debt or reserves |

## Sustainability Scoring

Score each Dividend Aristocrat on a 0–100 sustainability scale:

| Factor | Weight | Scoring |
|--------|--------|---------|
| FCF coverage ratio | 25% | >2x=25, 1.5–2x=20, 1.2–1.5x=15, 1–1.2x=8, <1x=0 |
| Earnings payout ratio | 15% | <50%=15, 50–65%=12, 65–80%=8, 80–90%=4, >90%=0 |
| Dividend growth consistency | 15% | Every year above inflation=15, every year below inflation=10, most years=5 |
| Earnings stability (EPS volatility) | 15% | Low vol=15, moderate=10, high=5, very high=0 |
| Balance sheet strength (D/EBITDA) | 15% | <1.5x=15, 1.5–3x=10, 3–4x=5, >4x=0 |
| Sector defensiveness | 10% | Staples/Healthcare/Utilities=10, Industrials/Tech=7, Cyclicals=4 |
| Management dividend commitment | 5% | Stated policy + track record=5, implicit only=3, no guidance=1 |

| Total Score | Rating |
|-------------|--------|
| 80–100 | ★★★★★ — Fortress dividend |
| 65–79 | ★★★★ — Very reliable |
| 50–64 | ★★★ — Reliable, some monitoring needed |
| 35–49 | ★★ — Moderate risk |
| < 35 | ★ — Elevated cut risk |

## Sector-Specific Adjustments

| Sector | Adjusted Payout Threshold | Notes |
|--------|--------------------------|-------|
| Utilities | 75% (earnings), 85% (regulated) | Regulated utilities have predictable cash flows |
| REITs | Use AFFO payout ratio instead | Required to pay 90% of taxable income |
| Consumer Staples | 65% | Stable but watch for volume declines |
| Financials | Use dividend/earnings + capital ratio | Regulatory capital requirements constrain payout |
| Technology | 50% | Higher reinvestment needs; lower payout is appropriate |
| Energy | Use FCF payout + reserve life | Commodity dependence adds volatility |

## Data Sources

- Dividend history: Company investor relations pages, S&P Dividend Aristocrats index methodology
- Financial data: Most recent quarterly (10-Q) and annual (10-K) filings
- Share price: Adjusted closing prices (split-adjusted, dividend-adjusted for total return)
- Analyst estimates: Consensus from ≥ 3 analysts for forward earnings and dividend estimates
- Always state the data period (e.g., "based on fiscal year ending December 2025")
