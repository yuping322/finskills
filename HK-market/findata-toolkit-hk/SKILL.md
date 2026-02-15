---
name: findata-toolkit-hk
description: 港股金融数据工具包。提供脚本获取港股实时行情、财务数据、南向资金、汇率数据、宏观经济指标。用于需要实时港股市场数据支撑投资分析时。所有数据源免费，无需API密钥。
license: Apache-2.0
---

# 金融数据工具包 — 港股市场

自包含的数据工具包，提供港股市场实时金融数据和定量计算。所有数据源**免费**，**无需API密钥**。

## 安装

安装依赖（一次性）：

```bash
pip install -r requirements.txt
```

## 可用工具

所有脚本位于 `scripts/` 目录。从技能根目录运行。

### 1. 港股行情数据 (`scripts/hk_stock_data.py`)

获取港股实时行情、历史数据和基本信息。

| 命令 | 用途 |
|------|------|
| `python scripts/hk_stock_data.py 00700` | 腾讯控股基本信息 |
| `python scripts/hk_stock_data.py 00700 --price` | 实时价格和历史数据 |
| `python scripts/hk_stock_data.py 00700 --financial` | 财务指标和估值数据 |
| `python scripts/hk_stock_data.py 00700 --dividend` | 股息历史和分红信息 |

### 2. 南向资金数据 (`scripts/southbound_flow.py`)

获取南向资金流向和持仓数据。

| 命令 | 用途 |
|------|------|
| `python scripts/southbound_flow.py --daily` | 每日南向资金流向 |
| `python scripts/southbound_flow.py --holdings` | 南向资金持仓明细 |
| `python scripts/southbound_flow.py --sector` | 行业资金流向分析 |
| `python scripts/southbound_flow.py --top` | 净买入/卖出TOP榜 |

### 3. 港股财务数据 (`scripts/hk_financials.py`)

获取港股财务报表和财务指标。

| 命令 | 用途 |
|------|------|
| `python scripts/hk_financials.py 00700 --income` | 损益表数据 |
| `python scripts/hk_financials.py 00700 --balance` | 资产负债表 |
| `python scripts/hk_financials.py 00700 --cashflow` | 现金流量表 |
| `python scripts/hk_financials.py 00700 --ratios` | 财务比率分析 |

### 4. 汇率数据 (`scripts/fx_data.py`)

获取港币汇率和相关数据。

| 命令 | 用途 |
|------|------|
| `python scripts/fx_data.py HKD --spot` | 港币即期汇率 |
| `python scripts/fx_data.py HKD --forward` | 远期汇率 |
| `python scripts/fx_data.py HKD --history` | 历史汇率走势 |
| `python scripts/fx_data.py HKD --volatility` | 汇率波动率 |

### 5. 港股宏观数据 (`scripts/hk_macro.py`)

获取香港宏观经济指标。

| 命令 | 用途 |
|------|------|
| `python scripts/hk_macro.py --gdp` | GDP数据 |
| `python scripts/hk_macro.py --cpi` | CPI通胀数据 |
| `python scripts/hk_macro.py --unemployment` | 失业率数据 |
| `python scripts/hk_macro.py --interest` | 利率数据 |

### 6. 港股ETF数据 (`scripts/hk_etf.py`)

获取港股ETF相关数据。

| 命令 | 用途 |
|------|------|
| `python scripts/hk_etf.py --list` | ETF列表和基本信息 |
| `python scripts/hk_etf.py 02800 --holdings` | ETF持仓明细 |
| `python scripts/hk_etf.py 02800 --flow` | ETF资金流向 |
| `python scripts/hk_etf.py --performance` | ETF表现分析 |

## 数据源说明

### 主要数据源
- **港交所数据**：实时行情、历史数据
- **港交所披露易**：公司公告、财务报表
- **香港金管局**：汇率、利率数据
- **香港政府统计处**：宏观经济数据
- **各大券商**：南向资金数据

### 数据更新频率
- **实时数据**：交易时间内实时更新
- **财务数据**：季度更新（季报）、半年度更新（中报）、年度更新（年报）
- **宏观数据**：月度、季度、年度更新
- **资金流向**：每日更新

## 输出格式

### 标准输出格式
```json
{
  "symbol": "00700.HK",
  "name": "腾讯控股",
  "price": {
    "current": 320.5,
    "change": 5.2,
    "change_pct": 1.65
  },
  "market_cap": 3072000000000,
  "pe_ratio": 18.5,
  "dividend_yield": 0.85,
  "timestamp": "2026-02-15 16:00:00"
}
```

### 财务数据格式
```json
{
  "symbol": "00700.HK",
  "financials": {
    "revenue": 560118000000,
    "net_profit": 115219000000,
    "eps": 12.0,
    "roe": 0.156,
    "debt_ratio": 0.234
  },
  "period": "2024Q3",
  "currency": "HKD"
}
```

## 错误处理

### 常见错误
- **网络连接问题**：检查网络连接
- **数据源限制**：部分数据可能有访问限制
- **股票代码错误**：确保使用正确的港股代码格式
- **时间限制**：避免过于频繁的数据请求

### 错误信息示例
```json
{
  "error": "Invalid stock code",
  "message": "Stock code 99999.HK not found",
  "suggestion": "Please check the stock code format"
}
```

## 使用示例

### 基础使用
```python
from scripts.hk_stock_data import get_stock_info

# 获取腾讯控股信息
info = get_stock_info("00700")
print(f"当前价格: {info['price']['current']} HKD")
print(f"市值: {info['market_cap']:,} HKD")
```

### 批量查询
```python
from scripts.southbound_flow import get_daily_flow

# 获取最近5天南向资金流向
for i in range(5):
    flow_data = get_daily_flow(days_back=i)
    print(f"第{i+1}天净流入: {flow_data['net_flow']:,} HKD")
```

## 配置说明

### 环境变量
```bash
# 可选：设置代理（如果需要）
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080

# 可选：设置缓存目录
export HK_DATA_CACHE=/path/to/cache
```

### 配置文件
```json
{
  "data_sources": {
    "hkex": {
      "base_url": "https://www.hkex.com.hk",
      "timeout": 30
    },
    "cache": {
      "enabled": true,
      "ttl": 300
    }
  }
}
```

## 注意事项

1. **数据延迟**：实时数据可能有轻微延迟
2. **交易时间**：港股交易时间为9:30-12:00, 13:00-16:00
3. **货币单位**：所有价格数据以港币(HKD)为单位
4. **股票代码**：使用5位数字代码，如00700表示腾讯控股
5. **数据准确性**：建议交叉验证重要数据

## 更新日志

### v1.0.0 (2026-02-15)
- 初始版本发布
- 支持基础港股数据获取
- 南向资金流向分析
- 财务数据查询功能

---

*HK Market Data Toolkit - 专业的港股数据获取工具*
