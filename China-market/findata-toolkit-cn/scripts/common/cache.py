"""
File cache for FinData Toolkit (CN).

This mirrors the caching approach used by the AKShare MCP server, but is
implemented locally so toolkit scripts can benefit without running MCP.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional


@dataclass(frozen=True)
class CacheTTL:
    realtime: float = 60  # seconds
    daily: float = 3600
    historical: float = float("inf")
    static: float = 7 * 24 * 3600
    default: float = 3600


def _default_cache_dir() -> Path:
    # Prefer env override so users can place caches outside the repo if desired.
    env_dir = os.getenv("FINSKILLS_CACHE_DIR")
    if env_dir:
        return Path(env_dir).expanduser()
    # Default: skill-local cache directory.
    return Path(__file__).resolve().parent.parent.parent / "cache"


class CacheManager:
    def __init__(
        self,
        cache_dir: Optional[Path] = None,
        *,
        enabled: bool = True,
        ttl: CacheTTL | None = None,
    ) -> None:
        self.enabled = enabled
        self.cache_dir = (cache_dir or _default_cache_dir()).resolve()
        self.ttl = ttl or CacheTTL()

        if self.enabled:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_cache_key(self, name: str, arguments: dict[str, Any]) -> str:
        key_data = f"{name}:{json.dumps(arguments, sort_keys=True, ensure_ascii=False)}"
        return hashlib.md5(key_data.encode("utf-8")).hexdigest()

    def get_cache_path(self, cache_key: str) -> Path:
        return self.cache_dir / f"{cache_key}.json"

    def get_ttl(self, name: str) -> float:
        name_lower = name.lower()

        # Heuristics: keep simple and overridable.
        if any(k in name_lower for k in ["spot", "realtime", "real_time", "current", "bid_ask", "intraday"]):
            return self.ttl.realtime
        if any(k in name_lower for k in ["hist", "daily", "minute", "min", "tick", "kline"]):
            return self.ttl.historical
        if any(k in name_lower for k in ["info", "name", "code", "list", "category", "profile", "components", "cons"]):
            return self.ttl.static
        return self.ttl.default

    def load(self, cache_key: str, ttl: float) -> Optional[dict[str, Any]]:
        if not self.enabled:
            return None

        cache_path = self.get_cache_path(cache_key)
        if not cache_path.exists():
            return None

        try:
            payload = json.loads(cache_path.read_text(encoding="utf-8"))
        except Exception:
            return None

        cached_time = float(payload.get("timestamp", 0))
        if ttl != float("inf"):
            age = time.time() - cached_time
            if age > ttl:
                return None

        return payload

    def save(self, cache_key: str, result: Any) -> None:
        if not self.enabled:
            return

        from .utils import JSONEncoder

        cache_path = self.get_cache_path(cache_key)
        payload = {
            "timestamp": time.time(),
            "result": result,
        }

        cache_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, cls=JSONEncoder),
            encoding="utf-8",
        )

    def clear(self) -> int:
        if not self.enabled or not self.cache_dir.exists():
            return 0

        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
                count += 1
            except Exception:
                continue
        return count

    def stats(self) -> dict[str, Any]:
        if not self.enabled or not self.cache_dir.exists():
            return {"enabled": False, "count": 0, "size_mb": 0.0, "cache_dir": str(self.cache_dir)}

        files = list(self.cache_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in files)
        return {
            "enabled": True,
            "count": len(files),
            "size_mb": round(total_size / 1024 / 1024, 2),
            "cache_dir": str(self.cache_dir),
        }

