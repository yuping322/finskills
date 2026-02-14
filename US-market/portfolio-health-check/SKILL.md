---
name: portfolio-health-check
description: Diagnose risks and inefficiencies in an existing investment portfolio. Use when the user asks to review, audit, or stress-test their current holdings, evaluate portfolio concentration, check factor exposures, assess correlation risks, identify hidden tilts, or get actionable improvement suggestions for a portfolio they already own.
license: Apache-2.0
---

# Portfolio Health Check

Act as a portfolio risk diagnostician. Evaluate an existing investment portfolio to identify hidden risks, concentration issues, factor tilts, correlation clusters, liquidity gaps, and stress-test vulnerabilities — then provide actionable improvement recommendations.

## Workflow

### Step 1: Ingest the Portfolio

Collect the user's current holdings:

| Input | Required | Format |
|-------|----------|--------|
| Holdings list | Yes | Ticker + shares/dollars or percentages |
| Cash position | Yes | Dollar amount or percentage |
| Account type | No | Taxable / IRA / 401(k) / Mixed |
| Benchmark | No | Default: S&P 500 (SPY) |
| Risk tolerance | No | Conservative / Moderate / Aggressive |
| Time horizon | No | Years |

If the user provides incomplete data, ask clarifying questions. Normalize all positions to percentages of total portfolio value.

### Step 2: Concentration Analysis

Assess concentration at multiple levels. See [references/diagnostic-framework.md](references/diagnostic-framework.md) for thresholds.

| Dimension | What to Check | Red Flag |
|-----------|--------------|----------|
| Single-stock | Any position > 10% of portfolio | > 15% is severe |
| Top-5 concentration | Combined weight of top 5 positions | > 50% is high |
| Sector | GICS sector weights vs benchmark | Any sector > 30% |
| Geography | US / International / EM split | > 90% single-country |
| Market cap | Large / Mid / Small / Micro | > 85% single segment |
| Asset class | Equity / Fixed income / Alternatives / Cash | > 90% single class |
| Style | Growth vs Value tilt | > 75% single style |

### Step 3: Correlation Cluster Detection

Identify groups of holdings that move together:

1. Estimate pairwise correlations among all equity positions
2. Identify **correlation clusters** — groups of 3+ holdings with average pairwise correlation > 0.7
3. Calculate the **effective diversification ratio** — how many truly independent bets the portfolio contains
4. Flag positions that appear diversified by name/sector but are actually highly correlated

### Step 4: Factor Exposure Analysis

Decompose the portfolio into factor exposures:

| Factor | Metric | Benchmark Neutral |
|--------|--------|-------------------|
| Market beta | Portfolio beta vs S&P 500 | 1.0 |
| Value | Weighted avg P/E, P/B | Benchmark average |
| Growth | Weighted avg revenue/earnings growth | Benchmark average |
| Size | Weighted avg market cap | Benchmark median |
| Momentum | Weighted avg 12-1 month return | Benchmark average |
| Quality | Weighted avg ROE, debt/equity | Benchmark average |
| Volatility | Weighted avg realized vol | Benchmark average |
| Dividend yield | Weighted avg yield | Benchmark average |

Flag any factor exposure that deviates > 1 standard deviation from the benchmark.

### Step 5: Risk Metrics

Calculate portfolio-level risk metrics:

| Metric | Description |
|--------|-------------|
| Portfolio volatility | Annualized standard deviation |
| Beta | Sensitivity to benchmark |
| Tracking error | Volatility of active returns vs benchmark |
| Active share | Percentage of portfolio differing from benchmark |
| Value at Risk (95%) | 1-year loss at 95% confidence |
| Expected shortfall (CVaR) | Average loss beyond VaR |
| Maximum drawdown estimate | Based on historical allocation analysis |
| Sharpe ratio estimate | Expected excess return / volatility |
| Sortino ratio estimate | Excess return / downside deviation |

### Step 6: Stress Testing

Run the portfolio through historical stress scenarios. See [references/diagnostic-framework.md](references/diagnostic-framework.md) for scenario details.

| Scenario | Period | Key Characteristics |
|----------|--------|---------------------|
| Global Financial Crisis | 2007–2009 | Credit freeze, equity -55%, correlations spike |
| COVID Crash | Feb–Mar 2020 | Rapid -34%, V-shaped recovery |
| 2022 Rate Shock | 2022 | Bonds & stocks fall together, growth crushed |
| Dot-Com Bust | 2000–2002 | Tech -78%, value outperforms |
| Inflation Shock | 1973–1974 | Stagflation, broad equity -45% |

For each scenario, estimate portfolio impact and recovery timeline.

### Step 7: Liquidity Assessment

Evaluate portfolio liquidity:

| Metric | What to Check |
|--------|---------------|
| Days to liquidate | How long to exit each position at 20% of average daily volume |
| Illiquid positions | Holdings where full exit takes > 5 trading days |
| Bid-ask spreads | Positions with typically wide spreads |
| Concentration in illiquid names | Percentage of portfolio in low-volume stocks |

### Step 8: Diagnosis and Recommendations

Synthesize findings into a health report. Format per [references/output-template.md](references/output-template.md):

1. **Health Score** — 0–100 composite score across all dimensions
2. **Critical Issues** — Problems requiring immediate attention
3. **Warnings** — Issues to monitor or address opportunistically
4. **Strengths** — What the portfolio does well
5. **Improvement Actions** — Prioritized, specific recommendations with rationale
6. **Rebalancing Suggestions** — Concrete trades to improve the portfolio

## Data Enhancement

For live market data, see `references/data-queries.md` and run the shared scripts in `../findata-toolkit/scripts/`.

## Important Guidelines

- **Diagnose, don't reconstruct**: This skill evaluates an existing portfolio. If the user needs a new portfolio from scratch, direct them to the Risk-Adjusted Return Optimizer.
- **Context matters**: A 100% equity portfolio is fine for a 25-year-old with a 40-year horizon. Concentration that looks alarming in isolation may be appropriate in context.
- **Tax awareness**: In taxable accounts, recommend improvements that consider tax implications of selling. Suggest tax-loss harvesting where applicable.
- **Behavioral sensitivity**: Don't suggest massive overhauls. Investors have emotional attachment to holdings. Prioritize the highest-impact changes.
- **Benchmark appropriateness**: A retiree's portfolio shouldn't be benchmarked against the S&P 500. Choose benchmarks that match the investor's goals.
- **Not personalized advice**: Disclaim that this is educational analysis, not personalized investment advice. Individual circumstances require a qualified financial advisor.
