# Methodology: Rebalancing Planner (US)

The objective is to **design systematic rebalancing rules** that balance portfolio drift (tracking error vs target allocation) against transaction costs and market impact. This is not a one-time optimization; it is a **dynamic decision framework** that adapts to market conditions, liquidity, and cost constraints.

## Data Definitions

### Sources and field mapping

Rebalancing requires:
- **Current portfolio**: Holdings (ticker, shares, market value, weight), target allocation (target weight per asset/sector/factor)
- **Price data**: Daily adjusted close, volume (yfinance or similar)
- **Transaction costs**: Bid-ask spread, commission, market impact estimates (from liquidity-impact-estimator)
- **Volatility data**: Realized volatility (20d, 60d) to estimate drift speed
- **Correlation data**: Asset correlations to estimate portfolio risk drift

Key fields:
- `Current_weight_i`: Current portfolio weight of asset i
- `Target_weight_i`: Target portfolio weight of asset i
- `Drift_i = Current_weight_i - Target_weight_i`
- `Abs_drift_i = |Drift_i|`
- `Portfolio_drift = Σ(Abs_drift_i) / 2` (half of sum of absolute drifts)
- `Tracking_error = sqrt(Σ(Drift_i² * σ_i²))` (approximate)
- `Transaction_cost_i = Spread_i + Commission_i + Impact_i` (in bps)
- `Rebalancing_cost = Σ(|Trade_value_i| * Transaction_cost_i)`

### Frequency and windows

- **Daily monitoring**: Track drift and trigger conditions
- **Rebalancing frequency**: Depends on strategy:
  - **Time-based**: Monthly, quarterly, annually
  - **Threshold-based**: When drift >= threshold (e.g., 5%, 10%)
  - **Hybrid**: Monthly review + threshold override
- **Lookback windows**:
  - Volatility: 20d / 60d for drift speed estimation
  - Correlation: 60d / 252d for risk drift estimation
  - Transaction costs: 20d average spread, 60d ADV

## Core Metrics

### Metric list and formulas

1. **Portfolio Drift**:
   - `Portfolio_drift = Σ(|Current_weight_i - Target_weight_i|) / 2`
   - Measures total deviation from target (0% = perfect alignment, 100% = complete mismatch)

2. **Tracking Error (TE)**:
   - `TE = sqrt(Σ(Drift_i² * σ_i²) + 2 * Σ(Drift_i * Drift_j * Cov_ij))`
   - Simplified: `TE ≈ sqrt(Σ(Drift_i² * σ_i²))` (ignoring cross-terms for speed)
   - Measures expected volatility of portfolio vs target

3. **Rebalancing Cost**:
   - `Rebalancing_cost = Σ(|Trade_value_i| * (Spread_bps_i + Commission_bps_i + Impact_bps_i)) / Portfolio_value`
   - Expressed as % of portfolio value

4. **Drift Speed**:
   - `Drift_speed_i = σ_i * sqrt(Days_since_last_rebalance / 252)`
   - Estimates expected drift based on volatility
   - Higher volatility → faster drift

5. **Cost-Benefit Ratio**:
   - `Cost_benefit = Rebalancing_cost / Expected_TE_reduction`
   - Rebalance if ratio < 1 (benefit > cost)

6. **Optimal Rebalancing Threshold** (theoretical):
   - `Optimal_threshold = sqrt(2 * Transaction_cost / (σ_p² * Time_horizon))`
   - Derived from minimizing total cost (transaction + tracking error)
   - Example: If transaction cost = 20 bps, σ_p = 15% annualized, time horizon = 1 year → threshold ≈ 5%

### Standardization

- Express all costs in **basis points (bps)** for consistency
- Express drift and thresholds as **percentage points** (e.g., 5% drift = 5 percentage points)
- Use **annualized tracking error** for comparability across time horizons
- Use **percentile ranks** for drift speed (identify fastest-drifting assets)

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

