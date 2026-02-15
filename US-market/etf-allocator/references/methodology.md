# Methodology: ETF Allocator & Exposure Analyzer (US)

The objective is to construct ETF allocations that meet specified constraints (risk budget, sector/factor exposures, liquidity) and quantify tracking error, concentration, and hidden factor tilts. This is a **portfolio construction and risk decomposition** tool.

## Data Definitions

### Sources and field mapping

ETF data:
- **yfinance**: ETF prices, volumes, expense ratios
- **ETF provider websites**: Holdings files (CSV/JSON) for sector/factor decomposition
- **FRED**: Risk-free rate (3-month T-bill) for Sharpe calculations

Key fields per ETF:
- `ticker`, `close`, `volume`, `expense_ratio`
- `holdings`: List of {ticker, weight, sector, market_cap}
- `AUM`, `avg_spread` (bid-ask)

Derived fields:
- `sector_exposure = Σ(holding_weight * holding_sector)`
- `factor_exposure = Σ(holding_weight * holding_factor_score)` (e.g., value, momentum, quality)
- `effective_N = 1 / Σ(weight_i^2)` (diversification measure)

### Frequency and windows

- **Portfolio construction**: Point-in-time (use latest holdings)
- **Backtest/risk**: Daily returns over 1y / 3y / 5y
- **Rebalance frequency**: Monthly or quarterly (user-specified)

## Core Metrics

### Metric list and formulas

#### Portfolio-level metrics

- **Expected return** (historical proxy):
  - `E[R_p] = Σ(w_i * μ_i)` where `μ_i` = trailing 1y/3y annualized return
  
- **Portfolio volatility**:
  - `σ_p = sqrt(w' Σ w)` where `Σ` = covariance matrix (252d rolling)
  
- **Sharpe ratio**:
  - `Sharpe = (E[R_p] - R_f) / σ_p`

- **Maximum drawdown**:
  - `MDD = max_t((peak_t - trough_t) / peak_t)`

#### Exposure metrics

- **Sector concentration**:
  - `HHI_sector = Σ(sector_weight^2)` (0 = perfectly diversified, 1 = single sector)
  
- **Factor tilts** (vs benchmark):
  - `Tilt_factor = Portfolio_factor_score - Benchmark_factor_score`
  - Factors: Value (P/E, P/B), Momentum (12m return), Quality (ROE, debt/equity), Size (market cap)

- **Effective number of holdings**:
  - `Effective_N = 1 / Σ(w_i^2)` across all underlying holdings

#### Tracking metrics (vs benchmark)

- **Tracking error**:
  - `TE = std(R_p - R_b)` annualized
  
- **Active share** (requires full holdings):
  - `ActiveShare = 0.5 * Σ|w_p,i - w_b,i|`
  - Range: 0% (perfect index replication) to 100% (no overlap with benchmark)

- **Beta to benchmark**:
  - `β = cov(R_p, R_b) / var(R_b)`

### Standardization

- Use percentiles for factor scores (0–100 within universe)
- Use z-scores for tracking error and volatility (vs historical distribution)
- Normalize sector weights to sum to 100%

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

Rule 1 (high concentration → tail risk):
IF {HHI_sector >= 0.30 OR Effective_N <= 20}
THEN {Portfolio faces higher idiosyncratic risk; drawdowns tend to be larger and more frequent than diversified portfolios, especially when holdings are correlated.}
CONFIDENCE {0.70 — initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US ETF portfolios; especially thematic/sector-focused allocations.}
FAILURE_MODE {Concentrated bet is correct (e.g., tech in 2010s); diversification hurts returns; risk is intentional.}
RISK_AMPLIFICATION {Risk is significantly amplified if:
  - Average pairwise correlation of top 10 holdings >= 0.6 (high correlation + high concentration = elevated tail risk)
  - Holdings are in same sector/factor with correlation >= 0.7 during stress periods
  Risk is mitigated if:
  - Holdings span uncorrelated sectors/factors with average correlation < 0.4
  - Concentration is intentional with hedges in place}

Rule 2a (low tracking error + low active share → strong closet indexing):
IF {Tracking_error <= 2% AND ActiveShare <= 30%}
THEN {Strong closet indexing signal; portfolio is effectively an expensive index fund; expected alpha is near zero; consider lower-cost passive alternative.}
CONFIDENCE {0.75 — initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US ETF portfolios benchmarked to broad indices (SPY, QQQ).}
FAILURE_MODE {Small tilts generate meaningful alpha; low TE is intentional for risk management.}

Rule 2b (moderate tracking error + moderate active share → moderate closet indexing):
IF {Tracking_error <= 3% AND ActiveShare <= 40% AND (TE * ActiveShare) <= 120}
THEN {Moderate closet indexing signal; limited alpha potential; evaluate if fees justify the strategy.}
CONFIDENCE {0.65 — initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US ETF portfolios with enhanced indexing strategies.}
FAILURE_MODE {Strategy generates consistent small alpha; risk-adjusted returns justify fees.}
NOTE {Combined metric (TE * ActiveShare) helps identify closet indexing: Pure index ≈ 0, True active ≈ 400, Closet indexer ≈ 60-120}

