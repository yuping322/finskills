.PHONY: venv install-cn cn-healthcheck cn-smoke-validate

VENV_DIR := .venv
VENV_PY  := $(VENV_DIR)/bin/python

define ensure_venv
PY=$$(command -v python3.12 2>/dev/null || command -v python3.11 2>/dev/null || command -v python3.10 2>/dev/null); \
if [ -z "$$PY" ]; then \
  echo "ERROR: Python 3.10–3.12 is required (python3.10/python3.11/python3.12 not found)."; \
  exit 2; \
fi; \
if [ ! -d "$(VENV_DIR)" ]; then \
  echo "Creating venv at $(VENV_DIR) using $$PY"; \
  $$PY -m venv "$(VENV_DIR)"; \
fi; \
$(VENV_PY) -m pip install -U pip setuptools wheel >/dev/null
endef

venv:
	@$(ensure_venv)

install-cn: venv
	@$(VENV_PY) -m pip install -e view-service
	@$(VENV_PY) -m pip install -r China-market/findata-toolkit-cn/requirements.txt

cn-smoke-validate: install-cn
	@$(VENV_PY) -m view_service.smoke_cn_skills --mode validate --repo-root . --out-json docs/smoke-validate-cn.json

cn-healthcheck: install-cn
	@$(VENV_PY) -m view_service.healthcheck_cn --repo-root . --out-json docs/healthcheck-cn.json
