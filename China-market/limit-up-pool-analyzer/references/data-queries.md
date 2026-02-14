# 数据获取命令（共享脚本）

运行时约定：仅支持 Python 3.10–3.12，并使用仓库根目录统一虚拟环境 `.venv`。

从本技能目录运行。共享数据脚本位于 `../findata-toolkit-cn/`。（分析涨停池/强势股/连板结构/次新等，提炼市场情绪、题材强弱与风险提示。当用户询问涨停池、连板、强势股、打板情绪、题材热度或需要涨停池复盘时使用。）


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
| limit_up_pool_daily | custom | composed view | 涨停池/强势股池聚合：涨停股池、昨日涨停、强势股、次新、炸板、跌停等（工具聚合视图）。 | common: date | data keys: zt_pool, zt_pool_previous, zt_pool_strong, zt_pool_sub_new, zt_pool_zbgc, zt_pool_dtgc |
#### `limit_up_pool_daily` 底层工具（plan 展开）


| key | tool | 说明 | 入参（必填/常用） | 关键输出字段（示例） |
| --- | --- | --- | --- | --- |
| zt_pool | stock_zt_pool_em | 东方财富网-行情中心-涨停板行情-涨停股池 | required: date | 序号, 代码, 涨跌幅, 最新价, 成交额, 流通市值, 总市值, 换手率, 封板资金, 首次封板时间 |
| zt_pool_previous | stock_zt_pool_previous_em | 东方财富网-行情中心-涨停板行情-昨日涨停股池 | required: date | 序号, 代码, 涨跌幅, 最新价, 涨停价, 成交额, 流通市值, 总市值, 换手率, 涨速 |
| zt_pool_strong | stock_zt_pool_strong_em | 东方财富网-行情中心-涨停板行情-强势股池 | required: date | 序号, 代码, 涨跌幅, 最新价, 涨停价, 成交额, 流通市值, 总市值, 换手率, 涨速 |
| zt_pool_sub_new | stock_zt_pool_sub_new_em | 东方财富网-行情中心-涨停板行情-次新股池 | required: date | 序号, 代码, 涨跌幅, 最新价, 涨停价, 成交额, 流通市值, 总市值, 转手率, 开板几日 |
| zt_pool_zbgc | stock_zt_pool_zbgc_em | 东方财富网-行情中心-涨停板行情-炸板股池 | required: date | 序号, 代码, 涨跌幅, 最新价, 涨停价, 成交额, 流通市值, 总市值, 换手率, 涨速 |
| zt_pool_dtgc | stock_zt_pool_dtgc_em | 东方财富网-行情中心-涨停板行情-跌停股池 | required: date | 序号, 代码, 涨跌幅, 最新价, 成交额, 流通市值, 总市值, 动态市盈率, 换手率, 封单资金 |


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
