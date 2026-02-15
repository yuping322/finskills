# Methodology: HK Sector Rotation Detector (港股板块轮动检测器)

港股板块轮动检测器提供行业轮动识别、资金流向分析和配置建议的综合框架。

## Data Definitions

### Sources and field mapping

**Primary Data Sources**:
- **HKEX**: Sector classification and trading data
- **Hang Seng Indexes**: Sector indices and constituents
- **Data Vendors**: Historical sector performance and flow data
- **Broker Research**: Sector rotation research and reports

**Core Sector Data**:
- **Sector Classification**: 11 major sectors based on GICS
- **Sector Indices**: HSI sector indices and custom sector baskets
- **Sector Returns**: Total return for each sector
- **Sector Market Cap**: Market capitalization by sector

**Flow Data**:
- **Sector Flow**: Net fund flow by sector
- **Institutional Flow**: Institutional buying/selling by sector
- **Southbound Flow**: Mainland capital flow by sector
- **ETF Flow**: ETF fund flow by sector

### Frequency and windows

- **Real-time Updates**: Every minute during trading hours
- **Intraday Windows**: 5min, 15min, 30min, 60min
- **Daily Windows**: 1d, 5d, 20d, 60d, 252d
- **Historical Data**: 10+ years for rotation analysis

## Core Metrics

### Metric list and formulas

**Relative Strength Metrics**:
1. **Sector Relative Strength**: `SRS = SectorReturn / MarketReturn`
2. **SRS Ranking**: Rank of sectors by relative strength
3. **SRS Momentum**: `SRSMom = (SRS_t - SRS_{t-20}) / SRS_{t-20}`
4. **SRS Trend**: Moving average of SRS over N days

**Flow Metrics**:
1. **Sector Net Flow**: `NetFlow = Inflow - Outflow`
2. **Flow Intensity**: `FlowIntensity = |NetFlow| / AvgDailyFlow`
3. **Flow Persistence**: `FlowPersist = ConsecutiveDaysWithSameSign`
4. **Flow Momentum**: `FlowMom = (NetFlow_t - NetFlow_{t-20}) / NetFlow_{t-20}`

**Rotation Signal Metrics**:
1. **Rotation Strength**: Composite score of relative strength and flow
2. **Rotation Persistence**: Expected duration of current rotation
3. **Rotation Certainty**: Confidence level of rotation signal
4. **Rotation Cycle**: Current position in rotation cycle

**Performance Metrics**:
1. **Sector Alpha**: `Alpha = SectorReturn - MarketReturn`
2. **Information Ratio**: `IR = Alpha / TrackingError`
3. **Sector Beta**: `Beta = Cov(Sector, Market) / Var(Market)`
4. **Sector Volatility**: Standard deviation of sector returns

### Standardization

- **Z-Score**: `Z = (x - μ) / σ` using 252-day rolling window
- **Percentile Ranking**: Based on historical distribution over 5 years
- **Min-Max Scaling**: For rotation scores (0-100 scale)
- **Relative Normalization**: Sector metrics relative to market average

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

**Rule 1 (Strong Rotation Signal)**:
```
IF {SRS > 1.2 AND FlowIntensity > 2.0 AND SRSMom > 15%}
THEN {Strong sector rotation, overweight sector}
CONFIDENCE: 75%
```

**Rule 2 (Rotation Confirmation Signal)**:
```
IF {SRS > 1.1 AND FlowPersist >= 3 AND SectorAlpha > 2%}
THEN {Rotation confirmed, increase sector exposure}
CONFIDENCE: 70%
```

**Rule 3 (Rotation Reversal Signal)**:
```
IF {SRS < 0.8 AND FlowIntensity < -1.5 AND SRSMom < -10%}
THEN {Rotation reversal, underweight sector}
CONFIDENCE: 80%
```

**Rule 4 (Early Rotation Signal)**:
```
IF {FlowIntensity > 1.5 AND SRSMom > 10% AND SRSRanking <= 3}
THEN {Early rotation signal, prepare for sector overweight}
CONFIDENCE: 65%
```

**Rule 5 (Rotation Divergence Signal)**:
```
IF {SRS > 1.1 AND FlowIntensity < -1.0 AND DivergenceStrength > 2σ}
THEN {Price-flow divergence, rotation risk}
CONFIDENCE: 70%
```

### Trigger conditions

- **Entry**: Any rule triggered with confidence ≥ 65%
- **Exit**: Rotation conditions reverse for 2 consecutive days
- **Invalidation**: Contradictory rotation signals or data quality issues

### Threshold rationale

- **SRS 1.2/0.8**: Strong outperformance/underperformance thresholds
- **FlowIntensity 2.0/-1.5**: Strong flow intensity thresholds
- **SRSMom ±15%/±10%**: Significant momentum change thresholds
- **FlowPersist 3**: Minimum persistence for trend confirmation
- **SRSRanking 3**: Top 3 sectors for early signals

