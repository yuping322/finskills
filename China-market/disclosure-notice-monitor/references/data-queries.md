# 数据获取命令（共享脚本）

运行时约定：仅支持 Python 3.10–3.12，并使用仓库根目录统一虚拟环境 `.venv`。

从本技能目录运行。共享数据脚本位于 `../findata-toolkit-cn/`。（梳理公司公告与信息披露（定期报告披露、重大事项）并生成事件清单、影响评估与监控要点。当用户询问公告梳理、信息披露、财报披露时间、重大事项清单或需要公告监控时使用。）


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
| notice_daily_dashboard | custom | composed view | 公告类别-按日汇总（stock_notice_report；工具聚合视图）。 | common: date | data keys: notice_report |
| cninfo_disclosure_search | custom | composed view | 巨潮资讯信息披露公告查询（按股票/类别/关键词/时间窗；工具聚合视图）。 | required: symbol, category; common: start_date, end_date | data keys: disclosure_reports |
| cninfo_disclosure_relation_search | custom | composed view | 巨潮资讯信息披露调研查询（工具聚合视图）。 | required: symbol; common: start_date, end_date | data keys: disclosure_relations |
| report_disclosure_calendar | custom | composed view | 定期报告披露日历（交易所口径汇总；工具聚合视图）。 | common: period | data keys: report_disclosure |
#### `notice_daily_dashboard` 底层工具（plan 展开）


| key | tool | 说明 | 入参（必填/常用） | 关键输出字段（示例） |
| --- | --- | --- | --- | --- |
| notice_report | stock_notice_report | 东方财富网-数据中心-公告大全-沪深京 A 股公告 | required: symbol, date | 代码, 公告标题, 公告类型, 公告日期, 网址 |

#### `cninfo_disclosure_search` 底层工具（plan 展开）


| key | tool | 说明 | 入参（必填/常用） | 关键输出字段（示例） |
| --- | --- | --- | --- | --- |
| disclosure_reports | stock_zh_a_disclosure_report_cninfo | 巨潮资讯-首页-公告查询-信息披露公告-沪深京 | required: symbol, market, keyword, category, start_date, end_date | 代码, 简称, 公告标题, 公告时间, 公告链接 |

#### `cninfo_disclosure_relation_search` 底层工具（plan 展开）


| key | tool | 说明 | 入参（必填/常用） | 关键输出字段（示例） |
| --- | --- | --- | --- | --- |
| disclosure_relations | stock_zh_a_disclosure_relation_cninfo | 巨潮资讯-首页-公告查询-信息披露调研-沪深京 | required: symbol, market, start_date, end_date | 代码, 简称, 公告标题, 公告时间, 公告链接 |

#### `report_disclosure_calendar` 底层工具（plan 展开）


| key | tool | 说明 | 入参（必填/常用） | 关键输出字段（示例） |
| --- | --- | --- | --- | --- |
| report_disclosure | stock_report_disclosure | 巨潮资讯-数据-预约披露的数据 | required: market, period | 股票代码, 股票简称, 首次预约, 初次变更, 二次变更, 三次变更, 实际披露 |


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
