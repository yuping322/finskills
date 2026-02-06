# FinSkills — Financial Analysis Skills Collection

[English](README.md) | [中文](README_CN.md)

A comprehensive collection of Claude Skills for financial investment analysis, covering both US and China A-share markets, providing end-to-end analytical capabilities from value screening to portfolio construction, risk diagnostics, and institutional-grade documentation.

> 💡 **Explore More Skills**: FinSkills is part of the broader [OpenSkills](https://github.com/Geeksfino/openskills.git) ecosystem — a comprehensive collection of open-source Claude Skills covering diverse domains and use cases. Check it out for more specialized AI capabilities!

## Overview

FinSkills provides 28 specialized skills (14 for US markets, 14 for A-share markets) designed to help investors and analysts make informed decisions through systematic, data-driven analysis. Each skill follows a consistent architecture with progressive disclosure to optimize context usage.

The skills are organized into three analytical tiers:

| Tier | Skills | Purpose |
|------|--------|---------|
| **Discovery & Screening** | Undervalued Stock Screener, Insider Trading Analyzer, Sentiment-Reality Gap, Small-Cap Growth Identifier, Quant Factor Screener, ESG Screener | Find investment candidates |
| **Deep Analysis** | Dividend Aristocrat Calculator, Tech Hype vs Fundamentals, Sector Rotation Detector, Financial Statement Analyzer, Event-Driven Detector | Evaluate specific opportunities |
| **Portfolio & Documentation** | Risk-Adjusted Return Optimizer, Portfolio Health Check, Suitability Report Generator | Construct, monitor, and document |

## Related Projects

**OpenSkills** — A comprehensive collection of open-source Claude Skills covering diverse domains and use cases. If you're interested in exploring more skills beyond financial analysis, check out the [OpenSkills repository](https://github.com/Geeksfino/openskills.git) for a wide range of specialized AI capabilities and workflows.

## Directory Structure

```
finskills/
├── US-market/                          # US Market Skills (English)
│   ├── undervalued-stock-screener/     # Value screening
│   ├── insider-trading-analyzer/       # Insider signal analysis
│   ├── sentiment-reality-gap/          # Contrarian analysis
│   ├── dividend-aristocrat-calculator/ # Income investing
│   ├── tech-hype-vs-fundamentals/      # Tech valuation
│   ├── sector-rotation-detector/       # Macro/sector strategy
│   ├── small-cap-growth-identifier/    # Small-cap discovery
│   ├── risk-adjusted-return-optimizer/ # Portfolio construction
│   ├── portfolio-health-check/         # Portfolio diagnostics
│   ├── suitability-report-generator/   # Investment documentation
│   ├── financial-statement-analyzer/   # Financial deep dive
│   ├── event-driven-detector/          # Special situations
│   ├── quant-factor-screener/          # Multi-factor screening
│   └── esg-screener/                   # ESG analysis
├── China-market/                       # A-Share Market Skills (Chinese)
│   ├── undervalued-stock-screener/
│   ├── insider-trading-analyzer/
│   ├── sentiment-reality-gap/
│   ├── high-dividend-strategy/
│   ├── tech-hype-vs-fundamentals/
│   ├── sector-rotation-detector/
│   ├── small-cap-growth-identifier/
│   ├── risk-adjusted-return-optimizer/
│   ├── portfolio-health-check/         # 组合健康诊断
│   ├── suitability-report-generator/   # 投资适当性报告
│   ├── financial-statement-analyzer/   # 财务报表深度分析
│   ├── event-driven-detector/          # 事件驱动机会
│   ├── quant-factor-screener/          # 量化因子筛选
│   └── esg-screener/                   # ESG筛选
├── README.md                           # This file (English)
└── README_CN.md                        # Chinese version
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
| 9 | **Portfolio Health Check** | Diagnose risks in existing portfolios: concentration, correlation clusters, factor tilts, stress testing, liquidity | [US-market/portfolio-health-check/](US-market/portfolio-health-check/) |
| 10 | **Suitability Report Generator** | Generate institutional-grade investment documentation with rationale, risk disclosure, and client suitability assessment | [US-market/suitability-report-generator/](US-market/suitability-report-generator/) |
| 11 | **Financial Statement Analyzer** | Forensic-level single-company analysis: DuPont decomposition, earnings quality, Z-score, M-score, working capital | [US-market/financial-statement-analyzer/](US-market/financial-statement-analyzer/) |
| 12 | **Event-Driven Detector** | Identify mispricing from corporate events: M&A arbitrage, spinoffs, buybacks, restructurings, index changes | [US-market/event-driven-detector/](US-market/event-driven-detector/) |
| 13 | **Quant Factor Screener** | Systematic multi-factor screening (value, momentum, quality, low-vol, size, growth) with factor timing and crowding analysis | [US-market/quant-factor-screener/](US-market/quant-factor-screener/) |
| 14 | **ESG Screener** | ESG scoring, controversy screening, carbon analysis, governance quality, and responsible investing integration | [US-market/esg-screener/](US-market/esg-screener/) |

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
| 9 | **组合健康诊断** | Diagnose existing portfolio risks: concentration, correlation, factor tilts, A-share stress testing, liquidity with limit-up/down considerations | [China-market/portfolio-health-check/](China-market/portfolio-health-check/) |
| 10 | **投资适当性报告生成器** | Generate CSRC/SAC-aligned suitability reports with qualified investor verification (Science/Technology Board, Beijing Stock Exchange thresholds) | [China-market/suitability-report-generator/](China-market/suitability-report-generator/) |
| 11 | **财务报表深度分析** | Forensic analysis of A-share financials: CAS-specific red flags, related-party transactions, government subsidy dependency, goodwill impairment risk | [China-market/financial-statement-analyzer/](China-market/financial-statement-analyzer/) |
| 12 | **事件驱动机会识别器** | Analyze A-share corporate events: asset injections, SOE reform, share buyback programs, spin-offs, index rebalancing, lock-up expirations | [China-market/event-driven-detector/](China-market/event-driven-detector/) |
| 13 | **量化因子筛选器** | Multi-factor A-share screening with China-specific factors (turnover rate, northbound capital), factor timing via PMI/social financing data | [China-market/quant-factor-screener/](China-market/quant-factor-screener/) |
| 14 | **ESG筛选器** | ESG analysis with Chinese characteristics: dual-carbon goals, common prosperity framework, CSRC ESG disclosure requirements | [China-market/esg-screener/](China-market/esg-screener/) |

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
| **Accounting Standards** | US GAAP | CAS (Chinese Accounting Standards) |
| **Valuation Characteristics** | Mature market valuation levels | A-share premium, policy premium, shell value (declining) |
| **Policy Impact** | Fed policy, SEC regulation | State Council, PBOC, CSRC, industrial policy (extremely high weight) |
| **Capital Structure** | Institution-dominated | High retail trading share, northbound capital marginal impact |
| **Investment Tools** | ETFs, Options, REITs | ETFs, Convertible bonds, Public REITs, QDII |
| **Trading Mechanics** | T+0, no daily limits | T+1, 10%/20% daily price limits |
| **ESG Framework** | TCFD, SEC climate disclosure, shareholder activism | Dual carbon goals, common prosperity, CSRC ESG disclosure |
| **Suitability Regulation** | SEC Reg BI, FINRA Rule 2111 | CSRC Investor Suitability Management, qualified investor thresholds |
| **Corporate Events** | M&A, spinoffs, buybacks | Asset injections, SOE reform, backdoor listings (declining) |
| **Factor Premiums** | Standard academic factors | Low-vol anomaly very strong, turnover rate as unique factor |

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
- *"Review my portfolio for hidden risks and concentration issues"*
- *"Generate a suitability report for this portfolio recommendation"*
- *"Do a deep dive into Apple's financial statements"*
- *"What merger arbitrage opportunities are available right now?"*
- *"Screen stocks using a multi-factor model with value and quality"*
- *"Find the best ESG-rated companies in the S&P 500"*

### China-market Triggers (Chinese)

- *"帮我筛选 A 股低估值股票"*
- *"分析最近有哪些公司董事长在大量增持"*
- *"当前宏观环境下应该超配哪些行业？"*
- *"用 30 万帮我构建一个稳健型投资组合"*
- *"科创板哪些公司估值泡沫最严重？"*
- *"帮我找几只被市场错杀的 A 股"*
- *"A 股有哪些高股息但分红可持续的标的？"*
- *"推荐几只市值小但增长快的专精特新公司"*
- *"帮我诊断一下我的持仓有什么风险"*
- *"为这个投资建议生成一份适当性报告"*
- *"深度分析一下贵州茅台的财务报表"*
- *"最近有哪些A股并购重组机会？"*
- *"用多因子模型帮我筛选A股"*
- *"帮我找ESG评分最高的沪深300成分股"*

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
6. For China-market skills, fully rewrite (don't translate) for A-share market characteristics

## Disclaimer

> **Important**: This skill collection is for informational and educational purposes only. It does not constitute investment advice, recommendations, or an offer to buy or sell any securities. All analyses are based on publicly available data and model assumptions, which may contain errors or omissions. Past performance does not guarantee future results. Investing involves risk, including possible loss of principal. Please consult a qualified investment advisor before making any investment decisions.

## License

Copyright 2025 FinoGeeks Technology Ltd

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