### Edge cases and fallbacks

**Data Quality Issues**:
- Missing data: Use previous day's data with interpolation
- Partial data: Use available stocks and mark as partial
- Inconsistent data: Cross-validate with multiple sources
- Sector reclassification: Adjust for sector classification changes

**Market Conditions**:
- Market holidays: Use last available rotation data with holiday flag
- Market crashes: Adjust thresholds for extreme conditions
- Sector events: Account for sector-specific events
- Regulatory changes: Adjust for regulatory impacts

**Structural Changes**:
- New sectors: Include after sufficient trading history
- Sector mergers: Adjust for sector consolidation
- Index changes: Account for index composition changes
- Market reforms: Adjust for market structure changes

## Backtest Framework

### Backtest Design

**Objective**: Test whether sector rotation signals predict sector returns and identify optimal sector allocation strategies.

**Methodology**:
1. **Signal Generation**: Calculate daily sector rotation signals
2. **Sector Allocation**: Allocate capital based on rotation signals
3. **Performance Measurement**: Track sector rotation strategy returns
4. **Risk Analysis**: Assess volatility and drawdown characteristics

### Test Specifications

**Universe**: 11 major HK market sectors
**Period**: 2010-2025 (15+ years including various market cycles)
**Frequency**: Monthly portfolio rebalancing based on rotation signals
**Benchmark**: Equal-weight sector portfolio

### Performance Metrics

**Rotation Analysis**:
- **Sector Timing Accuracy**: Percentage of correct sector rotation predictions
- **Signal Quality**: Correlation between rotation signals and sector returns
- **Hit Rate**: Percentage of profitable sector rotations
- **False Positive Rate**: Percentage of false rotation signals

**Risk-Adjusted Returns**:
- **Sector Alpha**: Excess returns over market
- **Information Ratio**: Risk-adjusted sector alpha
- **Maximum Drawdown**: Worst peak-to-trough decline
- **Sector Beta**: Sector sensitivity to market movements

**Portfolio Performance**:
- **Portfolio Returns**: Total returns of rotation strategy
- **Sector Contribution**: Contribution of each sector to portfolio returns
- **Turnover**: Portfolio turnover and trading costs
- **Concentration**: Sector concentration and diversification

### Statistical Validation

**Hypothesis Testing**:
- **H0**: Sector rotation signals have no predictive power for sector returns
- **H1**: Sector rotation signals provide statistically significant sector timing ability
- **Test**: Fama-MacBeth regression on sector returns

**Regression Analysis**:
```
SectorReturn_t+1 = α + β×RotationSignal_t + γ×MarketReturn_t + δ×SectorMomentum_t + ε
```

**Event Study**:
- **Rotation Events**: Identify strong rotation days (>2σ)
- **Abnormal Returns**: Calculate sector returns around rotation events
- **Persistence**: How long rotation effects persist

### Falsification Criteria

Strategy fails if:
- **No Rotation Alpha**: Sector rotation strategy doesn't outperform equal-weight
- **High Turnover**: Excessive trading erodes returns
- **Sector Bias**: Performance driven by specific sectors
- **Data Mining**: Results don't hold out-of-sample

### Robustness Checks

**Alternative Specifications**:
- **Different Rotation Measures**: Test various rotation indicators
- **Varying Thresholds**: Optimize signal thresholds for different risk levels
- **Alternative Rebalancing**: Test different rebalancing frequencies
- **Different Sectors**: Test with different sector classifications

**Transaction Cost Analysis**:
- **Trading Costs**: Include realistic commission and market impact
- **Sector Liquidity**: Account for different sector liquidity
- **Implementation Lag**: Delay between signal generation and execution
- **Market Impact**: Price impact of sector rotation trades

### Expected Performance

**Academic Evidence**:
- **Sector Rotation**: 2-4% annualized outperformance from sector rotation
- **Signal Persistence**: Rotation signals effective for 1-3 months
- **Risk Reduction**: 15-25% reduction in portfolio volatility
- **Flow Predictability**: 60-70% accuracy for flow-based signals

**Practical Expectations**:
- **Hit Rate**: 55-65% for high-confidence rotation signals
- **Alpha Generation**: 1-3% annualized after costs
- **Risk Reduction**: Improved risk-adjusted returns
- **Sector Timing**: Better sector timing than market timing

**Limitations**:
- **Sector Correlation**: High correlation between sectors reduces benefits
- **Transaction Costs**: High turnover may erode returns
- **Implementation Risk**: Sector rotation may be difficult to implement
- **Market Efficiency**: Reduced alpha as markets become more efficient

---

*港股板块轮动检测方法论 - 专业的行业轮动分析框架*
