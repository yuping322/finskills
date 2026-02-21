# Financial Analysis Skills for Kiro

专业的金融市场分析 skills 集合，支持中国A股、香港、美国三个市场。

## 📊 Skills 概览

- **总计**：107 个专业 skills
- **中国市场**：57 个（A股风险监控、市场分析、投资组合管理等）
- **香港市场**：13 个（汇率风险、南向资金、流动性监控等）
- **美国市场**：37 个（信用利差、收益率曲线、税务规划等）

## 🚀 快速开始

### 1. 环境设置（首次使用）

```bash
make install-cn
```

### 2. 测试配置

```bash
make cn-smoke-validate
```

### 3. 开始使用

在 Kiro 中直接提问：

```
帮我分析一下最近的大宗交易情况
检查一下有哪些股票有ST退市风险
分析一下南向资金最近的流向
```

## 📚 文档

| 文档 | 说明 |
|------|------|
| [docs/SETUP_COMPLETE.md](docs/SETUP_COMPLETE.md) | ✅ 配置完成状态 |
| [docs/QUICK_START.md](docs/QUICK_START.md) | 快速开始指南 |
| [docs/SKILLS_MAP.md](docs/SKILLS_MAP.md) | 完整的 107 个 skills 索引 |
| [docs/HOW_TO_USE_SKILLS.md](docs/HOW_TO_USE_SKILLS.md) | 详细使用说明 |
| [docs/SKILLS_VS_DATA.md](docs/SKILLS_VS_DATA.md) | ⚠️ Skills vs 数据脚本区别 |

## 🧪 测试工具

| 工具 | 说明 |
|------|------|
| [docs/TEST_TOOLS_README.md](docs/TEST_TOOLS_README.md) | 测试工具集概览 |
| [docs/QUICK_TEST_GUIDE.md](docs/QUICK_TEST_GUIDE.md) | ⭐ 快速测试指南（3步开始） |
| [docs/BATCH_TEST_GUIDE.md](docs/BATCH_TEST_GUIDE.md) | 批量测试详细指南 |
| `testing/auto_test_skills.py` | 生成测试模板（推荐） |
| `testing/batch_test_skills.sh` | 批量测试脚本 |

### 快速测试

```bash
# 1. 生成测试模板
python3 testing/auto_test_skills.py

# 2. 查看测试用例
cat testing/test-results/<时间戳>/.prompt_01.txt

# 3. 在 Kiro 中测试并记录结果
```

详见：[docs/QUICK_TEST_GUIDE.md](docs/QUICK_TEST_GUIDE.md)

## 🗂️ 项目结构

```
.
├── China-market/          # 中国A股市场 skills (57个)
│   ├── block-deal-monitor/
│   ├── dragon-tiger-list-analyzer/
│   ├── equity-pledge-risk-monitor/
│   ├── findata-toolkit-cn/    # A股数据工具包
│   └── ...
├── HK-market/             # 香港市场 skills (13个)
│   ├── hk-southbound-flow/
│   ├── hk-valuation-analyzer/
│   ├── findata-toolkit-hk/    # 港股数据工具包
│   └── ...
├── US-market/             # 美国市场 skills (37个)
│   ├── equity-research-orchestrator/
│   ├── yield-curve-regime-detector/
│   ├── findata-toolkit/       # 美股数据工具包
│   └── ...
├── .kiro/
│   └── steering/
│       └── market-analysis-skills.md  # Kiro 自动加载的配置
├── docs/                  # 文档目录
│   ├── SKILLS_MAP.md      # Skills 完整索引
│   ├── QUICK_START.md     # 快速开始指南
│   ├── HOW_TO_USE_SKILLS.md
│   └── ...
├── testing/               # 测试工具和结果
│   ├── auto_test_skills.py
│   ├── batch_test_skills.sh
│   └── test-results/      # 测试结果（不提交到git）
├── .venv/                 # Python 虚拟环境
├── Makefile               # 构建和测试命令
└── README.md              # 本文件
```

