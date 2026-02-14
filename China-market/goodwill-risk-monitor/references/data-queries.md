# 数据获取命令（共享脚本）

运行时约定：仅支持 Python 3.10–3.12，并使用仓库根目录统一虚拟环境 `.venv`。

从本技能目录运行。共享数据脚本位于 `../findata-toolkit-cn/`。（监控公司/行业商誉规模、减值明细与预警信号，识别潜在商誉减值风险与财报冲击。当用户询问商誉、商誉减值、商誉风险或需要商誉风险清单时使用。）


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
| goodwill_dashboard | custom | composed view | 商誉聚合：公司/行业商誉、减值明细与预期（工具聚合视图）。 | common: date | data keys: profile, goodwill_company, goodwill_industry, impairment_detail, impairment_expectation |
#### `goodwill_dashboard` 底层工具（plan 展开）


| key | tool | 说明 | 入参（必填/常用） | 关键输出字段（示例） |
| --- | --- | --- | --- | --- |
| profile | stock_sy_profile_em | 东方财富网-数据中心-特色数据-商誉-A股商誉市场概况 | - | 报告期, 商誉, 商誉减值, 净资产, 商誉占净资产比例, 商誉减值占净资产比例, 净利润规模, 商誉减值占净利润比例 |
| goodwill_company | stock_sy_em | 东方财富网-数据中心-特色数据-商誉-个股商誉明细 | required: date | 序号, 股票代码, 股票简称, 商誉, 商誉占净资产比例, 净利润, 净利润同比, 上年商誉, 公告日期, 交易市场 |
| goodwill_industry | stock_sy_hy_em | 东方财富网-数据中心-特色数据-商誉-行业商誉 | required: date | 公司家数, 商誉规模, 净资产, 商誉规模占净资产规模比例, 净利润规模 |
| impairment_detail | stock_sy_jz_em | 东方财富网-数据中心-特色数据-商誉-个股商誉减值明细 | required: date | 序号, 股票代码, 股票简称, 商誉, 商誉减值, 商誉减值占净资产比例, 净利润, 商誉减值占净利润比例, 公告日期, 交易市场 |
| impairment_expectation | stock_sy_yq_em | 东方财富网-数据中心-特色数据-商誉-商誉减值预期明细 | required: date | 序号, 股票代码, 股票简称, 业绩变动原因, 最新商誉报告期, 最新一期商誉, 上年商誉, 预计净利润-下限, 预计净利润-上限, 业绩变动幅度-下限 |


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
