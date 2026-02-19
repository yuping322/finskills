from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, List, Optional

import pandas as pd

from ..backtest_framework import BacktestConfig, BacktestFramework


def _to_ymd10(x: Any) -> str:
    s = str(x or "").strip()
    if not s:
        return ""
    if len(s) >= 10 and s[4] == "-" and s[7] == "-":
        return s[:10]
    if len(s) >= 8 and s[:8].isdigit():
        return f"{s[:4]}-{s[4:6]}-{s[6:8]}"
    return s[:10]


def enrich_block_deal_features(
    framework: BacktestFramework,
    df: pd.DataFrame,
    *,
    start: str,
    end: str,
    max_symbols: int = 0,
) -> pd.DataFrame:
    """
    Add required derived columns:
    - 折价率 = (成交价 - 收盘价) / 收盘价
    - 大宗成交额 = 成交额
    - 成交金额占比 = 大宗成交额 / 当日成交额
    - 日均成交额 = 近20日成交额均值（含当日）

    This is potentially expensive if df contains too many unique symbols.
    """
    if df.empty:
        return df

    out = df.copy()

    # Normalize expected columns
    if "交易日期" not in out.columns and "日期" in out.columns:
        out = out.rename(columns={"日期": "交易日期"})
    if "股票代码" not in out.columns and "代码" in out.columns:
        out = out.rename(columns={"代码": "股票代码"})
    if "成交价" not in out.columns and "成交价格" in out.columns:
        out = out.rename(columns={"成交价格": "成交价"})
    if "成交额" not in out.columns and "成交金额" in out.columns:
        out = out.rename(columns={"成交金额": "成交额"})

    need_cols = {"交易日期", "股票代码", "成交价", "成交额"}
    missing = [c for c in need_cols if c not in out.columns]
    if missing:
        raise ValueError(f"stock_dzjy_mrmx missing columns: {missing}")

    out["交易日期"] = out["交易日期"].map(_to_ymd10)
    out["股票代码"] = out["股票代码"].astype(str)

    # Limit symbols (optional) by total block amount.
    if max_symbols and max_symbols > 0:
        top = (
            out.groupby("股票代码")["成交额"]
            .sum()
            .sort_values(ascending=False)
            .head(int(max_symbols))
            .index.tolist()
        )
        out = out[out["股票代码"].isin(top)].copy()

    # Pull price history per symbol; join on date.
    frames: list[pd.DataFrame] = []
    for sym in sorted(set(out["股票代码"].tolist())):
        px = framework.get_price_history(sym, start, end).copy()
        if px.empty:
            continue
        if "日期" not in px.columns and "date" in px.columns:
            px = px.rename(columns={"date": "日期"})
        if "收盘" not in px.columns and "close" in px.columns:
            px = px.rename(columns={"close": "收盘"})
        if "成交额" not in px.columns and "amount" in px.columns:
            px = px.rename(columns={"amount": "成交额"})
        if "日期" not in px.columns or "收盘" not in px.columns or "成交额" not in px.columns:
            continue

        px["日期"] = px["日期"].astype(str).map(_to_ymd10)
        px = px.sort_values("日期")
        px["日均成交额"] = px["成交额"].astype(float).rolling(20, min_periods=1).mean()
        px["股票代码"] = sym
        one = px[["股票代码", "日期", "收盘", "成交额", "日均成交额"]].copy()
        one = one.rename(columns={"成交额": "当日成交额"})
        frames.append(one)

    if not frames:
        raise ValueError("No price history loaded; cannot compute discount.")

    px_all = pd.concat(frames, ignore_index=True)
    merged = out.merge(px_all, left_on=["股票代码", "交易日期"], right_on=["股票代码", "日期"], how="left").drop(columns=["日期"])

    merged["大宗成交额"] = merged["成交额"].astype(float)
    merged["收盘价"] = merged["收盘"].astype(float)
    merged["折价率"] = (merged["成交价"].astype(float) - merged["收盘价"]) / merged["收盘价"]
    merged["成交金额占比"] = merged["大宗成交额"] / merged["当日成交额"].astype(float)

    merged = merged.drop(columns=["收盘", "成交额", "收盘价"])

    merged = merged.dropna(subset=["折价率", "成交金额占比", "日均成交额"])
    return merged


def rule_1_building_position(df: pd.DataFrame, thresholds: dict[str, Any]) -> pd.DataFrame:
    df = df.copy()
    if "折价率" not in df.columns:
        raise ValueError("Missing column: 折价率.")
    discount_min = thresholds.get("discount_rate_min", -0.05)
    discount_max = thresholds.get("discount_rate_max", -0.02)
    signals = df[(df["折价率"] >= discount_min) & (df["折价率"] <= discount_max)].copy()
    signals["信号类型"] = "建仓型"
    return signals


def run(
    framework: BacktestFramework,
    *,
    start: str,
    end: str,
    holding: int,
    max_signals: int,
    symbol: str,
    max_symbols: int,
) -> dict[str, Any]:
    cfg = BacktestConfig(
        skill_name="block-deal-monitor",
        start_date=start,
        end_date=end,
        holding_period=holding,
        thresholds={
            "discount_rate_min": -0.05,
            "discount_rate_max": -0.02,
            "consecutive_days": 3,
            "avg_discount_change": 0.01,
        },
        max_signals=max_signals,
    )
    raw = framework.get_historical_data("stock_dzjy_mrmx", start, end, symbol=symbol, start_date=start, end_date=end)
    feat = enrich_block_deal_features(framework, raw, start=start, end=end, max_symbols=max_symbols)

    signals = rule_1_building_position(feat, cfg.thresholds)
    if cfg.max_signals and cfg.max_signals > 0 and len(signals) > cfg.max_signals:
        signals = signals.head(cfg.max_signals).copy()

    results = framework.calculate_returns(signals, cfg.holding_period)
    stats = framework.analyze_results(results)

    from ..backtest_framework import BacktestResult  # local import to keep file focused

    return BacktestResult(config=cfg, signals=results, **stats).to_dict()


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Backtest: block-deal-monitor thresholds (skeleton)")
    p.add_argument("--start", default="2020-01-01")
    p.add_argument("--end", default="2023-12-31")
    p.add_argument("--holding", type=int, default=20)
    p.add_argument("--max-signals", type=int, default=2000)
    p.add_argument("--symbol", default="A股", help="AKShare stock_dzjy_mrmx symbol arg (e.g. A股)")
    p.add_argument("--max-symbols", type=int, default=200)
    p.add_argument("--cache-dir", default="backtest_cache/block_deal")
    p.add_argument("--out", default="backtest_results/block_deal/rule1_building_position.json")
    args = p.parse_args(argv)

    fw = BacktestFramework(cache_dir=args.cache_dir)
    out = run(
        fw,
        start=args.start,
        end=args.end,
        holding=args.holding,
        max_signals=args.max_signals,
        symbol=args.symbol,
        max_symbols=args.max_symbols,
    )

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
