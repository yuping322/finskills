# Methodology: Volatility Regime Monitor (US)

Volatility is a practical **risk switch**: high-vol regimes tend to coincide with lower equity risk-adjusted returns, higher correlations, and worse liquidity. The goal is to classify regimes with simple, backtestable rules.

## Data Definitions

### Sources and field mapping

- Primary price series: index/ETF closes (e.g., SPY) from yfinance or any price provider.
- Optional implied vol: VIX (`VIXCLS` from FRED) if available.

Fields:
- `Close(t)`: adjusted close
- `r(t) = ln(Close(t)/Close(t-1))`

### Frequency and windows

- Daily returns.
- Vol windows:
  - `RV20`: 20d realized volatility
  - `RV60`: 60d realized volatility
  - Lookback for percentiles: 5y when possible

## Core Metrics

### Metric list and formulas

- `RVk(t) = sqrt(252) * stdev(r[t-k+1:t])`
- **Vol trend**: `RV20 / RV60`
- **Vol shock**: `RV20 - RV60`
- **Term structure proxy** (optional): VIX contango/backwardation if you have VIX futures; otherwise omit.

### Standardization

- Use percentiles of `RV20` in a rolling 5y window.
- Use z-scores on `RV20` only if return distribution is stable enough.

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

Rule 1 (high-vol regime → risk-off):
IF {RV20(t) >= 25% AND RV20/RV60 >= 1.1}
THEN {Over the next 20 trading days, equity returns skew negative and correlation rises; defensive/low-vol baskets tend to outperform high beta.}
CONFIDENCE {0.65}
APPLICABLE_UNIVERSE {US equities (index + liquid constituents); sector/style baskets; ETFs.}
FAILURE_MODE {Fast mean reversion after one-off shocks; volatility elevated but upward-trending markets (“high vol melt-up”).}

Rule 2 (volatility compression → risk-on):
IF {RV20(t) <= 15% AND RV20/RV60 <= 0.95}
THEN {Over the next 20–60 trading days, equities tend to have positive excess returns and trend-following signals work better.}
CONFIDENCE {0.60}
APPLICABLE_UNIVERSE {US equities broad and trend/rotation frameworks.}
FAILURE_MODE {Volatility is “artificially low” before a catalyst (earnings/Fed); sudden regime break.}

Rule 3 (spike then rapid decay → tactical rebound):
IF {RV20 percentile >= 90 AND RV20 drops by >= 20% (relative) over the next 10 trading days}
THEN {Over the next 5–20 trading days, equities often rebound (positive excess return), but medium-term risk depends on credit/earnings.}
CONFIDENCE {0.57}
APPLICABLE_UNIVERSE {US index/large-cap equities; short horizons.}
FAILURE_MODE {Credit stress persists; volatility “decays” while equities remain in a downtrend; rebounds are sold.}

### Trigger / exit / invalidation conditions

- **High-vol trigger**: `RV20 >= 25%` OR `RV20 percentile >= 80` with rising trend.
- **Exit**: `RV20 < 20%` and `RV20/RV60 < 1.0` for 10 consecutive trading days.
- **Invalidation**: if volatility is high but breadth/credit are improving strongly, downgrade bearishness.

### Threshold rationale

- 15%/25% are practical regime cutoffs for SPY-like indices; adjust by universe (single names will be higher).
- Percentiles are safer for single-stock analysis.

## Edge Cases and Degradation

### Missing data / outliers handling

- Use adjusted prices; corporate actions can create artificial jumps.
- Remove obvious bad ticks (e.g., returns > ±30% for index ETFs) before vol estimation.

### Fallback proxies

- If only weekly data exists: compute `RV8` and `RV26` on weekly returns and rescale.

## Backtest Notes (Minimal)

- Compute regime using EOD `t`, trade at `t+1`.
- Report forward 20d/60d excess returns and max drawdown conditional on regime.
- Falsification: if high-vol regime does not exhibit worse drawdowns than low-vol across long samples.
