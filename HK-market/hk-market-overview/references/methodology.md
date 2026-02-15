# Methodology: HK Market Overview (港股市场概览)

港股市场概览分析器提供港股市场整体表现、板块轮动、市场情绪和流动性的综合分析框架。

## Data Definitions

### Sources and field mapping

**Primary Data Sources**:
- Hong Kong Exchange (HKEX) real-time market data
- Hang Seng Indexes Company (HSI) index data
- Stock Connect southbound flow data
- Major broker research data

**Core Market Indices**:
- **HSI (恒生指数)**: Market capitalization-weighted index of top 80 companies
- **HSCEI (国企指数)**: H-share companies weighted by market cap
- **HSCCI (红筹指数)**: Red-chip companies listed in Hong Kong
- **HSTECH (科技指数)**: Technology sector companies

**Sector Classification**:
- **11 Major Sectors**: Financials, Properties, Utilities, Industrials, Consumer Goods, IT, Telecom, Materials, Energy, Healthcare, Conglomerates
- **Mapping**: Based on HKEX industry classification

### Frequency and windows

- **Real-time updates**: Every minute during trading hours (9:30-12:00, 13:00-16:00 HKT)
- **Intraday windows**: 5min, 15min, 30min, 60min
- **Daily windows**: 1d, 5d, 20d, 60d, 252d
- **Historical data**: 5+ years for trend analysis

## Core Metrics

### Metric list and formulas

**Market Performance Metrics**:
1. **Index Return**: `Return_t = (Price_t / Price_{t-1}) - 1`
2. **Market Cap**: `MarketCap = Σ(SharePrice_i × SharesOutstanding_i)`
3. **Total Volume**: `TotalVolume = Σ(Volume_i × Price_i)`
4. **Advancing/Declining Issues**: Count of stocks with positive/negative returns

**Sector Rotation Metrics**:
1. **Sector Return**: `SectorReturn_t = Σ(w_i × StockReturn_i)` for sector i
2. **Sector Relative Strength**: `RelativeStrength = SectorReturn / MarketReturn`
3. **Sector Flow**: `NetFlow = Inflow - Outflow` for each sector
4. **Rotation Score**: `RotationScore = Z(SectorReturn) + Z(RelativeStrength)`

**Market Sentiment Metrics**:
1. **Market Breadth**: `Breadth = (Advancing - Declining) / Total`
2. **Fear & Greed Index**: Composite of 7 indicators (volatility, momentum, breadth, etc.)
3. **Put/Call Ratio**: `PCR = PutVolume / CallVolume`
4. **New Highs/Lows**: Count of 52-week highs and lows

**Liquidity Metrics**:
1. **Southbound Flow**: `NetFlow = BuyVolume - SellVolume` from mainland investors
2. **Market Depth**: `Depth = Σ(BidSize_i) + Σ(AskSize_i)` at top 5 levels
3. **Turnover Rate**: `Turnover = DailyVolume / MarketCap`
4. **Liquidity Score**: Composite of volume, spread, and depth

### Standardization

- **Z-Score Normalization**: `Z = (x - μ) / σ` using 252-day rolling window
- **Percentile Ranking**: Based on historical distribution over 5 years
- **Min-Max Scaling**: For indicators with bounded ranges (0-100)

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

**Rule 1 (Market Trend Signal)**:
```
IF {HSI_20d_return > 5% AND MarketBreadth > 60% AND SouthboundFlow > 2亿}
THEN {Bullish market regime, increased risk appetite}
CONFIDENCE: 75%
```

**Rule 2 (Sector Rotation Signal)**:
```
IF {SectorRelativeStrength > 2.0 AND SectorFlow > 5亿 AND SectorReturn_5d > 3%}
THEN {Sector rotation opportunity, overweight sector}
CONFIDENCE: 70%
```

**Rule 3 (Market Extremes Signal)**:
```
IF {FearGreedIndex < 25 OR VIX > 30 OR NewHighs/NewLows < 0.2}
THEN {Market panic, contrarian opportunity}
CONFIDENCE: 80%
```

**Rule 4 (Liquidity Stress Signal)**:
```
IF {TotalVolume < 800亿 AND SouthboundFlow < -10亿 AND MarketDepth < 1000万}
THEN {Liquidity stress, reduce position size}
CONFIDENCE: 85%
```

**Rule 5 (Volatility Regime Signal)**:
```
IF {VIX_20d_avg > 25 AND IndexVolatility > 2% AND FearGreedIndex < 40}
THEN {High volatility regime, defensive positioning}
CONFIDENCE: 75%
```

