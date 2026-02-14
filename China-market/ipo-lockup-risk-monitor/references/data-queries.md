# 数据获取命令（共享脚本）

运行时约定：仅支持 Python 3.10–3.12，并使用仓库根目录统一虚拟环境 `.venv`。

从本技能目录运行。共享数据脚本位于 `../findata-toolkit-cn/`。（监控限售解禁、重要股东减持与供给冲击风险，输出时间表与风险提示。当用户询问解禁/减持、供给冲击、或需要解禁风险清单时使用。）


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
| restricted_release_dashboard | custom | composed view | 限售解禁聚合：解禁汇总/明细/个股解禁队列与股东信息（工具聚合视图）。 | common: symbol, start_date, end_date | data keys: release_summary, release_detail |
| stock_restricted_release_summary_em | tool | tool view (1:1) | 东方财富网-数据中心-特色数据-限售股解禁 | required: symbol, start_date, end_date | 序号, 解禁时间, 当日解禁股票家数, 解禁数量, 实际解禁数量, 实际解禁市值, 沪深300指数, 沪深300指数涨跌幅 |
| stock_restricted_release_detail_em | tool | tool view (1:1) | 东方财富网-数据中心-限售股解禁-解禁详情一览 | required: start_date, end_date | 序号, 股票代码, 股票简称, 解禁时间, 限售股类型, 解禁数量, 实际解禁数量, 实际解禁市值, 占解禁前流通市值比例, 解禁前一交易日收盘价 |
| stock_restricted_release_stockholder_em | tool | tool view (1:1) | 东方财富网-数据中心-个股限售解禁-解禁股东 | required: symbol, date | 序号, 解禁数量, 实际解禁数量, 解禁市值, 锁定期, 剩余未解禁数量, 限售股类型, 进度 |
#### `restricted_release_dashboard` 底层工具（plan 展开）


| key | tool | 说明 | 入参（必填/常用） | 关键输出字段（示例） |
| --- | --- | --- | --- | --- |
| release_summary | stock_restricted_release_summary_em | 东方财富网-数据中心-特色数据-限售股解禁 | required: symbol, start_date, end_date | 序号, 解禁时间, 当日解禁股票家数, 解禁数量, 实际解禁数量, 实际解禁市值, 沪深300指数, 沪深300指数涨跌幅 |
| release_detail | stock_restricted_release_detail_em | 东方财富网-数据中心-限售股解禁-解禁详情一览 | required: start_date, end_date | 序号, 股票代码, 股票简称, 解禁时间, 限售股类型, 解禁数量, 实际解禁数量, 实际解禁市值, 占解禁前流通市值比例, 解禁前一交易日收盘价 |


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
