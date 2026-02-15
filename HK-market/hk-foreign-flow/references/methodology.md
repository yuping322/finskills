# Methodology: HK Foreign Flow Analyzer (港股外资流向分析器)

港股外资流向分析器提供外资通过港股通、QFII、直接投资等方式的资金流向分析框架。

## Data Definitions

### Sources and field mapping

**Primary Data Sources**:
- **HKEX**: Stock Connect foreign investment data
- **CSRC**: QFII holdings and investment data
- **Major Brokers**: Foreign institutional flow reports
- **Data Vendors**: Historical foreign flow data and analytics

**Core Flow Data**:
- **Stock Connect Flow**: Northbound and southbound foreign investment
- **QFII Holdings**: Qualified Foreign Institutional Investor holdings
- **Direct Investment**: Foreign direct investment in HK stocks
- **Portfolio Investment**: Foreign portfolio investment flows

**Institutional Data**:
- **Institution Types**: Pension funds, sovereign funds, hedge funds, etc.
- **Geographic Distribution**: Foreign investment by region/country
- **Investment Styles**: Value, growth, momentum, etc.
- **Holding Period**: Average holding period by institution type

### Frequency and windows

- **Real-time Updates**: Stock Connect flow during trading hours
- **Daily Updates**: Daily foreign flow summaries
- **Monthly Updates**: QFII holdings and institutional data
- **Historical Data**: 10+ years for flow analysis

## Core Metrics

### Metric list and formulas

**Flow Metrics**:
1. **Net Foreign Flow**: `NetFlow = ForeignInflow - ForeignOutflow`
2. **Flow Intensity**: `FlowIntensity = |NetFlow| / AvgDailyFlow`
3. **Flow Persistence**: `FlowPersist = ConsecutiveDaysWithSameSign`
4. **Flow Momentum**: `FlowMom = (NetFlow_t - NetFlow_{t-20}) / NetFlow_{t-20}`

**Preference Metrics**:
1. **Sector Preference**: `SectorPref = SectorForeignFlow / TotalForeignFlow`
2. **Stock Preference**: `StockPref = StockForeignFlow / TotalForeignFlow`
3. **Style Preference**: `StylePref = StyleFlow / TotalForeignFlow`
4. **Geographic Preference**: `GeoPref = GeoFlow / TotalForeignFlow`

**Behavioral Metrics**:
1. **Holding Concentration**: `HHI = Σ(w_i²)` where w_i is weight in stock i
2. **Turnover Rate**: `Turnover = TradingVolume / TotalHoldings`
3. **Holding Period**: `AvgPeriod = 1 / TurnoverRate`
4. **Allocation Change**: `AllocChange = Weight_t - Weight_{t-1}`

**Risk Metrics**:
1. **Flow Volatility**: Standard deviation of foreign flows
2. **Concentration Risk**: `ConcRisk = HHI × FlowVolatility`
3. **Liquidity Risk**: `LiqRisk = FlowSize / AvgDailyVolume`
4. **Currency Risk**: `CurrencyRisk = ExchangeRateVolatility × ForeignExposure`

### Standardization

- **Z-Score**: `Z = (x - μ) / σ` using 252-day rolling window
- **Percentile Ranking**: Based on historical distribution over 5 years
- **Min-Max Scaling**: For preference scores (0-100 scale)
- **Relative Normalization**: Foreign flow relative to market average

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

**Rule 1 (Strong Foreign Flow Signal)**:
```
IF {NetFlow > 50亿 AND FlowIntensity > 2.0 AND FlowPersist >= 3}
THEN {Strong foreign interest, overweight foreign-preferred stocks}
CONFIDENCE: 75%
```

**Rule 2 (Foreign Preference Signal)**:
```
IF {SectorPref > 30% AND SectorFlow > 20亿 AND SectorReturn > 2%}
THEN {Foreign sector preference, overweight sector}
CONFIDENCE: 70%
```

**Rule 3 (Foreign Behavior Signal)**:
```
IF {HoldingConcentration > 0.25 AND Turnover < 0.1 AND HoldingPeriod > 180}
THEN {Long-term foreign holding, stable investment}
CONFIDENCE: 80%
```

**Rule 4 (Foreign Flow Reversal Signal)**:
```
IF {NetFlow_t < 0 AND NetFlow_{t-1} > 0 AND FlowMom < -0.5}
THEN {Foreign flow reversal, potential market correction}
CONFIDENCE: 65%
```

**Rule 5 (Foreign Geographic Signal)**:
```
IF {GeoPref_Change > 10% AND FlowIntensity > 1.5 AND GeoFlow > 15亿}
THEN {Geographic preference shift, follow new preference}
CONFIDENCE: 60%
```

### Trigger conditions

- **Entry**: Any rule triggered with confidence ≥ 60%
- **Exit**: Foreign flow conditions reverse for 2 consecutive days
- **Invalidation**: Contradictory flow patterns or data quality issues

