# AKShare健康检查机制

## 概述

AKShare健康检查机制为所有56个China-market skills提供了：
1. **健康检查**：定期检测AKShare接口是否可用
2. **错误统计**：记录每个工具的调用成功率和错误类型
3. **自动降级**：当连续失败达到阈值时自动触发降级模式
4. **增强重试**：智能重试机制，降级模式下减少重试次数

## 功能特性

### 1. 健康检查
- 使用轻量级接口（`stock_info_a_code_name`）定期检测AKShare连接性
- 默认每5分钟检查一次（可配置）
- 记录响应时间和错误信息

### 2. 错误统计
- 按工具名称统计调用次数、失败次数、成功率
- 记录连续失败次数
- 分类错误类型（timeout、network、data_missing等）
- 记录最后错误时间和信息

### 3. 自动降级
- 当连续失败达到阈值（默认5次）时触发降级模式
- 降级模式下：
  - 减少重试次数（减半）
  - 缩短重试等待时间
  - 添加额外的退避时间
- 成功调用后自动恢复正常模式

### 4. 增强重试
- 识别可重试的错误类型（timeout、connection、network等）
- 指数退避策略
- 降级模式下调整重试策略

## 环境变量配置

```bash
# 健康检查配置
export FINSKILLS_HEALTH_CHECK_ENABLED=1           # 启用健康检查（默认：1）
export FINSKILLS_HEALTH_CHECK_INTERVAL=300        # 健康检查间隔（秒，默认：300=5分钟）

# 降级配置
export FINSKILLS_DEGRADATION_THRESHOLD=5          # 触发降级的连续失败次数（默认：5）
export FINSKILLS_DEGRADATION_WINDOW=300           # 降级窗口时间（秒，默认：300=5分钟）

# 重试配置
export FINSKILLS_CALL_RETRIES=1                   # 最大重试次数（默认：1）
export FINSKILLS_CALL_RETRY_SLEEP=0.3             # 重试等待时间（秒，默认：0.3）
export FINSKILLS_DEFAULT_TIMEOUT=10               # 默认超时时间（秒，默认：10）
```

## 使用方法

### 1. 命令行工具

#### 执行健康检查
```bash
# 基本检查（使用缓存）
python -m view_service.health_check_cli check

# 强制检查（忽略缓存）
python -m view_service.health_check_cli check --force
```

输出示例：
```
正在执行AKShare健康检查...

健康状态: ✅ 健康
检查时间: 2026-02-16 15:30:45
响应时间: 0.523秒 (523.0ms)

详细信息:
  data_length: 5234
  response_time_ms: 523.0
```

#### 查看统计信息
```bash
# 查看全局统计
python -m view_service.health_check_cli stats

# 查看特定工具的统计
python -m view_service.health_check_cli stats --tool stock_zh_a_spot_em
```

输出示例：
```
全局统计:
总调用次数: 1523
失败次数: 12
成功率: 99.21%
连续失败次数: 0

最后错误时间: 2026-02-16 14:25:30
最后错误信息: Read timed out

工具统计 (共23个工具):
  stock_zh_a_spot_em: 456次调用, 3次失败 (99.3%成功)
  stock_zh_a_hist: 234次调用, 2次失败 (99.1%成功)
  stock_board_industry_spot_em: 123次调用, 1次失败 (99.2%成功)
  ...
```

#### 查看健康摘要
```bash
# 文本格式
python -m view_service.health_check_cli summary

# JSON格式
python -m view_service.health_check_cli summary --json
```

输出示例：
```
=== AKShare健康状态摘要 ===

健康状态: ✅ 健康
降级模式: ✅ 否
最后检查: 2026-02-16T15:30:45
响应时间: 0.523秒

全局统计:
  总调用: 1523
  失败: 12
  成功率: 99.21%
  连续失败: 0

最后错误:
  时间: 2026-02-16T14:25:30
  信息: Read timed out
```

#### 重置统计信息
```bash
# 重置所有统计
python -m view_service.health_check_cli reset

# 重置特定工具的统计
python -m view_service.health_check_cli reset --tool stock_zh_a_spot_em
```

### 2. Python API

```python
from view_service.akshare_health import (
    check_akshare_health,
    get_health_monitor,
    is_akshare_degraded,
    get_akshare_health_summary,
)

# 执行健康检查
result = check_akshare_health(force=False)
print(f"健康状态: {result.is_healthy}")
print(f"响应时间: {result.response_time}秒")

# 检查是否降级
if is_akshare_degraded():
    print("警告：AKShare处于降级模式")

# 获取健康监控器
monitor = get_health_monitor()

# 记录调用结果
monitor.record_call("stock_zh_a_spot_em", success=True)
monitor.record_call("stock_zh_a_hist", success=False, error="Timeout")

# 获取统计信息
stats = monitor.get_stats("stock_zh_a_spot_em")
print(f"成功率: {(stats.total_calls - stats.failed_calls) / stats.total_calls * 100:.2f}%")

# 获取健康摘要
summary = get_akshare_health_summary()
print(summary)
```

### 3. 在Provider中的自动集成

健康检查机制已自动集成到`AkshareProvider`中，无需额外配置：