Rule 3 (factor crowding → reversal risk):
IF {Portfolio has extreme factor tilt (>= 90th percentile on momentum or value within universe) AND
    Market-wide factor crowding is elevated (measured by one or more of:
      - Factor ETF net inflows >= 80th percentile over past 3 months
      - Aggregate institutional positioning shows >= 80th percentile factor exposure
      - Factor return dispersion <= 20th percentile, indicating crowded positioning) AND
    Factor valuation >= 90th percentile (expensive vs historical range)}
THEN {Over the next 6–24 months, factor reversal risk is elevated; consider rebalancing or hedging.}
CONFIDENCE {0.58 — initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US factor ETFs; style-tilted portfolios.}
FAILURE_MODE {Factor continues to work (e.g., momentum in strong trends); valuation metrics are poor timing tools.}
CONTRARIAN_NOTE {If portfolio tilt is OPPOSITE to market crowding (e.g., portfolio tilts value when market crowds growth), this represents contrarian positioning, not crowding risk; reversal risk is actually lower in this case.}

Rule 4 (liquidity mismatch → execution risk):
IF {Portfolio weight in ETF_i >= 10% AND ETF_i avg daily volume <= $5M}
THEN {Rebalancing or exit may face material slippage (>= 50bps); reduce position size or extend execution horizon.}
CONFIDENCE {0.72 — initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US ETF portfolios; especially with niche/thematic ETFs.}
FAILURE_MODE {Hidden liquidity (APs, dark pools) reduces impact; position is long-term hold (no rebalancing).}

### Trigger / exit / invalidation conditions

- **Trigger rebalance**: When sector/factor drift exceeds +/- 5% from target OR volatility regime shifts
- **Exit position**: When ETF liquidity deteriorates (ADV drops >= 30%) OR expense ratio increases materially
- **Invalidate allocation**: When holdings data is stale (>= 90 days old) OR ETF strategy changes (merger, reconstitution)

### Threshold rationale

- **HHI 0.30**: Equivalent to ~3-4 equal-weighted sectors; practical diversification threshold
- **Effective_N 20**: Minimum for reasonable idiosyncratic risk reduction
- **Tracking error 2%**: Typical "enhanced index" range; below this is closet indexing
- **ADV $5M**: Practical liquidity floor for institutional-sized positions

## Edge Cases and Degradation

### Missing data / outliers handling

- **Holdings unavailable**: Use sector classification from ETF name/description; mark factor analysis as unavailable
- **Short history**: If ETF has < 252 trading days, use available data but flag low confidence on volatility/correlation estimates
- **Corporate actions**: Adjust for splits, dividends in return calculations; use total return series when available
- **Outliers**: Winsorize daily returns at +/- 10% to reduce impact of flash crashes or data errors

### Fallback proxies when a data source is unavailable

- **No holdings files**: Use ETF category/style classification (Morningstar, ETF.com) as coarse sector proxy
- **No factor scores**: Use simple proxies:
  - Value: Inverse of P/E ratio
  - Momentum: Trailing 12-month return
  - Quality: Use sector as rough proxy (Tech/Healthcare tend to be higher quality) OR mark quality analysis as unavailable if fundamental data is missing
- **No benchmark data**: Use SPY as default benchmark for broad US equity portfolios
- **No expense ratios**: Assume 0.50% for active ETFs, 0.10% for passive; mark as estimate

## Backtest Notes (Minimal)

- Construct portfolio at month-end using latest holdings
- Rebalance monthly or quarterly (user-specified)
- Calculate realized Sharpe, MDD, tracking error over 1y / 3y / 5y
- Compare to benchmark and equal-weighted portfolio
- Validate concentration/liquidity rules by testing if they predict higher realized volatility or drawdowns
- Falsification: If optimized allocation does not improve risk-adjusted returns vs naive equal-weight after costs
- Note: Confidence levels above are initial estimates and should be updated based on backtest results

## Optimization Constraints (Optional)

When constructing allocations programmatically:

- **Weight bounds**: `w_i ∈ [w_min, w_max]` (e.g., [0.05, 0.30])
- **Sector limits**: `Σ(w_i * sector_i) <= sector_max` (e.g., Tech <= 30%)
- **Turnover limit**: `Σ|w_new - w_old| <= turnover_max` (e.g., 20% per rebalance)
- **Liquidity constraint**: `w_i * Portfolio_value <= k * ADV_i` (e.g., k=0.10 for 10% ADV)

Objective functions:
- Maximize Sharpe ratio
- Minimize volatility (subject to return target)
- Minimize tracking error (enhanced indexing)
- Maximize diversification (maximize Effective_N)
