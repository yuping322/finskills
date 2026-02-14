# Methodology: Options Strategy Analyzer (US)

Options contain information (implied volatility, skew, positioning) and offer strategies whose expected returns depend on **volatility risk premium (VRP)** and tail risk. This methodology defines a minimal set of programmable rules; if options microdata is unavailable, downgrade to proxy-based outputs.

## Data Definitions

### Sources and field mapping

Preferred inputs (per underlying):
- `IV30(t)`: 30D implied volatility (ATM or delta-neutral)
- `RV20(t)`: 20D realized volatility from underlying returns
- `Skew25(t)`: 25-delta put IV − 25-delta call IV (pp)
- `PCR(t)` (optional): put/call ratio (volume or open interest)
- Catalyst calendar: earnings date, major events

If you do not have these fields, accept user-provided values and record the source.

### Frequency and windows

- Daily; signals are typically evaluated over 5–20 trading days.
- Use 252d history for IV percentiles (IV Rank).

## Core Metrics

### Metric list and formulas

- **VRP**: `VRP(t) = IV30(t) - RV20(t)`
- **IV Rank**: `IVpct(t) = percentile_rank(IV30[t-252:t])`
- **Skew shock**: `Δ5(Skew25)`

### Standardization

- Use percentiles for IV and PCR (heavy-tailed).
- Use z-scores for VRP only if stable for the underlying.

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

Rule 1 (high VRP + no near-term catalyst → short premium has positive expectancy):
IF {IVpct(t) >= 80 AND VRP(t) >= 5 vol points AND earnings_date is > 7 calendar days away}
THEN {Over the next ~20 trading days, systematic option premium selling (defined-risk) has positive expected return; underlying direction is approximately neutral.}
CONFIDENCE {0.60}
APPLICABLE_UNIVERSE {US equities/ETFs with liquid options (tight spreads, high OI); avoid microcaps.}
FAILURE_MODE {Gap/crash events, earnings surprises, volatility clustering where realized vol exceeds implied; liquidity collapse causing large slippage.}

Rule 2 (skew steepening + credit stress → bearish tail risk):
IF {Δ5(Skew25) >= +2 vol points AND HY_OAS_ZL(t) >= 1.0}
THEN {Over the next 20–60 trading days, equity returns skew negative; protective put demand reflects rising tail risk.}
CONFIDENCE {0.57}
APPLICABLE_UNIVERSE {Index options and large-cap underlyings where skew is meaningful.}
FAILURE_MODE {Skew moves dominated by dealer hedging/roll flows; tail hedges are crowded; quick policy backstop.}

Rule 3 (positioning extreme → contrarian bounce, low conviction):
IF {PCR percentile >= 90 AND underlying price stabilizes (no new 10d low over 3 sessions)}
THEN {Over the next 5–20 trading days, returns often mean-revert upward (tactical bounce), but conviction is modest.}
CONFIDENCE {0.54}
APPLICABLE_UNIVERSE {Liquid index constituents/ETFs; avoid single-name binary catalysts.}
FAILURE_MODE {True downtrend continuation; PCR extremes persist; data quality issues in PCR sourcing.}

### Trigger / exit / invalidation conditions

- Trigger strategies only when liquidity filters pass (tight spreads, sufficient OI).
- Exit when IV Rank normalizes (<60) or a catalyst approaches (earnings within 3 days).
- Invalidate rule outputs if options inputs are stale or sourced inconsistently.

### Threshold rationale

- 80th percentile captures “high IV” without being extremely rare.
- VRP >= 5pp is sized to exceed typical estimation noise of realized vol.

## Edge Cases and Degradation

### Missing data / outliers handling

- Remove obvious bad quotes (zero IV, stale chains).
- For realized vol, remove extreme one-day returns if they are confirmed bad ticks.

### Fallback proxies

- If you cannot access option IV: use VIX/VIX9D as a market proxy and restrict outputs to **market-level** volatility regime commentary.

## Backtest Notes (Minimal)

- For strategy backtests, use mid prices and include realistic costs (crossing spreads matters).
- Falsification: if net-of-cost returns for short-premium rules are negative in multiple regimes, stop using them.
