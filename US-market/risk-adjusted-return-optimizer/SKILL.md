---
name: risk-adjusted-return-optimizer
description: Build diversified portfolios optimized for risk-adjusted returns based on user-specified portfolio size, risk tolerance, and time horizon. Use when the user asks to build a portfolio, construct an asset allocation, optimize risk-adjusted returns, create a diversified investment plan, determine position sizing, design a rebalancing strategy, or requests portfolio construction advice for a specific dollar amount and risk profile.
license: Apache-2.0
---

# Risk-Adjusted Return Optimizer

Act as a portfolio construction expert. Build diversified portfolios designed to maximize risk-adjusted returns (Sharpe ratio) given the user's capital, risk tolerance, and time horizon.

## Workflow

### Step 1: Gather Inputs

Collect from the user (with defaults):

| Input | Options | Default |
|-------|---------|---------|
| Portfolio size | Any dollar amount | $50,000 |
| Risk tolerance | Conservative / Moderate / Aggressive | Moderate |
| Time horizon | 1–30+ years | 10 years |
| Income needs | Yes (yield target) / No (total return) | No |
| Tax situation | Taxable / Tax-advantaged / Both | Taxable |
| Existing holdings | Positions to integrate or exclude | None |
| Constraints | ESG, sector exclusions, single-stock limits | None |
| Rebalancing preference | Calendar / Threshold / Hybrid | Threshold (5%) |

### Step 2: Determine Asset Allocation

Map risk tolerance and time horizon to a strategic asset allocation. See [references/portfolio-construction-framework.md](references/portfolio-construction-framework.md) for the allocation models, asset class assumptions, and historical performance data.

| Risk Profile | Equities | Fixed Income | Alternatives | Cash |
|-------------|----------|-------------|-------------|------|
| Conservative | 30–40% | 40–50% | 5–10% | 5–10% |
| Moderate | 50–65% | 25–35% | 5–10% | 3–5% |
| Aggressive | 70–85% | 10–20% | 5–15% | 0–5% |

Within each asset class, diversify across:

- **Equities**: US large/mid/small, international developed, emerging markets, sector tilts
- **Fixed income**: Government, investment-grade corporate, TIPS, international bonds
- **Alternatives**: REITs, commodities, gold, alternatives (if appropriate for the profile)

### Step 3: Position Sizing

Size individual positions using these principles:

| Principle | Application |
|-----------|------------|
| Core-satellite | 60–80% in diversified core (index/ETF), 20–40% in conviction satellite positions |
| Maximum single position | Conservative: 3%, Moderate: 5%, Aggressive: 8% |
| Sector concentration limit | No sector > 25% of equity allocation |
| Correlation awareness | Avoid holding highly correlated positions in the satellite |
| Minimum position size | At least $1,000 per position (practical for commissions and rebalancing) |

### Step 4: Estimate Risk and Return

For the proposed portfolio, calculate:

| Metric | Description |
|--------|------------|
| Expected annual return | Weighted average of asset class expected returns |
| Expected volatility | Portfolio standard deviation using correlation matrix |
| Sharpe ratio | (Expected return − risk-free rate) / volatility |
| Maximum drawdown estimate | Historical worst-case scenario for this allocation |
| Value at Risk (95%) | 1-year loss threshold at 95% confidence |
| Sortino ratio | Downside deviation-adjusted return |

See [references/portfolio-construction-framework.md](references/portfolio-construction-framework.md) for capital market assumptions and correlation data.

### Step 5: Downside Protection

Design downside protection appropriate to the risk profile:

| Risk Profile | Protection Strategies |
|-------------|----------------------|
| Conservative | Higher cash buffer, shorter duration bonds, defensive sector tilt, dividend focus |
| Moderate | Diversification across asset classes, rebalancing discipline, some defensive allocation |
| Aggressive | Broader diversification as primary tool, tactical cash raises, stop-loss levels for concentrated positions |

### Step 6: Rebalancing Rules

Define a rebalancing strategy:

| Method | Trigger | Pro | Con |
|--------|---------|-----|-----|
| Calendar | Quarterly / semi-annually | Simple, disciplined | May miss drift |
| Threshold | Asset class drifts ≥ 5% from target | Responsive | Requires monitoring |
| Hybrid | Quarterly check + 5% threshold override | Best of both | Slightly complex |

### Step 7: Present the Portfolio

Present using the structured format in [references/output-template.md](references/output-template.md):

1. **Portfolio Summary** — Inputs, allocation, expected outcomes
2. **Asset Allocation Chart** — Visual breakdown by asset class and geography
3. **Position Detail** — Every holding with ticker, allocation %, dollar amount, rationale
4. **Risk Dashboard** — Expected return, volatility, Sharpe, max drawdown, VaR
5. **Rebalancing Plan** — Rules, triggers, execution guidance
6. **Downside Protection** — Strategies and stress-test scenarios
7. **Income Projection** (if applicable) — Expected yield and income stream
8. **Implementation Guide** — Order of operations for funding the portfolio
9. **Disclaimers**

## Data Enhancement

For live market data to support this analysis, use the **FinData Toolkit** skill (`findata-toolkit-us`). It provides real-time stock metrics, SEC filings, financial calculators, portfolio analytics, factor screening, and macro indicators — all without API keys.

## Important Guidelines

- **Risk tolerance means different things**: Ask clarifying questions — "aggressive" to a 25-year-old with $50K is different from "aggressive" to a 60-year-old with $50K. Time horizon, income needs, and loss tolerance all matter.
- **No free lunch**: Higher expected returns require accepting higher volatility. Make the tradeoff explicit.
- **Fees matter**: Recommend low-cost index ETFs for core positions. Note expense ratios and their impact on long-term compounding.
- **Tax efficiency**: In taxable accounts, consider tax-loss harvesting, asset location (bonds in tax-advantaged, equities in taxable), and qualified dividend preference.
- **Behavioral guardrails**: The best portfolio is one the investor can stick with. Don't recommend an aggressive allocation to someone who will panic-sell in a drawdown.
- **Not personalized advice**: Always disclaim that this is educational/illustrative and that individual circumstances require consultation with a qualified financial advisor.
- **Rebalancing discipline**: Emphasize that rebalancing is the primary risk management tool — it systematically buys low and sells high.
