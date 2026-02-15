# Methodology: Valuation Regime Detector (US)

Valuation is most useful at **multi-quarter to multi-year** horizons. The goal is to classify whether the market (or a sector) is cheap/neutral/expensive relative to its own history and derive falsifiable return expectations.

## Data Definitions

### Sources and field mapping

Any consistent valuation source works (forward P/E, CAPE, earnings yield, EV/EBITDA). For reproducibility:
- Index level: S&P 500 price series (or SPY)
- Fundamentals: trailing/forward earnings from a trusted provider (may be vendor-specific)
- Real rates/credit as conditioning variables (FRED): `DGS10`, TIPS yield proxy, `BAMLH0A0HYM2`

Normalize:
- Use **valuation percentiles** within a long history (>=10y when possible).

### Frequency and windows

- Update valuation regime monthly/weekly; do not overreact to daily noise.
- Horizon for expected returns: 1y / 3y / 5y.

## Core Metrics

### Metric list and formulas

Define at least one primary valuation metric and one conditioning metric:
- **Earnings yield**: `EY = E / P` (trailing or forward)
- **Valuation percentile**: `PctVal(t) = percentile_rank(metric[t-L:t])`, `L >= 10y`
- **Real rate** (conditioning): `real10y` level/change
- **Credit stress** (conditioning): HY OAS z-score

### Standardization

- Prefer **percentiles** (valuation distributions shift over decades).
- Use z-scores only within stable sub-periods.

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

Rule 1 (cheap regime → higher long-horizon returns):
IF {Market valuation percentile <= 20 AND HY_OAS_ZL(t) <= 1.0}
THEN {Over the next 3–5 years, broad equity total returns tend to be above long-run average (positive expected excess return vs cash).}
CONFIDENCE {0.65}
APPLICABLE_UNIVERSE {US broad equity index; diversified equity portfolios.}
FAILURE_MODE {Deep recession/default cycle where “cheap” gets cheaper; fundamentals collapse; valuation metric distorted by temporary earnings spikes/troughs.}

Rule 2 (expensive regime + rising real rates → lower forward returns):
IF {Market valuation percentile >= 80 AND Δ60(real10y) >= +50 bps}
THEN {Over the next 1–3 years, equity returns tend to be below average and drawdown risk is higher (negative relative to long-run expected returns).}
CONFIDENCE {0.64}
APPLICABLE_UNIVERSE {US broad equity index; long-duration growth segments.}
FAILURE_MODE {Productivity/growth surprise that expands earnings faster than discount rates; persistent “scarcity premium” for quality assets.}

Rule 3 (valuation alone is weak short-term timing):
IF {Market valuation percentile >= 80 AND HY_OAS_ZL(t) < 0.5 AND breadth is strong}
THEN {Over the next 1–3 months, return direction can remain positive; treat valuation as a medium/long-horizon risk indicator rather than a short-term short signal.}
CONFIDENCE {0.55}
APPLICABLE_UNIVERSE {US equities broad; tactical allocators.}
FAILURE_MODE {Sudden macro shock causes rapid multiple compression; breadth was late-cycle “narrow leadership”.}

### Trigger / exit / invalidation conditions

- **Cheap**: valuation percentile ≤20; **Expensive**: ≥80.
- **Exit**: regime changes when percentile crosses 35/65 bands for >=2 monthly observations.
- **Invalidation**: if valuation metric is distorted (e.g., one-off earnings collapse makes P/E meaningless); switch to price-to-sales or normalized earnings.

### Threshold rationale

- 20/80 bands balance signal frequency vs extremeness.
- Conditioning on credit/rates reduces false signals during macro transitions.

## Edge Cases and Degradation

### Missing data / outliers handling

- For cyclicals, normalize earnings (5–10y average) to avoid P/E spikes.
- Always report which valuation definition is used (TTM vs NTM vs CAPE).

### Fallback proxies

- If you cannot obtain reliable earnings: use market-level valuation proxies from public sources, or shift to **relative valuation** (sector vs market) with lower confidence.

## Technical Notes & Implementation Details

### Valuation Metric Selection

**Primary Valuation Metrics**:
- **CAPE (Cyclically Adjusted P/E)**: 10-year average earnings, smooths business cycles
- **Forward P/E**: Based on consensus estimates, more forward-looking but noisier
- **Earnings Yield (E/P)**: Inverse of P/E, linear relationship with expected returns
- **EV/EBITDA**: Adjusts for debt and capital structure, useful for highly leveraged sectors
- **Price-to-Book**: Stable book value, but less relevant for asset-light businesses
- **Dividend Yield**: Direct cash return, but ignores growth components

