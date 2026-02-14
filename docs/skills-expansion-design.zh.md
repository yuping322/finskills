# FinSkills 扩展设计（Draft）

目标：在保持“技能即工作流 + 数据工具包即可执行脚本”的架构下，系统性扩展 FinSkills 的技能覆盖面，尤其是围绕 AKShare 的大量数据接口组合出可复用的数据视图与分析原语，从而支持更全面的 A 股研究、交易约束评估、组合监控与合规文档产出。

本文是一个可以不断迭代的“总设计”。它优先回答：

- 需要覆盖哪些分析场景（问题空间）
- 新技能应该如何组织、命名、触发与输出
- `findata-toolkit-cn`（AKShare）应如何扩展为“数据层 + 分析原语层”
- 分阶段落地的优先级与验收标准

---

## 1. 背景与现状

### 1.1 现状（仓库级）

- 已有技能：US-market 15 个、China-market 15 个（筛选 → 深度分析 → 组合与文档）+ 2 个数据工具包。
- US 数据工具包：脚本覆盖更广（财务计算、组合分析、因子筛选、EDGAR、宏观）。
- CN 数据工具包：目前集中在股票与宏观（`stock_data.py`、`macro_data.py`），接口覆盖仍有较大扩展空间（AKShare 支持基金/债券/衍生品/指数/市场宽度/资金流/事件等）。

### 1.2 扩展动机

- A 股研究往往“数据维度多、联动强”：同一分析结论需要拼接行情、财务、行业、资金、事件与制度约束（T+1/涨跌停/流动性）。
- AKShare 的“接口多”是一把双刃剑：能力强，但需要抽象出稳定的组合方式、统一输出与缓存/限速，否则分析技能会变得脆弱且难维护。

---

## 2. 设计目标与非目标

### 2.1 设计目标

1. **覆盖更全的分析场景**：从“选股/选基”扩展到“指数/ETF/可转债/期货期权/资金流/市场宽度/事件研究/风格与估值中枢/政策敏感度”。
2. **数据与分析解耦**：分析技能只描述工作流与判断框架；确定性的数据抓取与计算尽量落在工具包脚本中（可重复、可测试、可缓存）。
3. **标准化输出**：工具包脚本输出统一的 JSON Envelope，便于下游技能组合使用与调试。
4. **渐进式加载**：技能正文只放必要的“流程与决策点”；方法论与模板放 `references/`；可执行逻辑放脚本。
5. **易扩展、可维护**：新增一个 AKShare 接口，不需要改动多个技能；新增一个技能，只需组合已有数据视图与原语。

### 2.2 非目标（本轮不做/可后续）

- 依赖收费数据源或必须 API Key 的数据（如后续可做“可选增强”）。
- 高度主观的“新闻解读/情绪叙事”型技能（除非数据源明确且可复现）。
- 复杂的交易系统（下单、回测引擎、实时风控）——可以提供分析与建议，但不做自动化交易执行。

---

## 3. 总体架构：Skill → Toolkit → Data Views → Analysis Primitives

### 3.1 分层

1. **Skill（工作流层）**
   - 面向用户问题：筛选、诊断、归因、报告。
   - 产出结构化内容：候选列表、风险清单、观点框架、可交付文档模板。
   - 只在必要时调用工具包获取数据或计算。

2. **Toolkit（数据与计算层）**
   - `findata-toolkit-cn`（AKShare）与 `findata-toolkit-us`（yfinance/EDGAR/FRED）。
   - 提供“数据视图（views）”与“分析原语（primitives）”。

3. **Data Views（可复用数据视图）**
   - 例：`company_snapshot` = 行情 + 估值 + 财务摘要 + 分红 + 资金流 + 事件风险。
   - 例：`industry_panel` = 申万行业成分 + 行业指数表现 + 估值分位 + 资金流。

4. **Analysis Primitives（可复用分析原语）**
   - 例：回撤/波动/相关性、事件窗收益、风格暴露、分位数/排名、阈值报警、周期/流动性判断等。

### 3.2 统一 JSON Envelope（建议）

所有工具包脚本统一输出结构（示例）：

```json
{
  "meta": {
    "tool": "findata-toolkit-cn",
    "script": "equity_data",
    "as_of": "2026-02-11T12:34:56",
    "source": ["akshare"],
    "params": {"symbol": "600519", "window": "1y"}
  },
  "data": { "...": "..." },
  "warnings": ["..."],
  "errors": []
}
```

