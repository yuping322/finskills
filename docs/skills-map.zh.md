# FinSkills 技能地图（按场景快速选用）

这份地图用于快速回答“我该触发哪个技能？”——按**问题场景**把现有技能分组，并标出适用市场（A股/美股）。

> 触发方式：在提问中直接写 `$<skill-name>`（推荐），或用自然语言描述任务让系统自动匹配。

相关参考：
- A股技能触发问句示例：`/Users/fengzhi/Downloads/git/finskills/docs/skills-trigger-questions.zh.md`
- 常用“页面信号”方法论（数据源无关）：`/Users/fengzhi/Downloads/git/finskills/docs/analysis-methods.zh.md`

---

## 1) 市场总览 / 状态机 / 周报面板

- 市场总貌/交易所统计（A股）：`$market-overview-dashboard`
- 市场宽度/风险偏好（A股/美股）：`$market-breadth-monitor`
- 宏观流动性与流动性拐点（A股/美股）：`$macro-liquidity-monitor`
- 估值所处“分位/中枢/风格切换”（A股/美股）：`$valuation-regime-detector`
- 波动率状态与风险开关（A股/美股）：`$volatility-regime-monitor`
- 行业轮动信号（A股/美股）：`$sector-rotation-detector`
- 政策/宏观发布敏感行业与监控清单（A股/美股）：`$policy-sensitivity-brief`
- 每周市场简报生成器（A股/美股）：`$weekly-market-brief-generator`
- 收益率曲线状态（美股）：`$yield-curve-regime-detector`
- 信用利差/信用风险温度（美股）：`$credit-spread-monitor`

---

## 2) 板块 / 主题 / 产业链

- 概念板块分析与轮动（A股）：`$concept-board-analyzer`
- 行业板块分析与轮动（A股）：`$industry-board-analyzer`
- 产业链上下游映射与景气跟踪（A股）：`$industry-chain-mapper`

---

## 3) 资金 / 持仓 / 情绪 / 拥挤度

- 资金流监控（个股/行业/概念/大盘）（A股）：`$fund-flow-monitor`
- 北向资金：流入、偏好、背离（A股）：`$northbound-flow-analyzer`
- 沪深港通持股变化与集中度（A股）：`$hsgt-holdings-monitor`
- 两融/杠杆拥挤与踩踏风险（A股）：`$margin-risk-monitor`
- 人气榜/热度趋势与情绪背离（A股）：`$hot-rank-sentiment-monitor`
- 因子拥挤与风格挤压风险（A股/美股）：`$factor-crowding-monitor`
- “情绪叙事 vs 基本面”错配机会（A股/美股）：`$sentiment-reality-gap`

---

## 4) 事件 / 公告 / IPO / 内部人 / 事件研究

- 公告与披露监控、事件清单与影响评估（A股）：`$disclosure-notice-monitor`
- 事件驱动机会扫描（A股/美股）：`$event-driven-detector`
- 事件窗研究（A股/美股）：`$event-study`
- 业绩公告后市场反应（美股）：`$earnings-reaction-analyzer`
- 回购事件监控（美股）：`$buyback-monitor`
- 股份回购监控（A股）：`$share-repurchase-monitor`
- 新股/次新与发行节奏（A股）：`$ipo-newlist-monitor`
- 解禁/锁定期与供给冲击风险（A股）：`$ipo-lockup-risk-monitor`
- 内部人交易（董监高/重要股东）信号（A股/美股）：`$insider-trading-analyzer`
- 内部人情绪聚合（美股）：`$insider-sentiment-aggregator`

---

## 5) 基本面 / 财务 / 估值 / 可比 / 选股

- 单公司财务报表深度体检（A股/美股）：`$financial-statement-analyzer`
- 同业可比与相对估值差异（A股/美股）：`$peer-comparison-analyzer`
- 多因子量化筛选（A股/美股）：`$quant-factor-screener`
- 价值筛选（低估、稳健等）（A股/美股）：`$undervalued-stock-screener`
- 小盘高成长机会（A股/美股）：`$small-cap-growth-identifier`
- 科技股：泡沫叙事 vs 基本面（A股/美股）：`$tech-hype-vs-fundamentals`
- ESG 筛选与争议风险（A股/美股）：`$esg-screener`
- 高股息策略与可持续性（A股）：`$high-dividend-strategy`
- 分红/配股/除权除息与提醒（A股）：`$dividend-corporate-action-tracker`
- 股息贵族/分红稳定性（美股）：`$dividend-aristocrat-calculator`

