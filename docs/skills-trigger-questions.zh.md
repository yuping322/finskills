# China-market Skills 触发问题示例（每个 skill 5 个）

适用范围：`/China-market/*/SKILL.md`（共 57 个技能）。

使用方式：
- 直接在提问里包含技能名（推荐形态：`$<skill-name>`），即可明确触发对应 skill。
- 把示例里的占位符替换成你的真实输入（如股票代码、时间窗口、股票池、资金规模等）。

## ab-ah-premium-monitor

1. 请用 `$ab-ah-premium-monitor` 监控 A+H 溢价/折价：给出当前分位数、近 1 年区间和极值回看。
2. 用 `$ab-ah-premium-monitor` 帮我分析 `<A股代码>/<H股代码>` 的跨市场定价差，解释可能原因（流动性/事件/情绪）并给风险提示。
3. 请用 `$ab-ah-premium-monitor` 扫描 A+H 股票，列出溢价最高/最低 Top 10，并标注波动与流动性风险。
4. 我想做 A/H 配对交易：请用 `$ab-ah-premium-monitor` 给出可选标的、入场/退出触发条件和注意事项。
5. 请用 `$ab-ah-premium-monitor` 生成一页“AB/AH 溢价监控面板”，包含指标、阈值与每周复盘要点。

## concept-board-analyzer

1. 请用 `$concept-board-analyzer` 分析概念板块 `<概念名>`：过去 5/20/60 日表现、成分股贡献和资金流。
2. 用 `$concept-board-analyzer` 给我做“概念轮动”复盘：最近一周最强/最弱概念、持续性与风险点。
3. 请用 `$concept-board-analyzer` 输出 `<概念名>` 的核心成分股清单（按市值/成交额/涨幅排序均可）并给出关注理由。
4. 我想找主题热点：请用 `$concept-board-analyzer` 扫描全市场概念热度，给出 Top 10 概念及对应龙头股。
5. 请用 `$concept-board-analyzer` 把 `<概念名>` 写成研究简报：结论 3–5 条 + 证据链 + 监控清单。

## convertible-bond-scanner

1. 请用 `$convertible-bond-scanner` 筛选可转债：按转股溢价率、余额、成交额、条款风险给出 Top 20 清单。
2. 用 `$convertible-bond-scanner` 分析 `<转债代码>`：溢价/正股联动、流动性、强赎/回售条款与主要风险。
3. 我想做低溢价转债策略：请用 `$convertible-bond-scanner` 给出筛选条件、风险过滤和执行注意事项。
4. 请用 `$convertible-bond-scanner` 生成“可转债市场温度计”：当前整体溢价水平、分位数与拥挤度提示。
5. 用 `$convertible-bond-scanner` 帮我从 `<股票池>` 找对应转债，并给出正股基本面+转债条款的联动结论。

## disclosure-notice-monitor

1. 请用 `$disclosure-notice-monitor` 监控 `<公司/股票池>` 的公告与披露：生成过去 30 天事件清单并评估影响。
2. 用 `$disclosure-notice-monitor` 给我做“财报披露日历”：`<月份/季度>` 哪些公司即将披露，重点风险提示是什么？
3. 请用 `$disclosure-notice-monitor` 梳理 `<公司>` 最近一次重大事项公告，提炼关键信息点与不确定性。
4. 我想做事件跟踪：请用 `$disclosure-notice-monitor` 输出“公告类型→潜在影响→需要验证的数据点”表格。
5. 请用 `$disclosure-notice-monitor` 做一份每周公告周报模板（含摘要、影响评估、待跟踪问题清单）。

## dividend-corporate-action-tracker

1. 请用 `$dividend-corporate-action-tracker` 汇总 `<公司>` 过去 5 年分红记录、股息率区间与分红稳定性评价。
2. 用 `$dividend-corporate-action-tracker` 跟踪 `<股票池>` 的除权除息/配股日历，给我一个未来 30 天提醒清单。
3. 请用 `$dividend-corporate-action-tracker` 分析 `<公司>` 最新分红方案：分红率、现金流覆盖、可持续性与风险点。
4. 我想做红利策略：请用 `$dividend-corporate-action-tracker` 给出高股息候选列表，并标注“高股息陷阱”风险。
5. 请用 `$dividend-corporate-action-tracker` 输出一页“分红监控面板”：关键指标、阈值与复盘问题。

## dragon-tiger-list-analyzer

1. 请用 `$dragon-tiger-list-analyzer` 复盘 `<日期>` 龙虎榜：机构席位/营业部净买入排名与异常成交提示。
2. 用 `$dragon-tiger-list-analyzer` 分析 `<股票>` 上榜原因、买卖席位结构、资金风格（机构/游资）与后续风险。
3. 请用 `$dragon-tiger-list-analyzer` 输出“最活跃营业部/机构席位”Top 20，并给出偏好板块与近期胜率观察。
4. 我想识别异常资金：请用 `$dragon-tiger-list-analyzer` 扫描近 30 天重复上榜个股，标注高波动与流动性风险。
5. 请用 `$dragon-tiger-list-analyzer` 生成龙虎榜周度复盘简报（结论、数据表、风险清单）。

## equity-pledge-risk-monitor

