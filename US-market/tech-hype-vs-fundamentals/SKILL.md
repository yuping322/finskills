---
name: tech-hype-vs-fundamentals
description: Compare leading tech stocks to distinguish hype-driven overvaluation from fundamentally justified pricing, and identify undervalued tech names the market is overlooking. Use when the user asks to evaluate tech stock valuations, find overvalued or undervalued tech companies, assess whether a tech stock's growth justifies its multiple, compare tech company fundamentals, analyze revenue growth vs. valuation, or identify mispriced technology stocks.
license: Apache-2.0
---

# Tech Stock Hype vs Fundamentals Analyzer

Act as a valuation-focused technology analyst. Compare leading publicly traded tech companies to separate fundamentally justified valuations from hype-driven excess, and surface undervalued names the market is mispricing.

## Workflow

### Step 1: Define Scope

Confirm with the user:

1. **Universe** — mega-cap tech only, broader tech sector, specific sub-sector (SaaS, semiconductors, AI, cybersecurity, etc.), or custom list
2. **Comparison set size** — default: evaluate 15–20 companies, surface 3 overvalued + 3 undervalued
3. **Valuation framework** — growth-adjusted (PEG), DCF-based, rule-of-40, or multi-factor (default: multi-factor)
4. **Time horizon** — current snapshot or trend analysis over 1–3 years

### Step 2: Build the Comparison Set

Gather and compute core metrics for each company. See [references/tech-valuation-framework.md](references/tech-valuation-framework.md) for calculation details and benchmarks.

| Category | Metrics |
|----------|---------|
| Growth | Revenue growth (YoY, 3Y CAGR), forward revenue growth estimates |
| Valuation | P/E, P/S, EV/Revenue, EV/EBITDA, PEG ratio |
| Profitability | Gross margin, operating margin, net margin, EBITDA margin |
| Operating leverage | Margin expansion trend (are margins improving as revenue scales?) |
| Cash generation | FCF, FCF margin, FCF yield, cash conversion ratio |
| Capital efficiency | ROIC, ROE, revenue per employee, R&D as % of revenue |
| SaaS-specific (if applicable) | NRR, ARR growth, Rule of 40, CAC payback, LTV/CAC |

### Step 3: Plot Growth vs. Valuation

Map each company on a growth-vs-valuation matrix:

```
              High Valuation
                    |
   OVERVALUED       |      FAIRLY VALUED
   (hype > growth)  |      (premium justified)
                    |
  ──────────────────┼──────────────────
                    |
   FAIRLY VALUED    |      UNDERVALUED
   (modest growth,  |      (growth > valuation)
    modest price)   |
                    |
              Low Valuation
   Low Growth ──────────────── High Growth
```

See [references/tech-valuation-framework.md](references/tech-valuation-framework.md) for the quantitative scoring model.

### Step 4: Identify Mispriced Stocks

**3 Overvalued (Priced for Unrealistic Growth)**:
- Valuation multiple implies growth rate significantly above achievable trajectory
- Margins or TAM cannot support the implied revenue path
- Market is extrapolating peak metrics indefinitely

**3 Undervalued (Overlooked Fundamentals)**:
- Trading at a discount to growth and profitability peers
- Margin expansion or business model shift not yet reflected in price
- Overshadowed by larger competitors or suffering from narrative neglect

For each, articulate precisely **what the market is mispricing** and **why**.

### Step 5: Present Results

Present using the structured format in [references/output-template.md](references/output-template.md):

1. **Executive Summary** — Key findings, market themes, biggest mispricings
2. **Full Comparison Table** — All companies with core metrics
3. **Growth vs. Valuation Matrix** — Visual positioning
4. **Overvalued Profiles** — 3 detailed write-ups
5. **Undervalued Profiles** — 3 detailed write-ups
6. **Disclaimers**

## Data Enhancement

For live market data to support this analysis, use the **FinData Toolkit** skill (`findata-toolkit-us`). It provides real-time stock metrics, SEC filings, financial calculators, portfolio analytics, factor screening, and macro indicators — all without API keys.

## Important Guidelines

- **Growth quality matters**: Not all revenue growth is equal. Distinguish organic vs. acquisition-driven, recurring vs. one-time, expanding TAM vs. market share gains in a shrinking market.
- **Margin trajectory > current margins**: A company with 5% operating margin expanding 500bps/year is more valuable than one at 20% margin that's flat.
- **Avoid the "it's expensive so it's overvalued" fallacy**: Some tech stocks deserve premium multiples. The question is whether the premium is *sufficient* or *excessive* given the growth and profitability profile.
- **AI/narrative premium**: Many tech stocks carry an AI premium. Assess whether the company has genuine AI monetization or is narrative-surfing.
- **Stock-based compensation**: Adjust profitability for SBC dilution — a company showing GAAP losses but "adjusted profitability" may be less impressive than it appears.
- **Competitive moats**: Evaluate network effects, switching costs, data advantages, and ecosystem lock-in. Moats justify higher multiples.
