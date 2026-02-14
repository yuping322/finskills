# Methodology: Earnings Reaction Analyzer (US)

Earnings are discrete information events. The core “edge” hypotheses are:
- **Post-earnings announcement drift (PEAD)**: surprises can continue to drift in the same direction.
- **Overreaction**: extreme gaps can partially mean-revert, especially without fundamental confirmation.

## Data Definitions

### Sources and field mapping

Preferred:
- Earnings calendar + EPS actual vs estimate + revenue actual vs estimate (provider-dependent; yfinance sometimes supplies).
- Price/volume history (daily; optionally intraday around the event).

Key fields:
- `earn_date`
- `eps_actual`, `eps_est`
- `rev_actual`, `rev_est`
- `close`, `open`, `high`, `low`, `volume`
- Benchmark return (SPY) for abnormal returns

### Frequency and windows

- Event frequency: quarterly.
- Event windows:
  - Immediate reaction: day 0 (earnings date) and day +1 (first full session)
  - Drift window: +2 to +60 trading days
- Baseline estimation window for abnormal returns: [-120, -20] trading days.

## Core Metrics

### Metric list and formulas

- **EPS surprise**: `SurpEPS = (eps_actual - eps_est) / |eps_est|`
- **Standardized surprise**: z-score of `SurpEPS` over last 8–12 quarters (if history exists)
- **Gap**: `Gap = (Open_{t+1} - Close_t) / Close_t` (if after-hours earnings)
- **Abnormal return (AR)**: `AR_d = r_stock_d - beta*r_mkt_d` (or simple market-adjusted)
- **CAR(0,2)**: cumulative abnormal return over day 0..2
- **Volume ratio**: `VolRatio = Volume_{t+1} / ADV20`
- **Close location**: `CLV = (Close - Low) / (High - Low)` on reaction day

### Standardization

- Use percentiles for Gap and VolRatio (fat-tailed).
- Use z-score for surprise when enough quarters are available.

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

Rule 1 (positive surprise + strong tape → positive drift):
IF {SurpEPS_z >= +1.0 AND CAR(0,2) > +2% AND VolRatio >= 2.0 AND CLV >= 0.75}
THEN {Over the next 20–60 trading days, expected excess return vs sector/market is positive (PEAD).}
CONFIDENCE {0.60}
APPLICABLE_UNIVERSE {Liquid US equities with consistent earnings history; avoid microcaps.}
FAILURE_MODE {Guidance is negative despite beat; macro shock; one-off accounting beats not reflected in cash flow.}

Rule 2 (negative surprise + weak tape → negative drift):
IF {SurpEPS_z <= -1.0 AND CAR(0,2) < -2% AND VolRatio >= 2.0 AND CLV <= 0.25}
THEN {Over the next 20–60 trading days, expected excess return is negative; downside follow-through risk is elevated.}
CONFIDENCE {0.62}
APPLICABLE_UNIVERSE {Liquid US equities; particularly those with high leverage or weak balance sheets.}
FAILURE_MODE {Takeover/buyback support; rapid guidance reversal; broad market risk-on offsets idiosyncratic miss.}

Rule 3 (price gap without fundamental confirmation → partial mean reversion):
IF {abs(CAR(0,1)) >= 8% AND SurpEPS_z is between [-0.5, +0.5]}
THEN {Over the next 5–20 trading days, returns tend to mean-revert (fade extreme reaction) with modest positive expectancy.}
CONFIDENCE {0.55}
APPLICABLE_UNIVERSE {US equities with liquid trading and stable reporting.}
FAILURE_MODE {Hidden information in guidance/segment detail; subsequent analyst revisions validate the move; short squeeze dynamics.}

### Trigger / exit / invalidation conditions

- Trigger PEAD rules only when surprise and tape agree.
- Exit if price reverses strongly (e.g., breaks reaction-day low/high) within 3–5 sessions.
- Invalidate if the earnings date is misaligned (preliminary releases, multiple events clustered).

### Threshold rationale

- `±1.0` standardized surprise is large enough to matter but not too rare.
- `VolRatio >= 2` filters low-information events.

## Edge Cases and Degradation

### Missing data / outliers handling

- If estimates are missing: use YoY EPS growth surprise proxy or rely on CAR/volume only and lower confidence.
- Separate after-hours vs pre-market timing (gap definition differs).

### Fallback proxies

- If EPS estimate data is unavailable: define “surprise” by `CAR(0,2)` percentile and qualitative guidance summary; mark as lower confidence.

## Backtest Notes (Minimal)

- Event-study backtest with entry at `t+2` close (to avoid immediate noise) and hold 20–60 trading days.
- Include realistic costs (earnings weeks have wider spreads).
- Falsification: if PEAD effect disappears net of costs in the most recent decade for the universe tested.
