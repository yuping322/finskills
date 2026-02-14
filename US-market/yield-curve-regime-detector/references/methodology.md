# Methodology: Yield Curve Regime Detector (US)

The yield curve encodes **growth/inflation expectations and monetary stance**. Persistent inversion is historically associated with higher recession risk, while steepening can be “good” (growth up) or “bad” (late-cycle stress). This file defines measurable curve regimes and converts them into falsifiable “insight rules”.

## Data Definitions

### Sources and field mapping (FRED preferred)

Preferred daily series (FRED):
- `DGS10`: 10-year Treasury constant maturity yield (%)
- `DGS2`: 2-year Treasury yield (%)
- `TB3MS` (monthly) or `DGS3MO` (if available): 3-month Treasury yield (%)

Derived fields:
- `S10_2 = DGS10 - DGS2` (pp)
- `S10_3M = DGS10 - 3M` (pp)
- Convert to bps when reporting: `pp * 100`.

### Frequency and windows

- Primary: daily; align yields on common dates.
- Windows:
  - Regime persistence: 60–90 trading days
  - Trend: 20 trading days (≈1m)
  - Backtest horizons: 20 / 60 / 252 trading days

## Core Metrics

### Metric list and formulas

- **Slope level**: `S10_2(t)`, `S10_3M(t)`
- **Inversion duration**: `InvDays = count_{i=1..N}(S(t-i) < 0)` over `N=90`
- **Steepening type**:
  - Bull steepener: `DGS2` falling faster than `DGS10` (front-end easing)
  - Bear steepener: `DGS10` rising faster than `DGS2` (term premium/inflation shock)
- **Slope z-score** (optional): `ZSlope(t)` on `S10_2` over 5y lookback

### Standardization

- Prefer regime definitions by **sign + persistence** (robust).
- Use z-scores/percentiles for “extreme” classification when history is long enough.

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

Rule 1 (persistent inversion → late-cycle risk):
IF {S10_3M(t) < 0 for >= 60 trading days}
THEN {Over the next 6–18 months, US equities have below-average returns and higher drawdown risk; defensives (staples/healthcare) tend to outperform cyclicals.}
CONFIDENCE {0.63}
APPLICABLE_UNIVERSE {US broad equity index and sector baskets; liquid ETFs.}
FAILURE_MODE {Structural changes in term premium; heavy policy intervention; inversion driven by technical factors while growth stays strong.}

Rule 2 (re-steepening from inversion + credit stress is “bad steepening”):
IF {S10_2 increases by > +50 bps over 60 trading days AND HY_OAS_ZL(t) >= 1.0}
THEN {Over the next 1–3 months, equity returns skew negative and volatility rises (late-cycle transition).}
CONFIDENCE {0.60}
APPLICABLE_UNIVERSE {US equities, especially cyclicals/financials/small caps.}
FAILURE_MODE {Soft-landing with rapid disinflation and contained defaults; spreads tighten quickly after a brief stress pulse.}

Rule 3 (growth-driven steepening is risk-on):
IF {S10_2 increases by > +40 bps over 60 trading days AND credit spreads are tightening (HY_OAS_Δ20 < 0)}
THEN {Over the next 1–3 months, equities tend to have positive excess returns; cyclicals/industrials often outperform defensives.}
CONFIDENCE {0.58}
APPLICABLE_UNIVERSE {US equities and sector relative trades.}
FAILURE_MODE {Inflation shock masquerading as “growth”; sharp rate spikes that compress equity multiples; exogenous risk shocks.}

### Trigger / exit / invalidation conditions

- **Regime trigger**:
  - Inversion: `S10_3M < 0` (primary) or `S10_2 < 0` (secondary) with persistence ≥60d.
  - Steepening: `Δ60(S10_2) > +50 bps` and classify bull vs bear steepening by yield contributions.
- **Exit**: regime ends when slope returns above 0 and remains >0 for 20 trading days.
- **Invalidation**: if curve signals conflict with credit (spreads benign) and labor is strong; downgrade confidence.

### Threshold rationale

- 60 trading days reduces false positives from short-lived inversions.
- Magnitude thresholds (40–50 bps) are sized to exceed typical month-to-month noise.

## Edge Cases and Degradation

### Missing data / outliers handling

- Yields can have missing holidays; align on intersection of dates.
- Avoid spurious “jumps” from stale series; annotate as-of dates.

### Fallback proxies

- If 3M series is unavailable at daily frequency, use monthly `TB3MS` and perform monthly backtests.
- If curve data is delayed, use liquid rate proxies (e.g., 2Y/10Y Treasury ETFs) as rough substitutes and lower confidence.

## Backtest Notes (Minimal)

- Signal timestamp: compute at EOD `t` using yields up to `t`.
- Forward returns: 20d / 60d / 252d excess return vs SPY (or sector ETFs for relative tests).
- Falsification: rule fails if the sign of mean forward excess return is consistently opposite in rolling 10y windows.
