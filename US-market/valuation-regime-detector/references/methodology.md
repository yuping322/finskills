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

## Backtest Notes (Minimal)

- Run valuation-regime backtests at monthly frequency to avoid look-ahead noise.
- Evaluate 1y/3y/5y forward total returns; report dispersion and drawdowns.
- Falsification: if “cheap” regimes do not deliver higher forward returns than “expensive” regimes over long samples net of inflation.
