# Methodology: HK Market Breadth Monitor (港股市场广度监控器)

港股市场广度监控器提供市场宽度、参与度和趋势强度的综合评估框架。

## Data Definitions

### Sources and field mapping

**Primary Data Sources**:
- **HKEX**: Real-time trading data for all listed stocks
- **Data Vendors**: Historical breadth data and indicators
- **Market Indices**: HSI, HSCEI, HSCCI, HSTECH data
- **Broker Research**: Breadth analysis and market sentiment

**Core Breadth Metrics**:
- **Advancing Stocks**: Number of stocks with positive returns
- **Declining Stocks**: Number of stocks with negative returns
- **Unchanged Stocks**: Number of stocks with zero returns
- **Total Traded Stocks**: Total number of stocks with trading activity

**Volume Breadth Data**:
- **Up Volume**: Total volume of advancing stocks
- **Down Volume**: Total volume of declining stocks
- **Total Volume**: Total market trading volume
- **Volume Breadth**: `Up Volume / Total Volume`

### Frequency and windows

- **Real-time Updates**: Every minute during trading hours
- **Intraday Windows**: 5min, 15min, 30min, 60min
- **Daily Windows**: 1d, 5d, 20d, 60d, 252d
- **Historical Data**: 10+ years for breadth analysis

## Core Metrics

### Metric list and formulas

**Basic Breadth Indicators**:
1. **Advance-Decline Ratio**: `ADR = Advancing / Declining`
2. **Market Breadth**: `Breadth = (Advancing - Declining) / Total`
3. **Breadth Percentage**: `BreadthPct = Advancing / Total`
4. **Volume Breadth**: `VolBreadth = UpVolume / TotalVolume`

**Momentum Indicators**:
1. **Breadth Momentum**: `BreadthMom = (Breadth_t - Breadth_{t-5}) / Breadth_{t-5}`
2. **Breadth Acceleration**: `BreadthAcc = (BreadthMom_t - BreadthMom_{t-5}) / BreadthMom_{t-5}`
3. **Breadth Trend**: Moving average of breadth over N days
4. **Breadth Divergence**: Price vs breadth divergence

**Participation Indicators**:
1. **Participation Rate**: `Participation = ActiveStocks / TotalStocks`
2. **Volume Concentration**: `VolConc = Top10Volume / TotalVolume`
3. **Liquidity Participation**: `LiqPart = LiquidStocks / TotalStocks`
4. **Average Turnover**: `AvgTurnover = TotalVolume / TotalMarketCap`

**Extreme Indicators**:
1. **Extreme Reading**: Historical percentile of breadth indicators
2. **Fatigue Indicator**: Consecutive days of same breadth direction
3. **Divergence Strength**: Magnitude of price-breadth divergence
4. **Reversal Probability**: Historical reversal probability at current levels

### Standardization

- **Z-Score**: `Z = (x - μ) / σ` using 252-day rolling window
- **Percentile Ranking**: Based on historical distribution over 10 years
- **Min-Max Scaling**: For breadth scores (0-100 scale)
- **Relative Normalization**: Breadth relative to market conditions

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

**Rule 1 (Bullish Breadth Signal)**:
```
IF {BreadthPct > 60% AND VolBreadth > 65% AND BreadthMom > 10%}
THEN {Broad-based rally, bullish confirmation}
CONFIDENCE: 75%
```

**Rule 2 (Bearish Breadth Signal)**:
```
IF {BreadthPct < 40% AND VolBreadth < 35% AND BreadthMom < -10%}
THEN {Broad-based decline, bearish confirmation}
CONFIDENCE: 80%
```

**Rule 3 (Breadth Divergence Signal)**:
```
IF {IndexReturn > 2% AND BreadthPct < 45% AND DivergenceStrength > 2σ}
THEN {Narrow rally, bearish divergence}
CONFIDENCE: 70%
```

**Rule 4 (Participation Signal)**:
```
IF {Participation > 70% AND AvgTurnover > 1.0% AND VolConc < 50%}
THEN {High participation, sustainable trend}
CONFIDENCE: 65%
```

**Rule 5 (Extreme Reading Signal)**:
```
IF {BreadthPct > 80% OR BreadthPct < 20% AND FatigueDays > 5}
THEN {Extreme reading, reversal likely}
CONFIDENCE: 85%
```

### Trigger conditions

- **Entry**: Any rule triggered with confidence ≥ 65%
- **Exit**: Breadth conditions normalize for 2 consecutive days
- **Invalidation**: Contradictory breadth signals or data quality issues

### Threshold rationale

- **BreadthPct 60%/40%**: Historical thresholds for healthy/unhealthy markets
- **VolBreadth 65%/35%**: Volume confirmation thresholds
- **BreadthMom ±10%**: Significant momentum change thresholds
- **Participation 70%**: High participation threshold
- **Extreme 80%/20%**: Extreme market condition thresholds

