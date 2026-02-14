from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class ToolResult:
    meta: dict[str, Any]
    data: Any
    warnings: list[str]
    errors: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {"meta": self.meta, "data": self.data, "warnings": self.warnings, "errors": self.errors}


class ToolProvider(Protocol):
    def call_tool(self, name: str, args: dict[str, Any], *, refresh: bool, meta_script: str) -> ToolResult: ...

