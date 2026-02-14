# 数据获取命令（共享脚本）

运行时约定：仅支持 Python 3.10–3.12，并使用仓库根目录统一虚拟环境 `.venv`。

从本技能目录运行。共享数据脚本位于 `../findata-toolkit-cn/`。（分析行业板块（行业指数、成分股、资金流排名、历史表现）用于行业强弱与轮动判断。当用户询问行业板块表现、行业轮动、行业资金流、行业成分、或需要行业板块对比时使用。）


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
| industry_board_snapshot | custom | composed view | 行业板块快照：行业一览表/行业代码列表（工具聚合视图）。 | - | data keys: industry_summary_ths, industry_name_em, sector_fund_flow_rank |
| industry_board_detail | custom | composed view | 行业板块详情：实时行情/成分股/历史行情（工具聚合视图）。 | required: symbol; common: start_date, end_date, period, adjust | data keys: spot, constituents, history |
| stock_board_industry_name_em | tool | tool view (1:1) | 东方财富-沪深京板块-行业板块 | - | 排名, 板块代码, 最新价, 涨跌额, 涨跌幅, 总市值, 换手率, 上涨家数, 下跌家数, 领涨股票 |
| stock_board_industry_spot_em | tool | tool view (1:1) | 东方财富网-沪深板块-行业板块-实时行情 | required: symbol | item, value |
| stock_board_industry_index_ths | tool | tool view (1:1) | 同花顺-板块-行业板块-指数日频率数据 | required: start_date, end_date | 日期, 开盘价, 最高价, 最低价, 收盘价, 成交量, 成交额 |
| stock_fund_flow_industry | tool | tool view (1:1) | 同花顺-数据中心-资金流向-行业资金流 | required: symbol | tool envelope: {meta,data,warnings,errors} |
#### `industry_board_snapshot` 底层工具（plan 展开）


| key | tool | 说明 | 入参（必填/常用） | 关键输出字段（示例） |
| --- | --- | --- | --- | --- |
| industry_summary_ths | stock_board_industry_summary_ths | 同花顺-同花顺行业一览表 | - | 序号, 板块, 涨跌幅, 总成交量, 总成交额, 净流入, 上涨家数, 下跌家数, 均价, 领涨股 |
| industry_name_em | stock_board_industry_name_em | 东方财富-沪深京板块-行业板块 | - | 排名, 板块代码, 最新价, 涨跌额, 涨跌幅, 总市值, 换手率, 上涨家数, 下跌家数, 领涨股票 |
| sector_fund_flow_rank | stock_sector_fund_flow_rank | 东方财富网-数据中心-资金流向-板块资金流-排名 | required: indicator, sector_type | (columns as-is) |

#### `industry_board_detail` 底层工具（plan 展开）


| key | tool | 说明 | 入参（必填/常用） | 关键输出字段（示例） |
| --- | --- | --- | --- | --- |
| spot | stock_board_industry_spot_em | 东方财富网-沪深板块-行业板块-实时行情 | required: symbol | item, value |
| constituents | stock_board_industry_cons_em | 东方财富-沪深板块-行业板块-板块成份 | required: symbol | 序号, 代码, 最新价, 涨跌幅, 涨跌额, 成交量, 成交额, 振幅, 最高, 最低 |
| history | stock_board_industry_hist_em | 东方财富-沪深板块-行业板块-历史行情数据 | required: symbol, start_date, end_date, period, adjust | 日期, 开盘, 收盘, 最高, 最低, 涨跌幅, 涨跌额, 成交量, 成交额, 振幅 |


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
