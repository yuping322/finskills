# 数据获取命令（共享脚本）

运行时约定：仅支持 Python 3.10–3.12，并使用仓库根目录统一虚拟环境 `.venv`。

从本技能目录运行。共享数据脚本位于 `../findata-toolkit-cn/`。（分析龙虎榜数据（机构席位、营业部、买卖动向、个股上榜统计）以识别资金偏好与异常成交风险。当用户询问龙虎榜、机构席位动向、游资营业部、上榜原因、或需要龙虎榜复盘时使用。）


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
| dragon_tiger_daily | custom | composed view | 龙虎榜日度聚合：上榜明细 + 机构买卖统计 + 活跃营业部（工具聚合视图）。 | common: date | data keys: lhb_detail_daily_sina, lhb_detail_em, lhb_institution_buy_sell_stat, lhb_active_yyb |
| dragon_tiger_stock_detail | custom | composed view | 个股龙虎榜详情：按日期与上榜类型查询（工具聚合视图）。 | required: symbol, flag; common: date | data keys: lhb_stock_detail, lhb_stock_statistic |
#### `dragon_tiger_daily` 底层工具（plan 展开）


| key | tool | 说明 | 入参（必填/常用） | 关键输出字段（示例） |
| --- | --- | --- | --- | --- |
| lhb_detail_daily_sina | stock_lhb_detail_daily_sina | 新浪财经-龙虎榜-每日详情 | required: date | 序号, 股票代码, 收盘价, 对应值, 成交量, 成交额, 指标 |
| lhb_detail_em | stock_lhb_detail_em | 东方财富网-数据中心-龙虎榜单-龙虎榜详情 | required: start_date, end_date | 序号, 代码, 上榜日, 解读, 收盘价, 涨跌幅, 龙虎榜净买额, 龙虎榜买入额, 龙虎榜卖出额, 龙虎榜成交额 |
| lhb_institution_buy_sell_stat | stock_lhb_jgmmtj_em | 东方财富网-数据中心-龙虎榜单-机构买卖每日统计 | required: start_date, end_date | 序号, 代码, 收盘价, 涨跌幅, 买方机构数, 卖方机构数, 机构买入总额, 机构卖出总额, 机构买入净额, 市场总成交额 |
| lhb_active_yyb | stock_lhb_hyyyb_em | 东方财富网-数据中心-龙虎榜单-每日活跃营业部 | required: start_date, end_date | 序号, 上榜日, 买入个股数, 卖出个股数, 买入总金额, 卖出总金额, 总买卖净额, 买入股票 |

#### `dragon_tiger_stock_detail` 底层工具（plan 展开）


| key | tool | 说明 | 入参（必填/常用） | 关键输出字段（示例） |
| --- | --- | --- | --- | --- |
| lhb_stock_detail | stock_lhb_stock_detail_em | 东方财富网-数据中心-龙虎榜单-个股龙虎榜详情 | required: symbol, date, flag | 序号, 买入金额, 买入金额-占总成交比例, 卖出金额-占总成交比例, 净额, 类型 |
| lhb_stock_statistic | stock_lhb_stock_statistic_em | 东方财富网-数据中心-龙虎榜单-个股上榜统计 | required: symbol | 序号, 代码, 最近上榜日, 收盘价, 涨跌幅, 上榜次数, 龙虎榜净买额, 龙虎榜买入额, 龙虎榜卖出额, 龙虎榜总成交额 |


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
