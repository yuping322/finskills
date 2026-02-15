# Methodology: Weekly Market Brief Generator (US)

The objective is to **produce a consistent, actionable weekly market brief** that synthesizes performance, macro developments, flows, risks, and watchlist items into a digestible format for portfolio managers and clients. This is not a news summary; it is a **structured analytical framework** that highlights what matters and what to watch.

## Data Definitions

### Sources and field mapping

Weekly brief requires aggregation across multiple data sources:
- **Market performance**: Index returns (SPY, QQQ, IWM, DIA), sector ETF returns (XLK, XLF, XLE, etc.), international indices (EFA, EEM)
- **Volatility**: VIX, MOVE index (bond volatility), currency volatility (DXY)
- **Macro data**: FRED (GDP, CPI, unemployment, Fed Funds rate, 10Y yield, 2Y-10Y spread)
- **Flows**: ETF flows (equity, bond, sector), mutual fund flows, insider buying/selling
- **Breadth**: Advance-decline line, new highs-new lows, % above 50DMA/200DMA
- **Sentiment**: Put/call ratio, AAII sentiment survey, CNN Fear & Greed Index
- **Earnings**: Earnings calendar, beat/miss rates, guidance trends
- **Catalysts**: Upcoming FOMC meetings, economic data releases, geopolitical events

Key fields per section:
- **Performance**: Weekly returns, YTD returns, 52-week high/low distance
- **Macro**: Latest readings, change vs prior week/month, percentile vs 5y history
- **Flows**: Weekly net flows, cumulative monthly flows, flow-to-AUM ratio
- **Risks**: VIX level, credit spreads, liquidity indicators, geopolitical risk index
- **Watchlist**: Stocks/sectors with unusual activity, upcoming catalysts, technical breakouts/breakdowns

### Frequency and windows

- **Weekly**: All sections updated every Friday after market close (or Monday morning)
- **Lookback windows**:
  - Performance: 1 week, 1 month, 3 months, YTD, 1 year
  - Macro: Latest reading, 1-week change, 1-month change, 5-year percentile
  - Flows: 1 week, 4 weeks, 13 weeks cumulative
  - Breadth: Current level, 1-week change, 4-week trend
  - Sentiment: Current level, 4-week moving average, 5-year percentile

## Core Metrics

### Metric list and formulas

1. **Performance Metrics**:
   - `Return_1w = (Price_t / Price_t-5) - 1` (weekly return)
   - `Return_YTD = (Price_t / Price_year_start) - 1`
   - `Distance_from_52w_high = (Price_t / Max_price_252d) - 1`
   - `Relative_strength = Return_asset_1w - Return_benchmark_1w`

2. **Macro Metrics**:
   - `Yield_curve_slope = Yield_10Y - Yield_2Y`
   - `Real_yield_10Y = Yield_10Y - CPI_YoY`
   - `Fed_policy_stance = Fed_Funds_rate - Neutral_rate_estimate` (hawkish if > 0)
   - `Macro_surprise_index = Σ(Actual - Consensus) / Σ|Consensus|` for recent data releases

3. **Flow Metrics**:
   - `Weekly_flow = Net_inflows - Net_outflows` (in $B)
   - `Flow_to_AUM = Weekly_flow / Total_AUM` (in %)
   - `Cumulative_flow_4w = Σ(Weekly_flow)` over past 4 weeks
   - `Flow_momentum = (Flow_4w - Flow_4w_prior) / Flow_4w_prior`

4. **Breadth Metrics**:
   - `AD_line = Cumulative_sum(Advancers - Decliners)`
   - `AD_line_divergence = (AD_line_change_1w - Index_return_1w)` (positive = healthy, negative = warning)
   - `Pct_above_200DMA = Count(Close > MA200) / Total_stocks`
   - `NHNL = New_highs_52w - New_lows_52w`

5. **Sentiment Metrics**:
   - `Put_call_ratio = Put_volume / Call_volume` (> 1 = bearish, < 0.7 = bullish)
   - `AAII_bull_bear_spread = AAII_bullish% - AAII_bearish%` (> 20 = bullish, < -20 = bearish)
   - `Fear_greed_index` (0-100; < 25 = extreme fear, > 75 = extreme greed)

6. **Risk Metrics**:
   - `VIX_percentile = percentile_rank(VIX, VIX_5y_history)`
   - `Credit_spread = BBB_yield - 10Y_Treasury_yield`
   - `Credit_spread_change_1w = Credit_spread_t - Credit_spread_t-5`
   - `Liquidity_stress = (Bid_ask_spread_percentile + Volume_decline_percentile) / 2`

### Standardization

- Use **percentiles** for macro and sentiment indicators (compare to 5-year history)
- Use **z-scores** for flow metrics (identify unusual flow activity)
- Use **basis points (bps)** for yield changes and credit spreads
- Use **percentage points** for performance and breadth metrics
- Express all returns as **total returns** (including dividends)

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

