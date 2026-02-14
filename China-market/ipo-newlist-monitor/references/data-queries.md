# 数据获取命令（共享脚本）

运行时约定：仅支持 Python 3.10–3.12，并使用仓库根目录统一虚拟环境 `.venv`。

从本技能目录运行。共享数据脚本位于 `../findata-toolkit-cn/`。（跟踪 IPO 申报、新股上市、次新股与 IPO 受益股，输出事件清单与风险提示。当用户询问新股、次新、IPO 进展、IPO 受益股或需要新股日历/复盘时使用。）


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
| ipo_newlist_dashboard | custom | composed view | IPO/新股/次新聚合：申报、新股发行、新股列表、首日与受益股（工具聚合视图）。 | common: symbol | data keys: ipo_declare, new_ipo_cninfo, new_stock_list_em, sub_new_list_sina, new_list_first_day_ths, ipo_benefit_ths |
#### `ipo_newlist_dashboard` 底层工具（plan 展开）


| key | tool | 说明 | 入参（必填/常用） | 关键输出字段（示例） |
| --- | --- | --- | --- | --- |
| ipo_declare | stock_ipo_declare | 东方财富网-数据中心-新股申购-首发申报信息-首发申报企业信息 | - | 序号, 申报企业, 拟上市地, 保荐机构, 会计师事务所, 律师事务所, 备注 |
| new_ipo_cninfo | stock_new_ipo_cninfo | 巨潮资讯-数据中心-新股数据-新股发行 | - | 证劵代码, 证券简称, 上市日期, 申购日期, 发行价, 总发行数量, 发行市盈率, 上网发行中签率, 摇号结果公告日, 中签公告日 |
| new_stock_list_em | stock_zh_a_new_em | 东方财富网-行情中心-沪深个股-新股 | - | 序号, 代码, 最新价, 涨跌幅, 涨跌额, 成交量, 成交额, 振幅, 最高, 最低 |
| sub_new_list_sina | stock_zh_a_new | 新浪财经-行情中心-沪深股市-次新股 | - | symbol, code, name, open, high, low, volume, amount, mktcap, turnoverratio |
| new_list_first_day_ths | stock_xgsr_ths | 同花顺-数据中心-新股数据-新股上市首日 | - | 序号, 股票代码, 股票简称, 上市日期, 发行价, 最新价, 首日开盘价, 首日收盘价, 首日最高价, 首日最低价 |
| ipo_benefit_ths | stock_ipo_benefit_ths | 同花顺-数据中心-新股数据-IPO受益股 | - | 序号, 股票代码, 股票简称, 收盘价, 涨跌幅, 市值, 参股家数, 投资总额, 投资占市值比, 参股对象 |


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