Rule 1 (threshold-based rebalancing reduces TE vs time-based):
IF {Portfolio_drift >= 5% (threshold) AND Rebalancing_cost <= 0.20% (20 bps)}
THEN {Rebalancing now reduces expected tracking error by >= 50% and improves risk-adjusted returns vs waiting for calendar rebalance.}
CONFIDENCE {0.70; initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US equity portfolios with >= 10 holdings, moderate turnover (< 100% annually), and liquid assets (ADV >= $5M).}
FAILURE_MODE {Transaction costs are underestimated (hidden impact, timing costs); drift is mean-reverting (assets return to target naturally); market regime shift makes target allocation suboptimal.}

Rule 2 (high-volatility assets require tighter thresholds):
IF {Asset_i has σ_60d >= 30% (high volatility) AND Drift_i >= 3%}
THEN {Rebalancing asset i now prevents further drift and reduces tail risk; expected benefit >= 2x transaction cost over next 30 days.}
CONFIDENCE {0.65; initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US equity portfolios with high-volatility assets (small-caps, sector bets, leveraged positions).}
FAILURE_MODE {Volatility is trending (momentum continues); rebalancing into falling asset increases losses; correlation regime shifts amplify risk despite rebalancing.}

Rule 3 (cost-benefit ratio < 1 → rebalance):
IF {Expected_TE_reduction >= 1.5% (annualized) AND Rebalancing_cost <= 0.30% (30 bps)}
THEN {Rebalancing improves risk-adjusted returns; Sharpe ratio increases by >= 0.1 over next 12 months.}
CONFIDENCE {0.60; initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US equity/bond portfolios with measurable TE and transaction costs; strongest for institutional portfolios with low costs.}
FAILURE_MODE {TE reduction is overestimated (correlations change); transaction costs spike (liquidity crisis); target allocation becomes suboptimal (regime change).}

Rule 4 (avoid rebalancing during high-volatility regimes):
IF {VIX >= 30 (stress regime) AND Portfolio_drift <= 10% (moderate drift)}
THEN {Delaying rebalancing by 10-20 days reduces transaction costs by >= 30% as spreads and impact normalize; TE increase is acceptable.}
CONFIDENCE {0.65; initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US equity portfolios during market stress; strongest for portfolios with moderate drift and flexible mandates.}
FAILURE_MODE {Drift accelerates during delay (volatility persists); mandate requires strict tracking (no flexibility); client/regulator demands immediate rebalancing.}

### Trigger / exit / invalidation conditions

- **Trigger rebalancing**:
  - Threshold-based: When `Portfolio_drift >= Threshold` (e.g., 5%, 10%)
  - Time-based: On fixed calendar dates (monthly, quarterly)
  - Hybrid: Monthly review + threshold override (rebalance early if drift >= 10%)
  - Cost-benefit: When `Cost_benefit_ratio < 1`
  
- **Exit/skip rebalancing**:
  - When `Rebalancing_cost > Expected_TE_reduction` (cost > benefit)
  - When `VIX >= 30` and `Portfolio_drift <= 10%` (wait for volatility to normalize)
  - When asset is illiquid (ADV < $1M or Liquidity_days > 10)
  
- **Invalidate**:
  - When target allocation changes (strategy shift, mandate change)
  - When asset is delisted or suspended
  - When transaction cost estimates are stale (> 30 days old)

### Threshold rationale

- **5% drift threshold**: Common industry practice; balances tracking error vs transaction costs for typical portfolios (10-50 holdings, moderate volatility)
- **10% drift threshold**: For low-cost, low-turnover strategies (index funds, passive ETFs)
- **3% drift threshold**: For high-volatility assets or tight-tracking mandates (active funds, factor portfolios)
- **20 bps transaction cost**: Typical for liquid large-caps; adjust to 50-100 bps for small-caps or illiquid assets
- **VIX >= 30**: Stress regime threshold; spreads and impact typically 2-3x normal levels

## Edge Cases and Degradation

### Missing data / outliers handling

- **Missing target allocation**: Use equal-weight or market-cap-weight as default; flag as "no target specified"
- **Missing transaction cost data**: Use historical averages (20 bps for large-caps, 50 bps for mid-caps, 100 bps for small-caps); flag as "estimated costs"
- **Outliers in drift**: Cap individual asset drift at 50% (if drift > 50%, likely data error or corporate action)
- **Negative weights (short positions)**: Use absolute value for drift calculation; adjust transaction costs for borrow costs

### Fallback proxies

