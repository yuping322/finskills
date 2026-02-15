# Methodology: Policy Sensitivity Brief (US)

The objective is to map policy/macro releases (Fed decisions, fiscal changes, regulatory shifts) to likely sector/style sensitivities and produce a monitoring checklist. This is a **qualitative-quantitative hybrid** that combines transmission mechanism logic with observable market proxies.

## Data Definitions

### Sources and field mapping

Macro/policy inputs:
- **FRED**: Fed Funds Rate, 10Y Treasury Yield, 2Y-10Y spread, CPI, PPI, unemployment rate
- **Fed statements/minutes**: Tone analysis (manual or text-based)
- **Fiscal data**: Congressional Budget Office (CBO) projections, Treasury data

Market proxies:
- **yfinance**: Sector ETFs (XLF, XLE, XLK, XLU, XLV, XLI, XLB, XLP, XLY, XLRE, XLC), style factors (IWM, QQQ, DIA)
- **Volatility**: VIX, MOVE index (bond vol)
- **Credit spreads**: HYG-LQD spread proxy

Key fields:
- `policy_rate`, `yield_10y`, `yield_curve_slope`
- `sector_return`, `sector_beta_to_policy`
- `inflation_rate`, `real_rate = nominal_rate - inflation`

### Frequency and windows

- Policy events: Event-driven (FOMC meetings, major fiscal announcements)
- Market response: Daily returns; aggregate over event windows (T-1 to T+5, T+20)
- Historical calibration: 5–10 year lookback for sector sensitivities

## Core Metrics

### Metric list and formulas

- **Rate sensitivity (duration proxy)**:
  - `Beta_sector_to_10Y = cov(sector_return, Δyield_10y) / var(Δyield_10y)` over rolling 252d
  - Negative beta → rate-sensitive (inverse relationship): When yields rise, these sectors tend to underperform (Utilities, REITs, Staples)
  
- **Inflation sensitivity**:
  - `Beta_sector_to_CPI = cov(sector_return, Δinflation) / var(Δinflation)`
  - Positive beta → inflation beneficiaries (Energy, Materials)

- **Policy regime classification**:
  - Tightening: Fed Funds rising, yield curve flattening/inverting
  - Easing: Fed Funds falling, yield curve steepening
  - Neutral: Stable rates, normal curve shape

- **Sector relative strength**:
  - `RS_sector = sector_return / SPY_return` over event window
  - Percentile rank vs 5y history

### Standardization

- Use z-scores for rate/inflation changes to identify "significant" moves
- Use percentiles for sector relative performance (0–100 scale)
- Normalize policy tone scores (-1 to +1: dovish to hawkish)

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

Rule 1 (rate hikes → defensive rotation):
IF {Fed Funds rising by >= 25bps (at time T, FOMC announcement) AND 
    yield curve has flattened over past 20 trading days (2Y-10Y spread declined >= 20bps from T-20 to T)}
THEN {Over the next 1–3 months from T, rate-sensitive sectors (Utilities, REITs, Staples) tend to underperform due to higher discount rates; Financials face mixed signals (benefit from higher short-term rates but headwinds from flat/inverted curve); cyclicals face headwinds from tightening financial conditions.}
CONFIDENCE {0.65 — initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US sector ETFs; large-cap equities.}
FAILURE_MODE {Market already priced in hikes; "good tightening" (strong growth) supports cyclicals; curve steepens unexpectedly; Fed pivots quickly.}
PRE-CHECK {Before applying rule, verify market has not already priced in:
  - Compare Fed Funds futures implied rate to actual rate; if futures price in >= 50bps additional hikes, reduce confidence by 20%
  - Check if rate-sensitive sectors already underperformed by >= 1 std dev over past 20 days; if yes, skip rule (likely priced in)}

Rule 2a (inflation surprise + accommodative policy → commodity outperformance):
IF {CPI surprise >= +0.3% vs consensus AND 
    real rates declining AND 
    Fed does not signal aggressive tightening within 5 trading days (no hawkish pivot in statement/press conference) AND
    economic growth indicators remain positive (GDP growth > 2% or leading indicators stable)}
