# Skills 测试快速参考卡片

## 🚀 一分钟开始

```bash
# 1. 生成测试模板
python3 auto_test_skills.py

# 2. 查看第一个提示词
cat test-results/$(ls -t test-results/ | head -1)/.prompt_01.txt

# 3. 在 Kiro 中运行这个提示词

# 4. 记录结果
# 编辑 test-results/<时间戳>/01_*.md
```

## 📁 文件速查

| 文件 | 用途 | 命令 |
|------|------|------|
| `auto_test_skills.py` | 生成测试模板 | `python3 auto_test_skills.py` |
| `test_skills.sh` | 测试数据工具包 | `./test_skills.sh` |
| `QUICK_TEST_GUIDE.md` | 详细测试指南 | `cat QUICK_TEST_GUIDE.md` |
| `SKILLS_VS_DATA.md` | 概念区分 | `cat SKILLS_VS_DATA.md` |

## 🔍 常用命令

### 查看测试结果

```bash
# 最新测试目录
LATEST=$(ls -t test-results/ | head -1)

# 查看汇总报告
cat test-results/$LATEST/00_SUMMARY.md

# 查看第一个测试
cat test-results/$LATEST/01_*.md

# 查看所有提示词
cat test-results/$LATEST/.prompt_*.txt
```

### 搜索问题

```bash
# 进入最新测试目录
cd test-results/$(ls -t test-results/ | head -1)

# 搜索数据问题
grep -r "数据.*缺失\|数据.*不可用" .

# 搜索错误
grep -r "错误\|Error\|失败" .

# 统计完成情况
grep -c "\[x\] 成功" *.md
```

### 生成问题清单

```bash
cd test-results/$(ls -t test-results/ | head -1)

# 数据缺失的测试
grep -l "数据.*缺失" *.md > data_issues.txt

# 失败的测试
grep -l "\[x\] 失败" *.md > failed_tests.txt

# 查看清单
cat data_issues.txt
```

## ✅ 测试检查清单

每个测试需要检查：

- [ ] 数据是否完整？
- [ ] 输出格式是否正确？
- [ ] 分析逻辑是否合理？
- [ ] 是否有风险提示？
- [ ] 建议是否可执行？
- [ ] 是否有明显错误？

## 📊 默认测试用例

1. 大宗交易分析
2. 龙虎榜分析
3. 北向资金流向
4. ST退市风险
5. 股权质押风险
6. 涨跌停板分析
7. 概念板块分析
8. IPO解禁风险
9. 市场宽度监控
10. 周度市场简报

## 🎯 测试流程

```
生成模板 → 查看提示词 → Kiro中测试 → 记录结果 → 分析问题
```

## 💡 快速技巧

### 快速查看最新测试

```bash
# 设置别名
alias latest='cd test-results/$(ls -t test-results/ | head -1)'

# 使用
latest
ls -lh
```

### 批量查看提示词

```bash
cd test-results/$(ls -t test-results/ | head -1)
for f in .prompt_*.txt; do
    echo "=== $f ==="
    cat "$f"
    echo ""
done
```

### 对比两次测试

```bash
# 列出所有测试
ls -lt test-results/

# 对比
diff test-results/<旧时间戳>/01_*.md \
     test-results/<新时间戳>/01_*.md
```

## 🆘 遇到问题？

| 问题 | 解决方案 |
|------|---------|
| 找不到 python3 | 检查 Python 安装：`which python3` |
| 测试目录太多 | 删除旧测试：`rm -rf test-results/202602*` |
| 不知道如何记录 | 查看示例：`cat test-results/<时间戳>/01_*.md` |
| 概念不清楚 | 阅读：`cat SKILLS_VS_DATA.md` |

## 📖 详细文档

- [QUICK_TEST_GUIDE.md](QUICK_TEST_GUIDE.md) - 3步开始
- [TEST_TOOLS_README.md](TEST_TOOLS_README.md) - 工具概览
- [BATCH_TEST_GUIDE.md](BATCH_TEST_GUIDE.md) - 详细指南
- [TESTING_SUMMARY.md](TESTING_SUMMARY.md) - 完成总结

## 🎉 开始测试

```bash
python3 auto_test_skills.py
```

---

**提示**：将此文件保存为书签，方便随时查阅！

最后更新：2026-02-21
