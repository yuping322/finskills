# Methodology: HK Valuation Analyzer (港股估值分析器)

港股估值分析器提供市场整体估值、行业估值对比和个股估值深度分析的综合框架。

## Data Definitions

### Sources and field mapping

**Primary Data Sources**:
- **HKEX**: Official financial statements and market data
- **Bloomberg**: Real-time valuation multiples and consensus estimates
- **Reuters**: Historical valuation data and analyst coverage
- **Major Investment Banks**: Research reports and valuation models

**Core Valuation Metrics**:
- **PE (Price-Earnings)**: `PE = MarketCap / NetIncome`
- **PB (Price-Book)**: `PB = MarketCap / BookValue`
- **PS (Price-Sales)**: `PS = MarketCap / Revenue`
- **PCF (Price-CashFlow)**: `PCF = MarketCap / OperatingCashFlow`
- **EV/EBITDA**: `EV/EBITDA = (MarketCap + Debt - Cash) / EBITDA`

**Sector Classification**:
- **HKEX GICS Classification**: 11 major sectors for consistency
- **Mapping**: Aligned with HK market overview for cross-analysis
- **Weighting**: Market-cap weighted for sector-level calculations

### Frequency and windows

- **Real-time Updates**: Market price data during trading hours
- **Financial Data**: Quarterly updates (Q1, Q2, Q3, Q4)
- **Valuation Metrics**: Daily calculation based on latest data
- **Historical Analysis**: 10+ years for percentile calculations

## Core Metrics

### Metric list and formulas

**Market-Level Valuation**:
1. **Market PE**: `MarketPE = Σ(MarketCap_i) / Σ(NetIncome_i)`
2. **Market PB**: `MarketPB = Σ(MarketCap_i) / Σ(BookValue_i)`
3. **Market PS**: `MarketPS = Σ(MarketCap_i) / Σ(Revenue_i)`
4. **Market Dividend Yield**: `DivYield = Σ(Dividends_i) / Σ(MarketCap_i)`

**Sector-Level Valuation**:
1. **Sector PE**: `SectorPE = Σ(MarketCap_i) / Σ(NetIncome_i)` for sector i
2. **Sector PB**: `SectorPB = Σ(MarketCap_i) / Σ(BookValue_i)` for sector i
3. **Relative Valuation**: `RelativeVal = SectorVal / MarketVal`
4. **Valuation Spread**: `Spread = SectorVal - MarketVal`

**Stock-Level Valuation**:
1. **Historical PE**: `PE_t = Price_t / EPS_t`
2. **PE Percentile**: `PE_Pct = percentile(PE_t, historical_PE_distribution)`
3. **PE Deviation**: `PE_Dev = (PE_current - PE_median) / PE_median`
4. **Valuation Score**: `ValScore = w1×PE_Pct + w2×PB_Pct + w3×PS_Pct`

**DCF Valuation**:
1. **Free Cash Flow**: `FCF = OperatingCF - CapEx`
2. **Terminal Value**: `TV = FCF_n × (1+g) / (r-g)`
3. **Present Value**: `PV = Σ(FCF_t / (1+r)^t) + TV / (1+r)^n`
4. **DCF Price**: `Price_DCF = PV / SharesOutstanding`

**DDM Valuation**:
1. **Expected Dividend**: `ED = CurrentDividend × (1+g)`
2. **DDM Price**: `Price_DDM = ED / (r-g)`
3. **Growth Rate**: `g = ROE × RetentionRatio`
4. **Required Return**: `r = RiskFreeRate + Beta × EquityRiskPremium`

### Standardization

- **Percentile Ranking**: Based on 10-year historical distribution
- **Z-Score**: `Z = (x - μ) / σ` using 252-day rolling window
- **Min-Max Scaling**: For valuation scores (0-100 scale)
- **Relative Normalization**: Sector-relative to market average

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

**Rule 1 (Market Valuation Signal)**:
```
IF {MarketPE < 10 AND MarketPB < 1.0 AND DividendYield > 4%}
THEN {Market undervalued, overweight HK equities}
CONFIDENCE: 75%
```

**Rule 2 (Sector Valuation Signal)**:
```
IF {SectorPE < MarketPE × 0.7 AND SectorPB < MarketPB × 0.8 AND SectorFlow > 10亿}
THEN {Sector undervalued, overweight sector}
CONFIDENCE: 70%
```

**Rule 3 (Stock Valuation Signal)**:
```
IF {StockPE < SectorPE × 0.8 AND StockPB < SectorPB × 0.9 AND ROE > 15%}
THEN {Stock undervalued, buy signal}
CONFIDENCE: 65%
```

**Rule 4 (Valuation Reversal Signal)**:
```
IF {PE_Pct > 80 AND PE_Momentum < -0.2 AND InsiderSelling > 5%}
THEN {Overvaluation risk, sell signal}
CONFIDENCE: 80%
```

**Rule 5 (Value-Growth Signal)**:
```
IF {PE < 15 AND RevenueGrowth > 20% AND ROE > 18% AND DebtRatio < 0.5}
THEN {Value-growth opportunity, strong buy}
CONFIDENCE: 85%
```

