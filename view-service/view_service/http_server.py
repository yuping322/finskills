from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .provider_akshare import AkshareProvider
from .tool_registry import ToolRegistry
from .view_runner import run_view
from .views_cn import ViewSpec, build_tool_views, discover_custom_views


def _json_response(handler: BaseHTTPRequestHandler, status: int, payload: dict[str, Any]) -> None:
    raw = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(raw)))
    handler.end_headers()
    handler.wfile.write(raw)


class ViewServiceHandler(BaseHTTPRequestHandler):
    registry: ToolRegistry
    provider: AkshareProvider
    views: dict[str, ViewSpec]

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        # Keep stdout clean by default; uncomment if needed.
        return

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            return _json_response(self, 200, {"ok": True})

        if self.path == "/views":
            names = sorted(self.views.keys())
            return _json_response(self, 200, {"views": names, "count": len(names)})

        if self.path.startswith("/views/"):
            name = self.path[len("/views/") :].strip()
            spec = self.views.get(name)
            if not spec:
                return _json_response(self, 404, {"error": f"Unknown view: {name}"})
            return _json_response(
                self,
                200,
                {
                    "name": spec.name,
                    "kind": spec.kind,
                    "description": spec.description,
                    "params_schema": spec.params_schema,
                },
            )

        return _json_response(self, 404, {"error": "Not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/run":
            return _json_response(self, 404, {"error": "Not found"})

        try:
            length = int(self.headers.get("Content-Length") or "0")
            body = self.rfile.read(length) if length > 0 else b"{}"
            req = json.loads(body.decode("utf-8"))
        except Exception as e:
            return _json_response(self, 400, {"error": f"Invalid JSON body: {e}"})

        name = (req.get("name") or "").strip()
        params = req.get("params") or {}
        refresh = bool(req.get("refresh") or False)

        if not name:
            return _json_response(self, 400, {"error": "Missing 'name'"})
        if not isinstance(params, dict):
            return _json_response(self, 400, {"error": "'params' must be an object"})

        spec = self.views.get(name)
        if not spec:
            return _json_response(self, 404, {"error": f"Unknown view: {name}"})

        result = run_view(spec, params=params, provider=self.provider, refresh=refresh)
        return _json_response(self, 200, result.to_dict())


def _build_views(cn_toolkit_root: Path, registry: ToolRegistry) -> dict[str, ViewSpec]:
    custom = discover_custom_views(cn_toolkit_root / "scripts" / "views")
    tools = build_tool_views(sorted(registry.tool_index.keys()))

    # Custom views take precedence over tool views.
    merged = dict(tools)
    merged.update(custom)

    # Fill missing description/schema for tool views from registry.
    for name, spec in list(merged.items()):
        if spec.kind != "tool_view":
            continue
        fn = registry.describe(name) or {}
        desc = fn.get("description") if isinstance(fn, dict) else ""
        schema = fn.get("parameters") if isinstance(fn, dict) else None
        if not isinstance(schema, dict):
            schema = {"type": "object", "properties": {}, "required": []}
        merged[name] = ViewSpec(
            name=spec.name,
            kind="tool_view",
            description=str(desc or ""),
            params_schema=schema,
            module=None,
        )

    return merged


def main() -> int:
    p = argparse.ArgumentParser(description="FinSkills View Service (CN)")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8808)
    p.add_argument("--cn-toolkit-root", default="China-market/findata-toolkit-cn")
    args = p.parse_args()

    cn_root = Path(args.cn_toolkit_root).resolve()
    tools_json = cn_root / "config" / "litellm_tools.json"
    registry = ToolRegistry.load(tools_json)
    provider = AkshareProvider(registry=registry)
    views = _build_views(cn_root, registry)

    def handler_factory(*_args, **_kwargs):
        cls = ViewServiceHandler
        cls.registry = registry
        cls.provider = provider
        cls.views = views
        return cls(*_args, **_kwargs)

    httpd = ThreadingHTTPServer((args.host, args.port), handler_factory)
    print(f"Listening on http://{args.host}:{args.port} (views={len(views)})")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

