# 数据获取命令（共享脚本）

运行时约定：仅支持 Python 3.10–3.12，并使用仓库根目录统一虚拟环境 `.venv`。

从本技能目录运行。共享数据脚本位于 `../findata-toolkit-cn/`。（跟踪 AB 股比价与 A+H 溢价/折价，并结合流动性与事件因素给出风险提示。当用户询问AB股比价、A+H溢价、跨市场定价差或需要溢价监控时使用。）


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
| ab_ah_premium_dashboard | custom | composed view | AB/AH 比价聚合：AB股比价与AH股实时行情（工具聚合视图）。 | - | data keys: ab_comparison, ah_spot_em, ah_spot, ah_name |
#### `ab_ah_premium_dashboard` 底层工具（plan 展开）


| key | tool | 说明 | 入参（必填/常用） | 关键输出字段（示例） |
| --- | --- | --- | --- | --- |
| ab_comparison | stock_zh_ab_comparison_em | 东方财富网-行情中心-沪深京个股-AB股比价-全部AB股比价 | - | 序号, B股代码, 最新价B, 涨跌幅B, A股代码, 最新价A, 涨跌幅A, 比价 |
| ah_spot_em | stock_zh_ah_spot_em | 东方财富网-行情中心-沪深港通-AH股比价-实时行情, 延迟 15 分钟更新 | - | 序号, H股代码, 最新价-HKD, H股-涨跌幅, A股代码, 最新价-RMB, A股-涨跌幅, 比价, 溢价 |
| ah_spot | stock_zh_ah_spot | A+H 股数据是从腾讯财经获取的数据, 延迟 15 分钟更新 | - | 代码, 最新价, 涨跌幅, 涨跌额, 买入, 卖出, 成交量, 成交额, 今开, 昨收 |
| ah_name | stock_zh_ah_name | A+H 股数据是从腾讯财经获取的数据, 历史数据按日频率更新 | - | 代码 |


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
