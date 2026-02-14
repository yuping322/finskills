# 数据获取命令（共享脚本）

运行时约定：仅支持 Python 3.10–3.12，并使用仓库根目录统一虚拟环境 `.venv`。

从本技能目录运行。共享数据脚本位于 `../findata-toolkit-cn/`。（分析股权质押比例、质押分布、行业对比及结构特征，输出控制权与财务/流动性风险提示。当用户询问股权质押、质押比例、质押风险或需要质押风险扫描时使用。）


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
| equity_pledge_dashboard | custom | composed view | 股权质押风险聚合：质押概览、行业分布、质押比例（工具聚合视图）。 | common: date | data keys: profile, industry_data, distribute_company, distribute_bank, pledge_ratio, pledge_ratio_detail |
| stock_gpzy_pledge_ratio_em | tool | tool view (1:1) | 东方财富网-数据中心-特色数据-股权质押-上市公司质押比例 | required: date | 序号, 股票代码, 股票简称, 交易日期, 所属行业, 质押比例, 质押股数, 质押市值, 质押笔数, 无限售股质押数 |
| stock_gpzy_pledge_ratio_detail_em | tool | tool view (1:1) | 东方财富网-数据中心-特色数据-股权质押-重要股东股权质押明细 | - | 序号, 股票代码, 股票简称, 质押股份数量, 占所持股份比例, 占总股本比例, 质押机构, 最新价, 质押日收盘价, 预估平仓线 |
#### `equity_pledge_dashboard` 底层工具（plan 展开）


| key | tool | 说明 | 入参（必填/常用） | 关键输出字段（示例） |
| --- | --- | --- | --- | --- |
| profile | stock_gpzy_profile_em | 东方财富网-数据中心-特色数据-股权质押-股权质押市场概况 | - | 交易日期, A股质押总比例, 质押公司数量, 质押笔数, 质押总股数, 质押总市值, 沪深300指数, 涨跌幅 |
| industry_data | stock_gpzy_industry_data_em | 东方财富网-数据中心-特色数据-股权质押-上市公司质押比例-行业数据 | - | 行业, 平均质押比例, 公司家数, 质押总笔数, 质押总股本, 最新质押市值, 统计时间 |
| distribute_company | stock_gpzy_distribute_statistics_company_em | 东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-证券公司 | - | 序号, 质押机构, 质押公司数量, 质押笔数, 质押数量, 未达预警线比例, 达到预警线未达平仓线比例, 达到平仓线比例 |
| distribute_bank | stock_gpzy_distribute_statistics_bank_em | 东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-银行 | - | 序号, 质押机构, 质押公司数量, 质押笔数, 质押数量, 未达预警线比例, 达到预警线未达平仓线比例, 达到平仓线比例 |
| pledge_ratio | stock_gpzy_pledge_ratio_em | 东方财富网-数据中心-特色数据-股权质押-上市公司质押比例 | required: date | 序号, 股票代码, 股票简称, 交易日期, 所属行业, 质押比例, 质押股数, 质押市值, 质押笔数, 无限售股质押数 |
| pledge_ratio_detail | stock_gpzy_pledge_ratio_detail_em | 东方财富网-数据中心-特色数据-股权质押-重要股东股权质押明细 | - | 序号, 股票代码, 股票简称, 质押股份数量, 占所持股份比例, 占总股本比例, 质押机构, 最新价, 质押日收盘价, 预估平仓线 |


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