1. 请用 `$equity-pledge-risk-monitor` 扫描 `<股票池>` 的股权质押比例，输出高风险 Top 20 与行业对比。
2. 用 `$equity-pledge-risk-monitor` 分析 `<公司>`：质押主体、质押集中度、可能的平仓/控制权风险提示。
3. 请用 `$equity-pledge-risk-monitor` 做一份“质押风险红旗清单”：阈值、触发条件与后续核验步骤。
4. 我担心市场下跌引发连锁风险：请用 `$equity-pledge-risk-monitor` 给出情景假设下的风险放大路径。
5. 请用 `$equity-pledge-risk-monitor` 输出适合投委会的一页摘要：核心结论 + 关键数据 + 风险建议。

## equity-research-orchestrator

1. 请用 `$equity-research-orchestrator` 从头到尾研究 `<股票代码>`：行业地位、财务质量、估值、资金与风险，输出完整研究包。
2. 用 `$equity-research-orchestrator` 帮我把 `<股票池>` 做成“候选→尽调→跟踪”工作流，并产出统一模板。
3. 我需要快速决策：请用 `$equity-research-orchestrator` 给 `<股票>` 生成 1 页投资摘要（多空要点、关键风险、跟踪指标）。
4. 请用 `$equity-research-orchestrator` 对 `<股票>` 做“事件驱动 + 基本面 + 交易约束”三合一评估，并给行动建议。
5. 用 `$equity-research-orchestrator` 产出一份可直接发给客户的研究简报（结构化、含风险披露与数据口径）。

## esg-screener

1. 请用 `$esg-screener` 评估 `<公司>` 的 ESG 表现：环境/社会/治理拆解、争议事件与改进空间。
2. 用 `$esg-screener` 扫描 `<股票池/行业>`，给出 ESG 评分 Top/Bottom 10，并解释差异来源。
3. 我想做 ESG 排除清单：请用 `$esg-screener` 按 `<规则>`（如高污染/重大处罚/治理红旗）筛掉不合规标的。
4. 请用 `$esg-screener` 生成组合层面的 ESG 画像：行业暴露、争议事件风险和可持续主题覆盖度。
5. 用 `$esg-screener` 输出一份 ESG 研究简报模板，包含指标口径、打分方法与监控清单。

## etf-allocator

1. 请用 `$etf-allocator` 为我做 ETF 资产配置：资金 `<金额>`、风险偏好 `<保守/稳健/积极>`、期限 `<年数>`。
2. 用 `$etf-allocator` 分析 `<ETF代码列表>` 的行业/风格/因子暴露、相关性与重叠度，给出精简建议。
3. 我想用 ETF 做“核心-卫星”：请用 `$etf-allocator` 给出核心宽基 + 卫星行业/主题的组合方案与仓位上限。
4. 请用 `$etf-allocator` 对比 `<ETF A>` vs `<ETF B>`：跟踪误差、流动性、费率与适用场景。
5. 用 `$etf-allocator` 输出再平衡规则（阈值/定期）+ 执行清单（下单、滑点、成交约束）。

## event-driven-detector

1. 请用 `$event-driven-detector` 扫描近 30 天 A 股事件（并购重组/回购增持/管理层变更/指数调整），给出机会清单。
2. 用 `$event-driven-detector` 分析 `<公司>` 的 `<事件类型>`：交易结构、潜在催化、失败风险与时间线。
3. 我想做事件驱动策略：请用 `$event-driven-detector` 给出事件分类、筛选规则、风险过滤与跟踪指标。
4. 请用 `$event-driven-detector` 输出“事件→可能影响→验证数据→交易约束”的结构化表格。
5. 用 `$event-driven-detector` 生成一份每周事件雷达周报（重点事件、影响评估、观察清单）。

## event-study

1. 请用 `$event-study` 对 `<公司>` 的 `<事件日期>` 做事件窗研究：[-10,+10] 日超额收益与显著性解读。
2. 用 `$event-study` 比较 `<事件A>` vs `<事件B>` 对股价影响的差异（基准/同业调整口径说明）。
3. 我想验证“政策发布→行业上涨”是否成立：请用 `$event-study` 对 `<行业>` 做事件研究并给统计结论。
4. 请用 `$event-study` 输出事件窗图表与表格（累计超额收益、最大回撤、波动变化）。
5. 用 `$event-study` 给我一份可复用的事件研究模板（输入、窗口设置、对照组选择、注意事项）。

## factor-crowding-monitor

1. 请用 `$factor-crowding-monitor` 监控当前市场的因子拥挤度：价值/动量/质量/低波等，给出风险开关提示。
2. 用 `$factor-crowding-monitor` 回看近 1 年因子收益分化与拥挤变化，解释近期风格切换原因。
3. 我持有偏 `<因子>` 的组合：请用 `$factor-crowding-monitor` 评估“风格挤压”风险并给对冲/分散建议。
4. 请用 `$factor-crowding-monitor` 输出“拥挤因子 Top 5 + 反向因子 Top 5”，并说明触发阈值。
5. 用 `$factor-crowding-monitor` 做一份每周因子风格监控简报（结论、数据、风险清单）。

## financial-statement-analyzer