说明：
- `errors` 为空时代表成功；失败时脚本仍尽量输出 envelope（便于上游处理）。
- `meta.params` 记录关键参数，利于复现与缓存。

### 3.3 缓存与限速（建议）

在 `scripts/common/` 增加可选的轻量缓存与限速策略（仅建议，实施可分阶段）：

- 缓存目录：工具包根目录下 `.cache/`（按 `script + params` 哈希存 JSON）
- TTL：按数据类型配置（行情分钟级、财务日级/季度级、宏观月级）
- 限速：沿用 `rate_limit()`，并在高频接口（行情全市场）做批量拉取与本地复用

---

## 4. `findata-toolkit-cn` 扩展蓝图（AKShare）

### 4.1 模块拆分（建议脚本集合）

以“领域脚本 + 共享原语”的方式拆分，避免 `stock_data.py` 继续膨胀。

建议新增（候选）脚本：

- `scripts/universe.py`：股票/指数/基金/可转债“全量列表与基础过滤”（ST、上市时长、板块等）
- `scripts/equity_snapshot.py`：公司快照视图（行情/估值/财务摘要/分红/事件红旗）
- `scripts/industry_data.py`：申万行业映射、行业面板与轮动信号输入数据
- `scripts/flow_data.py`：北向、ETF 资金、行业资金、两融等资金维度
- `scripts/market_breadth.py`：市场宽度与微观结构（涨跌家数、涨停/跌停、成交集中度、换手/量价结构）
- `scripts/cb_data.py`：可转债列表、溢价、转股价值、赎回/回售条款与风险标签
- `scripts/fund_etf_data.py`：ETF/基金（规模、持仓、跟踪误差/折溢价等可得数据）
- `scripts/index_data.py`：指数与成分（用于行业/风格与基准对比）
- `scripts/derivatives_data.py`：期货/期权（如可得）与对冲工具输入
- `scripts/calendar_events.py`：宏观/政策/财报窗口日历（如可得）+ 事件敏感度模板输入

共享层（`scripts/common/`）建议补齐：

- `cache.py`：TTL 缓存（可选开关）
- `schema.py`：字段规范（symbol、date、return、amount 等）
- `normalize.py`：统一标的编码与交易所（A 股/指数/基金/可转债）
- `analytics.py`：通用原语（收益率、波动、回撤、分位数、事件窗收益、相关矩阵等）

> 注：以上脚本名称与 AKShare 具体接口需要在落地阶段逐个确认可用性与稳定性；设计先给出“能力模块边界”。

### 4.2 “组合视图”优先于“接口直出”

不建议让每个技能直接面向 AKShare 的“细碎接口”。建议先沉淀少量稳定的视图：

- `company_snapshot(symbol)`：单标的研究入口（80% 的深度分析技能都需要）
- `peer_comps(symbol, universe=industry)`：同业对比（估值、盈利质量、成长、杠杆）
- `industry_panel(level=sw1, window=1y)`：行业轮动/景气输入
- `liquidity_risk_panel(universe)`：涨跌停、成交、换手、冲击成本的风险代理
- `flow_panel(window)`：北向/两融/ETF 资金等
- `macro_dashboard()`：宏观与流动性仪表盘（已有，进一步标准化输出）

把这些视图作为“稳定 API”，新增技能只需要组合视图与原语。

### 4.3 AKShare MCP 接口对齐（可选数据层）

你提供的 `litellm_tools.json` 工具集包含 356 个 AKShare 相关接口（以 `stock_*` 为主），并配套了缓存与智能 TTL。它非常适合作为 `findata-toolkit-cn` 的“可选数据层”，让分析技能能稳定地拿到更丰富的数据面（尤其是板块/资金/龙虎榜/解禁/质押/商誉/披露等）。

接口按文档分类可归为 9 大类：

- 个股信息、其他、历史数据、基金数据、实时行情
- 市场总貌、成交数据、指数数据、行业数据

基于这些接口簇，已先行把对应的 China-market 技能目录骨架搭好（先占位，后续逐个填充方法论与输出模板，并在工具包脚本里实现稳定的数据视图）。

China-market（已新增目录）→ MCP 接口簇映射建议：

