#!/bin/bash
# Skills 批量测试脚本 - 通过 Kiro CLI 运行

# 配置
OUTPUT_DIR="test-results"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
TEST_SESSION_DIR="${OUTPUT_DIR}/${TIMESTAMP}"

# 创建输出目录
mkdir -p "${TEST_SESSION_DIR}"

echo "=== Kiro Skills 批量测试 ==="
echo "测试时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "输出目录: ${TEST_SESSION_DIR}"
echo ""

# 测试用例列表
declare -a TEST_CASES=(
    "帮我分析一下最近的大宗交易情况"
    "给我做一个龙虎榜分析"
    "分析一下最近北向资金的流向"
    "检查一下有哪些股票有ST退市风险"
    "帮我监控一下股权质押风险"
    "分析一下最近的涨跌停板情况"
    "给我做一个概念板块分析"
    "分析一下最近的IPO解禁风险"
    "帮我做一个市场宽度监控"
    "生成一份周度市场简报"
)

# 运行测试
TOTAL=${#TEST_CASES[@]}
CURRENT=0

for prompt in "${TEST_CASES[@]}"; do
    CURRENT=$((CURRENT + 1))
    
    # 生成安全的文件名
    SAFE_NAME=$(echo "$prompt" | sed 's/[^a-zA-Z0-9\u4e00-\u9fa5]/_/g' | cut -c1-50)
    OUTPUT_FILE="${TEST_SESSION_DIR}/${CURRENT}_${SAFE_NAME}.md"
    
    echo "[$CURRENT/$TOTAL] 测试: $prompt"
    echo "  输出文件: $OUTPUT_FILE"
    
    # 创建提示词文件
    PROMPT_FILE="${TEST_SESSION_DIR}/.prompt_${CURRENT}.txt"
    echo "$prompt" > "$PROMPT_FILE"
    
    # 写入测试信息到输出文件
    cat > "$OUTPUT_FILE" << EOF
# Skill 测试报告

## 测试信息
- **测试编号**: $CURRENT / $TOTAL
- **测试时间**: $(date '+%Y-%m-%d %H:%M:%S')
- **提示词**: $prompt
- **提示词文件**: $PROMPT_FILE

---

## 说明

请在 Kiro 中手动测试此提示词，或者将提示词复制到 Kiro 对话框中。

**提示词**：
\`\`\`
$prompt
\`\`\`

---

## 测试结果

请在此处记录测试结果：

### 执行状态
- [ ] 成功
- [ ] 失败
- [ ] 部分成功

### 发现的问题
1. 
2. 
3. 

### 数据可用性
- [ ] 数据完整
- [ ] 数据部分缺失
- [ ] 数据完全不可用

### 错误信息
\`\`\`
（如有错误，请在此处粘贴）
\`\`\`

### 输出质量
- [ ] 输出格式正确
- [ ] 分析逻辑正确
- [ ] 建议可执行

### 备注


EOF
    
    echo "  ✅ 测试模板已创建"
    
    echo ""
    
    # 不需要等待，因为只是生成模板
done

# 生成汇总报告
SUMMARY_FILE="${TEST_SESSION_DIR}/00_SUMMARY.md"

cat > "$SUMMARY_FILE" << EOF
# Skills 批量测试汇总报告

## 测试概况
- **测试时间**: $(date '+%Y-%m-%d %H:%M:%S')
- **测试总数**: $TOTAL
- **输出目录**: ${TEST_SESSION_DIR}

## 测试用例列表

EOF

CURRENT=0
for prompt in "${TEST_CASES[@]}"; do
    CURRENT=$((CURRENT + 1))
    SAFE_NAME=$(echo "$prompt" | sed 's/[^a-zA-Z0-9\u4e00-\u9fa5]/_/g' | cut -c1-50)
    OUTPUT_FILE="${CURRENT}_${SAFE_NAME}.md"
    
    echo "$CURRENT. **$prompt**" >> "$SUMMARY_FILE"
    echo "   - 输出文件: [\`$OUTPUT_FILE\`](./$OUTPUT_FILE)" >> "$SUMMARY_FILE"
    echo "" >> "$SUMMARY_FILE"
done

cat >> "$SUMMARY_FILE" << EOF

## 使用说明

### 查看单个测试结果
\`\`\`bash
cat ${TEST_SESSION_DIR}/<测试编号>_*.md
\`\`\`

### 查看所有测试结果
\`\`\`bash
ls -lh ${TEST_SESSION_DIR}/
\`\`\`

### 搜索错误
\`\`\`bash
grep -r "错误\|失败\|Error\|Failed" ${TEST_SESSION_DIR}/
\`\`\`

### 搜索数据缺失问题
\`\`\`bash
grep -r "数据不可用\|接口返回为空\|暂无数据" ${TEST_SESSION_DIR}/
\`\`\`

## 下一步

1. 查看汇总报告识别问题
2. 检查每个测试的详细输出
3. 修复发现的问题
4. 重新运行失败的测试

EOF

echo "=== 测试完成 ==="
echo ""
echo "汇总报告: $SUMMARY_FILE"
echo "详细结果: ${TEST_SESSION_DIR}/"
echo ""
echo "快速查看汇总:"
echo "  cat $SUMMARY_FILE"
echo ""
echo "搜索错误:"
echo "  grep -r '错误\|Error' ${TEST_SESSION_DIR}/"
echo ""