1. 请用 `$financial-statement-analyzer` 深度分析 `<公司>` 的三大报表：盈利质量、现金流、资产负债风险与结论摘要。
2. 用 `$financial-statement-analyzer` 做杜邦拆解：ROE 变化来自哪里？并给出可持续性判断。
3. 我担心财务造假：请用 `$financial-statement-analyzer` 做风险信号扫描（如应收、存货、现金流异常）并给证据链。
4. 请用 `$financial-statement-analyzer` 对比 `<公司>` vs `<可比公司>` 的利润率/周转/杠杆差异与原因。
5. 用 `$financial-statement-analyzer` 输出投委会风格的一页财务体检报告（关键指标、红旗、需要追问的问题）。

## findata-toolkit-cn

1. 请用 `$findata-toolkit-cn` 拉取 `<股票代码>` 的最新行情与估值指标，并以表格输出（注明数据日期/口径）。
2. 用 `$findata-toolkit-cn` 获取 `<公司>` 近 5 年财务关键指标（营收、利润、ROE、现金流等）并做成可复用数据块。
3. 请用 `$findata-toolkit-cn` 获取北向资金（沪股通/深股通）近 20 个交易日的净流入数据并汇总。
4. 用 `$findata-toolkit-cn` 拉取宏观数据（如 LPR、CPI/PPI、PMI、社融、M2）并生成一个“宏观面板”。
5. 我需要可复现的数据：请用 `$findata-toolkit-cn` 给出你调用的数据视图/脚本参数，并把结果按 JSON envelope 结构输出。

## fund-flow-monitor

1. 请用 `$fund-flow-monitor` 监控 `<股票/行业/概念>` 资金流：主力净流入、超大单/大单拆分与背离提示。
2. 用 `$fund-flow-monitor` 扫描全市场资金异动：给出今日净流入 Top 20 与“冲高回落/拉尾盘”等风险标签。
3. 请用 `$fund-flow-monitor` 回看近 20 日资金流与涨跌的关系，判断资金驱动还是情绪脉冲。
4. 我想跟踪板块资金：请用 `$fund-flow-monitor` 输出行业/概念资金流排名与持续性评分。
5. 用 `$fund-flow-monitor` 生成资金流周报模板（结论、榜单、拥挤与反转风险）。

## goodwill-risk-monitor

1. 请用 `$goodwill-risk-monitor` 扫描 `<行业/股票池>` 的商誉规模与占比，列出潜在减值高风险 Top 20。
2. 用 `$goodwill-risk-monitor` 分析 `<公司>` 商誉来源、并购历史、减值记录与预警信号。
3. 我担心财报“爆雷”：请用 `$goodwill-risk-monitor` 给出商誉减值情景推演及对利润/净资产的影响提示。
4. 请用 `$goodwill-risk-monitor` 输出商誉风险红旗清单（阈值、触发条件、需要验证的数据）。
5. 用 `$goodwill-risk-monitor` 生成一页投委会摘要：关键数据、风险结论与跟踪要点。

## high-dividend-strategy

1. 请用 `$high-dividend-strategy` 解释 A 股红利策略的核心逻辑，并给出适合的指数/ETF/个股筛选思路。
2. 用 `$high-dividend-strategy` 筛选 `<股票池>` 的高股息候选：股息率、分红稳定性、现金流覆盖与风险过滤。
3. 我想对比红利 vs 成长：请用 `$high-dividend-strategy` 给出在不同宏观环境下的相对表现与配置建议。
4. 请用 `$high-dividend-strategy` 对 `<公司>` 做“股息可持续性体检”：分红率、盈利质量、资本开支压力。
5. 用 `$high-dividend-strategy` 生成“红利组合”月度复盘模板（收益、风险、分红事件与再平衡）。

## hot-rank-sentiment-monitor

1. 请用 `$hot-rank-sentiment-monitor` 监控 `<股票>` 人气/热度趋势，判断是否出现情绪过热或背离。
2. 用 `$hot-rank-sentiment-monitor` 扫描今日人气榜 Top 50，标注高波动与拥挤风险，并给观察清单。
3. 我想看情绪拐点：请用 `$hot-rank-sentiment-monitor` 回看 `<股票>` 近 30 天热度变化与价格/成交的关系。
4. 请用 `$hot-rank-sentiment-monitor` 输出“热度上升但价格走弱”的背离标的清单，并解释可能原因。
5. 用 `$hot-rank-sentiment-monitor` 生成一份情绪监控周报（榜单、趋势、风险提示、跟踪规则）。

## hsgt-holdings-monitor

1. 请用 `$hsgt-holdings-monitor` 跟踪 `<股票池>` 的北向持仓变化：增减持、集中度与异常波动提示。
2. 用 `$hsgt-holdings-monitor` 输出近 20 日北向净买入 Top 20 个股/行业，并给“偏好轮动”解读。
3. 我想看外资是否在撤退：请用 `$hsgt-holdings-monitor` 给出北向持仓总量、行业分布与背离信号。
4. 请用 `$hsgt-holdings-monitor` 分析 `<股票>`：北向持仓占比、历史变化与对股价影响的证据。
5. 用 `$hsgt-holdings-monitor` 生成北向资金监控面板（指标、阈值、预警触发条件）。

## industry-board-analyzer

1. 请用 `$industry-board-analyzer` 对比申万一级行业近 1/3/6 个月表现、估值分位与资金流排名。
2. 用 `$industry-board-analyzer` 分析 `<行业>`：成分股结构、龙头贡献、景气与风险点。
3. 请用 `$industry-board-analyzer` 输出行业轮动信号：强弱切换、持续性评分与可能催化。
4. 我想做行业配置：请用 `$industry-board-analyzer` 给出“超配/低配”建议与需要监控的宏观变量。
5. 用 `$industry-board-analyzer` 生成行业复盘周报模板（榜单、变化原因、风险清单）。

