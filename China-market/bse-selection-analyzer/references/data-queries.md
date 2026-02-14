# 数据获取命令（共享脚本）

运行时约定：仅支持 Python 3.10–3.12，并使用仓库根目录统一虚拟环境 `.venv`。

从本技能目录运行。共享数据脚本位于 `../findata-toolkit-cn/`。（扫描与分析北交所（BSE）标的，按流动性、成长性、行业景气与“专精特新”特征输出候选清单，并给出流动性与波动风险提示。当用户询问北交所精选、北交所选股、专精特新筛选、或需要北交所板块研究时使用。）


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
| stock_info_bj_name_code | tool | tool view (1:1) | 北京证券交易所股票代码和简称数据 | - | 证券代码, 证券简称, 总股本, 流通股本, 上市日期, 所属行业, 地区, 报告日期 |
| stock_bj_a_spot_em | tool | tool view (1:1) | 东方财富网-京 A 股-实时行情数据 | - | 序号, 代码, 最新价, 涨跌幅, 涨跌额, 成交量, 成交额, 振幅, 最高, 最低 |
| stock_zcfz_bj_em | tool | tool view (1:1) | 东方财富-数据中心-年报季报-业绩快报-资产负债表 | required: date | 序号, 股票代码, 股票简称, 资产-货币资金, 资产-应收账款, 资产-存货, 资产-总资产, 资产-总资产同比, 负债-应付账款, 负债-总负债 |
| stock_zh_a_hist | tool | tool view (1:1) | 东方财富-沪深京 A 股日频率数据; 历史数据按日频率更新, 当日收盘价请在收盘后获取 | required: symbol, period, start_date, end_date, adjust; common: timeout | tool envelope: {meta,data,warnings,errors} |

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
