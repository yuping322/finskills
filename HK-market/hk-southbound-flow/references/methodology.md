# Methodology: HK Southbound Flow Analysis (港股南向资金流向分析)

南向资金流向分析器专门分析内地投资者通过港股通投资港股的资金流向、持仓变化和投资偏好。

## Data Definitions

### Sources and field mapping

**Primary Data Sources**:
- **HKEX Stock Connect**: Official southbound trading data
- **Shanghai Stock Exchange**: Shanghai-Hong Kong Stock Connect statistics
- **Shenzhen Stock Exchange**: Shenzhen-Hong Kong Stock Connect statistics
- **Major Brokers**: Southbound flow research reports

**Core Data Fields**:
- **Daily Net Flow**: `NetFlow = BuyVolume - SellVolume` in HKD
- **Cumulative Flow**: Running total of net flows since Stock Connect inception
- **Holdings Value**: Market value of southbound holdings
- **Turnover Rate**: Daily trading volume / total holdings

**Sector Classification**:
- **HKEX GICS Classification**: 11 major sectors
- **Mapping**: Consistent with HK market overview for comparability
- **Aggregation**: Sum of individual stock flows within each sector

### Frequency and windows

- **Daily Updates**: End-of-day official data (T+1 availability)
- **Intraday**: Real-time flow estimates during trading hours
- **Weekly/Monthly**: Aggregated flow trends and patterns
- **Historical**: Full history since November 2014 (Stock Connect launch)

## Core Metrics

### Metric list and formulas

**Flow Metrics**:
1. **Daily Net Flow**: `NetFlow_t = SouthboundBuy_t - SouthboundSell_t`
2. **Flow Intensity**: `FlowIntensity = |NetFlow| / AverageDailyFlow_252d`
3. **Flow Persistence**: `Persistence = ConsecutiveDaysWithSameSign`
4. **Flow Momentum**: `FlowMomentum = (NetFlow_t - NetFlow_{t-20d}) / NetFlow_{t-20d}`

**Holdings Metrics**:
1. **Holdings Concentration**: `HHI = Σ(w_i²)` where w_i is weight in stock i
2. **Holding Change Rate**: `ChangeRate = (Holdings_t - Holdings_{t-1}) / Holdings_{t-1}`
3. **Turnover Rate**: `Turnover = TradingVolume_t / TotalHoldings_t`
4. **Average Holding Period**: `AvgPeriod = 1 / TurnoverRate`

**Preference Metrics**:
1. **Sector Preference**: `SectorPref = SectorWeight / MarketWeight`
2. **Size Preference**: `SizePref = HoldingsBySize / MarketBySize`
3. **Valuation Preference**: `ValuationPref = AvgPE_Holdings / AvgPE_Market`
4. **Growth Preference**: `GrowthPref = AvgGrowth_Holdings / AvgGrowth_Market`

**Correlation Metrics**:
1. **Flow-Return Correlation**: `Corr(Flow_t, Return_{t+1})`
2. **Flow-Market Correlation**: `Corr(Flow_t, MarketReturn_t)`
3. **AH Premium Correlation**: `Corr(Flow_t, AHPremium_t)`

### Standardization

- **Z-Score**: `Z = (x - μ) / σ` using 252-day rolling window
- **Percentile Ranking**: Based on historical distribution since 2014
- **Min-Max Scaling**: For preference indices (0-100 scale)
- **Moving Average**: 5d, 20d, 60d for trend identification

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

**Rule 1 (Strong Inflow Signal)**:
```
IF {NetFlow_5d > 50亿 AND FlowIntensity > 2.0 AND Persistence >= 3}
THEN {Strong southbound interest, overweight HK market}
CONFIDENCE: 75%
```

**Rule 2 (Sector Rotation Signal)**:
```
IF {SectorNetFlow > 20亿 AND SectorPref > 1.5 AND SectorReturn_5d > 3%}
THEN {Sector rotation opportunity, overweight sector}
CONFIDENCE: 70%
```

**Rule 3 (Concentration Risk Signal)**:
```
IF {HHI > 0.25 AND Top10Weight > 60% AND SingleStock > 8%}
THEN {High concentration risk, diversification warning}
CONFIDENCE: 80%
```

**Rule 4 (Flow Reversal Signal)**:
```
IF {NetFlow_t < 0 AND NetFlow_{t-1} > 0 AND FlowMomentum < -0.5}
THEN {Flow reversal, potential market correction}
CONFIDENCE: 65%
```

**Rule 5 (AH Premium Signal)**:
```
IF {AHPremium > 30% AND SouthboundFlow_AH > 10亿 AND AHStockReturn > 2%}
THEN {AH arbitrage opportunity, overweight AH shares}
CONFIDENCE: 60%
```

### Trigger conditions

- **Entry**: Any rule triggered with confidence ≥ 65%
- **Exit**: Rule conditions reverse for 2 consecutive days
- **Invalidation**: Contradictory flow patterns or data quality issues

