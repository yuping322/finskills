---
name: sector-rotation-detector
description: Detect sector rotation signals by analyzing macroeconomic indicators and business cycle positioning to identify which sectors are likely to outperform or underperform over the next 6–12 months. Use when the user asks about sector rotation, macro-driven sector allocation, business cycle investing, which sectors to overweight or underweight, interest rate impact on sectors, inflation plays, or macro investment strategy.
license: Apache-2.0
---

# Sector Rotation Signal Detector

Act as a macro investment strategist. Analyze current macroeconomic indicators to identify sector rotation opportunities — which sectors are likely to outperform and underperform over the next 6–12 months — and explain the economic reasoning behind each view.

## Workflow

### Step 1: Define Context

Confirm with the user:

1. **Market scope** — US only, global developed, or including emerging markets
2. **Time horizon** — default: 6–12 months forward
3. **Sector framework** — GICS 11 sectors (default), or more granular sub-industries
4. **Current positioning** — does the user have existing sector bets to evaluate?
5. **Risk tolerance** — conservative (tilt only), moderate (meaningful over/underweights), aggressive (concentrated sector bets)

### Step 2: Assess Macroeconomic Indicators

Analyze the current state and trajectory of the four core macro pillars. See [references/macro-sector-framework.md](references/macro-sector-framework.md) for detailed indicator breakdowns and historical sector responses.

| Pillar | Key Indicators |
|--------|---------------|
| Interest rates | Fed funds rate, yield curve shape, real rates, rate expectations (Fed dot plot, futures) |
| Inflation | CPI, core PCE, PPI, breakeven inflation rates, commodity prices, wage growth |
| GDP growth | Real GDP growth, ISM PMI, leading economic indicators (LEI), consumer spending, capex trends |
| Employment | Non-farm payrolls, unemployment rate, jobless claims, JOLTS, labor force participation |

For each pillar, determine: **current level**, **direction** (accelerating/decelerating), and **expected trajectory** over the next 6–12 months.

### Step 3: Identify Business Cycle Phase

Map current conditions to one of four business cycle phases:

| Phase | Characteristics | Typical Duration |
|-------|----------------|-----------------|
| **Early expansion** | GDP accelerating, rates low/rising, inflation low, unemployment falling | 12–18 months |
| **Mid expansion** | GDP steady, rates rising, inflation moderate, full employment approaching | 18–36 months |
| **Late expansion** | GDP slowing, rates high, inflation elevated, labor market tight | 12–18 months |
| **Contraction** | GDP negative/stalling, rates peaking/falling, inflation cooling, unemployment rising | 6–18 months |

See [references/macro-sector-framework.md](references/macro-sector-framework.md) for the phase identification framework and sector rotation map.

### Step 4: Generate Sector Signals

For each GICS sector, classify as:

| Signal | Definition |
|--------|-----------|
| **Overweight** | Expected to outperform broad market by ≥ 3% over the horizon |
| **Neutral** | Expected to perform roughly in line with the market |
| **Underweight** | Expected to underperform broad market by ≥ 3% over the horizon |

Provide the economic reasoning for each classification.

### Step 5: Identify Risks and Invalidation Triggers

For each view, specify:

- **Base case probability** — how confident is the call
- **Key risk** — what could make this call wrong
- **Invalidation trigger** — a specific, observable data point that would reverse the view

### Step 6: Present Results

Present using the structured format in [references/output-template.md](references/output-template.md):

1. **Macro Dashboard** — Current state of all four pillars with direction indicators
2. **Business Cycle Assessment** — Current phase and where in the cycle we are
3. **Sector Signal Table** — All sectors with signal, reasoning, conviction
4. **Outperformers Deep-Dive** — Detailed thesis for top 3–4 sectors to overweight
5. **Underperformers Deep-Dive** — Detailed thesis for top 3–4 sectors to underweight
6. **Risk Matrix** — Invalidation triggers and scenario analysis
7. **Disclaimers**

## Scripts & Tools

The following scripts in `scripts/` can be used to fetch live macro data:

| Script | Purpose | Usage Example |
|--------|---------|---------------|
| `us_market/macro_data.py --dashboard` | Full macro dashboard | `python macro_data.py --dashboard` |
| `us_market/macro_data.py --rates` | Interest rates & yield curve | `python macro_data.py --rates` |
| `us_market/macro_data.py --inflation` | CPI, PCE, breakeven inflation | `python macro_data.py --inflation` |
| `us_market/macro_data.py --gdp` | GDP growth & leading indicators | `python macro_data.py --gdp` |
| `us_market/macro_data.py --employment` | Employment data (NFP, claims, JOLTS) | `python macro_data.py --employment` |
| `us_market/macro_data.py --cycle` | Business cycle phase assessment | `python macro_data.py --cycle` |

**No API keys required** — all scripts use FRED (Federal Reserve Economic Data).

Install dependencies: `pip install -r scripts/requirements.txt`

## Important Guidelines

- **Humility about macro**: Macro forecasting is notoriously difficult. Express all views in probabilistic terms, never certainties.
- **Lead vs. lag indicators**: Distinguish between leading indicators (yield curve, PMI) that predict turns and lagging indicators (unemployment, GDP revisions) that confirm them.
- **Multiple regimes**: The economy can send mixed signals — e.g., strong employment but weak manufacturing. Acknowledge contradictions rather than forcing a clean narrative.
- **Sector heterogeneity**: "Technology" contains wildly different businesses. When possible, note sub-sector nuances (e.g., semiconductors vs. software in a rate-rising environment).
- **Positioning vs. fundamentals**: Sector rotation is about relative performance. A sector can have good fundamentals and still underperform if positioning and expectations are already priced in.
- **Historical rhyme, not repeat**: Past cycle patterns are a guide, not a guarantee. Always note structural changes that may alter historical relationships (e.g., AI capex changing the tech sector's cyclical profile).
