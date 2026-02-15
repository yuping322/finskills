# Methodology: Insider Sentiment Aggregator (US)

Insider transactions (Form 4) are one of the few legally disclosed “skin in the game” signals. The signal is most informative when **multiple insiders buy** with meaningful size relative to wealth/market cap; selling is noisier due to diversification/taxes.

## Data Definitions

### Sources and field mapping (SEC EDGAR Form 4)

Preferred:
- SEC EDGAR Form 4 filings (transaction date, type, shares, price, insider role).

Key fields:
- `txn_type`: buy (`P`), sell (`S`), option exercise, etc.
- `shares`, `price`, `value = shares * price`
- `insider_role`: CEO/CFO/Director/10% owner
- `filing_date` and `txn_date`

Normalize:
- Scale by market cap: `value_pct_mcap = value / market_cap`.
- De-duplicate amended filings; keep the latest.

### Frequency and windows

- Event-driven; aggregate over rolling windows:
  - Short window: 30 calendar days
  - Medium: 90 days
- Backtest horizons: 3 / 6 / 12 months.

## Core Metrics

### Metric list and formulas

- **Net insider buying**: `NetValue = sum(buys_value) - sum(sells_value)` over window
- **Cluster count**: `UniqueBuyers = # of distinct insiders buying`
- **Role-weighted score** (example):
  - CEO/CFO buy weight = 2, Director = 1, 10% owner = 1.5
  - `InsiderScore = Σ(weight * sign(value))`
- **Abnormal intensity**: `NetValue_pct_mcap`

### Standardization

- Percentiles of `NetValue_pct_mcap` within the stock’s own 5y history.
- Cross-sectional rank within a coverage universe if available.

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

Rule 1 (cluster buying → positive):
IF {UniqueBuyers_30d >= 3 AND NetValue_pct_mcap_30d >= 0.10% AND at least one of {CEO, CFO} is a buyer}
THEN {Over the next 3–12 months, expected excess return vs SPY is positive; signal is strongest when buying follows a drawdown.}
CONFIDENCE {0.62}
APPLICABLE_UNIVERSE {US equities with reliable Form 4 coverage; prefer liquid mid/large caps.}
FAILURE_MODE {“Falling knife” distressed situations; insiders buy for optics; subsequent dilution/financing overwhelms signal; data lag in filings.}

Rule 2 (routine selling is weakly informative):
IF {NetValue_pct_mcap_90d is negative BUT sells are dominated by 10b5-1 planned sales and option-related transactions}
THEN {Return direction is ~neutral; do not treat as a bearish signal without corroboration (fundamentals/credit/price).}
CONFIDENCE {0.56}
APPLICABLE_UNIVERSE {US equities; especially high-SBC names where selling is routine.}
FAILURE_MODE {Selling cluster includes multiple executives outside plans; selling accompanies deteriorating fundamentals.}

Rule 3 (selling after strong run-up + valuation stretch → negative skew):
IF {NetValue_pct_mcap_30d <= -0.10% AND stock total return over last 6 months >= +30% AND valuation percentile >= 80}
THEN {Over the next 3–12 months, returns skew negative/mean-reverting (higher downside risk).}
CONFIDENCE {0.55}
APPLICABLE_UNIVERSE {US equities with valuation history and insider coverage.}
FAILURE_MODE {Genuine structural growth winners where insider selling is diversification; market continues re-rating.}

### Trigger / exit / invalidation conditions

- Trigger “bullish insider” only on **cluster buying** with meaningful value.
- Exit when subsequent filings reverse (cluster selling) or fundamentals/price invalidate the thesis.
- Invalidate when insider trades are dominated by administrative events (mergers, trusts) not discretionary sentiment.

### Threshold rationale

- 0.10% of market cap is sized to avoid noise from tiny purchases.
- Unique buyer count reduces the chance of one-person idiosyncrasy.

## Edge Cases and Degradation

### Missing data / outliers handling

- Correct for stock splits when converting shares to value.
- Remove obvious data errors (e.g., price=0, impossible timestamps).

### Fallback proxies

- If Form 4 parsing is unavailable: use reputable “insider buying” aggregates, but mark as lower confidence and always cite the provider.

## Backtest Notes (Minimal)

- Construct signals on filing/transaction date; trade at next close.
- Report 3/6/12m forward excess return vs SPY and sector; test separately for small vs large caps.
- Falsification: if cluster-buy portfolios do not outperform after excluding microcaps and excluding microcaps and applying liquidity screens.

---

## Technical Notes & Implementation Details

### SEC EDGAR Data Processing

