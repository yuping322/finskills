"""
阈值回测验证框架

用于验证methodology文档中的阈值合理性
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import pandas as pd
import numpy as np


@dataclass
class BacktestConfig:
    """回测配置"""
    skill_name: str
    start_date: str  # YYYY-MM-DD
    end_date: str  # YYYY-MM-DD
    holding_period: int  # 持有天数
    thresholds: dict[str, Any]  # 阈值配置
    

@dataclass
class SignalResult:
    """信号结果"""
    date: str
    symbol: str
    signal_type: str  # 信号类型
    entry_price: float  # 入场价格
    exit_price: float  # 出场价格
    return_pct: float  # 收益率
    max_drawdown: float  # 最大回撤
    holding_days: int  # 实际持有天数
    

@dataclass
class BacktestResult:
    """回测结果"""
    config: BacktestConfig
    signals: list[SignalResult]
    
    # 统计指标
    total_signals: int
    avg_return: float
    median_return: float
    win_rate: float
    profit_loss_ratio: float
    max_return: float
    min_return: float
    sharpe_ratio: float
    
    # 分位数
    return_25pct: float
    return_75pct: float
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'config': {
                'skill_name': self.config.skill_name,
                'start_date': self.config.start_date,
                'end_date': self.config.end_date,
                'holding_period': self.config.holding_period,
                'thresholds': self.config.thresholds,
            },
            'statistics': {
                'total_signals': self.total_signals,
                'avg_return': round(self.avg_return, 4),
                'median_return': round(self.median_return, 4),
                'win_rate': round(self.win_rate, 4),
                'profit_loss_ratio': round(self.profit_loss_ratio, 4),
                'max_return': round(self.max_return, 4),
                'min_return': round(self.min_return, 4),
                'sharpe_ratio': round(self.sharpe_ratio, 4),
                'return_25pct': round(self.return_25pct, 4),
                'return_75pct': round(self.return_75pct, 4),
            },
            'signals_count': len(self.signals),
        }


class BacktestFramework:
    """回测框架"""
    
    def __init__(self, cache_dir: str = "backtest_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_historical_data(
        self,
        data_source: str,
        start_date: str,
        end_date: str,
        **kwargs
    ) -> pd.DataFrame:
        """
        获取历史数据
        
        Args:
            data_source: 数据源名称（如 stock_dzjy_mrmx）
            start_date: 开始日期 YYYY-MM-DD
            end_date: 结束日期 YYYY-MM-DD
            **kwargs: 其他参数
        
        Returns:
            DataFrame with historical data
        """
        # 检查缓存
        cache_file = self.cache_dir / f"{data_source}_{start_date}_{end_date}.parquet"
        if cache_file.exists():
            print(f"Loading from cache: {cache_file}")
            return pd.read_parquet(cache_file)
        
        # 从AKShare获取数据
        print(f"Fetching data from AKShare: {data_source}")
        try:
            import akshare as ak
            func = getattr(ak, data_source)
            df = func(**kwargs)
            
            # 保存到缓存
            df.to_parquet(cache_file)
            print(f"Saved to cache: {cache_file}")
            
            return df
        except Exception as e:
            print(f"Error fetching data: {e}")
            return pd.DataFrame()
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        清洗数据
        
        Args:
            df: 原始数据
        
        Returns:
            清洗后的数据
        """
        if df.empty:
            return df
        
        # 剔除ST股票
        if '股票名称' in df.columns:
            df = df[~df['股票名称'].str.contains('ST', na=False)]
        if '名称' in df.columns:
            df = df[~df['名称'].str.contains('ST', na=False)]
        
        # 处理缺失值
        df = df.dropna(subset=df.columns[:5])  # 前5列不能有缺失
        
        return df
    
    def generate_signals(
        self,
        df: pd.DataFrame,
        rule_func: callable,
        thresholds: dict
    ) -> pd.DataFrame:
        """
        生成交易信号
        
        Args:
            df: 数据
            rule_func: 规则函数
            thresholds: 阈值配置
        
        Returns:
            带信号的DataFrame
        """
        return rule_func(df, thresholds)
    
    def calculate_returns(
        self,
        signals: pd.DataFrame,
        price_data: pd.DataFrame,
        holding_period: int
    ) -> list[SignalResult]:
        """
        计算收益
        
        Args:
            signals: 信号数据
            price_data: 价格数据
            holding_period: 持有天数
        
        Returns:
            信号结果列表
        """
        results = []
        
        for _, signal in signals.iterrows():
            symbol = signal.get('股票代码', signal.get('代码', ''))
            date = signal.get('交易日期', signal.get('日期', ''))
            signal_type = signal.get('信号类型', 'unknown')
            
            # 获取该股票的价格数据
            stock_prices = price_data[price_data['代码'] == symbol].copy()
            stock_prices = stock_prices.sort_values('日期')
            
            # 找到入场日期
            entry_idx = stock_prices[stock_prices['日期'] >= date].index
            if len(entry_idx) == 0:
                continue
            
            entry_idx = entry_idx[0]
            entry_price = stock_prices.loc[entry_idx, '收盘']
            
            # 找到出场日期（持有期后）
            exit_idx = entry_idx + holding_period
            if exit_idx >= len(stock_prices):
                exit_idx = len(stock_prices) - 1
            
            exit_price = stock_prices.iloc[exit_idx]['收盘']
            
            # 计算收益率
            return_pct = (exit_price - entry_price) / entry_price
            
            # 计算最大回撤
            period_prices = stock_prices.iloc[entry_idx:exit_idx+1]['收盘']
            cummax = period_prices.cummax()
            drawdown = (period_prices - cummax) / cummax
            max_drawdown = drawdown.min()
            
            results.append(SignalResult(
                date=date,
                symbol=symbol,
                signal_type=signal_type,
                entry_price=entry_price,
                exit_price=exit_price,
                return_pct=return_pct,
                max_drawdown=max_drawdown,
                holding_days=exit_idx - entry_idx,
            ))
        
        return results
    
    def analyze_results(self, results: list[SignalResult]) -> dict:
        """
        分析回测结果
        
        Args:
            results: 信号结果列表
        
        Returns:
            统计指标字典
        """
        if not results:
            return {
                'total_signals': 0,
                'avg_return': 0,
                'median_return': 0,
                'win_rate': 0,
                'profit_loss_ratio': 0,
                'max_return': 0,
                'min_return': 0,
                'sharpe_ratio': 0,
                'return_25pct': 0,
                'return_75pct': 0,
            }
        
        returns = [r.return_pct for r in results]
        returns_array = np.array(returns)
        
        # 基础统计
        total_signals = len(results)
        avg_return = returns_array.mean()
        median_return = np.median(returns_array)
        win_rate = (returns_array > 0).mean()
        
        # 盈亏比
        profits = returns_array[returns_array > 0]
        losses = returns_array[returns_array < 0]
        profit_loss_ratio = (
            abs(profits.mean() / losses.mean())
            if len(losses) > 0 and losses.mean() != 0
            else 0
        )
        
        # 极值
        max_return = returns_array.max()
        min_return = returns_array.min()
        
        # 夏普比率
        sharpe_ratio = (
            avg_return / returns_array.std()
            if returns_array.std() > 0
            else 0
        )
        
        # 分位数
        return_25pct = np.percentile(returns_array, 25)
        return_75pct = np.percentile(returns_array, 75)
        
        return {
            'total_signals': total_signals,
            'avg_return': avg_return,
            'median_return': median_return,
            'win_rate': win_rate,
            'profit_loss_ratio': profit_loss_ratio,
            'max_return': max_return,
            'min_return': min_return,
            'sharpe_ratio': sharpe_ratio,
            'return_25pct': return_25pct,
            'return_75pct': return_75pct,
        }
    
    def run_backtest(
        self,
        config: BacktestConfig,
        rule_func: callable,
        data_source: str,
        price_data_source: str = "stock_zh_a_hist",
        **data_kwargs
    ) -> BacktestResult:
        """
        运行回测
        
        Args:
            config: 回测配置
            rule_func: 规则函数
            data_source: 数据源
            price_data_source: 价格数据源
            **data_kwargs: 数据获取参数
        
        Returns:
            回测结果
        """
        print(f"\n{'='*60}")
        print(f"Running backtest for {config.skill_name}")
        print(f"Period: {config.start_date} to {config.end_date}")
        print(f"Holding period: {config.holding_period} days")
        print(f"Thresholds: {config.thresholds}")
        print(f"{'='*60}\n")
        
        # 1. 获取数据
        df = self.get_historical_data(
            data_source,
            config.start_date,
            config.end_date,
            **data_kwargs
        )
        
        # 2. 清洗数据
        df = self.clean_data(df)
        print(f"Data shape after cleaning: {df.shape}")
        
        # 3. 生成信号
        signals = self.generate_signals(df, rule_func, config.thresholds)
        print(f"Generated {len(signals)} signals")
        
        if len(signals) == 0:
            print("No signals generated, returning empty result")
            return BacktestResult(
                config=config,
                signals=[],
                total_signals=0,
                avg_return=0,
                median_return=0,
                win_rate=0,
                profit_loss_ratio=0,
                max_return=0,
                min_return=0,
                sharpe_ratio=0,
                return_25pct=0,
                return_75pct=0,
            )
        
        # 4. 获取价格数据（简化版，实际需要更复杂的逻辑）
        # TODO: 实现价格数据获取
        price_data = pd.DataFrame()  # Placeholder
        
        # 5. 计算收益
        results = self.calculate_returns(signals, price_data, config.holding_period)
        print(f"Calculated returns for {len(results)} signals")
        
        # 6. 分析结果
        stats = self.analyze_results(results)
        
        # 7. 创建回测结果
        backtest_result = BacktestResult(
            config=config,
            signals=results,
            **stats
        )
        
        print(f"\nBacktest Results:")
        print(f"  Total signals: {stats['total_signals']}")
        print(f"  Avg return: {stats['avg_return']:.2%}")
        print(f"  Win rate: {stats['win_rate']:.2%}")
        print(f"  Sharpe ratio: {stats['sharpe_ratio']:.2f}")
        
        return backtest_result
    
    def save_result(self, result: BacktestResult, output_file: str):
        """保存回测结果"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
        
        print(f"\nResult saved to: {output_path}")


# 示例：block-deal-monitor的规则函数
def block_deal_rule_1(df: pd.DataFrame, thresholds: dict) -> pd.DataFrame:
    """
    规则1：建仓型信号
    
    IF条件：
    - 折价率在 -5% ~ -2% 之间（温和折价）
    - 连续3天以上出现大宗交易
    - 平均折价率变化 < 1%（成交均价稳定）
    """
    # TODO: 实现规则逻辑
    signals = df.copy()
    signals['信号类型'] = '建仓型'
    return signals


if __name__ == "__main__":
    # 示例用法
    framework = BacktestFramework()
    
    config = BacktestConfig(
        skill_name="block-deal-monitor",
        start_date="2020-01-01",
        end_date="2023-12-31",
        holding_period=20,
        thresholds={
            'discount_rate_min': -0.05,
            'discount_rate_max': -0.02,
            'consecutive_days': 3,
            'avg_discount_change': 0.01,
        }
    )
    
    result = framework.run_backtest(
        config,
        rule_func=block_deal_rule_1,
        data_source="stock_dzjy_mrmx",
    )
    
    framework.save_result(result, "backtest_results/block-deal-monitor_rule1.json")