| skill 目录 | 覆盖主题 | 主要接口簇（按前缀/模式） |
|---|---|---|
| `concept-board-analyzer` | 概念板块 | `stock_board_concept_*`, `stock_fund_flow_concept`, `stock_concept_fund_flow_hist` |
| `industry-board-analyzer` | 行业板块 | `stock_board_industry_*`, `stock_fund_flow_industry`, `stock_sector_fund_flow_*` |
| `limit-up-pool-analyzer` | 涨停池/强势结构 | `stock_zt_pool_*` |
| `dragon-tiger-list-analyzer` | 龙虎榜/席位资金 | `stock_lhb_*` |
| `fund-flow-monitor` | 资金流向 | `*fund_flow*`, `stock_fund_flow_big_deal`, `stock_main_fund_flow`, `stock_market_fund_flow` |
| `hsgt-holdings-monitor` | 沪深港通持股 | `stock_hsgt_*`, `stock_sgt_*` |
| `equity-pledge-risk-monitor` | 股权质押 | `stock_gpzy_*` |
| `goodwill-risk-monitor` | 商誉/减值 | `stock_sy_*` |
| `disclosure-notice-monitor` | 公告/披露 | `*disclosure*`, `stock_notice_report`, `stock_report_disclosure`, `news_report_time_baidu` |
| `dividend-corporate-action-tracker` | 分红/配股 | `*dividend*`, `stock_fhps_*`, `news_trade_notify_dividend_baidu`, `stock_allotment_cninfo` |
| `ipo-newlist-monitor` | IPO/新股/次新 | `stock_ipo_*`, `stock_new_ipo_cninfo`, `stock_zh_a_new*`, `stock_xgsr_ths`, `stock_ipo_benefit_ths` |
| `st-delist-risk-scanner` | ST/退市 | `stock_zh_a_st_em`, `stock_zh_a_stop_em`, `stock_staq_net_stop` |
| `hot-rank-sentiment-monitor` | 人气/热度代理 | `stock_hot_rank_*`, `stock_comment_detail_*`, `stock_zh_vote_baidu` |
| `intraday-microstructure-analyzer` | 日内/盘口/逐笔 | `stock_bid_ask_em`, `stock_intraday_*`, `stock_zh_a_tick_tx`, `stock_zh_a_hist_min_em`, `stock_zh_a_minute`, `stock_zh_a_hist_pre_min_em` |
| `shareholder-structure-monitor` | 股东结构/筹码 | `*holder*`, `*hold*`, `stock_zh_a_gdhs*`, `stock_gdfx_*`, `stock_hold_*` |
| `market-overview-dashboard` | 交易所统计/总貌 | `stock_sse_*`, `stock_szse_*`, `stock_sse_deal_daily` |
| `ab-ah-premium-monitor` | AB/AH 比价 | `stock_zh_ab_comparison_em`, `stock_zh_ah_*` |

覆盖说明（避免误判）：

- 该 MCP 工具集当前覆盖重点是“股票与板块相关数据”。ETF/可转债/期货期权等若不在该工具集中，需要扩展 MCP server 暴露对应 AKShare 模块，或在 `findata-toolkit-cn` 里直接实现。
- 目录骨架先行的目的：先把“问题空间”占位，后续按复用度从工具包视图（views）开始补齐，最后补方法论与输出模板细节。

---

## 5. 技能体系扩展：覆盖“更全的分析情况”

### 5.1 问题空间分解（建议维度）

用一个“问题空间”帮助确保覆盖面完整：

- 分析阶段：发现/筛选 → 解释/归因 → 定价/估值 → 风险/约束 → 组合/监控 → 文档/合规
- 标的类型：个股、行业、指数、ETF/基金、可转债、利率/信用、期货期权、宏观
- 驱动类型：基本面、量价/技术、资金、事件、政策/周期、风格/因子
- 决策约束：流动性、交易制度（T+1/涨跌停）、集中度/相关性、适当性/合规

### 5.2 新技能候选清单（China-market 优先）

以下为“可落地、可复用、与 AKShare 高相关”的技能候选（命名为目录建议名）：

