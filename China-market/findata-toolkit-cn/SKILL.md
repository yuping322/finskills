---
name: findata-toolkit-cn
description: A股金融数据工具包。提供脚本获取A股实时行情、财务指标、董监高增减持、北向资金、宏观经济数据（LPR、CPI/PPI、PMI、社融、M2）。用于需要实时A股市场数据支撑投资分析时。所有数据源免费，无需API密钥。
license: Apache-2.0
---

# 金融数据工具包 — A股市场

自包含的数据工具包，提供A股市场实时金融数据和定量计算。所有数据源**免费**，**无需API密钥**。

## 安装

安装依赖（一次性）：

```bash
pip install -r requirements.txt
```

## 可用工具

所有脚本位于 `scripts/` 目录。从技能根目录运行。

### 0. AKShare 工具全集（`config/litellm_tools.json` → `scripts/akshare_tools.py`）

本工具包内置 `config/litellm_tools.json`（356 个接口定义），并提供统一的“工具运行器”脚本：

- 列出工具：`python scripts/akshare_tools.py list --contains fund_flow`
- 查看某工具入参 schema：`python scripts/akshare_tools.py describe stock_zt_pool_em`
- 直接调用（无参数）：`python scripts/akshare_tools.py stock_zh_a_spot_em`
- 直接调用（带参数）：`python scripts/akshare_tools.py stock_individual_info_em --set symbol=000001`
- JSON 入参调用：`python scripts/akshare_tools.py stock_zh_a_hist --args '{"symbol":"000001","period":"daily","start_date":"20250101","end_date":"20250201","adjust":"qfq"}'`

说明：
- 默认启用文件缓存（`FINSKILLS_CACHE_DIR` 可指定缓存目录）；可用 `--no-cache` 关闭，`--refresh` 强制刷新。
- `token/timeout` 等参数在工具定义中可能被标记为必填但默认 `None`；运行器会尽量做兼容处理（缺省则填 `None`）。

### 0.5 组合视图 Views（`scripts/views_runner.py`）

Views 用于把多个底层工具（356 个接口）组合成更稳定、可复用的“数据视图”，供上层分析技能直接引用。

- 同时，Views Runner 会把 **356 个底层工具自动暴露为同名 view**（view 名 == tool 名），从而在上层只需要统一调用 views。
- 列出可用 views：`python scripts/views_runner.py list`
- 查看 view 入参：`python scripts/views_runner.py describe fund_flow_dashboard`
- 运行 view：`python scripts/views_runner.py fund_flow_dashboard`
- 常用视图示例：`python scripts/views_runner.py repurchase_dashboard`、`python scripts/views_runner.py block_deal_dashboard`
- 运行“工具同名 view”（等价于直接调用 tool）：`python scripts/views_runner.py stock_zh_a_spot_em`
- 只看计划不执行（便于写 references）：`python scripts/views_runner.py dragon_tiger_daily --set date=20250211 --dry-run`

远程模式（推荐用于产品化/稳定取数）：

- 设置 `FINSKILLS_VIEW_API_URL` 或使用 `--remote-url`，`list/describe/run` 会直连远端 View API（只消费 `{meta,data,warnings,errors}`，不做本地清洗/转换）。
- 示例：`FINSKILLS_VIEW_API_URL=http://127.0.0.1:8808 python scripts/views_runner.py list`
- 示例：`python scripts/views_runner.py --remote-url http://127.0.0.1:8808 repurchase_dashboard --set symbol=000001`
- 远端可以暴露任意 view 名称（包括“工具同名 view”）；本地只按 view 名调用。
- 远程模式下 `--dry-run` 不可用（远端 API 默认不暴露 plan）。

可选鉴权/超时：

- `FINSKILLS_VIEW_API_TOKEN`（Bearer）或 `FINSKILLS_VIEW_API_KEY`
- `FINSKILLS_VIEW_API_TIMEOUT`（秒，默认 30）

输出可靠性提示：
- 所有 tool/view 输出均为统一 envelope：`{meta, data, warnings, errors}`；请优先检查 `errors` 和 `warnings` 再做结论。
- `meta.as_of` 记录抓取时间；若命中缓存，会在 `meta.cache` 里看到缓存 age/ttl。
- 每次 tool 调用的 `meta.result` 会尽量附带结果类型与规模（如 `type/rows/columns`）；空结果会写入 `warnings`，避免“无数据=无事件”的误判。

### 1. A股数据 (`scripts/stock_data.py`)

通过 AKShare 获取A股基本面、行情、财务指标。

| 命令 | 用途 |
|------|------|
| `python scripts/stock_data.py 600519` | 基本信息（贵州茅台） |
| `python scripts/stock_data.py 600519 --metrics` | 完整财务指标（估值、盈利、杠杆、增长） |
| `python scripts/stock_data.py 600519 --history` | 历史OHLCV行情 |
| `python scripts/stock_data.py 600519 --financials` | 利润表、资产负债表、现金流量表 |
| `python scripts/stock_data.py 600519 --insider` | 董监高增减持数据 |
| `python scripts/stock_data.py --northbound` | 北向资金流向（沪股通/深股通） |
| `python scripts/stock_data.py 600519 000858 --screen` | 批量筛选 |

### 2. 宏观数据 (`scripts/macro_data.py`)

通过 AKShare 获取中国宏观经济指标。

| 命令 | 用途 |
|------|------|
| `python scripts/macro_data.py --dashboard` | 完整宏观仪表盘 |
| `python scripts/macro_data.py --rates` | 利率数据（LPR、Shibor） |
| `python scripts/macro_data.py --inflation` | CPI/PPI数据 |
| `python scripts/macro_data.py --pmi` | PMI数据（制造业/非制造业） |
| `python scripts/macro_data.py --social-financing` | 社会融资规模 + M2 |
| `python scripts/macro_data.py --cycle` | 经济周期阶段判断 |

## 数据来源

| 来源 | 数据内容 | API密钥 |
|------|----------|---------|
| AKShare | A股行情、财务数据、董监高交易、北向资金、宏观指标 | 无需 |

## 输出格式

所有脚本以 **JSON** 输出到标准输出，便于解析。错误信息输出到标准错误。

## 配置

可选：编辑 `config/data_sources.yaml` 自定义速率限制或添加付费数据源API密钥。
