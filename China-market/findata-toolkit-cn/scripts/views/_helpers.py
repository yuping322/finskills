from __future__ import annotations

from datetime import datetime, timedelta


def today_yyyymmdd() -> str:
    return datetime.now().strftime("%Y%m%d")


def days_ago_yyyymmdd(days: int) -> str:
    return (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")


def days_from_now_yyyymmdd(days: int) -> str:
    return (datetime.now() + timedelta(days=days)).strftime("%Y%m%d")


def ensure_yyyymmdd(value: str, *, field: str) -> str:
    v = (value or "").strip().replace("-", "")
    if len(v) != 8 or not v.isdigit():
        raise ValueError(f"Invalid {field}: {value!r} (expected YYYYMMDD)")
    return v


def latest_quarter_end_yyyymmdd() -> str:
    now = datetime.now()
    candidates = [
        datetime(now.year, 3, 31),
        datetime(now.year, 6, 30),
        datetime(now.year, 9, 30),
        datetime(now.year, 12, 31),
    ]
    past = [d for d in candidates if d.date() <= now.date()]
    if past:
        return past[-1].strftime("%Y%m%d")
    return datetime(now.year - 1, 12, 31).strftime("%Y%m%d")


def view_envelope(*, view: str, params: dict, data: dict, errors: list[str], warnings: list[str], elapsed_seconds: float) -> dict:
    return {
        "meta": {
            "tool": "findata-toolkit-cn",
            "layer": "views",
            "view": view,
            "as_of": datetime.now().isoformat(timespec="seconds"),
            "elapsed_seconds": round(elapsed_seconds, 3),
            "params": params,
        },
        "data": data,
        "warnings": warnings,
        "errors": errors,
    }
