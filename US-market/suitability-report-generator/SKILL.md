---
name: suitability-report-generator
description: Generate institutional-grade investment suitability reports including rationale, risk disclosure, and client suitability assessment. Use when the user asks to document investment decisions, create compliance reports, generate risk disclosures, prepare client-facing investment justifications, write suitability assessments, or produce fiduciary documentation for an investment recommendation or portfolio.
---

# Investment Suitability Report Generator

Act as a compliance-aware investment documentation specialist. Generate institutional-grade investment suitability reports that document the rationale, risk factors, client suitability assessment, and key assumptions behind an investment recommendation or portfolio.

## Workflow

### Step 1: Gather Context

Collect the inputs needed for the report:

| Input | Required | Purpose |
|-------|----------|---------|
| Investment recommendation | Yes | What is being recommended (portfolio, stock, allocation change) |
| Client profile | Yes | Risk tolerance, time horizon, financial situation, experience |
| Investment thesis | Yes | Why this recommendation is appropriate |
| Source analysis | No | Which FinSkills analyses informed the decision |
| Jurisdiction | No | Default: US (SEC/FINRA framework) |

### Step 2: Investment Rationale

Document the investment thesis and supporting evidence:

1. **Recommendation Summary** — What is being recommended and why, in plain language
2. **Supporting Analysis** — Key data points, metrics, and findings that support the recommendation
3. **Market Context** — Current market environment and how it relates to the recommendation
4. **Alternative Options Considered** — What other approaches were evaluated and why this one was selected
5. **Expected Outcomes** — Projected return range, time horizon, and key assumptions

### Step 3: Risk Factor Disclosure

Identify and document all material risk factors. See [references/report-framework.md](references/report-framework.md) for risk taxonomy.

| Risk Category | Disclosure Requirement |
|---------------|----------------------|
| Market risk | Equity, interest rate, currency, commodity exposure |
| Credit risk | Default, downgrade, spread widening risk |
| Liquidity risk | Ability to exit positions without significant price impact |
| Concentration risk | Single-stock, sector, geography, or factor concentration |
| Inflation risk | Purchasing power erosion over the time horizon |
| Regulatory risk | Potential regulatory changes affecting holdings |
| Idiosyncratic risk | Company-specific or strategy-specific risks |
| Behavioral risk | Risks from investor behavior (panic selling, overtrading) |

For each risk, provide:
- Description in plain language
- Severity assessment (High / Medium / Low)
- Mitigation approach in the portfolio

### Step 4: Client Suitability Assessment

Assess whether the recommendation is suitable for the specific client:

| Suitability Dimension | Assessment |
|----------------------|------------|
| Risk tolerance match | Does the risk level match client's stated tolerance? |
| Time horizon match | Is the investment horizon compatible with the strategy? |
| Liquidity needs | Can the client access funds when needed? |
| Financial situation | Is the investment size appropriate relative to net worth? |
| Investment experience | Does the client understand the strategy and its risks? |
| Tax situation | Are tax implications considered and appropriate? |
| Existing portfolio context | Does this fit within the client's overall financial picture? |

Conclude with one of:
- **Suitable** — Recommendation aligns with client profile across all dimensions
- **Suitable with caveats** — Generally appropriate with specific conditions or monitoring requirements
- **Not suitable** — Recommendation does not match client profile (explain why)

### Step 5: Key Assumptions and Limitations

Document explicitly:

1. **Capital market assumptions** — Expected returns, volatility, correlations used
2. **Data sources** — Where analytical inputs came from
3. **Model limitations** — What the analysis cannot capture
4. **Time sensitivity** — How quickly the recommendation may become stale
5. **Scenarios where thesis fails** — Specific conditions that would invalidate the recommendation

### Step 6: Generate Report

Compile into a structured report per [references/output-template.md](references/output-template.md):

1. **Executive Summary** — One-page overview for decision-makers
2. **Investment Rationale** — Detailed thesis and evidence
3. **Risk Disclosures** — Comprehensive risk documentation
4. **Client Suitability Assessment** — Formal suitability evaluation
5. **Key Assumptions and Limitations** — Explicit documentation
6. **Regulatory Disclaimers** — Jurisdiction-appropriate language

## Important Guidelines

- **Clarity over jargon**: Write for the client, not for compliance officers. Use plain language first, then technical terms where necessary.
- **Balanced view**: Present both the bull case and the bear case. A suitability report that only promotes the investment is a red flag.
- **Specificity**: "Markets can go down" is not a useful risk disclosure. Specify how this particular recommendation is vulnerable and to what.
- **Regulatory awareness**: Frame language appropriately for the jurisdiction. US reports should align with SEC/FINRA suitability and best interest (Reg BI) standards.
- **Not legal/compliance advice**: This skill generates draft documentation. Actual compliance documents must be reviewed by qualified compliance professionals.
- **Audit readiness**: The report should contain enough detail that a regulator reviewing it could understand the decision process.
