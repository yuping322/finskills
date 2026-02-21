#!/usr/bin/env python3
"""
Skills 自动化测试脚本

通过创建临时对话文件的方式，让 Kiro 自动执行测试用例。
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path

# 测试用例列表
TEST_CASES = [
    "帮我分析一下最近的大宗交易情况",
    "给我做一个龙虎榜分析",
    "分析一下最近北向资金的流向",
    "检查一下有哪些股票有ST退市风险",
    "帮我监控一下股权质押风险",
    "分析一下最近的涨跌停板情况",
    "给我做一个概念板块分析",
    "分析一下最近的IPO解禁风险",
    "帮我做一个市场宽度监控",
    "生成一份周度市场简报",
]

def create_test_session():
    """创建测试会话目录"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("test-results") / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def sanitize_filename(text, max_length=50):
    """生成安全的文件名"""
    # 保留中文、英文、数字
    safe_chars = []
    for char in text:
        if char.isalnum() or '\u4e00' <= char <= '\u9fff':
            safe_chars.append(char)
        else:
            safe_chars.append('_')
    
    filename = ''.join(safe_chars)[:max_length]
    return filename

def create_test_template(output_dir, index, total, prompt):
    """创建测试模板文件"""
    safe_name = sanitize_filename(prompt)
    output_file = output_dir / f"{index:02d}_{safe_name}.md"
    prompt_file = output_dir / f".prompt_{index:02d}.txt"
    
    # 保存提示词到文件
    prompt_file.write_text(prompt, encoding='utf-8')
    
    # 创建测试模板
    template = f"""# Skill 测试报告

## 测试信息
- **测试编号**: {index} / {total}
- **测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **提示词**: {prompt}

---

## 使用说明

### 方法 1：在 Kiro 中手动测试
1. 打开 Kiro
2. 复制下面的提示词
3. 粘贴到 Kiro 对话框
4. 将输出结果粘贴到本文件的"测试结果"部分

**提示词**：
```
{prompt}
```

### 方法 2：使用提示词文件
提示词已保存到：`{prompt_file.name}`

---

## 测试结果

### 执行状态
- [ ] 成功
- [ ] 失败
- [ ] 部分成功

### Kiro 输出
```
（请在此处粘贴 Kiro 的完整输出）
```

### 发现的问题

#### 数据可用性
- [ ] 数据完整
- [ ] 数据部分缺失（请说明哪些数据缺失）
- [ ] 数据完全不可用

#### 错误信息
```
（如有错误，请在此处粘贴）
```

#### 输出质量
- [ ] 输出格式符合模板要求
- [ ] 分析逻辑正确
- [ ] 建议具体可执行
- [ ] 风险提示完整

### 需要改进的地方
1. 
2. 
3. 

### 备注


---

**测试完成后，请在上方勾选相应的复选框并填写详细信息。**
"""
    
    output_file.write_text(template, encoding='utf-8')
    return output_file, prompt_file

def create_summary(output_dir, test_files):
    """创建汇总报告"""
    summary_file = output_dir / "00_SUMMARY.md"
    
    summary = f"""# Skills 批量测试汇总报告

## 测试概况
- **测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **测试总数**: {len(test_files)}
- **输出目录**: `{output_dir}`

## 测试用例列表

"""
    
    for i, (output_file, prompt_file, prompt) in enumerate(test_files, 1):
        summary += f"{i}. **{prompt}**\n"
        summary += f"   - 测试文件: [`{output_file.name}`](./{output_file.name})\n"
        summary += f"   - 提示词文件: [`{prompt_file.name}`](./{prompt_file.name})\n"
        summary += "\n"
    
    summary += """
## 使用说明

### 1. 执行测试

**推荐方式**：在 Kiro 中逐个测试
1. 打开每个测试文件（`01_*.md`, `02_*.md`, ...）
2. 复制其中的提示词
3. 在 Kiro 中运行
4. 将结果粘贴回测试文件

**批量方式**：使用提示词文件
1. 在 Kiro 中打开工作区
2. 依次将提示词文件（`.prompt_*.txt`）的内容发送给 Kiro
3. 记录每次的输出结果

### 2. 记录结果

在每个测试文件中：
- 勾选执行状态
- 粘贴 Kiro 的完整输出
- 记录发现的问题
- 评估输出质量

### 3. 分析问题

**搜索数据缺失问题**：
```bash
grep -r "数据部分缺失\|数据完全不可用" {output_dir}/
```

**搜索错误**：
```bash
grep -r "错误\|Error\|失败" {output_dir}/
```

**统计完成情况**：
```bash
grep -c "\\[x\\] 成功" {output_dir}/*.md
```

### 4. 生成问题清单

```bash
# 提取所有标记为"数据缺失"的测试
grep -l "\\[x\\] 数据.*缺失" {output_dir}/*.md

# 提取所有失败的测试
grep -l "\\[x\\] 失败" {output_dir}/*.md
```

## 测试检查清单

对每个测试，请检查：

- [ ] 数据是否可用？
- [ ] 输出格式是否符合模板？
- [ ] 分析逻辑是否正确？
- [ ] 是否有风险提示？
- [ ] 建议是否具体可执行？
- [ ] 是否有明显错误？

## 常见问题类型

### 数据问题
- 数据接口不可用
- 数据返回为空
- 周末/节假日无数据
- 数据格式错误

### 分析问题
- 未应用方法论
- 阈值判断错误
- 缺少风险提示
- 建议不具体

### 格式问题
- 未按模板输出
- 缺少必要章节
- 表格格式错误

## 下一步

1. ✅ 完成所有测试用例
2. ✅ 记录每个测试的结果
3. ✅ 汇总发现的问题
4. ✅ 优先修复高频问题
5. ✅ 重新测试验证修复

## 相关文档

- [SKILLS_MAP.md](../../SKILLS_MAP.md) - Skills 完整索引
- [HOW_TO_USE_SKILLS.md](../../HOW_TO_USE_SKILLS.md) - Skills 使用指南
- [SKILLS_VS_DATA.md](../../SKILLS_VS_DATA.md) - Skills vs 数据脚本区别
- [BATCH_TEST_GUIDE.md](../../BATCH_TEST_GUIDE.md) - 批量测试详细指南

---

**测试完成后，请更新此汇总报告，添加整体结论和改进计划。**
"""
    
    summary_file.write_text(summary, encoding='utf-8')
    return summary_file

def main():
    """主函数"""
    print("=== Kiro Skills 批量测试 ===")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 创建测试会话
    output_dir = create_test_session()
    print(f"输出目录: {output_dir}")
    print()
    
    # 生成测试文件
    test_files = []
    total = len(TEST_CASES)
    
    for i, prompt in enumerate(TEST_CASES, 1):
        print(f"[{i}/{total}] 创建测试: {prompt}")
        output_file, prompt_file = create_test_template(output_dir, i, total, prompt)
        test_files.append((output_file, prompt_file, prompt))
        print(f"  ✅ {output_file.name}")
    
    print()
    
    # 生成汇总报告
    print("生成汇总报告...")
    summary_file = create_summary(output_dir, test_files)
    print(f"  ✅ {summary_file.name}")
    print()
    
    # 输出使用说明
    print("=== 测试文件已创建 ===")
    print()
    print("下一步：")
    print(f"  1. 查看汇总报告: cat {summary_file}")
    print(f"  2. 在 Kiro 中逐个测试提示词")
    print(f"  3. 将结果记录到对应的测试文件中")
    print()
    print("快速开始：")
    print(f"  cat {output_dir}/01_*.md")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