## 🎯 Skills 分类

### 中国市场 (China-market)

#### 风险监控类
- ST退市风险扫描器
- 股权质押风险监控
- IPO解禁风险监控
- 商誉减值风险监控
- 股东风险检查
- 融资融券风险监控
- 涨跌停风险检查器

#### 市场分析类
- 龙虎榜分析器
- 大宗交易监控
- 北向资金流向分析
- 资金流监控
- 市场宽度监控
- 板块轮动检测器
- 概念板块分析器
- 估值区间检测器
- 波动率区间监控

#### 投资组合类
- 投资组合监控编排器
- 投资组合健康检查
- 再平衡规划器
- 风险调整收益优化器
- ETF配置器

#### 研究工具类
- 股票研究流程编排器
- 财务报表分析器
- 同业对比分析器
- 事件研究
- 投资备忘录生成器

### 香港市场 (HK-market)

- 港股集中度风险监控
- 港股汇率风险监控
- 港股流动性风险监控
- 港股市场概览
- 港股南向资金流向
- 港股外资流向
- 港股估值分析
- 港股财务报表分析

### 美国市场 (US-market)

- 信用利差监控
- 收益率曲线区间检测器
- 税务感知再平衡规划器
- 期权策略分析器
- 内幕交易分析器
- 股息贵族计算器

## 💡 使用示例

### 示例 1：大宗交易分析

```bash
# 在 Kiro 中
你：帮我分析一下最近5天的大宗交易情况，重点关注折价率超过7%的交易

# 或直接运行脚本
.venv/bin/python3 China-market/findata-toolkit-cn/scripts/views_runner.py block_deal_dashboard --set start_date=20260214 --set end_date=20260221
```

### 示例 2：风险监控

```bash
# 在 Kiro 中
你：检查一下我的持仓中有没有股权质押风险
你：有哪些股票即将解禁？
你：帮我扫描一下ST退市风险
```

### 示例 3：市场分析

```bash
# 在 Kiro 中
你：分析一下最近的龙虎榜数据
你：北向资金最近流向哪些板块？
你：给我生成一份周度市场简报
```

## 🔧 技术栈

- **Python**: 3.9+
- **数据源**: AKShare（免费，无需API密钥）
- **核心库**: pandas, numpy, akshare
- **IDE集成**: Kiro

## 📖 Skill 标准结构

每个 skill 包含：

```
{skill-name}/
├── SKILL.md                    # 技能说明和工作流程
├── LICENSE.txt                 # 许可证
└── references/                 # 参考文档
    ├── methodology.md          # 方法论、指标定义、阈值
    ├── data-queries.md         # 数据获取方式
    └── output-template.md      # 输出格式模板
```

## 🛠️ 开发指南

### 添加新的 Skill

1. 在对应市场目录下创建新文件夹（kebab-case 命名）
2. 按照标准结构创建文件
3. 在 `docs/SKILLS_MAP.md` 中添加索引条目
4. 测试 skill 是否正常工作

### 贡献代码

1. Fork 本仓库
2. 创建特性分支
3. 提交更改
4. 发起 Pull Request

## 📋 可用命令

```bash
# 环境设置
make venv                  # 创建虚拟环境
make install-cn            # 安装中国市场依赖

# 测试
make cn-smoke-validate     # 运行烟雾测试
make cn-healthcheck        # 运行健康检查

# 自定义测试
python3 testing/auto_test_skills.py    # 生成测试模板
```

## ⚠️ 免责声明

所有 skills 输出仅供信息参考与教育目的，不构成投资建议。投资有风险，决策需谨慎。

## 📄 许可证

Apache-2.0 License

## 🤝 支持

- 查看文档：`docs/QUICK_START.md`, `docs/HOW_TO_USE_SKILLS.md`
- 在 Kiro 中提问获取帮助
- 查看各 skill 的详细文档

---

**最后更新**：2026-02-21

**状态**：✅ 环境配置完成，所有测试通过

开始使用 skills 吧！🎉
