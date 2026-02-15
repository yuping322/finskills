# Methodology: Event Study Analyzer (US)

The objective is to **measure abnormal returns around corporate or macro events** using a pre/post event window framework. This is a standard academic/practitioner tool to isolate the price impact of specific events (earnings, M&A, regulatory decisions, product launches) from normal market movements.

## Data Definitions

### Sources and field mapping

Event study requires:
- **Event data**: Event date (T=0), event type (earnings, M&A, FDA approval, etc.), event details (beat/miss, deal size, approval/rejection)
- **Price data**: Daily adjusted close for target stock(s) and benchmark (yfinance or similar)
- **Benchmark**: Market index (SPY, sector ETF) or peer portfolio
- **Risk-free rate**: Optional, for Sharpe-style adjustments (FRED: DGS3MO)

Key fields:
- `Event_date` (T=0): The announcement/occurrence date
- `Stock_return(t)`: Daily log return of target stock
- `Benchmark_return(t)`: Daily log return of benchmark
- `Abnormal_return(t) = Stock_return(t) - Expected_return(t)`
- `Expected_return(t)`: Estimated from pre-event estimation window using market model or mean-adjusted model

### Frequency and windows

Standard event study windows:
- **Estimation window**: T-252 to T-21 (1 year ending 1 month before event) to estimate normal returns
- **Event window**: T-5 to T+5 (11 days centered on event) or T-1 to T+1 (3 days) for short-term impact
- **Post-event window**: T+1 to T+60 (3 months) to measure drift or reversal

Adjustable based on event type:
- Earnings: T-1 to T+1 (immediate reaction)
- M&A: T-1 to T+20 (deal closure uncertainty)
- FDA approval: T-1 to T+5 (initial reaction + follow-through)
- Macro events (FOMC): T-1 to T+5 (policy digestion)

## Core Metrics

### Metric list and formulas

1. **Expected Return (Market Model)**:
   - Estimate during estimation window: `R_i(t) = α_i + β_i * R_m(t) + ε_i(t)`
   - Use OLS regression on T-252 to T-21
   - `Expected_return(t) = α_i + β_i * Benchmark_return(t)`

2. **Abnormal Return (AR)**:
   - `AR_i(t) = R_i(t) - Expected_return_i(t)`
   - For each day in event window

3. **Cumulative Abnormal Return (CAR)**:
   - `CAR_i(t1, t2) = Σ(AR_i(t))` for t in [t1, t2]
   - Example: `CAR(-1, +1)` = sum of AR from T-1 to T+1

4. **Average Abnormal Return (AAR)** (for multiple events):
   - `AAR(t) = mean_i(AR_i(t))` across N events
   - `CAAR(t1, t2) = Σ(AAR(t))` for t in [t1, t2]

5. **Statistical Significance**:
   - `t-stat(CAR) = CAR / (σ_AR * sqrt(event_window_length))`
   - `σ_AR` = standard deviation of AR during estimation window
   - Significant if |t-stat| >= 1.96 (95% confidence) or >= 2.58 (99% confidence)

6. **Buy-and-Hold Abnormal Return (BHAR)** (alternative to CAR):
   - `BHAR(t1, t2) = Π(1 + R_i(t)) - Π(1 + R_m(t))` for t in [t1, t2]
   - Accounts for compounding; preferred for longer windows (> 20 days)

### Standardization

- Use **log returns** for daily calculations (additive property)
- Use **BHAR** for windows > 20 days (compounding matters)
- Use **sector-adjusted benchmark** when possible (sector ETF vs SPY) to remove industry effects
- Use **peer-adjusted returns** for M&A studies (compare to peer portfolio, not market)

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

Rule 1 (positive earnings surprise → positive CAR):
IF {Earnings beat consensus by >= 5% AND CAR(-1, +1) > 0 AND t-stat(CAR) >= 1.96}
THEN {Over the next 20-60 trading days, stock tends to drift higher (post-earnings announcement drift, PEAD); CAR(+2, +60) is positive.}
CONFIDENCE {0.65; initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US equities with analyst coverage and liquid options; strongest for small/mid-caps.}
FAILURE_MODE {Guidance disappoints despite beat; sector rotation away from stock; macro shock overrides; drift already priced in by options market.}

Rule 2 (M&A announcement → immediate pop, then drift):
IF {M&A announced with premium >= 20% AND CAR(-1, +1) >= 15% AND deal is all-cash}
THEN {Over the next 1-5 days, CAR(0, +5) tends to stabilize near premium; over next 60 days, returns converge to deal price (arbitrage).}
CONFIDENCE {0.75; initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US equities with M&A announcements; strongest for deals with regulatory approval likelihood >= 80%.}
FAILURE_MODE {Deal breaks (regulatory rejection, financing issues); competing bid emerges; target management resists; market expects higher bid.}

Rule 3 (FDA rejection → negative CAR with reversal):
IF {FDA rejects drug approval AND CAR(-1, +1) <= -20% AND company has pipeline diversification}
THEN {Over the next 5-20 days, CAR(+2, +20) may partially reverse (oversold bounce) by 5-10% as market reassesses pipeline value.}
CONFIDENCE {0.55; initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US biotech/pharma with binary events; strongest for companies with multiple drug candidates.}
FAILURE_MODE {No pipeline diversification; cash burn concerns; secondary offering dilutes; sector-wide risk-off.}

