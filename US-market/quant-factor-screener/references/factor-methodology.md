# Factor Methodology

Detailed factor definitions, calculation methods, academic foundations, and factor timing framework.

## Table of Contents

1. [Factor Definitions](#factor-definitions)
2. [Scoring Methodology](#scoring-methodology)
3. [Factor Timing Framework](#factor-timing-framework)
4. [Factor Crowding Assessment](#factor-crowding-assessment)
5. [Historical Factor Performance](#historical-factor-performance)
6. [Factor Interaction and Correlation](#factor-interaction-and-correlation)

## Factor Definitions

### Value Factor

**Academic basis**: Fama-French HML (High Minus Low), 1993

| Sub-metric | Formula | Weight | Rationale |
|-----------|---------|--------|-----------|
| Earnings yield | EBIT / Enterprise Value | 30% | Operating earnings relative to total cost |
| Book-to-price | Book Value / Market Cap | 20% | Classic Fama-French value metric |
| Free cash flow yield | FCF / Enterprise Value | 30% | Cash generation relative to cost |
| EV/EBITDA (inverse) | EBITDA / Enterprise Value | 20% | Operating value metric |

**Exclusions**: Negative earnings or book value → exclude from value scoring
**Sector treatment**: Score within GICS sectors to avoid sector bets

### Momentum Factor

**Academic basis**: Jegadeesh and Titman, 1993; Carhart four-factor model, 1997

| Sub-metric | Formula | Weight | Rationale |
|-----------|---------|--------|-----------|
| Price momentum (12-1) | Total return over months 2–12 (skip most recent month) | 60% | Classic cross-sectional momentum |
| Earnings revision momentum | 3-month change in consensus EPS estimate / Absolute value of starting estimate | 40% | Fundamental momentum, less crash-prone |

**The skip-month**: Always exclude the most recent month's return — it captures short-term reversal, not momentum.
**Crash awareness**: Momentum is prone to sharp reversals, especially after market crashes. The earnings revision sub-metric partially mitigates this.

### Quality Factor

**Academic basis**: Asness, Frazzini, and Pedersen (QMJ — Quality Minus Junk), 2019

| Sub-metric | Formula | Weight | Rationale |
|-----------|---------|--------|-----------|
| Profitability (ROE) | Net income / Shareholders' equity | 30% | Earning power |
| Earnings stability | 1 − (5-year std dev of EPS growth) | 20% | Consistency |
| Financial strength | 1 − (Total debt / Total assets) | 25% | Low leverage |
| Accrual quality | Operating cash flow / Net income | 25% | Earnings quality |

**Higher quality** = high profitability, stable earnings, low leverage, cash-backed earnings.

### Low Volatility Factor

**Academic basis**: Baker, Bradley, and Wurgler, 2011; Ang et al., 2006

| Sub-metric | Formula | Weight | Rationale |
|-----------|---------|--------|-----------|
| Realized volatility | Standard deviation of daily returns (1Y) | 40% | Direct risk measure |
| Beta | CAPM beta vs S&P 500 (2Y weekly) | 30% | Systematic risk |
| Downside deviation | Semi-deviation (only negative returns) | 30% | Downside-specific risk |

**Scoring**: Invert — lower volatility = higher score.
**The low-volatility anomaly**: Lower-risk stocks have historically delivered equal or better risk-adjusted returns than higher-risk stocks, contradicting CAPM.

### Size Factor

**Academic basis**: Fama-French SMB (Small Minus Big), 1993

| Sub-metric | Formula | Weight |
|-----------|---------|--------|
| Market capitalization | Share price × Shares outstanding | 100% |

**Scoring**: Invert — smaller market cap = higher score.
**Refinement**: Combine with quality to avoid "small and junky" trap. Small + high quality is the profitable combination.

### Growth Factor

**Academic basis**: Various; GARP (Growth at a Reasonable Price) literature

| Sub-metric | Formula | Weight | Rationale |
|-----------|---------|--------|-----------|
| Revenue growth (3Y CAGR) | (Rev_now / Rev_3yr_ago)^(1/3) − 1 | 30% | Top-line growth |
| EPS growth (3Y CAGR) | (EPS_now / EPS_3yr_ago)^(1/3) − 1 | 30% | Bottom-line growth |
| Margin expansion | ΔOperating margin (3Y) | 20% | Improving economics |
| Forward revenue growth | Consensus next-year revenue growth | 20% | Forward-looking |

**Exclusions**: Exclude companies with negative base-year EPS for EPS CAGR calculation.

## Scoring Methodology

### Percentile Ranking

For each sub-metric:
1. Remove stocks with missing data
2. Winsorize at 2.5th and 97.5th percentiles (remove extreme outliers)
3. Rank within sector (sector-neutral) or full universe (unconstrained)
4. Convert to percentile score: `Score = Rank / N × 100`

### Composite Factor Score

```
Factor Score = Σ (Sub-metric weight × Sub-metric percentile score)
```

### Composite Multi-Factor Score

```
Multi-Factor Score = Σ (Factor weight × Factor score)
```

Default: equal weight (1/6 each). User can customize.

### Z-Score Alternative

For more granular comparison:
```
Z-Score = (Stock metric − Universe mean) / Universe standard deviation
```

Then: `Composite Z = Σ (Factor weight × Factor Z-score)`

## Factor Timing Framework

### Business Cycle Factor Map

| Phase | GDP | Inflation | Rates | Favored Factors | Disfavored Factors |
|-------|-----|-----------|-------|-----------------|-------------------|
| Early expansion | ↑ Accelerating | Low / Rising | ↓ then → | Size, Momentum, Growth | Low Volatility |
| Mid expansion | ↑ Stable growth | → Moderate | → | Momentum, Quality | Value (often) |
| Late expansion | → Decelerating | ↑ Rising | ↑ | Quality, Value | Size, Growth |
| Recession | ↓ Contracting | ↓ Falling | ↓ | Low Volatility, Quality | Momentum, Size |
| Recovery | ↑ Bottoming | Low | ↓ Low | Value (deep), Size | Low Volatility |

### Regime Detection Indicators

| Indicator | Source | What It Signals |
|-----------|--------|----------------|
| ISM Manufacturing PMI | Monthly survey | > 50 expansion, < 50 contraction |
| Yield curve slope | 10Y - 2Y Treasury spread | Negative = recession signal |
| Credit spreads | IG and HY OAS | Widening = stress, narrowing = confidence |
| Unemployment rate direction | BLS monthly | Rising = late cycle, falling = expansion |
| Core CPI / PCE | BLS / BEA | > 3% = inflationary; < 2% = disinflationary |
| Fed funds rate direction | FOMC decisions | Hiking = tightening; cutting = easing |

### Factor Timing Adjustment

Based on regime assessment, adjust default equal weights:

| Regime | Value | Momentum | Quality | Low Vol | Size | Growth |
|--------|-------|----------|---------|---------|------|--------|
| Early expansion | 15% | 20% | 10% | 5% | 25% | 25% |
| Mid expansion | 10% | 25% | 20% | 5% | 15% | 25% |
| Late expansion | 25% | 10% | 25% | 20% | 10% | 10% |
| Recession | 15% | 5% | 25% | 30% | 5% | 20% |
| Recovery | 30% | 15% | 10% | 5% | 25% | 15% |

**Caveat**: Factor timing is notoriously difficult. Default equal weight is a reasonable base case. Timing adjustments should be modest (±10% max from equal weight).

## Factor Crowding Assessment

### Crowding Indicators

| Indicator | How to Measure | Crowded If |
|-----------|---------------|-----------|
| Valuation spread | Ratio of cheapest quartile P/E to most expensive quartile P/E within factor | Spread narrowing (everyone bought the "cheap" ones) |
| Short interest in anti-factor | Short interest in stocks scoring poorly on the factor | High and rising |
| Factor ETF flows | Net inflows to factor-specific ETFs (VLUE, MTUM, QUAL, etc.) | Large sustained inflows |
| Quant fund crowding | Hedge fund 13F overlap on factor | High overlap |
| Factor return autocorrelation | Recent factor returns predicting future returns | Positive (trend-following into factor) |

### Crowding Risk

| Crowding Level | Expected Impact |
|---------------|----------------|
| Low | Factor premium likely intact |
| Moderate | Compressed expected return, normal risk |
| High | Risk of sharp reversal (factor crash) |
| Extreme | Near-term negative expected return |

## Historical Factor Performance

### Long-Term US Factor Premiums (1963–2023, approximate annualized)

| Factor | Annual Premium | Sharpe Ratio | Worst Drawdown | Worst Period |
|--------|---------------|-------------|----------------|-------------|
| Value (HML) | 3.5% | 0.35 | -45% | 2017–2020 |
| Momentum (UMD) | 6.0% | 0.50 | -50% | 2009 (March) |
| Quality (QMJ) | 4.0% | 0.55 | -20% | Various |
| Low Volatility | 2.5% | 0.60 | -15% (relative) | Strong bull markets |
| Size (SMB) | 2.0% | 0.20 | -30% | Various |
| Growth | ~0% vs value (compensated by momentum) | — | — | — |

**Key insight**: Quality and Low Volatility have the best Sharpe ratios. Value and Momentum have the highest raw premiums but with significant drawdown risk. Combining factors dramatically improves the Sharpe ratio.

## Factor Interaction and Correlation

### Factor Correlation Matrix (approximate)

| | Value | Momentum | Quality | Low Vol | Size |
|---|-------|----------|---------|---------|------|
| Value | 1.0 | -0.3 | -0.1 | +0.1 | +0.2 |
| Momentum | -0.3 | 1.0 | +0.1 | -0.1 | +0.1 |
| Quality | -0.1 | +0.1 | 1.0 | +0.3 | -0.3 |
| Low Vol | +0.1 | -0.1 | +0.3 | 1.0 | -0.4 |
| Size | +0.2 | +0.1 | -0.3 | -0.4 | 1.0 |

### Key Interactions

- **Value + Momentum**: Negatively correlated — combining them provides significant diversification
- **Quality + Low Vol**: Positively correlated — overlap in defensive characteristics
- **Size + Quality**: Negatively correlated — small caps tend to be lower quality; combining helps avoid "small junk"
- **Value + Quality**: The "value trap avoidance" combination — quality filter removes cheap-for-a-reason stocks
