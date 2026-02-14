# View Service (FinSkills)

A small, repo-local service layer that runs **China-market** views through a stable API.

Goals:
- Keep a **view abstraction** (tool views + composed views) so upper layers never call AKShare directly.
- Make it easy to swap providers later (e.g. `akshare-one`, paid vendors, self-hosted collectors).
- Reuse existing view logic under `China-market/findata-toolkit-cn/scripts/views/`.

## Run (dev)

```bash
cd /Users/fengzhi/Downloads/git/finskills
make install-cn
source .venv/bin/activate
python -m view_service.http_server \
  --host 127.0.0.1 --port 8808 \
  --cn-toolkit-root China-market/findata-toolkit-cn
```

## HTTP API

- `GET /health`
- `GET /views` (lists available view names)
- `GET /views/<name>` (returns a minimal spec: kind, description, params schema)
- `POST /run`

`POST /run` body:

```json
{
  "name": "fund_flow_dashboard",
  "params": {
    "rank_indicator": "今日"
  },
  "refresh": false
}
```

Response envelope (consistent for all views):

```json
{
  "meta": { "view": "...", "as_of": "...", "elapsed_seconds": 0.123, "params": {} },
  "data": { "...": { "meta": {}, "data": [], "warnings": [], "errors": [] } },
  "warnings": [],
  "errors": []
}
```

## Notes

- This service currently depends on:
  - `China-market/findata-toolkit-cn/config/litellm_tools.json` (tool schemas)
  - `China-market/findata-toolkit-cn/scripts/views/*.py` (custom view planning)
- Tool views are 1:1 with tool names (function names in the registry).
- Provider swap plan:
  - Keep view names stable.
  - Replace the provider implementation for tool calls.
