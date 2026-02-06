# Screening Methodology

Detailed criteria, thresholds, and edge cases for each screening filter.

## Table of Contents

1. [Valuation: P/E Ratio](#valuation-pe-ratio)
2. [Growth: Revenue & Earnings](#growth-revenue--earnings)
3. [Leverage: Debt-to-Equity](#leverage-debt-to-equity)
4. [Cash Flow: Free Cash Flow](#cash-flow-free-cash-flow)
5. [Returns: ROIC](#returns-roic)
6. [Upside: Analyst Consensus](#upside-analyst-consensus)
7. [Sector-Specific Adjustments](#sector-specific-adjustments)
8. [Data Sources & Verification](#data-sources--verification)

## Valuation: P/E Ratio

**Primary criterion**: Trailing P/E or forward P/E below the company's industry average.

**Nuances**:
- Use forward P/E when consensus estimates are available from ≥3 analysts
- For cyclical industries (e.g., autos, commodities, semiconductors), prefer P/E normalized over a full business cycle (Shiller-style or 5-year average earnings)
- Exclude companies with negative earnings — screen on EV/EBITDA instead (threshold: below industry median)
- Watch for earnings distortions: one-time gains/charges, accounting changes, stock-based compensation dilution
- For high-growth companies, supplement with PEG ratio < 1.0

**Red flags to disqualify**:
- P/E is low solely due to a one-time earnings spike
- Earnings are declining and P/E compression is masking deterioration

## Growth: Revenue & Earnings

**Primary criterion**: Positive revenue and EPS growth in at least 3 of the last 5 fiscal years.

**Preferred thresholds**:
- Revenue CAGR ≥ 5% over 3–5 years
- EPS CAGR ≥ 7% over 3–5 years
- Gross margin stable or expanding

**Nuances**:
- Allow one "down" year if caused by a clearly identifiable and non-recurring event (e.g., COVID, one-time restructuring)
- For companies in turnaround, require at least 2 consecutive years of improvement plus forward estimates showing continuation
- Organic growth is preferred — flag acquisitions-driven growth and check ROIC on acquired capital
- Check revenue quality: recurring vs. one-time, customer concentration

## Leverage: Debt-to-Equity

**Primary criterion**: Debt-to-equity ratio below the sector median.

**Calculation**: Total debt (short-term + long-term) / total shareholders' equity.

**Sector-adjusted thresholds** (examples):
| Sector | Typical D/E Range | Max Acceptable |
|--------|-------------------|----------------|
| Technology | 0.0–0.5 | 0.8 |
| Healthcare | 0.2–0.8 | 1.2 |
| Industrials | 0.3–1.0 | 1.5 |
| Consumer Staples | 0.5–1.5 | 2.0 |
| Utilities | 1.0–2.0 | 2.5 |
| Financials | Use Tier 1 Capital Ratio instead | — |
| REITs | Use Debt/Total Assets instead | 0.55 |

**Nuances**:
- Exclude financial companies from standard D/E screening; use Tier 1 capital ratio or CET1 ratio instead
- Check interest coverage ratio (EBIT/Interest Expense) ≥ 3x as a supplementary filter
- Distinguish between operating leases (IFRS 16 / ASC 842) and financial debt
- Assess debt maturity profile — near-term maturities in a rising rate environment are riskier

## Cash Flow: Free Cash Flow

**Primary criterion**: Positive FCF in each of the last 3 years, with a growing trend.

**Calculation**: Operating cash flow − capital expenditures.

**Preferred thresholds**:
- FCF yield (FCF / market cap) ≥ 4%
- FCF margin (FCF / revenue) stable or expanding
- FCF conversion ratio (FCF / net income) ≥ 0.8

**Nuances**:
- Distinguish between maintenance capex and growth capex — high capex for expansion is not inherently negative
- For capital-intensive industries (e.g., telecom, utilities), use FCFE (free cash flow to equity) after debt service
- Check for working capital manipulation: sudden reductions in receivables/inventory that artificially inflate operating cash flow
- Owner earnings (Buffett's definition) may be more appropriate for businesses with lumpy capex

## Returns: ROIC

**Primary criterion**: ROIC above the industry average, sustained over 3+ years.

**Calculation**: NOPAT / invested capital, where:
- NOPAT = Operating income × (1 − tax rate)
- Invested capital = Total equity + total debt − excess cash

**Preferred thresholds**:
- ROIC ≥ WACC (value creation test)
- ROIC ≥ 12% for most industries (exceptional: ≥ 20%)
- ROIC trend stable or improving

**Nuances**:
- Adjust for goodwill and intangibles from acquisitions — calculate ROIC both with and without goodwill to assess organic capital efficiency
- For asset-light businesses (e.g., software, consulting), ROIC may be very high but less meaningful — supplement with revenue growth and margin analysis
- Compare ROIC to cost of capital: a company with 15% ROIC and 12% WACC creates less value than one with 10% ROIC and 5% WACC

## Upside: Analyst Consensus

**Primary criterion**: Consensus 12-month price target implies ≥ 30% upside from current price.

**Nuances**:
- Require coverage from ≥ 3 analysts to ensure meaningful consensus
- Weight toward estimates from analysts with strong track records on the specific sector
- Check for estimate dispersion — if the range is very wide, consensus is weak
- Consider the direction of revisions: recent upward revisions are more bullish than stale targets
- Be skeptical of very high consensus upside (>80%) — may indicate distressed situation or speculative coverage

**Supplementary check**: Sum-of-the-parts (SOTP) or discounted cash flow (DCF) valuation to cross-validate analyst targets.

## Sector-Specific Adjustments

Different sectors require different screening approaches:

- **Financials**: Replace P/E with P/Book, D/E with capital adequacy, FCF with pre-provision profit growth
- **REITs**: Use P/FFO (funds from operations), Debt/Total Assets, AFFO yield
- **Biotech/Pharma**: Pre-revenue companies need pipeline-based valuation; exclude from standard earnings screens
- **Commodities/Mining**: Use EV/EBITDA over P/E; assess reserve life and all-in sustaining costs
- **Technology**: Weight growth and TAM expansion more heavily; accept higher valuations for proven SaaS metrics (NRR > 120%, Rule of 40)

## Data Sources & Verification

When presenting data, always:

1. State the source or basis (e.g., "based on trailing twelve months as of Q3 2025 filings")
2. Note if using estimates vs. actuals
3. Flag any data points that could not be independently verified
4. Use the most recently available quarterly or annual filings
5. Cross-reference at least 2 sources for key metrics when possible
