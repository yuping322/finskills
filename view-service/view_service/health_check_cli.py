#!/usr/bin/env python3
"""
AKShare健康检查CLI工具

用法:
    python -m view_service.health_check_cli check          # 执行健康检查
    python -m view_service.health_check_cli stats          # 查看统计信息
    python -m view_service.health_check_cli reset          # 重置统计信息
    python -m view_service.health_check_cli summary        # 查看健康摘要
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime

from .akshare_health import (
    check_akshare_health,
    get_health_monitor,
    get_akshare_health_summary,
)


def cmd_check(args):
    """执行健康检查"""
    print("正在执行AKShare健康检查...")
    result = check_akshare_health(force=args.force)
    
    print(f"\n健康状态: {'✅ 健康' if result.is_healthy else '❌ 不健康'}")
    print(f"检查时间: {result.check_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"响应时间: {result.response_time:.3f}秒 ({result.response_time * 1000:.1f}ms)")
    
    if result.error:
        print(f"错误信息: {result.error}")
    
    if result.details:
        print(f"\n详细信息:")
        for key, value in result.details.items():
            print(f"  {key}: {value}")
    
    return 0 if result.is_healthy else 1


def cmd_stats(args):
    """查看统计信息"""
    monitor = get_health_monitor()
    
    if args.tool:
        # 查看特定工具的统计
        stats = monitor.get_stats(args.tool)
        print(f"\n工具统计: {args.tool}")
        print(f"总调用次数: {stats.total_calls}")
        print(f"失败次数: {stats.failed_calls}")
        if stats.total_calls > 0:
            success_rate = (stats.total_calls - stats.failed_calls) / stats.total_calls * 100
            print(f"成功率: {success_rate:.2f}%")
        print(f"连续失败次数: {stats.consecutive_failures}")
        
        if stats.last_error_time:
            print(f"\n最后错误时间: {stats.last_error_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"最后错误信息: {stats.last_error_message}")
        
        if stats.error_types:
            print(f"\n错误类型分布:")
            for error_type, count in sorted(stats.error_types.items(), key=lambda x: x[1], reverse=True):
                print(f"  {error_type}: {count}")
    else:
        # 查看全局统计
        global_stats = monitor.get_stats(None)
        all_stats = monitor.get_all_stats()
        
        print(f"\n全局统计:")
        print(f"总调用次数: {global_stats.total_calls}")
        print(f"失败次数: {global_stats.failed_calls}")
        if global_stats.total_calls > 0:
            success_rate = (global_stats.total_calls - global_stats.failed_calls) / global_stats.total_calls * 100
            print(f"成功率: {success_rate:.2f}%")
        print(f"连续失败次数: {global_stats.consecutive_failures}")
        
        if global_stats.last_error_time:
            print(f"\n最后错误时间: {global_stats.last_error_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"最后错误信息: {global_stats.last_error_message}")
        
        if all_stats:
            print(f"\n工具统计 (共{len(all_stats)}个工具):")
            # 按失败次数排序
            sorted_tools = sorted(all_stats.items(), key=lambda x: x[1].failed_calls, reverse=True)
            for tool_name, stats in sorted_tools[:10]:  # 只显示前10个
                if stats.total_calls > 0:
                    success_rate = (stats.total_calls - stats.failed_calls) / stats.total_calls * 100
                    print(f"  {tool_name}: {stats.total_calls}次调用, {stats.failed_calls}次失败 ({success_rate:.1f}%成功)")
    
    return 0


def cmd_reset(args):
    """重置统计信息"""
    monitor = get_health_monitor()
    
    if args.tool:
        monitor.reset_stats(args.tool)
        print(f"已重置工具 {args.tool} 的统计信息")
    else:
        monitor.reset_stats(None)
        print("已重置所有统计信息")
    
    return 0


def cmd_summary(args):
    """查看健康摘要"""
    summary = get_akshare_health_summary()
    
    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print("\n=== AKShare健康状态摘要 ===\n")
        
        print(f"健康状态: {'✅ 健康' if summary['is_healthy'] else '❌ 不健康' if summary['is_healthy'] is not None else '⚠️  未检查'}")
        print(f"降级模式: {'🔴 是' if summary['is_degraded'] else '✅ 否'}")
        
        if summary['last_check_time']:
            print(f"最后检查: {summary['last_check_time']}")
        
        if summary['response_time']:
            print(f"响应时间: {summary['response_time']:.3f}秒")
        
        print(f"\n全局统计:")
        global_stats = summary['global_stats']
        print(f"  总调用: {global_stats['total_calls']}")
        print(f"  失败: {global_stats['failed_calls']}")
        print(f"  成功率: {global_stats['success_rate']}%")
        print(f"  连续失败: {global_stats['consecutive_failures']}")
        
        if global_stats['last_error_time']:
            print(f"\n最后错误:")
            print(f"  时间: {global_stats['last_error_time']}")
            print(f"  信息: {global_stats['last_error_message']}")
        
        if summary['degradation_info']:
            print(f"\n降级信息:")
            deg_info = summary['degradation_info']
            print(f"  状态: 🔴 已降级")
            print(f"  开始时间: {deg_info['degradation_start_time']}")
            print(f"  触发阈值: {deg_info['threshold']}次连续失败")
    
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="AKShare健康检查CLI工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # check命令
    check_parser = subparsers.add_parser("check", help="执行健康检查")
    check_parser.add_argument("--force", action="store_true", help="强制执行检查（忽略缓存）")
    check_parser.set_defaults(func=cmd_check)
    
    # stats命令
    stats_parser = subparsers.add_parser("stats", help="查看统计信息")
    stats_parser.add_argument("--tool", help="查看特定工具的统计")
    stats_parser.set_defaults(func=cmd_stats)
    
    # reset命令
    reset_parser = subparsers.add_parser("reset", help="重置统计信息")
    reset_parser.add_argument("--tool", help="重置特定工具的统计")
    reset_parser.set_defaults(func=cmd_reset)
    
    # summary命令
    summary_parser = subparsers.add_parser("summary", help="查看健康摘要")
    summary_parser.add_argument("--json", action="store_true", help="以JSON格式输出")
    summary_parser.set_defaults(func=cmd_summary)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        return args.func(args)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