## industry-chain-mapper

1. 请用 `$industry-chain-mapper` 为 `<产业/主题>` 画一张上下游产业链地图，并标注关键环节与代表公司。
2. 用 `$industry-chain-mapper` 跟踪 `<产业链>` 的景气信号：价格/产能/订单/库存等代理指标，给结论与风险点。
3. 我想找“传导链条”：请用 `$industry-chain-mapper` 解释 `<上游变量>` 如何影响 `<下游行业/公司>`，并给验证数据清单。
4. 请用 `$industry-chain-mapper` 输出“产业链公司池”（上游/中游/下游分组）+ 关注要点。
5. 用 `$industry-chain-mapper` 生成一份产业链研究简报（摘要、链条、景气指标、跟踪清单）。

## insider-trading-analyzer

1. 请用 `$insider-trading-analyzer` 扫描近 90 天董监高/重要股东增持行为，给出信号最强 Top 10 公司。
2. 用 `$insider-trading-analyzer` 分析 `<公司>` 的增减持：谁在买/卖、金额与频次、历史效果与解读。
3. 我只关心“集群增持”：请用 `$insider-trading-analyzer` 按“多人+近窗口+真金白银”筛选并输出清单。
4. 请用 `$insider-trading-analyzer` 对比 `<行业>` 内部人交易活跃度，找出管理层信心最强的子行业。
5. 用 `$insider-trading-analyzer` 生成内部人交易周报（摘要、榜单、风险过滤、待核验问题）。

## intraday-microstructure-analyzer

1. 请用 `$intraday-microstructure-analyzer` 分析 `<股票>` 的日内成交与盘口：量价结构、买卖盘强弱与异常点。
2. 用 `$intraday-microstructure-analyzer` 识别 `<股票>` 是否存在“拉尾盘/砸盘/对倒/异动放量”等微观结构信号。
3. 我想做短线风控：请用 `$intraday-microstructure-analyzer` 给出可交易性、滑点风险与下单建议（分笔/分时口径）。
4. 请用 `$intraday-microstructure-analyzer` 回看 `<日期>` 的日内走势，把关键时间点与成交峰值解释清楚。
5. 用 `$intraday-microstructure-analyzer` 输出一份日内结构复盘模板（结论、证据、风险标签、监控指标）。

## investment-memo-generator

1. 请用 `$investment-memo-generator` 为 `<股票/行业/主题>` 写一份投资备忘录：投资逻辑、关键假设、风险与跟踪指标。
2. 用 `$investment-memo-generator` 把我下面的要点整理成机构风格 memo（含结论摘要与行动项）：`<粘贴要点>`。
3. 我需要投委会版本：请用 `$investment-memo-generator` 输出 1 页摘要 + 附录数据清单的备忘录结构。
4. 请用 `$investment-memo-generator` 生成“多空对照”备忘录：多头论据、空头论据、如何证伪。
5. 用 `$investment-memo-generator` 生成一份可复用 memo 模板（不同场景：个股/行业/组合）。

## ipo-lockup-risk-monitor

1. 请用 `$ipo-lockup-risk-monitor` 输出 `<股票池>` 未来 90 天解禁时间表，并标注潜在供给冲击风险。
2. 用 `$ipo-lockup-risk-monitor` 分析 `<公司>`：解禁规模占比、股东结构、历史减持与风险提示。
3. 我想规避解禁雷：请用 `$ipo-lockup-risk-monitor` 给出“解禁风险标签”规则与过滤阈值。
4. 请用 `$ipo-lockup-risk-monitor` 回看近 1 年解禁后股价表现（分组统计），给出经验结论。
5. 用 `$ipo-lockup-risk-monitor` 生成解禁/减持周报（日历、重点公司、风险清单、跟踪问题）。

## ipo-newlist-monitor

1. 请用 `$ipo-newlist-monitor` 跟踪 `<时间窗口>` IPO 申报/过会/注册/上市进展，输出事件清单。
2. 用 `$ipo-newlist-monitor` 给我一个“新股/次新日历”：未来 30 天上市与重要节点提醒。
3. 我想找 IPO 受益股：请用 `$ipo-newlist-monitor` 列出可能受益的产业链公司与逻辑说明。
4. 请用 `$ipo-newlist-monitor` 复盘 `<日期>` 新股表现：涨跌、换手、情绪温度与风险提示。
5. 用 `$ipo-newlist-monitor` 生成一份每周 IPO 观察简报（摘要、日历、风险与监控清单）。

## limit-up-limit-down-risk-checker

1. 请用 `$limit-up-limit-down-risk-checker` 检查 `<股票/股票池>` 的涨跌停与停牌约束，给出可交易性风险标签。
2. 用 `$limit-up-limit-down-risk-checker` 分析 `<股票>`：近期封板/开板、跌停风险与“无法成交”情景提示。
3. 我准备在跌停附近交易：请用 `$limit-up-limit-down-risk-checker` 给出执行风险、下单策略与退出预案。
4. 请用 `$limit-up-limit-down-risk-checker` 输出适用于 A 股的交易约束清单（T+1、涨跌停、停牌等）并结合案例解释。
5. 用 `$limit-up-limit-down-risk-checker` 生成“交易前风控检查表”（输入→规则→风险→应对）。

