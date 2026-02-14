# 数据获取命令（共享脚本）

运行时约定：仅支持 Python 3.10–3.12，并使用仓库根目录统一虚拟环境 `.venv`。

从本技能目录运行。共享数据脚本位于 `../findata-toolkit-cn/`。（跟踪股东户数、十大股东/流通股东、机构/基金持股与持仓变化，输出筹码结构与供给冲击风险提示。当用户询问股东户数、股东结构、机构/基金持股、持仓变化或需要筹码分析时使用。）


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
| shareholder_structure_dashboard | custom | composed view | 股东结构/筹码聚合：股东户数、主要股东、流通股东、持股变动与监管披露（工具聚合视图）。 | required: symbol | data keys: gdhs_quarter_list, gdhs_detail, main_stock_holder, circulate_stock_holder, shareholder_change_ths, share_hold_change_sse, share_hold_change_szse, share_hold_change_bse, hold_num_cninfo, hold_change_cninfo |
#### `shareholder_structure_dashboard` 底层工具（plan 展开）


| key | tool | 说明 | 入参（必填/常用） | 关键输出字段（示例） |
| --- | --- | --- | --- | --- |
| gdhs_quarter_list | stock_zh_a_gdhs | 东方财富网-数据中心-特色数据-股东户数数据 | required: symbol | 代码, 最新价, 涨跌幅, 股东户数-本次, 股东户数-上次, 股东户数-增减, 股东户数-增减比例, 区间涨跌幅, 股东户数统计截止日-本次, 股东户数统计截止日-上次 |
| gdhs_detail | stock_zh_a_gdhs_detail_em | 东方财富网-数据中心-特色数据-股东户数详情 | required: symbol | 股东户数统计截止日, 区间涨跌幅, 股东户数-本次, 股东户数-上次, 股东户数-增减, 股东户数-增减比例, 户均持股市值, 户均持股数量, 总市值, 总股本 |
| main_stock_holder | stock_main_stock_holder | 新浪财经-股本股东-主要股东 | required: stock | 编号, 持股数量, 持股比例, 股本性质, 截至日期, 公告日期, 股东说明, 股东总数, 平均持股数 |
| circulate_stock_holder | stock_circulate_stock_holder | 新浪财经-股东股本-流通股东 | required: symbol | 截止日期, 公告日期, 编号, 持股数量, 占流通股比例, 股本性质 |
| shareholder_change_ths | stock_shareholder_change_ths | 同花顺-公司大事-股东持股变动 | required: symbol | 公告日期, 变动股东, 变动数量, 交易均价, 剩余股份总数, 变动期间, 变动途径 |
| share_hold_change_sse | stock_share_hold_change_sse | 上海证券交易所-披露-监管信息公开-公司监管-董董监高人员股份变动 | required: symbol | 公司代码, 姓名, 职务, 股票种类, 货币种类, 本次变动前持股数, 变动数, 本次变动平均价格, 变动后持股数, 变动原因 |
| share_hold_change_szse | stock_share_hold_change_szse | 深圳证券交易所-信息披露-监管信息公开-董监高人员股份变动 | required: symbol | 证券代码, 证券简称, 董监高姓名, 变动日期, 变动股份数量, 成交均价, 变动原因, 变动比例, 当日结存股数, 股份变动人姓名 |
| share_hold_change_bse | stock_share_hold_change_bse | 北京证券交易所-信息披露-监管信息-董监高及相关人员持股变动 | required: symbol | 代码, 简称, 姓名, 职务, 变动日期, 变动股数, 变动前持股数, 变动后持股数, 变动均价, 变动原因 |
| hold_num_cninfo | stock_hold_num_cninfo | 巨潮资讯-数据中心-专题统计-股东股本-股东人数及持股集中度 | required: date | 证劵代码, 证券简称, 变动日期, 本期股东人数, 上期股东人数, 股东人数增幅, 本期人均持股数量, 上期人均持股数量, 人均持股数量增幅 |
| hold_change_cninfo | stock_hold_change_cninfo | 巨潮资讯-数据中心-专题统计-股东股本-股本变动 | required: symbol | 证券代码, 证券简称, 交易市场, 公告日期, 变动日期, 变动原因, 总股本, 已流通股份, 已流通比例, 流通受限股份 |
| hold_control_cninfo | stock_hold_control_cninfo | 巨潮资讯-数据中心-专题统计-股东股本-实际控制人持股变动 | required: symbol | 证劵代码, 证券简称, 变动日期, 控股数量, 控股比例, 控制类型 |


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