### Threshold rationale

- **NetFlow 50亿**: Historically significant foreign flow threshold
- **FlowIntensity 2.0**: 2x average daily flow indicates strong interest
- **SectorPref 30%**: Significant sector preference threshold
- **HoldingConcentration 0.25**: High concentration threshold
- **GeoPref_Change 10%**: Significant geographic preference change

### Edge cases and fallbacks

**Data Quality Issues**:
- Missing data: Use previous day's flow with interpolation
- Reporting delays: Mark as estimated and update when available
- Inconsistent data: Cross-validate with multiple sources
- Currency effects: Adjust for exchange rate changes

**Market Conditions**:
- Market holidays: No foreign flow data, mark as holiday
- Market suspensions: Use last available data with suspension flag
- Regulatory changes: Adjust for new foreign investment rules
- Capital controls: Account for capital flow restrictions

**Structural Changes**:
- New investment channels: Include new foreign investment mechanisms
- Policy changes: Adjust for regulatory environment changes
- Market reforms: Account for market structure changes
- Global events: Account for global financial events

## Backtest Framework

### Backtest Design

**Objective**: Test whether foreign flow signals predict market returns and identify profitable foreign flow following strategies.

**Methodology**:
1. **Signal Generation**: Calculate daily foreign flow signals
2. **Portfolio Construction**: Based on foreign flow preferences
3. **Performance Measurement**: Track foreign flow strategy returns
4. **Risk Analysis**: Assess volatility and drawdown characteristics

### Test Specifications

**Universe**: HKEX main board constituents with foreign investment
**Period**: 2014-2025 (Stock Connect launch to present)
**Frequency**: Monthly portfolio rebalancing based on foreign flow signals
**Benchmark**: HSI total return index

### Performance Metrics

**Flow Analysis**:
- **Foreign Flow Predictability**: Correlation between foreign flows and future returns
- **Signal Quality**: Hit rate of foreign flow signals
- **Flow Persistence**: How long foreign flow signals remain predictive
- **Flow Impact**: Market impact of foreign flows

**Performance Analysis**:
- **Foreign Flow Alpha**: Excess returns from following foreign flows
- **Risk-Adjusted Returns**: Sharpe ratio, Sortino ratio, information ratio
- **Maximum Drawdown**: Worst peak-to-trough decline
- **Turnover Analysis**: Portfolio turnover and trading costs

**Behavioral Analysis**:
- **Institutional Performance**: Performance by institution type
- **Geographic Performance**: Performance by geographic region
- **Style Performance**: Performance by investment style
- **Holding Period Analysis**: Performance by holding period

### Statistical Validation

**Hypothesis Testing**:
- **H0**: Foreign flows have no predictive power for returns
- **H1**: Foreign flows provide statistically significant return predictability
- **Test**: Granger causality test and regression analysis

**Regression Analysis**:
```
StockReturn_t+1 = α + β×ForeignFlow_t + γ×MarketReturn_t + δ×Size_t + ε×Value_t + θ
```

**Event Study**:
- **Flow Events**: Identify large foreign flow days (>2σ)
- **Abnormal Returns**: Calculate returns around flow events
- **Persistence**: How long abnormal returns persist

### Falsification Criteria

Strategy fails if:
- **No Predictive Power**: Foreign flows don't predict returns
- **High Transaction Costs**: Trading costs exceed potential returns
- **Capacity Issues**: Strategy doesn't scale with capital
- **Data Mining**: Results don't hold out-of-sample

### Robustness Checks

**Alternative Specifications**:
- **Different Flow Measures**: Test various foreign flow indicators
- **Varying Thresholds**: Optimize signal thresholds for different risk levels
- **Alternative Time Windows**: Test different lookback periods
- **Different Institutions**: Test performance by institution type

**Transaction Cost Analysis**:
- **Trading Costs**: Include realistic commission and market impact
- **Liquidity Constraints**: Position limits based on trading volume
- **Implementation Lag**: Delay between signal generation and execution
- **Market Impact**: Price impact of following foreign flows

### Expected Performance

**Academic Evidence**:
- **Foreign Flow Predictability**: 55-65% accuracy for return prediction
- **Signal Persistence**: Foreign flow signals effective for 1-4 weeks
- **Institutional Advantage**: 2-3% annualized outperformance
- **Geographic Patterns**: Different regions have different performance

**Practical Expectations**:
- **Hit Rate**: 60-70% for high-confidence foreign flow signals
- **Alpha Generation**: 1-3% annualized after costs
- **Risk Reduction**: Improved risk-adjusted returns
- **Capacity**: Strategy scalable up to several billion HKD

**Limitations**:
- **Data Delay**: Foreign flow data may have reporting delays
- **Market Impact**: Following foreign flows may impact prices
- **Regulatory Risk**: Foreign investment policy may change
- **Currency Risk**: Exchange rate risk affects foreign returns

---

*港股外资流向分析方法论 - 专业的资金流向分析框架*
