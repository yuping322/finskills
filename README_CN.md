# FinSkills — 金融分析技能集

一套面向金融投资分析的 Claude Skills 集合，覆盖美股和 A 股两大市场，提供从价值筛选到组合构建的全流程分析能力。

## 概述

FinSkills 提供 16 个专业技能（8 个美股技能，8 个 A 股技能），旨在通过系统化、数据驱动的分析帮助投资者和分析师做出明智决策。每个技能遵循一致的架构，采用渐进式加载设计以优化上下文使用。

## 目录结构

```
finskills/
├── US-market/          # 美股市场技能（英文）
│   ├── undervalued-stock-screener/
│   ├── insider-trading-analyzer/
│   ├── sentiment-reality-gap/
│   ├── dividend-aristocrat-calculator/
│   ├── tech-hype-vs-fundamentals/
│   ├── sector-rotation-detector/
│   ├── small-cap-growth-identifier/
│   └── risk-adjusted-return-optimizer/
├── China-market/       # A股市场技能（中文）
│   ├── undervalued-stock-screener/
│   ├── insider-trading-analyzer/
│   ├── sentiment-reality-gap/
│   ├── high-dividend-strategy/
│   ├── tech-hype-vs-fundamentals/
│   ├── sector-rotation-detector/
│   ├── small-cap-growth-identifier/
│   └── risk-adjusted-return-optimizer/
├── README.md           # 英文版本
└── README_CN.md        # 本文件（中文版本）
```

## 技能一览

### US-market（美股 · 英文）

| # | 技能名称 | 说明 | 目录 |
|---|---------|------|------|
| 1 | **Undervalued Stock Screener** | 使用 P/E、P/B、增长率和 ROIC 等指标筛选基本面强劲但被低估的公司 | [US-market/undervalued-stock-screener/](US-market/undervalued-stock-screener/) |
| 2 | **Insider Trading Analyzer** | 分析内部交易模式（Form 4 文件）以识别管理层信心信号 | [US-market/insider-trading-analyzer/](US-market/insider-trading-analyzer/) |
| 3 | **Sentiment-Reality Gap** | 识别市场情绪与基本面背离的逆向投资机会 | [US-market/sentiment-reality-gap/](US-market/sentiment-reality-gap/) |
| 4 | **Dividend Aristocrat Calculator** | 评估股息贵族（连续 25 年以上增长）的收入可靠性和总回报 | [US-market/dividend-aristocrat-calculator/](US-market/dividend-aristocrat-calculator/) |
| 5 | **Tech Hype vs Fundamentals** | 使用增长-估值框架区分科技股炒作与基本面价值 | [US-market/tech-hype-vs-fundamentals/](US-market/tech-hype-vs-fundamentals/) |
| 6 | **Sector Rotation Detector** | 基于宏观经济指标（利率、通胀、GDP）检测行业轮动信号 | [US-market/sector-rotation-detector/](US-market/sector-rotation-detector/) |
| 7 | **Small-Cap Growth Identifier** | 发现被忽视的小盘成长股（市值 < 20 亿美元） | [US-market/small-cap-growth-identifier/](US-market/small-cap-growth-identifier/) |
| 8 | **Risk-Adjusted Return Optimizer** | 为特定风险偏好、时间跨度和资金规模构建优化投资组合 | [US-market/risk-adjusted-return-optimizer/](US-market/risk-adjusted-return-optimizer/) |

### China-market（A 股 · 中文）

| # | 技能名称 | 说明 | 目录 |
|---|---------|------|------|
| 1 | **低估值股票筛选器** | 扫描A股市场，筛选基本面强劲但被低估的上市公司 | [China-market/undervalued-stock-screener/](China-market/undervalued-stock-screener/) |
| 2 | **董监高增减持分析器** | 分析董监高及重要股东增减持行为，识别管理层信心信号 | [China-market/insider-trading-analyzer/](China-market/insider-trading-analyzer/) |
| 3 | **市场情绪与基本面偏差分析** | 识别被过度看空但基本面稳健的逆向投资机会 | [China-market/sentiment-reality-gap/](China-market/sentiment-reality-gap/) |
| 4 | **高股息策略分析器** | 评估A股高股息股票的分红可持续性与长期回报 | [China-market/high-dividend-strategy/](China-market/high-dividend-strategy/) |
| 5 | **科技股炒作vs基本面分析** | 区分A股科技公司的概念炒作与基本面支撑 | [China-market/tech-hype-vs-fundamentals/](China-market/tech-hype-vs-fundamentals/) |
| 6 | **行业轮动信号探测器** | 通过宏观经济指标识别A股行业轮动机会 | [China-market/sector-rotation-detector/](China-market/sector-rotation-detector/) |
| 7 | **小盘成长股发现器** | 发现被市场忽视的小市值高成长A股公司（20-200 亿元市值） | [China-market/small-cap-growth-identifier/](China-market/small-cap-growth-identifier/) |
| 8 | **风险调整收益优化器** | 为中国投资者构建风险调整后收益最优的投资组合 | [China-market/risk-adjusted-return-optimizer/](China-market/risk-adjusted-return-optimizer/) |