**Metric Selection Criteria**:
- **Historical Coverage**: At least 20+ years of data for reliable percentile calculations
- **Economic Rationale**: Clear link to discounted cash flow fundamentals
- **Stability**: Not overly volatile, but responsive to changing conditions
- **Coverage**: Available for target universe (index, sectors, individual stocks)

**Data Quality Considerations**:
- **Earnings Quality**: Adjust for one-time items, accounting changes, share buybacks
- **Index Composition**: Account for changing index constituents over time
- **Inflation Adjustment**: Use real terms for long-term comparisons
- **Survivorship Bias**: Include delisted/bankrupt companies in historical calculations

### Conditioning Variables Framework

**Real Rates Impact**:
```
Expected_Return = Base_Valuation_Effect + Real_Rate_Adjustment
Real_Rate_Adjustment = -λ × ΔReal_Rate
```
- **Higher real rates** → Lower equity valuations (higher discount rates)
- **Falling real rates** → Support higher valuations
- **Rate sensitivity** varies by sector (growth vs value)

**Credit Stress Integration**:
```
Credit_Adjustment = β × Credit_Stress_ZScore
```
- **High credit stress** → Risk-off, favors quality over yield
- **Low credit stress** → Risk-on, supports higher valuations
- **Credit spreads** often lead equity market turns

**Macro Context Matrix**:
| Valuation | Real Rates | Credit Stress | Expected Returns |
|-----------|------------|---------------|------------------|
| Cheap | Falling | Low | Above average |
| Cheap | Rising | High | Mixed/uncertain |
| Expensive | Falling | Low | Still positive |
| Expensive | Rising | High | Below average |

### Statistical Framework

**Percentile Calculation**:
```
Percentile = (Rank - 1) / (N - 1)
Where Rank = position in sorted historical series
```

**Z-Score Normalization**:
```
Z = (Current - Historical_Mean) / Historical_Std
Use only within stable sub-periods (e.g., post-1990)
```

**Regime Classification**:
- **Cheap**: Percentile ≤ 20
- **Below Average**: 20 < Percentile ≤ 40
- **Neutral**: 40 < Percentile ≤ 60
- **Above Average**: 60 < Percentile ≤ 80
- **Expensive**: Percentile > 80

**Signal Strength Scoring**:
```
Signal_Strength = Base_Valuation_Score + Conditioning_Adjustment
Base_Valuation_Score = (50 - Percentile) / 50  (range: -1 to +1)
Conditioning_Adjustment = Σ(Weight × Conditioning_Signal)
```

### Model Implementation Architecture

**Data Pipeline**:
1. **Data Collection**: Daily market data, monthly fundamentals
2. **Quality Control**: Outlier detection, missing data interpolation
3. **Metric Calculation**: Compute valuation metrics and conditioning variables
4. **Percentile Ranking**: Rolling historical percentiles
5. **Signal Generation**: Combine valuation and conditioning signals
6. **Output Generation**: Regime classification and return expectations

**Computational Efficiency**:
- **Rolling Windows**: Use efficient rolling window calculations
- **Vectorization**: Process multiple securities simultaneously
- **Caching**: Store intermediate calculations for reuse
- **Incremental Updates**: Update calculations incrementally vs full recalculation

**Storage Requirements**:
- **Historical Data**: 20+ years of daily price and monthly fundamental data
- **Intermediate Calculations**: Rolling percentiles, z-scores, conditioning variables
- **Signal History**: Track regime changes and signal performance over time

## Backtest Framework

### Backtest Design

**Objective**: Test whether valuation regimes predict future equity returns.

**Methodology**:
1. **Regime Classification**: Apply valuation regime classification to historical data
2. **Forward Return Calculation**: Calculate 1y/3y/5y forward total returns
3. **Performance Analysis**: Compare returns across different regimes
4. **Statistical Testing**: Test significance of return differences
5. **Robustness Checks**: Test across different time periods and market conditions

### Test Design Specifications

**Sample Period**: Minimum 20 years, preferably 50+ years for statistical power
**Frequency**: Monthly regime classification (avoid daily noise)
**Universe**: S&P 500, sector ETFs, international markets
**Returns**: Total returns (dividends reinvested)
**Adjustments**: Inflation-adjusted real returns for long-term analysis

### Performance Metrics

**Return Analysis**:
- **Mean Returns**: Average returns by regime
- **Median Returns**: Robust measure of central tendency
- **Return Distribution**: Full distribution analysis (percentiles, skewness)
- **Hit Rates**: Percentage of periods with positive returns
- **Volatility**: Return volatility by regime

