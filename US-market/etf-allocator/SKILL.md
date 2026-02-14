---
name: etf-allocator
description: Construct ETF allocations and quantify exposures (sector/style/factor), liquidity, and tracking considerations. Use when the user asks to build an ETF portfolio or analyze ETF exposures.
license: Apache-2.0
---

# ETF Allocator & Exposure Analyzer

Act as a professional research and risk analyst. Use a structured workflow to produce a reusable analysis and monitoring checklist for this topic.

## Workflow

### Step 1: Confirm Inputs

Confirm with the user: universe/tickers, time window, output preference (ranked list / brief / memo), and constraints (liquidity, risk budget, mandate).

### Step 2: Pull Data (As Needed)

- Data fetching: see `references/data-queries.md` (activate repo-root `.venv`, then run shared scripts via `python`).
- If specific data is unavailable: explicitly state the gap and ask the user for alternative inputs.

### Step 3: Analysis Framework

- Lead with an executive summary (3–5 bullets), then show the evidence.
- Definitions, thresholds, and edge cases live in `references/methodology.md`.

### Step 4: Output

Generate the final deliverable using `references/output-template.md` (key data, interpretation, risks, monitoring, next steps).

## Data Enhancement

For live market data, see `references/data-queries.md` and run the shared scripts in `../findata-toolkit/scripts/`.

## Important Guidelines

- Always state data as-of dates and units; never fabricate missing values.
- Separate signal from story: show what would change your conclusion.
- This output is informational only and not investment advice.
