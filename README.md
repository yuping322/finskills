# FinSkills — Financial Analysis Skills Collection

A comprehensive collection of Claude Skills for financial investment analysis, covering both US and China A-share markets, providing end-to-end analytical capabilities from value screening to portfolio construction.

## Overview

FinSkills provides 16 specialized skills (8 for US markets, 8 for A-share markets) designed to help investors and analysts make informed decisions through systematic, data-driven analysis. Each skill follows a consistent architecture with progressive disclosure to optimize context usage.

## Directory Structure

```
finskills/
├── US-market/          # US Market Skills (English)
│   ├── undervalued-stock-screener/
│   ├── insider-trading-analyzer/
│   ├── sentiment-reality-gap/
│   ├── dividend-aristocrat-calculator/
│   ├── tech-hype-vs-fundamentals/
│   ├── sector-rotation-detector/
│   ├── small-cap-growth-identifier/
│   └── risk-adjusted-return-optimizer/
├── China-market/       # A-Share Market Skills (Chinese)
│   ├── undervalued-stock-screener/
│   ├── insider-trading-analyzer/
│   ├── sentiment-reality-gap/
│   ├── high-dividend-strategy/
│   ├── tech-hype-vs-fundamentals/
│   ├── sector-rotation-detector/
│   ├── small-cap-growth-identifier/
│   └── risk-adjusted-return-optimizer/
├── README.md           # This file (English)
└── README_CN.md        # Chinese version
```

## Skills Overview

### US-market (US Stocks · English)

| # | Skill | Description | Directory |
|---|-------|-------------|-----------|
| 1 | **Undervalued Stock Screener** | Screen for fundamentally strong but undervalued companies using P/E, P/B, growth, and ROIC filters | [US-market/undervalued-stock-screener/](US-market/undervalued-stock-screener/) |
| 2 | **Insider Trading Analyzer** | Analyze insider trading patterns (Form 4 filings) to identify management confidence signals | [US-market/insider-trading-analyzer/](US-market/insider-trading-analyzer/) |
| 3 | **Sentiment-Reality Gap** | Identify contrarian opportunities where market sentiment diverges from fundamentals | [US-market/sentiment-reality-gap/](US-market/sentiment-reality-gap/) |
| 4 | **Dividend Aristocrat Calculator** | Evaluate dividend aristocrats (25+ years of increases) for income reliability and total return | [US-market/dividend-aristocrat-calculator/](US-market/dividend-aristocrat-calculator/) |
| 5 | **Tech Hype vs Fundamentals** | Separate tech stock hype from fundamental value using growth-valuation frameworks | [US-market/tech-hype-vs-fundamentals/](US-market/tech-hype-vs-fundamentals/) |
| 6 | **Sector Rotation Detector** | Detect sector rotation signals based on macroeconomic indicators (rates, inflation, GDP) | [US-market/sector-rotation-detector/](US-market/sector-rotation-detector/) |
| 7 | **Small-Cap Growth Identifier** | Discover overlooked small-cap growth companies (<$2B market cap) with strong fundamentals | [US-market/small-cap-growth-identifier/](US-market/small-cap-growth-identifier/) |
| 8 | **Risk-Adjusted Return Optimizer** | Construct optimized portfolios for specific risk profiles, time horizons, and capital sizes | [US-market/risk-adjusted-return-optimizer/](US-market/risk-adjusted-return-optimizer/) |

### China-market (A-Shares · Chinese)

| # | Skill Name | Description | Directory |
|---|-----------|-------------|-----------|
| 1 | **低估值股票筛选器** | Screen A-share market for fundamentally strong but undervalued companies | [China-market/undervalued-stock-screener/](China-market/undervalued-stock-screener/) |
| 2 | **董监高增减持分析器** | Analyze director/executive/shareholder trading activities for management confidence signals | [China-market/insider-trading-analyzer/](China-market/insider-trading-analyzer/) |
| 3 | **市场情绪与基本面偏差分析** | Identify contrarian opportunities where sentiment diverges from fundamentals | [China-market/sentiment-reality-gap/](China-market/sentiment-reality-gap/) |
| 4 | **高股息策略分析器** | Evaluate high-dividend A-share stocks for dividend sustainability and long-term returns | [China-market/high-dividend-strategy/](China-market/high-dividend-strategy/) |
| 5 | **科技股炒作vs基本面分析** | Distinguish between concept-driven hype and fundamental value in A-share tech stocks | [China-market/tech-hype-vs-fundamentals/](China-market/tech-hype-vs-fundamentals/) |
| 6 | **行业轮动信号探测器** | Identify sector rotation opportunities through macroeconomic indicator analysis | [China-market/sector-rotation-detector/](China-market/sector-rotation-detector/) |
| 7 | **小盘成长股发现器** | Discover overlooked small-cap growth companies (20-200B RMB market cap) | [China-market/small-cap-growth-identifier/](China-market/small-cap-growth-identifier/) |
| 8 | **风险调整收益优化器** | Construct optimized portfolios for Chinese investors with specific risk profiles | [China-market/risk-adjusted-return-optimizer/](China-market/risk-adjusted-return-optimizer/) |