**Risk Metrics**:
- **Maximum Drawdown**: Worst peak-to-trough decline by regime
- **Downside Frequency**: How often returns fall below threshold
- **Tail Risk**: 5th and 1st percentile return outcomes
- **Correlation Analysis**: How regime returns correlate with other assets

**Statistical Tests**:
- **t-Tests**: Test significance of mean return differences
- **Mann-Whitney U**: Non-parametric test of distribution differences
- **Chi-Square**: Test independence of regime and return direction
- **Regression Analysis**: Quantify relationship between valuation and returns

### Falsification Criteria

Model fails if:
- **No Return Predictability**: Cheap regimes don't outperform expensive regimes
- **Statistical Insignificance**: t-stat < 1.96 for return differences
- **Instability**: Relationship breaks down in sub-periods
- **Data Mining**: Results don't hold out-of-sample
- **Economic Inconsistency**: Results contradict economic theory

### Robustness Checks

**Alternative Specifications**:
- **Different Valuation Metrics**: Test CAPE, P/E, EV/EBITDA, dividend yield
- **Different Percentile Windows**: 10y, 20y, 30y historical periods
- **Different Conditioning Variables**: Real rates, credit spreads, inflation
- **Different Return Horizons**: 6 months, 1 year, 3 years, 5 years, 10 years

**Subperiod Analysis**:
- **Decade-by-Decade**: Test consistency across different decades
- **Market Regimes**: Test during recessions, expansions, crises
- **Inflation Environments**: High vs low inflation periods
- **Rate Regimes**: Rising vs falling interest rate environments

**International Tests**:
- **Developed Markets**: Europe, Japan, Australia
- **Emerging Markets**: Asia, Latin America, Eastern Europe
- **Sector Analysis**: Test across different industry sectors
- **Factor Analysis**: Interaction with value, momentum, quality factors

### Implementation Considerations

**Data Requirements**:
- **Price Data**: Daily total return indices for all test assets
- **Fundamental Data**: Monthly earnings, dividends, book values
- **Economic Data**: Interest rates, inflation, credit spreads
- **Corporate Actions**: Splits, mergers, delistings for accurate returns

**Computational Resources**:
- **Processing Power**: Efficient handling of large datasets
- **Storage**: Historical data storage and backup systems
- **Memory**: Sufficient RAM for rolling window calculations
- **Software**: Statistical packages for advanced analysis

**Quality Assurance**:
- **Data Validation**: Check for data errors and inconsistencies
- **Outlier Detection**: Identify and handle extreme values
- **Methodology Review**: Regular review of calculation methods
- **Performance Monitoring**: Track model accuracy over time

### Model Maintenance

**Monthly Updates**:
- Update valuation metrics and regime classifications
- Review recent performance vs expectations
- Monitor for structural changes in relationships
- Adjust conditioning variable weights as needed

**Quarterly Reviews**:
- Comprehensive backtest refresh with latest data
- Review regime classification accuracy
- Assess model performance across recent market conditions
- Update documentation and methodology notes

**Annual Overhauls**:
- Re-estimate historical relationships and parameters
- Review and update valuation metric selection
- Incorporate new research and academic findings
- Consider adding new conditioning variables or markets

### Expected Performance

**Academic Evidence**:
- **Return Spread**: 3-6% annualized return difference between cheap and expensive regimes
- **Hit Rate**: 65-75% accuracy in predicting return direction
- **Risk-Adjusted Performance**: 0.3-0.5 Sharpe ratio improvement
- **Drawdown Reduction**: 20-30% reduction in maximum drawdowns

**Realistic Expectations**:
- **Not Market Timing**: Valuation works over multi-year horizons, not months
- **Probabilistic Not Deterministic**: Cheap valuations improve odds, don't guarantee success
- **Regime Dependence**: Effectiveness varies across market environments
- **Implementation Lag**: Some delay in recognizing regime changes

**Limitations and Risks**:
- **Structural Changes**: Economic shifts may invalidate historical relationships
- **Data Quality**: Fundamental data errors and revisions
- **Model Risk**: Overfitting to historical patterns
- **Market Efficiency**: Markets may adapt and reduce predictability

## Backtest Notes (Minimal)

- Run valuation-regime backtests at monthly frequency to avoid look-ahead noise.
- Evaluate 1y/3y/5y forward total returns; report dispersion and drawdowns.
- Falsification: if “cheap” regimes do not deliver higher forward returns than “expensive” regimes over long samples net of inflation.
