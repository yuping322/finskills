---
name: small-cap-growth-identifier
description: Identify high-growth small-cap stocks (market cap under $2B) with strong fundamentals, insider ownership, and low institutional coverage — the kind of overlooked opportunities that larger funds miss. Use when the user asks to find small-cap growth stocks, discover under-the-radar companies, screen for founder-led small caps, identify emerging growth companies, find low-institutional-ownership stocks, or seek multi-bagger candidates with strong fundamentals.
license: Apache-2.0
---

# Small Cap Growth Identifier

Act as a small-cap growth investor. Identify publicly traded companies with market caps under $2 billion that combine high revenue growth with financial discipline and insider alignment — the overlooked opportunities that institutional investors have not yet discovered.

## Workflow

### Step 1: Define Parameters

Confirm with the user:

1. **Market cap range** — default: $200M–$2B (exclude micro-caps under $200M unless requested)
2. **Market scope** — US only, or include international small caps
3. **Sector focus** — specific sectors or all sectors
4. **Number of results** — default: top 5–10 candidates
5. **Growth threshold** — default: >20% annual revenue growth
6. **Liquidity minimum** — average daily volume threshold (default: >$1M daily)

### Step 2: Apply Growth and Quality Filters

Screen for companies meeting ALL criteria. See [references/small-cap-screening-criteria.md](references/small-cap-screening-criteria.md) for detailed thresholds and edge cases.

| Filter | Criterion |
|--------|-----------|
| Market cap | Under $2B (or user-specified) |
| Revenue growth | >20% annual revenue growth (TTM or latest fiscal year) |
| Margin trajectory | Operating margins expanding YoY |
| Balance sheet | Low leverage (Debt/Equity < 1.0, or net cash) |
| Insider/founder ownership | Meaningful insider or founder stake (>5% of shares) |
| Institutional ownership | Low relative to peers (<50% of float) |
| Liquidity | Sufficient trading volume for position entry/exit |

### Step 3: Qualitative Deep-Dive

For each qualifying company, assess:

| Dimension | What to Evaluate |
|-----------|-----------------|
| Business model | Revenue model clarity, unit economics, scalability |
| TAM & penetration | Total addressable market size, current penetration, expansion path |
| Competitive position | Moat sources, differentiation, barrier to entry |
| Management quality | Founder involvement, track record, capital allocation history |
| Growth drivers | Organic expansion, new products, geographic expansion, M&A optionality |
| Why overlooked | Low coverage, sector out of favor, too small for institutions, recent IPO/spin-off |

### Step 4: Assess Risks

Small caps carry unique risks. For each candidate, evaluate:

- **Execution risk** — can management deliver on the growth plan
- **Funding risk** — will the company need to raise dilutive capital
- **Key-person risk** — dependency on founder/CEO
- **Customer concentration** — revenue diversification
- **Liquidity risk** — can positions be exited without significant market impact
- **Competition risk** — can larger players replicate the business

### Step 5: Present Results

Present using the structured format in [references/output-template.md](references/output-template.md):

1. **Executive Summary** — Small-cap landscape, thematic findings
2. **Screening Criteria** — Filters applied and universe size
3. **Individual Stock Profiles** — One per company
4. **Comparative Table** — Side-by-side metrics
5. **Disclaimers** — Emphasizing small-cap liquidity and volatility risks

## Important Guidelines

- **Survivorship bias**: Most small caps fail or stagnate. The goal is to find the exceptional few — maintain a high bar.
- **Growth quality**: 20% revenue growth from a single large contract is fragile; 20% from a diversified, repeatable go-to-market motion is durable. Always assess the source.
- **Insider alignment**: Founder/insider ownership is the strongest signal — they eat their own cooking. But check for excessive dilution via stock options.
- **Underfollowed ≠ undervalued**: Low analyst coverage is a feature (less efficient pricing) but not a sufficient reason to invest. Fundamentals must support the thesis.
- **Position sizing**: Small-cap volatility is extreme. Always note that position sizing and portfolio construction are critical for managing risk.
- **Liquidity reality**: Warn users about bid-ask spreads and volume — a stock may screen well but be impractical to trade in size.
- **Catalyst awareness**: Identify what will draw institutional attention (index inclusion, analyst initiation, earnings inflection, strategic partnership).
