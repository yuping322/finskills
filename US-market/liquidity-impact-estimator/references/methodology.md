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

---

## Technical Notes & Implementation Details

### Market Microstructure Considerations

**Impact Model Theory**: The square-root impact model (`Impact ∝ σ * √(SizeToADV)`) is based on empirical observations that market impact scales with the square root of order size, not linearly. This reflects:
- **Order book depth**: Liquidity providers replenish at marginal rates
- **Information leakage**: Large orders signal information to market participants
- **Inventory risk**: Market makers demand compensation for holding large positions

**Venue-Specific Adjustments**:
- **Lit exchanges**: Higher impact but immediate execution
- **Dark pools**: Lower impact but execution uncertainty
- **Internalization**: Best for retail flow, limited for institutional sizes
- **ATS (Alternative Trading Systems**: Varies by venue type and participant mix

### Data Quality and Limitations

**Daily Data Limitations**:
- ADV20 masks intraday volume patterns (opening/closing auctions vs midday)
- Doesn't capture order flow imbalance (buy vs sell pressure)
- Missing hidden liquidity (dark pool volume, reserve orders)
- Spread proxy (High-Low) overstates true tradable spread

**Enhanced Data Sources** (if available):
- **TAQ (Trade and Quote) data**: Intraday price/volume at millisecond granularity
- **ITCH/LOB data**: Full order book depth and dynamics
- **FIX message data**: Actual order flow and execution details
- **Alternative data**: Payment for order flow, routing information

### Execution Strategy Integration

**Algorithm Selection Framework**:
- **VWAP (Volume-Weighted Average Price)**: Best for `SizeToADV < 20%`
- **TWAP (Time-Weighted Average Price)**: Simple, predictable execution
- **Implementation Shortfall**: Balances impact vs timing risk
- **Liquidity Seeking**: Multi-venue, adaptive algorithms
- **Passive/Reserve**: Hidden orders, minimal market impact

**Sizing Recommendations**:
```
SizeToADV < 5%:   Immediate execution acceptable
5-15%:           Use algorithmic execution over 1-3 days
15-30%:          Spread over 3-5 days, use liquidity seeking
>30%:            Consider block trading or multiple venues
```

### Cost-Benefit Analysis Framework

**Total Implementation Cost = Market Impact + Timing Risk + Opportunity Cost**

**Market Impact Components**:
- **Temporary impact**: Price moves due to order pressure (recovers)
- **Permanent impact**: Information effect, price moves permanently
- **Spread cost**: Bid-ask spread crossing cost
- **Crossing network fees**: Access fees and rebates

**Timing Risk Components**:
- **Price volatility**: σ * √(time) * position size
- **Gap risk**: Overnight/weekend price jumps
- **Liquidity risk**: ADVol deterioration during execution

**Optimization Objective**:
```
Minimize: Total Cost = Impact + λ * TimingRisk
Subject to: Execution constraints (time, venue, participation rate)
```

---

## Backtest Framework

### Backtest Design

**Objective**: Validate that liquidity impact estimates predict actual implementation shortfall.

**Methodology**:
1. **Historical Order Simulation**: Create synthetic orders of various sizes across different stocks and time periods
2. **Execution Cost Calculation**: Simulate execution using realistic algorithms (VWAP, TWAP, Implementation Shortfall)
3. **Impact Estimation**: Apply the impact model to estimate expected costs
4. **Comparison**: Compare estimated vs actual implementation shortfall

### Test Scenarios

**Size Buckets**:
- Small: SizeToADV < 2%
- Medium: SizeToADV 2-10%
- Large: SizeToADV 10-20%
- Very Large: SizeToADV > 20%

**Market Regimes**:
- Normal: VIX < 20, stable ADVol
- Volatile: VIX 20-30, moderate ADVol fluctuation
- Stress: VIX > 30, significant ADVol deterioration

**Stock Categories**:
- Mega-cap: > $100B market cap
- Large-cap: $10-100B
- Mid-cap: $2-10B
- Small-cap: $300M-2B
- Micro-cap: < $300M

### Performance Metrics

**Accuracy Metrics**:
- **Mean Absolute Error**: Average difference between predicted and actual impact
- **Root Mean Square Error**: Penalizes large errors more heavily
- **R-squared**: Proportion of variance explained by the model
- **Bias**: Systematic over/under estimation

**Utility Metrics**:
- **Hit Rate**: Percentage of times model correctly identifies high-cost trades
- **False Positive Rate**: Times model flagged high cost but actual cost was low
- **False Negative Rate**: Times model missed high-cost trades
- **Cost Savings**: Difference in implementation cost using model vs naive execution

### Statistical Validation

**Hypothesis Testing**:
- **H0**: Model predictions are not correlated with actual costs
- **H1**: Model predictions have significant predictive power
- **Test**: Correlation test, regression analysis, out-of-sample validation

**Robustness Checks**:
- **Time series cross-validation**: Rolling window validation
- **Sector-specific validation**: Test across different industries
- **Market cap segmentation**: Validate for different size categories
- **Regime analysis**: Test during different market conditions

### Falsification Criteria

Model fails if:
- **R-squared < 0.1**: Model explains less than 10% of variance
- **Hit rate < 60%**: Worse than random for identifying high-cost trades
- **Systematic bias**: Consistent over/under estimation > 20%
- **Regime breakdown**: Model performs poorly in volatile markets
- **Sector bias**: Works well only in specific industries

### Implementation Notes

**Data Requirements**:
- **Historical trade data**: At least 2 years of daily price/volume
- **Corporate action data**: Splits, dividends, symbol changes
- **Market data**: Benchmark returns, volatility indices
- **Optional**: Intraday data for enhanced accuracy

**Computational Requirements**:
- **Database**: Efficient storage and retrieval of historical data
- **Processing**: Batch processing for backtest simulations
- **Optimization**: Parameter calibration and model tuning
- **Monitoring**: Real-time model performance tracking

**Integration Points**:
- **Order Management System (OMS)**: Real-time impact estimates before order entry
- **Execution Management System (EMS)**: Algorithm selection and parameter tuning
- **Portfolio Management**: Position sizing and liquidity constraints
- **Risk Management**: Pre-trade risk checks and limits

### Model Maintenance

**Monthly Reviews**:
- Update impact coefficients based on recent market conditions
- Monitor model accuracy across different market regimes
- Adjust sector-specific parameters as needed
- Review venue-specific performance metrics

**Quarterly Reviews**:
- Comprehensive backtest refresh with latest data
- Assess model degradation and recalibrate if necessary
- Review market structure changes affecting liquidity
- Update cost-benefit optimization parameters

**Annual Overhauls**:
- Re-estimate fundamental model parameters
- Consider structural changes in market microstructure
- Evaluate new data sources and methodologies
- Update documentation and training materials

### Expected Performance

**Academic Benchmarks**:
- **R-squared**: 0.2-0.4 for simple models, 0.4-0.6 for enhanced models
- **Hit Rate**: 65-75% for identifying high-cost trades
- **Bias**: Within ±10% for well-calibrated models
- **Cost Savings**: 5-15 bps improvement over naive execution

**Realistic Expectations**:
- Model will not perfectly predict impact (inherent uncertainty)
- Performance varies by market regime and stock characteristics
- Benefits compound over many trades, not single transactions
- Regular monitoring and adjustment essential for sustained performance
