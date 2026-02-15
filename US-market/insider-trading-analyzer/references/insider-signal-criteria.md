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

---

## Technical Notes & Implementation Details

### Legal and Regulatory Distinction

**IMPORTANT**: This analysis focuses on **legal insider trading** (SEC Form 4 filings), not illegal insider trading. Legal insider trading refers to transactions by corporate insiders (officers, directors, 10%+ owners) that are properly disclosed to the public. These transactions can provide valuable signals about insiders' view of company prospects.

### Data Timeliness Considerations

- **Filing Deadline**: Form 4 must be filed within 2 business days of the transaction
- **Processing Lag**: Data aggregators may have additional 1-2 day processing delay
- **Effective Signal Age**: By the time you receive the signal, the transaction may be 3-5 days old
- **Market Impact**: Significant insider buying often moves the price immediately after filing

### Context Importance

The same transaction can have different meanings depending on context:

**Strong Signal Contexts**:
- After >20% stock price decline
- During sector-wide selloffs
- Before known positive catalysts
- When insiders have historically good timing

**Weak Signal Contexts**:
- After positive earnings announcements
- During strong price rallies
- When immediately following new executive appointments
- When company has active buyback program

### Signal Validation Framework

Before acting on insider signals, validate through:

1. **Historical Accuracy**: Track this insider's past transactions and subsequent stock performance
2. **Cluster Consistency**: Multiple insiders buying around the same time is stronger than single insider
3. **Size Significance**: Large purchases relative to compensation and existing holdings
4. **Strategic Timing**: Buying before known catalysts or after negative news
5. **Absence of Counter-signals**: No simultaneous selling by other insiders

---

## Backtest Framework

### Backtest Design

**Objective**: Test whether insider buying signals predict future stock outperformance.

**Methodology**:
1. **Signal Generation**: Identify all insider purchases meeting criteria (open-market, meaningful size, cluster buying)
2. **Portfolio Construction**: Equal-weight portfolio of all stocks with active signals
3. **Holding Period**: Hold for 3 months, 6 months, and 12 months (separate tests)
4. **Benchmark**: Compare against SPY and relevant sector ETFs
5. **Frequency**: Rebalance weekly (new signals added, expired signals removed)

### Performance Metrics

- **Cumulative Returns**: Total return over holding period
- **Alpha**: Excess return vs benchmark (CAPM alpha)
- **Hit Rate**: Percentage of signals with positive returns
- **Average Win/Loss**: Mean positive vs negative return
- **Sharpe Ratio**: Risk-adjusted performance
- **Max Drawdown**: Worst peak-to-trough decline

### Statistical Tests

- **t-test**: Test if mean returns are significantly different from zero
- **Bootstrap**: Resample returns to assess robustness
- **Factor Analysis**: Control for market, size, value, momentum factors
- **Subperiod Analysis**: Test performance across different market regimes

### Falsification Criteria

A signal rule fails if:
- Hit rate <= 52% (not better than random)
- Alpha not statistically significant (t-stat < 1.96)
- Underperforms benchmark in > 60% of rolling 12-month periods
- Performance deteriorates in recent years (suggests pattern detection by market)

### Robustness Checks

**Alternative Specifications**:
- Vary holding periods (1 month, 3 months, 6 months, 12 months)
- Different signal strength thresholds (minimum purchase size, cluster requirements)
- Sector-specific tests (tech, healthcare, financials, etc.)
- Market cap segments (large-cap vs small-cap)

**Data Quality Tests**:
- Exclude micro-caps (< $300M market cap) where manipulation is more common
- Test with/without 10b5-1 plan transactions
- Compare real-time vs backfilled data performance

### Expected Results (Based on Academic Literature)

**Typical Findings**:
- Insider buying shows modest outperformance (2-4% annualized alpha)
- Stronger for small-cap stocks (less analyst coverage)
- Cluster buying outperforms individual insider buying
- Contrarian buying (after price declines) is most effective
- Signals weaken as more participants detect them

**Realistic Expectations**:
- Not all signals will be profitable
- Hit rate typically 55-65% (not 80-90%)
- Performance varies by market environment
- Transaction costs can erode returns for small-cap signals

### Implementation Notes

**Data Requirements**:
- Complete Form 4 filing history (2000-present recommended)
- Insider compensation data for meaningfulness assessment
- Historical stock prices and benchmark data
- Corporate action adjustments (splits, dividends, spin-offs)

**Computational Considerations**:
- Process ~10,000 Form 4 filings per month
- Need efficient database for insider historical performance
- Real-time processing pipeline for signal generation
- Automated portfolio rebalancing system

**Risk Management**:
- Position sizing based on signal strength and stock liquidity
- Stop-loss rules for signals that deteriorate quickly
- Diversification across multiple signals to reduce idiosyncratic risk
- Monitor for signal decay (alpha decreasing over time)

### Monitoring and Maintenance

**Quarterly Reviews**:
- Update signal accuracy statistics
- Adjust thresholds based on recent performance
- Review sector-specific effectiveness
- Monitor for regulatory changes affecting filings

**Annual Reviews**:
- Comprehensive backtest refresh with latest data
- Compare performance against academic benchmarks
- Assess whether signals remain profitable after costs
- Consider model enhancements or retirement of ineffective rules
