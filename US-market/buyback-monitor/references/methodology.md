# Methodology: Buyback Monitor (US)

Buybacks can be (a) an efficient capital return and undervaluation signal, or (b) a cosmetic offset to dilution / poorly-timed leverage. This methodology focuses on **net share count reduction**, **funding quality**, and **valuation context**.

## Data Definitions

### Sources and field mapping (SEC filings + price)

Preferred:
- SEC 10-Q/10-K cash flow statement and equity footnotes (repurchases, SBC).
- Shares outstanding (quarterly) + market cap/price (daily).
- Optional: debt metrics from filings or financial statements.

Key fields (names vary by provider/XBRL):
- `repurchase_cash`: cash paid for repurchase of common stock (quarterly)
- `shares_out`: diluted shares outstanding (quarterly)
- `sbc`: share-based compensation expense (quarterly)
- `fcf`: free cash flow = CFO − CapEx (TTM)
- `net_debt`: total debt − cash (quarterly)

### Frequency and windows

- Repurchase & shares: quarterly; compute trailing 4 quarters (TTM).
- Price/market cap: daily; use quarter-end or trailing average for alignment.
- Backtest horizons: 3 / 6 / 12 months.

## Core Metrics

### Metric list and formulas

- **Gross buyback yield (TTM)**: `GBY = repurchase_cash_TTM / market_cap`
- **Net share change (TTM)**: `ΔShares = (shares_out_t - shares_out_{t-4q}) / shares_out_{t-4q}`
- **Net buyback yield (TTM)**: `NBY = -ΔShares` (positive if shares shrink)
- **SBC dilution proxy**: `SBC_yield = sbc_TTM / market_cap`
- **Shareholder yield** (optional): `NBY + dividend_yield`
- **Funding quality**:
  - `FCF_yield = fcf_TTM / market_cap`
  - `Leverage = net_debt / EBITDA` (or debt/FCF if EBITDA unavailable)

### Standardization

- Cross-sectional: percentile ranks within sector/industry.
- Time-series: compare `NBY` vs the company’s 5y history (percentiles).

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

Rule 1 (net buybacks funded by FCF → positive):
IF {NBY_TTM >= 2% AND FCF_yield >= 3% AND Leverage is stable or improving over the last 4 quarters}
THEN {Over the next 3–12 months, the stock’s excess return vs SPY is more likely positive; buybacks act as a supportive demand/discipline signal.}
CONFIDENCE {0.62}
APPLICABLE_UNIVERSE {US listed common stocks with reliable filings; prefer mkt cap > $1B and adequate liquidity.}
FAILURE_MODE {Buybacks are badly timed at valuation peaks; earnings cycle turns down; repurchases are announced but not executed; accounting changes distort FCF.}

Rule 2 (buybacks mostly offset dilution → neutral/negative):
IF {GBY_TTM >= 2% AND NBY_TTM <= 0.5% AND SBC_yield >= 2%}
THEN {Over the next 3–12 months, expected excess return is neutral-to-negative vs peers; buybacks are primarily dilution management, not genuine shrink.}
CONFIDENCE {0.58}
APPLICABLE_UNIVERSE {US stocks with material SBC (often tech/growth); require consistent share count reporting.}
FAILURE_MODE {Company enters a sustained hyper-growth phase where SBC is efficiently “reinvested”; buybacks accelerate later after growth slows.}

Rule 3 (levered buybacks into tightening credit → negative tail risk):
IF {NBY_TTM >= 2% AND Leverage is rising AND credit spreads are widening (HY_OAS_ZL >= 1.0)}
THEN {Over the next 3–12 months, downside risk increases and expected excess return skews negative (buybacks increase fragility).}
CONFIDENCE {0.60}
APPLICABLE_UNIVERSE {US stocks using debt-funded repurchases; credit-sensitive sectors.}
FAILURE_MODE {Earnings/FCF surprises upward; refinancing remains cheap; management buys back at truly depressed valuations.}

### Trigger / exit / invalidation conditions

- Trigger “constructive buyback” only when **net shares shrink** and funding quality is acceptable.
- Exit/downgrade when net shares stop shrinking for 2 consecutive quarters or leverage deteriorates.
- Invalidate if share count changes are dominated by M&A, splits, or one-off recap events.

### Threshold rationale

- 2% net buyback yield is large enough to matter vs typical US equity issuance.
- Conditioning on FCF and leverage separates “healthy return” from “financial engineering”.

## Edge Cases and Degradation

### Missing data / outliers handling

- Shares outstanding can jump due to splits or acquisitions; adjust for splits and annotate M&A.
- Repurchase cash flow can be lumpy; prefer TTM sums.

### Fallback proxies

- If repurchase cash is missing: use `NBY` from shares outstanding as the primary measure.
- If SBC is missing: infer dilution risk from rising share count despite reported buybacks (lower confidence).

## Backtest Notes (Minimal)

- Rebalance signals quarterly on filing updates; evaluate 3/6/12m forward excess returns vs SPY and sector.
- Falsification: if net-buyback portfolios do not outperform after controlling for size/quality and net of reasonable costs.
