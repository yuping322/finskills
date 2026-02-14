# 数据获取命令（共享脚本）

运行时约定：仅支持 Python 3.10–3.12，并使用仓库根目录统一虚拟环境 `.venv`。

从本技能目录运行。共享数据脚本位于 `../findata-toolkit-cn/`。（分析概念板块（同花顺/东方财富）的实时/历史表现、成分股、资金流与热度，用于识别主题热点与轮动。当用户询问概念板块走势、概念轮动、板块成分、概念资金流、或需要概念板块分析时使用。）


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
| concept_board_snapshot | custom | composed view | 概念板块快照：概念列表 + 实时行情（工具聚合视图）。 | - | data keys: concept_list, concept_spot |
| concept_board_detail | custom | composed view | 概念板块详情：成分股 + 历史行情（工具聚合视图）。 | required: symbol; common: start_date, end_date, period, adjust | data keys: constituents, history |
| stock_board_concept_name_em | tool | tool view (1:1) | 东方财富网-行情中心-沪深京板块-概念板块 | - | 排名, 板块代码, 最新价, 涨跌额, 涨跌幅, 总市值, 换手率, 上涨家数, 下跌家数, 领涨股票 |
| stock_board_concept_spot_em | tool | tool view (1:1) | 东方财富网-行情中心-沪深京板块-概念板块-实时行情 | - | item, value |
| stock_board_concept_cons_em | tool | tool view (1:1) | 东方财富-沪深板块-概念板块-板块成份 | - | 序号, 代码, 最新价, 涨跌幅, 涨跌额, 成交量, 成交额, 振幅, 最高, 最低 |
#### `concept_board_snapshot` 底层工具（plan 展开）


| key | tool | 说明 | 入参（必填/常用） | 关键输出字段（示例） |
| --- | --- | --- | --- | --- |
| concept_list | stock_board_concept_name_em | 东方财富网-行情中心-沪深京板块-概念板块 | - | 排名, 板块代码, 最新价, 涨跌额, 涨跌幅, 总市值, 换手率, 上涨家数, 下跌家数, 领涨股票 |
| concept_spot | stock_board_concept_spot_em | 东方财富网-行情中心-沪深京板块-概念板块-实时行情 | - | item, value |

#### `concept_board_detail` 底层工具（plan 展开）


| key | tool | 说明 | 入参（必填/常用） | 关键输出字段（示例） |
| --- | --- | --- | --- | --- |
| constituents | stock_board_concept_cons_em | 东方财富-沪深板块-概念板块-板块成份 | - | 序号, 代码, 最新价, 涨跌幅, 涨跌额, 成交量, 成交额, 振幅, 最高, 最低 |
| history | stock_board_concept_hist_em | 东方财富-沪深板块-概念板块-历史行情数据 | required: symbol, period, start_date, end_date, adjust | 日期, 开盘, 收盘, 最高, 最低, 涨跌幅, 涨跌额, 成交量, 成交额, 振幅 |


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
