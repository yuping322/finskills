# 数据获取命令（共享脚本）

运行时约定：仅支持 Python 3.10–3.12，并使用仓库根目录统一虚拟环境 `.venv`。

从本技能目录运行。共享数据脚本位于 `../findata-toolkit-cn/`。（跟踪沪深港通持股（北向持仓排行、个股持仓明细、板块排行、机构统计）并输出增减持与集中度风险提示。当用户询问北向持仓、外资持股、陆股通持仓变化、或需要持仓监控时使用。）


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
| hsgt_dashboard | custom | composed view | 沪深港通/北向资金聚合：资金流、历史序列、持股排行、板块增持排行（工具聚合视图）。 | common: start_date, end_date | data keys: fund_flow_summary, hist, hold_stock_rank, board_rank, fund_min |
| stock_hsgt_fund_flow_summary_em | tool | tool view (1:1) | 东方财富网-数据中心-资金流向-沪深港通资金流向 | - | 交易日, 类型, 板块, 资金方向, 交易状态, 成交净买额, 资金净流入, 当日资金余额, 上涨数, 持平数 |
| stock_hsgt_hold_stock_em | tool | tool view (1:1) | 东方财富网-数据中心-沪深港通持股-个股排行 | required: market, indicator | 序号, 代码, 今日收盘价, 今日涨跌幅, 今日持股-股数, 今日持股-市值, 今日持股-占流通股比, 今日持股-占总股本比, 增持估计-股数, 增持估计-市值 |
#### `hsgt_dashboard` 底层工具（plan 展开）


| key | tool | 说明 | 入参（必填/常用） | 关键输出字段（示例） |
| --- | --- | --- | --- | --- |
| fund_flow_summary | stock_hsgt_fund_flow_summary_em | 东方财富网-数据中心-资金流向-沪深港通资金流向 | - | 交易日, 类型, 板块, 资金方向, 交易状态, 成交净买额, 资金净流入, 当日资金余额, 上涨数, 持平数 |
| hist | stock_hsgt_hist_em | 东方财富网-数据中心-资金流向-沪深港通资金流向-沪深港通历史数据 | required: symbol | (columns as-is) |
| hold_stock_rank | stock_hsgt_hold_stock_em | 东方财富网-数据中心-沪深港通持股-个股排行 | required: market, indicator | 序号, 代码, 今日收盘价, 今日涨跌幅, 今日持股-股数, 今日持股-市值, 今日持股-占流通股比, 今日持股-占总股本比, 增持估计-股数, 增持估计-市值 |
| board_rank | stock_hsgt_board_rank_em | 东方财富网-数据中心-沪深港通持股-板块排行 | required: symbol, indicator | 序号, 最新涨跌幅, 北向资金今日持股-股票只数, 北向资金今日持股-市值, 北向资金今日持股-占板块比, 北向资金今日持股-占北向资金比, 北向资金今日增持估计-股票只数, 北向资金今日增持估计-市值, 北向资金今日增持估计-市值增幅, 北向资金今日增持估计-占板块比 |
| fund_min | stock_hsgt_fund_min_em | 东方财富-数据中心-沪深港通-市场概括-分时数据 | required: symbol | (columns as-is) |


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
