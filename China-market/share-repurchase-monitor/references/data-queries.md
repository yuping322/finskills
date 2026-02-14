# 数据获取命令（共享脚本）

运行时约定：仅支持 Python 3.10–3.12，并使用仓库根目录统一虚拟环境 `.venv`。

从本技能目录运行。共享数据脚本位于 `../findata-toolkit-cn/`。（跟踪并解读A股股份回购（目的、进度、均价、区间、完成度），用于评估管理层信号、估值锚与“利好兑现/利好出尽”风险，并输出可跟踪的回购清单与规则。当用户询问A股回购、回购进度、回购均价、回购信号或需要回购筛选时使用。）


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
| repurchase_dashboard | custom | composed view | 股票回购聚合视图：回购清单 + 个股股本变动（可选；工具聚合视图）。 | common: symbol, start_date, end_date | data keys: repurchase_list, share_change |
#### `repurchase_dashboard` 底层工具（plan 展开）


| key | tool | 说明 | 入参（必填/常用） | 关键输出字段（示例） |
| --- | --- | --- | --- | --- |
| repurchase_list | stock_repurchase_em | 东方财富网-数据中心-股票回购-股票回购数据 | - | 序号, 股票代码, 股票简称, 最新价, 计划回购价格区间, 计划回购数量区间-下限, 计划回购数量区间-上限, 占公告前一日总股本比例-下限, 占公告前一日总股本比例-上限, 计划回购金额区间-下限 |
| share_change | stock_share_change_cninfo | 巨潮资讯-数据-公司股本变动 | required: symbol, start_date, end_date | 证券简称, 境外法人持股, 证券投资基金持股, 国家持股-受限, 国有法人持股, 配售法人股, 发起人股份, 未流通股份, 其中：境外自然人持股, 其他流通受限股份 |


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
