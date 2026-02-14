# Development Notes

## Running tests

From repo root:

```bash
make install-cn
source .venv/bin/activate
python -m unittest discover -s view-service/tests -p 'test_*.py'
```

## Smoke check (CN skills)

Validate that every China-market skill’s dependent views exist and custom view plans can be built:

```bash
make cn-smoke-validate
```

Run (actually calls the provider; requires network + installed akshare deps):

```bash
source .venv/bin/activate
python -m view_service.smoke_cn_skills --mode run --repo-root . --out-json docs/smoke-run-cn.json --limit-skills 5
```

## View source of truth (CN)

- Tool schemas: `China-market/findata-toolkit-cn/config/litellm_tools.json`
- Custom view planning: `China-market/findata-toolkit-cn/scripts/views/*.py`

## Dependency artifacts (generated)

These are for planning / lineage, not for executing views:

- Skill → views index: `docs/view-deps.json`
- Per-view specs (plan snapshots): `docs/view-specs/*.json`
- Data lineage (primitive/provider impact): `docs/data-lineage.md`
