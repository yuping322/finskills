from __future__ import annotations

VIEW_NAME = "concept_board_snapshot"
DESCRIPTION = "概念板块快照：概念列表 + 实时行情（工具聚合视图）。"
PARAMS_SCHEMA = {"type": "object", "properties": {}, "required": []}


def plan(params: dict) -> list[dict]:
    return [
        {"key": "concept_list", "tool": "stock_board_concept_name_em", "args": {}},
        {"key": "concept_spot", "tool": "stock_board_concept_spot_em", "args": {}},
    ]

