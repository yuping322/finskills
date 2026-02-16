"""
AKShare健康检查和监控模块

提供AKShare接口的健康检查、错误统计、降级策略等功能
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any
from threading import Lock


@dataclass
class HealthCheckResult:
    """健康检查结果"""
    is_healthy: bool
    check_time: datetime
    response_time: float  # 秒
    error: str | None = None
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class ErrorStats:
    """错误统计"""
    total_calls: int = 0
    failed_calls: int = 0
    last_error_time: datetime | None = None
    last_error_message: str | None = None
    consecutive_failures: int = 0
    error_types: dict[str, int] = field(default_factory=dict)


class AKShareHealthMonitor:
    """AKShare健康监控器"""
    
    def __init__(self):
        self._lock = Lock()
        self._last_health_check: HealthCheckResult | None = None
        self._health_check_interval = float(os.getenv("FINSKILLS_HEALTH_CHECK_INTERVAL", "300"))  # 5分钟
        self._error_stats: dict[str, ErrorStats] = {}  # 按工具名称统计
        self._global_stats = ErrorStats()
        
        # 降级阈值配置
        self._degradation_threshold = int(os.getenv("FINSKILLS_DEGRADATION_THRESHOLD", "5"))  # 连续失败5次触发降级
        self._degradation_window = float(os.getenv("FINSKILLS_DEGRADATION_WINDOW", "300"))  # 5分钟内
        self._is_degraded = False
        self._degradation_start_time: datetime | None = None
        
    def check_health(self, force: bool = False) -> HealthCheckResult:
        """
        检查AKShare健康状态
        
        Args:
            force: 是否强制检查（忽略缓存）
            
        Returns:
            健康检查结果
        """
        with self._lock:
            # 如果有缓存且未过期，直接返回
            if not force and self._last_health_check:
                elapsed = (datetime.now() - self._last_health_check.check_time).total_seconds()
                if elapsed < self._health_check_interval:
                    return self._last_health_check
            
            # 执行健康检查
            result = self._perform_health_check()
            self._last_health_check = result
            return result
    
    def _perform_health_check(self) -> HealthCheckResult:
        """执行实际的健康检查"""
        start_time = time.time()
        
        try:
            import akshare as ak
            
            # 使用轻量级接口测试连接性
            # stock_info_a_code_name 是一个相对稳定且快速的接口
            df = ak.stock_info_a_code_name()
            
            response_time = time.time() - start_time
            
            # 检查返回数据是否有效
            if df is None or len(df) == 0:
                return HealthCheckResult(
                    is_healthy=False,
                    check_time=datetime.now(),
                    response_time=response_time,
                    error="返回数据为空",
                    details={"data_length": 0}
                )
            
            return HealthCheckResult(
                is_healthy=True,
                check_time=datetime.now(),
                response_time=response_time,
                details={
                    "data_length": len(df),
                    "response_time_ms": round(response_time * 1000, 2)
                }
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheckResult(
                is_healthy=False,
                check_time=datetime.now(),
                response_time=response_time,
                error=str(e),
                details={"error_type": type(e).__name__}
            )
    
    def record_call(self, tool_name: str, success: bool, error: str | None = None):
        """
        记录工具调用结果
        
        Args:
            tool_name: 工具名称
            success: 是否成功
            error: 错误信息（如果失败）
        """
        with self._lock:
            # 更新工具级别统计
            if tool_name not in self._error_stats:
                self._error_stats[tool_name] = ErrorStats()
            
            stats = self._error_stats[tool_name]
            stats.total_calls += 1
            
            if not success:
                stats.failed_calls += 1
                stats.consecutive_failures += 1
                stats.last_error_time = datetime.now()
                stats.last_error_message = error
                
                # 统计错误类型
                if error:
                    error_type = self._classify_error(error)
                    stats.error_types[error_type] = stats.error_types.get(error_type, 0) + 1
            else:
                stats.consecutive_failures = 0
            
            # 更新全局统计
            self._global_stats.total_calls += 1
            if not success:
                self._global_stats.failed_calls += 1
                self._global_stats.consecutive_failures += 1
                self._global_stats.last_error_time = datetime.now()
                self._global_stats.last_error_message = error
            else:
                self._global_stats.consecutive_failures = 0
            
            # 检查是否需要触发降级
            self._check_degradation()
    
    def _classify_error(self, error: str) -> str:
        """分类错误类型"""
        error_lower = error.lower()
        
        if "timeout" in error_lower or "timed out" in error_lower:
            return "timeout"
        elif "connection" in error_lower or "network" in error_lower:
            return "network"
        elif "keyerror" in error_lower:
            return "data_missing"
        elif "403" in error_lower or "forbidden" in error_lower:
            return "access_denied"
        elif "404" in error_lower or "not found" in error_lower:
            return "not_found"
        elif "500" in error_lower or "502" in error_lower or "503" in error_lower:
            return "server_error"
        else:
            return "unknown"
    
    def _check_degradation(self):
        """检查是否需要触发降级模式"""
        # 如果连续失败次数超过阈值，触发降级
        if self._global_stats.consecutive_failures >= self._degradation_threshold:
            if not self._is_degraded:
                self._is_degraded = True
                self._degradation_start_time = datetime.now()
                print(f"[AKShare Health] 触发降级模式：连续失败{self._global_stats.consecutive_failures}次")
        
        # 如果已经降级，检查是否可以恢复
        elif self._is_degraded:
            # 如果最近一次成功调用，尝试恢复
            if self._global_stats.consecutive_failures == 0:
                self._is_degraded = False
                self._degradation_start_time = None
                print("[AKShare Health] 恢复正常模式")
    
    def is_degraded(self) -> bool:
        """是否处于降级模式"""
        with self._lock:
            return self._is_degraded
    
    def get_stats(self, tool_name: str | None = None) -> ErrorStats:
        """
        获取错误统计
        
        Args:
            tool_name: 工具名称，None表示获取全局统计
            
        Returns:
            错误统计
        """
        with self._lock:
            if tool_name is None:
                return self._global_stats
            return self._error_stats.get(tool_name, ErrorStats())
    
    def get_all_stats(self) -> dict[str, ErrorStats]:
        """获取所有工具的统计信息"""
        with self._lock:
            return dict(self._error_stats)
    
    def reset_stats(self, tool_name: str | None = None):
        """
        重置统计信息
        
        Args:
            tool_name: 工具名称，None表示重置所有统计
        """
        with self._lock:
            if tool_name is None:
                self._error_stats.clear()
                self._global_stats = ErrorStats()
                self._is_degraded = False
                self._degradation_start_time = None
            elif tool_name in self._error_stats:
                self._error_stats[tool_name] = ErrorStats()
    
    def get_health_summary(self) -> dict[str, Any]:
        """获取健康状态摘要"""
        with self._lock:
            health_check = self._last_health_check
            
            summary = {
                "is_healthy": health_check.is_healthy if health_check else None,
                "is_degraded": self._is_degraded,
                "last_check_time": health_check.check_time.isoformat() if health_check else None,
                "response_time": health_check.response_time if health_check else None,
                "global_stats": {
                    "total_calls": self._global_stats.total_calls,
                    "failed_calls": self._global_stats.failed_calls,
                    "success_rate": (
                        round((self._global_stats.total_calls - self._global_stats.failed_calls) / 
                              self._global_stats.total_calls * 100, 2)
                        if self._global_stats.total_calls > 0 else 100.0
                    ),
                    "consecutive_failures": self._global_stats.consecutive_failures,
                    "last_error_time": (
                        self._global_stats.last_error_time.isoformat() 
                        if self._global_stats.last_error_time else None
                    ),
                    "last_error_message": self._global_stats.last_error_message,
                },
                "degradation_info": {
                    "is_degraded": self._is_degraded,
                    "degradation_start_time": (
                        self._degradation_start_time.isoformat() 
                        if self._degradation_start_time else None
                    ),
                    "threshold": self._degradation_threshold,
                } if self._is_degraded else None,
            }
            
            return summary


# 全局健康监控器实例
_health_monitor: AKShareHealthMonitor | None = None


def get_health_monitor() -> AKShareHealthMonitor:
    """获取全局健康监控器实例"""
    global _health_monitor
    if _health_monitor is None:
        _health_monitor = AKShareHealthMonitor()
    return _health_monitor


def check_akshare_health(force: bool = False) -> HealthCheckResult:
    """
    检查AKShare健康状态（便捷函数）
    
    Args:
        force: 是否强制检查
        
    Returns:
        健康检查结果
    """
    monitor = get_health_monitor()
    return monitor.check_health(force=force)


def is_akshare_degraded() -> bool:
    """检查AKShare是否处于降级模式（便捷函数）"""
    monitor = get_health_monitor()
    return monitor.is_degraded()


def get_akshare_health_summary() -> dict[str, Any]:
    """获取AKShare健康状态摘要（便捷函数）"""
    monitor = get_health_monitor()
    return monitor.get_health_summary()
