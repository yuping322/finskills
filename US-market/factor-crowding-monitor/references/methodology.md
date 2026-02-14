# Methodology: Factor Crowding Monitor (US)

“Crowding” means a large fraction of capital is positioned similarly (same factor, same winners), increasing the risk of **violent reversals** when volatility rises or liquidity tightens. This methodology uses **observable proxies** that are programmable from price data (and optionally flows).

## Data Definitions

### Sources and field mapping

Minimum:
- Daily prices for factor proxies (factor ETFs) and/or factor-sorted baskets.

Optional:
- ETF flows/AUM (provider-dependent).
- Positioning indicators (CFTC, prime broker) if available.

Core inputs:
- Factor proxy returns (e.g., momentum, value, quality, low vol) using ETFs or custom baskets.
- Underlying constituents (for dispersion/correlation proxies) if available.

### Frequency and windows

- Daily updates; crowding is typically a multi-week signal.
- Windows: 20d / 60d / 252d, with 5y history for percentiles.

## Core Metrics

### Metric list and formulas

Define a crowding score using at least two independent proxies:

1) **Factor momentum (crowding build-up)**:
- `FMOM = return_factor(60d) - return_market(60d)`

2) **Dispersion (low dispersion often implies crowding)**:
- `Disp20 = cross_sectional_std(20d returns of constituents)`

3) **Correlation (high correlation implies crowded positioning)**:
- `Corr20 = average_pairwise_corr(returns constituents, 20d)`

Example composite:
- `CrowdScore = +0.5*Z(FMOM) -0.25*Z(Disp20) +0.25*Z(Corr20)`

### Standardization

- Percentiles are preferred (fat tails).
- Ensure constituent universe is stable; otherwise use factor ETF-only proxies.

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

Rule 1 (crowded + volatility rising → reversal risk):
IF {CrowdScore percentile >= 90 AND RV20 is rising (RV20/RV60 >= 1.05)}
THEN {Over the next 20–60 trading days, the crowded factor’s relative return tends to mean-revert (negative expected relative return) and drawdown risk rises.}
CONFIDENCE {0.60}
APPLICABLE_UNIVERSE {US factor portfolios or ETFs (momentum/value/quality/low-vol); large/mid-cap universes.}
FAILURE_MODE {Persistent factor trend supported by fundamentals; “crowding” proxy is wrong due to unstable constituent sets; volatility rises but liquidity remains ample.}

Rule 2 (momentum crowding + market drawdown → momentum crash risk):
IF {Momentum factor CrowdScore percentile >= 90 AND market drawdown from 6m high <= -8%}
THEN {Over the next 20 trading days, momentum factor relative return tends to be negative (crash risk) and low-vol/quality may outperform.}
CONFIDENCE {0.65}
APPLICABLE_UNIVERSE {US momentum/quality/low-vol factor baskets.}
FAILURE_MODE {Market rebounds quickly; leadership remains stable; the drawdown is idiosyncratic to non-momentum segments.}

Rule 3 (uncrowded + improving breadth → positive relative return):
IF {CrowdScore percentile <= 20 AND factor valuation spread is favorable (value cheap vs growth, etc.)}
THEN {Over the next 3–12 months, expected relative return of the uncrowded factor is positive (mean reversion + reallocation).}
CONFIDENCE {0.55}
APPLICABLE_UNIVERSE {US factor baskets with measurable valuation spreads.}
FAILURE_MODE {Structural shifts in factor premia; valuation spread persists due to fundamental divergence; measurement differences across providers.}

### Trigger / exit / invalidation conditions

- Trigger “crowded warning” at percentile ≥90 for at least 5 consecutive sessions.
- Exit when percentile falls below 70 or volatility regime normalizes.
- Invalidate when factor definition changes (ETF reconstitution, index rule changes).

### Threshold rationale

- 90th percentile keeps the signal rare and meaningful.
- Conditioning on volatility addresses the common “crowded but still working” phase.

## Edge Cases and Degradation

### Missing data / outliers handling

- If constituent-level data is unavailable, omit Disp/Corr proxies and downgrade confidence.
- Winsorize extreme daily returns before dispersion/correlation estimation.

### Fallback proxies

- Use factor ETF return dispersion across sectors as a crude crowding proxy if only ETF data exists.

## Backtest Notes (Minimal)

- Backtest relative returns of factor proxies conditional on crowding percentiles and volatility regimes.
- Falsification: if crowded states do not show worse forward relative returns than neutral states net of trading costs.
