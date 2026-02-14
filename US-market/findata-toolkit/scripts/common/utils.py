"""
FinData Toolkit Shared Utilities
Common functions used across all scripts.
"""
import json
import sys
import time
import functools
from datetime import datetime, date
from typing import Any


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

class JSONEncoder(json.JSONEncoder):
    """Custom encoder that handles dates, numpy types, etc."""

    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        try:
            import numpy as np
            if isinstance(obj, (np.integer,)):
                return int(obj)
            if isinstance(obj, (np.floating,)):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            if isinstance(obj, np.bool_):
                return bool(obj)
        except ImportError:
            pass
        try:
            import pandas as pd
            if isinstance(obj, pd.Timestamp):
                return obj.isoformat()
            if pd.isna(obj):
                return None
        except ImportError:
            pass
        return super().default(obj)


def output_json(data: Any, pretty: bool = True) -> str:
    """Serialize *data* to JSON and print to stdout."""
    text = json.dumps(data, cls=JSONEncoder, indent=2 if pretty else None,
                      ensure_ascii=False)
    print(text)
    return text


def output_table(headers: list[str], rows: list[list], title: str = ""):
    """Print a nicely formatted text table."""
    try:
        from tabulate import tabulate
        if title:
            print(f"\n{'='*60}")
            print(f"  {title}")
            print(f"{'='*60}")
        print(tabulate(rows, headers=headers, tablefmt="pipe",
                        floatfmt=".2f"))
    except ImportError:
        # Fallback: simple CSV-ish output
        if title:
            print(f"\n--- {title} ---")
        print(" | ".join(headers))
        print("-" * (len(" | ".join(headers))))
        for row in rows:
            print(" | ".join(str(c) for c in row))


def error_exit(message: str, code: int = 1):
    """Print an error message and exit."""
    print(json.dumps({"error": message}), file=sys.stderr)
    sys.exit(code)


# ---------------------------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------------------------

def rate_limit(calls_per_second: float = 2.0):
    """Decorator that rate-limits a function."""
    min_interval = 1.0 / calls_per_second

    def decorator(func):
        last_call = [0.0]

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            last_call[0] = time.time()
            return func(*args, **kwargs)

        return wrapper
    return decorator


# ---------------------------------------------------------------------------
# Safe numeric helpers
# ---------------------------------------------------------------------------

def safe_div(a, b, default=None):
    """Division that returns *default* when b is 0 or either value is None."""
    if a is None or b is None:
        return default
    try:
        if float(b) == 0:
            return default
        return float(a) / float(b)
    except (ValueError, TypeError):
        return default


def safe_float(val, default=None):
    """Convert *val* to float, returning *default* on failure."""
    if val is None:
        return default
    try:
        import math
        result = float(val)
        if math.isnan(result) or math.isinf(result):
            return default
        return result
    except (ValueError, TypeError):
        return default


def pct(val, decimals=2):
    """Format a decimal as a percentage string."""
    if val is None:
        return "N/A"
    return f"{val * 100:.{decimals}f}%"


def require_dependency(module_name: str, *, requirements_path: str) -> None:
    """
    Exit with an actionable message when an optional dependency is missing.

    Note: keep this in `common/utils.py` so scripts can check deps before
    doing work (and before importing heavy third-party libraries).
    """
    try:
        __import__(module_name)
    except ImportError as e:
        error_exit(
            f"Missing dependency: '{module_name}'. Install toolkit deps first (from repo root): "
            f"pip install -r {requirements_path}"
        )
