# Gap Analysis Methodology

Detailed framework for measuring sentiment-fundamental misalignment, classifying negative catalysts, and scoring gap magnitude.

## Table of Contents

1. [Sentiment Measurement](#sentiment-measurement)
2. [Fundamental Strength Validation](#fundamental-strength-validation)
3. [Issue Classification Framework](#issue-classification-framework)
4. [Gap Magnitude Scoring](#gap-magnitude-scoring)
5. [Historical Reversion Patterns](#historical-reversion-patterns)
6. [Common Sentiment Traps](#common-sentiment-traps)

## Sentiment Measurement

### Quantitative Sentiment Indicators

Score each on a 1–5 scale (5 = most negative sentiment):

| Indicator | 1 (Neutral) | 3 (Moderately Negative) | 5 (Extremely Negative) |
|-----------|-------------|------------------------|----------------------|
| Price drawdown from 52-wk high | < 10% | 20–35% | > 50% |
| Short interest (% of float) | < 3% | 5–10% | > 15% |
| Analyst rating shift (90d) | Stable | 1–2 downgrades | ≥ 3 downgrades, no upgrades |
| Put/call ratio vs. average | < 1.0x | 1.0–1.5x | > 2.0x |
| Institutional ownership change (QoQ) | Stable | -2% to -5% | > -5% |
| Days to cover (short interest) | < 3 | 3–7 | > 7 |

**Composite sentiment score**: Average across all available indicators. ≥ 3.5 qualifies as "heavily negative sentiment."

### Qualitative Sentiment Indicators

Supplement quantitative scores with:

- **Media tone analysis**: Count of negative vs. positive headlines over 30/60/90 days
- **Earnings call language**: Management tone shift — defensive, apologetic, or unusually cautious language
- **Conference/investor day cancellations**: Companies pulling back from investor engagement
- **Social media/retail sentiment**: Reddit, StockTwits, FinTwit sentiment polarity
- **Sell-side abandonment**: Analysts dropping coverage (often worse than downgrades)

### Sentiment Timeline Construction

Build a timeline to understand sentiment evolution:

1. **Trigger event** — What initiated the negative sentiment (earnings miss, lawsuit, macro shock, etc.)
2. **Amplification phase** — Media pile-on, analyst downgrades, fund outflows
3. **Current state** — Has sentiment stabilized, worsened, or begun to recover
4. **Inflection signals** — Early signs of sentiment turning (insider buying, activist involvement, stabilizing short interest)

## Fundamental Strength Validation

### Tier 1: Must-Pass (Disqualifying if failed)

| Check | Pass Criteria | Fail = Exclude |
|-------|--------------|----------------|
| Solvency | Current ratio > 1.0 AND no debt maturity wall within 12 months | Immediate liquidity risk |
| Revenue trajectory | Revenue decline < 15% YoY (or sequential improvement) | Accelerating revenue collapse |
| Cash burn | FCF positive OR cash runway > 18 months | Running out of cash |
| Accounting integrity | No restatements, SEC inquiries, or auditor changes in last 2 years | Trust deficit |

### Tier 2: Strength Indicators (Score 0–3 each)

| Check | 0 (Weak) | 1 (Adequate) | 2 (Strong) | 3 (Excellent) |
|-------|----------|--------------|------------|----------------|
| EPS trend | Declining | Flat | Growing < 10% | Growing ≥ 10% |
| Gross margin vs. 3Y avg | > 300bps below | 100–300bps below | Within 100bps | Above average |
| Debt/equity vs. sector | > 2x median | 1–2x median | At median | Below median |
| FCF yield | < 2% | 2–4% | 4–7% | > 7% |
| ROIC vs. WACC | Below WACC | At WACC | WACC + 2–5% | WACC + > 5% |
| Dividend coverage | Cut or at risk | < 1.5x | 1.5–2.5x | > 2.5x or no div |

**Minimum qualifying score**: ≥ 10/18 on Tier 2 indicators (after passing all Tier 1 checks).

### Supplementary Checks

- **Customer/revenue concentration**: Top customer < 20% of revenue
- **Management stability**: No unexpected C-suite departures in last 6 months
- **Backlog/pipeline**: Forward indicators stable or growing
- **Capex discipline**: Not slashing growth investments (may signal management panic)

## Issue Classification Framework

### Decision Tree

```
Is the negative catalyst...
│
├── Affecting the company's core business model viability?
│   ├── YES → Is there a viable pivot or adaptation path?
│   │   ├── YES → TRANSITIONAL (proceed with caution)
│   │   └── NO → STRUCTURAL (exclude)
│   └── NO → Continue ↓
│
├── Likely to persist beyond 2–3 years?
│   ├── YES → STRUCTURAL (exclude)
│   └── NO → Continue ↓
│
├── Driven by macro/cyclical factors common to peers?
│   ├── YES → Is the company outperforming peers through the cycle?
│   │   ├── YES → TEMPORARY/CYCLICAL (strong candidate)
│   │   └── NO → TEMPORARY/CYCLICAL (moderate candidate)
│   └── NO → Continue ↓
│
├── Primarily driven by narrative/headlines with limited fundamental impact?
│   ├── YES → NARRATIVE-DRIVEN (strong candidate)
│   └── NO → Continue ↓
│
└── A one-time event (lawsuit, product recall, management scandal)?
    ├── YES → Is the event contained and quantifiable?
    │   ├── YES → TEMPORARY (strong candidate)
    │   └── NO → Assess further, may be STRUCTURAL
    └── NO → Reassess — may not fit the framework
```

### Classification Definitions

| Type | Definition | Examples | Investment Implication |
|------|-----------|----------|----------------------|
| **Temporary** | Discrete event with finite duration | Bad quarter, product recall, one-time legal charge | High gap potential — typically reverts within 6–12 months |
| **Cyclical** | Industry-wide downturn phase | Commodity price crash, rate cycle impact, inventory correction | Moderate gap — reverts with cycle but timing uncertain |
| **Narrative-driven** | Sentiment exceeds fundamental impact | Guilt by association, headline FUD, social media panic | Highest gap potential — narrative can collapse quickly |
| **Transitional** | Business model shift underway | Legacy business declining, new segment growing | Cautious — gap exists but thesis depends on execution |
| **Structural** | Permanent impairment | Disruption, obsolescence, terminal regulatory risk | **Exclude** — sentiment is correct |

## Gap Magnitude Scoring

Combine sentiment and fundamental scores into a gap magnitude:

```
Gap Score = Sentiment Negativity Score × Fundamental Strength Score × Valuation Discount Factor
```

### Valuation Discount Factor

| Current P/E vs. 5Y Average | Factor |
|-----------------------------|--------|
| > 40% below | 1.5x |
| 25–40% below | 1.3x |
| 10–25% below | 1.1x |
| Within 10% | 1.0x |
| Above average | 0.7x (sentiment may be justified) |

### Gap Score Interpretation

| Score Range | Gap Assessment | Conviction Level |
|-------------|---------------|-----------------|
| > 25 | Extreme misalignment | Very high — sentiment wildly disconnected |
| 18–25 | Large gap | High — compelling contrarian case |
| 12–18 | Moderate gap | Moderate — worth monitoring |
| < 12 | Narrow gap | Low — sentiment may be roughly fair |

## Historical Reversion Patterns

When assessing potential upside, reference these historical patterns:

### Mean Reversion Timelines

| Catalyst Type | Typical Reversion Period | Median Recovery (12mo) |
|--------------|------------------------|----------------------|
| Earnings miss (single quarter) | 1–3 quarters | +15–25% |
| Sector rotation | 3–6 months | +10–20% |
| Headline/narrative shock | 1–6 months | +20–40% |
| Macro cycle trough | 6–18 months | +25–50% |
| Management crisis (resolved) | 6–12 months | +15–30% |

*These are illustrative ranges based on historical academic research (e.g., DeBondt & Thaler overreaction studies, Lakonishok et al. contrarian strategies). Actual results vary.*

### Reversion Catalysts to Monitor

- Earnings beat after a miss (strongest single reversion trigger)
- Activist investor involvement (forces value recognition)
- Share buyback authorization (management signaling)
- Insider buying cluster (see insider-trading-analyzer skill)
- Analyst upgrade cycle beginning
- Short squeeze dynamics (high short interest + positive catalyst)

## Common Sentiment Traps

Pitfalls to avoid when hunting for sentiment-reality gaps:

### Value Traps

- **Declining moat**: Metrics look fine today but competitive position is eroding
- **Financial engineering**: EPS growth via buybacks masking revenue decline
- **Melting ice cube**: Slowly deteriorating business with artificially maintained margins
- **Cyclical peak earnings**: Low P/E because earnings are at cyclical peak, not because stock is cheap

### Narrative Traps

- **"It's already priced in"**: Sometimes the negative sentiment *is* the correct price — not every selloff is an overreaction
- **Anchoring to past highs**: A stock down 50% from its peak may still be overvalued if the peak was a bubble
- **Survivorship bias**: Looking at past recoveries ignores stocks that never recovered
- **Confirmation bias**: Seeking only data that supports the contrarian thesis while ignoring warning signs

### Timing Traps

- **Too early = wrong**: Being right about fundamentals but wrong on timing can be as costly as being wrong outright
- **Catching a falling knife**: Sentiment may worsen further before it improves — position sizing matters
- **Catalyst dependency**: Without a clear catalyst to close the gap, misalignment can persist indefinitely
