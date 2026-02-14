from __future__ import annotations

import argparse
import json
import re
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .provider_akshare import AkshareProvider
from .tool_registry import ToolRegistry
from .view_runner import run_view
from .views_cn import ViewSpec, discover_custom_views, build_tool_views


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _schema_required(schema: dict[str, Any] | None) -> list[str]:
    if not isinstance(schema, dict):
        return []
    req = schema.get("required")
    if isinstance(req, list):
        return [str(x) for x in req]
    return []


def _schema_properties(schema: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(schema, dict):
        return {}
    props = schema.get("properties")
    return props if isinstance(props, dict) else {}


def _sample_params(schema: dict[str, Any] | None) -> dict[str, Any]:
    """
    Best-effort sample params for required fields only.
    Designed to keep calls lightweight and deterministic.
    """
    if not isinstance(schema, dict):
        return {}
    props = _schema_properties(schema)
    req = [r for r in _schema_required(schema) if r not in {"timeout", "token"}]
    out: dict[str, Any] = {}

    def _first_enum(p: dict[str, Any] | None) -> str | None:
        if not isinstance(p, dict):
            return None
        enum = p.get("enum")
        if isinstance(enum, list) and enum:
            return str(enum[0])
        return None

    def _extract_example(desc: str, key: str) -> str | None:
        # e.g. symbol="SZ000665"
        m = re.search(rf'{re.escape(key)}\s*=\s*"([^"]+)"', desc)
        if m:
            return m.group(1)
        m = re.search(rf"{re.escape(key)}\s*=\s*'([^']+)'", desc)
        if m:
            return m.group(1)
        return None

    def _extract_choice(desc: str) -> str | None:
        # e.g. choice of {"今日", "5日", "10日"} or choice of {'年报', ...}
        m = re.search(r"choice of\s*\{([^}]+)\}", desc)
        if not m:
            return None
        body = m.group(1)
        # Split by comma, strip whitespace and quotes/brackets.
        parts = []
        for raw in body.split(","):
            s = raw.strip().strip("“”\"' ")
            if not s:
                continue
            parts.append(s)
        return parts[0] if parts else None

    for k in req:
        ks = str(k)
        p = props.get(ks) if isinstance(props, dict) else None
        typ = (p or {}).get("type") if isinstance(p, dict) else None
        kl = ks.lower()
        desc = str((p or {}).get("description", "")) if isinstance(p, dict) else ""

        enum_val = _first_enum(p if isinstance(p, dict) else None)
        if enum_val is not None:
            out[ks] = enum_val
            continue

        example_val = _extract_example(desc, ks)
        if example_val is not None:
            out[ks] = example_val
            continue

        choice_val = _extract_choice(desc)
        if choice_val is not None:
            out[ks] = choice_val
            continue

        if typ == "boolean":
            out[ks] = False
        elif typ == "integer":
            out[ks] = 0
        elif typ == "number":
            out[ks] = 0.0
        else:
            if "symbol" in kl:
                # Prefer leading zeros for A-share stock code.
                # Heuristics for non-stock symbols.
                if "概念" in desc:
                    out[ks] = "AI应用"
                elif "行业" in desc:
                    out[ks] = "半导体"
                else:
                    out[ks] = "000001"
            elif kl in {"start_date", "end_date"}:
                out[ks] = "20250101"
            elif "date" in kl:
                out[ks] = "20250101"
            elif "period" in kl:
                out[ks] = "daily"
            elif "adjust" in kl:
                out[ks] = "qfq"
            elif "indicator" in kl:
                # Often expects 今日/5日/10日 etc.
                out[ks] = "今日" if "今日" in desc else "按报告期"
            elif kl == "category":
                # Commonly required for cninfo disclosure search.
                out[ks] = "公司治理"
            elif "flag" in kl:
                out[ks] = "default"
            else:
                out[ks] = "demo"

    # Some known required params are pseudo-optional in practice; provide safe defaults if present.
    if "timeout" in props and "timeout" not in out:
        out["timeout"] = int(os.getenv("FINSKILLS_DEFAULT_TIMEOUT", "10"))
    if "token" in props and "token" not in out:
        out["token"] = None

    return out


def _build_views(cn_toolkit_root: Path, registry: ToolRegistry) -> dict[str, ViewSpec]:
    custom = discover_custom_views(cn_toolkit_root / "scripts" / "views")
    tools = build_tool_views(sorted(registry.tool_index.keys()))
    merged = dict(tools)
    merged.update(custom)

    # Fill tool view schema/desc from registry.
    for name, spec in list(merged.items()):
        if spec.kind != "tool_view":
            continue
        fn = registry.describe(name) or {}
        desc = fn.get("description") if isinstance(fn, dict) else ""
        schema = fn.get("parameters") if isinstance(fn, dict) else None
        if not isinstance(schema, dict):
            schema = {"type": "object", "properties": {}, "required": []}
        merged[name] = ViewSpec(
            name=name,
            kind="tool_view",
            description=str(desc or ""),
            params_schema=schema,
            module=None,
        )

    return merged


@dataclass(frozen=True)
class SmokeItemResult:
    skill: str
    view: str
    ok: bool
    mode: str  # validate|run
    error: str | None


def _view_run_ok(*, spec: ViewSpec, result: dict[str, Any]) -> bool:
    """
    Define 'ok' as: the view returned at least some usable data.
    - tool_view: requires its single envelope to have non-null `data` and empty `errors`.
    - custom_view: requires at least one child envelope to have non-null `data` and empty `errors`.
    """
    data = result.get("data") or {}
    if not isinstance(data, dict):
        return False

    if spec.kind == "tool_view":
        env = data.get(spec.name) if isinstance(data, dict) else None
        if not isinstance(env, dict):
            return False
        if env.get("data") is None:
            return False
        errs = env.get("errors") or []
        return not errs

    if spec.kind == "custom_view":
        for env in data.values():
            if not isinstance(env, dict):
                continue
            if env.get("data") is None:
                continue
            errs = env.get("errors") or []
            if not errs:
                return True
        return False

    return False


def _validate_view_exists(views: dict[str, ViewSpec], name: str) -> str | None:
    if name not in views:
        return f"Unknown view: {name}"
    spec = views[name]
    if spec.kind == "custom_view":
        if not spec.module or not hasattr(spec.module, "plan") or not callable(getattr(spec.module, "plan")):
            return f"Invalid custom view module: {name}"
    return None


def _validate_view_plan(spec: ViewSpec) -> str | None:
    if spec.kind != "custom_view":
        return None
    try:
        _ = spec.module.plan({})  # type: ignore[union-attr]
        return None
    except Exception:
        # Some views require params. Validate with required-only sample.
        try:
            sample = _sample_params(spec.params_schema)
            _ = spec.module.plan(sample)  # type: ignore[union-attr]
            return None
        except Exception as e:
            return f"Plan build failed: {e}"


def main() -> int:
    p = argparse.ArgumentParser(description="Smoke test CN skills via view-service")
    p.add_argument("--repo-root", default=".", help="Repo root (default: .)")
    p.add_argument("--cn-toolkit-root", default="China-market/findata-toolkit-cn")
    p.add_argument("--deps-json", default="docs/view-deps.json")
    p.add_argument("--mode", choices=["validate", "run"], default="validate", help="validate: no network calls; run: actually call provider")
    p.add_argument("--only-skill", default="", help="Regex filter for skill name")
    p.add_argument("--only-view", default="", help="Regex filter for view name")
    p.add_argument("--limit-skills", type=int, default=0, help="Limit number of skills to process")
    p.add_argument("--limit-views", type=int, default=0, help="Limit number of views per skill")
    p.add_argument("--refresh", action="store_true", help="Bypass cache (if provider supports)")
    p.add_argument("--dedupe-views", action="store_true", default=True, help="Run each view at most once (default: true)")
    p.add_argument("--no-dedupe-views", action="store_false", dest="dedupe_views", help="Run views per-skill (slower)")
    p.add_argument("--no-proxy", action="store_true", help="Force-disable proxy env vars during calls")
    p.add_argument("--out-json", default="", help="Write per-item results JSON to path")
    args = p.parse_args()

    repo_root = Path(args.repo_root).resolve()
    cn_root = (repo_root / args.cn_toolkit_root).resolve()
    deps_path = (repo_root / args.deps_json).resolve()

    if not deps_path.exists():
        print(f"deps json not found: {deps_path}", file=sys.stderr)
        return 2

    tools_json = cn_root / "config" / "litellm_tools.json"
    registry = ToolRegistry.load(tools_json)
    provider = AkshareProvider(registry=registry)
    views = _build_views(cn_root, registry)

    if args.no_proxy:
        os.environ["FINSKILLS_FORCE_NO_PROXY"] = "1"

    if args.mode == "run":
        # Keep runs bounded: allow providers to return lightweight data for very heavy endpoints.
        os.environ.setdefault("FINSKILLS_SMOKE", "1")

    deps = _read_json(deps_path)
    china: dict[str, dict[str, Any]] = deps.get("china") or {}

    only_skill = re.compile(args.only_skill) if args.only_skill else None
    only_view = re.compile(args.only_view) if args.only_view else None

    results: list[SmokeItemResult] = []
    failures = 0
    view_cache: dict[str, dict[str, Any]] = {}

    skills = sorted(china.keys())
    if only_skill:
        skills = [s for s in skills if only_skill.search(s)]
    if args.limit_skills and args.limit_skills > 0:
        skills = skills[: args.limit_skills]

    for skill in skills:
        skill_views = list(china.get(skill, {}).get("views") or [])
        if only_view:
            skill_views = [v for v in skill_views if only_view.search(str(v))]
        if args.limit_views and args.limit_views > 0:
            skill_views = skill_views[: args.limit_views]

        for view_name in skill_views:
            view_name = str(view_name)

            err = _validate_view_exists(views, view_name)
            if not err:
                err = _validate_view_plan(views[view_name])

            if args.mode == "validate":
                ok = err is None
                results.append(SmokeItemResult(skill=skill, view=view_name, ok=ok, mode="validate", error=err))
                if not ok:
                    failures += 1
                continue

            # run mode
            if err:
                results.append(SmokeItemResult(skill=skill, view=view_name, ok=False, mode="run", error=err))
                failures += 1
                continue

            spec = views[view_name]
            params = _sample_params(spec.params_schema)
            try:
                if args.dedupe_views and view_name in view_cache:
                    out_dict = view_cache[view_name]
                else:
                    print(f"[run] view={view_name}", file=sys.stderr)
                    out = run_view(spec, params=params, provider=provider, refresh=bool(args.refresh))
                    out_dict = out.to_dict()
                    if args.dedupe_views:
                        view_cache[view_name] = out_dict

                ok = _view_run_ok(spec=spec, result=out_dict)
                err_text = None
                if not ok:
                    errs = out_dict.get("errors") or []
                    err_text = "; ".join(str(x) for x in errs) if errs else "no usable data"
                results.append(SmokeItemResult(skill=skill, view=view_name, ok=ok, mode="run", error=err_text))
                if not ok:
                    failures += 1
            except Exception as e:
                results.append(SmokeItemResult(skill=skill, view=view_name, ok=False, mode="run", error=str(e)))
                failures += 1

    payload = {
        "mode": args.mode,
        "skills": len(skills),
        "items": len(results),
        "failures": failures,
        "results": [r.__dict__ for r in results],
    }

    if args.out_json:
        out_path = Path(args.out_json).expanduser().resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({k: payload[k] for k in ["mode", "skills", "items", "failures"]}, ensure_ascii=False, indent=2))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