### Trigger conditions

- **Entry**: Any rule triggered with confidence ≥ 70%
- **Exit**: Rule conditions reverse for 3 consecutive days
- **Invalidation**: Contradictory signals from multiple rules

### Threshold rationale

- **Market Return 5%**: Historically significant for trend identification
- **Market Breadth 60%**: Indicates broad-based participation
- **Southbound Flow 2亿**: Significant institutional participation level
- **Fear & Greed 25/75**: Historical extremes for contrarian signals
- **VIX 25**: Volatility regime change threshold

### Edge cases and fallbacks

**Data Quality Issues**:
- Missing index data: Use previous day's close with warning
- Delayed data: Mark as delayed and use last available
- Inconsistent data: Cross-validate with multiple sources

**Market Holidays**:
- No trading days: Use previous day's data with holiday flag
- Early close: Adjust for shortened trading session
- Half-day trading: Normalize volume for comparison

**Extreme Market Conditions**:
- Market suspension: Use last available data with suspension flag
- Circuit breakers: Record event and resume when market reopens
- System errors: Fall back to cached data with error notification

## Backtest Framework

### Backtest Design

**Objective**: Test whether market overview signals predict future market returns and sector performance.

**Methodology**:
1. **Signal Generation**: Calculate daily market overview signals
2. **Portfolio Construction**: Based on sector rotation and market trend signals
3. **Performance Measurement**: Track market and sector returns
4. **Risk Analysis**: Assess volatility and drawdown characteristics

### Test Specifications

**Universe**: HSI constituents and major sector ETFs
**Period**: 2018-2025 (7+ years including various market cycles)
**Frequency**: Daily signal generation, monthly portfolio rebalancing
**Benchmark**: HSI total return index

### Performance Metrics

**Return Analysis**:
- **Market Timing Accuracy**: Percentage of correct market direction predictions
- **Sector Rotation Success**: Hit rate of sector overweight/underweight calls
- **Risk-Adjusted Returns**: Sharpe ratio, Sortino ratio, information ratio
- **Maximum Drawdown**: Worst peak-to-trough decline

**Signal Quality**:
- **Signal Decay**: How long signals remain predictive
- **False Positive Rate**: Percentage of signals that don't materialize
- **Signal Strength**: Correlation between signal strength and subsequent returns
- **Regime Performance**: Performance across different market conditions

### Statistical Validation

**Hypothesis Testing**:
- **H0**: Market overview signals have no predictive power
- **H1**: Signals provide statistically significant predictive ability
- **Test**: t-test on signal-based strategy vs benchmark returns

**Regression Analysis**:
```
MarketReturn_t+1 = α + β×Signal_t + γ×MarketReturn_t + δ×Volatility_t + ε
```

### Falsification Criteria

Strategy fails if:
- **No Alpha**: Signal-based strategy doesn't outperform benchmark
- **High Volatility**: Excessive volatility without commensurate returns
- **Poor Timing**: Low hit rate on market direction predictions
- **Data Mining**: Results don't hold out-of-sample

### Robustness Checks

**Alternative Specifications**:
- **Different Windows**: Test 5d, 10d, 20d, 60d signal windows
- **Varying Thresholds**: Optimize signal thresholds for different risk levels
- **Alternative Weights**: Different sector classification and weighting schemes
- **Market Conditions**: Test performance in bull, bear, and sideways markets

**Transaction Cost Analysis**:
- **Trading Costs**: Include realistic commission and market impact
- **Liquidity Constraints**: Position limits based on trading volume
- **Implementation Lag**: Delay between signal generation and execution

### Expected Performance

**Academic Evidence**:
- **Market Timing**: 55-60% accuracy for trend identification
- **Sector Rotation**: 2-3% annual alpha from successful rotation
- **Risk Management**: 20-30% reduction in maximum drawdown
- **Signal Persistence**: Most signals effective for 1-4 weeks

**Practical Expectations**:
- **Hit Rate**: 60-70% for high-confidence signals
- **Alpha Generation**: 1-2% annualized after costs
- **Risk Reduction**: Improved risk-adjusted returns
- **Timeliness**: Early warning for major market regime changes

**Limitations**:
- **Market Efficiency**: Limited alpha in highly efficient markets
- **Signal Lag**: Real-time data delays affect performance
- **Regime Changes**: Structural market changes may invalidate historical patterns
- **Implementation Costs**: Trading costs erode returns, especially for frequent signals

---

*港股市场概览方法论 - 综合市场分析框架*
