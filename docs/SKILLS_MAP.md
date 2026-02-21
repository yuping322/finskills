# Skills Map - 技能索引地图

本文档提供所有 skills 的完整索引，方便大模型和用户快速查找和管理技能。

## 文档结构说明

每个 skill 包含以下标准文件：
- `SKILL.md` - 技能说明、工作流程、使用指南
- `LICENSE.txt` - 许可证信息
- `references/` - 参考文档目录
  - `methodology.md` - 方法论、指标定义、阈值说明
  - `data-queries.md` - 数据获取方式、脚本调用说明
  - `output-template.md` - 输出格式模板

## 快速导航

- [中国市场 Skills (China-market)](#中国市场-skills-china-market)
  - [风险监控类](#风险监控类-risk-monitoring)
  - [市场分析类](#市场分析类-market-analysis)
  - [投资组合类](#投资组合类-portfolio-management)
  - [研究工具类](#研究工具类-research-tools)
  - [数据工具类](#数据工具类-data-toolkits)
- [香港市场 Skills (HK-market)](#香港市场-skills-hk-market)
  - [风险监控类](#hk-风险监控类-risk-monitoring)
  - [市场分析类](#hk-市场分析类-market-analysis)
  - [研究工具类](#hk-研究工具类-research-tools)
  - [数据工具类](#hk-数据工具类-data-toolkits)
- [美国市场 Skills (US-market)](#美国市场-skills-us-market)
  - [风险监控类](#us-风险监控类-risk-monitoring)
  - [市场分析类](#us-市场分析类-market-analysis)
  - [投资组合类](#us-投资组合类-portfolio-management)
  - [研究工具类](#us-研究工具类-research-tools)
  - [数据工具类](#us-数据工具类-data-toolkits)

---

## 中国市场 Skills (China-market)

### 风险监控类 (Risk Monitoring)

| Skill Name | 目录 | 描述 | 关键词 |
|-----------|------|------|--------|
| ST退市风险扫描器 | `st-delist-risk-scanner` | 监控ST、*ST、退市风险警示股票 | ST, 退市, 风险警示 |
| 股权质押风险监控 | `equity-pledge-risk-monitor` | 跟踪大股东质押比例、平仓风险 | 质押, 平仓线, 控制权风险 |
| IPO解禁风险监控 | `ipo-lockup-risk-monitor` | 监控限售股解禁时间表、规模 | 解禁, 限售股, 供给冲击 |
| 商誉减值风险监控 | `goodwill-risk-monitor` | 识别高商誉占比、减值风险 | 商誉, 减值, 并购 |
| 股东风险检查 | `shareholder-risk-check` | 分析股东结构、减持计划、一致行动人 | 股东, 减持, 控制权 |
| 融资融券风险监控 | `margin-risk-monitor` | 跟踪两融余额、融资买入占比 | 融资融券, 杠杆, 两融 |
| 涨跌停风险检查器 | `limit-up-limit-down-risk-checker` | 识别连续涨跌停、流动性枯竭风险 | 涨停, 跌停, 流动性 |

### 市场分析类 (Market Analysis)

| Skill Name | 目录 | 描述 | 关键词 |
|-----------|------|------|--------|
| 龙虎榜分析器 | `dragon-tiger-list-analyzer` | 解读龙虎榜数据、游资席位、机构动向 | 龙虎榜, 游资, 席位 |
| 大宗交易监控 | `block-deal-monitor` | 跟踪大宗交易折溢价、买卖方、连续性 | 大宗交易, 折价, 机构接盘 |
| 北向资金流向分析 | `northbound-flow-analyzer` | 分析陆股通/港股通资金流向 | 北向资金, 陆股通, 外资 |
| 资金流监控 | `fund-flow-monitor` | 跟踪主力资金、散户资金流向 | 资金流, 主力, 净流入 |
| 市场宽度监控 | `market-breadth-monitor` | 跟踪涨跌家数、新高新低、市场情绪 | 市场宽度, 涨跌比, 情绪 |
| 板块轮动检测器 | `sector-rotation-detector` | 识别行业/板块轮动信号 | 板块轮动, 行业, 资金切换 |
| 概念板块分析器 | `concept-board-analyzer` | 分析热点概念、题材炒作 | 概念股, 题材, 热点 |
| 行业板块分析器 | `industry-board-analyzer` | 分析行业基本面、估值、景气度 | 行业, 板块, 景气度 |
| 估值区间检测器 | `valuation-regime-detector` | 判断市场/个股估值水平 | 估值, PE, PB, 高估低估 |
| 波动率区间监控 | `volatility-regime-monitor` | 跟踪市场波动率状态 | 波动率, VIX, 风险 |
| 宏观流动性监控 | `macro-liquidity-monitor` | 跟踪货币政策、流动性指标 | 流动性, 货币政策, 利率 |
| 政策敏感度简报 | `policy-sensitivity-brief` | 分析政策对市场/行业的影响 | 政策, 监管, 影响 |
| 因子拥挤度监控 | `factor-crowding-monitor` | 识别因子拥挤、反转风险 | 因子, 拥挤, 反转 |
| 周度市场简报生成器 | `weekly-market-brief-generator` | 自动生成周度市场总结 | 周报, 市场总结, 简报 |
| 市场概览仪表板 | `market-overview-dashboard` | 提供市场全景视图 | 仪表板, 概览, 全景 |

### 投资组合类 (Portfolio Management)

| Skill Name | 目录 | 描述 | 关键词 |
|-----------|------|------|--------|
| 投资组合监控编排器 | `portfolio-monitor-orchestrator` | 编排完整组合监控流程 | 组合监控, 编排, 全流程 |
| 投资组合健康检查 | `portfolio-health-check` | 诊断组合风险、集中度、流动性 | 组合诊断, 健康检查, 风险 |
| 再平衡规划器 | `rebalancing-planner` | 生成再平衡方案、交易清单 | 再平衡, 调仓, 交易计划 |
| 风险调整收益优化器 | `risk-adjusted-return-optimizer` | 优化夏普比率、最大回撤 | 夏普比率, 风险调整, 优化 |
| ETF配置器 | `etf-allocator` | 生成ETF组合配置方案 | ETF, 配置, 资产配置 |
| 适配性报告生成器 | `suitability-report-generator` | 生成投资者适配性报告 | 适配性, 风险承受, 合规 |

### 研究工具类 (Research Tools)

| Skill Name | 目录 | 描述 | 关键词 |
|-----------|------|------|--------|
| 股票研究流程编排器 | `equity-research-orchestrator` | 编排完整个股研究流程 | 个股研究, 编排, 全流程 |
| 财务报表分析器 | `financial-statement-analyzer` | 分析财报质量、盈利能力、现金流 | 财报, 财务分析, 盈利 |
| 同业对比分析器 | `peer-comparison-analyzer` | 横向对比同行业公司 | 同业对比, 横向比较, 行业 |
| 事件研究 | `event-study` | 量化事件对股价的影响 | 事件研究, 超额收益, 事件窗口 |
| 投资备忘录生成器 | `investment-memo-generator` | 生成投资决策备忘录 | 投资备忘录, 决策, 记录 |
| ESG筛选器 | `esg-screener` | 基于ESG标准筛选股票 | ESG, 可持续, 社会责任 |
| 量化因子筛选器 | `quant-factor-screener` | 基于多因子模型筛选股票 | 因子, 量化, 筛选 |
| 低估值股票筛选器 | `undervalued-stock-screener` | 识别低估值投资机会 | 低估值, 价值投资, 筛选 |
| 小盘成长股识别器 | `small-cap-growth-identifier` | 识别小盘成长机会 | 小盘股, 成长股, 机会 |
| 高股息策略 | `high-dividend-strategy` | 筛选高股息率股票 | 股息, 分红, 收益 |
| 科技炒作vs基本面 | `tech-hype-vs-fundamentals` | 区分炒作与真实价值 | 炒作, 基本面, 泡沫 |
| 情绪与现实差距 | `sentiment-reality-gap` | 识别情绪与基本面背离 | 情绪, 背离, 反转 |

### 交易与事件类 (Trading & Events)

| Skill Name | 目录 | 描述 | 关键词 |
|-----------|------|------|--------|
| IPO新股监控 | `ipo-newlist-monitor` | 跟踪新股上市、破发风险 | IPO, 新股, 上市 |
| 公告监控 | `disclosure-notice-monitor` | 监控重要公告、信息披露 | 公告, 披露, 信息 |
| 股东结构监控 | `shareholder-structure-monitor` | 跟踪股东变化、持股集中度 | 股东结构, 持股, 集中度 |
| 股份回购监控 | `share-repurchase-monitor` | 跟踪回购计划、执行进度 | 回购, 注销, 股本 |
| 分红与公司行动跟踪 | `dividend-corporate-action-tracker` | 跟踪分红、送转、配股等 | 分红, 送转, 除权 |
| 内幕交易分析器 | `insider-trading-analyzer` | 分析高管、大股东交易行为 | 内幕交易, 高管, 增减持 |
| 事件驱动检测器 | `event-driven-detector` | 识别事件驱动投资机会 | 事件驱动, 并购, 重组 |
| 涨停板池分析器 | `limit-up-pool-analyzer` | 分析涨停板、打板机会 | 涨停板, 打板, 短线 |
| 可转债扫描器 | `convertible-bond-scanner` | 筛选可转债投资机会 | 可转债, 转债, 套利 |

### 特色分析类 (Specialized Analysis)

| Skill Name | 目录 | 描述 | 关键词 |
|-----------|------|------|--------|
| AB-AH溢价监控 | `ab-ah-premium-monitor` | 跟踪A股H股溢价率 | AH溢价, 港股, 套利 |
| 北交所精选层分析 | `bse-selection-analyzer` | 分析北交所精选层股票 | 北交所, 精选层, 新三板 |
| 沪深港通持仓监控 | `hsgt-holdings-monitor` | 跟踪外资持仓变化 | 沪深港通, 外资持仓, 北向 |
| 热度排行情绪监控 | `hot-rank-sentiment-monitor` | 跟踪股票热度、舆情 | 热度, 舆情, 情绪 |
| 流动性冲击估算器 | `liquidity-impact-estimator` | 估算大额交易的市场冲击 | 流动性, 冲击成本, 滑点 |
| 盘中微观结构分析 | `intraday-microstructure-analyzer` | 分析盘中订单流、微观结构 | 微观结构, 订单流, 高频 |
| 产业链映射器 | `industry-chain-mapper` | 绘制产业链上下游关系 | 产业链, 上下游, 关联 |

### 数据工具类 (Data Toolkits)

| Skill Name | 目录 | 描述 | 关键词 |
|-----------|------|------|--------|
| 中国金融数据工具包 | `findata-toolkit-cn` | 提供A股数据获取脚本和工具 | 数据工具, akshare, 数据获取 |

---

## 香港市场 Skills (HK-market)

### HK-风险监控类 (Risk Monitoring)

| Skill Name | 目录 | 描述 | 关键词 |
|-----------|------|------|--------|
| 港股集中度风险监控 | `hk-concentration-risk` | 监控投资组合集中度风险、行业集中度、个股集中度 | 集中度, 风险管理, 分散化 |
| 港股汇率风险监控 | `hk-currency-risk` | 监控港币汇率波动、汇率风险敞口、对冲策略 | 汇率, 外汇, 对冲, 港币 |
| 港股流动性风险监控 | `hk-liquidity-risk` | 监控市场流动性状况、个股流动性风险、市场深度 | 流动性, 市场深度, 交易风险 |

### HK-市场分析类 (Market Analysis)

| Skill Name | 目录 | 描述 | 关键词 |
|-----------|------|------|--------|
| 港股市场概览 | `hk-market-overview` | 提供港股市场整体表现、主要指数、板块轮动、市场情绪 | 市场概览, 恒生指数, 港股 |
| 港股市场广度监控 | `hk-market-breadth` | 监控市场广度指标、上涨下跌家数、新高新低比率 | 市场广度, 涨跌比, 趋势强度 |
| 港股板块轮动检测 | `hk-sector-rotation` | 监控各板块资金流向、相对强度、轮动信号 | 板块轮动, 行业配置, 资金流向 |
| 港股估值分析 | `hk-valuation-analyzer` | 提供市场整体估值、行业估值对比、个股估值分析 | 估值, PE, PB, 相对估值 |
| 港股南向资金流向 | `hk-southbound-flow` | 分析内地投资者通过港股通的资金流向、持仓变化 | 南向资金, 港股通, 内地资金 |
| 港股外资流向 | `hk-foreign-flow` | 分析外资通过港股通、QFII、直接投资的资金动向 | 外资, 国际资金, QFII |
| 港股ETF资金流向 | `hk-etf-flow` | 分析港股ETF资金流向、持仓变化、溢价折价 | ETF, 资金流向, 溢价折价 |

### HK-研究工具类 (Research Tools)

| Skill Name | 目录 | 描述 | 关键词 |
|-----------|------|------|--------|
| 港股财务报表分析 | `hk-financial-statement` | 提供财务报表分析、财务比率计算、财务健康度评估 | 财报, 财务分析, 基本面 |
| 港股股息跟踪 | `hk-dividend-tracker` | 监控股息政策、分红历史、股息收益率 | 股息, 分红, 收益率 |

### HK-数据工具类 (Data Toolkits)

| Skill Name | 目录 | 描述 | 关键词 |
|-----------|------|------|--------|
| 港股金融数据工具包 | `findata-toolkit-hk` | 提供港股实时行情、财务数据、南向资金、汇率数据获取脚本 | 数据工具, 港股数据, 数据获取 |

---

## 美国市场 Skills (US-market)

### US-风险监控类 (Risk Monitoring)

| Skill Name | 目录 | 描述 | 关键词 |
|-----------|------|------|--------|
| 信用利差监控 | `credit-spread-monitor` | 跟踪信用利差、违约风险 | credit spread, default risk, bond |

### US-市场分析类 (Market Analysis)

| Skill Name | 目录 | 描述 | 关键词 |
|-----------|------|------|--------|
| 市场宽度监控 | `market-breadth-monitor` | 跟踪涨跌家数、新高新低 | market breadth, advance-decline, sentiment |
| 板块轮动检测器 | `sector-rotation-detector` | 识别行业轮动信号 | sector rotation, industry, capital flow |
| 估值区间检测器 | `valuation-regime-detector` | 判断市场估值水平 | valuation, PE, PB, overvalued |
| 波动率区间监控 | `volatility-regime-monitor` | 跟踪VIX、波动率状态 | volatility, VIX, risk |
| 宏观流动性监控 | `macro-liquidity-monitor` | 跟踪美联储政策、流动性 | liquidity, Fed, monetary policy |
| 政策敏感度简报 | `policy-sensitivity-brief` | 分析政策对市场影响 | policy, regulation, impact |
| 因子拥挤度监控 | `factor-crowding-monitor` | 识别因子拥挤风险 | factor, crowding, reversal |
| 周度市场简报生成器 | `weekly-market-brief-generator` | 自动生成周度市场总结 | weekly brief, market summary |
| 收益率曲线区间检测器 | `yield-curve-regime-detector` | 分析收益率曲线形态 | yield curve, inversion, recession |

### US-投资组合类 (Portfolio Management)

| Skill Name | 目录 | 描述 | 关键词 |
|-----------|------|------|--------|
| 投资组合监控编排器 | `portfolio-monitor-orchestrator` | 编排完整组合监控流程 | portfolio monitoring, orchestrator |
| 投资组合健康检查 | `portfolio-health-check` | 诊断组合风险、集中度 | portfolio health, risk, concentration |
| 再平衡规划器 | `rebalancing-planner` | 生成再平衡方案 | rebalancing, trading plan |
| 风险调整收益优化器 | `risk-adjusted-return-optimizer` | 优化夏普比率 | Sharpe ratio, risk-adjusted, optimization |
| ETF配置器 | `etf-allocator` | 生成ETF组合配置 | ETF, allocation, asset allocation |
| 适配性报告生成器 | `suitability-report-generator` | 生成投资者适配性报告 | suitability, risk tolerance, compliance |
| 税务感知再平衡规划器 | `tax-aware-rebalancing-planner` | 考虑税务的再平衡方案 | tax-loss harvesting, capital gains, tax |

### US-研究工具类 (Research Tools)

| Skill Name | 目录 | 描述 | 关键词 |
|-----------|------|------|--------|
| 股票研究流程编排器 | `equity-research-orchestrator` | 编排完整个股研究流程 | equity research, orchestrator |
| 财务报表分析器 | `financial-statement-analyzer` | 分析财报质量、盈利能力 | financial statement, earnings, cash flow |
| 同业对比分析器 | `peer-comparison-analyzer` | 横向对比同行业公司 | peer comparison, industry, benchmarking |
| 事件研究 | `event-study` | 量化事件对股价影响 | event study, abnormal return, event window |
| 投资备忘录生成器 | `investment-memo-generator` | 生成投资决策备忘录 | investment memo, decision, documentation |
| ESG筛选器 | `esg-screener` | 基于ESG标准筛选 | ESG, sustainability, social responsibility |
| 量化因子筛选器 | `quant-factor-screener` | 基于多因子模型筛选 | factor, quant, screening |
| 低估值股票筛选器 | `undervalued-stock-screener` | 识别低估值机会 | undervalued, value investing, screening |
| 小盘成长股识别器 | `small-cap-growth-identifier` | 识别小盘成长机会 | small cap, growth, opportunity |
| 科技炒作vs基本面 | `tech-hype-vs-fundamentals` | 区分炒作与真实价值 | hype, fundamentals, bubble |
| 情绪与现实差距 | `sentiment-reality-gap` | 识别情绪与基本面背离 | sentiment, divergence, reversal |

### US-交易与事件类 (Trading & Events)

| Skill Name | 目录 | 描述 | 关键词 |
|-----------|------|------|--------|
| 内幕交易分析器 | `insider-trading-analyzer` | 分析内部人交易行为 | insider trading, executives, buying/selling |
| 内幕情绪聚合器 | `insider-sentiment-aggregator` | 聚合内部人交易情绪 | insider sentiment, aggregation, signal |
| 事件驱动检测器 | `event-driven-detector` | 识别事件驱动机会 | event-driven, M&A, restructuring |
| 股份回购监控 | `buyback-monitor` | 跟踪回购计划执行 | buyback, repurchase, share count |
| 股息贵族计算器 | `dividend-aristocrat-calculator` | 识别股息贵族股票 | dividend aristocrat, dividend growth, yield |
| 财报反应分析器 | `earnings-reaction-analyzer` | 分析财报发布后的市场反应 | earnings reaction, surprise, post-earnings drift |
| 期权策略分析器 | `options-strategy-analyzer` | 分析期权策略、隐含波动率 | options, implied volatility, strategy |

### US-特色分析类 (Specialized Analysis)

| Skill Name | 目录 | 描述 | 关键词 |
|-----------|------|------|--------|
| 流动性冲击估算器 | `liquidity-impact-estimator` | 估算大额交易市场冲击 | liquidity, market impact, slippage |

### US-数据工具类 (Data Toolkits)

| Skill Name | 目录 | 描述 | 关键词 |
|-----------|------|------|--------|
| 美国金融数据工具包 | `findata-toolkit` | 提供美股数据获取工具 | data toolkit, yfinance, data fetching |

---

## 使用指南

### 对于大模型

1. **查找 Skill**：根据用户需求关键词，在上表中搜索匹配的 skill
2. **读取文档**：定位到具体目录后，读取 `SKILL.md` 了解工作流程
3. **获取数据**：查看 `references/data-queries.md` 了解数据获取方式
4. **应用方法**：参考 `references/methodology.md` 了解指标定义和阈值
5. **格式化输出**：按照 `references/output-template.md` 生成结构化结果

### 对于用户

1. **浏览分类**：根据需求类型（风险监控、市场分析等）快速定位
2. **查看描述**：通过描述和关键词判断是否符合需求
3. **添加新 Skill**：
   - 在对应市场目录下创建新文件夹（使用 kebab-case 命名）
   - 复制现有 skill 的文件结构
   - 更新本文档的对应分类表格
4. **维护索引**：添加或修改 skill 后，及时更新本文档

### Skill 命名规范

- 使用 kebab-case（小写字母，单词间用连字符）
- 名称应清晰描述功能
- 避免过长的名称（建议 2-4 个单词）

### 文件结构规范

```
{market-name}/{skill-name}/
├── SKILL.md              # 必需：技能说明和工作流程
├── LICENSE.txt           # 必需：许可证
└── references/           # 必需：参考文档目录
    ├── methodology.md    # 必需：方法论和指标定义
    ├── data-queries.md   # 必需：数据获取说明
    └── output-template.md # 必需：输出格式模板
```

---

## 统计信息

- **中国市场 Skills 总数**：57
- **香港市场 Skills 总数**：13
- **美国市场 Skills 总数**：37
- **总计**：107

最后更新：2026-02-21
