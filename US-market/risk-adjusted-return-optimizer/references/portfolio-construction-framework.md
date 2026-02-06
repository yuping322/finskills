# Portfolio Construction Framework

Asset allocation models, capital market assumptions, risk metrics, and rebalancing strategies.

## Table of Contents

1. [Risk Profile Definitions](#risk-profile-definitions)
2. [Strategic Asset Allocation Models](#strategic-asset-allocation-models)
3. [Capital Market Assumptions](#capital-market-assumptions)
4. [Position Sizing Rules](#position-sizing-rules)
5. [Risk Metrics Calculation](#risk-metrics-calculation)
6. [Rebalancing Strategies](#rebalancing-strategies)
7. [Downside Protection Toolkit](#downside-protection-toolkit)
8. [Tax Efficiency Considerations](#tax-efficiency-considerations)

## Risk Profile Definitions

### Conservative

- **Investor profile**: Capital preservation priority; limited tolerance for drawdowns; shorter time horizon or near-term income needs
- **Max acceptable drawdown**: -10% to -15%
- **Target volatility**: 6–10% annualized
- **Return expectation**: 4–6% nominal annualized
- **Behavioral note**: Will likely panic and sell if portfolio drops >15%; design for this reality

### Moderate

- **Investor profile**: Balanced growth and preservation; can tolerate temporary losses; 5–15 year horizon
- **Max acceptable drawdown**: -20% to -30%
- **Target volatility**: 10–14% annualized
- **Return expectation**: 6–8% nominal annualized
- **Behavioral note**: May get uncomfortable at -20% but unlikely to sell if properly coached

### Aggressive

- **Investor profile**: Maximum long-term growth; high tolerance for volatility; 10–30+ year horizon
- **Max acceptable drawdown**: -30% to -50%
- **Target volatility**: 14–20% annualized
- **Return expectation**: 8–11% nominal annualized
- **Behavioral note**: Must genuinely be able to hold through a 40%+ drawdown lasting 1–2 years

## Strategic Asset Allocation Models

### Conservative Portfolio

| Asset Class | Allocation | Vehicle Examples |
|------------|-----------|-----------------|
| **US Large Cap** | 15% | VOO, SPY, IVV |
| **US Mid/Small Cap** | 5% | VO, VB, IJR |
| **International Developed** | 7% | VXUS, EFA, IXUS |
| **Emerging Markets** | 3% | VWO, IEMG |
| **US Aggregate Bonds** | 30% | BND, AGG |
| **TIPS** | 10% | TIP, SCHP |
| **Short-Term Treasuries** | 10% | SHV, BIL, SGOV |
| **Investment Grade Corporate** | 5% | LQD, VCIT |
| **REITs** | 5% | VNQ, SCHH |
| **Gold/Commodities** | 3% | GLD, IAU, GLDM |
| **Cash** | 7% | Money market, HYSA |

### Moderate Portfolio

| Asset Class | Allocation | Vehicle Examples |
|------------|-----------|-----------------|
| **US Large Cap** | 25% | VOO, SPY, IVV |
| **US Mid Cap** | 8% | VO, IJH |
| **US Small Cap** | 5% | VB, IJR, AVUV |
| **International Developed** | 12% | VXUS, EFA |
| **Emerging Markets** | 5% | VWO, IEMG |
| **US Aggregate Bonds** | 18% | BND, AGG |
| **TIPS** | 5% | TIP, SCHP |
| **International Bonds** | 5% | BNDX, IAGG |
| **REITs** | 5% | VNQ, SCHH |
| **Gold/Commodities** | 4% | GLD, IAU, DJP |
| **Alternatives** | 3% | Managed futures, market neutral |
| **Cash** | 5% | Money market |

### Aggressive Portfolio

| Asset Class | Allocation | Vehicle Examples |
|------------|-----------|-----------------|
| **US Large Cap** | 30% | VOO, SPY, QQQ |
| **US Mid Cap** | 10% | VO, IJH |
| **US Small Cap** | 10% | VB, IJR, AVUV |
| **International Developed** | 15% | VXUS, EFA, VEA |
| **Emerging Markets** | 8% | VWO, IEMG, AVES |
| **US Aggregate Bonds** | 8% | BND, AGG |
| **TIPS** | 3% | TIP, SCHP |
| **REITs** | 5% | VNQ, SCHH, VNQ |
| **Gold/Commodities** | 4% | GLD, DJP |
| **Alternatives** | 5% | Managed futures, private market access ETFs |
| **Cash** | 2% | Money market |

## Capital Market Assumptions

*Long-term expected returns (10-year forward, nominal, before fees):*

| Asset Class | Expected Return | Expected Volatility | Sharpe Ratio |
|------------|----------------|--------------------|----|
| US Large Cap | 7–9% | 15–17% | 0.35–0.45 |
| US Small Cap | 8–11% | 19–22% | 0.35–0.45 |
| International Developed | 7–9% | 16–18% | 0.35–0.40 |
| Emerging Markets | 8–11% | 20–25% | 0.30–0.40 |
| US Aggregate Bonds | 4–5% | 5–7% | 0.30–0.50 |
| TIPS | 3–4% | 5–7% | 0.20–0.35 |
| High Yield Bonds | 5–7% | 8–12% | 0.35–0.45 |
| REITs | 6–8% | 18–22% | 0.25–0.35 |
| Gold | 3–5% | 15–18% | 0.10–0.20 |
| Commodities | 3–5% | 15–20% | 0.10–0.20 |
| Cash | 3–4% | 0.5% | — |

*These are illustrative assumptions. Adjust based on current market conditions (starting valuations, yield levels, etc.).*

### Correlation Matrix (Simplified)

| | US Equity | Intl Equity | Bonds | REITs | Gold | Commodities |
|---|----------|------------|-------|-------|------|-------------|
| **US Equity** | 1.00 | 0.75 | -0.10 | 0.60 | 0.00 | 0.30 |
| **Intl Equity** | 0.75 | 1.00 | -0.05 | 0.55 | 0.10 | 0.35 |
| **Bonds** | -0.10 | -0.05 | 1.00 | 0.15 | 0.20 | -0.10 |
| **REITs** | 0.60 | 0.55 | 0.15 | 1.00 | 0.05 | 0.20 |
| **Gold** | 0.00 | 0.10 | 0.20 | 0.05 | 1.00 | 0.30 |
| **Commodities** | 0.30 | 0.35 | -0.10 | 0.20 | 0.30 | 1.00 |

*Low or negative correlations provide diversification benefits. Note: correlations tend to increase during crises.*

## Position Sizing Rules

### Core-Satellite Approach

| Component | Allocation | Purpose | Vehicle Type |
|-----------|-----------|---------|-------------|
| **Core** | 60–80% | Market exposure, low cost | Broad index ETFs |
| **Satellite** | 20–40% | Alpha generation, tactical tilts | Sector ETFs, factor ETFs, individual stocks |

### Maximum Position Limits

| Risk Profile | Single Stock Max | Single ETF Max | Sector Max | Geography Max |
|-------------|-----------------|---------------|-----------|--------------|
| Conservative | 2% (if at all) | 15% | 20% | 70% US |
| Moderate | 5% | 20% | 25% | 65% US |
| Aggressive | 8% | 25% | 30% | 55% US |

### Minimum Position Size

- **Practical minimum**: $1,000 per position (below this, transaction costs and rebalancing are impractical)
- **For a $50K portfolio**: Aim for 15–25 positions to balance diversification with manageability
- **For a $10K portfolio**: Simplify to 5–8 positions using broad ETFs only

## Risk Metrics Calculation

### Expected Portfolio Return

```
E(Rp) = Σ (wi × E(Ri))
```
Where wi = weight of asset i, E(Ri) = expected return of asset i.

### Portfolio Volatility

```
σp = √(Σ Σ wi × wj × σi × σj × ρij)
```
Where ρij = correlation between assets i and j.

### Sharpe Ratio

```
Sharpe = (E(Rp) − Rf) / σp
```
Where Rf = risk-free rate (current T-bill yield).

| Sharpe | Assessment |
|--------|-----------|
| > 1.0 | Excellent risk-adjusted returns |
| 0.7–1.0 | Good |
| 0.5–0.7 | Adequate |
| < 0.5 | Suboptimal — reconsider allocation |

### Maximum Drawdown Estimate

Use historical worst-case for the allocation:

| Allocation | Approx Worst Drawdown (historical) |
|-----------|-----------------------------------|
| 30/70 (Conservative) | -15% to -20% |
| 60/40 (Moderate) | -30% to -35% |
| 80/20 (Aggressive) | -45% to -55% |
| 100/0 (All equity) | -50% to -60% |

### Value at Risk (95%, 1-Year)

```
VaR(95%) = Portfolio Value × (E(Rp) − 1.65 × σp)
```

Translate to dollar terms for the specific portfolio size.

## Rebalancing Strategies

### Calendar-Based

| Frequency | Pros | Cons | Best For |
|-----------|------|------|----------|
| Quarterly | Regular discipline | May miss drift | Conservative investors |
| Semi-annual | Lower transaction costs | Less responsive | Moderate, tax-conscious |
| Annual | Minimal costs | Drift can be significant | Simple portfolios |

### Threshold-Based

| Threshold | Trigger | Pros | Cons |
|-----------|---------|------|------|
| 3% absolute | Rebalance when any asset class drifts ≥ 3% from target | Responsive | Frequent trading |
| 5% absolute | Rebalance when any asset class drifts ≥ 5% from target | Balanced | Standard recommendation |
| 25% relative | Rebalance when an asset class deviates ≥ 25% of its target weight | Scale-aware | More complex to monitor |

### Hybrid (Recommended)

- Check allocations quarterly
- Rebalance only positions that have drifted ≥ 5% from target
- Always rebalance after a ≥ 10% market move (up or down)
- Use cash inflows/outflows to rebalance when possible (reduces trading)

### Tax-Aware Rebalancing

- Rebalance using new contributions first
- Direct dividends to underweight positions
- Sell overweight positions with highest cost basis (minimize gains)
- Harvest losses in taxable accounts when rebalancing

## Downside Protection Toolkit

| Strategy | Risk Profile | Implementation | Cost |
|----------|-------------|----------------|------|
| Cash buffer | Conservative | Hold 5–10% in cash/money market | Opportunity cost only |
| Bond ladder | Conservative | Diversified maturity schedule | Low |
| Defensive tilt | All | Overweight staples, healthcare, utilities | Moderate tracking error |
| Dividend focus | Conservative/Moderate | Emphasize dividend aristocrats for income floor | Low |
| Stop-loss rules | Aggressive (satellite only) | Sell satellite positions at -15% to -20% | Potential whipsaw |
| Rebalancing | All | Systematically buy low, sell high | Transaction costs |
| Diversification | All | Low correlation across asset classes | Reduced upside in bull markets |
| Dollar-cost averaging | All (new capital) | Invest fixed amounts on schedule | Psychological cost of "waiting" |

### Stress Test Scenarios

Always present how the portfolio would perform under:

| Scenario | Description | Expected Impact |
|----------|-------------|----------------|
| 2008-style financial crisis | Equities -50%, credit +spreads | Calculate with correlation spike |
| 2020 COVID crash | Sharp -35% and rapid recovery | Assess recovery timeline |
| 2022 rate shock | Bonds -13%, equities -20% | Test 60/40 resilience |
| Stagflation | Rates up, growth down, inflation up | Test inflation protection |
| Goldilocks | Moderate growth, low inflation | Assess upside capture |

## Tax Efficiency Considerations

### Asset Location (Which Account for What)

| Asset | Taxable Account | Tax-Advantaged Account |
|-------|----------------|----------------------|
| US equity index ETFs | ✅ Preferred (low distributions, LTCG) | ✅ Fine |
| International equity | ✅ Preferred (foreign tax credit) | ⚠️ Lose foreign tax credit |
| Taxable bonds | ❌ Avoid (ordinary income) | ✅ Preferred |
| REITs | ❌ Avoid (non-qualified dividends) | ✅ Preferred |
| High-yield bonds | ❌ Avoid (ordinary income) | ✅ Preferred |
| TIPS | ❌ Avoid (phantom income) | ✅ Preferred |
| Growth stocks | ✅ Good (defer gains) | ✅ Fine |
| Dividend stocks | ✅ OK (if qualified) | ✅ Fine |

### Tax-Loss Harvesting

- Monitor positions for unrealized losses ≥ $1,000
- Sell and replace with similar (but not "substantially identical") fund
- Example swaps: VOO → IVV → SPLG (all S&P 500 trackers)
- Observe 30-day wash sale rule
- Harvest losses throughout the year, not just December
