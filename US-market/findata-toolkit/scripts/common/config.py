"""
FinData Toolkit Configuration Manager
Load data source configuration and API keys.
"""
import os
import json
from pathlib import Path


# Base paths
SCRIPT_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = SCRIPT_DIR.parent
CONFIG_DIR = PROJECT_DIR / "config"


def get_config() -> dict:
    """Load configuration from YAML or return defaults."""
    try:
        import yaml
        config_path = CONFIG_DIR / "data_sources.yaml"
        if config_path.exists():
            with open(config_path) as f:
                cfg = yaml.safe_load(f)
            # Resolve environment variable references
            _resolve_env_vars(cfg)
            return cfg
    except ImportError:
        pass

    # Fallback defaults (no external config needed)
    return {
        "us_market": {
            "primary": {
                "stock_data": "yahoo_finance",
                "filings": "sec_edgar",
                "macro": "fred",
            },
            "optional": {
                "alpha_vantage_key": os.getenv("ALPHA_VANTAGE_API_KEY"),
            },
        },
        "sec_edgar": {
            "user_agent": os.getenv(
                "SEC_EDGAR_USER_AGENT", "FinSkills research@example.com"
            ),
        },
        "rate_limits": {
            "yahoo_finance": 2,
            "sec_edgar": 10,
            "fred": 5,
        },
    }


def _resolve_env_vars(obj):
    """Recursively resolve ${ENV_VAR} references in config values."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and v.startswith("${") and v.endswith("}"):
                env_key = v[2:-1]
                obj[k] = os.getenv(env_key)
            elif isinstance(v, (dict, list)):
                _resolve_env_vars(v)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, str) and v.startswith("${") and v.endswith("}"):
                env_key = v[2:-1]
                obj[i] = os.getenv(env_key)
            elif isinstance(v, (dict, list)):
                _resolve_env_vars(v)