---

## 6) 交易制度 / 可交易性 / 风险红旗

- 冲击成本/流动性约束与可交易性评分（A股/美股）：`$liquidity-impact-estimator`
- 日内微观结构/盘口与异常行为识别（A股）：`$intraday-microstructure-analyzer`
- 大宗交易（折溢价/抛压/承接）监控（A股）：`$block-deal-monitor`
- 涨跌停/制度性不可交易风险检查（A股）：`$limit-up-limit-down-risk-checker`
- 涨停池强势结构与复盘（A股）：`$limit-up-pool-analyzer`
- 龙虎榜/席位资金与异常成交（A股）：`$dragon-tiger-list-analyzer`
- 质押风险（A股）：`$equity-pledge-risk-monitor`
- 商誉减值风险（A股）：`$goodwill-risk-monitor`
- 股东结构/筹码与变化（A股）：`$shareholder-structure-monitor`
- 股东层面的治理/质押/解禁等风险检查（A股）：`$shareholder-risk-check`
- ST/退市风险扫描（A股）：`$st-delist-risk-scanner`

---

## 7) 跨市场 / 特定品类（ETF、转债、期权…）

- AB 股比价与 A+H 溢价监控（A股/港股）：`$ab-ah-premium-monitor`
- ETF 配置：暴露、约束与组合方案（A股/美股）：`$etf-allocator`
- 可转债筛选：溢价、条款与正股联动（A股）：`$convertible-bond-scanner`
- 期权策略分析（美股）：`$options-strategy-analyzer`

---

## 7.1) 北交所（BSE）

- 北交所精选分析（流动性/成长/风险）（A股）：`$bse-selection-analyzer`

---

## 8) 组合构建 / 再平衡 / 监控编排

- 风险调整后收益最优化建仓（A股/美股）：`$risk-adjusted-return-optimizer`
- 再平衡规则与执行清单（A股/美股）：`$rebalancing-planner`
- 税务约束下再平衡（美股）：`$tax-aware-rebalancing-planner`
- 组合健康检查（集中度/相关性/暴露/风控）（A股/美股）：`$portfolio-health-check`
- 组合监控编排（把多项检查整合成一份报告）（A股/美股）：`$portfolio-monitor-orchestrator`

---

## 9) 文档交付 / 合规

- 投资备忘录/研究简报生成（A股/美股）：`$investment-memo-generator`
- 适当性/合规说明报告（A股/美股）：`$suitability-report-generator`
- 深度研究“一键编排”（A股/美股）：`$equity-research-orchestrator`

---

## 10) 数据工具包（用于提供可执行的数据抓取与计算）

- A股数据工具包（AKShare）：`$findata-toolkit-cn`
- 美股数据工具包（yfinance/EDGAR/FRED 等）：`$findata-toolkit`

---

## 11) 还想“覆盖所有情况”？推荐的扩展方向（Backlog）

下面这些属于常见高频、且目前覆盖不够完整/可继续加深的“技能簇”（按优先级建议从上到下）：

1. **指数/基金更深**：基金持仓穿透、风格漂移、折溢价/跟踪误差、ETF 申赎与资金、指数成分/权重变动监控。
2. **固收与利率（CN）**：国债/国开/同业存单收益率曲线、期限利差、信用利差、资金面（DR007 等）与政策传导。
3. **衍生品（CN）**：期货基差/期限结构、期权隐波曲面、IV/RV、波动率风险溢价与情景压力测试。
4. **商品/外汇/全球宏观联动**：大宗/美元/利率对行业与风格的敏感度映射，宏观情景组合影响。
5. **财务舞弊与治理红旗（更系统）**：收入确认、应收/存货、关联交易、审计意见、现金流质量等多维异常检测。
6. **策略回测与复盘模板化**：把常用筛选/信号变成可重复的“回测—归因—风控”工作流（不做自动下单）。

如果你愿意，我可以按你的常用问题（例如：你最常问的 10 类问题）把这些扩展方向拆成一批具体技能目录名 + 每个 skill 的 `SKILL.md` 骨架 + 对应 `findata-toolkit-*` 脚本接口需求清单。
