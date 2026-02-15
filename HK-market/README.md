# HK Market Skills 港股市场技能

港股市场金融分析技能集合，涵盖港股特有的交易机制、监管环境和投资策略。

## 🌟 港股市场特点

### 市场特征
- **T+2 交割制度**：不同于A股的T+1和美股的T+2
- **港币计价**：汇率风险考虑
- **国际投资者主导**：外资占比高
- **自由兑换**：资本流动自由
- **无涨跌停限制**：价格波动更大
- **做市商制度**：流动性提供机制

### 监管环境
- **香港证监会(SFC)**监管
- **上市规则**：主板vs创业板
- **信息披露**：与A股、美股不同的披露要求
- **公司治理**：国际标准

## 📊 技能分类

### 1. 市场监控类 (Market Monitoring)
- `hk-market-overview` - 港股市场概览
- `hk-market-breadth` - 市场广度监控
- `hk-sector-rotation` - 板块轮动检测
- `hk-volatility-regime` - 波动率制度监控

### 2. 资金流向类 (Capital Flow)
- `hk-southbound-flow` - 南向资金分析
- `hk-foreign-flow` - 外资流向监控
- `hk-etf-flow` - ETF资金流向
- `hk-institutional-flow` - 机构资金流向

### 3. 公司基本面类 (Fundamentals)
- `hk-financial-statement` - 财务报表分析
- `hk-valuation-analyzer` - 估值分析器
- `hk-dividend-tracker` - 股息跟踪器
- `hk-buyback-monitor` - 回购监控器

### 4. 风险管理类 (Risk Management)
- `hk-liquidity-risk` - 流动性风险监控
- `hk-concentration-risk` - 集中度风险
- `hk-currency-risk` - 汇率风险监控
- `hk-regulatory-risk` - 监管风险评估

### 5. 交易策略类 (Trading Strategy)
- `hk-pairs-trading` - 配对交易
- `hk-arbitrage-opportunity` - 套利机会识别
- `hk-momentum-strategy` - 动量策略
- `hk-value-investing` - 价值投资策略

### 6. 事件驱动类 (Event Driven)
- `hk-earnings-reaction` - 业绩反应分析
- `hk-m-a-analyzer` - 并购分析器
- `hk-corporate-action` - 公司行动跟踪
- `hk-ipo-analysis` - IPO分析

## 🛠️ 数据工具

### HK Market Data Toolkit
- **实时行情数据**：港交所实时数据
- **财务数据**：年报、中报、季报
- **资金流向**：南向资金、外资流向
- **宏观经济**：香港经济指标
- **汇率数据**：港币汇率走势

## 📈 使用场景

### 投资研究
- 港股公司基本面分析
- 行业比较和板块轮动
- 估值和投资机会识别

### 风险管理
- 流动性风险评估
- 汇率风险对冲
- 集中度风险监控

### 交易执行
- 套利机会识别
- 配对交易策略
- 事件驱动交易

## 🌐 与其他市场的联动

### A股联动
- 南向资金流向分析
- A/H股溢价监控
- 跨市场套利机会

### 美股联动
- 中概股回归分析
- 跨市场估值比较
- 全球配置策略

## 📚 文档结构

每个技能包含：
- `SKILL.md` - 技能描述和使用指南
- `references/methodology.md` - 方法论文档
- `references/data-queries.md` - 数据查询说明
- `references/output-template.md` - 输出模板

## 🚀 快速开始

1. **安装依赖**
```bash
pip install -r requirements.txt
```

2. **配置数据源**
```bash
# 配置港交所数据API
# 配置汇率数据API
# 配置资金流向数据源
```

3. **运行技能**
```bash
# 运行市场概览
python hk-market-overview/scripts/main.py

# 运行资金流向分析
python hk-southbound-flow/scripts/main.py
```

## 📞 支持

- **文档**：查看各技能的详细说明
- **示例**：参考 `examples/` 目录
- **问题反馈**：提交Issue到项目仓库

---

*HK Market Skills - 专业的港股市场分析工具集*
