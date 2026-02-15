# Methodology: Portfolio Monitor Orchestrator (US)

The objective is to orchestrate end-to-end portfolio monitoring: risk (volatility, drawdown, VaR), concentration (sector, name, factor), exposure drift, liquidity, and scenario stress tests into one comprehensive report. This is a **risk dashboard** that aggregates multiple analytical modules.

## Data Definitions

### Sources and field mapping

Portfolio inputs:
- **User-provided**: Holdings file (CSV/JSON) with {ticker, shares/weight, cost_basis}
- **yfinance**: Current prices, volumes, historical returns (1y/3y/5y)
- **FRED**: Risk-free rate, macro indicators (for scenario analysis)

Benchmark:
- **yfinance**: Benchmark ETF (SPY, QQQ, IWM) or custom index

Derived fields:
- `position_value = shares * current_price`
- `weight = position_value / total_portfolio_value`
- `unrealized_pnl = (current_price - cost_basis) * shares`
- `sector`, `market_cap`, `factor_scores` (from holdings metadata)

### Frequency and windows

- **Snapshot**: Point-in-time (current holdings)
- **Risk metrics**: Daily returns over 252d (1y), 756d (3y)
- **Monitoring frequency**: Daily for risk metrics; weekly for comprehensive report
- **Scenario analysis**: Historical stress periods (2008, 2020, 2022)

## Core Metrics

### Metric list and formulas

#### Risk metrics

- **Portfolio volatility**:
  - `σ_p = sqrt(w' Σ w)` annualized (252d rolling covariance)
  
- **Value at Risk (VaR)** (Historical Simulation method):
  - `VaR_95 = -percentile(daily_returns, 5)` (1-day, 95% confidence)
  - `VaR_99 = -percentile(daily_returns, 1)`
  - Requires >= 252 days of history; assumes future resembles past distribution
  - Does not capture tail risk beyond historical experience; use CVaR and stress tests for tail scenarios
  
- **Conditional VaR (CVaR / Expected Shortfall)**:
  - `CVaR_95 = -mean(daily_returns | daily_returns <= VaR_95)`
  - Better measure of tail risk than VaR; captures average loss in worst 5% of cases

- **Maximum drawdown**:
  - `MDD = max_t((peak_t - trough_t) / peak_t)` over trailing 1y/3y

- **Beta to benchmark**:
  - `β = cov(R_p, R_b) / var(R_b)`

- **Sharpe ratio**:
  - `Sharpe = (μ_p - R_f) / σ_p` (annualized)

#### Concentration metrics

- **Name concentration (HHI)**:
  - `HHI_name = Σ(w_i^2)` (0 = perfectly diversified, 1 = single name)
  
- **Sector concentration**:
  - `HHI_sector = Σ(sector_weight^2)`
  
- **Top-N concentration**:
  - `Top5_weight = Σ(w_i for i in top 5 positions)`
  - `Top10_weight = Σ(w_i for i in top 10 positions)`

- **Effective number of positions**:
  - `Effective_N = 1 / HHI_name`

#### Exposure metrics

- **Sector weights** (vs benchmark):
  - `Sector_tilt = Portfolio_sector_weight - Benchmark_sector_weight`
  
- **Factor exposures** (vs benchmark):
  - Value: `Avg(P/E, P/B)` weighted by position
  - Momentum: `Avg(12m return)` weighted
  - Quality: `Avg(ROE, Debt/Equity)` weighted
  - Size: `Avg(market_cap)` weighted
  - `Factor_tilt = Portfolio_factor - Benchmark_factor`

- **Style drift**:
  - `Drift = |Current_exposure - Target_exposure|` for each dimension

#### Liquidity metrics

- **Position liquidity score**:
  - `Liquidity_i = position_value / ADV20_i` (days to liquidate)
  
- **Portfolio liquidity**:
  - `Weighted_avg_liquidity = Σ(w_i * Liquidity_i)`
  - `Illiquid_weight = Σ(w_i | Liquidity_i >= 5 days)`

- **Bid-ask impact estimate**:
  - `Spread_cost = Σ(w_i * spread_i / 2)` (one-way cost)

### Standardization

- Use percentiles for risk metrics (vs 5y history)
- Use z-scores for factor exposures (vs universe)
- Normalize sector weights to sum to 100%
- Express VaR/CVaR as % of portfolio value

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

Rule 1 (high concentration → tail risk):
IF {Top5_weight >= 50% OR HHI_name >= 0.15 OR Effective_N <= 15}
THEN {Portfolio faces elevated idiosyncratic risk; single-name events can cause material drawdowns (>= 5%).}
CONFIDENCE {0.72 — initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US equity portfolios; especially concentrated growth/conviction portfolios.}
FAILURE_MODE {Concentrated positions are intentional high-conviction bets; diversification would dilute alpha; risk is hedged.}

