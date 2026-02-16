#!/usr/bin/env python3
"""
测试AKShare健康检查功能
"""
from __future__ import annotations

import os
import sys

# 启用健康检查
os.environ["FINSKILLS_HEALTH_CHECK_ENABLED"] = "1"

from view_service.akshare_health import get_health_monitor, check_akshare_health


def test_health_check():
    """测试健康检查"""
    print("=" * 60)
    print("测试1: 健康检查")
    print("=" * 60)
    
    result = check_akshare_health(force=True)
    print(f"健康状态: {'✅ 健康' if result.is_healthy else '❌ 不健康'}")
    print(f"响应时间: {result.response_time:.3f}秒")
    if result.error:
        print(f"错误: {result.error}")
    print()


def test_stats_recording():
    """测试统计记录"""
    print("=" * 60)
    print("测试2: 统计记录")
    print("=" * 60)
    
    monitor = get_health_monitor()
    
    # 模拟一些调用
    print("模拟10次成功调用...")
    for i in range(10):
        monitor.record_call("test_tool", success=True)
    
    print("模拟3次失败调用...")
    for i in range(3):
        monitor.record_call("test_tool", success=False, error="Test error")
    
    # 查看统计
    stats = monitor.get_stats("test_tool")
    print(f"\n统计结果:")
    print(f"  总调用: {stats.total_calls}")
    print(f"  失败: {stats.failed_calls}")
    print(f"  成功率: {(stats.total_calls - stats.failed_calls) / stats.total_calls * 100:.2f}%")
    print(f"  连续失败: {stats.consecutive_failures}")
    print()


def test_degradation():
    """测试降级机制"""
    print("=" * 60)
    print("测试3: 降级机制")
    print("=" * 60)
    
    monitor = get_health_monitor()
    
    # 重置统计
    monitor.reset_stats()
    
    print("模拟连续失败以触发降级...")
    threshold = int(os.getenv("FINSKILLS_DEGRADATION_THRESHOLD", "5"))
    
    for i in range(threshold + 1):
        monitor.record_call("test_tool_2", success=False, error=f"Error {i+1}")
        is_degraded = monitor.is_degraded()
        print(f"  失败 {i+1}/{threshold}: 降级状态 = {is_degraded}")
    
    print(f"\n最终降级状态: {'🔴 已降级' if monitor.is_degraded() else '✅ 正常'}")
    
    # 模拟恢复
    print("\n模拟成功调用以恢复...")
    monitor.record_call("test_tool_2", success=True)
    print(f"恢复后状态: {'🔴 已降级' if monitor.is_degraded() else '✅ 正常'}")
    print()


def test_error_classification():
    """测试错误分类"""
    print("=" * 60)
    print("测试4: 错误分类")
    print("=" * 60)
    
    monitor = get_health_monitor()
    monitor.reset_stats()
    
    # 模拟不同类型的错误
    errors = [
        "Read timed out",
        "Connection aborted",
        "KeyError: '代码'",
        "403 Forbidden",
        "404 Not Found",
        "500 Internal Server Error",
        "Unknown error",
    ]
    
    print("记录不同类型的错误...")
    for error in errors:
        monitor.record_call("test_tool_3", success=False, error=error)
    
    stats = monitor.get_stats("test_tool_3")
    print(f"\n错误类型分布:")
    for error_type, count in sorted(stats.error_types.items(), key=lambda x: x[1], reverse=True):
        print(f"  {error_type}: {count}")
    print()


def test_health_summary():
    """测试健康摘要"""
    print("=" * 60)
    print("测试5: 健康摘要")
    print("=" * 60)
    
    monitor = get_health_monitor()
    summary = monitor.get_health_summary()
    
    print("健康摘要:")
    print(f"  健康状态: {summary['is_healthy']}")
    print(f"  降级模式: {summary['is_degraded']}")
    print(f"  总调用: {summary['global_stats']['total_calls']}")
    print(f"  失败: {summary['global_stats']['failed_calls']}")
    print(f"  成功率: {summary['global_stats']['success_rate']}%")
    print()


def main():
    print("\n" + "=" * 60)
    print("AKShare健康检查功能测试")
    print("=" * 60 + "\n")
    
    try:
        test_health_check()
        test_stats_recording()
        test_degradation()
        test_error_classification()
        test_health_summary()
        
        print("=" * 60)
        print("✅ 所有测试完成")
        print("=" * 60)
        return 0
    except Exception as e:
        print(f"\n❌ 测试失败: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
