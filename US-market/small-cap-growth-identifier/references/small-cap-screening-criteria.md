# Small-Cap Screening Criteria

Detailed thresholds, scoring methodology, and edge cases for small-cap growth stock identification.

## Table of Contents

1. [Universe Definition](#universe-definition)
2. [Quantitative Filters](#quantitative-filters)
3. [Insider Ownership Analysis](#insider-ownership-analysis)
4. [Institutional Ownership Assessment](#institutional-ownership-assessment)
5. [Quality Scoring Model](#quality-scoring-model)
6. [Why Overlooked Framework](#why-overlooked-framework)
7. [Small-Cap Specific Risks](#small-cap-specific-risks)

## Universe Definition

### Market Cap Tiers

| Tier | Range | Characteristics |
|------|-------|----------------|
| Nano-cap | < $50M | Extremely illiquid, high fraud risk — **exclude by default** |
| Micro-cap | $50M–$200M | Low liquidity, limited coverage — include only if user requests |
| Small-cap | $200M–$2B | Target universe — sufficient liquidity, under-covered |

### Liquidity Minimums

| Metric | Minimum Threshold | Preferred |
|--------|-------------------|-----------|
| Average daily volume (shares) | 100K | > 500K |
| Average daily volume (dollars) | $1M | > $5M |
| Bid-ask spread | < 1% | < 0.5% |
| Market makers | ≥ 2 | ≥ 4 |

**Exclude** companies with ADV below minimums — even great fundamentals are useless if positions can't be practically traded.

### Exclude

- SPACs and blank-check companies
- ADRs with limited US trading volume (unless user requests international)
- Companies with pending delisting notices
- Stocks trading below $5 (penny stock territory) unless recently above $5

## Quantitative Filters

### Revenue Growth

**Primary threshold**: > 20% annual revenue growth

| Measurement | How to Apply |
|------------|-------------|
| TTM revenue growth | (TTM Revenue / Prior TTM Revenue) − 1 |
| Latest fiscal year growth | Most recent annual report |
| Two-year CAGR | Smooths out lumpiness |

**Edge cases**:
- **Seasonal businesses**: Use comparable period (YoY quarter, not sequential)
- **Acquisition-driven growth**: Calculate organic growth by excluding acquired revenue; must show >15% organic growth
- **Recent IPO**: May have limited history — 2 quarters of >20% growth is acceptable
- **Base effect**: 20% growth from a $10M base is less meaningful than 20% from a $500M base; note the context

### Operating Margin Trajectory

**Requirement**: Expanding operating margins YoY

| Pattern | Assessment |
|---------|-----------|
| Positive and expanding | ✅ Ideal — scaling business |
| Negative but improving ≥ 500bps YoY | ✅ Acceptable — on path to profitability |
| Positive but flat | ⚠️ Monitor — growth may require continued investment |
| Positive but contracting | ❌ Exclude — deteriorating unit economics |
| Negative and worsening | ❌ Exclude — cash burn accelerating |

### Balance Sheet Strength

| Metric | Threshold | Notes |
|--------|-----------|-------|
| Debt/Equity | < 1.0 | Or net cash position (preferred) |
| Current ratio | > 1.5 | Liquidity buffer |
| Cash runway | > 18 months (if unprofitable) | Based on current burn rate |
| Debt maturity | No significant maturities < 12 months | Refinancing risk |
| Dilution | Shares outstanding growth < 5%/year | Excessive dilution erodes returns |

**Net cash preferred**: For growth small caps, a net cash balance sheet (cash > total debt) is a strong positive signal — removes funding risk as a variable.

## Insider Ownership Analysis

### What Qualifies as "Meaningful"

| Ownership Level | Assessment |
|-----------------|-----------|
| Founder/CEO owns > 20% | Exceptional alignment — eating their own cooking |
| Insider collective > 15% | Strong alignment |
| Insider collective 5–15% | Adequate — meeting the threshold |
| Insider collective < 5% | Does not qualify — insufficient skin in the game |

### What to Check

- **Ownership type**: Direct shares vs. options/RSUs (direct ownership is a stronger signal)
- **Trend**: Are insiders buying or selling on a net basis over the last 12 months?
- **Lockup status**: If post-IPO, are insiders still within lockup or voluntarily holding post-lockup?
- **Voting control**: Dual-class structures — does insider ownership translate to voting power?
- **Pledged shares**: Insiders who have pledged shares as loan collateral are a risk — forced selling if stock drops

### Red Flags

- Founder recently sold > 25% of their position
- Executive team has no direct stock ownership (only options/RSUs)
- Insider selling accelerating while promoting the growth story
- Board members with minimal ownership and no recent purchases

## Institutional Ownership Assessment

### Why Low Institutional Ownership Matters

Low institutional ownership suggests the stock is:
- Not yet on institutional radar (information asymmetry opportunity)
- Below size thresholds for most funds ($2B+ AUM funds often can't own stocks < $500M market cap)
- Under-covered by sell-side analysts (fewer price targets = less efficient pricing)

### Thresholds

| Institutional Ownership | Assessment |
|------------------------|-----------|
| < 20% of float | Very low — highest potential for discovery-driven re-rating |
| 20–35% | Low — still meaningful discovery potential |
| 35–50% | Moderate — some institutional interest, less undiscovered |
| 50–70% | Average — typical for small caps |
| > 70% | High — well-discovered; not a "hidden gem" |

### Supplementary Checks

- **Analyst coverage**: < 5 analysts covering = under-covered; 0 analysts = truly undiscovered
- **Index membership**: Not in major indices = missed by passive flows
- **Recent institutional additions**: Rising institutional ownership from low base = early discovery phase (bullish)
- **Smart money**: Check if quality-focused small-cap funds (well-known boutiques) have recently initiated positions

## Quality Scoring Model

Rank candidates using a composite quality score:

| Factor | Weight | Scoring (0–10) |
|--------|--------|----------------|
| Revenue growth rate | 20% | 20%=4, 25%=5, 30%=6, 40%=8, 50%+=10 |
| Margin trajectory | 15% | Expanding rapidly=10, expanding modestly=7, flat=4, contracting=0 |
| Balance sheet | 15% | Net cash=10, low debt=7, moderate debt=4, high debt=0 |
| Insider ownership | 15% | >20%=10, 15–20%=8, 10–15%=6, 5–10%=4 |
| Low inst. ownership | 10% | <20%=10, 20–35%=7, 35–50%=4, >50%=1 |
| TAM opportunity | 10% | Large + early penetration=10, moderate=6, limited=3 |
| Competitive moat | 10% | Strong=10, moderate=6, weak=3, none=0 |
| Management quality | 5% | Proven founder=10, experienced team=7, unproven=3 |

**Minimum qualifying score**: ≥ 55/100

## "Why Overlooked" Framework

For each qualifying company, explain WHY the market hasn't found it yet using one or more of these reasons:

| Reason | Description | Typical Reversion Trigger |
|--------|-------------|--------------------------|
| **Too small** | Below institutional size thresholds | Market cap growth into fund mandates |
| **No coverage** | Zero or minimal analyst coverage | First analyst initiation |
| **Wrong sector** | Sector is out of favor with growth investors | Sector rotation or company-specific catalyst |
| **Recent IPO/spin-off** | Hasn't built a following yet | Track record establishment (2–3 quarters) |
| **Complexity** | Business model is hard to categorize | Simplified investor messaging |
| **Geography** | Headquartered in overlooked market | Index inclusion, ADR listing |
| **Boring name** | Not a "sexy" industry (e.g., industrial tech, niche SaaS) | Earnings inflection draws attention |
| **Post-selloff** | Got caught in a broad selloff despite differentiated fundamentals | Next earnings beat |

## Small-Cap Specific Risks

Always assess and disclose these risks unique to small caps:

| Risk | What to Check | Severity |
|------|--------------|----------|
| **Liquidity** | Can a meaningful position be entered/exited? | High — can't sell when you need to |
| **Key-person** | Does the thesis depend on one individual? | High — unfixable if they leave |
| **Funding** | Will the company need to raise capital? | High — dilution or death |
| **Customer concentration** | Top 3 customers as % of revenue | Medium-High — single loss is devastating |
| **Competition** | Can a larger player replicate this? | Medium — "gorilla risk" |
| **Governance** | Dual-class shares, related-party transactions | Medium — minority shareholder risk |
| **Reporting quality** | Audit firm quality, restatement history | Medium — trust factor |
| **Index exclusion** | Not in major indices = no passive buying support | Low-Medium — headwind to flows |
