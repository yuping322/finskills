# Skills 测试工具集

本目录包含多个测试工具，帮助你系统地测试和验证 107 个 Market Analysis Skills。

## 工具概览

| 工具 | 用途 | 推荐度 | 使用场景 |
|------|------|--------|---------|
| `auto_test_skills.py` | 生成测试模板 | ⭐⭐⭐⭐⭐ | 系统化测试所有 Skills |
| `batch_test_skills.sh` | 批量测试脚本 | ⭐⭐⭐ | 生成测试框架 |
| `test_skills.sh` | 数据工具包测试 | ⭐⭐⭐⭐ | 验证数据接口 |

## 快速开始（推荐）

### 1. 测试数据工具包

首先确保数据工具包正常工作：

```bash
./test_skills.sh
```

**预期输出**：
- ✅ 列出可用 views
- ✅ 搜索功能正常
- ✅ 参数说明正常
- ✅ 执行计划正常

### 2. 生成 Skills 测试模板

```bash
python3 auto_test_skills.py
```

**输出**：
- `test-results/<时间戳>/` 目录
- 10 个测试模板文件
- 10 个提示词文件
- 1 个汇总报告

### 3. 在 Kiro 中测试

```bash
# 查看第一个测试的提示词
cat test-results/<时间戳>/.prompt_01.txt

# 在 Kiro 中运行这个提示词
# 将输出记录到 test-results/<时间戳>/01_*.md
```

### 4. 分析结果

```bash
# 查看汇总报告
cat test-results/<时间戳>/00_SUMMARY.md

# 搜索问题
grep -r "数据.*缺失\|错误" test-results/<时间戳>/
```

## 详细文档

### 核心文档
- **[QUICK_TEST_GUIDE.md](QUICK_TEST_GUIDE.md)** - 快速测试指南（3 步开始）⭐ 推荐阅读
- **[BATCH_TEST_GUIDE.md](BATCH_TEST_GUIDE.md)** - 批量测试详细指南
- **[SKILLS_VS_DATA.md](SKILLS_VS_DATA.md)** - Skills vs 数据脚本区别 ⭐ 重要概念

### Skills 使用文档
- **[SKILLS_MAP.md](SKILLS_MAP.md)** - 107 个 Skills 完整索引
- **[HOW_TO_USE_SKILLS.md](HOW_TO_USE_SKILLS.md)** - Skills 使用指南
- **[QUICK_START.md](QUICK_START.md)** - 快速开始

### 环境配置
- **[SETUP_COMPLETE.md](SETUP_COMPLETE.md)** - 环境配置完成说明
- `setup_skills_env.sh` - 环境配置脚本

## 工具详解

### 1. auto_test_skills.py（推荐）

**用途**：生成结构化的测试模板，方便在 Kiro 中逐个测试并记录结果。

**优点**：
- ✅ 生成标准化的测试模板
- ✅ 包含完整的检查清单
- ✅ 便于记录和分析结果
- ✅ 支持自定义测试用例

**使用方法**：
```bash
# 生成测试模板
python3 auto_test_skills.py

# 查看输出
ls -lh test-results/<时间戳>/

# 开始测试
cat test-results/<时间戳>/.prompt_01.txt
# 在 Kiro 中运行，记录结果
```

**自定义测试用例**：
编辑 `auto_test_skills.py`，修改 `TEST_CASES` 列表。

### 2. batch_test_skills.sh

**用途**：批量生成测试框架。

**优点**：
- ✅ 快速生成测试结构
- ✅ 自动创建目录和文件

**使用方法**：
```bash
./batch_test_skills.sh
```

### 3. test_skills.sh

**用途**：测试底层数据工具包（不是 Skills）。

**重要**：这个脚本测试的是数据脚本，不是完整的 Skills！

**使用方法**：
```bash
./test_skills.sh
```

**输出**：原始 JSON 数据（不包含分析、建议等）

详见：[SKILLS_VS_DATA.md](SKILLS_VS_DATA.md)

## 测试流程

### 完整测试流程

```
1. 环境准备
   └─> ./setup_skills_env.sh

2. 验证数据工具包
   └─> ./test_skills.sh

3. 生成测试模板
   └─> python3 auto_test_skills.py

4. 在 Kiro 中测试
   ├─> 复制提示词
   ├─> 在 Kiro 中运行
   └─> 记录结果到测试文件

5. 分析结果
   ├─> 查看汇总报告
   ├─> 搜索问题
   └─> 生成问题清单

6. 修复问题
   └─> 更新 Skills 文档或代码

7. 重新测试
   └─> 重复步骤 3-5
```