**Form 4 Structure**:
- **Transaction Type Codes**: P=Purchase, S=Sale, M=Option Exercise, A=Award, G=Gift
- **Insider Roles**: CEO, CFO, COO, President, VP, Director, 10% Owner, Officer
- **Ownership Type**: Direct, Indirect (trust, family, corporate)
- **Derivative Securities**: Options, warrants, convertible securities

**Data Quality Considerations**:
- **Filing Delays**: Form 4 must be filed within 2 business days, but processing delays add 1-2 days
- **Amendments**: Original filings may be amended; always use latest version
- **Corporate Actions**: Splits, mergers, spin-offs affect share counts and values
- **Survivorship Bias**: Include delisted/bankrupt companies for accurate historical analysis

**Processing Pipeline**:
1. **Download**: Daily fetch of new Form 4 filings from SEC EDGAR
2. **Parse**: Extract transaction details, insider information, ownership data
3. **Clean**: Remove duplicates, handle amendments, standardize formats
4. **Enrich**: Add market cap, stock prices, insider compensation data
5. **Aggregate**: Calculate metrics over rolling windows
6. **Score**: Apply sentiment scoring algorithms

### Signal Enhancement Framework

**Transaction Filtering**:
```
Include Only:
- Open-market purchases (Code P)
- Direct ownership transactions
- Transactions >= $10,000 in value
- Insiders with >= 1 year tenure

Exclude:
- Option exercises (Code M) - often mechanical
- Awards/Grants (Code A) - compensation, not conviction
- Gifts (Code G) - estate/tax planning
- 10b5-1 plan sales - pre-programmed
```

**Meaningfulness Adjustment**:
```
Size_Score = min(1.0, Transaction_Value / (0.01 × Market_Cap))
Compensation_Score = min(1.0, Transaction_Value / (0.1 × Annual_Compensation))
History_Score = min(1.0, Transaction_Value / (0.25 × Existing_Holdings))
```

**Seniority Weighting**:
```
CEO/CFO:      3.0x weight (highest information advantage)
President:    2.5x weight (strategic visibility)
Director:     2.0x weight (governance oversight)
VP/Officer:   1.5x weight (functional visibility)
10% Owner:    1.0x weight (financial stake, limited operational insight)
```

### Composite Sentiment Scoring

**Base Sentiment Score**:
```
Sentiment_Base = Σ(Seniority_Weight × Size_Score × Sign(Transaction))
```

**Context Adjustments**:
- **Price Context**: 20% boost for buying at 52-week lows
- **Sector Context**: 15% boost when sector is down 10%+ 
- **Market Context**: 10% boost during market corrections (VIX > 30)
- **Timing Context**: 5% boost before earnings announcements

**Quality Filters**:
- **Historical Accuracy**: Track each insider's past signal performance
- **Consistency**: Prefer insiders with consistent behavior patterns
- **Independence**: Reduce weight for coordinated buying patterns
- **Liquidity**: Adjust for stock's trading volume and market cap

### Advanced Signal Components

**Cluster Detection**:
```
Cluster_Strength = (Unique_Buyers × Average_Transaction_Size) / Time_Window
Cluster_Quality = Σ(Seniority_Weight × Historical_Accuracy)
```

**Contrarian Signal**:
```
Contrarian_Score = Sentiment_Base × (1 + Price_Discount_Rate)
Where Price_Discount_Rate = (52_Week_High - Current_Price) / 52_Week_High
```

**Persistence Factor**:
```
Persistence = Σ(Sentiment_t-i × Decay_Factor^i) for i=0 to 29
Where Decay_Factor = 0.9 (30-day exponential decay)
```

---

## Backtest Framework

### Backtest Design

**Objective**: Test whether insider sentiment scores predict future stock returns.

**Methodology**:
1. **Signal Generation**: Calculate daily sentiment scores for all stocks
2. **Portfolio Construction**: Form portfolios based on sentiment rankings
3. **Performance Measurement**: Track portfolio returns over multiple horizons
4. **Statistical Analysis**: Test significance of return predictability
5. **Robustness Testing**: Validate across different market conditions

### Test Specifications

**Universe**: US equities with sufficient insider activity and market data
**Period**: 15+ years for statistical significance (post-Reg FD era)
**Frequency**: Daily signal generation, monthly portfolio rebalancing
**Benchmark**: Market-cap weighted index and sector benchmarks

**Portfolio Construction**:
- **Top Decile**: Highest sentiment scores (strong bullish signals)
- **Middle 80%**: Neutral sentiment (no strong signals)
- **Bottom Decile**: Lowest sentiment scores (bearish signals)
- **Liquidity Filter**: Exclude stocks with ADV < $1M to reduce micro-cap bias

### Performance Metrics

