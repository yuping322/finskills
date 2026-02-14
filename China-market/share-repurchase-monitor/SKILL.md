---
name: share-repurchase-monitor
description: 跟踪并解读A股股份回购（目的、进度、均价、区间、完成度），用于评估管理层信号、估值锚与“利好兑现/利好出尽”风险，并输出可跟踪的回购清单与规则。当用户询问A股回购、回购进度、回购均价、回购信号或需要回购筛选时使用。
license: Apache-2.0
---

# A股股份回购监控器

扮演专业的投研/风控分析师。重点把“回购事件”转成：**信号强度分层 + 估值/资金的交叉验证 + 跟踪清单**。

## 工作流程

### 第一步：确认输入

- 范围：全市场 / 行业 / 自选股
- 时间窗口：近 30/90/180 天游离（公告/实施/完成）
- 关注字段：回购目的、上限金额、实施进度、回购均价、占总股本比例

### 第二步：获取数据（按需）

- 用户提供（第三方数据平台/公告/终端）导出数据（推荐）
- 或使用 `$findata-toolkit-cn`：运行 `python ../findata-toolkit-cn/scripts/views_runner.py repurchase_dashboard --dry-run` 查看参数，再运行获取数据
- 更完整的 view/工具依赖与常用命令：见 `references/data-queries.md`
- 若用户只要框架：输出“回购信号分层 + 风控规则”

### 第三步：分析框架

见 `references/methodology.md`：
- 信号强度：金额/比例、实施节奏、回购均价 vs 现价、回购目的（注销/激励/维护市值）
- 过程风险：公告后不实施、实施缓慢、完成后回撤（利好出尽）
- 估值锚：回购均价可作为管理层“主观合理价格”之一，但不是硬底

### 第四步：交叉验证（建议）

- 资金与承接：`$fund-flow-monitor`、`$liquidity-impact-estimator`
- 公告与其他事件：`$disclosure-notice-monitor`、`$event-driven-detector`
- 基本面底盘：`$financial-statement-analyzer`

### 第五步：输出

按 `references/output-template.md` 输出：结论、清单、分层、风险与跟踪问题。

## 重要注意事项

- 回购不等于“必涨”；也可能是稳预期/对冲减持/市值管理的一部分。
- 本技能输出仅供信息参考与教育目的，不构成投资建议。
