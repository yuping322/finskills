# Tech Valuation Framework

Quantitative model for comparing tech stock valuations against fundamentals to identify mispricings.

## Table of Contents

1. [Growth-Adjusted Valuation Model](#growth-adjusted-valuation-model)
2. [Profitability Assessment](#profitability-assessment)
3. [Capital Efficiency Metrics](#capital-efficiency-metrics)
4. [SaaS-Specific Metrics](#saas-specific-metrics)
5. [Mispricing Identification](#mispricing-identification)
6. [Common Valuation Pitfalls in Tech](#common-valuation-pitfalls-in-tech)

## Growth-Adjusted Valuation Model

### Core Principle

A tech stock's valuation multiple should be proportional to its growth rate, profitability, and durability of growth. Compare actual valuation to "justified" valuation.

### PEG-Based Screening

```
PEG Ratio = Forward P/E / Expected EPS Growth Rate (%)
```

| PEG Range | Assessment |
|-----------|-----------|
| < 0.8 | Potentially undervalued — growth not fully priced |
| 0.8–1.2 | Fairly valued — growth roughly matches multiple |
| 1.2–2.0 | Growth premium — justified only with high-quality growth |
| > 2.0 | Potentially overvalued — multiple assumes unrealistic growth |

### Revenue Multiple Framework (P/S or EV/Revenue)

For pre-profit or early-profit tech companies, P/E is less useful. Use EV/Revenue benchmarks:

| Revenue Growth | Gross Margin > 70% | Gross Margin 50–70% | Gross Margin < 50% |
|---------------|-------------------|--------------------|--------------------|
| > 40% | 15–25x justified | 10–18x justified | 6–12x justified |
| 25–40% | 10–18x justified | 7–12x justified | 4–8x justified |
| 15–25% | 6–12x justified | 4–8x justified | 2–5x justified |
| < 15% | 3–7x justified | 2–5x justified | 1–3x justified |

*These are illustrative ranges based on historical SaaS/tech multiples. Adjust for market regime (bull vs. bear).*

### Rule of 40 (SaaS)

```
Rule of 40 Score = Revenue Growth (%) + FCF Margin (%)
```

| Score | Assessment |
|-------|-----------|
| > 60 | Elite — commands premium multiples |
| 40–60 | Strong — above the threshold |
| 25–40 | Below threshold — multiple compression risk |
| < 25 | Weak — likely value trap or turnaround situation |

## Profitability Assessment

### Margin Stack Analysis

Evaluate the full margin waterfall:

| Margin | What It Reveals | Tech Benchmarks |
|--------|----------------|----------------|
| Gross margin | Unit economics, pricing power | Elite: >75%, Good: 60–75%, Weak: <50% |
| Operating margin | Operational leverage, SG&A efficiency | Mature: >25%, Scaling: 10–25%, Investing: <10% |
| Net margin | After-tax profitability | Varies widely; assess trend over level |
| FCF margin | Cash generation ability | Elite: >25%, Good: 15–25%, Adequate: 5–15% |

### Operating Leverage Test

The key question: **Are margins expanding as revenue grows?**

```
Operating Leverage = Change in Operating Income (%) / Change in Revenue (%)
```

| Leverage | Interpretation |
|----------|---------------|
| > 1.5x | Strong leverage — revenue growth is accelerating profits |
| 1.0–1.5x | Moderate leverage — profits growing with revenue |
| < 1.0x | Weak leverage — spending growing faster than revenue |
| Negative | Deteriorating — red flag unless explained by strategic investment |

### SBC (Stock-Based Compensation) Adjustment

Many tech companies show "adjusted profitability" excluding SBC. Always check:

```
SBC-Adjusted Operating Margin = (Operating Income − SBC) / Revenue
```

| SBC as % of Revenue | Concern Level |
|---------------------|--------------|
| < 5% | Minimal dilution impact |
| 5–10% | Moderate — typical for growth tech |
| 10–20% | Elevated — significant shareholder dilution |
| > 20% | Excessive — GAAP profitability illusory |

## Capital Efficiency Metrics

| Metric | Formula | What It Shows |
|--------|---------|--------------|
| ROIC | NOPAT / Invested Capital | Returns on deployed capital |
| ROE | Net Income / Shareholders' Equity | Returns on equity |
| Revenue per employee | Revenue / Employees | Operational efficiency |
| R&D efficiency | Revenue Growth / R&D Spend | Innovation ROI |
| CAC payback (SaaS) | CAC / (ARPU × Gross Margin) | Sales efficiency |
| Magic number (SaaS) | Net New ARR / Prior Quarter S&M Spend | Go-to-market efficiency |

### Capital Efficiency Benchmarks

| Metric | Elite | Good | Below Average |
|--------|-------|------|---------------|
| ROIC | > 25% | 15–25% | < 15% |
| Revenue / Employee | > $500K | $250–500K | < $250K |
| Magic Number | > 1.0x | 0.5–1.0x | < 0.5x |
| LTV/CAC | > 5x | 3–5x | < 3x |

## SaaS-Specific Metrics

For SaaS/cloud companies, supplement with:

| Metric | What It Measures | Benchmark |
|--------|-----------------|-----------|
| Net Revenue Retention (NRR) | Expansion within existing customers | Elite: >130%, Good: 110–130%, Concerning: <100% |
| Gross retention | Customer churn | Good: >90%, Concerning: <85% |
| ARR growth | Recurring revenue momentum | High-growth: >30%, Moderate: 15–30% |
| RPO growth | Forward revenue visibility | Should track or exceed ARR growth |
| Customer concentration | Revenue dependency risk | Top customer < 10% of revenue ideal |

## Mispricing Identification

### Overvalued Indicators (Hype > Fundamentals)

A stock is likely overpriced when:

1. **Implied growth is unreachable**: Current EV/Revenue implies revenue CAGR that would require >100% of the TAM
2. **Multiple expansion without fundamental improvement**: P/S rising while growth is decelerating
3. **Narrative dependency**: Valuation rests on a story (AI, metaverse, etc.) without revenue proof
4. **Peak margins being capitalized**: Market treating cyclically high margins as permanent
5. **Consensus is uniformly bullish**: No bears left — asymmetric downside risk
6. **Insider selling acceleration**: Management selling into the rally

### Undervalued Indicators (Fundamentals > Perception)

A stock is likely underpriced when:

1. **Valuation discount to growth peers**: Lower P/S or P/E despite equal or better growth
2. **Margin inflection not priced**: Company transitioning from investment to harvest phase
3. **Hidden optionality**: New product, market, or business model not in consensus estimates
4. **Guilt by association**: Sold with sector but fundamentals are differentiated
5. **Analyst coverage gap**: Under-covered relative to quality of business
6. **Insider buying**: Management purchasing with personal capital (see insider-trading-analyzer skill)

### What the Market Is Mispricing — Framework

For each mispriced stock, articulate the mispricing as:

```
The market is pricing [Company] as if [Market's Implied Assumption].
In reality, [Actual Fundamental Evidence].
This creates a [X]% gap between implied and actual [metric].
The catalyst to close this gap is [specific event/trend].
```

## Common Valuation Pitfalls in Tech

- **TAM fallacy**: Assuming the company can capture a large % of an enormous TAM without competition
- **Winner-take-all assumption**: Tech markets often support 2–3 major players, not monopolies
- **Linear extrapolation**: Projecting current growth rates indefinitely ignores base effects and market saturation
- **Multiple comparison without context**: Comparing P/S across companies with different margins, growth, and quality is misleading
- **Ignoring dilution**: High SBC-adjusted margins that evaporate on a GAAP basis
- **Revenue quality blindness**: $1 of recurring SaaS revenue ≠ $1 of hardware revenue ≠ $1 of services revenue
