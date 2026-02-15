# Methodology: Equity Research Orchestrator (US)

The objective is to **orchestrate a comprehensive equity research workflow** by systematically calling relevant analysis modules (valuation, momentum, quality, risk, catalysts) and assembling a coherent, actionable deliverable. This is not a single-metric screener; it is a **structured research process** that ensures completeness and consistency.

## Data Definitions

### Sources and field mapping

The orchestrator aggregates inputs from multiple modules:
- **Price/returns**: yfinance (daily adjusted close, volume)
- **Fundamentals**: SEC EDGAR 10-K/10-Q filings (revenue, earnings, cash flow, balance sheet)
- **Valuation multiples**: Computed from price + fundamentals (P/E, P/B, EV/EBITDA, FCF yield)
- **Analyst estimates**: Optional (consensus EPS, revenue estimates if available)
- **Macro context**: FRED (rates, inflation, GDP growth)
- **Peer universe**: Industry classification (GICS sector/industry)

Key fields per module:
- Valuation: `P/E`, `P/B`, `EV/EBITDA`, `FCF_yield`, sector percentiles
- Momentum: `Return_1m`, `Return_3m`, `Return_12m`, `RSI_14d`
- Quality: `ROE`, `ROA`, `Debt/Equity`, `Interest_coverage`, `FCF/Net_income`
- Risk: `Beta`, `Volatility_60d`, `Max_drawdown_252d`, `Liquidity_days`
- Catalysts: Earnings date, product launches, regulatory events (manual input or calendar scraping)

### Frequency and windows

- **Daily**: Price, volume, momentum indicators
- **Quarterly**: Fundamentals (10-K/10-Q filings)
- **Annual**: Long-term quality metrics (5-year ROE, debt trends)
- **Event-driven**: Catalyst calendar (earnings, conferences, regulatory decisions)

Suggested windows:
- Short-term momentum: 1m / 3m
- Medium-term trends: 6m / 12m
- Quality assessment: 3y / 5y trailing
- Valuation comparison: Current vs 5y historical range

## Core Metrics

### Metric list and formulas

The orchestrator computes a **composite research score** by aggregating module outputs:

1. **Valuation Score (0-100)**:
   - `Valuation_Score = mean(percentile_rank(P/E), percentile_rank(P/B), percentile_rank(EV/EBITDA), percentile_rank(FCF_yield))`
   - Lower multiples → higher score (inverted percentiles for P/E, P/B, EV/EBITDA)
   - Higher FCF yield → higher score

2. **Momentum Score (0-100)**:
   - `Momentum_Score = weighted_mean(Return_1m * 0.2, Return_3m * 0.3, Return_12m * 0.5)`
   - Standardized to percentile ranks within sector

3. **Quality Score (0-100)**:
   - `Quality_Score = mean(percentile_rank(ROE), percentile_rank(ROA), percentile_rank(Interest_coverage), inverted_percentile_rank(Debt/Equity))`
   - Higher profitability + lower leverage → higher score

4. **Risk Score (0-100)**:
   - `Risk_Score = 100 - mean(percentile_rank(Volatility_60d), percentile_rank(Max_drawdown_252d), percentile_rank(Beta))`
   - Lower risk → higher score (inverted)

5. **Catalyst Score (0-100)**:
   - Binary/manual: Upcoming earnings (20 pts), product launch (30 pts), regulatory approval (50 pts)
   - Decay over time: full points if event within 30 days, 50% if 30-60 days, 0% if > 60 days

6. **Composite Research Score**:
   - `Composite = Valuation * 0.25 + Momentum * 0.20 + Quality * 0.25 + Risk * 0.15 + Catalyst * 0.15`
   - Weights are adjustable based on investment style (value vs growth vs momentum)

### Standardization

- Use **sector-relative percentiles** for valuation and quality (avoid comparing tech to utilities)
- Use **market-wide percentiles** for momentum and risk (cross-sector comparison valid)
- Use **z-scores** for outlier detection (flag if any metric > 3 std dev from sector mean)

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

