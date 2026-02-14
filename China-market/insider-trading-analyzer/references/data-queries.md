# 数据获取命令（共享脚本）

运行时约定：仅支持 Python 3.10–3.12，并使用仓库根目录统一虚拟环境 `.venv`。

从本技能目录运行。共享数据脚本位于 `../findata-toolkit-cn/`。（分析A股市场董监高及重要股东增减持行为，识别具有显著管理层信心信号的公司。当用户询问董监高增持、大股东买入、内部人交易分析、管理层增持信号、股东增减持动态时使用此技能。）


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
| stock_ggcg_em | tool | tool view (1:1) | 东方财富网-数据中心-特色数据-高管持股 | required: symbol | 代码, 最新价, 涨跌幅, 持股变动信息-增减, 持股变动信息-变动数量, 持股变动信息-占总股本比例, 持股变动信息-占流通股比例, 变动后持股情况-持股总数, 变动后持股情况-占总股本比例, 变动后持股情况-持流通股数 |
| stock_inner_trade_xq | tool | tool view (1:1) | 雪球-行情中心-沪深股市-内部交易 | - | 股票代码, 变动日期, 变动人, 变动股数, 成交均价, 变动后持股数, 与董监高关系, 董监高职务 |
| stock_shareholder_change_ths | tool | tool view (1:1) | 同花顺-公司大事-股东持股变动 | required: symbol | 公告日期, 变动股东, 变动数量, 交易均价, 剩余股份总数, 变动期间, 变动途径 |

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
