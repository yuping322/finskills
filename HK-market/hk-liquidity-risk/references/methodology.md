# Methodology: HK Liquidity Risk Monitor (港股流动性风险监控器)

港股流动性风险监控器提供市场流动性分析、个股流动性风险评估和交易执行建议的综合框架。

## Data Definitions

### Sources and field mapping

**Primary Data Sources**:
- **HKEX**: Real-time order book and trade data
- **Major Brokers**: Liquidity research and execution data
- **Data Vendors**: High-frequency market data services
- **Academic Research**: Liquidity risk models and studies

**Core Liquidity Metrics**:
- **Bid-Ask Spread**: `Spread = (Ask - Bid) / MidPrice`
- **Market Depth**: Sum of available shares at best bid/ask prices
- **Trading Volume**: Number of shares traded in given period
- **Turnover Rate**: `Turnover = Volume / SharesOutstanding`

**Order Book Data**:
- **Level 1 Data**: Best bid/ask prices and sizes
- **Level 2 Data**: Full order book (typically 5-10 levels)
- **Trade Data**: All executed trades with timestamps
- **Quote Data**: All quote updates with timestamps

### Frequency and windows

- **Real-time**: Tick-by-tick data during trading hours
- **Intraday**: 1-minute, 5-minute, 15-minute aggregations
- **Daily**: End-of-day liquidity metrics
- **Historical**: 5+ years for liquidity regime analysis

## Core Metrics

### Metric list and formulas

**Market-Level Liquidity**:
1. **Market Spread**: `MarketSpread = Σ(Weight_i × Spread_i)`
2. **Market Depth**: `MarketDepth = Σ(BidSize_i + AskSize_i)`
3. **Market Volume**: `MarketVolume = Σ(Volume_i)`
4. **Liquidity Index**: `LiqIndex = (Volume / Spread) × (Depth / MarketCap)`

**Stock-Level Liquidity**:
1. **Amihud Illiquidity**: `ILLIQ = |Return| / (Volume × Price)`
2. **Roll Spread**: `Spread_Roll = 2 × sqrt(Var(ΔPrice))`
3. **Effective Spread**: `EffSpread = 2 × |TradePrice - MidPrice| / MidPrice`
4. **Liquidity Score**: `LiqScore = w1×VolumeScore + w2×SpreadScore + w3×DepthScore`

**Market Impact Models**:
1. **Linear Impact**: `Impact = λ × Size / ADV`
2. **Square Root Impact**: `Impact = λ × sqrt(Size / ADV)`
3. **Temporary Impact**: `TempImpact = γ × Size / ADV`
4. **Permanent Impact**: `PermImpact = δ × Sign(Size) × sqrt(Size / ADV)`

**Execution Quality Metrics**:
1. **Implementation Shortfall**: `IS = (DecisionPrice - ExecutionPrice) / DecisionPrice`
2. **Market Impact Cost**: `MIC = (VWAP - ArrivalPrice) / ArrivalPrice`
3. **Timing Cost**: `TC = (ArrivalPrice - DecisionPrice) / DecisionPrice`
4. **Total Cost**: `TotalCost = MIC + TC + Commission`

### Standardization

- **Z-Score**: `Z = (x - μ) / σ` using 252-day rolling window
- **Percentile Ranking**: Based on historical distribution
- **Min-Max Scaling**: For liquidity scores (0-100 scale)
- **Relative Normalization**: Stock-relative to market average

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

**Rule 1 (Market Liquidity Signal)**:
```
IF {MarketSpread > 0.3% AND MarketDepth < 5000万 AND Volume < 800亿}
THEN {Market liquidity stress, reduce position size}
CONFIDENCE: 80%
```

**Rule 2 (Stock Liquidity Signal)**:
```
IF {StockSpread > 0.5% AND AmihudILLIQ > 0.001 AND Volume < 1000万}
THEN {Stock illiquid, avoid large positions}
CONFIDENCE: 85%
```

**Rule 3 (Liquidity Deterioration Signal)**:
```
IF {Spread_t/Spread_{t-5} > 1.5 AND Volume_t/Volume_{t-5} < 0.7}
THEN {Liquidity deteriorating, exit position}
CONFIDENCE: 75%
```

**Rule 4 (Execution Cost Signal)**:
```
IF {ExpectedImpact > 0.2% AND Size > 1% ADV AND Volatility > 2%}
THEN {High execution cost, split order}
CONFIDENCE: 70%
```

**Rule 5 (Liquidity Crisis Signal)**:
```
IF {MarketSpread > 1.0% AND Volume < 500亿 AND VIX > 30}
THEN {Liquidity crisis, emergency exit}
CONFIDENCE: 90%
```

### Trigger conditions

- **Entry**: Any rule triggered with confidence ≥ 70%
- **Exit**: Liquidity conditions return to normal for 3 consecutive days
- **Invalidation**: Data quality issues or market structure changes

### Threshold rationale

