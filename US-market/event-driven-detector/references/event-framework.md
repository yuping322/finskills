# Event-Driven Analysis Framework

Classification, analysis methodology, and risk assessment for corporate events that create investment opportunities.

## Table of Contents

1. [Event Classification](#event-classification)
2. [Merger Arbitrage](#merger-arbitrage)
3. [Spinoffs and Carve-outs](#spinoffs-and-carve-outs)
4. [Share Buyback Analysis](#share-buyback-analysis)
5. [Restructuring and Turnarounds](#restructuring-and-turnarounds)
6. [Index Changes](#index-changes)
7. [Activist Campaigns](#activist-campaigns)
8. [Risk Assessment Matrix](#risk-assessment-matrix)

## Event Classification

### Event Type Spectrum

| Event Type | Typical Spread | Time Horizon | Risk Level | Capital Requirement |
|-----------|---------------|-------------|-----------|-------------------|
| Definitive M&A | 2–8% | 2–6 months | Low-Medium | Medium |
| Preliminary M&A (LOI) | 10–25% | 3–12 months | Medium-High | Medium |
| Hostile / Contested M&A | 15–40% | 3–18 months | High | Medium |
| Spinoff (announced) | Varies | 3–12 months | Medium | Low |
| Spinoff (post-completion) | 10–30% | 6–18 months | Medium | Low |
| Buyback programs | 3–10% annual | 1–3 years | Low | Low |
| Restructuring | 20–50% | 6–24 months | High | Low |
| Index addition | 3–8% | 1–6 weeks | Low-Medium | Low |
| Activist campaign | 15–40% | 6–24 months | Medium-High | Low |

## Merger Arbitrage

### Spread Calculation

**Cash deal**:
```
Gross spread = (Offer price − Current price) / Current price
Annualized spread = Gross spread × (365 / Expected days to close)
```

**Stock deal**:
```
Implied offer = Acquirer price × Exchange ratio
Gross spread = (Implied offer − Target price) / Target price
```

**Cash + Stock**:
```
Implied offer = Cash component + (Acquirer price × Exchange ratio)
```

### Deal Probability Assessment

| Factor | High Probability | Low Probability |
|--------|-----------------|-----------------|
| Regulatory | No antitrust overlap | Significant market concentration |
| Financing | Fully committed financing | Subject to financing condition |
| Shareholder | Board unanimously approved | Significant opposition |
| Strategic fit | Clear synergies | Questionable rationale |
| Precedent | Similar deals approved | Novel regulatory territory |
| Termination fee | > 3% of deal value | < 2% or none |
| MAC clause | Standard | Broad material adverse change provisions |

### Deal Break Downside

Estimate where the target trades if the deal fails:

```
Downside = Current price − Pre-announcement "undisturbed" price
```

Typically 15–40% below current trading price. Consider:
- Pre-announcement trading level (adjust for market moves)
- Standalone value
- Whether other bidders might emerge

### Expected Value Calculation

```
EV = (Deal probability × Upside) + ((1 − Deal probability) × Downside)
```

Only take positions where EV > 0 after transaction costs.

## Spinoffs and Carve-outs

### Why Spinoffs Create Value

1. **Forced selling**: Index funds sell the spinoff if it's too small for the index
2. **Neglect**: Analysts don't cover the new entity initially
3. **Management focus**: Separated businesses can optimize independently
4. **Valuation re-rating**: Hidden divisions valued at conglomerate discount get standalone multiples
5. **Incentive alignment**: New management with equity compensation tied to spun-off entity

### Spinoff Analysis Framework

| Analysis | What to Assess |
|----------|---------------|
| Sum-of-parts | Is the parent trading below sum of segment values? |
| New entity quality | Revenue growth, margins, competitive position |
| Management quality | Track record of new CEO/team |
| Insider ownership | Management equity stake in spinoff |
| Forced selling estimate | Index fund ownership in parent × estimated spinoff allocation |
| Comparable valuation | What are pure-play peers valued at? |
| Capital structure | Is the spinoff being loaded with debt? |

### Historical Spinoff Performance

- Academic studies show spinoffs outperform the market by 10–20% in the first 12–24 months
- Both parent and spinoff tend to outperform
- Smaller spinoffs (< 20% of parent) tend to outperform more (greater neglect effect)
- Performance is strongest 3–12 months after separation

## Share Buyback Analysis

### Signal Strength Assessment

| Factor | Strong Signal | Weak Signal |
|--------|-------------|-------------|
| Buyback size vs market cap | > 5% of outstanding | < 2% |
| Funding source | Operating cash flow | Debt-funded |
| Valuation context | Below intrinsic value | At or above fair value |
| Insider behavior | Insiders also buying | Insiders selling while company buys |
| Execution | Aggressive (ASR, tender) | Slow open-market (may never complete) |
| History | Consistently completes programs | Announces but doesn't execute |

### Buyback Effectiveness Metrics

```
Completion rate = Shares actually repurchased / Shares authorized
```

| Completion Rate | Signal |
|----------------|--------|
| > 80% | Strong commitment |
| 50–80% | Moderate |
| < 50% | Potential "buyback theater" |

```
Net buyback yield = (Buyback spending − Share issuance value) / Market cap
```

A company buying back $1B while issuing $800M in new shares for compensation has only $200M net buyback.

## Restructuring and Turnarounds

### Turnaround Assessment

| Factor | Positive Indicator | Negative Indicator |
|--------|-------------------|-------------------|
| New management | Track record of successful turnarounds | Insider promotion, same culture |
| Balance sheet | Adequate liquidity runway (18+ months) | Near-term debt maturities, covenant risk |
| Cost structure | Identified, quantified savings targets | Vague "efficiency" promises |
| Revenue base | Stable core business | Declining core |
| Asset quality | Valuable assets (brands, IP, real estate) | Mostly goodwill |
| Industry position | Still competitive, defensible niche | Structurally disrupted |

### Turnaround Timeline

Typical phases:
1. **Stabilization** (0–6 months): Stop the bleeding, cut costs, fix liquidity
2. **Foundation** (6–18 months): New strategy, portfolio rationalization
3. **Growth pivot** (18–36 months): Reinvestment in winning businesses
4. **Re-rating** (24–48 months): Market recognizes transformation

Most value accrues to investors who enter during Phase 1–2 and hold through Phase 4.

## Index Changes

### Mechanics

When a stock is added to a major index:
- Index funds must buy shares (proportional to index weight)
- Creates mechanical buying pressure
- Typically 3–5% price impact for S&P 500 additions

When a stock is removed:
- Index funds must sell
- Creates mechanical selling pressure
- Price recovery often occurs over 2–4 weeks post-deletion

### Index Event Timeline

| Index | Announcement | Effective | Typical Lead Time |
|-------|-------------|-----------|-------------------|
| S&P 500 | Variable | Variable | 1–5 trading days |
| Russell 1000/2000 | June (preliminary) | Late June | ~4 weeks |
| MSCI | Quarterly reviews | ~2 weeks after announcement | ~2 weeks |
| Nasdaq 100 | December | December rebalance | ~2 weeks |

### Trading Strategy

- **Additions**: Buy between announcement and effective date; sell on effective date or shortly after
- **Deletions**: Short between announcement and effective date; cover post-effective date
- **Rebalancing**: Front-run anticipated changes based on market cap/liquidity criteria

## Activist Campaigns

### Campaign Type Classification

| Type | Objective | Typical Value Creation |
|------|----------|----------------------|
| Financial engineering | Buybacks, dividends, leverage | 5–15% near-term |
| Operational improvement | Cost cuts, margin expansion | 10–25% over 12–18 months |
| Strategic change | M&A, spinoffs, divestitures | 15–40% over 12–24 months |
| Board change | Governance reform, management change | Variable |

### Activist Success Predictors

| Factor | Higher Success Rate | Lower Success Rate |
|--------|-------------------|-------------------|
| Activist track record | Proven operators (Icahn, Elliott, ValueAct) | Unknown activists |
| Thesis clarity | Specific, quantifiable proposals | Vague "unlock value" |
| Company performance | Clear underperformance vs peers | Company doing reasonably well |
| Board receptivity | Willing to engage | Hostile / entrenched board |
| Stake size | > 5% ownership | < 2% |
| Other shareholder support | ISS/Glass Lewis support | Shareholder opposition |

## Risk Assessment Matrix

### Probability-Impact Grid

| Impact ↓ / Probability → | High (>70%) | Medium (40–70%) | Low (<40%) |
|--------------------------|-------------|-----------------|------------|
| **High impact (>20% move)** | Strong conviction | Attractive if asymmetric | Speculative |
| **Medium (10–20%)** | Core position | Position with stops | Small position |
| **Low (<10%)** | Large position OK | Monitor | Not worth the attention |

### Position Sizing by Event Type

| Event Category | Suggested Position Size | Rationale |
|---------------|------------------------|-----------|
| Definitive M&A | 3–5% of portfolio | Lower risk, lower return |
| Spinoffs | 2–4% | Moderate risk, asymmetric upside |
| Buybacks | Factor into broader thesis | Not standalone position driver |
| Restructuring | 1–3% | Higher risk, higher potential |
| Index changes | 1–2% | Short duration, mechanical |
| Activist situations | 2–4% | Medium risk, timeline uncertainty |