### Edge cases and fallbacks

**Data Quality Issues**:
- Missing data: Use previous day's breadth with interpolation
- Partial data: Use available stocks and mark as partial
- Inconsistent data: Cross-validate with multiple sources
- Stale data: Identify and exclude stale quotes

**Market Conditions**:
- Market holidays: Use last available breadth with holiday flag
- Early close: Adjust for shortened trading session
- Suspended stocks: Exclude from breadth calculations
- New listings: Include after sufficient trading history

**Extreme Events**:
- Market crashes: Adjust thresholds for extreme conditions
- Circuit breakers: Record event and resume when market reopens
- System errors: Use cached data with error notification
- Data gaps: Use statistical imputation methods

## Backtest Framework

### Backtest Design

**Objective**: Test whether breadth signals predict market returns and identify optimal market timing strategies.

**Methodology**:
1. **Signal Generation**: Calculate daily breadth signals
2. **Market Timing**: Generate buy/sell signals based on breadth
3. **Performance Measurement**: Track strategy returns vs buy-and-hold
4. **Risk Analysis**: Assess volatility and drawdown characteristics

### Test Specifications

**Universe**: HKEX main board constituents with adequate liquidity
**Period**: 2010-2025 (15+ years including various market cycles)
**Frequency**: Daily signal generation, market timing strategy
**Benchmark**: HSI total return index

### Performance Metrics

**Timing Analysis**:
- **Market Timing Accuracy**: Percentage of correct market direction predictions
- **Signal Quality**: Correlation between breadth signals and future returns
- **Hit Rate**: Percentage of profitable signals
- **False Positive Rate**: Percentage of false signals

**Risk-Adjusted Returns**:
- **Sharpe Ratio**: Risk-adjusted return of breadth strategy
- **Sortino Ratio**: Downside risk-adjusted return
- **Maximum Drawdown**: Worst peak-to-trough decline
- **Calmar Ratio**: Return to maximum drawdown ratio

**Signal Effectiveness**:
- **Signal Decay**: How long breadth signals remain predictive
- **Regime Performance**: Performance in different market conditions
- **Sector Impact**: Breadth signals across different sectors
- **Volatility Impact**: Performance in different volatility regimes

### Statistical Validation

**Hypothesis Testing**:
- **H0**: Breadth signals have no predictive power for market returns
- **H1**: Breadth signals provide statistically significant market timing ability
- **Test**: T-test on breadth strategy vs benchmark returns

**Regression Analysis**:
```
MarketReturn_t+1 = α + β×BreadthSignal_t + γ×MarketReturn_t + δ×Volatility_t + ε
```

**Event Study**:
- **Breadth Events**: Identify extreme breadth days (>2σ)
- **Abnormal Returns**: Calculate market returns around breadth events
- **Persistence**: How long abnormal returns persist

### Falsification Criteria

Strategy fails if:
- **No Timing Ability**: Breadth strategy doesn't outperform buy-and-hold
- **High Whipsaw**: Excessive false signals generate losses
- **Poor Risk-Adjusted Returns**: Sharpe ratio below benchmark
- **Data Mining**: Results don't hold out-of-sample

### Robustness Checks

**Alternative Specifications**:
- **Different Breadth Measures**: Test various breadth indicators
- **Varying Thresholds**: Optimize signal thresholds for different risk levels
- **Alternative Time Windows**: Test different lookback periods
- **Different Markets**: Test breadth signals in other markets

**Transaction Cost Analysis**:
- **Trading Costs**: Include realistic commission and market impact
- **Execution Lag**: Delay between signal generation and execution
- **Market Impact**: Price impact of following breadth signals
- **Liquidity Constraints**: Position limits based on market liquidity

### Expected Performance

**Academic Evidence**:
- **Market Timing**: 55-65% accuracy for breadth-based timing
- **Signal Persistence**: Breadth signals effective for 1-4 weeks
- **Risk Reduction**: 20-30% reduction in maximum drawdown
- **Divergence Signals**: 70-80% accuracy for divergence predictions

**Practical Expectations**:
- **Hit Rate**: 60-70% for high-confidence breadth signals
- **Alpha Generation**: 1-3% annualized after costs
- **Risk Reduction**: Improved risk-adjusted returns
- **Regime Adaptation**: Better performance in different market regimes

**Limitations**:
- **Market Efficiency**: Reduced alpha in highly efficient markets
- **Signal Lag**: Breadth data may lag price movements
- **False Signals**: Whipsaw in choppy markets
- **Implementation Risk**: Trading costs may erode returns

---

*港股市场广度监控方法论 - 专业的市场广度分析框架*
