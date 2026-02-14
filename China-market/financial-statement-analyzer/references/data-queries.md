# 数据获取命令（共享脚本）

运行时约定：仅支持 Python 3.10–3.12，并使用仓库根目录统一虚拟环境 `.venv`。

从本技能目录运行。共享数据脚本位于 `../findata-toolkit-cn/`。（对单个A股上市公司的财务报表进行深度分析，评估盈利质量、财务健康状况、财务造假风险和运营效率。当用户要求深入分析某家公司的财务报表、杜邦分析、盈利质量检查、资产负债表分析、现金流分析、Z值评分、M值评分、营运资本分析，或任何详细的单公司财务审视时使用此技能。）


## 一次性环境准备

```bash
# 激活仓库根目录虚拟环境（统一 .venv）
source ../../.venv/bin/activate

# 安装 A股工具包依赖
python -m pip install -r ../findata-toolkit-cn/requirements.txt
```

## 本技能依赖的数据（views / tools）

口径约定：

- `views_runner.py` 输出统一为 JSON：`{meta, data, warnings, errors}`。
- tool view 的 `data` 字段保持底层实现的原始字段名/单位（不做二次清洗）。
- 自定义 view 的 `data` 是多个 tool view 调用结果的聚合字典（每个 value 仍是 tool envelope）。

### Views（建议）

| view 名称 | 类型 | 定位 | 用途 | 入参（必填/常用） | 产出/口径 |
| --- | --- | --- | --- | --- | --- |
| stock_financial_abstract_ths | tool | tool view (1:1) | 同花顺-财务指标-主要指标 | required: symbol, indicator | 报告期, 净利润, 净利润同比增长率, 扣非净利润, 扣非净利润同比增长率, 营业总收入, 营业总收入同比增长率, 基本每股收益, 每股净资产, 每股资本公积金 |
| stock_financial_analysis_indicator | tool | tool view (1:1) | 新浪财经-财务分析-财务指标 | required: symbol, start_year | 日期, 摊薄每股收益(元), 加权每股收益(元), 每股收益_调整后(元), 扣除非经常性损益后的每股收益(元), 每股净资产_调整前(元), 每股净资产_调整后(元), 每股经营性现金流(元), 每股资本公积金(元), 每股未分配利润(元) |
| stock_balance_sheet_by_report_em | tool | tool view (1:1) | 东方财富-股票-财务分析-资产负债表-按报告期 | required: symbol | - |
| stock_profit_sheet_by_report_em | tool | tool view (1:1) | 东方财富-股票-财务分析-利润表-报告期 | required: symbol | - |
| stock_cash_flow_sheet_by_report_em | tool | tool view (1:1) | 东方财富-股票-财务分析-现金流量表-按报告期 | required: symbol | - |

## 常用命令

```bash
# 确保已激活虚拟环境（统一 .venv）
source ../../.venv/bin/activate

# 发现可用 view（包含 tool views 与组合 views）
python ../findata-toolkit-cn/scripts/views_runner.py list --contains <keyword>

# 查看 view 的入参 schema
python ../findata-toolkit-cn/scripts/views_runner.py describe <view_or_tool_name>

# 只生成调用计划（不执行真实抓取；便于写分析/复现）
python ../findata-toolkit-cn/scripts/views_runner.py <view_or_tool_name> --dry-run --set key=value

# 示例：A股实时行情 / 历史K线
python ../findata-toolkit-cn/scripts/views_runner.py stock_zh_a_spot_em
python ../findata-toolkit-cn/scripts/views_runner.py stock_zh_a_hist --set symbol=000001 --set period=daily --set start_date=20250101 --set end_date=20250201 --set adjust=qfq
```

## 可选

- 缓存目录：`FINSKILLS_CACHE_DIR=/tmp/finskills-cache`
- 若某些接口需要雪球 token：设置 `XUEQIU_TOKEN` 环境变量（当工具入参包含 `token` 时）
