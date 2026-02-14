# 数据获取命令（共享脚本）

运行时约定：仅支持 Python 3.10–3.12，并使用仓库根目录统一虚拟环境 `.venv`。

从本技能目录运行。共享数据脚本位于 `../findata-toolkit-cn/`。（跟踪宏观流动性指标（利率、通胀、信用、政策取向）并总结对资产/行业的影响。当用户询问流动性环境、政策对市场影响或需要宏观流动性仪表盘时使用。）


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
| macro_china_dashboard | custom | composed view | 宏观仪表盘：利率(LPR/Shibor)、通胀(CPI/PPI)、PMI、社融与M2（工具聚合视图）。 | - | data keys: lpr, shibor, cpi, ppi, pmi, social_financing, m2 |
#### `macro_china_dashboard` 底层工具（plan 展开）


| key | tool | 说明 | 入参（必填/常用） | 关键输出字段（示例） |
| --- | --- | --- | --- | --- |
| lpr | macro_china_lpr | 中国-宏观-贷款市场报价利率(LPR) | - | (columns as-is) |
| shibor | rate_interbank | 中国-宏观-同业拆借利率(如 Shibor) | required: market, symbol, indicator | (columns as-is) |
| cpi | macro_china_cpi_monthly | 中国-宏观-CPI(月度) | - | (columns as-is) |
| ppi | macro_china_ppi | 中国-宏观-PPI | - | (columns as-is) |
| pmi | macro_china_pmi | 中国-宏观-PMI(月度) | - | (columns as-is) |
| social_financing | macro_china_shrzgm | 中国-宏观-社会融资规模(月度) | - | (columns as-is) |
| m2 | macro_china_m2_yearly | 中国-宏观-M2(年度) | - | (columns as-is) |


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
