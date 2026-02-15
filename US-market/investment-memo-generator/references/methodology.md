# Methodology: Investment Memo Generator (US)

The objective is to **produce a structured, institutional-quality investment memo** that synthesizes thesis, valuation, catalysts, risks, and monitoring into a reusable decision document. This is not a marketing pitch; it is a **rigorous analytical framework** that supports investment committee review and ongoing portfolio management.

## Data Definitions

### Sources and field mapping

Investment memo requires comprehensive data aggregation:
- **Company fundamentals**: SEC EDGAR 10-K/10-Q (revenue, earnings, cash flow, balance sheet, segment data)
- **Valuation data**: Price, shares outstanding, market cap, enterprise value (yfinance + manual calculation)
- **Peer comparison**: Industry peers (GICS classification), peer multiples (P/E, EV/EBITDA, P/B, FCF yield)
- **Historical performance**: 1y/3y/5y stock returns, volatility, beta, max drawdown
- **Analyst data**: Consensus estimates (EPS, revenue), price targets, ratings (if available)
- **Macro context**: Relevant macro indicators (GDP growth, interest rates, sector trends) from FRED
- **Catalyst calendar**: Earnings dates, product launches, regulatory decisions, M&A rumors (manual input or calendar scraping)

Key fields per section:
- **Thesis**: Business model, competitive advantage, growth drivers, market position
- **Valuation**: Current multiples, historical range, peer comparison, DCF/DDM assumptions
- **Catalysts**: Upcoming events, expected timing, probability, potential impact
- **Risks**: Downside scenarios, probability, mitigation strategies
- **Monitoring**: Key metrics to track, trigger points for re-evaluation

### Frequency and windows

- **Quarterly**: Update fundamentals after earnings release
- **Monthly**: Update price, valuation multiples, peer comparison
- **Weekly**: Update catalyst calendar and risk factors
- **Event-driven**: Update immediately after major announcements (M&A, regulatory, management changes)

Suggested windows:
- Historical performance: 1y / 3y / 5y
- Valuation comparison: Current vs 5y historical range
- Peer comparison: Current quarter vs trailing 12 months
- Catalyst horizon: Next 6-12 months

## Core Metrics

### Metric list and formulas

1. **Valuation Metrics**:
   - `P/E = Price / EPS_ttm` (trailing twelve months)
   - `Forward_P/E = Price / EPS_consensus_next_year`
   - `P/B = Market_cap / Book_value`
   - `EV/EBITDA = (Market_cap + Net_debt) / EBITDA_ttm`
   - `FCF_yield = FCF_ttm / Market_cap`
   - `Dividend_yield = Annual_dividend / Price`

2. **Relative Valuation**:
   - `P/E_percentile = percentile_rank(P/E, Historical_5y_P/E)`
   - `Peer_P/E_discount = (Stock_P/E - Peer_median_P/E) / Peer_median_P/E`
   - `PEG_ratio = P/E / EPS_growth_rate` (< 1 = undervalued relative to growth)

3. **Quality Metrics**:
   - `ROE = Net_income / Shareholders_equity`
   - `ROA = Net_income / Total_assets`
   - `ROIC = NOPAT / Invested_capital`
   - `Debt/Equity = Total_debt / Shareholders_equity`
   - `Interest_coverage = EBIT / Interest_expense`
   - `FCF_conversion = FCF / Net_income` (> 1 = high quality earnings)

4. **Growth Metrics**:
   - `Revenue_CAGR_3y = (Revenue_current / Revenue_3y_ago)^(1/3) - 1`
   - `EPS_CAGR_3y = (EPS_current / EPS_3y_ago)^(1/3) - 1`
   - `Consensus_EPS_growth = (EPS_next_year / EPS_current) - 1`

5. **Risk Metrics**:
   - `Beta_60m = Cov(Stock_returns, Market_returns) / Var(Market_returns)` over 60 months
   - `Volatility_252d = Std_dev(Daily_returns) * sqrt(252)` (annualized)
   - `Max_drawdown_252d = max(Peak_to_trough_decline)` over 1 year
   - `Sharpe_ratio_252d = (Annualized_return - Risk_free_rate) / Volatility_252d`

6. **Catalyst Scoring**:
   - `Catalyst_impact = Probability * Expected_price_move`
   - Example: FDA approval (60% probability, +30% price move) → impact = 18%
   - `Total_catalyst_score = Σ(Catalyst_impact_i)` for all catalysts in next 6 months