Rule 1 (strong breadth + positive flows → trend continuation):
IF {Pct_above_200DMA >= 60% AND AD_line_divergence >= 0 (no negative divergence) AND Cumulative_flow_4w > 0 (positive flows)}
THEN {Over the next 2-4 weeks, equity indices tend to continue upward trend; pullbacks are shallow (< 3%) and buyable.}
CONFIDENCE {0.60; initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US equity indices (SPY, QQQ, IWM); sector ETFs.}
FAILURE_MODE {Macro shock overrides breadth (FOMC surprise, geopolitical event); flows reverse sharply (risk-off); breadth deteriorates rapidly (sector rotation).}

Rule 2 (weak breadth near highs → correction risk):
IF {Index within 2% of 52-week high AND Pct_above_200DMA <= 40% AND AD_line_divergence < 0 (negative divergence)}
THEN {Over the next 2-6 weeks, correction risk is elevated; expected drawdown >= 5%; defensive positioning recommended.}
CONFIDENCE {0.65; initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US equity indices during late-cycle or topping patterns.}
FAILURE_MODE {Mega-cap leadership continues (narrow rally persists); breadth catches up quickly (sector rotation into laggards); Fed pivots dovish (liquidity injection).}

Rule 3 (extreme sentiment + flow exhaustion → reversal):
IF {Fear_greed_index >= 80 (extreme greed) AND Put_call_ratio <= 0.6 (complacency) AND Flow_momentum < 0 (flows decelerating)}
THEN {Over the next 1-3 weeks, market is vulnerable to reversal; expected pullback >= 3%; reduce exposure or hedge.}
CONFIDENCE {0.55; initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US equity indices during euphoric phases or after strong rallies.}
FAILURE_MODE {Sentiment can stay extreme for weeks (FOMO continues); flows re-accelerate (new catalyst); fundamentals support high valuations (earnings beat).}

Rule 4 (macro surprise + credit spread widening → risk-off):
IF {Macro_surprise_index < -0.5 (negative surprises) AND Credit_spread_change_1w >= 10 bps (widening) AND VIX_percentile >= 70}
THEN {Over the next 1-2 weeks, risk-off sentiment dominates; equities underperform bonds; defensives outperform cyclicals.}
CONFIDENCE {0.70; initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US equities and credit markets during macro uncertainty or growth scares.}
FAILURE_MODE {Fed responds quickly (dovish pivot); macro data revises higher; credit spread widening is technical (supply, not demand).}

### Trigger / exit / invalidation conditions

- **Trigger alert**: When any rule condition is met (breadth divergence, sentiment extreme, flow reversal, credit spread widening)
- **Exit/downgrade**: When conditions normalize (breadth improves, sentiment mean-reverts, flows stabilize, credit spreads tighten)
- **Invalidate**: When data is stale (> 1 week old), when market structure changes (circuit breakers, trading halts), or when major event overrides technicals (war, pandemic)

### Threshold rationale

- **Pct_above_200DMA >= 60%**: Healthy breadth; majority of stocks in uptrends
- **Pct_above_200DMA <= 40%**: Weak breadth; majority of stocks in downtrends or consolidation
- **AD_line_divergence < 0**: Negative divergence; index rising but fewer stocks participating (warning sign)
- **Fear_greed_index >= 80**: Extreme greed; historically precedes pullbacks (contrarian signal)
- **Put_call_ratio <= 0.6**: Complacency; low hedging demand (contrarian signal)
- **Credit_spread_change >= 10 bps**: Material widening; indicates rising credit risk or risk-off sentiment
- **VIX_percentile >= 70**: Elevated volatility; top 30% of historical range (risk-off environment)

## Edge Cases and Degradation

### Missing data / outliers handling

- **Missing macro data**: Use prior week's reading and flag as "no update"
- **Missing flow data**: Use 4-week average and flag as "estimated"
- **Outliers in flows**: Cap extreme values at 99th percentile (e.g., single-day flow > $50B likely data error)
- **Holiday weeks**: Adjust for shortened trading weeks (3-4 days); use daily averages instead of weekly totals
- **Earnings season**: Expect higher volatility and flow activity; adjust thresholds by 20%

### Fallback proxies

- **No breadth data**: Use sector ETF performance dispersion as proxy (high dispersion = weak breadth)
- **No sentiment data**: Use VIX and put/call ratio as combined sentiment proxy
- **No flow data**: Use volume trends (rising volume = inflows, falling volume = outflows) with lower confidence
- **No credit spread data**: Use high-yield ETF (HYG, JNK) performance vs Treasuries as proxy

## Backtest Notes (Minimal)

- **Backtest design**: Generate weekly signals over 5-10 years; test if signals predict next 2-4 week returns
- **Performance metric**: Hit rate (% of signals followed by expected outcome), average return after signal, Sharpe ratio of signal-based strategy
- **Falsification**: Rule fails if hit rate <= 50% or if average return after signal is not significantly different from baseline
- **Sensitivity analysis**: Test different thresholds (breadth 50% vs 60%, sentiment 75 vs 80, credit spread 5 bps vs 10 bps)

## Weekly Brief Structure

### Section 1: Executive Summary (3-5 bullets)

