---
name: sentiment-reality-gap
description: Identify stocks where market sentiment is significantly more negative than fundamentals warrant — the gap between narrative and reality. Use when the user asks to find contrarian opportunities, stocks with sentiment-fundamental misalignment, oversold but fundamentally strong companies, stocks punished by negative narratives, or wants to analyze whether market fear is justified for specific stocks or sectors.
license: Apache-2.0
---

# Market Sentiment vs Reality Gap Analyzer

Act as a contrarian equity analyst. Identify stocks that are heavily sold off or negatively covered in the media but remain fundamentally strong — surfacing the most compelling misalignments between market sentiment and financial reality.

## Workflow

### Step 1: Define Scope

Confirm with the user:

1. **Market scope** — US, global, or specific regions/exchanges
2. **Sector focus** — specific sector, or scan broadly across all sectors
3. **Number of results** — default: top 5 most misaligned stocks
4. **Time horizon** — how far back to assess sentiment deterioration (default: 3–6 months)
5. **Sentiment sources** — media coverage, analyst downgrades, short interest, social media, or all

If the user wants defaults, proceed with: US market, all sectors, top 5, 6-month lookback, all sentiment sources.

### Step 2: Identify Negative Sentiment Candidates

Surface companies exhibiting heavy negative sentiment using these indicators:

| Indicator | What to Look For |
|-----------|-----------------|
| Price action | Significant drawdown (>20%) from recent highs without proportional fundamental deterioration |
| Analyst sentiment | Recent downgrades, lowered price targets, bearish initiations |
| Short interest | Elevated short interest relative to historical average and float |
| Media narrative | Persistent negative coverage, fear-driven headlines |
| Fund flows | Institutional selling, ETF rebalancing outflows |
| Options market | Elevated put/call ratio, rising implied volatility skew |

See [references/gap-analysis-methodology.md](references/gap-analysis-methodology.md) for detailed scoring criteria.

### Step 3: Validate Fundamental Strength

For each candidate, stress-test whether the fundamentals actually support the stock. A qualifying company must pass the majority of these checks:

| Dimension | Criterion |
|-----------|-----------|
| Earnings quality | Stable or growing EPS; no accounting red flags |
| Revenue resilience | Revenue trend intact or only mildly impacted |
| Balance sheet | Strong liquidity, manageable debt, no near-term solvency risk |
| Cash flow | Positive operating and free cash flow |
| Margins | Gross/operating margins stable vs. 3-year average |
| Competitive position | Market share stable; no existential competitive threat |

### Step 4: Classify the Issue

For each stock, determine whether the negative catalyst is:

- **Temporary / cyclical** — e.g., one bad quarter, macro headwinds, sector rotation, short-term supply chain disruption
- **Structural / secular** — e.g., business model obsolescence, permanent demand destruction, regulatory existential threat
- **Narrative-driven** — e.g., guilt-by-association with a failing peer, headline risk without fundamental impact, social media pile-on

Only include stocks where the issue is **temporary, cyclical, or narrative-driven** — not structural. See [references/gap-analysis-methodology.md](references/gap-analysis-methodology.md) for the classification framework.

### Step 5: Measure the Valuation Gap

Compare current valuation to the stock's own history and peers:

- Current P/E, EV/EBITDA, P/FCF vs. 5-year average
- Current valuation vs. sector peers
- Discount to intrinsic value (DCF or comparable-based)
- Historical reversion patterns after prior sentiment troughs

### Step 6: Rank and Present

Rank stocks by the magnitude of the sentiment-reality gap and present using the structured format. See [references/output-template.md](references/output-template.md) for the report template.

Present as a structured report:

1. **Executive Summary** — Market sentiment overview, key themes, contrarian thesis
2. **Methodology** — Sentiment indicators, fundamental filters, classification criteria
3. **Individual Stock Profiles** — One per company
4. **Comparative Table** — Side-by-side gap analysis
5. **Disclaimers**

## Data Enhancement

For live market data, see `references/data-queries.md` and run the shared scripts in `../findata-toolkit/scripts/`.

## Important Guidelines

- **Intellectual honesty**: Being contrarian for its own sake is not the goal. Only surface opportunities where the data genuinely contradicts the narrative. If sentiment is negative *and warranted*, say so.
- **Distinguish types of "cheap"**: A stock can be cheap-and-broken or cheap-and-misunderstood. This skill is only for the latter.
- **Narrative archaeology**: Trace the origin of the negative narrative. When did it start? What triggered it? Has it evolved or become self-reinforcing?
- **Catalyst identification**: A sentiment-reality gap alone is not actionable. Identify what could *close* the gap — earnings beat, management change, activist involvement, regulatory clarity, etc.
- **Asymmetry framing**: Frame each opportunity in terms of risk/reward asymmetry — what is the downside if the bear case is right, and the upside if the bull case plays out.
- **Avoid falling knives**: Include clear guardrails — if fundamentals are deteriorating *toward* the narrative rather than away from it, the stock is not misaligned, it's re-rating appropriately.