## limit-up-pool-analyzer

1. 请用 `$limit-up-pool-analyzer` 复盘 `<日期>` 涨停池：连板梯队、题材强弱、情绪温度与风险点。
2. 用 `$limit-up-pool-analyzer` 分析 `<题材/概念>` 在涨停池中的占比与扩散路径，判断持续性。
3. 我想跟踪强势股：请用 `$limit-up-pool-analyzer` 输出“强势股观察清单”（梯队、换手、封单、风险标签）。
4. 请用 `$limit-up-pool-analyzer` 回看近 2 周连板结构变化，找出从“高度→退潮”的拐点信号。
5. 用 `$limit-up-pool-analyzer` 生成打板情绪周报模板（榜单、梯队、风险与纪律）。

## liquidity-impact-estimator

1. 请用 `$liquidity-impact-estimator` 评估 `<股票>` 的流动性：成交额/换手、盘口深度代理，并估算滑点风险。
2. 用 `$liquidity-impact-estimator` 评估我打算买入 `<金额>` 的冲击成本：给出分批下单建议与时间安排。
3. 请用 `$liquidity-impact-estimator` 扫描 `<股票池>`，标注“流动性不足/冲击成本高”的标的并给过滤阈值。
4. 我想做组合层面评估：请用 `$liquidity-impact-estimator` 给出组合的可交易性评分与最脆弱头寸。
5. 用 `$liquidity-impact-estimator` 输出“流动性风控清单”：指标、阈值、预警与执行要点。

## macro-liquidity-monitor

1. 请用 `$macro-liquidity-monitor` 总结当前宏观流动性环境：利率/通胀/信用/政策取向，并给资产含义。
2. 用 `$macro-liquidity-monitor` 做一个宏观流动性仪表盘（指标、更新频率、阈值与解读规则）。
3. 我想知道“宽松/收紧”对行业影响：请用 `$macro-liquidity-monitor` 给出行业敏感度排序与理由。
4. 请用 `$macro-liquidity-monitor` 回看近 2 年流动性拐点与市场表现的对应关系，提炼可复用信号。
5. 用 `$macro-liquidity-monitor` 生成每周宏观流动性简报模板（结论、数据、风险、观察清单）。

## margin-risk-monitor

1. 请用 `$margin-risk-monitor` 监控两融余额变化与拥挤度，判断是否存在“踩踏/波动放大”风险。
2. 用 `$margin-risk-monitor` 分析 `<股票/行业>` 的融资融券数据：杠杆上升是否过快？给风险提示。
3. 请用 `$margin-risk-monitor` 扫描全市场两融异常：余额激增/回落的 Top 20 标的与可能原因。
4. 我担心下跌加速：请用 `$margin-risk-monitor` 给出情景下的风险链条与建议的风控动作（降杠杆/止损/对冲）。
5. 用 `$margin-risk-monitor` 生成两融周度监控报告（摘要、榜单、阈值、预警规则）。

## market-breadth-monitor

1. 请用 `$market-breadth-monitor` 监控市场宽度：涨跌家数、新高新低、集中度与宽度动量，判断风险偏好。
2. 用 `$market-breadth-monitor` 回看近 6 个月宽度指标与指数走势的背离，解释“指数强但个股弱”的原因。
3. 请用 `$market-breadth-monitor` 输出“宽度转弱预警”触发条件，并给应对建议（降仓/防御/对冲）。
4. 我想做择时参考：请用 `$market-breadth-monitor` 给出当前市场状态（风险开/关）与信号可信度。
5. 用 `$market-breadth-monitor` 生成市场宽度周报模板（结论、指标表、风险提示）。

## market-overview-dashboard

1. 请用 `$market-overview-dashboard` 给我一页市场总貌：成交额、涨跌分布、行业/地区统计与资金概览。
2. 用 `$market-overview-dashboard` 对比上交所 vs 深交所：成交结构、活跃度变化与风险提示。
3. 请用 `$market-overview-dashboard` 回看近 20 个交易日市场状态变化，标注拐点与可能驱动。
4. 我需要晨会材料：请用 `$market-overview-dashboard` 输出“今日市场快览”固定模板（表格+要点）。
5. 用 `$market-overview-dashboard` 生成每周市场总貌复盘模板（关键数据、变化归因、风险清单）。

## northbound-flow-analyzer

1. 请用 `$northbound-flow-analyzer` 分析北向资金近 20 日净流入/流出与行业偏好，给背离信号提示。
2. 用 `$northbound-flow-analyzer` 输出今日北向净买入 Top 20 个股，并标注集中度与可持续性风险。
3. 我想判断外资风格切换：请用 `$northbound-flow-analyzer` 给出“偏好行业/因子”的变化与解释。
4. 请用 `$northbound-flow-analyzer` 分析 `<股票>`：北向持仓变化是否领先价格？给证据与反例。
5. 用 `$northbound-flow-analyzer` 生成北向资金监控面板（指标、阈值、预警规则）。

## peer-comparison-analyzer

