# 数据获取命令（共享脚本）

运行时约定：仅支持 Python 3.10–3.12，并使用仓库根目录统一虚拟环境 `.venv`。

从本技能目录运行。共享数据脚本位于 `../findata-toolkit-cn/`。（分析A股高股息策略，评估红利股的收益可持续性与长期回报。当用户询问高股息股票、红利策略、A股分红分析、现金分红覆盖率、中证红利指数成分股、股息率排名或长期收入型投资时使用此技能。）


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
| dividend_actions_dashboard | custom | composed view | 分红/配股聚合：分红配送、交易提醒、个股历史分红与配股方案（工具聚合视图）。 | common: symbol | data keys: fhps_by_period, trade_notify_dividend |
| stock_history_dividend | tool | tool view (1:1) | 新浪财经-发行与分配-历史分红 | - | 代码, 上市日期, 累计股息, 年均股息, 分红次数, 融资总额, 融资次数 |
| stock_history_dividend_detail | tool | tool view (1:1) | 新浪财经-发行与分配-分红配股 | required: symbol, indicator, date | tool envelope: {meta,data,warnings,errors} |
| stock_dividend_cninfo | tool | tool view (1:1) | 巨潮资讯-个股-历史分红 | required: symbol | 实施方案公告日期, 送股比例, 转增比例, 派息比例, 股权登记日, 除权日, 派息日, 股份到账日, 实施方案分红说明, 分红类型 |
#### `dividend_actions_dashboard` 底层工具（plan 展开）


| key | tool | 说明 | 入参（必填/常用） | 关键输出字段（示例） |
| --- | --- | --- | --- | --- |
| fhps_by_period | stock_fhps_em | 东方财富-数据中心-年报季报-分红配送 | required: date | 代码, 送转股份-送转总比例, 送转股份-送转比例, 送转股份-转股比例, 现金分红-现金分红比例, 现金分红-股息率, 每股收益, 每股净资产, 每股公积金, 每股未分配利润 |
| trade_notify_dividend | news_trade_notify_dividend_baidu | 百度股市通-交易提醒-分红派息 | required: date | 股票代码, 除权日, 分红, 送股, 转增, 实物, 交易所, 股票简称, 报告期 |


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