### Threshold rationale

- **Net Flow 50亿**: Historically significant for market impact
- **Flow Intensity 2.0**: 2x average daily flow indicates strong interest
- **HHI 0.25**: High concentration threshold for risk management
- **AH Premium 30%**: Significant arbitrage opportunity threshold
- **Persistence 3 days**: Minimum for trend confirmation

### Edge cases and fallbacks

**Data Quality Issues**:
- Missing data: Use previous day's value with interpolation
- Reporting delays: Mark as estimated and update when available
- Inconsistent data: Cross-validate with multiple sources

**Market Holidays**:
- HK holidays: No flow data, mark as holiday
- Mainland holidays: Southbound trading suspended
- Partial holidays: Adjust for reduced trading hours

**Regulatory Changes**:
- Quota changes: Adjust for new quota limits
- Eligibility changes: Update stock universe
- Trading rule changes: Modify calculation methods accordingly

## Backtest Framework

### Backtest Design

**Objective**: Test whether southbound flow signals predict future market returns and identify profitable investment strategies.

**Methodology**:
1. **Signal Generation**: Calculate daily southbound flow signals
2. **Portfolio Construction**: Based on flow signals and preferences
3. **Performance Measurement**: Track strategy returns vs benchmarks
4. **Risk Analysis**: Assess volatility and drawdown characteristics

### Test Specifications

**Universe**: HKEX main board constituents eligible for Stock Connect
**Period**: 2014-2025 (full Stock Connect history)
**Frequency**: Daily signal generation, weekly portfolio rebalancing
**Benchmark**: HSI total return index

### Performance Metrics

**Return Analysis**:
- **Flow Strategy Returns**: Returns based on following flow signals
- **Sector Rotation Returns**: Returns from sector-based flow strategies
- **Alpha Generation**: Excess returns over market benchmark
- **Risk-Adjusted Returns**: Sharpe ratio, Sortino ratio, information ratio

**Signal Quality**:
- **Predictive Power**: Correlation between flow and future returns
- **Signal Decay**: How long flow signals remain predictive
- **Hit Rate**: Percentage of correct directional predictions
- **False Positive Rate**: Percentage of signals that don't materialize

**Liquidity Impact**:
- **Market Impact**: Price impact of large flow movements
- **Execution Costs**: Trading costs and slippage
- **Capacity Constraints**: Maximum AUM that can follow signals
- **Timing Analysis**: Optimal execution timing for flow signals

### Statistical Validation

**Hypothesis Testing**:
- **H0**: Southbound flows have no predictive power
- **H1**: Flows provide statistically significant return predictability
- **Test**: Granger causality test and regression analysis

**Regression Analysis**:
```
StockReturn_t+1 = α + β×SouthboundFlow_t + γ×MarketReturn_t + δ×Size_t + ε×Value_t + θ
```

**Event Study**:
- **Flow Events**: Identify large flow days (>2σ)
- **Abnormal Returns**: Calculate returns around flow events
- **Persistence**: How long abnormal returns persist

### Falsification Criteria

Strategy fails if:
- **No Predictive Power**: Flow signals don't predict returns
- **High Transaction Costs**: Trading costs exceed potential returns
- **Capacity Issues**: Strategy doesn't scale with capital
- **Data Mining**: Results don't hold out-of-sample

### Robustness Checks

**Alternative Specifications**:
- **Different Flow Windows**: Test 1d, 5d, 20d, 60d flow aggregation
- **Varying Thresholds**: Optimize signal thresholds for different risk levels
- **Alternative Benchmarks**: Test against different market indices
- **Subperiod Analysis**: Test performance in different market regimes

**Liquidity Analysis**:
- **Market Impact Model**: Estimate price impact of following flows
- **Execution Strategy**: Optimal execution for large positions
- **Capacity Constraints**: Maximum capital that can be deployed
- **Slippage Analysis**: Realistic trading cost assumptions

### Expected Performance

**Academic Evidence**:
- **Flow Predictability**: 55-65% accuracy for return prediction
- **Sector Rotation**: 2-4% annual alpha from sector flow following
- **Concentration Risk**: High concentration leads to underperformance
- **AH Premium**: Flow-AH premium relationship significant at 5% level

**Practical Expectations**:
- **Hit Rate**: 60-70% for high-confidence flow signals
- **Alpha Generation**: 1-3% annualized after costs
- **Risk Reduction**: Improved risk-adjusted returns
- **Capacity**: Strategy scalable up to several billion HKD

**Limitations**:
- **Data Delay**: T+1 data availability affects timeliness
- **Market Impact**: Large flows may move prices against strategy
- **Regulatory Risk**: Policy changes may affect Stock Connect
- **Currency Risk**: HKD exposure needs currency hedging

---

*港股南向资金流向分析方法论 - 专业的资金流向分析框架*