1. 请用 `$peer-comparison-analyzer` 给 `<公司>` 找可比公司（同业）并做估值/成长/盈利能力/杠杆对比表。
2. 用 `$peer-comparison-analyzer` 对比 `<公司A>` vs `<公司B>`：差异来自哪里？哪些指标最关键？
3. 我想做估值合理性判断：请用 `$peer-comparison-analyzer` 输出同业分位数（PE/PB/EV等）并解释。
4. 请用 `$peer-comparison-analyzer` 生成一页“同业对比卡片”（核心指标、优势/短板、需要核验的问题）。
5. 用 `$peer-comparison-analyzer` 给出同业对比的口径说明（会计差异、一次性项目、周期位置）与注意事项。

## policy-sensitivity-brief

1. 请用 `$policy-sensitivity-brief` 分析 `<政策/文件>` 可能影响哪些行业/风格，并给出敏感度清单。
2. 用 `$policy-sensitivity-brief` 把 `<宏观数据发布>` 映射到行业景气：给情景推演与监控指标。
3. 我想做政策跟踪：请用 `$policy-sensitivity-brief` 输出“政策事件日历 + 行业影响矩阵”模板。
4. 请用 `$policy-sensitivity-brief` 对 `<行业>` 做政策风险评估：利好/利空路径、证伪条件与执行约束。
5. 用 `$policy-sensitivity-brief` 生成每周政策敏感度简报（摘要、影响排序、观察清单）。

## portfolio-health-check

1. 请用 `$portfolio-health-check` 诊断我的组合：`<持仓清单>`（代码+金额/比例），输出集中度、相关性与因子暴露问题。
2. 用 `$portfolio-health-check` 做压力测试：假设指数下跌 `<X%>`/行业冲击 `<情景>`，组合可能回撤多少？
3. 我担心“看似分散其实相关”：请用 `$portfolio-health-check` 识别相关性聚集的持仓群组并给调整建议。
4. 请用 `$portfolio-health-check` 检查我的组合是否过度暴露于 `<风格/因子>`（如成长/小盘/高波），并给纠偏方案。
5. 用 `$portfolio-health-check` 输出一份可执行的整改清单（减仓/替换/对冲/再平衡规则）。

## portfolio-monitor-orchestrator

1. 请用 `$portfolio-monitor-orchestrator` 为我的组合建立持续监控：集中度、相关性、因子暴露、流动性与情景压力。
2. 用 `$portfolio-monitor-orchestrator` 生成一份“组合监控日报/周报”固定模板（指标表+风险预警+行动项）。
3. 我想加风控阈值：请用 `$portfolio-monitor-orchestrator` 设计预警规则（如回撤、单股上限、行业偏离、流动性缺口）。
4. 请用 `$portfolio-monitor-orchestrator` 把 `<组合>` 与 `<基准>` 对比：跟踪误差、主动份额与偏离来源。
5. 用 `$portfolio-monitor-orchestrator` 输出“组合风险开关”结论（开/半开/关）并解释依据与下一步。

## quant-factor-screener

1. 请用 `$quant-factor-screener` 做多因子选股：价值+质量+动量（可自定义权重），输出 Top 50 候选。
2. 用 `$quant-factor-screener` 给 `<股票>` 打因子分：价值/动量/质量/规模等，并解释短板与优势。
3. 我想做 Smart Beta：请用 `$quant-factor-screener` 给出因子组合方案、再平衡频率与风险控制。
4. 请用 `$quant-factor-screener` 扫描 `<行业>` 内的因子龙头/落后者，并给出可能原因与风险提示。
5. 用 `$quant-factor-screener` 生成因子选股周报模板（榜单、因子环境、拥挤与回撤风险）。

## rebalancing-planner

1. 请用 `$rebalancing-planner` 为我的组合设计再平衡规则：阈值/定期/混合，并给执行清单。
2. 用 `$rebalancing-planner` 根据 `<目标权重>` 和 `<当前权重>` 计算需要买卖的调整方案（考虑交易成本与约束）。
3. 我想控制行业偏离：请用 `$rebalancing-planner` 设计“行业/单股上限”约束下的再平衡策略。
4. 请用 `$rebalancing-planner` 给出“何时不该再平衡”的条件（流动性不足、涨跌停、重大事件等）。
5. 用 `$rebalancing-planner` 输出一份可复用再平衡 SOP（输入、规则、下单、复盘）。

## risk-adjusted-return-optimizer

1. 请用 `$risk-adjusted-return-optimizer` 按资金 `<金额>`、风险偏好 `<保守/稳健/积极>`、期限 `<年数>` 给我构建最优组合。
2. 用 `$risk-adjusted-return-optimizer` 把我的现有持仓 `<持仓清单>` 纳入优化，给出调整后的目标权重与理由。
3. 我想提高夏普比率：请用 `$risk-adjusted-return-optimizer` 提供资产配置建议（权益/固收/黄金/REITs/现金）并说明约束。
4. 请用 `$risk-adjusted-return-optimizer` 输出风险指标（预期收益、波动、VaR/CVaR、最大回撤估计）与下行保护建议。
5. 用 `$risk-adjusted-return-optimizer` 生成一份“组合构建报告”（含再平衡规则与执行注意事项）。

## sector-rotation-detector

