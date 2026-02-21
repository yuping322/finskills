# Skills 快速开始指南

## 一、环境设置（首次使用）

### 1. 自动设置（推荐）

```bash
./setup_skills_env.sh
```

这会自动完成所有设置。

### 2. 手动设置

```bash
# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境（macOS/Linux）
source .venv/bin/activate

# 安装依赖
pip install -r China-market/findata-toolkit-cn/requirements.txt
```

## 二、使用 Skills

### ⚠️ 重要概念区分

**Skill ≠ 数据脚本**

- **Skill（完整体验）** = 大模型 + 数据获取 + 方法论 + 分析框架 + 结构化输出
- **数据脚本（底层工具）** = 仅获取原始数据，无分析无建议

### 方式 1：在 Kiro 对话中使用（✅ 推荐 - 完整 Skill）

直接在 Kiro 中提问，大模型会：
1. 读取 skill 文档（SKILL.md, methodology.md）
2. 获取所需数据
3. 应用分析框架和方法论
4. 生成结构化的分析报告
5. 提供可执行的建议

```
你：帮我分析一下最近的大宗交易情况
你：检查一下有哪些股票有ST退市风险
你：分析一下南向资金最近的流向
```

**这才是真正的 Skill 使用方式！**

### 方式 2：直接运行数据脚本（⚙️ 高级用户 - 仅数据层）

如果你只需要原始数据（不需要分析），可以直接运行：

```bash
# 查看可用的数据 views
.venv/bin/python3 China-market/findata-toolkit-cn/scripts/views_runner.py list

# 查看参数说明
.venv/bin/python3 China-market/findata-toolkit-cn/scripts/views_runner.py describe block_deal_dashboard

# 获取原始数据（JSON格式）
.venv/bin/python3 China-market/findata-toolkit-cn/scripts/views_runner.py block_deal_dashboard --set start_date=20260214 --set end_date=20260221
```

**注意**：这只会返回原始 JSON 数据，没有：
- ❌ 分析和解读
- ❌ 风险提示
- ❌ 改进建议
- ❌ 结构化报告

**适用场景**：
- 你想自己分析数据
- 你要导出数据到其他工具
- 你在开发或调试

## 三、常用命令速查

### A股市场

```bash
# 列出所有可用的 views
.venv/bin/python3 China-market/findata-toolkit-cn/scripts/views_runner.py list

# 搜索特定关键词的 views
.venv/bin/python3 China-market/findata-toolkit-cn/scripts/views_runner.py list --contains 大宗

# 查看 view 的参数说明
.venv/bin/python3 China-market/findata-toolkit-cn/scripts/views_runner.py describe <view_name>

# 只看执行计划（不实际获取数据）
.venv/bin/python3 China-market/findata-toolkit-cn/scripts/views_runner.py <view_name> --dry-run
```

### 常用 Views

| View 名称 | 用途 | 示例命令 |
|----------|------|---------|
| `block_deal_dashboard` | 大宗交易分析 | `.venv/bin/python3 China-market/findata-toolkit-cn/scripts/views_runner.py block_deal_dashboard` |
| `stock_zh_a_spot_em` | A股实时行情 | `.venv/bin/python3 China-market/findata-toolkit-cn/scripts/views_runner.py stock_zh_a_spot_em` |
| `stock_zh_a_hist` | A股历史K线 | `.venv/bin/python3 China-market/findata-toolkit-cn/scripts/views_runner.py stock_zh_a_hist --set symbol=000001` |
| `fund_flow_dashboard` | 资金流监控 | `.venv/bin/python3 China-market/findata-toolkit-cn/scripts/views_runner.py fund_flow_dashboard` |

## 四、创建便捷别名（可选）

在 `~/.zshrc` 或 `~/.bashrc` 中添加：

```bash
# Skills 快捷命令
alias skills-py='.venv/bin/python3'
alias skills-view='skills-py China-market/findata-toolkit-cn/scripts/views_runner.py'
alias skills-list='skills-view list'
```

然后就可以使用：

```bash
skills-list
skills-view describe block_deal_dashboard
skills-view block_deal_dashboard
```

## 五、故障排查

### 问题 1：找不到 python3

**解决方案**：
```bash
# 检查 Python 版本
python3 --version

# 如果没有 python3，安装 Python 3.9+
# macOS: brew install python@3.9
# Ubuntu: sudo apt install python3.9
```

### 问题 2：虚拟环境激活失败

**解决方案**：
```bash
# 不需要激活虚拟环境，直接使用虚拟环境的 Python
.venv/bin/python3 <script>
```

### 问题 3：数据获取超时

**原因**：某些 views 需要抓取大量数据（如全市场行情）

**解决方案**：
- 使用更具体的参数缩小范围
- 使用 `--dry-run` 先查看执行计划
- 耐心等待（首次获取会较慢，后续有缓存）

### 问题 4：SSL 警告

**现象**：
```
NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+
```

**说明**：这是警告不是错误，不影响使用。如果想消除警告：
```bash
pip install 'urllib3<2.0'
```

### 问题 5：数据接口返回错误

**原因**：
- 数据源网站可能临时不可用
- 参数格式不正确
- 网络连接问题

**解决方案**：
- 检查参数格式（使用 `describe` 查看）
- 稍后重试
- 查看错误信息中的 `errors` 字段

## 六、进阶使用

### 使用缓存

```bash
# 设置缓存目录
export FINSKILLS_CACHE_DIR=/tmp/finskills-cache

# 强制刷新缓存
.venv/bin/python3 China-market/findata-toolkit-cn/scripts/views_runner.py <view_name> --refresh

# 禁用缓存
.venv/bin/python3 China-market/findata-toolkit-cn/scripts/views_runner.py <view_name> --no-cache
```

### 远程 API 模式

如果你有部署的 View API 服务：

```bash
# 设置远程 API URL
export FINSKILLS_VIEW_API_URL=http://127.0.0.1:8808

# 或者在命令中指定
.venv/bin/python3 China-market/findata-toolkit-cn/scripts/views_runner.py --remote-url http://127.0.0.1:8808 list
```

## 七、更多资源

- **完整 Skills 索引**：查看 `SKILLS_MAP.md`
- **详细使用说明**：查看 `HOW_TO_USE_SKILLS.md`
- **Skill 文档**：查看各 skill 目录下的 `SKILL.md`
- **方法论**：查看各 skill 的 `references/methodology.md`
- **数据获取**：查看各 skill 的 `references/data-queries.md`

## 八、获取帮助

在 Kiro 中直接问：
- "如何使用大宗交易监控 skill？"
- "有哪些风险监控类的 skills？"
- "帮我查看 block_deal_dashboard 的参数说明"
