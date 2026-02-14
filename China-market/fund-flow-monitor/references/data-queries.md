# 数据获取命令（共享脚本）

运行时约定：仅支持 Python 3.10–3.12，并使用仓库根目录统一虚拟环境 `.venv`。

从本技能目录运行。共享数据脚本位于 `../findata-toolkit-cn/`。（整合个股/行业/概念/大盘/主力/大单资金流向，识别资金驱动、背离与拥挤风险。当用户询问资金流向、主力净流入、行业/概念资金、资金异动或需要资金监控面板时使用。）


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
| fund_flow_dashboard | custom | composed view | 整合大盘/主力/板块资金流向与大单追踪（工具聚合视图）。 | - | data keys: market_fund_flow, main_fund_flow_rank, individual_fund_flow_rank, sector_fund_flow_rank, big_deal_tracker |
| stock_market_fund_flow | tool | tool view (1:1) | 东方财富网-数据中心-资金流向-大盘 | - | 日期, 上证-收盘价, 上证-涨跌幅, 深证-收盘价, 深证-涨跌幅, 主力净流入-净额, 主力净流入-净占比, 超大单净流入-净额, 超大单净流入-净占比, 大单净流入-净额 |
| stock_sector_fund_flow_rank | tool | tool view (1:1) | 东方财富网-数据中心-资金流向-板块资金流-排名 | required: indicator, sector_type | tool envelope: {meta,data,warnings,errors} |
| stock_fund_flow_big_deal | tool | tool view (1:1) | 同花顺-数据中心-资金流向-大单追踪 | - | tool envelope: {meta,data,warnings,errors} |
#### `fund_flow_dashboard` 底层工具（plan 展开）


| key | tool | 说明 | 入参（必填/常用） | 关键输出字段（示例） |
| --- | --- | --- | --- | --- |
| market_fund_flow | stock_market_fund_flow | 东方财富网-数据中心-资金流向-大盘 | - | 日期, 上证-收盘价, 上证-涨跌幅, 深证-收盘价, 深证-涨跌幅, 主力净流入-净额, 主力净流入-净占比, 超大单净流入-净额, 超大单净流入-净占比, 大单净流入-净额 |
| main_fund_flow_rank | stock_main_fund_flow | 东方财富网-数据中心-资金流向-主力净流入排名 | required: symbol | 序号, 代码, 最新价, 今日排行榜-主力净占比, 今日排行榜-今日排名, 今日排行榜-今日涨跌, 5日排行榜-主力净占比, 5日排行榜-5日排名, 5日排行榜-5日涨跌, 10日排行榜-主力净占比 |
| individual_fund_flow_rank | stock_individual_fund_flow_rank | 东方财富网-数据中心-资金流向-排名 | required: indicator | (columns as-is) |
| sector_fund_flow_rank | stock_sector_fund_flow_rank | 东方财富网-数据中心-资金流向-板块资金流-排名 | required: indicator, sector_type | (columns as-is) |
| big_deal_tracker | stock_fund_flow_big_deal | 同花顺-数据中心-资金流向-大单追踪 | - | (columns as-is) |


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