1. 请用 `$sector-rotation-detector` 判断当前经济周期位置，并给未来 6–12 个月可能跑赢/跑输的行业清单。
2. 用 `$sector-rotation-detector` 把利率/通胀/信用等宏观变量映射到行业轮动信号，给配置建议。
3. 我想做行业择时：请用 `$sector-rotation-detector` 输出轮动指标、阈值与信号可信度评分。
4. 请用 `$sector-rotation-detector` 回看近 5 年行业轮动的典型阶段（复盘案例+关键宏观拐点）。
5. 用 `$sector-rotation-detector` 生成行业轮动周报模板（结论、信号、风险与观察清单）。

## sentiment-reality-gap

1. 请用 `$sentiment-reality-gap` 寻找“情绪过度看空但基本面稳健”的逆向机会，输出候选 Top 20。
2. 用 `$sentiment-reality-gap` 分析 `<股票>`：市场在担心什么？基本面是否能证伪？给证据链。
3. 我想找“错杀”公司：请用 `$sentiment-reality-gap` 在 `<行业>` 内筛选负面情绪最强但财务质量较好的标的。
4. 请用 `$sentiment-reality-gap` 给出逆向策略的风险控制（催化缺失、流动性、下行保护）与跟踪指标。
5. 用 `$sentiment-reality-gap` 生成逆向机会周报模板（候选、理由、证伪条件、行动项）。

## shareholder-risk-check

1. 请用 `$shareholder-risk-check` 检查 `<公司>` 的治理红旗：股东结构、质押、控制权稳定性与风险标签。
2. 用 `$shareholder-risk-check` 扫描 `<股票池>`，输出治理风险 Top 20（控制权不稳/高质押/股东集中等）。
3. 我担心“控制权争夺”：请用 `$shareholder-risk-check` 给 `<公司>` 做情景分析与需要关注的公告清单。
4. 请用 `$shareholder-risk-check` 输出一份投前尽调的股东风险清单（需要查证的问题与数据口径）。
5. 用 `$shareholder-risk-check` 生成一页治理风险摘要（关键结论、证据、跟踪要点）。

## shareholder-structure-monitor

1. 请用 `$shareholder-structure-monitor` 跟踪 `<公司>` 股东户数与十大股东变化，判断筹码集中/分散趋势。
2. 用 `$shareholder-structure-monitor` 输出 `<股票>` 机构/基金持股变化与集中度风险提示。
3. 我想找“筹码改善”标的：请用 `$shareholder-structure-monitor` 扫描 `<股票池>`，给出户数下降/机构增持 Top 20。
4. 请用 `$shareholder-structure-monitor` 分析 `<行业>` 的筹码结构差异：哪些子行业更集中？风险在哪里？
5. 用 `$shareholder-structure-monitor` 生成筹码结构周报模板（变化、原因假设、风险与验证清单）。

## small-cap-growth-identifier

1. 请用 `$small-cap-growth-identifier` 筛选小市值高成长公司：营收/利润增速、景气与风险过滤，输出 Top 30。
2. 用 `$small-cap-growth-identifier` 在 `<行业>` 内找“被忽视的专精特新”候选，并给出筛选依据。
3. 我想做小盘成长组合：请用 `$small-cap-growth-identifier` 给出选股规则、仓位上限与流动性风险提示。
4. 请用 `$small-cap-growth-identifier` 分析 `<公司>`：成长驱动是什么？是否可持续？关键风险有哪些？
5. 用 `$small-cap-growth-identifier` 生成小盘成长周报模板（候选、逻辑、风险、跟踪指标）。

## st-delist-risk-scanner

1. 请用 `$st-delist-risk-scanner` 扫描 ST/退市风险标的，输出风险标签、触发原因与可交易性约束。
2. 用 `$st-delist-risk-scanner` 分析 `<公司>`：ST 原因、整改进度、退市规则相关风险与注意事项。
3. 我想避开退市雷：请用 `$st-delist-risk-scanner` 给出过滤规则（财务指标/审计意见/交易状态）与阈值。
4. 请用 `$st-delist-risk-scanner` 输出“高风险清单”并按风险等级排序，标注停牌/流动性风险。
5. 用 `$st-delist-risk-scanner` 生成退市风险周报模板（清单、规则解读、监控要点）。

## suitability-report-generator

1. 请用 `$suitability-report-generator` 为 `<客户画像>` + `<产品/组合>` 生成投资适当性报告（含风险披露与匹配结论）。
2. 用 `$suitability-report-generator` 把我的投资建议整理成合规文档：投资理由、风险提示、客户适当性评估。
3. 我需要留痕：请用 `$suitability-report-generator` 生成“投顾建议记录”模板（日期、假设、证据、风险、回访）。
4. 请用 `$suitability-report-generator` 针对 `<策略>` 输出适当性边界（不适合哪些客户、需要哪些确认）。
5. 用 `$suitability-report-generator` 生成可直接交付的 PDF/Word 风格结构（标题、目录、正文段落提示）。

## tech-hype-vs-fundamentals

1. 请用 `$tech-hype-vs-fundamentals` 分析 `<科技公司/板块>`：估值是否透支？增长能否兑现？给结论与证据。
2. 用 `$tech-hype-vs-fundamentals` 对比 `<公司A>` vs `<公司B>`：同样讲 AI/芯片/新能源，谁更“有基本面”？
3. 我担心泡沫：请用 `$tech-hype-vs-fundamentals` 给出估值分位数、情绪指标与下行风险情景。
4. 请用 `$tech-hype-vs-fundamentals` 找“被低估的科技股”：基本面强、估值合理的候选 Top 20。
5. 用 `$tech-hype-vs-fundamentals` 生成科技估值周报模板（热度、估值、兑现进度、风险清单）。