### Standardization

- Use **sector-relative percentiles** for valuation (avoid comparing tech to utilities)
- Use **market-wide percentiles** for risk metrics (beta, volatility)
- Use **z-scores** for outlier detection (flag if any metric > 3 std dev from sector mean)
- Express all growth rates as **CAGR** for comparability across time periods
- Express all returns as **annualized** for consistency

## Signals and Thresholds

### Insight Rules (Testable Hypotheses)

Rule 1 (undervalued quality + catalyst → outperformance):
IF {P/E_percentile <= 30 (cheap vs history) AND Peer_P/E_discount <= -20% (cheap vs peers) AND ROE >= 15% (high quality) AND Total_catalyst_score >= 15%}
THEN {Over the next 6-12 months, stock tends to outperform sector by >= 10% as valuation gap closes and catalysts materialize.}
CONFIDENCE {0.65; initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US large/mid-cap equities with analyst coverage and identifiable catalysts.}
FAILURE_MODE {Catalysts disappoint or delay; quality deteriorates (earnings miss, margin compression); sector rotation away from stock; macro shock overrides fundamentals.}

Rule 2 (high growth + reasonable valuation → sustained outperformance):
IF {EPS_CAGR_3y >= 20% AND PEG_ratio <= 1.5 AND ROIC >= 15% (capital-efficient growth)}
THEN {Over the next 12-24 months, stock tends to deliver >= 15% annualized returns as growth compounds and multiple expands.}
CONFIDENCE {0.60; initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US growth stocks (tech, healthcare, consumer discretionary) with sustainable competitive advantages.}
FAILURE_MODE {Growth decelerates (market saturation, competition); multiple contracts (rate hikes, risk-off); capital efficiency declines (margin pressure, capex surge).}

Rule 3 (value trap detection → avoid):
IF {P/E_percentile <= 20 (very cheap) AND ROE <= 10% (poor quality) AND EPS_CAGR_3y <= 0% (no growth) AND Debt/Equity >= 1.5 (high leverage)}
THEN {Stock is likely a value trap; over the next 12 months, returns tend to be negative or underperform sector by >= 10%.}
CONFIDENCE {0.70; initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US equities across all market caps; strongest signal for cyclicals and financials with deteriorating fundamentals.}
FAILURE_MODE {Turnaround catalyst emerges (new management, asset sale, restructuring); sector-wide revaluation lifts all boats; activist investor involvement; debt restructuring succeeds.}

