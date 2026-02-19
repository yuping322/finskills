"""
阈值回测验证框架（CN）

目标：
- 把 methodology 里的“阈值 + 规则”转成可重复的历史验证
- 输出：信号数量、收益分布、胜率、夏普、最大回撤等

设计原则：
- offline-first：支持注入 data/price provider（便于在无网络环境跑单测）
- online 可用：默认用 AKShare 拉取数据，并做本地缓存
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Optional

import numpy as np
import pandas as pd


@dataclass
class BacktestConfig:
    """回测配置"""

    skill_name: str
    start_date: str  # YYYY-MM-DD
    end_date: str  # YYYY-MM-DD
    holding_period: int  # 持有天数
    thresholds: dict[str, Any]  # 阈值配置
    max_signals: int = 0  # 0 means no limit


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
            "config": {
                "skill_name": self.config.skill_name,
                "start_date": self.config.start_date,
                "end_date": self.config.end_date,
                "holding_period": self.config.holding_period,
                "thresholds": self.config.thresholds,
                "max_signals": self.config.max_signals,
            },
            "statistics": {
                "total_signals": self.total_signals,
                "avg_return": round(self.avg_return, 6),
                "median_return": round(self.median_return, 6),
                "win_rate": round(self.win_rate, 6),
                "profit_loss_ratio": round(self.profit_loss_ratio, 6),
                "max_return": round(self.max_return, 6),
                "min_return": round(self.min_return, 6),
                "sharpe_ratio": round(self.sharpe_ratio, 6),
                "return_25pct": round(self.return_25pct, 6),
                "return_75pct": round(self.return_75pct, 6),
            },
            "signals_count": len(self.signals),
        }


class BacktestFramework:
    """回测框架"""

    def __init__(
        self,
        cache_dir: str = "backtest_cache",
        *,
        data_provider: Optional[Callable[[str, str, str, dict[str, Any]], pd.DataFrame]] = None,
        price_provider: Optional[Callable[[str, str, str], pd.DataFrame]] = None,
    ):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self._data_provider = data_provider or self._akshare_data_provider
        self._price_provider = price_provider or self._akshare_price_provider

    @staticmethod
    def _akshare_data_provider(data_source: str, start_date: str, end_date: str, kwargs: dict[str, Any]) -> pd.DataFrame:
        import akshare as ak

        func = getattr(ak, data_source)
        return func(**(kwargs or {}))

    @staticmethod
    def _normalize_a_symbol(symbol: str) -> str:
        """
        Normalize A-share symbol strings into 6-digit format when possible.
        Accepts: '000001', 'SZ000001', 'sh600000', etc.
        """
        s = (symbol or "").strip().upper()
        if not s:
            return ""
        for pfx in ("SZ", "SH", "BJ"):
            if s.startswith(pfx) and len(s) >= 8:
                s = s[len(pfx) :]
        digits = "".join(ch for ch in s if ch.isdigit())
        if len(digits) >= 6:
            return digits[-6:]
        return digits

    @staticmethod
    def _ymd(s: str) -> str:
        """YYYY-MM-DD -> YYYYMMDD"""
        s = (s or "").strip()
        if not s:
            return ""
        if "-" in s:
            return s.replace("-", "")
        return s

    def _akshare_price_provider(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        import akshare as ak

        sym = self._normalize_a_symbol(symbol)
        if not sym:
            return pd.DataFrame()
        sd = self._ymd(start_date)
        ed = self._ymd(end_date)
        try:
            df = ak.stock_zh_a_hist(symbol=sym, period="daily", start_date=sd, end_date=ed, adjust="")
        except TypeError:
            df = ak.stock_zh_a_hist(symbol=sym, period="daily", start_date=sd, end_date=ed)
        return df if isinstance(df, pd.DataFrame) else pd.DataFrame()

    def _cache_key(self, name: str, start_date: str, end_date: str, kwargs: dict[str, Any]) -> str:
        payload = json.dumps({"name": name, "start": start_date, "end": end_date, "kwargs": kwargs}, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]

    def _cache_paths(self, base: str) -> tuple[Path, Path]:
        return (self.cache_dir / f"{base}.csv.gz", self.cache_dir / f"{base}.parquet")

    def get_historical_data(self, data_source: str, start_date: str, end_date: str, **kwargs) -> pd.DataFrame:
        kwargs = kwargs or {}
        key = self._cache_key(data_source, start_date, end_date, kwargs)
        base = f"{data_source}_{start_date}_{end_date}_{key}"
        cache_csv, cache_parquet = self._cache_paths(base)

        if cache_parquet.exists():
            try:
                return pd.read_parquet(cache_parquet)
            except Exception:
                pass
        if cache_csv.exists():
            try:
                return pd.read_csv(cache_csv)
            except Exception:
                pass

        df = self._data_provider(data_source, start_date, end_date, kwargs)
        if not isinstance(df, pd.DataFrame):
            return pd.DataFrame()

        try:
            df.to_parquet(cache_parquet)
        except Exception:
            df.to_csv(cache_csv, index=False, compression="gzip")
        return df

    def get_price_history(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        sym = self._normalize_a_symbol(symbol)
        if not sym:
            return pd.DataFrame()
        key = self._cache_key(f"price_{sym}", start_date, end_date, {})
        base = f"price_{sym}_{start_date}_{end_date}_{key}"
        cache_csv, cache_parquet = self._cache_paths(base)

        if cache_parquet.exists():
            try:
                return pd.read_parquet(cache_parquet)
            except Exception:
                pass
        if cache_csv.exists():
            try:
                return pd.read_csv(cache_csv)
            except Exception:
                pass

        df = self._price_provider(sym, start_date, end_date)
        if not isinstance(df, pd.DataFrame) or df.empty:
            return pd.DataFrame()
        try:
            df.to_parquet(cache_parquet)
        except Exception:
            df.to_csv(cache_csv, index=False, compression="gzip")
        return df

    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df

        if "股票名称" in df.columns:
            df = df[~df["股票名称"].astype(str).str.contains("ST", na=False)]
        if "名称" in df.columns:
            df = df[~df["名称"].astype(str).str.contains("ST", na=False)]

        if len(df.columns) >= 5:
            df = df.dropna(subset=df.columns[:5])
        return df

    @staticmethod
    def generate_signals(df: pd.DataFrame, rule_func: Callable, thresholds: dict) -> pd.DataFrame:
        return rule_func(df, thresholds)

    def calculate_returns(self, signals: pd.DataFrame, holding_period: int) -> list[SignalResult]:
        results: list[SignalResult] = []

        for _, signal in signals.iterrows():
            symbol = signal.get("股票代码", signal.get("代码", ""))
            date = signal.get("交易日期", signal.get("日期", ""))
            signal_type = signal.get("信号类型", "unknown")

            sym = self._normalize_a_symbol(str(symbol))
            if not sym:
                continue

            try:
                d0 = datetime.strptime(str(date)[:10], "%Y-%m-%d")
            except Exception:
                try:
                    d0 = datetime.strptime(str(date)[:8], "%Y%m%d")
                except Exception:
                    continue

            d1 = d0 + timedelta(days=max(int(holding_period) * 3, 30))
            stock_prices = self.get_price_history(sym, d0.strftime("%Y-%m-%d"), d1.strftime("%Y-%m-%d")).copy()
            if stock_prices.empty:
                continue

            if "日期" not in stock_prices.columns and "date" in stock_prices.columns:
                stock_prices = stock_prices.rename(columns={"date": "日期"})
            if "收盘" not in stock_prices.columns and "close" in stock_prices.columns:
                stock_prices = stock_prices.rename(columns={"close": "收盘"})
            if "日期" not in stock_prices.columns or "收盘" not in stock_prices.columns:
                continue

            stock_prices["日期"] = stock_prices["日期"].astype(str).str.slice(0, 10)
            stock_prices = stock_prices.sort_values("日期")

            entry_pos = stock_prices[stock_prices["日期"] >= d0.strftime("%Y-%m-%d")].index
            if len(entry_pos) == 0:
                continue
            entry_i = stock_prices.index.get_loc(entry_pos[0])
            entry_price = float(stock_prices.iloc[entry_i]["收盘"])

            exit_i = min(entry_i + int(holding_period), len(stock_prices) - 1)
            exit_price = float(stock_prices.iloc[exit_i]["收盘"])

            return_pct = (exit_price - entry_price) / entry_price

            period_prices = stock_prices.iloc[entry_i : exit_i + 1]["收盘"].astype(float)
            cummax = period_prices.cummax()
            drawdown = (period_prices - cummax) / cummax
            max_drawdown = float(drawdown.min())

            results.append(
                SignalResult(
                    date=d0.strftime("%Y-%m-%d"),
                    symbol=sym,
                    signal_type=str(signal_type),
                    entry_price=entry_price,
                    exit_price=exit_price,
                    return_pct=float(return_pct),
                    max_drawdown=max_drawdown,
                    holding_days=int(exit_i - entry_i),
                )
            )

        return results

    @staticmethod
    def analyze_results(results: list[SignalResult]) -> dict[str, Any]:
        if not results:
            return {
                "total_signals": 0,
                "avg_return": 0.0,
                "median_return": 0.0,
                "win_rate": 0.0,
                "profit_loss_ratio": 0.0,
                "max_return": 0.0,
                "min_return": 0.0,
                "sharpe_ratio": 0.0,
                "return_25pct": 0.0,
                "return_75pct": 0.0,
            }

        returns_array = np.array([r.return_pct for r in results], dtype=float)
        total_signals = int(len(results))
        avg_return = float(returns_array.mean())
        median_return = float(np.median(returns_array))
        win_rate = float((returns_array > 0).mean())

        profits = returns_array[returns_array > 0]
        losses = returns_array[returns_array < 0]
        profit_loss_ratio = float(abs(profits.mean() / losses.mean())) if len(losses) > 0 and float(losses.mean()) != 0.0 else 0.0

        max_return = float(returns_array.max())
        min_return = float(returns_array.min())

        std = float(returns_array.std())
        sharpe_ratio = float(avg_return / std) if std > 0 else 0.0

        return_25pct = float(np.percentile(returns_array, 25))
        return_75pct = float(np.percentile(returns_array, 75))

        return {
            "total_signals": total_signals,
            "avg_return": avg_return,
            "median_return": median_return,
            "win_rate": win_rate,
            "profit_loss_ratio": profit_loss_ratio,
            "max_return": max_return,
            "min_return": min_return,
            "sharpe_ratio": sharpe_ratio,
            "return_25pct": return_25pct,
            "return_75pct": return_75pct,
        }

    def run_backtest(self, config: BacktestConfig, rule_func: Callable, data_source: str, **data_kwargs) -> BacktestResult:
        df = self.get_historical_data(data_source, config.start_date, config.end_date, **(data_kwargs or {}))
        df = self.clean_data(df)

        signals = self.generate_signals(df, rule_func, config.thresholds)
        if config.max_signals and config.max_signals > 0 and len(signals) > config.max_signals:
            signals = signals.head(config.max_signals).copy()

        if len(signals) == 0:
            return BacktestResult(
                config=config,
                signals=[],
                total_signals=0,
                avg_return=0.0,
                median_return=0.0,
                win_rate=0.0,
                profit_loss_ratio=0.0,
                max_return=0.0,
                min_return=0.0,
                sharpe_ratio=0.0,
                return_25pct=0.0,
                return_75pct=0.0,
            )

        results = self.calculate_returns(signals, config.holding_period)
        stats = self.analyze_results(results)
        return BacktestResult(config=config, signals=results, **stats)

    @staticmethod
    def save_result(result: BacktestResult, output_file: str) -> None:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