**Return Analysis**:
- **Excess Returns**: Portfolio return vs benchmark return
- **Alpha**: CAPM-adjusted excess return
- **Hit Rate**: Percentage of periods with positive excess returns
- **Win/Loss Ratio**: Average gain vs average loss
- **Information Ratio**: Excess return / tracking error

**Risk Analysis**:
- **Volatility**: Portfolio return standard deviation
- **Maximum Drawdown**: Worst peak-to-trough decline
- **Beta**: Portfolio sensitivity to market movements
- **Correlation**: Portfolio correlation with benchmark

**Signal Quality**:
- **Decay Analysis**: How long signals remain predictive
- **Regime Performance**: Performance in different market conditions
- **Sector Analysis**: Performance across different industries
- **Size Segmentation**: Performance by market cap category

### Statistical Validation

**Hypothesis Testing**:
- **H0**: Insider sentiment has no predictive power
- **H1**: High sentiment predicts positive excess returns
- **Test**: t-test on portfolio excess returns, bootstrap analysis

**Regression Analysis**:
```
Return_t+1 = α + β×Sentiment_t + γ×Market_Return_t + δ×Size_t + ε×Value_t + θ
```
- Control for market, size, and value factors
- Test significance of sentiment coefficient (β)

**Cross-Validation**:
- **Time Series**: Rolling window out-of-sample testing
- **Cross-Section**: Holdout sample of stocks
- **Parameter Stability**: Test consistency across different periods

### Falsification Criteria

Strategy fails if:
- **No Alpha**: Portfolio doesn't generate significant excess returns
- **High Turnover Costs**: Excessive trading erodes returns
- **Micro-cap Bias**: Performance driven solely by small, illiquid stocks
- **Data Mining**: Results don't hold in out-of-sample testing
- **Regime Dependence**: Only works in specific market conditions

### Robustness Checks

**Alternative Specifications**:
- **Different Windows**: 15d, 30d, 60d, 90d aggregation periods
- **Weight Schemes**: Different seniority and size weightings
- **Filters**: Vary liquidity, market cap, and minimum transaction size
- **Benchmarks**: Test against different market and sector benchmarks

**Subsample Analysis**:
- **Time Periods**: Test across different decades
- **Market Conditions**: Bull vs bear markets, high vs low volatility
- **Sectors**: Technology, healthcare, financials, industrial
- **Market Caps**: Large-cap vs small-cap segments

**Transaction Cost Analysis**:
- **Trading Costs**: Include realistic commission and spread costs
- **Market Impact**: Price impact of portfolio rebalancing
- **Liquidity Constraints**: Position limits based on trading volume
- **Implementation Lag**: Delay between signal and execution

### Implementation Considerations

**Data Requirements**:
- **SEC Filings**: Complete Form 4 history (2002-present)
- **Market Data**: Daily prices, volumes, market cap
- **Insider Data**: Compensation, tenure, historical performance
- **Corporate Actions**: Splits, mergers, delistings

**Computational Resources**:
- **Processing Power**: Handle ~10,000 daily Form 4 filings
- **Storage**: Historical filing data and calculated metrics
- **Network**: Reliable SEC EDGAR data access
- **Backup**: Redundant data sources and validation

**Integration Points**:
- **Portfolio Management**: Use sentiment scores for position sizing
- **Risk Management**: Monitor insider sentiment as risk factor
- **Research**: Combine with other fundamental and technical signals
- **Compliance**: Ensure compliance with insider trading regulations

### Model Maintenance

**Daily Updates**:
- Process new Form 4 filings
- Update sentiment scores for all stocks
- Flag significant sentiment changes
- Monitor data quality and completeness

**Weekly Reviews**:
- Analyze sentiment trends and patterns
- Review portfolio performance vs expectations
- Assess market conditions affecting sentiment
- Update signal parameters if needed

**Monthly Maintenance**:
- Comprehensive backtest refresh
- Review model accuracy and calibration
- Update insider compensation and tenure data
- Assess need for model enhancements

### Expected Performance

**Academic Evidence**:
- **Excess Return**: 2-4% annualized alpha for top sentiment decile
- **Hit Rate**: 55-65% accuracy in predicting positive returns
- **Persistence**: Signals remain predictive for 3-6 months
- **Size Effect**: Stronger for small/mid-cap stocks

**Practical Expectations**:
- **Signal Quality**: Not all insider activity is informative
- **Market Adaptation**: Markets may adapt to widely known signals
- **Implementation Costs**: Trading costs and market impact matter
- **Regulatory Risk**: Must comply with insider trading regulations

**Limitations**:
- **Data Lag**: 2-4 day delay between transaction and signal
- **Noise**: Many insider transactions are non-informational
- **Coverage**: Limited to companies with insider reporting requirements
- **Interpretation**: Context matters for transaction meaning
