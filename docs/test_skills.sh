#!/bin/bash
# Skills 快速测试脚本

PYTHON=".venv/bin/python3"
VIEWS_RUNNER="China-market/findata-toolkit-cn/scripts/views_runner.py"

echo "=== Skills 功能测试 ==="
echo ""

# 测试 1: 列出可用 views
echo "测试 1: 列出可用 views（前10个）"
echo "命令: $PYTHON $VIEWS_RUNNER list"
echo ""
$PYTHON $VIEWS_RUNNER list | head -20
echo ""

# 测试 2: 搜索大宗交易相关 views
echo "测试 2: 搜索大宗交易相关 views"
echo "命令: $PYTHON $VIEWS_RUNNER list --contains block_deal"
echo ""
$PYTHON $VIEWS_RUNNER list --contains block_deal
echo ""

# 测试 3: 查看 view 参数说明
echo "测试 3: 查看 block_deal_dashboard 参数说明"
echo "命令: $PYTHON $VIEWS_RUNNER describe block_deal_dashboard"
echo ""
$PYTHON $VIEWS_RUNNER describe block_deal_dashboard
echo ""

# 测试 4: 查看执行计划（不实际获取数据）
echo "测试 4: 查看 block_deal_dashboard 执行计划"
echo "命令: $PYTHON $VIEWS_RUNNER block_deal_dashboard --dry-run --set start_date=20260214 --set end_date=20260221"
echo ""
$PYTHON $VIEWS_RUNNER block_deal_dashboard --dry-run --set start_date=20260214 --set end_date=20260221
echo ""

echo "=== 测试完成 ==="
echo ""
echo "如果以上测试都成功，说明数据工具包环境配置正确！"
echo ""
echo "⚠️  重要提示："
echo "  - 以上测试的是【数据脚本】，只返回原始 JSON 数据"
echo "  - 这不等于【Skills】！Skills = 数据 + 方法论 + 分析 + 建议"
echo ""
echo "推荐使用方式："
echo "  ✅ 在 Kiro 中直接提问（完整的 Skill 体验）"
echo "     例如：'帮我分析一下最近的大宗交易情况'"
echo ""
echo "高级用户："
echo "  ⚙️  直接运行数据脚本获取原始数据"
echo "     命令：$PYTHON $VIEWS_RUNNER <view_name>"
echo ""
echo "详细说明请查看：SKILLS_VS_DATA.md"
echo ""