- **Market Spread 0.3%**: Historically high spread indicating stress
- **Market Depth 5000万**: Minimum depth for normal market functioning
- **Volume 800亿**: Below-average daily volume threshold
- **Stock Spread 0.5%**: High spread for individual stocks
- **Amihud ILLIQ 0.001**: Illiquidity threshold for stocks

### Edge cases and fallbacks

**Data Quality Issues**:
- Missing quotes: Use last available quote with interpolation
- Stale data: Identify and exclude stale quotes
- Bad data: Filter out obvious data errors
- System errors: Fall back to cached data with error flag

**Market Conditions**:
- Market suspension: Use last available data with suspension flag
- Early close: Adjust for shortened trading session
- Circuit breakers: Record event and resume when market reopens
- Halts: Exclude halted stocks from calculations

**Extreme Events**:
- Market crashes: Adjust thresholds for extreme conditions
- Liquidity crises: Use crisis-mode parameters
- Regulatory changes: Update calculation methods
- Structural changes: Re-calibrate models

## Backtest Framework

### Backtest Design

**Objective**: Test whether liquidity signals predict trading costs and identify optimal execution strategies.

**Methodology**:
1. **Signal Generation**: Calculate liquidity risk signals
2. **Execution Simulation**: Simulate different execution strategies
3. **Cost Analysis**: Measure actual vs expected trading costs
4. **Performance Impact**: Assess impact on portfolio returns

### Test Specifications

**Universe**: HKEX main board constituents with adequate trading history
**Period**: 2018-2025 (7+ years including various liquidity regimes)
**Frequency**: Daily liquidity assessment, execution simulation
**Benchmark**: VWAP execution without liquidity optimization

### Performance Metrics

**Cost Analysis**:
- **Execution Costs**: Actual vs expected trading costs
- **Market Impact**: Price impact of large trades
- **Timing Costs**: Cost of delayed execution
- **Total Cost**: Comprehensive execution cost measure

**Signal Quality**:
- **Predictive Power**: Correlation between liquidity signals and costs
- **Cost Reduction**: Percentage cost reduction vs benchmark
- **Hit Rate**: Percentage of accurate liquidity predictions
- **False Positive Rate**: False liquidity warnings

**Risk Analysis**:
- **Liquidity Risk**: Exposure to liquidity shocks
- **Execution Risk**: Risk of failed or costly executions
- **Capacity Analysis**: Maximum AUM that can be efficiently traded
- **Stress Testing**: Performance during liquidity crises

### Statistical Validation

**Hypothesis Testing**:
- **H0**: Liquidity signals have no predictive power for trading costs
- **H1**: Liquidity-optimized execution reduces costs
- **Test**: Paired t-test on execution costs with/without optimization

**Regression Analysis**:
```
ExecutionCost = α + β×LiquidityScore + γ×TradeSize + δ×Volatility + ε
```

**Simulation Analysis**:
- **Monte Carlo**: Simulate various execution scenarios
- **Historical Replay**: Replay historical trades with different strategies
- **Stress Testing**: Test performance during liquidity crises
- **Sensitivity Analysis**: Test parameter sensitivity

### Falsification Criteria

Strategy fails if:
- **No Cost Reduction**: Optimized execution doesn't reduce costs
- **High Complexity**: Complexity doesn't justify benefits
- **Poor Scalability**: Strategy doesn't work for larger sizes
- **Data Mining**: Results don't hold out-of-sample

### Robustness Checks

**Alternative Specifications**:
- **Different Impact Models**: Linear, square-root, temporary/permanent
- **Varying Windows**: Test different liquidity measurement windows
- **Alternative Benchmarks**: TWAP, POV, implementation shortfall
- **Market Conditions**: Test in bull, bear, and sideways markets

**Transaction Cost Analysis**:
- **Realistic Costs**: Include commission, taxes, and market impact
- **Liquidity Constraints**: Position limits based on available liquidity
- **Execution Algorithms**: Test different algorithmic execution strategies
- **Market Impact**: Estimate actual market impact of following signals

### Expected Performance

**Academic Evidence**:
- **Cost Reduction**: 10-30% reduction in execution costs
- **Impact Prediction**: 60-70% accuracy for cost prediction
- **Liquidity Premium**: 2-4% annualized premium for illiquid stocks
- **Execution Quality**: Improved execution quality metrics

**Practical Expectations**:
- **Cost Savings**: 15-25% reduction in trading costs
- **Risk Reduction**: Lower execution risk and better fill rates
- **Capacity**: Strategy scalable up to several billion HKD
- **Timeliness**: Real-time liquidity assessment and adjustment

**Limitations**:
- **Data Requirements**: High-quality, high-frequency data needed
- **Model Risk**: Liquidity models may not capture all market dynamics
- **Market Impact**: Following signals may itself impact liquidity
- **Regulatory Risk**: Execution algorithms may face regulatory constraints

---

*港股流动性风险监控方法论 - 专业的流动性风险管理框架*