| 技能目录名（建议） | 核心用途 | 主要依赖（建议 toolkit 视图/脚本） |
|---|---|---|
| `market-breadth-monitor` | 市场宽度与微观结构监控（风险偏好/拐点） | `market_breadth.py` |
| `northbound-flow-analyzer` | 北向资金：行业/个股偏好、背离与风险提示 | `flow_data.py` |
| `margin-risk-monitor` | 融资融券与杠杆风险（拥挤/踩踏） | `flow_data.py` |
| `industry-chain-mapper` | 产业链映射与景气跟踪（上中下游联动） | `industry_data.py` + `index_data.py` |
| `peer-comparison-analyzer` | 同业可比公司对比：估值/盈利质量/成长/杠杆 | `peer_comps` 视图 |
| `valuation-regime-detector` | 估值中枢/风格切换：分位数与回归到均值框架 | `industry_panel` + `analytics.py` |
| `earnings-warning-detector-cn` | 业绩预告/预警扫描（若数据可得） | `calendar_events.py` + `equity_snapshot.py` |
| `shareholder-risk-check` | 股东结构、质押、解禁与治理风险标签（若数据可得） | `equity_snapshot.py` |
| `convertible-bond-scanner` | 可转债筛选：溢价、流动性、条款风险、正股质量 | `cb_data.py` + `company_snapshot` |
| `etf-allocator-cn` | ETF 资产配置：风格/行业暴露、跟踪误差与流动性代理 | `fund_etf_data.py` + `index_data.py` |
| `event-study-cn` | A股事件研究：公告/回购/解禁等事件窗收益与归因 | `calendar_events.py` + `analytics.py` |
| `liquidity-impact-estimator` | 冲击成本代理：成交/换手/涨跌停与可交易性评分 | `liquidity_risk_panel` |
| `policy-sensitivity-brief` | 政策/宏观数据发布敏感度：行业与风格清单化输出 | `macro_data.py` + `industry_panel` |

说明：
- “若数据可得”的技能，落地时优先选择 AKShare 覆盖稳定的接口；若接口不稳定，降级为“框架型技能 + 手动输入数据”。
- 候选清单不追求一次性全做，重点是先补齐可复用的 toolkit 视图与原语。

### 5.3 Orchestrator（编排型）技能（建议）

随着技能数增长，用户会希望“一句话跑全流程”。建议新增少量编排技能：

- `china-equity-research-orchestrator`：输入标的/行业 → 自动串联：快照 → 同业 → 风险 → 估值区间 → 结论摘要
- `china-portfolio-monitor-orchestrator`：输入持仓 → 风险诊断 → 资金/风格暴露 → 压力情景 → 监控要点

编排技能不做新逻辑，主要负责“选择调用哪些技能/视图、如何组织输出”。

---

## 6. 技能模板与一致性规范（建议）

### 6.1 每个分析技能的最小骨架

- `SKILL.md`
  - 角色：研究分析师/基金经理/风控/合规
  - 工作流：参数确认 → 数据获取 → 分析 → 风险 → 输出模板
  - “数据增强”段落：引用 `findata-toolkit-cn`
- `references/methodology.md`
  - 指标口径、阈值建议、A 股特有注意点（扣非、政府补助、涨跌停、T+1）
- `references/output-template.md`
  - 固定结构（表格字段、结论要点、免责声明）

### 6.2 输出规范（建议）

分析技能输出建议包含：

- `结论摘要（3-5 条）`
- `关键证据（数据点 + 口径）`
- `风险清单（触发条件 + 监控指标）`
- `下一步（需要补充的数据/核验点）`

---

## 7. 交付节奏：分阶段落地（建议）

### Phase 0：AKShare 能力盘点与字段规范

- 产出：工具包“数据视图与字段规范”文档 + 端点可用性清单（可脚本化生成）
- 验收：最少 5 个稳定 views（`company_snapshot` 等）可在不同标的复用

### Phase 1：补齐高复用数据脚本 + 10 个高价值技能

- 工具包：`universe / industry / flow / market_breadth / cb` 先落地（优先级可调整）
- 技能：从 5.2 表中选 10 个，覆盖“资金 + 宽度 + 可转债 + 行业 + 流动性风险”

### Phase 2：编排型技能 + 组合监控增强

- 增加 orchestrator；把“分析技能输出”拼装成可交付的研究简报/监控周报模板

---

## 8. 待你确认的 3 个关键决策（下一步）

1. **优先市场**：先只扩 A 股（AKShare）还是同时扩 US（yfinance/EDGAR）？
2. **优先人群/场景**：偏“长期基本面研究”还是偏“交易/择时/风险监控”（会影响 toolkit 先做哪类视图）？
3. **输出形态**：你更希望新增技能输出“候选列表 + 打分”，还是“研究报告/投资备忘录”，或两者都要？