- **No volatility data**: Use sector average volatility or market volatility (SPY σ) with lower confidence
- **No correlation data**: Assume zero correlation (conservative; overestimates TE reduction benefit)
- **No liquidity data**: Use market cap as proxy (large-cap = liquid, small-cap = illiquid); flag as "estimated liquidity"
- **No spread data**: Use 0.05% for large-caps, 0.10% for mid-caps, 0.20% for small-caps as rough estimates

## Backtest Notes (Minimal)

- **Backtest design**: Simulate portfolio over 5-10 years with different rebalancing rules:
  - Monthly rebalancing (time-based)
  - 5% drift threshold (threshold-based)
  - 10% drift threshold (threshold-based)
  - Hybrid (monthly + 10% override)
  - Cost-benefit optimization (rebalance when ratio < 1)
  
- **Performance metrics**:
  - Tracking error (annualized)
  - Transaction costs (% of portfolio value annually)
  - Sharpe ratio vs target allocation
  - Turnover (% of portfolio traded annually)
  
- **Falsification**: Rule fails if threshold-based rebalancing does not reduce TE vs time-based, or if transaction costs exceed TE reduction
  
- **Sensitivity analysis**: Test different thresholds (3%, 5%, 7%, 10%), different cost assumptions (10 bps, 20 bps, 50 bps), and different volatility regimes (VIX < 20, 20-30, > 30)

## Rebalancing Workflow

### Step-by-step process

1. **Define target allocation**: Specify target weights for all assets/sectors/factors
2. **Monitor drift**: Calculate current weights and drift daily
3. **Evaluate trigger conditions**: Check if drift >= threshold or calendar date reached
4. **Estimate transaction costs**: Use liquidity-impact-estimator for each asset
5. **Compute cost-benefit ratio**: Compare rebalancing cost vs expected TE reduction
6. **Check market conditions**: If VIX >= 30, consider delaying unless drift is extreme (>= 15%)
7. **Generate trade list**: Calculate required trades to return to target weights
8. **Optimize execution**: Use VWAP, TWAP, or participation algorithms for large trades
9. **Execute trades**: Submit orders and monitor fills
10. **Update portfolio**: Record new weights and reset drift tracking

### Quality checks

- **Drift calculation accuracy**: Ensure current weights sum to 100% (or 100% + cash)
- **Transaction cost realism**: Verify spread and impact estimates are recent (< 30 days old)
- **Target allocation validity**: Confirm target weights sum to 100% and are feasible (no shorts if long-only mandate)
- **Liquidity constraints**: Flag assets with Liquidity_days > 5 (may require multi-day execution)

### Monitoring checklist

- **Daily**: Update current weights and drift
- **Weekly**: Review drift trends and estimate time to threshold breach
- **Monthly**: Review rebalancing performance (TE, costs, Sharpe ratio)
- **Quarterly**: Re-evaluate target allocation and rebalancing thresholds
- **Event-driven**: Rebalance immediately if mandate changes or asset is delisted

## Advanced Considerations

### Dynamic thresholds

Adjust thresholds based on market conditions:
- **Normal regime (VIX < 20)**: Use standard thresholds (5%, 10%)
- **Elevated regime (VIX 20-30)**: Widen thresholds by 20% (6%, 12%) to reduce turnover
- **Stress regime (VIX > 30)**: Widen thresholds by 50% (7.5%, 15%) or pause rebalancing unless drift is extreme

### Partial rebalancing

Instead of full rebalancing (return to exact target), use partial rebalancing:
- **Half-way rule**: Reduce drift by 50% (trade half the required amount)
- **Threshold band**: Rebalance to edge of tolerance band (e.g., if target = 10%, band = 8-12%, rebalance to 8% or 12% instead of 10%)
- **Cost-constrained**: Rebalance only assets where benefit > 2x cost

### Tax-aware rebalancing

For taxable accounts:
- **Harvest losses**: Prioritize selling assets with unrealized losses (tax benefit)
- **Defer gains**: Delay selling assets with short-term gains (< 1 year holding period)
- **Donate appreciated assets**: Use charitable donations to rebalance without triggering capital gains
- **Tax-loss threshold**: Rebalance if drift >= 5% OR unrealized loss >= 10%