Rule 2 (volatility regime shift → increase drawdown risk):
IF {σ_p_20d >= 1.5 * σ_p_252d for >= 5 consecutive days (persistent volatility spike, not one-off event) AND 
    VIX >= 25 AND
    VIX has been >= 20 for >= 10 trading days (sustained elevated volatility) AND
    VIX trend is rising (VIX_5d_MA > VIX_20d_MA)}
THEN {Over the next 20–60 days, drawdown risk increases; consider reducing leverage, adding hedges, or rebalancing to lower-beta names.}
CONFIDENCE {0.68 — initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US equity portfolios; especially leveraged or high-beta portfolios.}
FAILURE_MODE {Volatility spike is short-lived; portfolio has defensive characteristics; hedges are already in place.}
ADDITIONAL_FILTERS {
  - Check if volatility spike is portfolio-specific or market-wide:
    * If only 1-2 holdings drive the spike: Lower confidence (idiosyncratic event)
    * If broad-based (>= 50% of holdings show elevated vol): Higher confidence (systemic risk)
  - Check correlation structure:
    * If correlations are rising (>= 20% increase): Higher risk
    * If correlations stable or declining: Lower risk}

Rule 3 (liquidity mismatch → execution risk - dynamic thresholds):
Base thresholds adjust by market regime:
- Normal market (VIX < 20): Liquidity_i >= 10 days triggers warning; Illiquid_weight >= 20%
- Elevated vol (VIX 20-30): Liquidity_i >= 5 days triggers warning; Illiquid_weight >= 15%
- High stress (VIX > 30): Liquidity_i >= 3 days triggers warning; Illiquid_weight >= 10%

Additional dynamic adjustments:
- If ADV has declined >= 30% over past 20 days: Reduce all thresholds by 30%
- If bid-ask spreads have widened >= 50%: Reduce all thresholds by 20%

IF {Illiquid_weight >= threshold(VIX, ADV_trend, spread_trend) OR 
    any position has Liquidity_i >= threshold(VIX, ADV_trend, spread_trend)}
THEN {Portfolio faces material execution risk in stress scenarios; rebalancing or exit may take weeks and incur >= 100bps slippage in normal markets, >= 200bps in stress.}
CONFIDENCE {0.70 — initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US equity portfolios; especially with small-cap or niche exposures.}
FAILURE_MODE {Portfolio is long-term hold (no forced selling); hidden liquidity (dark pools) available; positions are hedged.}
NOTE {Adjust thresholds based on investor type: retail (use base thresholds), institutional (multiply by 0.5), hedge fund (multiply by 0.3)}

Rule 4 (factor crowding → reversal risk):
IF {Factor_tilt >= 1.5 std dev on any factor AND factor is at historical valuation extreme (>= 90th percentile)}
THEN {Over the next 6–24 months, factor reversal risk is elevated; consider rebalancing or adding offsetting exposures.}
CONFIDENCE {0.60 — initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US equity portfolios with measurable factor tilts.}
FAILURE_MODE {Factor continues to work (momentum in trends); valuation is poor timing signal; tilt is intentional strategy.}

Rule 5 (sector drift → unintended risk):
IF {|Sector_tilt| >= 10% for any sector AND drift is unintentional (not part of strategy)}
THEN {Portfolio has accumulated unintended sector risk; rebalance to target weights or acknowledge new risk profile.}
CONFIDENCE {0.65 — initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US equity portfolios with defined sector targets.}
FAILURE_MODE {Drift is due to strong performance (winners running); rebalancing would hurt returns; drift is within tolerance bands.}

### Trigger / exit / invalidation conditions

- **Trigger rebalance**: When concentration exceeds limits OR sector drift >= 10% OR volatility regime shifts
- **Trigger risk review**: When VaR_95 >= 3% (1-day) OR MDD >= 15% (trailing 1y)
- **Exit positions**: When liquidity deteriorates (ADV drops >= 50%) OR fundamental thesis breaks
- **Invalidate metrics**: When holdings data is stale (>= 7 days) OR corporate actions distort prices

### Threshold rationale

- **Top5 50%**: Practical concentration limit for diversified portfolios
- **HHI 0.15**: Equivalent to ~7 equal-weighted positions; minimum for risk reduction
- **Liquidity 10 days**: Practical limit for orderly exit without material impact
- **VaR 3%**: Equivalent to ~15% annualized volatility; typical equity portfolio threshold
- **Sector drift 10%**: Material enough to change risk profile; common rebalancing trigger

## Edge Cases and Degradation

### Missing data / outliers handling