## Skill Architecture

Each skill follows a consistent three-layer architecture:

```
skill-name/
├── SKILL.md                        # Main file: Trigger conditions, workflow, core guidance
└── references/
    ├── xxx-methodology.md          # Detailed methodology: Formulas, scoring criteria, industry benchmarks
    └── output-template.md          # Report template: Structured output format
```

### Progressive Disclosure Design

- **Always in context**: Only the YAML frontmatter (`name`, `description`) from `SKILL.md` is used for trigger detection
- **Loaded on trigger**: The `SKILL.md` body — workflow and core guidance
- **Loaded on demand**: Files in `references/` directory — detailed methodologies and templates loaded only when executing analysis

This design optimizes context window usage while providing complete analytical frameworks when needed.

## Market-Specific Design

China-market skills are not simple translations of US-market versions. They are comprehensively rewritten to address A-share market characteristics:

| Dimension | US-market | China-market |
|-----------|-----------|-------------|
| **Language** | English | Chinese |
| **Market Structure** | NYSE/NASDAQ, SEC regulation | SSE/SZSE/Beijing Stock Exchange, CSRC regulation |
| **Industry Classification** | GICS | Shenwan Industry Classification |
| **Insider Trading** | SEC Form 4 filings | Director/executive/shareholder trading announcements |
| **Dividends** | Quarterly dividends, Dividend Aristocrats | Annual dividends, CSI Dividend Index |
| **Tax System** | Capital gains tax, dividend tax | No capital gains tax, dividend tax tied to holding period |
| **Valuation Characteristics** | Mature market valuation levels | A-share premium, policy premium, shell value (declining) |
| **Policy Impact** | Fed policy, SEC regulation | State Council, PBOC, CSRC, industrial policy (extremely high weight) |
| **Capital Structure** | Institution-dominated | High retail trading share, northbound capital marginal impact |
| **Investment Tools** | ETFs, Options, REITs | ETFs, Convertible bonds, Public REITs, QDII |

## Usage Examples

### US-market Triggers

- *"Screen for undervalued stocks in the technology sector"*
- *"Analyze insider buying patterns in healthcare companies"*
- *"Build me a $100K moderate-risk portfolio for a 10-year horizon"*
- *"Identify tech stocks where hype exceeds fundamentals"*
- *"What sectors should outperform based on current macro indicators?"*
- *"Find small-cap growth stocks under $2B with strong fundamentals"*
- *"Calculate total return for dividend aristocrats with DRIP"*
- *"Identify stocks where sentiment is overly negative but fundamentals are strong"*

### China-market Triggers (Chinese)

- *"帮我筛选 A 股低估值股票"*
- *"分析最近有哪些公司董事长在大量增持"*
- *"当前宏观环境下应该超配哪些行业？"*
- *"用 30 万帮我构建一个稳健型投资组合"*
- *"科创板哪些公司估值泡沫最严重？"*
- *"帮我找几只被市场错杀的 A 股"*
- *"A 股有哪些高股息但分红可持续的标的？"*
- *"推荐几只市值小但增长快的专精特新公司"*

## Installation & Usage

These skills are designed for Claude (Anthropic's AI assistant). To use them:

1. **Install skills**: Place the skill directories in your Claude skills directory (typically `$CODEX_HOME/skills/` or similar)
2. **Trigger naturally**: Use natural language queries that match the skill descriptions
3. **Follow workflows**: Each skill will guide you through its analysis workflow
4. **Review references**: Detailed methodologies are available in `references/` subdirectories

## Contributing

Contributions are welcome! When adding new skills:

1. Follow the three-layer architecture (`SKILL.md` + `references/`)
2. Use progressive disclosure principles
3. Include comprehensive methodology documentation
4. Provide structured output templates
5. Add appropriate disclaimers

## Disclaimer

> **Important**: This skill collection is for informational and educational purposes only. It does not constitute investment advice, recommendations, or an offer to buy or sell any securities. All analyses are based on publicly available data and model assumptions, which may contain errors or omissions. Past performance does not guarantee future results. Investing involves risk, including possible loss of principal. Please consult a qualified investment advisor before making any investment decisions.

## License

[Specify license if applicable]

---

For the Chinese version, see [README_CN.md](README_CN.md).
