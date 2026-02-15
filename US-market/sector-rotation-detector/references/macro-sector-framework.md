# Macro-Sector Framework

Business cycle phase identification, sector rotation map, and macro indicator analysis for sector allocation decisions.

## Table of Contents

1. [Business Cycle Phase Identification](#business-cycle-phase-identification)
2. [Sector Rotation Map](#sector-rotation-map)
3. [Macro Indicator Deep-Dive](#macro-indicator-deep-dive)
4. [Cross-Asset Confirmation Signals](#cross-asset-confirmation-signals)
5. [Historical Sector Performance by Phase](#historical-sector-performance-by-phase)
6. [Structural Shifts to Consider](#structural-shifts-to-consider)

## Business Cycle Phase Identification

### Indicator Matrix

Score each indicator to determine current phase:

| Indicator | Early Expansion | Mid Expansion | Late Expansion | Contraction |
|-----------|----------------|---------------|----------------|-------------|
| GDP growth | Accelerating from trough | Steady, above trend | Decelerating | Negative or near-zero |
| ISM PMI | Rising above 50 | Sustained >55 | Peaking, beginning to fall | Below 50 |
| Unemployment | Falling rapidly | Approaching NAIRU | At or below NAIRU | Rising |
| Inflation (core CPI) | Low, <2% | Rising toward 2–3% | Elevated, >3% | Falling |
| Fed funds rate | Low / being cut | Rising gradually | Restrictive | Being cut aggressively |
| Yield curve | Steepening | Flat to slightly flat | Flat to inverting | Steepening (from inversion) |
| Credit spreads | Tightening | Tight | Beginning to widen | Wide |
| Corporate earnings | Trough, beginning recovery | Strong growth | Peaking | Declining |
| Consumer confidence | Rising | High | Peaking, cracks forming | Low |
| Housing starts | Recovering | Strong | Slowing | Weak |

### Phase Scoring

For each indicator, assign +1 to the most matching phase. The phase with the highest total score is the current phase. If two phases tie, the economy is in **transition** — note both and flag increased uncertainty.

### Mixed Signals Protocol

When indicators conflict (e.g., strong employment + weak manufacturing):

1. Weight leading indicators (yield curve, PMI, LEI) more heavily than lagging (unemployment, CPI)
2. Note the conflict explicitly — it often indicates a phase transition
3. Consider sector-level impacts of each signal separately
4. Reduce conviction on all sector calls (narrower over/underweights)

## Sector Rotation Map

### Classic Sector Rotation by Phase

| Phase | Overweight | Neutral | Underweight |
|-------|-----------|---------|-------------|
| **Early Expansion** | Technology, Consumer Discretionary, Industrials, Financials, Real Estate | Materials, Communication Services | Utilities, Consumer Staples, Healthcare, Energy |
| **Mid Expansion** | Technology, Industrials, Materials, Energy | Financials, Consumer Discretionary, Communication Services | Utilities, Consumer Staples, Real Estate |
| **Late Expansion** | Energy, Materials, Healthcare, Consumer Staples | Utilities, Financials | Technology, Consumer Discretionary, Industrials, Real Estate |
| **Contraction** | Utilities, Healthcare, Consumer Staples | Communication Services, Real Estate | Technology, Consumer Discretionary, Industrials, Financials, Energy, Materials |

### Economic Logic by Sector

| Sector | Rate Sensitivity | Inflation Sensitivity | Growth Sensitivity | Defensive? |
|--------|-----------------|---------------------|-------------------|-----------|
| Technology | High (long duration) | Low | High | No |
| Healthcare | Low | Low | Low | Yes |
| Financials | High (benefits from steeper curve) | Moderate | Moderate | No |
| Consumer Discretionary | High (credit-sensitive) | Moderate | High | No |
| Consumer Staples | Low | Moderate (pricing power) | Low | Yes |
| Industrials | Moderate | Moderate | High | No |
| Energy | Low | High (commodity-linked) | Moderate | Partial |
| Materials | Low | High (commodity-linked) | Moderate | No |
| Utilities | Very High (bond proxy) | Moderate | Low | Yes |
| Real Estate | Very High (rate-sensitive) | Moderate | Moderate | Partial |
| Communication Services | Moderate | Low | Moderate | Mixed |

## Macro Indicator Deep-Dive

### Interest Rates

**What to track**:
- Fed funds rate (current + dot plot projections)
- 2Y Treasury yield (rate expectations)
- 10Y Treasury yield (growth + inflation expectations)
- 2s/10s spread (yield curve shape)
- Real rates (TIPS yields)

**Sector implications**:
| Rate Environment | Favored Sectors | Hurt Sectors |
|-----------------|----------------|-------------|
| Rates falling | Real Estate, Utilities, Technology, Growth | Financials (NIM compression) |
| Rates rising | Financials, Energy, Value | Utilities, Real Estate, Growth/Tech |
| Rates peaking | Transition — start rotating from late-cycle to defensive | — |
| Inverted curve | Defensive (Staples, Healthcare, Utilities) | Cyclicals, Financials |

### Inflation

**What to track**:
- Headline CPI, Core CPI, Core PCE (Fed's preferred)
- PPI (pipeline inflation)
- 5Y breakeven inflation rate (market expectations)
- Wage growth (employment cost index)
- Commodity indices (CRB, WTI, copper)

**Sector implications**:
| Inflation Environment | Favored Sectors | Hurt Sectors |
|----------------------|----------------|-------------|
| Rising inflation | Energy, Materials, Real Estate (hard assets) | Consumer Discretionary, Technology |
| Falling inflation | Technology, Consumer Discretionary, Growth | Energy, Materials |
| Stagflation | Healthcare, Utilities, Consumer Staples, Gold | Cyclicals, Financials |

### GDP Growth

**What to track**:
- Real GDP (quarterly, annualized)
- GDP Now/tracking estimates (real-time)
- ISM Manufacturing & Services PMI
- Conference Board LEI (leading economic indicators)
- Retail sales, industrial production

**Sector implications**:
| Growth Environment | Favored Sectors | Hurt Sectors |
|-------------------|----------------|-------------|
| Accelerating | Industrials, Technology, Consumer Discretionary, Materials | Defensive (relative underperformance) |
| Decelerating | Healthcare, Utilities, Consumer Staples | Cyclicals |
| Recession | Utilities, Healthcare, Consumer Staples | Everything else, especially Financials and Industrials |

### Employment

**What to track**:
- Non-farm payrolls (monthly)
- Unemployment rate vs. NAIRU
- Initial and continuing jobless claims (weekly, leading)
- JOLTS (job openings, quits rate)
- Labor force participation rate
- Average hourly earnings (wage inflation)

**Sector implications**:
| Employment Environment | Signal | Implication |
|-----------------------|--------|-------------|
| Strong hiring + rising wages | Late cycle | Margin pressure on labor-intensive sectors (retail, restaurants) |
| Weakening claims trend | Early recession signal | Rotate to defensives |
| Rising participation | Healthy expansion | Broad cyclical tailwind |
| Falling quits rate | Confidence waning | Consumer spending at risk → underweight Discretionary |

## Cross-Asset Confirmation Signals

Use other asset classes to confirm or challenge sector rotation signals:

| Signal | Confirms | Challenges |
|--------|----------|-----------|
| Dollar strengthening | Overweight domestic-focused sectors | Challenges EM exposure, commodity sectors |
| Dollar weakening | Overweight multinationals, EM, commodities | Challenges US domestic value |
| Credit spreads widening | Late cycle/contraction rotation | Challenges risk-on sector calls |
| Copper/gold ratio falling | Growth slowing | Challenges cyclical overweights |
| VIX rising | Defensive rotation | Challenges aggressive positioning |
| Oil prices rising | Energy overweight | Challenges consumer/transportation |

## Historical Sector Performance by Phase

*Annualized excess returns vs. S&P 500 by business cycle phase (1962–2023 averages):*

| Sector | Early Expansion | Mid Expansion | Late Expansion | Contraction |
|--------|----------------|---------------|----------------|-------------|
| Technology | +5–8% | +2–4% | -3–5% | -5–10% |
| Healthcare | -2–4% | 0–2% | +2–4% | +3–6% |
| Financials | +4–7% | +1–3% | -2–4% | -6–10% |
| Consumer Disc. | +6–10% | +1–3% | -4–7% | -8–12% |
| Consumer Staples | -3–5% | -1–2% | +2–4% | +5–8% |
| Industrials | +4–7% | +2–4% | -1–3% | -5–8% |
| Energy | -2–5% | +1–3% | +4–8% | -3–6% |
| Materials | +3–6% | +2–4% | +1–3% | -5–8% |
| Utilities | -5–8% | -2–4% | +1–3% | +6–10% |
| Real Estate | +4–8% | +1–2% | -3–5% | -4–8% |

*These are historical averages and can vary significantly by cycle. Always layer current-cycle context.*

## Structural Shifts to Consider

Historical patterns may not hold when structural changes alter sector dynamics:

- **AI capex cycle**: Technology spending may be more resilient than historical late-cycle patterns
- **Energy transition**: Traditional energy sector dynamics changing with renewables growth
- **Deglobalization**: Supply chain reshoring benefits Industrials differently than past cycles
- **Fiscal dominance**: Government spending may dampen cyclical swings in certain sectors
- **Remote work**: Commercial real estate and consumer patterns may differ from historical
- **Healthcare innovation**: Biotech/GLP-1 breakthroughs may make Healthcare more growth-like
- **Rate regime**: Transition from 0% to higher structural rates changes rate-sensitivity calculus

Always note relevant structural shifts when applying historical rotation patterns.

---

## Technical Notes & Implementation Details

### Data Source Considerations

**Primary Data Sources**:
- **FRED (Federal Reserve Economic Data)**: GDP, PMI, unemployment, inflation, interest rates
- **Treasury Yield Curve**: Daily Treasury yield curve rates (2Y, 10Y, 30Y)
- **Sector ETFs**: SPDR Sector ETFs (XLY, XLP, XLE, XLF, XLV, XLI, XLB, XLK, XLU, XLRE)
- **Credit Markets**: ICE BofA US Corporate Index spreads, Moody's BAA spreads
- **Commodity Markets**: Oil (WTI), Copper, Gold prices
- **Volatility Index**: VIX and sector-specific volatility measures

**Data Quality Notes**:
- **Revision Risk**: Many macro indicators are revised (GDP, employment); use real-time data for backtesting
- **Frequency Mismatch**: Some data monthly (GDP), some daily (yields); align appropriately
- **Survivorship Bias**: Sector ETF composition changes over time; adjust for historical accuracy

### Model Implementation Framework

**Phase Identification Algorithm**:
```
Phase_Score = Σ(Indicator_Weight × Phase_Match_Score)
Current_Phase = argmax(Phase_Score)
Confidence = (Max_Score - Second_Max_Score) / Total_Score
```

**Indicator Weighting**:
- **Leading Indicators** (40% weight): Yield curve, PMI, LEI, housing starts
- **Coincident Indicators** (35% weight): GDP, employment, industrial production
- **Lagging Indicators** (25% weight): Inflation, unemployment rate, credit spreads

**Signal Generation Logic**:
1. **Phase Detection**: Identify current business cycle phase
2. **Sector Ranking**: Rank sectors by expected performance in current phase
3. **Signal Strength**: Adjust based on indicator confidence and cross-asset confirmation
4. **Risk Overlay**: Apply risk management constraints (max overweight, diversification)

### Structural Change Adaptation

**Dynamic Weight Adjustment**:
- **AI Era (2010-present)**: Increase Technology sector weight in late cycle
- **Energy Transition (2015-present)**: Adjust Energy sector dynamics, include Clean Energy
- **COVID Impact (2020-present)**: Higher weight to Healthcare and Technology
- **Rate Regime Shift (2022-present)**: Increased sensitivity to rate changes

**Regime Detection**:
```
Regime_Change_Signal = |Current_Indicator - Historical_Mean| / Historical_Std
If Regime_Change_Signal > 2.0: Flag structural change
```

### Cross-Asset Confirmation Framework

**Confirmation Matrix**:
- **Equity-Bond Correlation**: Negative correlation supports equity risk-on
- **Credit Spread Trend**: Tightening spreads support cyclical outperformance
- **Commodity Trends**: Rising commodities support inflation-sensitive sectors
- **Currency Signals**: USD strength impacts multinational earnings

**Divergence Handling**:
When asset classes send conflicting signals:
1. **Weight by Historical Reliability**: Some indicators more reliable than others
2. **Time Lag Consideration**: Some signals lead, others lag
3. **Magnitude Assessment**: Strong signals override weak conflicting signals
4. **Explicit Flagging**: Note conflicts for manual review

---

## Backtest Framework

### Backtest Design

**Objective**: Test whether sector rotation based on macro indicators generates alpha.

**Methodology**:
1. **Historical Signal Generation**: Apply phase identification algorithm to historical data (1960-present)
2. **Portfolio Construction**: Construct sector portfolios based on rotation signals
3. **Performance Measurement**: Compare against benchmark (S&P 500) and buy-and-hold
4. **Regime Analysis**: Test performance across different market environments

### Portfolio Construction Rules

**Base Strategy**:
- **Overweight**: Top 3 sectors for current phase (15% each vs 10% benchmark)
- **Underweight**: Bottom 3 sectors for current phase (5% each vs 10% benchmark)
- **Neutral**: Remaining 4 sectors (10% each)
- **Rebalancing**: Monthly or when phase changes

**Enhanced Strategies**:
- **Signal Strength Weighting**: Scale overweights by signal confidence
- **Momentum Overlay**: Combine rotation with relative momentum
- **Risk Parity**: Adjust weights by sector volatility
- **Liquidity Filter**: Exclude sectors with insufficient liquidity

### Performance Metrics

**Return Metrics**:
- **Annualized Return**: Geometric average return
- **Excess Return**: Return vs S&P 500 benchmark
- **Alpha**: CAPM-adjusted excess return
- **Information Ratio**: Excess return / tracking error

**Risk Metrics**:
- **Volatility**: Annualized standard deviation
- **Maximum Drawdown**: Worst peak-to-trough decline
- **Sharpe Ratio**: Risk-adjusted performance
- **Sortino Ratio**: Downside risk-adjusted performance

**Turnover Analysis**:
- **Portfolio Turnover**: Frequency and magnitude of rebalancing
- **Transaction Costs**: Impact of trading costs on net returns
- **Holding Period**: Average time positions are held

### Statistical Validation

**Hypothesis Testing**:
- **H0**: Sector rotation strategy does not outperform benchmark
- **H1**: Sector rotation strategy generates positive alpha
- **Test**: t-test on excess returns, bootstrap analysis

**Robustness Checks**:
- **Time Period Analysis**: Test across different decades
- **Regime Analysis**: Performance during recessions, expansions, crises
- **Parameter Sensitivity**: Vary rebalancing frequency, weighting schemes
- **Sector Definition**: Test with different sector classifications

### Falsification Criteria

Strategy fails if:
- **Alpha not significant**: t-stat < 1.96 for excess returns
- **High turnover**: Annual turnover > 200% erodes returns after costs
- **Regime dependence**: Only works in specific market conditions
- **Data mining**: Performance deteriorates in out-of-sample testing
- **Survivorship bias**: Results depend on sector selection criteria

### Implementation Considerations

**Data Requirements**:
- **Macro Data**: 50+ years of monthly economic indicators
- **Market Data**: Daily sector ETF prices, total return indices
- **Corporate Actions**: Adjust for splits, dividends, composition changes
- **Benchmark Data**: S&P 500 total return for comparison

**Computational Complexity**:
- **Signal Generation**: Real-time processing of 10+ macro indicators
- **Portfolio Optimization**: Quadratic programming for risk-adjusted weights
- **Backtesting**: Efficient historical simulation with realistic costs
- **Monitoring**: Daily performance tracking and signal updates

**Integration Points**:
- **Risk Management**: Portfolio-level risk limits and stress testing
- **Execution**: Sector ETF trading and liquidity management
- **Reporting**: Performance attribution and signal explanation
- **Compliance**: Investment guidelines and regulatory constraints

### Model Maintenance

**Monthly Updates**:
- Update macro indicator data and phase identification
- Review sector performance vs expectations
- Adjust signal weights based on recent accuracy
- Monitor structural change indicators

**Quarterly Reviews**:
- Comprehensive backtest refresh with latest data
- Review sector classification changes
- Assess model performance across recent market conditions
- Update structural change assumptions

**Annual Overhauls**:
- Re-estimate phase identification parameters
- Review and update sector rotation maps
- Incorporate new research and academic findings
- Consider adding new indicators or sectors

### Expected Performance

**Academic Evidence**:
- **Excess Return**: 2-4% annualized alpha before costs
- **Hit Rate**: 55-65% of quarterly periods outperform benchmark
- **Sharpe Improvement**: 0.2-0.4 improvement over benchmark
- **Drawdown Reduction**: 10-20% reduction in maximum drawdown

**Realistic Expectations**:
- **Not a crystal ball**: Macro signals have noise and false positives
- **Cyclical dependence**: Works better in some cycles than others
- **Implementation costs**: Trading costs and tracking error matter
- **Structural changes**: Historical patterns may not repeat exactly

**Risk Factors**:
- **Model risk**: Overfitting to historical patterns
- **Timing risk**: Phase transitions are identified with lag
- **Structural risk**: Economic changes invalidate historical relationships
- **Execution risk**: Sector ETF liquidity and tracking error
