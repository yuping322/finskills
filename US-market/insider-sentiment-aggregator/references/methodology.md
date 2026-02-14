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
- Falsification: if cluster-buy portfolios do not outperform after excluding microcaps and applying liquidity screens.