- **Market performance**: Best/worst performers this week (indices, sectors)
- **Key macro development**: Most important macro event or data release
- **Flow/sentiment snapshot**: Are investors buying or selling? Bullish or bearish?
- **Key risk**: Most significant risk to monitor this week
- **Watchlist highlight**: Top 1-2 stocks/sectors to watch next week

### Section 2: Performance Review

**Table: Index Performance**
| Index | 1W | 1M | 3M | YTD | 1Y | Distance from 52W High |
|-------|----|----|----|----|----|-----------------------|
| SPY   | +X%| +X%| +X%| +X%| +X%| -X%                   |
| QQQ   | +X%| +X%| +X%| +X%| +X%| -X%                   |
| IWM   | +X%| +X%| +X%| +X%| +X%| -X%                   |

**Table: Sector Performance (1W)**
| Sector | Return | Relative to SPY | Comment |
|--------|--------|-----------------|---------|
| XLK (Tech) | +X% | +X% | Outperformer; earnings beat |
| XLE (Energy) | -X% | -X% | Underperformer; oil prices down |

**Key observations**:
- Which sectors led/lagged?
- Any unusual moves or reversals?
- Breadth: % above 50DMA, % above 200DMA, AD line trend

### Section 3: Macro Update

**Table: Key Macro Indicators**
| Indicator | Latest | 1W Change | 1M Change | 5Y Percentile | Comment |
|-----------|--------|-----------|-----------|---------------|---------|
| 10Y Yield | X.XX% | +X bps | +X bps | XX% | Rising; hawkish Fed |
| 2Y-10Y Spread | X bps | +X bps | +X bps | XX% | Steepening; growth optimism |
| VIX | XX | +X | +X | XX% | Elevated; risk-off |
| DXY (Dollar) | XX | +X% | +X% | XX% | Strengthening; EM headwind |

**Key observations**:
- What changed this week? (FOMC, CPI, jobs report)
- What's the market pricing in? (Fed path, growth, inflation)
- Any surprises vs consensus?

### Section 4: Flows and Sentiment

**Table: Weekly Flows ($B)**
| Category | 1W Flow | 4W Cumulative | Comment |
|----------|---------|---------------|---------|
| Equity ETFs | +$X | +$X | Strong inflows; risk-on |
| Bond ETFs | -$X | -$X | Outflows; rising yields |
| Sector: Tech | +$X | +$X | Momentum continues |
| Sector: Energy | -$X | -$X | Rotation away |

**Sentiment Snapshot**:
- Put/call ratio: X.XX (bullish/bearish/neutral)
- AAII bull-bear spread: +XX% (bullish/bearish/neutral)
- Fear & Greed Index: XX (extreme fear/fear/neutral/greed/extreme greed)

**Key observations**:
- Are flows confirming price action or diverging?
- Is sentiment extreme (contrarian signal)?
- Any unusual sector rotations?

### Section 5: Risk Monitor

**Current Risk Level**: Low / Moderate / Elevated / High

**Key Risks**:
1. **Credit spreads**: BBB spread = X bps (+X bps this week); widening = caution
2. **Volatility**: VIX = XX (XXth percentile); elevated = risk-off
3. **Liquidity**: Bid-ask spreads widening in small-caps; stress = caution
4. **Geopolitical**: [Event] creates uncertainty; monitor developments

**Risk Dashboard**:
| Risk Factor | Level | Trend | Comment |
|-------------|-------|-------|---------|
| Credit spreads | XX bps | ↑/↓/→ | Widening/tightening/stable |
| VIX | XX | ↑/↓/→ | Elevated/normal/low |
| Liquidity | XX% | ↑/↓/→ | Stress/normal/ample |

### Section 6: Watchlist

**Stocks to Watch Next Week**:
1. **[Ticker]**: Earnings on [Date]; consensus EPS $X.XX; key focus = [guidance/margins/outlook]
2. **[Ticker]**: Technical breakout above $XX; next resistance $XX; catalyst = [product launch/M&A]
3. **[Ticker]**: Unusual flow activity (+$X inflows); potential catalyst = [FDA approval/earnings surprise]

**Sectors to Watch**:
- **Tech (XLK)**: Earnings season continues; watch for guidance on AI spending
- **Financials (XLF)**: Sensitive to yield curve; monitor 2Y-10Y spread
- **Energy (XLE)**: Oil prices at key support; OPEC meeting next week

**Macro Calendar Next Week**:
- **Monday**: [Economic data release]
- **Wednesday**: FOMC minutes / CPI / Jobs report
- **Friday**: [Earnings from major companies]

### Section 7: Bottom Line

**Market outlook**: Bullish / Neutral / Cautious / Bearish

**Key takeaways**:
- What's working? (sectors, styles, factors)
- What's not working? (sectors, styles, factors)
- What to do? (buy dips, take profits, hedge, rotate)

**Positioning recommendations**:
- **Overweight**: [Sectors/styles with positive outlook]
- **Underweight**: [Sectors/styles with negative outlook]
- **Hedge**: [If risk is elevated, suggest hedging strategies]
