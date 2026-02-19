"""
Compatibility shim.

Prefer importing from `view_service.backtest_framework` and running backtests via
`python -m view_service.backtests.<name>`.
"""

from view_service.backtest_framework import *  # noqa: F401,F403

