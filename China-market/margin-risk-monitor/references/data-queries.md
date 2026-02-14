# 数据获取命令（共享脚本）

运行时约定：仅支持 Python 3.10–3.12，并使用仓库根目录统一虚拟环境 `.venv`。

从本技能目录运行。共享数据脚本位于 `../findata-toolkit-cn/`。（监控融资融券与杠杆风险（余额变化、拥挤度、下跌加速风险），用于识别踩踏与波动放大。当用户询问两融数据、杠杆风险、市场拥挤、或需要两融监控时使用。）


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
| margin_dashboard | custom | composed view | 两融汇总视图：沪深两融汇总、明细与账户信息（工具聚合视图）。 | common: date, start_date, end_date | data keys: margin_ratio_pa, margin_account_info, margin_sse_summary, margin_sse_detail, margin_szse_summary, margin_szse_detail, margin_underlying_szse |
#### `margin_dashboard` 底层工具（plan 展开）


| key | tool | 说明 | 入参（必填/常用） | 关键输出字段（示例） |
| --- | --- | --- | --- | --- |
| margin_ratio_pa | stock_margin_ratio_pa | 融资融券-标的证券名单及保证金比例查询 | required: date | 证券代码, 证券简称, 融资比例, 融券比例 |
| margin_account_info | stock_margin_account_info | 东方财富网-数据中心-融资融券-融资融券账户统计-两融账户信息 | - | 日期, 融资余额, 融券余额, 融资买入额, 融券卖出额, 证券公司数量, 营业部数量, 个人投资者数量, 机构投资者数量, 参与交易的投资者数量 |
| margin_sse_summary | stock_margin_sse | 上海证券交易所-融资融券数据-融资融券汇总数据 | required: start_date, end_date | 信用交易日期, 融资余额, 融资买入额, 融券余量, 融券余量金额, 融券卖出量, 融资融券余额 |
| margin_sse_detail | stock_margin_detail_sse | 上海证券交易所-融资融券数据-融资融券明细数据 | required: date | 信用交易日期, 标的证券代码, 标的证券简称, 融资余额, 融资买入额, 融资偿还额, 融券余量, 融券卖出量, 融券偿还量 |
| margin_szse_summary | stock_margin_szse | 深圳证券交易所-融资融券数据-融资融券汇总数据 | required: date | 融资买入额, 融资余额, 融券卖出量, 融券余量, 融券余额, 融资融券余额 |
| margin_szse_detail | stock_margin_detail_szse | 深证证券交易所-融资融券数据-融资融券交易明细数据 | required: date | 证券代码, 证券简称, 融资买入额, 融资余额, 融券卖出量, 融券余量, 融券余额, 融资融券余额 |
| margin_underlying_szse | stock_margin_underlying_info_szse | 深圳证券交易所-融资融券数据-标的证券信息 | required: date | 证券代码, 证券简称, 融资标的, 融券标的, 当日可融资, 当日可融券, 融券卖出价格限制, 涨跌幅限制 |


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
