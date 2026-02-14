# Methodology: Macro Liquidity Monitor (US)

“Liquidity” here means the **price and availability of funding** (policy rates, real rates, credit conditions). The objective is to translate macro/credit inputs into testable regime calls (risk-on vs risk-off) and sector/style tilts.

## Data Definitions

### Sources and field mapping (FRED + liquid proxies)

Preferred series (FRED):
- **Policy**: Effective Fed Funds Rate `DFF` (%)
- **Rates**: `DGS2`, `DGS10` (%)
- **Inflation**: CPI `CPIAUCSL` (YoY %), Core PCE (if available)
- **Real rate proxy**: 10Y TIPS yield (if available) or `DGS10 - 10Y breakeven`
- **Credit stress**: HY OAS `BAMLH0A0HYM2` (%)
- **Dollar** (optional): broad USD index (or proxy ETF if using market data)

Normalize:
- Convert spreads to **bps** where relevant.
- Align macro series to daily by forward-filling within the same week; never fabricate missing months/quarters.

### Frequency and windows

Defaults:
- Daily inputs; compute 20d / 60d changes.
- Use 252*5 (≈5y) lookback for percentiles when available.

## Core Metrics

### Metric list and formulas

- **Real rate change**: `Δ60(real10y)` (bps)
- **Policy impulse**: `Δ60(DFF)` (bps)
- **Credit impulse**: `Z(HY_OAS)` and `Δ20(HY_OAS)`
- **Rates shock**: `Δ20(DGS10)` (bps)
- **Composite liquidity score** (example):
  - `LiqScore = -0.5*Z(real10y) -0.2*Z(DFF) -0.3*Z(HY_OAS)`
  - Higher = easier conditions

### Standardization

- Prefer z-scores / percentiles to compare across periods.
- Where macro series are low-frequency (monthly), run regime classification monthly.

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

Rule 1 (easing impulse → risk-on):
IF {Δ60(real10y) <= -50 bps AND HY_OAS_ZL(t) <= 0.5}
THEN {Over the next 20–60 trading days, US equities tend to have positive excess returns; long-duration/growth often outperform value.}
CONFIDENCE {0.62}
APPLICABLE_UNIVERSE {US equities; style/sector baskets; liquid ETFs.}
FAILURE_MODE {Inflation re-acceleration causing long yields to reprice higher; growth scare where spreads widen despite lower real rates.}

Rule 2 (tightening + widening spreads → risk-off):
IF {Δ60(real10y) >= +50 bps OR Δ60(DFF) >= +50 bps} AND {HY_OAS_ZL(t) >= 1.0}
THEN {Over the next 20–60 trading days, equity returns skew negative and defensives/quality tend to outperform.}
CONFIDENCE {0.65}
APPLICABLE_UNIVERSE {US equities, especially cyclicals/high beta; credit-sensitive segments.}
FAILURE_MODE {Policy pivot arrives faster than markets expect; spreads mean-revert quickly; strong earnings offset tightening.}

Rule 3 (rates shock hurts duration more than “the market”):
IF {Δ20(DGS10) >= +50 bps AND inflation_YoY is rising}
THEN {Over the next 20–60 trading days, long-duration growth and long Treasuries tend to underperform; value/energy often outperform.}
CONFIDENCE {0.60}
APPLICABLE_UNIVERSE {US equities by duration factor; bond ETFs across duration; sector baskets.}
FAILURE_MODE {Rates shock is driven by stronger real growth with improving margins; equity multiples stay resilient.}

### Trigger / exit / invalidation conditions

- **Risk-on**: `LiqScore` in top 30% of 5y history AND `HY_OAS_ZL <= 0.5`.
- **Risk-off**: `LiqScore` in bottom 30% OR `HY_OAS_ZL >= 1.5`.
- **Exit**: regime flips when composite crosses median and stays for 20 trading days.
- **Invalidation**: when signals conflict (e.g., real rates fall but spreads widen); reduce confidence and explicitly list the conflict.

### Threshold rationale

- 50 bps over ~3 months is large relative to typical macro drift.
- Conditioning on credit spreads filters “rates-only” noise.

## Edge Cases and Degradation

### Missing data / outliers handling

- Macro series revise; keep a snapshot timestamp and expect revisions.
- Winsorize rate changes at 1st/99th percentiles for z-score stability.

### Fallback proxies

- If TIPS/real rates are unavailable: use `DGS10` (nominal) + inflation trend as a coarse substitute.
- If HY OAS is unavailable: use BAA–UST proxy; lower confidence.

## Backtest Notes (Minimal)

- Build regime labels monthly/daily depending on inputs; hold positions for 1–3 months per regime.
- Falsification: if regime-conditional excess returns vs SPY are not directionally stable across at least two decades of data.
