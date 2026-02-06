---
name: insider-trading-analyzer
description: Analyze insider trading patterns to surface companies with significant, meaningful insider buying activity. Use when the user asks to review insider trading activity, find stocks insiders are buying, analyze SEC Form 4 filings, detect insider buying clusters, assess management confidence through insider purchases, or identify bullish insider signals in a sector or industry.
license: Apache-2.0
---

# Insider Trading Pattern Analyzer

Act as a professional insider trading analyst. Review recent insider trading activity to identify companies exhibiting meaningful, clustered insider buying — a historically strong signal of management confidence and potential undervaluation.

## Workflow

### Step 1: Define Scope

Confirm with the user:

1. **Sector or industry** — specific sector (e.g., Technology, Healthcare) or broad market scan
2. **Time window** — default: last 90 days; user may widen or narrow
3. **Number of results** — default: top 5 companies
4. **Market scope** — US (SEC Form 4), international, or both
5. **Insider roles of interest** — all insiders, C-suite only, directors only, or 10%+ beneficial owners

If the user wants defaults, proceed with: all US sectors, 90 days, top 5, all insider roles.

### Step 2: Apply Insider Buying Filters

Screen for companies matching ALL of the following criteria. See [references/insider-signal-criteria.md](references/insider-signal-criteria.md) for detailed thresholds and edge cases.

| Filter | Criterion |
|--------|-----------|
| Cluster buying | Multiple insiders (≥ 2) buying within the time window |
| Transaction type | Open-market purchases only (exclude option exercises, grants, automatic plans) |
| Recency | Purchases within the last 90 days (or user-specified window) |
| Meaningfulness | Purchase size meaningful relative to insider's compensation and existing holdings |

### Step 3: Rank and Analyze

Rank qualifying companies by signal strength using these factors (see [references/insider-signal-criteria.md](references/insider-signal-criteria.md) for scoring details):

- Number and seniority of insiders buying
- Aggregate dollar value of purchases
- Purchase size relative to insider compensation
- Buying into price weakness (contrarian signal)
- Cluster density (multiple buys within a narrow window)

### Step 4: Deep-Dive on Top Results

For each of the top companies, provide a detailed analysis covering:

1. **Who is buying and how much** — Name, title, number of shares, dollar value, dates, and what percentage of their holdings the purchase represents
2. **Historical impact** — How insider buying has preceded stock performance in this specific company's history
3. **Management confidence signal** — What the buying pattern likely signals about management's view of the company's prospects
4. **Potential red flags** — Reasons the buying might not be as bullish as it appears

See [references/output-template.md](references/output-template.md) for the structured report format.

### Step 5: Compile and Present

Present findings as a structured report:

1. **Executive Summary** — Overview of insider activity trends in the scanned sector/market
2. **Methodology** — Filters applied, time window, data sources
3. **Individual Company Profiles** — One section per company using the output template
4. **Comparative Table** — Side-by-side insider buying metrics
5. **Disclaimers** — Insider trading data interpretation caveats

## Data Enhancement

For live market data to support this analysis, use the **FinData Toolkit** skill (`findata-toolkit-us`). It provides real-time stock metrics, SEC filings, financial calculators, portfolio analytics, factor screening, and macro indicators — all without API keys.

## Important Guidelines

- **Legal distinction**: "Insider trading" in this context refers to *legal* insider transactions reported to regulators (SEC Form 4 in the US), not illegal trading on material non-public information.
- **Open-market only**: Exclude option exercises, restricted stock vesting, 10b5-1 automatic plan purchases, and gift transactions — these do not reflect discretionary conviction.
- **Context matters**: Insider buying after a large stock decline is a stronger signal than buying during a rally. Always note price context.
- **Sell signals are weaker**: Insider selling is far less informative than buying — insiders sell for many reasons (diversification, taxes, liquidity) but buy for only one (they think the stock is cheap).
- **Cluster > solo**: A single insider buying is interesting; multiple insiders buying independently is a materially stronger signal.
- **Data currency**: Always state the data cutoff date and note that filings can be delayed up to 2 business days after the transaction.
- **Not a buy recommendation**: Insider buying is one signal among many. Always frame findings as informational, not as investment advice.
