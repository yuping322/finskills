# 如何在 Kiro 中使用 Market Analysis Skills

本仓库包含 107 个专业的市场分析 skills，现在已经配置好可以在 Kiro 中使用。

## ⚠️ 重要概念

**Skill ≠ 数据脚本！**

- **Skill**（完整体验）= 大模型 + 数据 + 方法论 + 分析框架 + 结构化输出 + 可执行建议
- **数据脚本**（底层工具）= 仅获取原始 JSON 数据

**推荐使用方式**：在 Kiro 中直接提问，享受完整的 Skill 体验！

详细说明请查看：[SKILLS_VS_DATA.md](SKILLS_VS_DATA.md)

## 快速开始

### 1. 查找你需要的 Skill

打开 `SKILLS_MAP.md`，根据你的需求查找对应的 skill：

```
例如：想分析大宗交易 → 搜索"大宗交易" → 找到 China-market/block-deal-monitor
```

### 2. 在 Kiro 中使用

直接在 Kiro 对话中提出需求，大模型会自动：
1. 从 SKILLS_MAP.md 中查找相关 skill
2. 读取对应的 SKILL.md 和参考文档
3. 按照 skill 的工作流程执行分析
4. 按照标准格式输出结果

### 3. 使用示例

**示例 1：分析大宗交易**
```
你：帮我分析一下最近的大宗交易情况，重点关注折价率超过7%的交易

Kiro 会：
1. 读取 China-market/block-deal-monitor/SKILL.md
2. 按照工作流程确认参数
3. 参考 methodology.md 应用分析框架
4. 按照 output-template.md 格式化输出
```

**示例 2：监控股权质押风险**
```
你：检查一下我的持仓中有没有股权质押风险

Kiro 会：
1. 读取 China-market/equity-pledge-risk-monitor/SKILL.md
2. 获取质押数据
3. 应用风险评估框架
4. 输出风险清单和监控建议
```

**示例 3：港股南向资金分析**
```
你：分析一下最近南向资金的流向

Kiro 会：
1. 读取 HK-market/hk-southbound-flow/SKILL.md
2. 获取南向资金数据
3. 分析流向和持仓变化
4. 输出分析报告
```

## 配置说明

### 已完成的配置

✅ 创建了 `.kiro/steering/market-analysis-skills.md`（自动包含）
✅ 创建了 `SKILLS_MAP.md`（完整索引）
✅ 所有 skills 文档已就位
✅ 虚拟环境已配置（`.venv`）
✅ 数据工具包依赖已安装

### 环境设置（首次使用）

如果虚拟环境未设置，运行：

```bash
./setup_skills_env.sh
```

这会自动：
- 创建 Python 虚拟环境（`.venv`）
- 安装所有数据工具包依赖（akshare, pandas, numpy 等）
- 验证安装是否成功

### Steering 机制

`.kiro/steering/market-analysis-skills.md` 文件会自动被 Kiro 加载，让大模型知道：
- 有哪些 skills 可用
- 如何查找和使用这些 skills
- Skills 的目录结构和文档位置

## 可用的 Skills 分类

### 中国市场 (57 个)
- 风险监控：ST退市、股权质押、解禁风险等
- 市场分析：龙虎榜、大宗交易、北向资金等
- 投资组合：组合监控、再平衡、风险优化等
- 研究工具：个股研究、财报分析、同业对比等

### 香港市场 (13 个)
- 风险监控：集中度、汇率、流动性风险
- 市场分析：南向资金、外资流向、板块轮动
- 研究工具：财报分析、估值分析、股息跟踪

### 美国市场 (37 个)
- 风险监控：信用利差监控
- 市场分析：市场宽度、板块轮动、收益率曲线
- 投资组合：税务感知再平衡、风险优化
- 研究工具：财报分析、内幕交易、期权策略

## 数据获取

每个市场都有对应的数据工具包：

- **A股数据**：`China-market/findata-toolkit-cn`（基于 akshare）
- **港股数据**：`HK-market/findata-toolkit-hk`
- **美股数据**：`US-market/findata-toolkit`（基于 yfinance）

查看各工具包的 `SKILL.md` 和 `references/data-queries.md` 了解使用方法。

**注意**：数据工具包只是底层工具，直接运行只会返回原始 JSON 数据。要获得完整的分析报告，请在 Kiro 中使用 Skills。

## 测试 Skills

你可以尝试以下问题来测试 skills（在 Kiro 中提问）：

1. "帮我分析一下最近的龙虎榜数据"
2. "检查一下有哪些股票有ST退市风险"
3. "分析一下南向资金最近的流向"
4. "给我生成一份周度市场简报"
5. "帮我做一个投资组合健康检查"

**这些都是完整的 Skill 体验**，包含数据获取、方法论应用、分析框架、风险提示和改进建议。

## 高级用法

### 组合使用多个 Skills

某些 skills（如 `equity-research-orchestrator`）会自动调用其他相关 skills，形成完整的分析流程。

### 自定义参数

每个 skill 都支持自定义参数（时间窗口、阈值、筛选条件等），在对话中明确说明即可。

### 数据导入

如果你有自己的数据源，可以直接提供数据，skills 会基于你的数据进行分析。

## 故障排查

**问题：Kiro 没有使用 skill**
- 检查 `.kiro/steering/market-analysis-skills.md` 是否存在
- 尝试更明确地描述需求，包含关键词

**问题：找不到数据**
- 查看对应的 `findata-toolkit` 使用说明
- 确认数据源是否可用
- 可以提供自己的数据

**问题：输出格式不符合预期**
- 明确要求按照 skill 的 output-template 格式输出
- 提供具体的格式要求

## 贡献新的 Skills

如果你想添加新的 skill：

1. 在对应市场目录下创建新文件夹（kebab-case 命名）
2. 按照标准结构创建文件（SKILL.md, LICENSE.txt, references/）
3. 在 `SKILLS_MAP.md` 中添加索引条目
4. 测试新 skill 是否正常工作

## 反馈和改进

如果你发现任何问题或有改进建议，欢迎：
- 更新对应 skill 的文档
- 在 SKILLS_MAP.md 中补充说明
- 创建新的 steering 规则优化使用体验
