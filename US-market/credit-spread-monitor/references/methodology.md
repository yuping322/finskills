# Methodology: Credit Spreads Monitor (US)

Credit spreads summarize **the market’s price of default/liquidity risk**. When spreads widen sharply, equities (especially cyclicals/financials/small caps) tend to face higher drawdown risk; when spreads tighten sustainably, risk appetite usually improves.

This methodology is designed to produce **programmable, backtestable, falsifiable** “insight rules” rather than narrative-only commentary.

## Data Definitions

### Sources and field mapping (FRED preferred)

Use any consistent source; for reproducibility, prefer FRED series:

- **High yield OAS**: ICE BofA US High Yield Option-Adjusted Spread (e.g., `BAMLH0A0HYM2`, units: %).
- **Investment grade OAS**: ICE BofA US Corporate OAS (e.g., `BAMLC0A0CM`, units: %).
- **Corporate vs Treasury proxy** (fallback): Moody’s BAA yield minus 10Y Treasury (`BAA` − `DGS10`), units: %.
- **Risk controls** (optional): VIX (`VIXCLS`), 10Y Treasury yield (`DGS10`), unemployment (`UNRATE`).

Field normalization:
- Convert percent to **basis points**: `spread_bps = spread_pct * 100`.
- Align to **daily** frequency; forward-fill macro series within the same week (but do not forward-fill across missing weeks).

### Frequency and windows (daily/weekly)

Default calculation windows (trading days):
- Short change: `Δ5 = spread(t) - spread(t-5)`
- Medium change: `Δ20`
- Regime: `Δ60`
- Standardization lookback: `L = 252 * 5` (≈5y) when available; otherwise `L = 252 * 3`.

## Core Metrics

### Metric list and formulas

- **Level**: `S(t)` = HY OAS in bps (or IG OAS / BAA–UST proxy).
- **Change**: `Δk(t) = S(t) - S(t-k)`.
- **Z-score** (level): `ZL(t) = (S(t) - mean(S[t-L:t])) / std(S[t-L:t])`.
- **Z-score** (momentum): `ZM20(t) = (Δ20(t) - mean(Δ20[t-L:t])) / std(Δ20[t-L:t])`.
- **Stress composite** (optional): `Stress(t) = 0.7*ZL(t) + 0.3*ZM20(t)`.

### Standardization (z-scores, percentiles)

Preferred:
- Use **rolling z-scores** on levels and changes (stable across regimes).
- Also report **percentile rank** of `S(t)` within the last 5y (robust to fat tails).

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

Rule 1 (risk-off impulse):
IF {HY_OAS_ZL(t) >= 1.5 AND HY_OAS_Δ20(t) > 0}
THEN {Over the next 20–60 trading days, broad equities (SPY) have higher drawdown probability and negative/weak excess returns vs cash; defensives tend to outperform cyclicals.}
CONFIDENCE {0.67}
APPLICABLE_UNIVERSE {US large/mid-cap equities; sector baskets (defensive vs cyclical); liquid ETFs.}
FAILURE_MODE {Rapid policy backstop/liquidity injection that reverses spreads; idiosyncratic spread widening isolated to one sector without broader contagion; measurement breaks from series revisions.}

Rule 2 (stress peak → reflexive bounce):
IF {HY_OAS_ZL(t) >= 2.0 AND HY_OAS_Δ5(t) < 0 AND SPY drawdown from 60d high <= -8%}
THEN {Over the next 5–20 trading days, equities often stage a tactical rebound (positive excess return), but medium-term risk can remain elevated.}
CONFIDENCE {0.58}
APPLICABLE_UNIVERSE {US index/large-cap equities; tactical horizons; highly liquid names.}
FAILURE_MODE {True credit event (defaults/liquidity freeze) where spreads remain elevated; macro recession acceleration; equities gap lower despite initial spread tightening.}

Rule 3 (non-confirmation / weak signal):
IF {HY_OAS_ZL(t) < 1.0 AND HY_OAS_Δ20(t) > 0 AND VIX_Z(t) < 1.0}
THEN {Credit spreads are not confirming an equity risk-off regime; treat as a low-conviction warning rather than a trade signal (equity return direction ~neutral).}
CONFIDENCE {0.55}
APPLICABLE_UNIVERSE {US equities broad; cross-asset monitors.}
FAILURE_MODE {VIX suppressed by structural flows while credit deteriorates; delayed equity reaction; macro data revisions that reclassify the period ex-post.}

### Trigger / exit / invalidation conditions

- **Trigger (risk-off)**: `HY_OAS_ZL >= 1.5` OR `Stress >= 1.5`.
- **Exit (risk-off)**: `HY_OAS_ZL <= 0.5` AND `HY_OAS_Δ20 < 0`.
- **Invalidation** (do not generalize): spread move is driven by a narrow sector (e.g., energy) while IG OAS and breadth indicators stay benign; or data is stale/revised.

### Threshold rationale (historical distribution)

- `Z >= 1.5` is a practical “stress” threshold across long samples where spreads are heavy-tailed.
- Use percentiles when history is short: stress if `S(t)` is in the **top decile** of the last 3–5 years.

## Edge Cases and Degradation

### Missing data / outliers handling

- Winsorize `S(t)` changes at the 1st/99th percentile of `Δ20` for z-score stability.
- If `std` in lookback is near 0 (rare), fall back to percentile-based thresholds.
- Always annotate **as-of** timestamps; some series update with a lag.

### Fallback proxies when a data source is unavailable

- If HY OAS is unavailable: use `BAA - DGS10` as a coarse proxy.
- If all spread data is missing: use ETF proxies (e.g., relative returns of `HYG` vs `LQD`, and `LQD` vs `TLT`) and treat results as **lower confidence**.

## Backtest Notes (Minimal)

- Signal timestamp: compute at EOD `t`; evaluate forward returns from `t+1` close.
- Horizons: 5d / 20d / 60d; report **excess return vs SPY** (or vs cash for “risk-off” rules).
- Falsification: a rule is considered broken if rolling 5y mean excess return flips sign **and** net-of-cost Sharpe is non-positive.
