# P1问题2：备用数据源MVP实施计划

## MVP范围

鉴于完整实现需要较长时间，我们先实现一个MVP版本，专注于：

1. **单一核心工具**：stock_zh_a_spot_em（实时行情）
2. **单一备用源**：腾讯财经API（已有部分代码）
3. **基础切换机制**：主数据源失败时自动切换
4. **简单监控**：记录切换日志

## MVP实施步骤

### 步骤1：完善腾讯数据源实现（已有基础）

当前provider_akshare.py已经有腾讯数据源的部分实现，需要：
- ✅ 完善_parse_tx_quote_payload函数
- ✅ 添加批量查询支持
- ✅ 统一数据格式（与AKShare保持一致）

### 步骤2：实现简单的fallback机制

在provider_akshare.py中添加：
```python
def _fetch_with_tencent_fallback(tool_name: str, **kwargs):
    """带腾讯数据源fallback的获取函数"""
    try:
        # 尝试AKShare
        return _fetch_from_akshare(tool_name, **kwargs)
    except Exception as e:
        # 记录失败
        logger.warning(f"AKShare failed for {tool_name}: {e}")
        
        # 尝试腾讯数据源
        if tool_name == "stock_zh_a_spot_em":
            try:
                return _fetch_from_tencent_realtime(**kwargs)
            except Exception as e2:
                logger.error(f"Tencent fallback also failed: {e2}")
                raise
        else:
            raise  # 其他工具暂不支持fallback
```

### 步骤3：添加切换日志

```python
# 记录数据源切换
def _log_source_switch(tool_name: str, from_source: str, to_source: str, reason: str):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "tool": tool_name,
        "from": from_source,
        "to": to_source,
        "reason": reason
    }
    # 写入日志文件
    with open("backup_source_switches.log", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
```

### 步骤4：测试验证

- ✅ 测试AKShare正常时使用AKShare
- ✅ 测试AKShare失败时切换到腾讯
- ✅ 测试数据格式一致性
- ✅ 测试切换日志记录

## MVP时间表

- **Day 1**：完善腾讯数据源实现（2-3小时）
- **Day 2**：实现fallback机制（2-3小时）
- **Day 3**：测试和文档（2-3小时）

**总计**：6-9小时（约1-1.5个工作日）

## MVP成功标准

1. ✅ stock_zh_a_spot_em在AKShare失败时能自动切换到腾讯数据源
2. ✅ 数据格式与AKShare保持一致
3. ✅ 切换过程有日志记录
4. ✅ 对上层skills透明（无需修改代码）

## 后续扩展

MVP完成后，可以逐步扩展：
1. 添加更多工具的备用数据源
2. 添加更多备用数据源（新浪、网易等）
3. 实现完整的DataSourceManager
4. 添加配置文件支持
5. 添加CLI监控工具

## 当前决策

考虑到：
1. P1-2是一个较大的工程，完整实现需要1-2周
2. P1-3（阈值回测验证）也是重要的P1问题
3. 用户可能更关心快速看到进展

**建议**：
- **选项A**：先完成P1-2的MVP（1-1.5天），然后继续P1-3
- **选项B**：先完成P1-3（相对独立，3-5天），再回来完成P1-2完整版
- **选项C**：询问用户优先级，由用户决定

**我的建议**：选项B - 先完成P1-3，因为：
1. P1-3相对独立，不依赖P1-2
2. P1-3的阈值验证对methodology文档的完善很重要
3. P1-2的MVP虽然快，但功能有限，不如等有时间做完整版
4. P1-1（健康检查）已经在一定程度上缓解了数据源不稳定的问题

## 用户确认

请用户确认优先级：
1. 继续P1-2（备用数据源）- MVP版本（1-1.5天）
2. 继续P1-2（备用数据源）- 完整版本（1-2周）
3. 转向P1-3（阈值回测验证）（3-5天）
4. 其他优先级调整