## 技能架构

每个技能遵循统一的三层架构：

```
skill-name/
├── SKILL.md                        # 主文件：触发条件、工作流程、核心指引
└── references/
    ├── xxx-methodology.md          # 详细方法论：计算公式、评分标准、行业基准
    └── output-template.md          # 报告模板：结构化输出格式
```

### 渐进式加载（Progressive Disclosure）

- **始终在上下文中**：仅 `SKILL.md` 的 YAML frontmatter（`name`、`description`），用于判断是否触发
- **触发时加载**：`SKILL.md` 正文 — 工作流程、核心指引
- **按需加载**：`references/` 目录下的详细方法论和模板 — 仅在执行分析时读取

这种设计确保在不需要时节省上下文窗口，在需要时提供完整的分析框架。

## 市场差异化设计

China-market 技能并非简单翻译 US-market 版本，而是针对 A 股市场特性进行了全面重写：

| 维度 | US-market | China-market |
|------|-----------|-------------|
| **语言** | English | 中文 |
| **市场结构** | NYSE/NASDAQ、SEC 监管 | 沪深交易所/北交所、证监会监管 |
| **行业分类** | GICS | 申万行业分类 |
| **内部交易** | SEC Form 4 | 董监高增减持公告 |
| **分红** | 季度分红、Dividend Aristocrats | 年度分红、中证红利指数 |
| **税制** | 资本利得税、分红税 | 无资本利得税、分红税与持有期挂钩 |
| **估值特点** | 成熟市场估值中枢 | A股溢价、政策溢价、壳价值（下降中） |
| **政策影响** | 联储政策、监管 | 国务院、央行、证监会、产业政策（权重极高） |
| **资金结构** | 机构主导 | 散户交易占比高、北向资金边际影响大 |
| **投资工具** | ETFs、Options、REITs | ETF、可转债、公募 REITs、QDII |

## 使用示例

### US-market 触发示例（英文）

- *"Screen for undervalued stocks in the technology sector"*
- *"Analyze insider buying patterns in healthcare companies"*
- *"Build me a $100K moderate-risk portfolio for a 10-year horizon"*
- *"Identify tech stocks where hype exceeds fundamentals"*
- *"What sectors should outperform based on current macro indicators?"*
- *"Find small-cap growth stocks under $2B with strong fundamentals"*
- *"Calculate total return for dividend aristocrats with DRIP"*
- *"Identify stocks where sentiment is overly negative but fundamentals are strong"*

### China-market 触发示例（中文）

- *"帮我筛选 A 股低估值股票"*
- *"分析最近有哪些公司董事长在大量增持"*
- *"当前宏观环境下应该超配哪些行业？"*
- *"用 30 万帮我构建一个稳健型投资组合"*
- *"科创板哪些公司估值泡沫最严重？"*
- *"帮我找几只被市场错杀的 A 股"*
- *"A 股有哪些高股息但分红可持续的标的？"*
- *"推荐几只市值小但增长快的专精特新公司"*

## 安装与使用

这些技能专为 Claude（Anthropic 的 AI 助手）设计。使用方法：

1. **安装技能**：将技能目录放置在您的 Claude 技能目录中（通常为 `$CODEX_HOME/skills/` 或类似路径）
2. **自然触发**：使用与技能描述匹配的自然语言查询
3. **遵循工作流程**：每个技能将引导您完成其分析工作流程
4. **查阅参考资料**：详细方法论可在 `references/` 子目录中找到

## 贡献指南

欢迎贡献！添加新技能时请遵循：

1. 遵循三层架构（`SKILL.md` + `references/`）
2. 使用渐进式加载原则
3. 包含全面的方法论文档
4. 提供结构化输出模板
5. 添加适当的免责声明

## 免责声明

> **重要提示**：本技能集仅供信息参考和教育目的，不构成任何投资建议、推荐或买卖任何证券的要约。所有分析基于公开数据和模型假设，可能存在错误或遗漏。过往业绩不代表未来表现。投资有风险，入市需谨慎。在做出任何投资决策前，请咨询合格的投资顾问。

## 许可证

[如适用，请指定许可证]

---

英文版本请参阅 [README.md](README.md)。
