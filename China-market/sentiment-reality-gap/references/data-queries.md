# 数据获取命令（共享脚本）

运行时约定：仅支持 Python 3.10–3.12，并使用仓库根目录统一虚拟环境 `.venv`。

从本技能目录运行。共享数据脚本位于 `../findata-toolkit-cn/`。（识别A股市场中被过度看空但基本面稳健的逆向投资机会。当用户询问逆向投资、超跌反弹、市场错误定价、情绪与基本面背离、被市场误解的公司、负面情绪过度反应、或者寻找"市场错杀"机会时使用此技能。）


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
| hot_rank_sentiment_dashboard | custom | composed view | 人气/热度与情绪代理聚合：人气榜、相关股票、关注指数、投票等（工具聚合视图）。 | common: symbol | data keys: hot_rank_list, xq_hot_deal |
| stock_hot_rank_em | tool | tool view (1:1) | 东方财富网站-股票热度 | - | 当前排名, 代码, 最新价, 涨跌额, 涨跌幅 |
| stock_hot_rank_detail_em | tool | tool view (1:1) | 东方财富网-股票热度-历史趋势及粉丝特征 | required: symbol | 时间, 排名, 证券代码, 新晋粉丝, 铁杆粉丝 |
| stock_hot_keyword_em | tool | tool view (1:1) | 东方财富-个股人气榜-热门关键词 | required: symbol | 时间, 股票代码, 概念代码, 热度 |
#### `hot_rank_sentiment_dashboard` 底层工具（plan 展开）


| key | tool | 说明 | 入参（必填/常用） | 关键输出字段（示例） |
| --- | --- | --- | --- | --- |
| hot_rank_list | stock_hot_rank_em | 东方财富网站-股票热度 | - | 当前排名, 代码, 最新价, 涨跌额, 涨跌幅 |
| xq_hot_deal | stock_hot_deal_xq | 雪球-沪深股市-热度排行榜-交易排行榜 | required: symbol | 股票代码, 股票简称, 关注, 最新价 |


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
