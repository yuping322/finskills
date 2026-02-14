# 数据获取命令（共享脚本）

运行时约定：仅支持 Python 3.10–3.12，并使用仓库根目录统一虚拟环境 `.venv`。

从本技能目录运行。共享数据脚本位于 `../findata-toolkit-cn/`。（使用正式因子模型进行系统化多因子A股筛选，识别具有有利因子暴露的个股。当用户询问因子投资、多因子筛选、价值/动量/质量因子分析、因子打分、因子择时、Smart Beta策略、量化选股或基于学术因子的系统化选股时使用此技能。）


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
| stock_zh_a_spot_em | tool | tool view (1:1) | 东方财富网-沪深京 A 股-实时行情数据 | - | 序号, 代码, 最新价, 涨跌幅, 涨跌额, 成交量, 成交额, 振幅, 最高, 最低 |
| stock_a_indicator_lg | tool | tool view (1:1) | 乐咕乐股-A 股个股指标: 市盈率, 市净率, 股息率 | required: symbol | trade_date, pe, pe_ttm, pb, ps, ps_ttm, dv_ratio, dv_ttm, total_mv |
| stock_financial_abstract_ths | tool | tool view (1:1) | 同花顺-财务指标-主要指标 | required: symbol, indicator | 报告期, 净利润, 净利润同比增长率, 扣非净利润, 扣非净利润同比增长率, 营业总收入, 营业总收入同比增长率, 基本每股收益, 每股净资产, 每股资本公积金 |

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
