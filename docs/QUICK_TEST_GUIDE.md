# Skills 快速测试指南

## 快速开始（3 步）

### 1. 生成测试文件

```bash
python3 auto_test_skills.py
```

这会创建：
- `test-results/<时间戳>/` 目录
- 10 个测试模板文件（`01_*.md` 到 `10_*.md`）
- 10 个提示词文件（`.prompt_01.txt` 到 `.prompt_10.txt`）
- 1 个汇总报告（`00_SUMMARY.md`）

### 2. 在 Kiro 中测试

**方法 A：手动复制粘贴**（推荐）

1. 打开第一个测试文件：
   ```bash
   cat test-results/<时间戳>/01_*.md
   ```

2. 复制其中的提示词

3. 在 Kiro 中粘贴并运行

4. 将 Kiro 的完整输出复制回测试文件的"测试结果"部分

5. 勾选相应的复选框，记录问题

6. 重复步骤 1-5 完成所有测试

**方法 B：使用提示词文件**

1. 查看提示词：
   ```bash
   cat test-results/<时间戳>/.prompt_01.txt
   ```

2. 在 Kiro 中输入这个提示词

3. 记录结果到对应的测试文件

### 3. 分析结果

```bash
# 查看汇总报告
cat test-results/<时间戳>/00_SUMMARY.md

# 搜索数据问题
grep -r "数据.*缺失\|数据.*不可用" test-results/<时间戳>/

# 搜索错误
grep -r "错误\|Error" test-results/<时间戳>/

# 统计完成情况
grep -c "\[x\] 成功" test-results/<时间戳>/*.md
```

## 测试文件结构

每个测试文件包含：

```markdown
# Skill 测试报告

## 测试信息
- 测试编号、时间、提示词

## 使用说明
- 如何在 Kiro 中测试

## 测试结果
- [ ] 执行状态（成功/失败/部分成功）
- [ ] 数据可用性
- [ ] 输出质量
- 发现的问题
- 备注
```

## 记录测试结果的示例

假设你测试了"帮我分析一下最近的大宗交易情况"，在测试文件中记录：

```markdown
## 测试结果

### 执行状态
- [x] 成功
- [ ] 失败
- [ ] 部分成功

### Kiro 输出
```
# 大宗交易监控分析报告

## 0) 数据口径与时间
- 数据范围：全A股市场
- 时间窗口：2026-02-14 至 2026-02-21
...
（完整输出）
```

### 发现的问题

#### 数据可用性
- [x] 数据完整
- [ ] 数据部分缺失
- [ ] 数据完全不可用

#### 错误信息
```
无错误
```

#### 输出质量
- [x] 输出格式符合模板要求
- [x] 分析逻辑正确
- [x] 建议具体可执行
- [x] 风险提示完整

### 需要改进的地方
1. 无

### 备注
测试通过，输出质量良好。
```

## 常见问题

### Q1: 如何快速查看所有提示词？

```bash
cd test-results/<时间戳>/
cat .prompt_*.txt
```

### Q2: 如何只测试某几个用例？

编辑 `auto_test_skills.py`，修改 `TEST_CASES` 列表：

```python
TEST_CASES = [
    "帮我分析一下最近的大宗交易情况",
    "给我做一个龙虎榜分析",
    # 注释掉不需要的测试
]
```

### Q3: 如何添加自定义测试用例？

编辑 `auto_test_skills.py`，在 `TEST_CASES` 列表中添加：

```python
TEST_CASES = [
    # ... 现有测试用例 ...
    "你的自定义测试用例1",
    "你的自定义测试用例2",
]
```

### Q4: 测试结果保存在哪里？

所有测试结果保存在 `test-results/<时间戳>/` 目录中，每次运行脚本会创建新的时间戳目录。

### Q5: 如何对比不同时间的测试结果？

```bash
# 列出所有测试会话
ls -lt test-results/

# 对比两次测试的某个用例
diff test-results/20260221_103348/01_*.md test-results/20260221_143022/01_*.md
```

## 测试检查清单

对每个测试，请检查：

- [ ] **数据可用性**：数据是否完整？是否有缺失？
- [ ] **输出格式**：是否符合 output-template.md？
- [ ] **方法论应用**：是否应用了 methodology.md 中的规则？
- [ ] **分析逻辑**：计算是否正确？判断是否合理？
- [ ] **风险提示**：是否有 A股特性提示？边界条件说明？
- [ ] **改进建议**：建议是否具体？是否可执行？
- [ ] **错误处理**：是否有明显错误？错误信息是否清晰？

## 问题分类

### 数据问题（P0 - 最高优先级）
- 数据接口不可用
- 数据返回为空
- 数据格式错误

### 分析问题（P1 - 高优先级）
- 未应用方法论
- 阈值判断错误
- 缺少风险提示

### 格式问题（P2 - 中优先级）
- 未按模板输出
- 缺少必要章节
- 表格格式错误

### 优化问题（P3 - 低优先级）
- 建议不够具体
- 可以增加更多分析维度

## 工作流程建议

```bash
# 1. 生成测试文件
python3 auto_test_skills.py

# 2. 记录最新的测试目录
LATEST=$(ls -t test-results/ | head -1)
echo "测试目录: test-results/$LATEST"

# 3. 查看汇总报告
cat test-results/$LATEST/00_SUMMARY.md

# 4. 逐个测试（在 Kiro 中）
# 测试 1
cat test-results/$LATEST/.prompt_01.txt
# 在 Kiro 中运行，记录结果

# 测试 2
cat test-results/$LATEST/.prompt_02.txt
# 在 Kiro 中运行，记录结果

# ... 继续其他测试 ...

# 5. 分析问题
grep -r "数据.*缺失" test-results/$LATEST/
grep -r "\[x\] 失败" test-results/$LATEST/

# 6. 生成问题清单
grep -l "数据.*缺失" test-results/$LATEST/*.md > issues.txt
cat issues.txt

# 7. 修复问题后重新测试
python3 auto_test_skills.py
# 重复步骤 4-6
```

## 批量操作技巧

### 快速查看所有提示词

```bash
cd test-results/<时间戳>/
for f in .prompt_*.txt; do
    echo "=== $f ==="
    cat "$f"
    echo ""
done
```

### 提取所有未完成的测试

```bash
cd test-results/<时间戳>/
grep -L "\[x\]" *.md | grep -v "00_SUMMARY"
```

### 统计测试结果

```bash
cd test-results/<时间戳>/
echo "成功: $(grep -c '\[x\] 成功' *.md)"
echo "失败: $(grep -c '\[x\] 失败' *.md)"
echo "部分成功: $(grep -c '\[x\] 部分成功' *.md)"
```

## 相关文档

- [BATCH_TEST_GUIDE.md](BATCH_TEST_GUIDE.md) - 详细的批量测试指南
- [SKILLS_MAP.md](SKILLS_MAP.md) - Skills 完整索引
- [HOW_TO_USE_SKILLS.md](HOW_TO_USE_SKILLS.md) - Skills 使用指南
- [SKILLS_VS_DATA.md](SKILLS_VS_DATA.md) - Skills vs 数据脚本区别

---

最后更新：2026-02-21
