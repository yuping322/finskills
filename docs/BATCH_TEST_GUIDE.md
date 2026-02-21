# Skills 批量测试指南

## 概述

`batch_test_skills.sh` 脚本可以批量运行多个 Skill 测试用例，并将每个测试的完整输出（包括大模型的中间过程）保存到独立的文件中。

## 使用方法

### 1. 基础使用

直接运行脚本：

```bash
./batch_test_skills.sh
```

脚本会：
- 创建 `test-results/<时间戳>/` 目录
- 依次运行所有测试用例
- 将每个测试的完整输出保存到独立的 `.md` 文件
- 生成汇总报告 `00_SUMMARY.md`

### 2. 查看结果

**查看汇总报告**：
```bash
cat test-results/<时间戳>/00_SUMMARY.md
```

**查看单个测试结果**：
```bash
cat test-results/<时间戳>/1_*.md
```

**查看所有测试文件**：
```bash
ls -lh test-results/<时间戳>/
```

### 3. 搜索问题

**搜索错误**：
```bash
grep -r "错误\|失败\|Error\|Failed" test-results/<时间戳>/
```

**搜索数据缺失问题**：
```bash
grep -r "数据不可用\|接口返回为空\|暂无数据\|weekend" test-results/<时间戳>/
```

**搜索特定 Skill**：
```bash
grep -r "block-deal-monitor\|龙虎榜" test-results/<时间戳>/
```

## 默认测试用例

脚本包含 10 个测试用例：

1. 帮我分析一下最近的大宗交易情况
2. 给我做一个龙虎榜分析
3. 分析一下最近北向资金的流向
4. 检查一下有哪些股票有ST退市风险
5. 帮我监控一下股权质押风险
6. 分析一下最近的涨跌停板情况
7. 给我做一个概念板块分析
8. 分析一下最近的IPO解禁风险
9. 帮我做一个市场宽度监控
10. 生成一份周度市场简报

## 自定义测试用例

### 方法 1：编辑脚本

编辑 `batch_test_skills.sh`，修改 `TEST_CASES` 数组：

```bash
declare -a TEST_CASES=(
    "你的测试用例1"
    "你的测试用例2"
    "你的测试用例3"
)
```

### 方法 2：创建测试用例文件

创建 `test_cases.txt` 文件，每行一个测试用例：

```
帮我分析一下最近的大宗交易情况
给我做一个龙虎榜分析
分析一下最近北向资金的流向
```

然后修改脚本读取这个文件（需要修改脚本逻辑）。

### 方法 3：单独运行测试

使用 Kiro CLI 单独运行某个测试：

```bash
kiro chat "你的测试提示词" > output.md 2>&1
```

## 输出文件结构

```
test-results/
└── 20260221_143022/              # 时间戳目录
    ├── 00_SUMMARY.md             # 汇总报告
    ├── 1_帮我分析一下最近的大宗交易情况.md
    ├── 2_给我做一个龙虎榜分析.md
    ├── 3_分析一下最近北向资金的流向.md
    └── ...
```

每个测试文件包含：
- 测试信息（编号、时间、提示词）
- Kiro 的完整输出（包括中间过程）
- 执行状态（成功/失败）

## 常见问题

### Q1: Kiro CLI 命令不存在

**问题**：运行脚本时提示 `kiro: command not found`

**解决方案**：
1. 检查 Kiro 是否已安装
2. 检查 Kiro CLI 命令名称（可能是 `kiro-cli` 或其他）
3. 修改脚本中的命令名称

### Q2: 测试运行太慢

**问题**：10 个测试用例需要很长时间

**解决方案**：
1. 减少测试用例数量（编辑脚本）
2. 调整 `sleep 2` 的等待时间（但不要太短，避免请求过快）
3. 分批运行测试

### Q3: 输出文件乱码

**问题**：中文文件名显示乱码

**解决方案**：
1. 检查终端编码设置（应为 UTF-8）
2. 使用 `ls -lh` 查看文件列表
3. 文件内容应该正常（即使文件名乱码）

### Q4: 如何只运行失败的测试

**解决方案**：
1. 查看汇总报告，识别失败的测试
2. 手动运行失败的测试：
   ```bash
   kiro chat "失败的测试提示词" > retry.md 2>&1
   ```

## 高级用法

### 1. 并行运行测试（不推荐）

如果你想加快测试速度，可以并行运行：

```bash
# 警告：可能导致 API 限流或输出混乱
for prompt in "${TEST_CASES[@]}"; do
    kiro chat "$prompt" > "output_${RANDOM}.md" 2>&1 &
done
wait
```

### 2. 定时运行测试

使用 cron 定时运行测试：

```bash
# 每天早上 9 点运行测试
0 9 * * * cd /path/to/finskills && ./batch_test_skills.sh
```

### 3. 集成到 CI/CD

在 CI/CD 流程中运行测试：

```yaml
# .github/workflows/test-skills.yml
name: Test Skills
on:
  schedule:
    - cron: '0 9 * * *'  # 每天早上 9 点
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Skills Tests
        run: ./batch_test_skills.sh
      - name: Upload Results
        uses: actions/upload-artifact@v2
        with:
          name: test-results
          path: test-results/
```

## 分析测试结果

### 1. 统计成功率

```bash
cd test-results/<时间戳>/
grep -c "✅ 成功" *.md
grep -c "❌ 失败" *.md
```

### 2. 提取所有错误信息

```bash
cd test-results/<时间戳>/
grep -A 5 "错误\|Error" *.md > errors_summary.txt
```

### 3. 检查数据可用性

```bash
cd test-results/<时间戳>/
grep -c "数据不可用\|接口返回为空" *.md
```

### 4. 生成问题清单

```bash
cd test-results/<时间戳>/
grep -h "数据不可用\|接口返回为空\|错误" *.md | sort | uniq > issues.txt
```

## 最佳实践

1. **定期运行测试**：每周或每次更新 Skills 后运行
2. **保留测试历史**：不要删除旧的测试结果，便于对比
3. **记录问题**：发现问题后在 `issues.txt` 中记录
4. **逐步修复**：优先修复高频问题
5. **验证修复**：修复后重新运行测试验证

## 示例工作流

```bash
# 1. 运行批量测试
./batch_test_skills.sh

# 2. 查看汇总报告
cat test-results/$(ls -t test-results/ | head -1)/00_SUMMARY.md

# 3. 搜索错误
grep -r "错误\|Error" test-results/$(ls -t test-results/ | head -1)/

# 4. 查看具体失败的测试
cat test-results/$(ls -t test-results/ | head -1)/3_*.md

# 5. 修复问题后重新运行单个测试
kiro chat "分析一下最近北向资金的流向" > retry.md 2>&1

# 6. 对比结果
diff test-results/$(ls -t test-results/ | head -1)/3_*.md retry.md
```

## 相关文档

- [SKILLS_MAP.md](SKILLS_MAP.md) - Skills 完整索引
- [HOW_TO_USE_SKILLS.md](HOW_TO_USE_SKILLS.md) - Skills 使用指南
- [SKILLS_VS_DATA.md](SKILLS_VS_DATA.md) - Skills vs 数据脚本区别

---

最后更新：2026-02-21
