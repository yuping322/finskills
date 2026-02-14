from __future__ import annotations

VIEW_NAME = "ab_ah_premium_dashboard"
DESCRIPTION = "AB/AH 比价聚合：AB股比价与AH股实时行情（工具聚合视图）。"
PARAMS_SCHEMA = {"type": "object", "properties": {}, "required": []}


def plan(params: dict) -> list[dict]:
    return [
        {"key": "ab_comparison", "tool": "stock_zh_ab_comparison_em", "args": {}},
        {"key": "ah_spot_em", "tool": "stock_zh_ah_spot_em", "args": {}},
        {"key": "ah_spot", "tool": "stock_zh_ah_spot", "args": {}},
        {"key": "ah_name", "tool": "stock_zh_ah_name", "args": {}},
    ]