Rule 1 (high composite score → positive forward returns):
IF {Composite_Score >= 75 AND Valuation_Score >= 60 AND Quality_Score >= 60}
THEN {Over the next 3-6 months, stock tends to outperform sector benchmark by >= 5% (annualized alpha).}
CONFIDENCE {0.65; initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US large/mid-cap equities with liquid options and analyst coverage.}
FAILURE_MODE {Macro shock overrides fundamentals; sector rotation away from stock's industry; hidden accounting issues not captured by quality metrics; catalyst fails to materialize.}

Rule 2 (valuation trap detection):
IF {Valuation_Score >= 80 (very cheap) AND Quality_Score <= 40 (poor fundamentals) AND Momentum_Score <= 30 (weak price action)}
THEN {Stock is likely a value trap; over the next 6-12 months, returns tend to be negative or underperform sector.}
CONFIDENCE {0.70; initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US equities across all market caps; strongest signal for small/mid-caps with deteriorating fundamentals.}
FAILURE_MODE {Turnaround catalyst emerges (new management, asset sale, restructuring); sector-wide revaluation lifts all boats; activist investor involvement.}

Rule 3 (momentum + catalyst convergence → short-term outperformance):
IF {Momentum_Score >= 70 AND Catalyst_Score >= 50 (major event within 30 days) AND Risk_Score >= 50 (moderate risk)}
THEN {Over the next 1-3 months, stock tends to outperform sector by >= 3% as event approaches and momentum persists.}
CONFIDENCE {0.60; initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US equities with identifiable catalysts (earnings, FDA approvals, product launches).}
FAILURE_MODE {Catalyst disappoints (earnings miss, regulatory rejection); momentum reverses sharply; volatility spikes and risk-off sentiment dominates.}

Rule 4 (quality + valuation mismatch → mean reversion opportunity):
IF {Quality_Score >= 75 (high quality) AND Valuation_Score <= 30 (expensive) AND Momentum_Score <= 40 (weak recent performance)}
THEN {Over the next 6-12 months, stock may mean-revert as quality is re-rated; consider waiting for better entry or using options.}
CONFIDENCE {0.55; initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US large-cap equities with stable business models and long track records.}
FAILURE_MODE {Growth expectations justify high valuation; secular tailwinds sustain premium multiples; quality deteriorates unexpectedly.}

### Trigger / exit / invalidation conditions

- **Trigger research**: When Composite_Score >= 70 or when a major catalyst is identified
- **Exit/downgrade**: When Composite_Score drops below 50 or when a key module score (Valuation, Quality, Momentum) drops by >= 30 points within 1 quarter
- **Invalidate**: When fundamental data is stale (> 6 months old), when sector classification changes materially, or when liquidity dries up (ADV drops >= 50%)

### Threshold rationale

- 75th percentile (score >= 75) is a practical cutoff for "high conviction" ideas
- 60th percentile (score >= 60) for individual modules ensures minimum quality bar
- Composite weights (Valuation 25%, Quality 25%, Momentum 20%, Risk 15%, Catalyst 15%) balance fundamental and technical factors
- Adjust weights for different strategies: value-focused (Valuation 40%, Quality 30%), momentum-focused (Momentum 40%, Catalyst 20%)

## Edge Cases and Degradation

### Missing data / outliers handling

- **Missing fundamentals**: If 10-K/10-Q data is unavailable, use trailing 12-month estimates or peer averages with confidence penalty (-20 points on Quality_Score)
- **Missing analyst estimates**: Skip Catalyst_Score contribution or use historical earnings surprise patterns
- **Outliers**: Cap extreme values at 99th percentile (e.g., P/E > 100 or negative) to avoid distortion
- **Negative earnings**: Use EV/Sales or P/B instead of P/E; flag as "not meaningful" in output

### Fallback proxies

- **No sector data**: Use market-wide percentiles with lower confidence (-10 points)
- **No catalyst calendar**: Set Catalyst_Score = 50 (neutral) and rely on other modules
- **Illiquid stocks**: If ADV < $1M, add warning and increase Risk_Score penalty (+20 points to risk, which lowers overall Risk_Score)
- **Recent IPO (< 1 year)**: Insufficient history for momentum/quality; use shorter windows (3m/6m) and flag as "limited history"

## Backtest Notes (Minimal)

- **Backtest design**: Build Composite_Score EOD on last trading day of each month; hold top quintile for 1 month, rebalance monthly
- **Performance metric**: Compare Sharpe ratio and alpha vs sector benchmark (e.g., SPY, sector ETFs)
- **Falsification**: Rule fails if top quintile does not outperform bottom quintile by >= 3% annualized over 5-year sample
- **Sensitivity analysis**: Test different weight combinations (value-tilt, momentum-tilt, quality-tilt) to identify robust configurations
- **Transaction costs**: Assume 10 bps per trade; if turnover > 50% monthly, net alpha may be negative

## Orchestration Workflow

### Step-by-step process

1. **Input validation**: Confirm ticker, sector, market cap, liquidity threshold
2. **Data collection**: Pull price, fundamentals, peer data from all sources
3. **Module execution**: Compute Valuation, Momentum, Quality, Risk, Catalyst scores
4. **Composite scoring**: Aggregate module scores using defined weights
5. **Peer comparison**: Rank stock vs sector peers on Composite_Score
6. **Catalyst check**: Identify upcoming events and adjust Catalyst_Score
7. **Risk assessment**: Flag high-risk stocks (Risk_Score < 40) and illiquid names
8. **Output generation**: Produce structured report with scores, rankings, key drivers, risks, and monitoring checklist

### Quality checks

- **Data freshness**: Flag if any data source is > 30 days stale
- **Consistency**: Ensure all module scores are on 0-100 scale
- **Peer validity**: Confirm >= 10 peers in sector for meaningful percentiles
- **Outlier detection**: Flag if any raw metric is > 3 std dev from sector mean

### Monitoring checklist

- **Weekly**: Update price, momentum, risk metrics
- **Quarterly**: Update fundamentals after earnings release
- **Event-driven**: Update Catalyst_Score when new events are announced
- **Annual**: Review sector classification and peer universe
