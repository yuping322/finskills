# Portfolio Diagnostic Framework

Detailed thresholds, scoring methodology, stress-test parameters, and factor analysis for portfolio health assessment.

## Table of Contents

1. [Concentration Thresholds](#concentration-thresholds)
2. [Correlation Analysis](#correlation-analysis)
3. [Factor Exposure Framework](#factor-exposure-framework)
4. [Health Score Model](#health-score-model)
5. [Stress Test Scenarios](#stress-test-scenarios)
6. [Liquidity Assessment](#liquidity-assessment)
7. [Common Portfolio Pathologies](#common-portfolio-pathologies)

## Concentration Thresholds

### Single-Stock Concentration

| Weight | Severity | Recommendation |
|--------|----------|----------------|
| < 5% | Safe | No action needed |
| 5–10% | Monitor | Acceptable if high-conviction position with thesis |
| 10–15% | Warning | Consider trimming; document rationale if holding |
| 15–25% | High risk | Strongly recommend reducing; tax-lot optimization |
| > 25% | Critical | Significant idiosyncratic risk; immediate attention |

### Sector Concentration

| Sector Weight vs Benchmark | Severity |
|---------------------------|----------|
| Within ±5% | Neutral |
| ±5–10% | Mild tilt — acceptable if intentional |
| ±10–20% | Significant overweight/underweight |
| > ±20% | Extreme concentration — flag as critical |

### Top-N Concentration

| Top-N Weight | Assessment |
|-------------|------------|
| Top 5 < 30% | Well-diversified |
| Top 5: 30–50% | Moderately concentrated |
| Top 5: 50–70% | Concentrated — flag |
| Top 5 > 70% | Highly concentrated — critical |
| HHI > 0.15 | Concentrated by Herfindahl index |

### Asset Class Minimums (by Risk Profile)

| Asset Class | Conservative | Moderate | Aggressive |
|-------------|-------------|----------|------------|
| Equities | 25–40% | 45–65% | 65–85% |
| Fixed income | 35–55% | 20–35% | 5–20% |
| Alternatives | 0–10% | 5–15% | 5–20% |
| Cash | 5–15% | 2–8% | 0–5% |

## Correlation Analysis

### Cluster Detection Method

1. Compute trailing 3-year weekly return correlations for all equity pairs
2. Apply hierarchical clustering (average linkage) with correlation distance
3. Define a cluster as ≥ 3 positions with average pairwise correlation > 0.70
4. Calculate cluster weight = sum of all positions in the cluster

### Correlation Risk Levels

| Cluster Weight | Risk Level |
|---------------|------------|
| < 15% | Low — normal sector/factor overlap |
| 15–30% | Moderate — some diversification benefit lost |
| 30–50% | High — significant hidden concentration |
| > 50% | Critical — portfolio dominated by one risk driver |

### Effective Diversification Ratio

```
EDR = (sum of individual volatilities) / portfolio volatility
```

| EDR | Interpretation |
|-----|---------------|
| > 1.5 | Good diversification benefit |
| 1.2–1.5 | Moderate diversification |
| 1.0–1.2 | Weak diversification — holdings move together |
| ~1.0 | Virtually no diversification benefit |

## Factor Exposure Framework

### Factor Definitions

| Factor | Metric | Overexposed If |
|--------|--------|----------------|
| Market (beta) | Portfolio beta | > 1.3 or < 0.7 vs target |
| Value | Weighted P/E, P/B | P/E < 12 or > 30 (extremes) |
| Growth | Revenue growth rate | > 25% weighted avg (aggressive growth tilt) |
| Size | Weighted avg market cap | < $10B avg (small-cap heavy) |
| Momentum | 12-1 month return | Strongly skewed to recent winners |
| Quality | ROE, debt/equity | Low ROE or high leverage vs benchmark |
| Low volatility | Realized vol | All positions below-average vol (defensive clustering) |
| Yield | Dividend yield | > 3.5% avg (income-heavy tilt) |

### Factor Tilt Scoring

For each factor, compute the portfolio's z-score vs the benchmark:

| Z-Score | Tilt Assessment |
|---------|----------------|
| -0.5 to +0.5 | Neutral |
| ±0.5 to ±1.0 | Mild tilt — likely intentional |
| ±1.0 to ±2.0 | Significant tilt — should be intentional |
| > ±2.0 | Extreme tilt — flag for review |

## Health Score Model

### Scoring Components (0–100 total)

| Component | Weight | Scoring |
|-----------|--------|---------|
| Diversification | 25 | HHI-based; low concentration = high score |
| Correlation efficiency | 15 | EDR-based; high EDR = high score |
| Factor balance | 15 | Average absolute z-score across factors; low = high score |
| Risk-return efficiency | 15 | Sharpe/Sortino vs achievable frontier |
| Liquidity | 10 | % that can liquidate within 1 day at 20% ADV |
| Stress resilience | 10 | Average drawdown across stress scenarios vs pure benchmark |
| Cost efficiency | 10 | Weighted expense ratios (if ETFs/funds) vs alternatives |

### Health Score Interpretation

| Score | Rating | Interpretation |
|-------|--------|---------------|
| 85–100 | Excellent | Well-constructed, few improvements needed |
| 70–84 | Good | Solid portfolio, some optimization opportunities |
| 55–69 | Fair | Notable issues; targeted improvements recommended |
| 40–54 | Needs attention | Multiple risk factors; significant rebalancing advised |
| < 40 | Poor | Critical issues; major restructuring recommended |

## Stress Test Scenarios

### Global Financial Crisis (2007–2009)

| Asset Class | Approximate Drawdown |
|-------------|---------------------|
| US Large Cap | -55% |
| US Small Cap | -58% |
| International Developed | -57% |
| Emerging Markets | -62% |
| US Aggregate Bond | +7% |
| US Treasuries (Long) | +25% |
| Corporate High Yield | -33% |
| REITs | -68% |
| Gold | +12% |
| Commodities | -55% |

**Key characteristic**: Correlation spike — everything except treasuries and gold dropped together.

### COVID Crash (Feb–Mar 2020)

| Asset Class | Drawdown | Recovery Time |
|-------------|----------|--------------|
| US Large Cap | -34% | 5 months |
| US Small Cap | -41% | 8 months |
| International | -34% | 12+ months |
| Bonds (Agg) | -6% | 2 months |
| High Yield | -20% | 5 months |
| REITs | -42% | 14 months |
| Gold | -12% (brief) | 1 month |

**Key characteristic**: Extreme speed of decline; rapid recovery.

### 2022 Rate Shock

| Asset Class | Annual Return |
|-------------|-------------|
| US Large Cap (S&P 500) | -18% |
| US Growth (Nasdaq) | -33% |
| US Value | -5% |
| US Aggregate Bond | -13% |
| Long Treasuries (TLT) | -31% |
| REITs | -26% |
| Gold | 0% |
| Commodities | +16% |

**Key characteristic**: Bonds and stocks fell together. Traditional 60/40 failed. Commodity/value were only shelters.

### Dot-Com Bust (2000–2002)

| Asset Class | Cumulative Return |
|-------------|-------------------|
| Nasdaq | -78% |
| S&P 500 | -49% |
| US Value | -10% |
| US Small Value | +30% |
| US Bonds | +30% |
| REITs | +35% |
| Gold | +12% |

**Key characteristic**: Growth/tech concentration devastating. Value, bonds, and REITs provided genuine protection.

### Stagflation (1973–1974)

| Asset Class | Approximate Impact |
|-------------|-------------------|
| US Equities | -45% |
| US Bonds | -10% |
| Gold | +65% |
| Real estate | Positive |
| Cash (T-bills) | +8% (but negative real) |

**Key characteristic**: Both stocks and bonds declined in real terms. Only real assets protected.

## Liquidity Assessment

### Days to Liquidate Calculation

```
Days to liquidate = Position value / (Average daily volume × assumed participation rate)
```

Default participation rate: 20% of ADV (conservative institutional assumption).

### Liquidity Categories

| Days to Liquidate | Category | Flag |
|-------------------|----------|------|
| < 1 day | Highly liquid | None |
| 1–3 days | Liquid | None |
| 3–5 days | Moderately liquid | Monitor |
| 5–10 days | Low liquidity | Warning |
| > 10 days | Illiquid | Critical |

### Portfolio-Level Liquidity Score

```
Liquidity score = Σ (position weight × liquidity category score)
```

Where: Highly liquid = 100, Liquid = 80, Moderate = 50, Low = 20, Illiquid = 0.

## Common Portfolio Pathologies

| Pathology | Symptoms | Common Cause |
|-----------|----------|--------------|
| **Employer stock syndrome** | Single stock > 20% | Company stock from compensation |
| **Home bias** | > 90% domestic, 0% international | Familiarity bias |
| **Recency bias tilt** | Overweight recent winners | Chasing performance |
| **Closet indexing** | Active share < 20% with high fees | Paying active fees for index-like returns |
| **Dividend trap** | Overweight high yield, ignoring growth | Income focus without total return view |
| **Zombie positions** | Many tiny positions (< 1%) | Accumulated over years, never cleaned up |
| **Correlation clustering** | 60%+ portfolio in correlated names | Sector/style concentration not recognized |
| **Duration mismatch** | Long-duration bonds with short horizon | Not matching bond duration to time horizon |
| **Fee drag** | Weighted ER > 0.50% with index alternatives | Legacy funds or advisor-selected products |
| **Tax inefficiency** | Bonds in taxable, equities in IRA | Suboptimal asset location |