Rule 4 (high-risk, high-reward binary event → size appropriately):
IF {Total_catalyst_score >= 30% (major binary event) AND Volatility_252d >= 40% (high risk) AND Market_cap <= $5B (small/mid-cap)}
THEN {Position size should be <= 2% of portfolio; expected return is high but tail risk is significant; use options for asymmetric payoff.}
CONFIDENCE {0.75; initial estimate; requires historical validation}
APPLICABLE_UNIVERSE {US small/mid-cap equities with binary catalysts (biotech FDA approvals, tech product launches, M&A targets).}
FAILURE_MODE {Catalyst succeeds but stock doesn't move (already priced in); volatility underestimates true risk (liquidity crisis, fraud); options are mispriced (IV too high).}

### Trigger / exit / invalidation conditions

- **Trigger investment**: When composite score (valuation + quality + growth + catalyst) is compelling and risk is acceptable
- **Exit/sell**: When:
  - Valuation reaches target (P/E >= 75th percentile or peer premium >= 20%)
  - Thesis breaks (quality deteriorates, growth stalls, catalyst fails)
  - Risk escalates (leverage spikes, liquidity dries up, fraud/governance issues)
  - Better opportunity emerges (opportunity cost)
  
- **Invalidate memo**: When:
  - Fundamental data is stale (> 6 months old)
  - Major corporate action (M&A, spin-off, bankruptcy)
  - Sector classification changes materially
  - Analyst coverage drops (no consensus estimates)

### Threshold rationale

- **P/E_percentile <= 30**: Bottom tercile of historical range; indicates potential undervaluation
- **Peer_P/E_discount <= -20%**: Significant discount to peers; suggests market is overly pessimistic or missing something
- **ROE >= 15%**: Above-average profitability; indicates competitive advantage
- **PEG_ratio <= 1.5**: Growth at reasonable price; < 1 is ideal, < 1.5 is acceptable
- **Total_catalyst_score >= 15%**: Material upside potential from identifiable events
- **Position size <= 2%**: Risk management for high-volatility, binary-event stocks

## Edge Cases and Degradation

### Missing data / outliers handling

- **Missing fundamentals**: If 10-K/10-Q data is unavailable, use trailing 12-month estimates or peer averages with confidence penalty
- **Missing analyst estimates**: Skip forward P/E and PEG ratio; rely on trailing metrics
- **Negative earnings**: Use EV/Sales, P/B, or DCF instead of P/E; flag as "not meaningful"
- **Outliers**: Cap extreme values at 99th percentile (e.g., P/E > 100, Debt/Equity > 5) to avoid distortion
- **Recent IPO (< 1 year)**: Insufficient history for percentile calculations; use peer comparison only and flag as "limited history"

### Fallback proxies

- **No peer data**: Use sector ETF multiples as proxy with lower confidence
- **No catalyst calendar**: Set catalyst score = 0 (neutral) and rely on valuation + quality
- **No historical data**: Use market-wide percentiles instead of stock-specific; flag as "no history"
- **Illiquid stocks**: If ADV < $1M, add liquidity risk warning and suggest smaller position size (< 1%)

## Backtest Notes (Minimal)

- **Backtest design**: Build investment memos for all stocks in universe at end of each quarter; rank by composite score; hold top quintile for 1 quarter, rebalance quarterly
- **Performance metric**: Compare Sharpe ratio, alpha, and max drawdown vs sector benchmark (SPY, sector ETFs)
- **Falsification**: Rule fails if top quintile does not outperform bottom quintile by >= 5% annualized over 5-year sample
- **Sensitivity analysis**: Test different weight combinations (valuation-heavy, growth-heavy, catalyst-heavy) to identify robust configurations
- **Transaction costs**: Assume 20 bps per trade; if turnover > 100% annually, net alpha may be negative

## Investment Memo Structure

### Section 1: Executive Summary (3-5 bullets)

- **Thesis in one sentence**: What is the investment case?
- **Valuation**: Current vs historical vs peers (cheap/fair/expensive)
- **Key catalyst**: Most important upcoming event and expected impact
- **Key risk**: Most significant downside scenario
- **Recommendation**: Buy/Hold/Sell with target price and time horizon

### Section 2: Business Overview

- **Business model**: How does the company make money?
- **Competitive position**: Market share, competitive advantages, moats
- **Industry dynamics**: Growth drivers, headwinds, competitive intensity
- **Management quality**: Track record, capital allocation, governance

### Section 3: Financial Analysis

- **Historical performance**: Revenue, earnings, margins, ROIC over 3-5 years
- **Quality assessment**: ROE, FCF conversion, balance sheet strength
- **Growth trajectory**: Historical CAGR, consensus estimates, sustainability

### Section 4: Valuation

- **Current multiples**: P/E, EV/EBITDA, P/B, FCF yield
- **Historical comparison**: Current vs 5y range (percentile)
- **Peer comparison**: Discount/premium vs sector median
- **Intrinsic value estimate**: DCF, DDM, or sum-of-parts (if applicable)
- **Target price**: 12-month price target with upside/downside

### Section 5: Catalysts

- **Near-term (0-6 months)**: Earnings, product launches, regulatory decisions
- **Medium-term (6-12 months)**: Strategic initiatives, M&A, market expansion
- **Probability and impact**: For each catalyst, estimate probability and expected price move
- **Total catalyst score**: Sum of probability-weighted impacts

### Section 6: Risks

- **Downside scenarios**: What could go wrong? (earnings miss, competition, regulation, macro)
- **Probability and impact**: For each risk, estimate probability and expected price move
- **Mitigation strategies**: How to reduce risk? (hedging, position sizing, stop-loss)
- **Downside target**: Worst-case price target with probability

### Section 7: Monitoring Checklist

- **Key metrics to track**: Revenue growth, margins, FCF, leverage, market share
- **Trigger points for re-evaluation**: What would change the thesis? (earnings miss, catalyst failure, leverage spike)
- **Update frequency**: Quarterly (earnings), monthly (price/valuation), event-driven (catalysts)

### Section 8: Conclusion and Recommendation

- **Investment decision**: Buy/Hold/Sell
- **Position size**: % of portfolio (based on conviction and risk)
- **Time horizon**: Expected holding period (6 months, 1 year, 2+ years)
- **Exit strategy**: When to sell? (target price, thesis break, time stop)
