from __future__ import annotations

import pandas as pd

from view_service.backtest_framework import BacktestFramework, BacktestConfig


def test_calculate_returns_offline_price_provider():
    # One signal on 2020-01-02, hold 2 trading days: 10 -> 12 (20%).
    signals = pd.DataFrame(
        [
            {"交易日期": "2020-01-02", "股票代码": "000001", "信号类型": "test"},
        ]
    )

    prices = pd.DataFrame(
        [
            {"日期": "2020-01-02", "收盘": 10.0},
            {"日期": "2020-01-03", "收盘": 11.0},
            {"日期": "2020-01-06", "收盘": 12.0},
        ]
    )

    def price_provider(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        assert symbol == "000001"
        return prices.copy()

    fw = BacktestFramework(cache_dir="backtest_cache/test", price_provider=price_provider, data_provider=lambda *_: pd.DataFrame())
    out = fw.calculate_returns(signals, holding_period=2)
    assert len(out) == 1
    assert out[0].symbol == "000001"
    assert abs(out[0].return_pct - 0.2) < 1e-9


def test_run_backtest_limits_signals():
    df = pd.DataFrame(
        [
            {"交易日期": "2020-01-02", "股票代码": "000001", "信号类型": "a"},
            {"交易日期": "2020-01-02", "股票代码": "000001", "信号类型": "b"},
            {"交易日期": "2020-01-02", "股票代码": "000001", "信号类型": "c"},
        ]
    )

    prices = pd.DataFrame(
        [
            {"日期": "2020-01-02", "收盘": 10.0},
            {"日期": "2020-01-03", "收盘": 10.0},
            {"日期": "2020-01-06", "收盘": 10.0},
        ]
    )

    def data_provider(data_source: str, start_date: str, end_date: str, kwargs: dict) -> pd.DataFrame:
        return df.copy()

    def price_provider(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        return prices.copy()

    fw = BacktestFramework(cache_dir="backtest_cache/test2", data_provider=data_provider, price_provider=price_provider)

    cfg = BacktestConfig(
        skill_name="x",
        start_date="2020-01-01",
        end_date="2020-01-10",
        holding_period=1,
        thresholds={},
        max_signals=2,
    )

    def rule_func(d: pd.DataFrame, thresholds: dict) -> pd.DataFrame:
        return d.copy()

    res = fw.run_backtest(cfg, rule_func=rule_func, data_source="dummy")
    assert res.total_signals == 2
