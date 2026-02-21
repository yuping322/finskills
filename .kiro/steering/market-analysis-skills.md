---
inclusion: auto
---

# 市场分析 Skills 使用指南

本工作区包含 107 个专业的市场分析 skills，覆盖中国A股、香港、美国三个市场。

## Skills 索引位置

完整的 skills 索引文档位于：`SKILLS_MAP.md`

## 如何使用 Skills

当用户提出市场分析、投资研究、风险监控等需求时：

1. **查找相关 Skill**：
   - 根据用户需求关键词，在 `SKILLS_MAP.md` 中查找匹配的 skill
   - 每个 skill 都有清晰的描述和关键词标签

2. **读取 Skill 文档**：
   - 定位到具体目录：`{market-name}/{skill-name}/`
   - 读取 `SKILL.md` 了解工作流程和使用方法
   - 查看 `references/methodology.md` 了解方法论和指标定义
   - 查看 `references/data-queries.md` 了解数据获取方式
   - 查看 `references/output-template.md` 了解输出格式

3. **应用 Skill**：
   - 按照 SKILL.md 中的工作流程执行分析
   - 使用 methodology.md 中定义的指标和阈值
   - 按照 output-template.md 格式化输出结果

## Skill 目录结构

```
{market-name}/{skill-name}/
├── SKILL.md              # 技能说明和工作流程
├── LICENSE.txt           # 许可证
└── references/           # 参考文档目录
    ├── methodology.md    # 方法论和指标定义
    ├── data-queries.md   # 数据获取说明
    └── output-template.md # 输出格式模板
```

## 市场分类

- **China-market/**: 57 个 A股市场分析 skills
- **HK-market/**: 13 个香港市场分析 skills  
- **US-market/**: 37 个美国市场分析 skills

## 常用 Skills 快速参考

### 风险监控
- `China-market/st-delist-risk-scanner` - ST退市风险扫描
- `China-market/equity-pledge-risk-monitor` - 股权质押风险监控
- `HK-market/hk-liquidity-risk` - 港股流动性风险监控

### 市场分析
- `China-market/dragon-tiger-list-analyzer` - 龙虎榜分析
- `China-market/block-deal-monitor` - 大宗交易监控
- `HK-market/hk-southbound-flow` - 南向资金流向分析

### 投资组合
- `China-market/portfolio-monitor-orchestrator` - 投资组合监控编排
- `China-market/rebalancing-planner` - 再平衡规划
- `US-market/tax-aware-rebalancing-planner` - 税务感知再平衡

### 研究工具
- `China-market/equity-research-orchestrator` - 股票研究流程编排
- `China-market/financial-statement-analyzer` - 财务报表分析
- `HK-market/hk-valuation-analyzer` - 港股估值分析

## 数据工具包

- `China-market/findata-toolkit-cn` - A股数据获取工具（基于 akshare）
- `HK-market/findata-toolkit-hk` - 港股数据获取工具
- `US-market/findata-toolkit` - 美股数据获取工具（基于 yfinance）

## 重要提示

1. **数据获取**：大多数 skills 需要实时市场数据，请先查看对应的 `findata-toolkit` 使用说明
2. **方法论**：每个 skill 的 `methodology.md` 包含关键指标定义和阈值，务必参考
3. **输出格式**：按照 `output-template.md` 格式化输出，保持一致性
4. **免责声明**：所有 skills 输出仅供信息参考与教育目的，不构成投资建议

## 示例使用流程

用户问："帮我分析一下最近的大宗交易情况"

1. 在 SKILLS_MAP.md 中搜索"大宗交易"关键词
2. 找到 `China-market/block-deal-monitor`
3. 读取 `China-market/block-deal-monitor/SKILL.md`
4. 按照工作流程执行：
   - 确认输入参数（范围、时间窗口、阈值）
   - 获取数据（参考 data-queries.md）
   - 应用分析框架（参考 methodology.md）
   - 格式化输出（参考 output-template.md）