Rule 4 (FOMC hawkish surprise → sector rotation):
IF {FOMC raises rates by >= 50bps (vs 25bps expected) AND CAR(-1, +1) for growth stocks <= -3% AND CAR for value stocks >= 0%}
THEN {Over the next 20-60 days, value outperforms growth by >= 5% as rate sensitivity drives rotation.}
CONFIDENCE {0.60; initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US equities across sectors; strongest for high-duration growth (tech) vs low-duration value (financials, energy).}
FAILURE_MODE {Growth earnings resilience offsets rate impact; recession fears dominate (flight to quality); Fed pivots quickly.}

### Trigger / exit / invalidation conditions

- **Trigger event study**: When event is announced or occurs (T=0 is known)
- **Exit/stop monitoring**: When CAR stabilizes (no significant daily AR for >= 10 consecutive days) or when event window ends (T+60)
- **Invalidate**: When confounding events occur during event window (e.g., another major announcement within T-5 to T+5), when estimation window has insufficient data (< 100 days), or when stock is illiquid (ADV < $1M)

### Threshold rationale

- **T-252 to T-21 estimation window**: Standard in academic literature; avoids event contamination while providing sufficient data for regression
- **T-1 to T+1 event window**: Captures immediate market reaction; extends to T-5 to T+5 for slower information diffusion
- **T+2 to T+60 post-event window**: Captures drift or reversal; 60 days is practical horizon before other events dominate
- **t-stat >= 1.96**: 95% confidence threshold; use 2.58 for 99% confidence in high-stakes decisions
- **CAR thresholds (5%, 15%, 20%)**: Based on typical market reactions to earnings, M&A, and binary events; adjust by event type and market cap

## Edge Cases and Degradation

### Missing data / outliers handling

- **Missing benchmark data**: Use market-wide index (SPY) if sector ETF is unavailable; flag as lower confidence
- **Gaps in stock data**: If stock is halted during event window, use last available price and flag as "incomplete event window"
- **Outliers in estimation window**: Remove days with |return| > 3 std dev before running market model regression
- **Confounding events**: If another major event occurs within T-5 to T+5, flag as "contaminated event window" and consider excluding or using multivariate model

### Fallback proxies

- **No benchmark**: Use mean-adjusted model (Expected_return = mean return during estimation window) with lower confidence
- **Short history (< 100 days)**: Use shorter estimation window (T-60 to T-21) and flag as "limited history"
- **Illiquid stocks**: Extend event window to T-5 to T+10 to capture delayed price discovery; flag as "illiquid"
- **Multiple events on same day**: Use portfolio approach (equal-weight all events) and report AAR/CAAR instead of individual CAR

## Backtest Notes (Minimal)

- **Backtest design**: Collect all events of a given type (e.g., earnings beats) over 5-10 years; compute CAR for each; test if mean(CAR) > 0 and t-stat >= 1.96
- **Performance metric**: Mean CAR, median CAR, % positive CAR, t-stat, Sharpe ratio of event-driven strategy
- **Falsification**: Rule fails if mean(CAR) is not significantly different from zero or if % positive CAR <= 50%
- **Cross-sectional tests**: Segment by market cap, sector, event magnitude to identify where rules are strongest
- **Robustness checks**: Test with different estimation windows (T-126 to T-21, T-504 to T-21), different event windows (T-2 to T+2, T-1 to T+5), and different benchmarks (SPY, sector ETF, peer portfolio)

## Event Study Workflow

### Step-by-step process

1. **Define event**: Identify event date (T=0), event type, and event details
2. **Select benchmark**: Choose market index, sector ETF, or peer portfolio
3. **Collect data**: Pull daily returns for stock and benchmark from T-252 to T+60
4. **Estimate normal returns**: Run market model regression on T-252 to T-21
5. **Compute abnormal returns**: Calculate AR for each day in event window (T-5 to T+5 or T-1 to T+1)
6. **Compute CAR**: Sum AR over event window
7. **Test significance**: Compute t-stat and p-value
8. **Analyze post-event drift**: Compute CAR(+2, +60) to check for continuation or reversal
9. **Report results**: Provide CAR, t-stat, % positive days, and interpretation

### Quality checks

- **Estimation window quality**: Ensure R² >= 0.10 in market model regression (if R² < 0.10, stock is weakly correlated with market; consider peer benchmark)
- **Event window contamination**: Check for other major announcements within T-5 to T+5
- **Data integrity**: Verify no splits, dividends, or corporate actions distort returns
- **Statistical power**: For multiple events, ensure N >= 30 for reliable t-stats

### Monitoring checklist

- **Daily (during event window)**: Update AR and CAR as new prices arrive
- **Weekly (post-event)**: Monitor for drift or reversal
- **Event-driven**: Re-run analysis if confounding events occur
- **Quarterly**: Review event study results across all events to refine thresholds and confidence levels
