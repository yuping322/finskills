# China-market Skills 测试报告

测试日期：2026-02-15  
测试范围：56个China-market skills，137个views  
测试模式：validate（配置验证）+ run（实际数据获取）

---

## 测试概览

### 验证模式（Validate Mode）
- **测试项目**：137个views
- **通过率**：100% (137/137)
- **失败数**：0
- **结论**：所有views的配置都正确，plan函数可以正常构建

### 运行模式（Run Mode）
- **测试项目**：137个views（去重后实际运行74个unique views）
- **通过率**：99.3% (136/137)
- **失败数**：1
- **失败view**：`notice_daily_dashboard` (disclosure-notice-monitor skill)
- **失败原因**：`stock_notice_report: '代码'` - 数据字段缺失

---

## 失败详情

### 1. disclosure-notice-monitor
- **失败view**：notice_daily_dashboard
- **错误信息**：stock_notice_report: '代码'
- **问题分析**：
  1. 底层AKShare接口`stock_notice_report`返回的数据缺少'代码'字段
  2. 可能是AKShare接口变更或数据源问题
  3. view的plan函数期望该字段存在，但实际数据中不存在
- **影响范围**：disclosure-notice-monitor skill无法正常获取公告数据
- **建议修复**：
  1. 检查AKShare的`stock_notice_report`接口文档，确认字段名称
  2. 更新view的字段映射逻辑，适配新的字段名
  3. 添加字段缺失的降级处理

---

## 成功运行的Skills（55个）

以下skills的所有views都成功运行并返回了有效数据：

1. ✅ ab-ah-premium-monitor (1 view)
2. ✅ block-deal-monitor (1 view)
3. ✅ bse-selection-analyzer (4 views)
4. ✅ concept-board-analyzer (5 views)
5. ✅ convertible-bond-scanner (2 views)
6. ✅ dividend-corporate-action-tracker (4 views)
7. ✅ dragon-tiger-list-analyzer (2 views)
8. ✅ equity-pledge-risk-monitor (3 views)
9. ✅ equity-research-orchestrator (2 views)
10. ✅ esg-screener (8 views)
11. ✅ etf-allocator (2 views)
12. ✅ event-driven-detector (2 views)
13. ✅ event-study (2 views)
14. ✅ factor-crowding-monitor (2 views)
15. ✅ financial-statement-analyzer (5 views)
16. ✅ fund-flow-monitor (4 views)
17. ✅ goodwill-risk-monitor (1 view)
18. ✅ high-dividend-strategy (4 views)
19. ✅ hot-rank-sentiment-monitor (4 views)
20. ✅ hsgt-holdings-monitor (3 views)
21. ✅ industry-board-analyzer (6 views)
22. ✅ industry-chain-mapper (4 views)
23. ✅ insider-trading-analyzer (3 views)
24. ✅ intraday-microstructure-analyzer (1 view)
25. ✅ investment-memo-generator (2 views)
26. ✅ ipo-lockup-risk-monitor (4 views)
27. ✅ ipo-newlist-monitor (1 view)
28. ✅ limit-up-limit-down-risk-checker (2 views)
29. ✅ limit-up-pool-analyzer (1 view)
30. ✅ liquidity-impact-estimator (1 view)
31. ✅ macro-liquidity-monitor (1 view)
32. ✅ margin-risk-monitor (1 view)
33. ✅ market-breadth-monitor (2 views)
34. ✅ market-overview-dashboard (1 view)
35. ✅ northbound-flow-analyzer (3 views)
36. ✅ peer-comparison-analyzer (2 views)
37. ✅ policy-sensitivity-brief (1 view)
38. ✅ portfolio-health-check (1 view)
39. ✅ portfolio-monitor-orchestrator (1 view)
40. ✅ quant-factor-screener (3 views)
41. ✅ rebalancing-planner (1 view)
42. ✅ risk-adjusted-return-optimizer (1 view)
43. ✅ sector-rotation-detector (4 views)
44. ✅ sentiment-reality-gap (4 views)
45. ✅ share-repurchase-monitor (1 view)
46. ✅ shareholder-risk-check (2 views)
47. ✅ shareholder-structure-monitor (1 view)
48. ✅ small-cap-growth-identifier (3 views)
49. ✅ st-delist-risk-scanner (1 view)
50. ✅ suitability-report-generator (2 views)
51. ✅ tech-hype-vs-fundamentals (2 views)
52. ✅ undervalued-stock-screener (3 views)
53. ✅ valuation-regime-detector (3 views)
54. ✅ volatility-regime-monitor (1 view)
55. ✅ weekly-market-brief-generator (2 views)

---

## 每个Skill的潜在问题分析

基于methodology文档、data-queries配置和测试结果，以下是每个skill可能存在的3-5个问题：