### 快速测试流程（单个 Skill）

```bash
# 1. 在 Kiro 中直接提问
"帮我分析一下最近的大宗交易情况"

# 2. 检查输出质量
- 数据是否完整？
- 格式是否正确？
- 分析是否合理？
- 建议是否可执行？

# 3. 记录问题（如有）
echo "大宗交易分析：数据缺失 - 折溢价率" >> issues.txt
```

## 测试用例列表

默认包含 10 个测试用例：

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

**覆盖的 Skill 类型**：
- 风险监控（ST退市、股权质押、IPO解禁）
- 市场分析（龙虎榜、大宗交易、北向资金、涨跌停）
- 投资组合（市场宽度）
- 研究工具（概念板块、市场简报）

## 常见问题

### Q1: 应该先运行哪个脚本？

**推荐顺序**：
1. `./test_skills.sh` - 验证数据工具包
2. `python3 auto_test_skills.py` - 生成测试模板
3. 在 Kiro 中逐个测试

### Q2: 测试结果保存在哪里？

所有测试结果保存在 `test-results/<时间戳>/` 目录中。

### Q3: 如何添加更多测试用例？

编辑 `auto_test_skills.py`，在 `TEST_CASES` 列表中添加。

### Q4: 如何自动化测试？

目前需要手动在 Kiro 中测试，因为：
- Kiro CLI 不支持直接运行对话
- 需要人工判断输出质量
- 需要记录详细的问题

### Q5: 测试失败了怎么办？

1. 检查数据工具包是否正常（`./test_skills.sh`）
2. 查看错误信息
3. 检查 Skill 文档是否完整
4. 在测试文件中记录问题
5. 修复后重新测试

## 测试检查清单

对每个测试，请检查：

### 数据层面
- [ ] 数据接口是否可用？
- [ ] 数据是否完整？
- [ ] 数据格式是否正确？

### 分析层面
- [ ] 是否应用了 methodology.md 中的规则？
- [ ] 计算是否正确？
- [ ] 阈值判断是否合理？

### 输出层面
- [ ] 是否符合 output-template.md？
- [ ] 是否有风险提示？
- [ ] 建议是否具体可执行？

### 错误处理
- [ ] 是否有明显错误？
- [ ] 错误信息是否清晰？
- [ ] 边界条件是否处理？

## 问题优先级

### P0 - 阻塞性问题（立即修复）
- 数据接口完全不可用
- 程序崩溃或报错
- 输出完全错误

### P1 - 严重问题（尽快修复）
- 数据部分缺失
- 分析逻辑错误
- 缺少关键章节

### P2 - 一般问题（计划修复）
- 格式不完全符合模板
- 建议不够具体
- 缺少部分风险提示

### P3 - 优化建议（可选）
- 可以增加更多分析维度
- 可以优化输出格式
- 可以增加更多示例

## 下一步

1. ✅ 阅读 [QUICK_TEST_GUIDE.md](QUICK_TEST_GUIDE.md)
2. ✅ 运行 `python3 auto_test_skills.py` 生成测试模板
3. ✅ 在 Kiro 中逐个测试
4. ✅ 记录结果和问题
5. ✅ 分析问题并修复
6. ✅ 重新测试验证

## 相关资源

### 文档
- [SKILLS_MAP.md](SKILLS_MAP.md) - Skills 索引
- [HOW_TO_USE_SKILLS.md](HOW_TO_USE_SKILLS.md) - 使用指南
- [SKILLS_VS_DATA.md](SKILLS_VS_DATA.md) - 概念区分

### 脚本
- `auto_test_skills.py` - 测试模板生成器
- `batch_test_skills.sh` - 批量测试脚本
- `test_skills.sh` - 数据工具包测试
- `setup_skills_env.sh` - 环境配置

### 配置
- `.kiro/steering/market-analysis-skills.md` - Kiro 自动加载配置

---

**开始测试**：`python3 auto_test_skills.py`

**获取帮助**：查看 [QUICK_TEST_GUIDE.md](QUICK_TEST_GUIDE.md)

最后更新：2026-02-21
