# Methodology: Liquidity Impact Estimator (US)

The objective is to estimate whether a desired order size can be executed with acceptable **implementation shortfall** (slippage + market impact) and how that affects expected net returns. This is not a precise execution model; it is a **risk filter** and sizing guide.

## Data Definitions

### Sources and field mapping

Minimum required:
- Daily price + volume (yfinance or any provider).

Optional enhancements:
- Bid-ask spread (NBBO mid/quotes) if available.
- Intraday volume profile if available.

Key fields:
- `close`, `volume`
- `dollar_volume = close * volume`
- `ADV20`, `ADV60` (average daily dollar volume)

### Frequency and windows

- Daily; compute ADV and realized volatility on rolling windows.
- Suggested windows: 20d / 60d / 252d.

## Core Metrics

### Metric list and formulas

- **Size-to-liquidity**: `SizeToADV = OrderValue / ADV20`
- **Realized volatility**: `RV20` (annualized)
- **Spread proxy** (if no quotes): `SpreadProxy ≈ (High-Low)/Close` averaged over 20d
- **Impact proxy** (square-root intuition):
  - `ImpactProxy_bps ∝ RV20 * sqrt(SizeToADV) * 10000`
  - Calibrate constant per venue/universe if you have historical fills.

### Standardization

- Use percentiles of `SizeToADV` and `ADV20` within the universe.
- Use z-score for ADV changes to detect liquidity deterioration.

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

Rule 1 (order too large vs ADV → negative net expectancy):
IF {SizeToADV >= 10%}
THEN {Expected net return of immediate execution is lower (negative vs “paper” return) due to impact/slippage; reduce size or extend execution horizon.}
CONFIDENCE {0.75}
APPLICABLE_UNIVERSE {US equities; strongest for mid/small caps and names with unstable volume.}
FAILURE_MODE {Hidden liquidity (dark pools) materially reduces impact; participation algorithms outperform proxy; order is executed over many days.}

Rule 2 (liquidity deteriorating → higher tail risk):
IF {ADV20 drops by >= 30% vs its 252d median AND RV20 is rising}
THEN {Exit risk increases; expected downside tail risk rises and risk-adjusted returns deteriorate (negative skew).}
CONFIDENCE {0.60}
APPLICABLE_UNIVERSE {US equities with changing liquidity (post-news, post-rebalance, small caps).}
FAILURE_MODE {ADV drop is seasonal/holiday-driven; liquidity returns quickly; fundamental catalyst improves volume.}

Rule 3 (wide spreads + high vol → slippage dominates short-horizon trades):
IF {Spread percentile >= 80 AND RV20 percentile >= 80}
THEN {Short-horizon expected returns after costs are negative; avoid frequent trading and use limit orders/longer horizons.}
CONFIDENCE {0.70}
APPLICABLE_UNIVERSE {US equities with measurable spread proxies; less applicable to mega-caps with consistently tight spreads.}
FAILURE_MODE {Spread measure is poor proxy; execution venue provides price improvement; trader has superior microstructure access.}

### Trigger / exit / invalidation conditions

- Trigger “liquidity warning” when `SizeToADV >= 10%` or ADV collapses materially.
- Exit when `SizeToADV <= 5%` and ADV stabilizes (>= 3 weeks).
- Invalidate if volume data is stale or corporate actions distort dollar volume.

### Threshold rationale

- 10% ADV is a practical cutoff where impact often becomes non-linear for many names.
- Percentiles adapt across market-cap tiers.

## Edge Cases and Degradation

### Missing data / outliers handling

- Remove split-adjustment anomalies and bad ticks before ADV estimation.
- Treat single-day volume spikes as outliers; use median-based ADV as robustness check.

### Fallback proxies

- If you only have shares volume (no price): approximate dollar volume using last close and mark as lower confidence.

## Backtest Notes (Minimal)

- Backtest “impact filters” by comparing next-day/next-week realized PnL net of assumed bps costs across buckets of `SizeToADV`.
- Falsification: if large `SizeToADV` buckets do not show higher implementation shortfall vs small buckets in your own fills/history.