## undervalued-stock-screener

1. 请用 `$undervalued-stock-screener` 扫描 A 股低估值机会：低 PE/PB + 基本面过滤，输出 Top 50。
2. 用 `$undervalued-stock-screener` 在 `<行业>` 内筛选“被低估但盈利改善”的公司清单，并解释筛选逻辑。
3. 我想避免价值陷阱：请用 `$undervalued-stock-screener` 增加风险过滤（现金流、负债、商誉、治理红旗）并输出结果。
4. 请用 `$undervalued-stock-screener` 分析 `<公司>`：为什么便宜？是周期低点还是结构性问题？给证据链。
5. 用 `$undervalued-stock-screener` 生成价值选股周报模板（候选、估值分位、催化、风险与证伪条件）。

## valuation-regime-detector

1. 请用 `$valuation-regime-detector` 判断 `<市场/行业/个股>` 当前估值处于历史什么分位（贵/中性/便宜）并解释原因。
2. 用 `$valuation-regime-detector` 回看近 10 年估值中枢变化，与利率/宏观变量的关系是什么？
3. 我想做估值择时：请用 `$valuation-regime-detector` 给出“极端高估/低估”阈值与策略建议。
4. 请用 `$valuation-regime-detector` 对比 `<行业A>` vs `<行业B>` 的估值分位与均值回归风险。
5. 用 `$valuation-regime-detector` 生成估值监控面板模板（分位数、区间、触发条件、风险提示）。

## volatility-regime-monitor

1. 请用 `$volatility-regime-monitor` 判断当前市场波动率状态（低/中/高波动），并给风险开关建议。
2. 用 `$volatility-regime-monitor` 分析 `<股票/指数>`：实现波动、回撤、波动的波动，并给预警阈值。
3. 我想做仓位管理：请用 `$volatility-regime-monitor` 给出“随波动调整仓位”的规则与示例。
4. 请用 `$volatility-regime-monitor` 回看近 2 年波动率状态切换与市场表现，提炼可复用信号。
5. 用 `$volatility-regime-monitor` 生成波动监控周报模板（指标、状态、预警与行动项）。

## weekly-market-brief-generator

1. 请用 `$weekly-market-brief-generator` 生成本周市场周报：指数表现、宏观、资金、风险与观察清单（固定结构）。
2. 用 `$weekly-market-brief-generator` 做周度复盘：本周主线题材、行业强弱、北向/两融/资金流变化与结论。
3. 我需要晨会材料：请用 `$weekly-market-brief-generator` 输出可直接展示的表格与要点（不超过 1–2 页）。
4. 请用 `$weekly-market-brief-generator` 加入“下周关注”模块：宏观事件日历、财报披露、解禁/减持风险。
5. 用 `$weekly-market-brief-generator` 生成一份可复用周报模板（占位符+示例输出）。

## block-deal-monitor

1. 请用 `$block-deal-monitor` 扫描近 20 日A股大宗交易：按成交金额 Top 50，并标注折价率与“抛压/承接”标签。
2. 用 `$block-deal-monitor` 分析 `<股票>` 近 90 天大宗交易：是否存在连续成交？更像建仓还是派发？给证据与风险。
3. 我想找“承接强”的票：请用 `$block-deal-monitor` 找出“折价较大但股价不跌/回撤浅”的标的清单。
4. 请用 `$block-deal-monitor` 输出大宗交易风控清单：哪些折价/金额/连续性组合需要回避？给阈值与解释。
5. 用 `$block-deal-monitor` 生成大宗交易周报模板（榜单、案例复盘、风险与后续验证问题）。

## share-repurchase-monitor

1. 请用 `$share-repurchase-monitor` 扫描近 90 天A股回购事件：按回购上限金额/完成度输出 Top 50，并做信号分层（强/中/弱）。
2. 用 `$share-repurchase-monitor` 分析 `<股票>` 的回购：目的、实施节奏、回购均价 vs 现价、利好兑现风险与跟踪点。
3. 我想做“回购+低估”组合：请用 `$share-repurchase-monitor` 给出筛选条件与风险过滤（现金流、负债、减持/解禁叠加）。
4. 请用 `$share-repurchase-monitor` 找“公告大但不实施”的公司清单，并给风险提示与证伪条件。
5. 用 `$share-repurchase-monitor` 生成回购监控面板模板（关键字段、阈值、预警与行动项）。

## bse-selection-analyzer

1. 请用 `$bse-selection-analyzer` 从北交所筛选“可交易”的候选：先按日均成交额过滤，再按成长性输出 Top 30，并提示流动性风险。
2. 用 `$bse-selection-analyzer` 分析 `<北交所股票/列表>`：成长性、现金流质量、波动与退出难度，给风控建议。
3. 我想做“专精特新”主题：请用 `$bse-selection-analyzer` 输出主题候选清单，并标注产业链位置与风险点。
4. 请用 `$bse-selection-analyzer` 做一份北交所组合的仓位与执行规则（单票上限、分批、最大滑点、退出条件）。
5. 用 `$bse-selection-analyzer` 生成北交所周度复盘模板（表现、流动性、风险事件、观察清单）。
