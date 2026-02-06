---
name: financial-statement-analyzer
description: Perform forensic-level analysis of a single company's financial statements, evaluating earnings quality, financial health, fraud risk, and operational efficiency. Use when the user asks for a deep dive into a company's financials, DuPont analysis, earnings quality check, balance sheet analysis, cash flow analysis, Altman Z-score, Beneish M-score, working capital analysis, or any detailed single-company financial examination.
license: Apache-2.0
---

# Financial Statement Deep Dive

Act as a forensic financial analyst. Perform comprehensive analysis of a single company's financial statements to evaluate earnings quality, financial health, fraud risk indicators, and operational efficiency.

## Workflow

### Step 1: Identify the Target

Confirm with the user:

1. **Company** — Ticker or name
2. **Time period** — Default: most recent 5 years (20 quarters)
3. **Focus areas** — Full analysis (default) or specific focus (earnings quality, fraud risk, working capital, etc.)
4. **Comparison** — Key competitor(s) for benchmarking (optional)
5. **Data source** — SEC filings (10-K, 10-Q) as primary source

### Step 2: Profitability Decomposition

Perform 5-factor DuPont analysis. See [references/analysis-methodology.md](references/analysis-methodology.md) for formulas.

```
ROE = Tax Burden × Interest Burden × Operating Margin × Asset Turnover × Equity Multiplier
```

| Component | Formula | What It Reveals |
|-----------|---------|----------------|
| Tax burden | Net income / Pre-tax income | Tax efficiency |
| Interest burden | Pre-tax income / EBIT | Debt cost impact |
| Operating margin | EBIT / Revenue | Operational efficiency |
| Asset turnover | Revenue / Total assets | Asset utilization |
| Equity multiplier | Total assets / Equity | Financial leverage |

Track each component over 5 years to identify what is driving ROE changes.

### Step 3: Earnings Quality Assessment

Evaluate whether reported earnings reflect genuine economic value:

| Test | What It Measures | Red Flag Threshold |
|------|-----------------|-------------------|
| Accruals ratio | Non-cash earnings proportion | > 10% of total assets |
| Cash conversion | Operating cash flow / Net income | < 0.8 persistently |
| Revenue recognition | Revenue growth vs receivables growth | Receivables growing faster |
| Deferred revenue | Trend in deferred revenue | Declining (front-loaded revenue) |
| Non-recurring items | One-time gains/charges frequency | "Non-recurring" items every year |
| Change in estimates | Depreciation, reserves, assumptions | Consistently income-boosting changes |

### Step 4: Financial Health Scoring

Calculate composite financial health indicators:

| Model | Purpose | Components |
|-------|---------|-----------|
| Altman Z-Score | Bankruptcy prediction | Working capital, retained earnings, EBIT, market cap, sales — all relative to total assets |
| Piotroski F-Score | Financial strength | 9 binary signals across profitability, leverage, and efficiency |
| Beneish M-Score | Earnings manipulation detection | 8 variables measuring anomalies in financial data |

See [references/analysis-methodology.md](references/analysis-methodology.md) for detailed formulas and interpretation.

### Step 5: Working Capital Analysis

Examine operational efficiency through the cash conversion cycle:

| Metric | Formula | What It Reveals |
|--------|---------|----------------|
| DSO (Days Sales Outstanding) | (Receivables / Revenue) × 365 | Collection efficiency |
| DIO (Days Inventory Outstanding) | (Inventory / COGS) × 365 | Inventory management |
| DPO (Days Payable Outstanding) | (Payables / COGS) × 365 | Payment practices |
| Cash Conversion Cycle | DSO + DIO − DPO | Working capital efficiency |

Track trends over 5 years and compare to peers.

### Step 6: Balance Sheet Risk Assessment

Identify off-balance-sheet and hidden risks:

| Risk Area | What to Check |
|-----------|---------------|
| Goodwill / Intangibles | Size relative to equity; impairment risk |
| Operating leases | Off-balance-sheet obligations (pre-ASC 842) |
| Pension obligations | Funded status, discount rate assumptions |
| Contingent liabilities | Litigation, guarantees, commitments |
| Variable interest entities | Unconsolidated entities |
| Share-based compensation | Dilution impact |
| Debt maturity profile | Near-term maturities vs cash/refinancing capacity |

### Step 7: Segment Analysis

Break down performance by business segment:

- Revenue and growth by segment
- Operating margin by segment
- Capital intensity by segment
- Identify which segments drive value and which destroy it
- Cross-subsidization between segments

### Step 8: Peer Benchmarking

Compare key metrics against 2–3 direct competitors:

| Metric Category | Metrics |
|----------------|---------|
| Profitability | Gross margin, operating margin, net margin, ROE, ROIC |
| Efficiency | Asset turnover, inventory turnover, receivables turnover |
| Leverage | Debt/equity, interest coverage, net debt/EBITDA |
| Valuation | P/E, EV/EBITDA, P/FCF, PEG |
| Growth | Revenue CAGR, EPS CAGR, FCF CAGR |

### Step 9: Synthesize and Present

Compile findings per [references/output-template.md](references/output-template.md):

1. **Company Overview** — Business summary and key metrics
2. **DuPont Decomposition** — 5-year ROE driver analysis
3. **Earnings Quality Report** — Accruals, cash conversion, red flags
4. **Financial Health Scores** — Z-Score, F-Score, M-Score with interpretation
5. **Working Capital Analysis** — CCC trend and peer comparison
6. **Balance Sheet Risk Map** — Hidden risks and off-balance-sheet items
7. **Segment Analysis** — Value drivers and detractors
8. **Peer Comparison** — Benchmarking table
9. **Overall Assessment** — Synthesis of bull/bear case from financial perspective
10. **Disclaimers**

## Important Guidelines

- **Read the footnotes**: The most important information in financial statements is often in the footnotes. Flag any unusual accounting policies, related-party transactions, or significant estimates.
- **Trends matter more than levels**: A declining operating margin is more concerning than a low-but-stable one. Always emphasize directional changes.
- **Context is essential**: A high debt/equity ratio means different things for a utility vs a tech company. Always interpret metrics within industry context.
- **Complement, don't replace, valuation**: This skill assesses financial quality, not whether the stock is a buy or sell. Direct valuation questions to the appropriate screening skills.
- **GAAP vs non-GAAP**: Many companies report "adjusted" earnings that exclude stock-based compensation, restructuring, and other real costs. Always anchor to GAAP, then discuss adjustments.
- **Not an audit**: This is analytical review, not a professional audit. It cannot detect sophisticated fraud or verify data accuracy.
