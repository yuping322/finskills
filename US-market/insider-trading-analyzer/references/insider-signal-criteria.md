# Insider Signal Criteria

Detailed filtering criteria, scoring methodology, and edge cases for insider trading pattern analysis.

## Table of Contents

1. [Transaction Type Classification](#transaction-type-classification)
2. [Cluster Buying Detection](#cluster-buying-detection)
3. [Meaningfulness Assessment](#meaningfulness-assessment)
4. [Signal Strength Scoring](#signal-strength-scoring)
5. [Red Flags & False Positives](#red-flags--false-positives)
6. [Data Sources & Filing Types](#data-sources--filing-types)

## Transaction Type Classification

### Include (Discretionary Purchases)

| Code | Description | Signal Strength |
|------|-------------|-----------------|
| P | Open-market purchase | Strong |
| P (direct) | Open-market purchase, direct ownership | Strongest |
| P (indirect) | Open-market purchase via trust/family | Strong |

### Exclude (Non-Discretionary / Non-Informative)

| Code | Description | Why Exclude |
|------|-------------|-------------|
| A | Award/grant | Compensation, not conviction |
| M | Option exercise | Often mechanical, tax-driven |
| F | Tax withholding on vesting | Forced transaction |
| G | Gift | Estate/tax planning |
| S (10b5-1) | Automatic plan sale | Pre-programmed, no timing signal |
| J | Other (misc.) | Ambiguous signal |
| D | Disposition to issuer | Often buyback-related |

### Edge Cases

- **Option exercise + hold**: If insider exercises options AND does not sell the underlying shares, treat as moderately bullish — they chose to deploy capital and maintain exposure.
- **10b5-1 plan adoption/termination**: Adoption of a new selling plan is mildly bearish; termination of an existing selling plan is mildly bullish.
- **Secondary offerings participation**: Insiders buying in a secondary offering shows conviction but at a known discount — weight less than open-market buys.

## Cluster Buying Detection

### Definition

Cluster buying = ≥ 2 distinct insiders making open-market purchases within the specified time window.

### Scoring Tiers

| Tier | Criteria | Signal |
|------|----------|--------|
| Exceptional | ≥ 4 insiders buying, including CEO or CFO | Very Strong |
| Strong | 3 insiders buying, at least one C-suite | Strong |
| Moderate | 2 insiders buying | Moderate |
| Weak | 1 insider buying (informational only) | Weak |

### Seniority Weighting

Not all insiders carry equal informational advantage:

| Role | Weight | Rationale |
|------|--------|-----------|
| CEO | 5x | Broadest strategic visibility |
| CFO | 4x | Deepest financial visibility |
| COO / President | 4x | Operational visibility |
| Other C-suite (CTO, CMO, etc.) | 3x | Functional visibility |
| SVP / EVP | 2x | Business unit visibility |
| Director (Board) | 2x | Governance-level oversight |
| VP / Other officer | 1.5x | Moderate visibility |
| 10%+ beneficial owner | 1x | May have different motivations |

### Temporal Clustering

Tighter clustering within the window is a stronger signal:

- All purchases within 2 weeks: **Strong cluster** — suggests a shared catalyst or information set
- Purchases spread over 30–60 days: **Moderate cluster** — consistent but less urgent
- Purchases spread over 60–90 days: **Weak cluster** — may be coincidental

## Meaningfulness Assessment

A $10,000 purchase by a CEO earning $15M is noise. A $500,000 purchase is a signal. Assess meaningfulness using:

### Relative to Compensation

| Purchase as % of Annual Compensation | Assessment |
|--------------------------------------|------------|
| > 100% | Exceptional conviction |
| 50–100% | Very meaningful |
| 25–50% | Meaningful |
| 10–25% | Moderate |
| < 10% | Likely immaterial |

### Relative to Existing Holdings

| Purchase as % of Existing Holdings | Assessment |
|------------------------------------|------------|
| > 50% (doubling down) | Exceptional conviction |
| 25–50% | Very meaningful increase |
| 10–25% | Meaningful increase |
| < 10% | Incremental addition |

### Absolute Dollar Thresholds

As a secondary filter:
- **> $1M**: Always meaningful regardless of compensation
- **$250K–$1M**: Meaningful for most executives
- **$100K–$250K**: Meaningful for directors, mid-level officers
- **< $100K**: Only meaningful if compensation is also modest

### New Position vs. Addition

- **First-ever purchase**: Stronger signal — insider is initiating a new position with personal capital
- **Addition to existing position**: Still positive, but less novel

## Signal Strength Scoring

Combine factors into an overall signal score:

```
Signal Score = Cluster Tier × Seniority Weight × Meaningfulness × Context Multiplier
```

### Context Multipliers

| Context | Multiplier | Rationale |
|---------|------------|-----------|
| Buying into 52-week low / after >20% decline | 1.5x | Contrarian conviction |
| Buying during sector-wide selloff | 1.3x | Stock-specific conviction despite macro fear |
| Buying ahead of known catalyst (earnings, FDA, etc.) | 1.2x | Potentially informed timing |
| Buying during price rally | 0.8x | May be momentum chasing |
| Buying right after positive earnings | 0.7x | Information already public |
| New CEO/CFO buying immediately after appointment | 0.6x | Often signaling/optics, not deep conviction |

## Red Flags & False Positives

Always check for these patterns that may weaken the bullish signal:

### Diluted Signal

- **Coordinated signaling**: Board may collectively agree to buy as a PR exercise after bad news — check if buys are suspiciously uniform in size and timing
- **Contractual obligations**: Some employment agreements require minimum stock ownership — buying may be compliance, not conviction
- **Wash activity**: Insider sold larger amounts recently and is buying back a fraction — net position is still reduced

### Counter-Signals

- **Simultaneous selling by other insiders**: If some insiders are buying while others sell, the signal is ambiguous
- **10b5-1 plan adoption by the same insider**: If an insider buys and then adopts a selling plan, bullish signal is negated
- **Company buyback announcement**: Insider buying concurrent with a buyback may reflect coordination rather than independent conviction

### Structural Concerns

- **Low-liquidity stocks**: Insider buying in micro/nano-cap stocks may be designed to prop up the price
- **Pre-capital-raise buying**: Insiders buying before an equity issuance may be trying to stabilize the price
- **Regulatory scrutiny**: Check if the company is under SEC investigation — insider buying during investigations can be a diversionary tactic

## Data Sources & Filing Types

### Primary Sources

- **SEC EDGAR** — Form 4 filings (US companies)
  - Filed within 2 business days of transaction
  - Includes transaction type, price, shares, ownership form
- **SEDI (Canada)** — Insider trading reports for TSX-listed companies
- **UK FCA** — PDMR (Persons Discharging Managerial Responsibilities) notifications

### Filing Interpretation

- **Form 4**: Standard insider transaction report; primary data source
- **Form 3**: Initial statement of beneficial ownership (new insider); informational only
- **Form 5**: Annual summary of transactions that should have been on Form 4; may indicate late filings
- **Schedule 13D/G**: Beneficial ownership > 5%; relevant for activist investors, not standard insiders

### Timing Notes

- Transactions must be reported within 2 business days (Form 4)
- Some filings are amended — always check for amendments that change transaction details
- Holiday/weekend transactions may have filing delays