### Trigger conditions

- **Entry**: Any rule triggered with confidence ≥ 65%
- **Exit**: Valuation metrics return to fair value range
- **Invalidation**: Fundamental deterioration or data quality issues

### Threshold rationale

- **Market PE 10**: Historically attractive valuation level
- **Market PB 1.0**: Book value support level
- **Dividend Yield 4%**: Attractive income threshold
- **Sector Discount 20-30%**: Significant undervaluation threshold
- **PE Percentile 80**: Overvaluation warning level

### Edge cases and fallbacks

**Data Quality Issues**:
- Negative earnings: Use normalized earnings or exclude from PE calculation
- Negative book value: Use tangible book value or exclude from PB calculation
- Missing data: Use industry averages or historical averages
- Extreme values: Winsorize at 1st/99th percentiles

**Market Conditions**:
- Financial crisis: Adjust valuation thresholds downward
- Market bubbles: Increase valuation thresholds
- Structural changes: Update historical distributions
- Regulatory changes: Adjust calculation methods

**Company-Specific Issues**:
- Restructuring: Use adjusted earnings or cash flow
- M&A activity: Use pro-forma financials
- Cyclical companies: Use normalized earnings over cycle
- Growth companies: Use forward-looking metrics

## Backtest Framework

### Backtest Design

**Objective**: Test whether valuation signals predict future returns and identify profitable investment strategies.

**Methodology**:
1. **Signal Generation**: Calculate valuation signals for market, sectors, and stocks
2. **Portfolio Construction**: Based on valuation rankings and signals
3. **Performance Measurement**: Track strategy returns vs benchmarks
4. **Risk Analysis**: Assess volatility and drawdown characteristics

### Test Specifications

**Universe**: HKEX main board constituents with adequate liquidity
**Period**: 2010-2025 (15+ years including various market cycles)
**Frequency**: Monthly portfolio rebalancing based on valuation signals
**Benchmark**: HSI total return index

### Performance Metrics

**Return Analysis**:
- **Value Premium**: Returns of low-valuation vs high-valuation stocks
- **Sector Rotation**: Returns from sector valuation timing
- **Market Timing**: Returns from market valuation signals
- **Risk-Adjusted Returns**: Sharpe ratio, Sortino ratio, information ratio

**Signal Quality**:
- **Predictive Power**: Correlation between valuation and future returns
- **Signal Decay**: How long valuation signals remain predictive
- **Hit Rate**: Percentage of correct valuation predictions
- **False Positive Rate**: Percentage of overvalued stocks that outperform

**Factor Analysis**:
- **Value Factor**: HML (High Minus Low) returns
- **Size Effect**: Small vs large cap valuation differences
- **Momentum Interaction**: Valuation combined with momentum
- **Quality Interaction**: Valuation combined with quality metrics

### Statistical Validation

**Hypothesis Testing**:
- **H0**: Valuation has no predictive power for returns
- **H1**: Low valuation stocks outperform high valuation stocks
- **Test**: Fama-MacBeth regression and portfolio analysis

**Regression Analysis**:
```
StockReturn_t+1 = α + β×Valuation_t + γ×Size_t + δ×Momentum_t + ε×Quality_t + θ
```

**Cross-Validation**:
- **Time Series**: Rolling window out-of-sample testing
- **Cross-Section**: Holdout sample of stocks
- **Parameter Stability**: Test consistency across different periods

### Falsification Criteria

Strategy fails if:
- **No Value Premium**: Low valuation stocks don't outperform
- **High Turnover**: Excessive trading erodes returns
- **Sector Bias**: Performance driven by specific sectors
- **Data Mining**: Results don't hold out-of-sample

### Robustness Checks

**Alternative Specifications**:
- **Different Valuation Metrics**: Test PE, PB, PS, PCF, EV/EBITDA
- **Varying Windows**: Test 1m, 3m, 6m, 12m formation periods
- **Different Rebalancing**: Monthly vs quarterly vs annual
- **Alternative Benchmarks**: Test against different market indices

**Transaction Cost Analysis**:
- **Trading Costs**: Include realistic commission and market impact
- **Liquidity Constraints**: Position limits based on trading volume
- **Implementation Lag**: Delay between signal generation and execution
- **Market Impact**: Price impact of large trades

### Expected Performance

**Academic Evidence**:
- **Value Premium**: 3-5% annualized outperformance for value stocks
- **Predictive Power**: 60-70% accuracy for valuation signals
- **Persistence**: Value signals effective for 6-12 months
- **Cross-Market**: Value premium consistent across markets

**Practical Expectations**:
- **Hit Rate**: 55-65% for valuation-based strategies
- **Alpha Generation**: 2-4% annualized after costs
- **Risk Reduction**: Lower volatility than growth strategies
- **Drawdown Protection**: Better downside protection in bear markets

**Limitations**:
- **Value Traps**: Low valuation may reflect fundamental problems
- **Cyclicality**: Value strategies may underperform in growth cycles
- **Data Quality**: Financial data quality affects valuation accuracy
- **Market Efficiency**: Reduced alpha as markets become more efficient

---

*港股估值分析方法论 - 专业的估值分析框架*
