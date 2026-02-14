# 数据获取命令（共享脚本）

运行时约定：仅支持 Python 3.10–3.12，并使用仓库根目录统一虚拟环境 `.venv`。

从本技能目录运行。共享数据脚本位于 `../findata-toolkit-cn/`。（跟踪并解读A股大宗交易（折溢价、买卖方、金额、连续性），用于识别潜在建仓/派发、短期抛压与承接强弱，并输出可执行的跟踪清单与风控规则。当用户询问大宗交易、折价率、大额成交、机构接盘、或想用大宗交易做信号时使用。）


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
| block_deal_dashboard | custom | composed view | 大宗交易聚合视图：市场统计、区间每日统计/明细、活跃个股与活跃营业部（工具聚合视图）。 | common: start_date, end_date | data keys: market_stats, daily_stats, daily_detail, active_stocks, active_brokers, broker_ranking |
#### `block_deal_dashboard` 底层工具（plan 展开）


| key | tool | 说明 | 入参（必填/常用） | 关键输出字段（示例） |
| --- | --- | --- | --- | --- |
| market_stats | stock_dzjy_sctj | 东方财富网-数据中心-大宗交易-市场统计 | - | 序号, 交易日期, 上证指数, 上证指数涨跌幅, 大宗交易成交总额, 溢价成交总额, 溢价成交总额占比, 折价成交总额, 折价成交总额占比 |
| daily_stats | stock_dzjy_mrtj | 东方财富网-数据中心-大宗交易-每日统计 | required: start_date, end_date | 序号, 交易日期, 证券代码, 证券简称, 涨跌幅, 收盘价, 成交均价, 折溢率, 成交笔数, 成交总量 |
| daily_detail | stock_dzjy_mrmx | 东方财富网-数据中心-大宗交易-每日明细 | required: symbol, start_date, end_date | (columns as-is) |
| active_stocks | stock_dzjy_hygtj | 东方财富网-数据中心-大宗交易-活跃 A 股统计 | required: symbol | 序号, 证券代码, 证券简称, 最新价, 涨跌幅, 最近上榜日, 上榜次数-总计, 上榜次数-溢价, 上榜次数-折价, 总成交额 |
| active_brokers | stock_dzjy_hyyybtj | 东方财富网-数据中心-大宗交易-活跃营业部统计 | required: symbol | 序号, 最近上榜日, 次数总计-买入, 次数总计-卖出, 成交金额统计-买入, 成交金额统计-卖出, 成交金额统计-净买入额, 买入的股票 |
| broker_ranking | stock_dzjy_yybph | 东方财富网-数据中心-大宗交易-营业部排行 | required: symbol | 序号, 上榜后1天-买入次数, 上榜后1天-平均涨幅, 上榜后1天-上涨概率, 上榜后5天-买入次数, 上榜后5天-平均涨幅, 上榜后5天-上涨概率, 上榜后10天-买入次数, 上榜后10天-平均涨幅, 上榜后10天-上涨概率 |


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