THEN {Over the next 1–6 months, Energy, Materials, and commodity-linked equities tend to outperform; long-duration growth underperforms.}
CONFIDENCE {0.60 — initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US equities; sector rotation strategies.}
FAILURE_MODE {Stagflation concerns emerge (growth slows + inflation persists); demand destruction offsets pricing power; commodity supply increases; Fed eventually forced to tighten aggressively.}

Rule 2b (inflation surprise + hawkish response → mixed signals):
IF {CPI surprise >= +0.3% vs consensus AND 
    Fed signals aggressive tightening (dot plot shifts up >= 50bps OR explicit hawkish language)}
THEN {Short-term (1-4 weeks): commodity stocks may rally on inflation theme; Medium-term (1-3 months): cyclicals face headwinds from tightening; defensive sectors may outperform.}
CONFIDENCE {0.50 — initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US equities; tactical trading strategies.}
FAILURE_MODE {Inflation proves transitory; Fed credibility restores quickly; market front-runs the tightening cycle.}

Rule 3 (fiscal stimulus announcement → cyclical/small-cap boost):
IF {Major fiscal package announced (infrastructure, tax cuts) with credible passage likelihood}
THEN {Over the next 3–12 months, cyclical sectors (Industrials, Materials, Discretionary) and small caps (IWM) tend to outperform; defensive sectors lag.}
CONFIDENCE {0.58 — initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US equities; particularly domestic-focused names.}
FAILURE_MODE {Stimulus is smaller than expected; implementation delays; offset by tax increases or regulatory headwinds; market already priced in.}

Rule 4 (regulatory tightening → sector-specific headwinds):
IF {New regulation targets specific sector (e.g., tech antitrust, healthcare pricing, financial capital requirements)}
THEN {Over the next 6–24 months, affected sector faces margin pressure and multiple compression; relative performance deteriorates.}
CONFIDENCE {0.55 — initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US equities; sector-specific.}
FAILURE_MODE {Regulation is watered down; sector adapts better than expected; offsetting tailwinds (demand growth, innovation).}

### Trigger / exit / invalidation conditions

- **Trigger**: Policy announcement or significant macro data surprise (>= 1 std dev)
- **Monitor**: Track sector relative performance over T+5, T+20, T+60 days
- **Exit**: When policy stance reverses or market response contradicts historical pattern
- **Invalidate**: When structural changes break historical relationships (e.g., post-2008 ZIRP, post-COVID fiscal dominance)

### Threshold rationale

- 25bps rate change: Standard Fed move size; market-moving
- 0.3% CPI surprise: ~1 std dev; material enough to shift expectations
- Percentile thresholds (80/20): Capture tail events without excessive noise

## Edge Cases and Degradation

### Missing data / outliers handling

- **Policy tone**: If Fed minutes unavailable, use market-implied rate expectations (Fed Funds futures)
- **Sector data gaps**: If specific sector ETF has low liquidity, use constituent-weighted index or skip with disclaimer
- **Outlier events**: Remove COVID-era (2020 Q1-Q2) from historical calibration unless explicitly modeling crisis scenarios

### Fallback proxies when a data source is unavailable

- **No FRED access**: Use Treasury.gov for yields; BLS.gov for CPI
- **No sector ETFs**: Use GICS sector indices from S&P or MSCI
- **No credit spreads**: Use VIX as risk appetite proxy (inverse relationship)
- **No policy text**: Rely purely on quantitative rate/yield changes; mark qualitative analysis as unavailable

## Backtest Notes (Minimal)

- Construct policy event calendar (FOMC dates, major fiscal announcements)
- Measure sector excess returns (vs SPY) over T+5, T+20, T+60 windows
- Test if high-sensitivity sectors (by historical beta) show directionally consistent responses
- Calculate realized confidence levels by measuring hit rate of directional predictions
- Falsification: If sector responses are random or opposite to transmission mechanism logic across multiple cycles
- Note: Confidence levels above are initial estimates and should be updated based on backtest results

## Monitoring Checklist Template

For each policy event, track:
1. Policy change magnitude and direction
2. Market-implied expectations (Fed Funds futures, breakeven inflation)
3. Sector relative performance vs historical sensitivity
4. Divergences from expected pattern (flag for investigation)
5. Update sensitivity betas quarterly
