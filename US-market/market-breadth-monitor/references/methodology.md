# Methodology: Market Breadth Monitor (US)

Breadth answers: **is the market’s strength broad-based or concentrated**? Weak breadth near index highs often precedes higher volatility or drawdowns; improving breadth supports trend persistence.

## Data Definitions

### Sources and field mapping

Breadth requires a constituent universe:
- US listed equities (NYSE/Nasdaq) or an index universe (S&P 500 / Russell 3000).
- Inputs per stock: adjusted close, volume.

Computed breadth series:
- `PctAbove200DMA(t)`: % of universe with close above 200-day MA
- `PctAbove50DMA(t)`
- `NHNL(t)`: new highs minus new lows (e.g., 252d lookback)
- `AD(t)`: advance-decline count or line

### Frequency and windows

- Daily computation; weekly summaries reduce noise.
- Lookbacks:
  - Trend MAs: 50d / 200d
  - New highs/lows: 252d
  - Signal smoothing: 5d / 20d

## Core Metrics

### Metric list and formulas

- `MAk_i(t) = mean(Close_i[t-k+1:t])`
- `PctAbove200DMA(t) = mean_i(1{Close_i(t) > MA200_i(t)})`
- `NH(t) = count_i(1{Close_i(t) = max(Close_i[t-252:t])})`
- `NL(t) = count_i(1{Close_i(t) = min(Close_i[t-252:t])})`
- `NHNL(t) = NH(t) - NL(t)` (or normalize by N)
- `AD(t) = Advancers(t) - Decliners(t)`

### Standardization

- Use percentiles for `PctAbove200DMA` and `NHNL` over 5–10y history.
- Use z-scores for `AD` only with stable universe definitions.

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

Rule 1 (broad participation → positive drift):
IF {PctAbove200DMA(t) >= 60% AND NHNL(t) is positive AND AD_line is rising over 20d}
THEN {Over the next 20–60 trading days, broad equities tend to show positive excess returns; breakouts are more reliable.}
CONFIDENCE {0.60}
APPLICABLE_UNIVERSE {US equities within the chosen universe; index/sector ETFs.}
FAILURE_MODE {Macro shock overrides breadth; universe definition changes (reconstitutions) create artificial breadth moves.}

Rule 2 (narrow leadership near highs → drawdown risk):
IF {Index is within 5% of 252d high AND PctAbove200DMA(t) <= 40% AND PctAbove200DMA trend is falling over 20d}
THEN {Over the next 20–60 trading days, drawdown probability increases and returns skew negative/weak; defensive rotation tends to help.}
CONFIDENCE {0.62}
APPLICABLE_UNIVERSE {US equity indices; sector/style rotations.}
FAILURE_MODE {Mega-cap leadership continues with strong earnings; breadth “catches up” without a drawdown.}

Rule 3 (breadth thrust off lows → tactical rebound):
IF {PctAbove50DMA rises from <= 25% to >= 50% within 10 trading days}
THEN {Over the next 5–20 trading days, equities often rally (positive excess return) as risk appetite recovers.}
CONFIDENCE {0.57}
APPLICABLE_UNIVERSE {US equity indices; tactical horizons.}
FAILURE_MODE {Bear-market rallies that fade; credit spreads remain stressed; volatility regime stays high.}

### Trigger / exit / invalidation conditions

- Trigger breadth thrust with fast transitions (10d windows).
- Exit when breadth stops improving (flat/down for 20d) or volatility regime flips higher.
- Invalidation when the universe changes materially (index reconstitution) without adjusting history.

### Threshold rationale

- 60%/40% on `PctAbove200DMA` are common “healthy vs fragile” regimes; calibrate by universe.
- Breadth thrust definitions are designed to be rare and meaningful.

## Edge Cases and Degradation

### Missing data / outliers handling

- Remove suspended/delisted names from daily denominators to avoid bias.
- Corporate actions can break MA computations; use adjusted prices.

### Fallback proxies

- If full universe data is unavailable: use sector breadth (e.g., % of sector ETFs above MAs) as a coarse substitute with lower confidence.

## Backtest Notes (Minimal)

- Build signals EOD `t`; evaluate forward 20d/60d excess return vs SPY.
- Falsification: rule fails if breadth deterioration does not increase drawdown frequency vs baseline across long samples.