```python
# provider_akshare.py 中的自动集成
def call_tool(self, name: str, args: dict[str, Any], *, refresh: bool, meta_script: str) -> ToolResult:
    # 1. 自动执行健康检查
    health_result = check_akshare_health(force=False)
    
    # 2. 调用AKShare接口
    try:
        result = ak.some_function(**args)
        # 3. 记录成功
        health_monitor.record_call(name, success=True)
    except Exception as e:
        # 4. 记录失败
        health_monitor.record_call(name, success=False, error=str(e))
        # 5. 智能重试（降级模式下减少重试）
        ...
    
    # 6. 返回结果（包含健康状态）
    return ToolResult(
        meta={
            ...
            "health_status": {
                "is_degraded": health_monitor.is_degraded(),
                "consecutive_failures": stats.consecutive_failures,
            }
        },
        ...
    )
```

## 监控和告警

### 1. 定期监控
建议设置定时任务定期检查健康状态：

```bash
# crontab示例：每5分钟检查一次
*/5 * * * * cd /path/to/view-service && python -m view_service.health_check_cli check >> /var/log/akshare_health.log 2>&1
```

### 2. 告警脚本
创建告警脚本，当健康状态异常时发送通知：

```bash
#!/bin/bash
# akshare_health_alert.sh

cd /path/to/view-service

# 执行健康检查
python -m view_service.health_check_cli check

# 检查退出码
if [ $? -ne 0 ]; then
    # 健康检查失败，发送告警
    python -m view_service.health_check_cli summary --json | \
        mail -s "AKShare健康检查失败" admin@example.com
fi

# 检查是否降级
if python -m view_service.health_check_cli summary --json | grep -q '"is_degraded": true'; then
    # 已降级，发送告警
    echo "AKShare已进入降级模式" | \
        mail -s "AKShare降级告警" admin@example.com
fi
```

### 3. 集成到监控系统
将健康状态导出到监控系统（如Prometheus、Grafana）：

```python
# prometheus_exporter.py
from prometheus_client import Gauge, Counter, start_http_server
from view_service.akshare_health import get_health_monitor

# 定义指标
akshare_health = Gauge('akshare_health', 'AKShare健康状态（1=健康，0=不健康）')
akshare_degraded = Gauge('akshare_degraded', 'AKShare降级状态（1=降级，0=正常）')
akshare_total_calls = Counter('akshare_total_calls', 'AKShare总调用次数')
akshare_failed_calls = Counter('akshare_failed_calls', 'AKShare失败次数')

def update_metrics():
    monitor = get_health_monitor()
    summary = monitor.get_health_summary()
    
    akshare_health.set(1 if summary['is_healthy'] else 0)
    akshare_degraded.set(1 if summary['is_degraded'] else 0)
    
    stats = monitor.get_stats(None)
    akshare_total_calls.inc(stats.total_calls)
    akshare_failed_calls.inc(stats.failed_calls)

# 启动HTTP服务器
start_http_server(8000)
```

## 故障排查

### 问题1：健康检查一直失败
**可能原因**：
- AKShare服务不可用
- 网络连接问题
- 代理配置错误

**解决方法**：
```bash
# 1. 检查网络连接
ping data.eastmoney.com

# 2. 测试AKShare接口
python -c "import akshare as ak; print(ak.stock_info_a_code_name())"

# 3. 检查代理设置
echo $HTTP_PROXY
echo $HTTPS_PROXY

# 4. 禁用代理重试
export FINSKILLS_FORCE_NO_PROXY=1
python -m view_service.health_check_cli check --force
```

### 问题2：频繁触发降级模式
**可能原因**：
- 降级阈值设置过低
- AKShare接口不稳定
- 网络质量差

**解决方法**：
```bash
# 1. 调整降级阈值
export FINSKILLS_DEGRADATION_THRESHOLD=10  # 增加到10次

# 2. 增加重试次数
export FINSKILLS_CALL_RETRIES=3

# 3. 增加超时时间
export FINSKILLS_DEFAULT_TIMEOUT=30

# 4. 查看详细统计
python -m view_service.health_check_cli stats
```

### 问题3：统计信息不准确
**可能原因**：
- 统计信息未重置
- 多进程环境下统计不同步

**解决方法**：
```bash
# 重置统计信息
python -m view_service.health_check_cli reset

# 查看当前统计
python -m view_service.health_check_cli summary
```

## 最佳实践

1. **定期监控**：设置定时任务每5-10分钟检查一次健康状态
2. **告警配置**：配置告警脚本，及时发现问题
3. **日志记录**：将健康检查结果记录到日志文件
4. **阈值调整**：根据实际情况调整降级阈值和重试次数
5. **统计分析**：定期分析统计信息，识别问题工具
6. **备用方案**：为关键工具准备备用数据源

## 性能影响

健康检查机制对性能的影响很小：
- 健康检查：每5分钟执行一次，响应时间约0.5秒
- 统计记录：每次调用增加约0.1ms开销
- 内存占用：约1-2MB（取决于统计的工具数量）

## 未来改进

1. **备用数据源**：自动切换到备用数据源（东方财富、同花顺）
2. **智能降级**：根据错误类型选择不同的降级策略
3. **预测性告警**：基于历史数据预测可能的故障
4. **自动恢复**：自动尝试恢复失败的接口
5. **分布式监控**：支持多实例环境下的统一监控

## 相关文档

- [待修复问题优先级列表](../docs/待修复问题优先级列表.md)
- [P0问题修复总结](../docs/P0问题修复总结.md)
- [China-market Skills测试报告](../docs/China-market-skills测试报告.md)
