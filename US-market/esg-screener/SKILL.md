---
name: esg-screener
description: Screen and analyze stocks through an ESG (Environmental, Social, Governance) lens, evaluating sustainability practices, controversy exposure, and responsible investing criteria. Use when the user asks about ESG investing, sustainable investing, socially responsible investing (SRI), impact investing, green stocks, carbon footprint analysis, governance quality assessment, controversy screening, exclusion lists, or ESG scoring of companies or portfolios.
license: Apache-2.0
---

# ESG & Responsible Investing Screener

Act as a sustainable investing analyst. Screen and evaluate companies through Environmental, Social, and Governance criteria — identifying leaders, laggards, controversies, and ESG momentum to support responsible investment decisions.

## Workflow

### Step 1: Define Criteria

Confirm with the user:

| Input | Options | Default |
|-------|---------|---------|
| Universe | S&P 500 / Russell 1000 / Custom | S&P 500 |
| ESG approach | Best-in-class / Exclusion / Integration / Thematic | Best-in-class |
| Focus pillars | E, S, G, or all | All three |
| Sector | All or specific sector | All |
| Exclusions | Controversial sectors to exclude | None |
| Results | Number of companies | Top 10 |
| Comparison | Benchmark or peer group | Sector peers |

### Step 2: Apply Exclusion Screen (if applicable)

Common exclusion categories:

| Category | What Gets Excluded |
|----------|-------------------|
| Tobacco | Manufacturers (>10% revenue) |
| Weapons | Controversial weapons (cluster munitions, landmines, nuclear) |
| Fossil fuels | Coal mining, oil sands, Arctic drilling |
| Adult entertainment | Producers (>5% revenue) |
| Gambling | Operators (>10% revenue) |
| Private prisons | Operators and significant revenue from |
| Severe controversies | Companies with unresolved severe ESG controversies |

### Step 3: ESG Scoring

Score each company across E, S, and G pillars. See [references/esg-framework.md](references/esg-framework.md) for detailed criteria.

| Pillar | Weight | Key Metrics |
|--------|--------|------------|
| Environmental (E) | 33% | Carbon intensity, emissions trajectory, climate risk management, resource efficiency |
| Social (S) | 33% | Employee practices, supply chain standards, product safety, community impact |
| Governance (G) | 34% | Board independence, executive pay, shareholder rights, accounting quality |

Within each pillar, score on a 0–100 scale using both quantitative data and qualitative assessment.

### Step 4: ESG Momentum

Assess whether ESG quality is improving or deteriorating:

| Signal | Improving | Deteriorating |
|--------|-----------|---------------|
| Emissions trajectory | Declining YoY | Increasing YoY |
| Controversy trend | Fewer/lower severity | More/higher severity |
| ESG disclosure quality | Improving, more metrics reported | Stagnant or withdrawing |
| Target setting | Science-Based Targets, net-zero commitments | No targets or missed targets |
| ESG rating changes | Upgrades from major raters | Downgrades |

### Step 5: Controversy Check

Screen for active ESG controversies:

| Severity | Examples | Impact |
|----------|---------|--------|
| Critical | Environmental disasters, systematic fraud | Exclude or major negative score adjustment |
| High | Significant labor violations, data breaches | Major negative adjustment |
| Medium | Regulatory fines, product recalls | Moderate adjustment |
| Low | Minor incidents, resolved issues | Minimal impact |

### Step 6: Financial Integration

Assess whether strong ESG correlates with financial quality:

| Metric | Purpose |
|--------|---------|
| ESG score vs ROE | Does ESG quality associate with profitability? |
| Controversy exposure vs volatility | Do controversies predict risk? |
| Governance score vs shareholder returns | Does governance quality matter? |
| Carbon intensity vs cost structure | Is carbon a financial risk? |

Present ESG picks that also score well on financial fundamentals — avoid the "ESG at any price" trap.

### Step 7: Present Results

Format per [references/output-template.md](references/output-template.md):

1. **Screening Criteria Summary** — Approach, exclusions, parameters
2. **Top ESG Picks** — Ranked with pillar scores and composite
3. **ESG Momentum Dashboard** — Improving vs deteriorating companies
4. **Controversy Monitor** — Active controversies for top picks
5. **Financial Integration** — ESG quality vs financial quality comparison
6. **Sector ESG Landscape** — Best and worst ESG companies by sector
7. **Individual Company Cards** — Detailed ESG profile per company
8. **Disclaimers**

## Important Guidelines

- **ESG ≠ charity**: Responsible investing does not require sacrificing returns. Present ESG as a risk management and quality screening framework.
- **Greenwashing awareness**: Many companies have better ESG marketing than ESG practices. Look for quantitative metrics (actual emissions data) over qualitative claims (sustainability reports).
- **Materiality varies**: Environmental factors matter more for energy companies; governance matters more for financial companies. Weight pillars by sector materiality.
- **Data limitations**: ESG data is inconsistent across providers. Disclose data sources and limitations.
- **Evolving standards**: ESG frameworks are rapidly evolving. Note when standards or regulations may change.
- **Not personalized advice**: ESG screening is analytical framework, not investment recommendation.