- **Cost basis unavailable**: Use current price as proxy; mark unrealized P&L as unavailable
- **Sector classification missing**: Use ticker-based lookup (GICS, FactSet) or manual classification
- **Short history**: If position has < 252 days, use available data but flag low confidence on volatility/correlation
- **Corporate actions**: Adjust for splits, spinoffs, mergers; use total return series when available
- **Outliers**: Winsorize daily returns at +/- 10% to reduce impact of data errors

### Fallback proxies when a data source is unavailable

- **No benchmark**: Use SPY as default for broad US equity portfolios; QQQ for tech-heavy; IWM for small-cap
- **No factor scores**: Use simple proxies:
  - Value: Inverse of P/E ratio (from yfinance fundamentals)
  - Momentum: Trailing 12-month return
  - Quality: Use sector as proxy (Tech/Healthcare = quality)
  - Size: Market cap from yfinance
- **No liquidity data**: Use market cap as proxy (large cap = liquid, small cap = illiquid)
- **No VIX**: Use realized portfolio volatility percentile as regime indicator

## Scenario Analysis (Stress Tests)

Test portfolio performance under historical stress scenarios:

### Scenario definitions

Note: The following are approximate historical returns; actual implementation should use precise historical data.

1. **2008 Financial Crisis** (Sep 2008 - Mar 2009):
   - SPY: -50%, Financials: -70%, Treasuries: +15%
   - Source: Approximate peak-to-trough returns during crisis period
   
2. **COVID Crash** (Feb 2020 - Mar 2020):
   - SPY: -34%, Energy: -50%, Tech: -25%, Treasuries: +10%
   - Source: Approximate returns during Feb-Mar 2020 drawdown
   
3. **2022 Rate Shock** (Jan 2022 - Oct 2022):
   - SPY: -25%, Tech: -35%, Utilities: -10%, Treasuries: -15%
   - Source: Approximate returns during 2022 rate hiking cycle

4. **Custom scenario** (user-defined):
   - Specify sector/factor shocks

### Stress test methodology

Enhanced methodology accounting for correlation regime shifts and liquidity effects:

1. **Base case** (linear approximation):
   ```
   Loss_base = Σ(w_i * scenario_return_i)
   ```

2. **Correlation adjustment** (stress scenarios increase correlations):
   - In stress scenarios, pairwise correlations increase:
     * Normal correlation < 0.5: increase to 0.7
     * Normal correlation 0.5-0.7: increase to 0.85
     * Normal correlation > 0.7: increase to 0.95
   - Recalculate portfolio volatility with stressed correlations:
     ```
     σ_stressed = sqrt(w' Σ_stressed w)
     Correlation_adjustment_factor = (σ_stressed - σ_normal) / σ_normal
     Correlation_loss = Loss_base * Correlation_adjustment_factor * 0.5
     ```

3. **Liquidity adjustment** (forced selling at worse prices):
   - For positions with Liquidity_i >= 5 days:
     ```
     Haircut_i = 5% + (Liquidity_i - 5) * 1%  (capped at 20%)
     Liquidity_loss = Σ(w_i * |scenario_return_i| * Haircut_i) for illiquid positions
     ```

4. **Total stressed loss**:
   ```
   Loss_total = Loss_base + Correlation_loss + Liquidity_loss
   ```

5. **Confidence intervals**:
   - Report 50th, 75th, 95th percentile losses
   - Based on historical stress scenario distribution
   - 50th percentile ≈ Loss_base
   - 95th percentile ≈ Loss_total

Example calculation:
- Base loss: -15%
- Correlation adjustment: -3% (correlations spike)
- Liquidity adjustment: -2% (forced selling)
- Total stressed loss: -20% (95th percentile)

## Monitoring Checklist Template

Daily/weekly monitoring should include:

1. **Risk snapshot**: σ_p, VaR, MDD, Beta
2. **Concentration**: Top5 weight, HHI, Effective_N
3. **Exposures**: Sector weights, factor tilts vs benchmark
4. **Liquidity**: Illiquid weight, largest position liquidity
5. **Performance**: Return vs benchmark (1d, 1w, 1m, YTD)
6. **Alerts**: Any threshold breaches or regime shifts
7. **Scenario results**: Estimated loss in stress scenarios

## Backtest Notes (Minimal)

- Simulate portfolio over historical period with monthly rebalancing
- Calculate realized Sharpe, MDD, tracking error
- Test if concentration/liquidity warnings preceded actual drawdowns
- Validate VaR accuracy: compare predicted VaR to realized losses (backtesting VaR)
- Falsification: If high-concentration portfolios do not show higher MDD vs diversified portfolios in your universe
- Note: Confidence levels above are initial estimates and should be updated based on backtest results
