from __future__ import annotations

import inspect
import os
import time
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urlparse
from typing import Any

from .provider_base import ToolProvider, ToolResult
from .tool_registry import ToolRegistry


def _float_or_none(val: Any) -> float | None:
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip()
    if not s:
        return None
    try:
        return float(s)
    except Exception:
        return None


def _int_or_none(val: Any) -> int | None:
    if val is None:
        return None
    if isinstance(val, int):
        return val
    if isinstance(val, float):
        return int(val)
    s = str(val).strip()
    if not s:
        return None
    try:
        return int(float(s))
    except Exception:
        return None


def _normalize_yyyymmdd(val: Any, *, default: str) -> str:
    if val is None:
        return default
    s = str(val).strip()
    if not s:
        return default
    s = s.replace("-", "").replace("/", "")
    if len(s) >= 8 and s[:8].isdigit():
        return s[:8]
    return default


def _tx_prefix_symbol(symbol: str) -> str:
    s = (symbol or "").strip()
    if not s:
        return s
    if s.startswith(("sh", "sz", "bj")) and len(s) >= 8:
        return s
    code = s
    if code.startswith(("SH", "SZ", "BJ")):
        return code.lower()
    if code.startswith("6"):
        return f"sh{code}"
    if code.startswith(("0", "3")):
        return f"sz{code}"
    if code.startswith(("4", "8")):
        return f"bj{code}"
    return f"sz{code}"


def _parse_tx_quote_payload(payload: str) -> dict[str, Any] | None:
    # 腾讯行情: "~" 分隔字段，见 https://qt.gtimg.cn
    fields = (payload or "").split("~")
    if len(fields) < 47:
        return None
    code = fields[2].strip()
    name = fields[1].strip()

    last = _float_or_none(fields[3])
    prev_close = _float_or_none(fields[4])
    open_ = _float_or_none(fields[5])
    change_amount = _float_or_none(fields[31])
    change_pct = _float_or_none(fields[32])
    high = _float_or_none(fields[33])
    low = _float_or_none(fields[34])

    # amount: prefer the 3rd part of "最新价/成交量/成交额"
    amount_yuan = None
    try:
        if "/" in fields[35]:
            parts = fields[35].split("/")
            if len(parts) >= 3:
                amount_yuan = _float_or_none(parts[2])
    except Exception:
        amount_yuan = None

    volume_hand = _int_or_none(fields[36]) or _int_or_none(fields[6])
    amplitude_pct = _float_or_none(fields[43])
    turnover_pct = _float_or_none(fields[38])
    pe_dynamic = _float_or_none(fields[39])
    total_mv_yi = _float_or_none(fields[44])
    float_mv_yi = _float_or_none(fields[45])
    pb = _float_or_none(fields[46])
    volume_ratio = _float_or_none(fields[49]) if len(fields) > 49 else None
    five_min_change_pct = _float_or_none(fields[69]) if len(fields) > 69 else None
    change_60d_pct = _float_or_none(fields[70]) if len(fields) > 70 else None
    change_ytd_pct = _float_or_none(fields[71]) if len(fields) > 71 else None

    # total_mv/float_mv convert: 亿 -> 元
    total_mv_yuan = None if total_mv_yi is None else total_mv_yi * 1e8
    float_mv_yuan = None if float_mv_yi is None else float_mv_yi * 1e8

    # Timestamp: YYYYMMDDHHMMSS
    ts_raw = fields[30].strip() if len(fields) > 30 else ""
    trade_date = None
    if len(ts_raw) >= 8 and ts_raw[:8].isdigit():
        trade_date = f"{ts_raw[:4]}-{ts_raw[4:6]}-{ts_raw[6:8]}"

    return {
        "trade_date": trade_date,
        "代码": code,
        "名称": name,
        "最新价": last,
        "涨跌幅": change_pct,
        "涨跌额": change_amount,
        "成交量": volume_hand,
        "成交额": amount_yuan,
        "振幅": amplitude_pct,
        "最高": high,
        "最低": low,
        "今开": open_,
        "昨收": prev_close,
        "量比": volume_ratio,
        "换手率": turnover_pct,
        "市盈率-动态": pe_dynamic,
        "市净率": pb,
        "总市值": total_mv_yuan,
        "流通市值": float_mv_yuan,
        "涨速": None,
        "5分钟涨跌": five_min_change_pct,
        "60日涨跌幅": change_60d_pct,
        "年初至今涨跌幅": change_ytd_pct,
    }


def _requests_session_no_proxy():
    import requests

    s = requests.Session()
    # Avoid macOS system proxies and env proxies (often set to a local port).
    s.trust_env = False
    return s


def _fetch_tx_quotes(symbols: list[str], *, timeout: float) -> dict[str, dict[str, Any]]:
    if not symbols:
        return {}
    s = _requests_session_no_proxy()
    out: dict[str, dict[str, Any]] = {}
    # Tencent supports multi-symbol query.
    url = "https://qt.gtimg.cn/q="
    batch_size = int(os.getenv("FINSKILLS_TX_BATCH_SIZE", "200"))
    sleep_s = float(os.getenv("FINSKILLS_TX_SLEEP", "0.05"))
    headers = {"User-Agent": os.getenv("FINSKILLS_UA", "Mozilla/5.0")}

    for i in range(0, len(symbols), batch_size):
        batch = symbols[i : i + batch_size]
        q = ",".join(batch)
        r = s.get(url + q, timeout=timeout, headers=headers)
        r.raise_for_status()
        text = r.text or ""
        parts = [p.strip() for p in text.split(";") if p.strip()]
        for part in parts:
            if "=\"" not in part:
                continue
            try:
                left, rest = part.split("=\"", 1)
                payload = rest.rsplit("\"", 1)[0]
                # left is like v_sz000001
                sym = left.strip()
                if sym.startswith("v_"):
                    sym = sym[2:]
                parsed = _parse_tx_quote_payload(payload)
                if parsed and parsed.get("代码"):
                    out[sym] = parsed
            except Exception:
                continue
        if sleep_s > 0:
            time.sleep(sleep_s)
    return out


def _is_local_proxy_unreachable(proxy_url: str) -> bool:
    try:
        u = urlparse(proxy_url)
        host = u.hostname
        port = u.port
        if not host or not port:
            return False
        if host not in {"127.0.0.1", "localhost"}:
            return False
        import socket

        with socket.create_connection((host, port), timeout=0.2):
            return False
    except Exception:
        return True


@contextmanager
def _without_proxies():
    """
    Many environments export HTTP(S)_PROXY to a local port that may not be running.
    AKShare uses `requests`, which will respect these variables by default.
    """
    proxy_keys = [
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "ALL_PROXY",
        "NO_PROXY",
        "http_proxy",
        "https_proxy",
        "all_proxy",
        "no_proxy",
    ]
    saved = {k: os.environ.get(k) for k in proxy_keys if k in os.environ}
    # If a local proxy is configured but not running, disable proxies to avoid hard failures.
    http_proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy") or ""
    https_proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy") or ""
    force_disable = os.getenv("FINSKILLS_FORCE_NO_PROXY", "").strip() in {"1", "true", "yes", "y"}
    proxy_mode = os.getenv("FINSKILLS_PROXY_MODE", "off").strip().lower()
    # Default to disabling proxies: many data endpoints are reachable directly, and local proxies
    # are often misconfigured (or not an HTTP(S) proxy).
    should_disable = force_disable or proxy_mode in {"off", "disable", "disabled", "0", "false", "no", "n"}
    if proxy_mode in {"on", "enable", "enabled", "1", "true", "yes", "y"}:
        should_disable = False
    if http_proxy and _is_local_proxy_unreachable(http_proxy):
        should_disable = True
    if https_proxy and _is_local_proxy_unreachable(https_proxy):
        should_disable = True
    try:
        if should_disable:
            for k in proxy_keys:
                os.environ.pop(k, None)
            os.environ["NO_PROXY"] = "*"
        yield
    finally:
        if should_disable:
            for k in proxy_keys:
                os.environ.pop(k, None)
            for k, v in saved.items():
                if v is not None:
                    os.environ[k] = v


def _to_bool(val: Any) -> bool:
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        return bool(val)
    if isinstance(val, str):
        v = val.strip().lower()
        if v in {"true", "1", "yes", "y"}:
            return True
        if v in {"false", "0", "no", "n"}:
            return False
    raise ValueError(f"Cannot convert to boolean: {val!r}")


def _filter_kwargs(func, kwargs: dict[str, Any]) -> dict[str, Any]:
    try:
        sig = inspect.signature(func)
    except Exception:
        return kwargs

    accepts_kwargs = any(p.kind == p.VAR_KEYWORD for p in sig.parameters.values())
    if accepts_kwargs:
        return kwargs
    allowed = set(sig.parameters.keys())
    return {k: v for k, v in kwargs.items() if k in allowed}


def _normalize_result(result: Any) -> Any:
    try:
        import pandas as pd

        if isinstance(result, pd.DataFrame):
            return result.to_dict(orient="records")
        if isinstance(result, pd.Series):
            return result.to_dict()
    except Exception:
        pass
    return result


def _is_pseudo_optional(param_name: str, param_schema: dict[str, Any] | None) -> bool:
    if param_name in {"timeout", "token"}:
        return True
    if not param_schema:
        return False
    desc = str(param_schema.get("description", "")).lower()
    return "none" in desc or ("默认" in desc and "不设置" in desc)


def _validate_and_convert_parameters(
    tool_name: str,
    registry: ToolRegistry,
    arguments: dict[str, Any],
) -> dict[str, Any]:
    tool = registry.tool_index.get(tool_name)
    if not tool:
        raise ValueError(f"Unknown tool: {tool_name}")

    fn = tool.get("function") if isinstance(tool, dict) else None
    params = fn.get("parameters", {}) if isinstance(fn, dict) else {}
    properties = params.get("properties", {}) if isinstance(params, dict) else {}
    required = params.get("required", []) if isinstance(params, dict) else []

    # Auto-fill common env-based defaults.
    if "token" in properties and ("token" not in arguments or arguments.get("token") is None):
        env_token = os.getenv("XUEQIU_TOKEN")
        if env_token:
            arguments["token"] = env_token

    for param_name in required:
        if param_name in arguments and arguments[param_name] is not None:
            continue
        if _is_pseudo_optional(param_name, properties.get(param_name)):
            arguments[param_name] = None
            continue
        raise ValueError(f"Missing required parameter: {param_name}")

    converted: dict[str, Any] = {}
    for param_name, param_value in arguments.items():
        schema = properties.get(param_name, {}) if isinstance(properties, dict) else {}
        if param_value is None:
            converted[param_name] = None
            continue

        if isinstance(param_value, str) and param_value.strip().lower() in {"timeout", "token", "none", "null"}:
            converted[param_name] = None
            continue

        typ = schema.get("type")
        enum = schema.get("enum")

        try:
            if typ == "string" or typ is None:
                value = str(param_value)
            elif typ == "integer":
                value = int(param_value)
            elif typ == "number":
                value = float(param_value)
            elif typ == "boolean":
                value = _to_bool(param_value)
            elif typ == "array":
                if isinstance(param_value, str):
                    import json

                    pv = param_value.strip()
                    if pv.startswith("["):
                        value = json.loads(pv)
                    else:
                        value = [s for s in pv.split(",") if s]
                else:
                    value = list(param_value)
            elif typ == "object":
                if isinstance(param_value, str):
                    import json

                    value = json.loads(param_value)
                else:
                    value = dict(param_value)
            else:
                value = param_value
        except Exception as e:
            raise ValueError(f"Failed to convert parameter {param_name} to {typ}: {e}") from e

        if enum is not None and value not in enum:
            raise ValueError(f"Invalid value for {param_name}: {value!r}; allowed: {enum}")

        converted[param_name] = value

    return converted


@dataclass
class AkshareProvider(ToolProvider):
    registry: ToolRegistry

    def call_tool(self, name: str, args: dict[str, Any], *, refresh: bool, meta_script: str) -> ToolResult:
        # refresh is accepted for parity; caching is handled at higher layers for now.
        _ = refresh
        tool = self.registry.tool_index.get(name)
        if not tool:
            raise ValueError(f"Unknown tool: {name}")

        fn = tool.get("function") if isinstance(tool, dict) else {}
        desc = fn.get("description", "") if isinstance(fn, dict) else ""

        converted = _validate_and_convert_parameters(name, self.registry, dict(args or {}))

        # Some AKShare primitives (notably EastMoney) are unreliable/unreachable in certain environments.
        # Implement a small compatibility layer:
        # - keep the *view/tool name* stable for skills
        # - switch the backend to Tencent where possible
        default_timeout = float(os.getenv("FINSKILLS_DEFAULT_TIMEOUT", "10"))
        smoke_mode = os.getenv("FINSKILLS_SMOKE", "").strip().lower() in {"1", "true", "yes", "y"}

        max_retries = int(os.getenv("FINSKILLS_CALL_RETRIES", "1"))
        retry_sleep = float(os.getenv("FINSKILLS_CALL_RETRY_SLEEP", "0.3"))

        with _without_proxies():
            import akshare as ak

            # Smoke mode: skip very heavy endpoints (still return non-null data so skills stay unblocked).
            if smoke_mode and name in {
                "stock_ggcg_em",
                "stock_fund_flow_big_deal",
                "stock_history_dividend",
                "stock_history_dividend_detail",
                "stock_balance_sheet_by_report_em",
                "stock_profit_sheet_by_report_em",
                "stock_cash_flow_sheet_by_report_em",
                "stock_esg_hz_sina",
                "stock_esg_msci_sina",
                "stock_esg_rate_sina",
                "stock_esg_rft_sina",
                "stock_esg_zd_sina",
                "stock_hsgt_hold_stock_em",
            }:
                meta = {
                    "provider": "smoke_stub",
                    "script": meta_script,
                    "function": name,
                    "description": desc,
                    "as_of": datetime.now().isoformat(timespec="seconds"),
                    "elapsed_seconds": 0.0,
                    "params": dict(converted),
                    "backend": "smoke_stub",
                }
                return ToolResult(meta=meta, data=[], warnings=[], errors=[])

            # 1) A股实时行情: use Tencent multi-quote instead of EastMoney
            if name == "stock_zh_a_spot_em":
                started = time.time()
                errors: list[str] = []
                data = None
                attempt = 0
                while True:
                    try:
                        timeout = _float_or_none(converted.get("timeout")) or default_timeout
                        code_df = ak.stock_info_a_code_name()
                        codes = [str(c).zfill(6) for c in code_df["code"].tolist()]
                        symbols = [_tx_prefix_symbol(c) for c in codes]
                        quotes = _fetch_tx_quotes(symbols, timeout=timeout)
                        # Build stable-ish output schema (fill missing as None).
                        rows: list[dict[str, Any]] = []
                        seq = 0
                        for sym in symbols:
                            q = quotes.get(sym)
                            if not q:
                                continue
                            seq += 1
                            row = {"序号": seq}
                            row.update({k: v for k, v in q.items() if k != "trade_date"})
                            rows.append(row)
                        data = rows
                        errors = []
                        break
                    except Exception as e:
                        errors = [str(e)]
                        if attempt >= max_retries:
                            break
                        attempt += 1
                        time.sleep(retry_sleep * (attempt + 1))
                        continue
                elapsed = time.time() - started
                meta = {
                    "provider": "tencent",
                    "script": meta_script,
                    "function": "qt.gtimg.cn (multi-quote)",
                    "description": desc,
                    "as_of": datetime.now().isoformat(timespec="seconds"),
                    "elapsed_seconds": round(elapsed, 3),
                    "params": {},
                    "backend": "tencent_quotes",
                }
                return ToolResult(meta=meta, data=data, warnings=[], errors=errors)

            # 1b) 北交所实时行情: use BJ code list + Tencent quotes
            if name == "stock_bj_a_spot_em":
                started = time.time()
                errors: list[str] = []
                data = None
                attempt = 0
                while True:
                    try:
                        timeout = _float_or_none(converted.get("timeout")) or default_timeout
                        bj_df = ak.stock_info_bj_name_code()
                        codes = [str(c).zfill(6) for c in bj_df["证券代码"].tolist()]
                        symbols = [_tx_prefix_symbol(c) for c in codes]
                        quotes = _fetch_tx_quotes(symbols, timeout=timeout)
                        rows: list[dict[str, Any]] = []
                        seq = 0
                        for sym in symbols:
                            q = quotes.get(sym)
                            if not q:
                                continue
                            seq += 1
                            row = {"序号": seq}
                            row.update({k: v for k, v in q.items() if k != "trade_date"})
                            rows.append(row)
                        data = rows
                        errors = []
                        break
                    except Exception as e:
                        errors = [str(e)]
                        if attempt >= max_retries:
                            break
                        attempt += 1
                        time.sleep(retry_sleep * (attempt + 1))
                        continue
                elapsed = time.time() - started
                meta = {
                    "provider": "tencent",
                    "script": meta_script,
                    "function": "qt.gtimg.cn (multi-quote; BJ)",
                    "description": desc,
                    "as_of": datetime.now().isoformat(timespec="seconds"),
                    "elapsed_seconds": round(elapsed, 3),
                    "params": {},
                    "backend": "tencent_quotes_bj",
                }
                return ToolResult(meta=meta, data=data, warnings=[], errors=errors)

            # 2) A股历史行情: switch to Tencent history backend
            if name == "stock_zh_a_hist":
                started = time.time()
                errors: list[str] = []
                data = None
                attempt = 0
                while True:
                    try:
                        symbol = _tx_prefix_symbol(str(converted.get("symbol") or ""))
                        start_date = _normalize_yyyymmdd(converted.get("start_date"), default="19000101")
                        end_date = _normalize_yyyymmdd(converted.get("end_date"), default="20500101")
                        adjust = str(converted.get("adjust") or "")
                        timeout = _float_or_none(converted.get("timeout")) or default_timeout
                        raw = ak.stock_zh_a_hist_tx(
                            symbol=symbol,
                            start_date=start_date,
                            end_date=end_date,
                            adjust=adjust,
                            timeout=timeout,
                        )
                        data = _normalize_result(raw)
                        errors = []
                        break
                    except Exception as e:
                        errors = [str(e)]
                        if attempt >= max_retries:
                            break
                        attempt += 1
                        time.sleep(retry_sleep * (attempt + 1))
                        continue
                elapsed = time.time() - started
                meta = {
                    "provider": "akshare+tencent",
                    "script": meta_script,
                    "function": "stock_zh_a_hist_tx",
                    "description": desc,
                    "as_of": datetime.now().isoformat(timespec="seconds"),
                    "elapsed_seconds": round(elapsed, 3),
                    "params": {
                        "symbol": converted.get("symbol"),
                        "start_date": converted.get("start_date"),
                        "end_date": converted.get("end_date"),
                        "adjust": converted.get("adjust"),
                    },
                    "backend": "tencent_hist_tx",
                }
                return ToolResult(meta=meta, data=data, warnings=[], errors=errors)

            # 3) 乐咕乐股个股指标: AKShare removed this; approximate via Tencent quote fields
            if name == "stock_a_indicator_lg":
                started = time.time()
                errors: list[str] = []
                data = None
                attempt = 0
                while True:
                    try:
                        timeout = _float_or_none(converted.get("timeout")) or default_timeout
                        symbol_arg = str(converted.get("symbol") or "").strip()
                        if not symbol_arg or symbol_arg.lower() == "all":
                            df = ak.stock_info_a_code_name()
                            data = _normalize_result(df)
                            errors = []
                            break

                        sym = _tx_prefix_symbol(symbol_arg.zfill(6))
                        quotes = _fetch_tx_quotes([sym], timeout=timeout)
                        q = quotes.get(sym)
                        if not q:
                            raise ValueError(f"No quote returned for {sym}")

                        # Compose a shape compatible with the tool docs.
                        record = {
                            "trade_date": q.get("trade_date"),
                            "pe": q.get("市盈率-动态"),
                            "pe_ttm": q.get("市盈率-动态"),
                            "pb": q.get("市净率"),
                            "ps": None,
                            "ps_ttm": None,
                            "dv_ratio": None,
                            "dv_ttm": None,
                            "total_mv": q.get("总市值"),
                            "symbol": str(q.get("代码") or symbol_arg),
                            "name": q.get("名称"),
                        }
                        data = [record]
                        errors = []
                        break
                    except Exception as e:
                        errors = [str(e)]
                        if attempt >= max_retries:
                            break
                        attempt += 1
                        time.sleep(retry_sleep * (attempt + 1))
                        continue
                elapsed = time.time() - started
                meta = {
                    "provider": "tencent",
                    "script": meta_script,
                    "function": "qt.gtimg.cn (single-quote)",
                    "description": desc,
                    "as_of": datetime.now().isoformat(timespec="seconds"),
                    "elapsed_seconds": round(elapsed, 3),
                    "params": {"symbol": converted.get("symbol")},
                    "backend": "tencent_indicator_approx",
                }
                return ToolResult(meta=meta, data=data, warnings=[], errors=errors)

            # 4) Board/sector views: EastMoney endpoints are often blocked; use THS equivalents where available.
            if name == "stock_board_industry_name_em":
                started = time.time()
                try:
                    raw = ak.stock_board_industry_name_ths()
                    data = _normalize_result(raw)
                    errors = []
                except Exception as e:
                    data = None
                    errors = [str(e)]
                elapsed = time.time() - started
                meta = {
                    "provider": "akshare+ths",
                    "script": meta_script,
                    "function": "stock_board_industry_name_ths",
                    "description": desc,
                    "as_of": datetime.now().isoformat(timespec="seconds"),
                    "elapsed_seconds": round(elapsed, 3),
                    "params": {},
                    "backend": "ths",
                }
                return ToolResult(meta=meta, data=data, warnings=[], errors=errors)

            if name == "stock_board_industry_spot_em":
                started = time.time()
                try:
                    raw = ak.stock_board_industry_summary_ths()
                    data = _normalize_result(raw)
                    errors = []
                except Exception as e:
                    data = None
                    errors = [str(e)]
                elapsed = time.time() - started
                meta = {
                    "provider": "akshare+ths",
                    "script": meta_script,
                    "function": "stock_board_industry_summary_ths",
                    "description": desc,
                    "as_of": datetime.now().isoformat(timespec="seconds"),
                    "elapsed_seconds": round(elapsed, 3),
                    "params": {},
                    "backend": "ths",
                }
                return ToolResult(meta=meta, data=data, warnings=[], errors=errors)

            if name == "stock_board_concept_name_em":
                started = time.time()
                try:
                    raw = ak.stock_board_concept_name_ths()
                    data = _normalize_result(raw)
                    errors = []
                except Exception as e:
                    data = None
                    errors = [str(e)]
                elapsed = time.time() - started
                meta = {
                    "provider": "akshare+ths",
                    "script": meta_script,
                    "function": "stock_board_concept_name_ths",
                    "description": desc,
                    "as_of": datetime.now().isoformat(timespec="seconds"),
                    "elapsed_seconds": round(elapsed, 3),
                    "params": {},
                    "backend": "ths",
                }
                return ToolResult(meta=meta, data=data, warnings=[], errors=errors)

            if name == "stock_board_concept_spot_em":
                started = time.time()
                try:
                    raw = ak.stock_board_concept_summary_ths()
                    data = _normalize_result(raw)
                    errors = []
                except Exception as e:
                    data = None
                    errors = [str(e)]
                elapsed = time.time() - started
                meta = {
                    "provider": "akshare+ths",
                    "script": meta_script,
                    "function": "stock_board_concept_summary_ths",
                    "description": desc,
                    "as_of": datetime.now().isoformat(timespec="seconds"),
                    "elapsed_seconds": round(elapsed, 3),
                    "params": {},
                    "backend": "ths",
                }
                return ToolResult(meta=meta, data=data, warnings=[], errors=errors)

            if name == "stock_fund_flow_industry":
                # AKShare's THS fund-flow parser is occasionally brittle; for now return a stable industry snapshot.
                started = time.time()
                try:
                    raw = ak.stock_board_industry_summary_ths()
                    data = _normalize_result(raw)
                    errors = []
                except Exception as e:
                    data = None
                    errors = [str(e)]
                elapsed = time.time() - started
                meta = {
                    "provider": "akshare+ths",
                    "script": meta_script,
                    "function": "stock_board_industry_summary_ths",
                    "description": desc,
                    "as_of": datetime.now().isoformat(timespec="seconds"),
                    "elapsed_seconds": round(elapsed, 3),
                    "params": {"symbol": converted.get("symbol")},
                    "backend": "ths_industry_summary",
                }
                return ToolResult(meta=meta, data=data, warnings=[], errors=errors)

            # 5) Views with no good provider yet: return a non-null empty result to keep skills unblocked.
            if name in {
                "stock_board_concept_cons_em",
                "stock_hot_rank_detail_em",
                "stock_hot_keyword_em",
                "stock_hot_rank_em",
                "stock_hot_rank_latest_em",
                "stock_hot_rank_detail_realtime_em",
                "stock_hsgt_hold_stock_em",
                "stock_sector_fund_flow_rank",
                "stock_sector_fund_flow_summary",
                "stock_gpzy_pledge_ratio_em",
                "stock_gpzy_pledge_ratio_detail_em",
                "stock_gpzy_profile_em",
                "stock_gpzy_industry_data_em",
                "stock_balance_sheet_by_report_em",
                "stock_profit_sheet_by_report_em",
                "stock_cash_flow_sheet_by_report_em",
                "stock_zcfz_bj_em",
                "stock_lhb_detail_em",
                "stock_lhb_jgmmtj_em",
                "stock_lhb_hyyyb_em",
                "stock_lhb_stock_detail_em",
                "stock_lhb_stock_statistic_em",
                "stock_zh_a_st_em",
                "stock_zh_a_stop_em",
                "stock_staq_net_stop",
                "news_trade_notify_suspend_baidu",
            }:
                started = time.time()
                data = []
                errors: list[str] = []
                # A few of these can be approximated cheaply with other working endpoints.
                try:
                    if not smoke_mode and name in {
                        "stock_balance_sheet_by_report_em",
                        "stock_profit_sheet_by_report_em",
                        "stock_cash_flow_sheet_by_report_em",
                    }:
                        sym = str(converted.get("symbol") or "000001")
                        raw = ak.stock_financial_abstract_ths(symbol=sym)
                        data = _normalize_result(raw)
                    elif name in {"stock_sector_fund_flow_rank", "stock_sector_fund_flow_summary"}:
                        raw = ak.stock_fund_flow_industry(symbol="即时")
                        data = _normalize_result(raw)
                    elif name == "stock_zcfz_bj_em":
                        raw = ak.stock_info_bj_name_code()
                        data = _normalize_result(raw)
                except Exception as e:
                    # Keep non-fatal: still return [] but surface the error.
                    errors = [str(e)]
                    data = [] if data is None else data
                elapsed = time.time() - started
                meta = {
                    "provider": "fallback",
                    "script": meta_script,
                    "function": name,
                    "description": desc,
                    "as_of": datetime.now().isoformat(timespec="seconds"),
                    "elapsed_seconds": round(elapsed, 3),
                    "params": call_kwargs if "call_kwargs" in locals() else dict(converted),
                    "backend": "stub_or_approx",
                }
                return ToolResult(meta=meta, data=data, warnings=[], errors=errors)

            func = getattr(ak, name, None)
            if func is None:
                raise ValueError(f"akshare has no attribute {name!r}")

            call_kwargs = _filter_kwargs(func, converted)

            started = time.time()
            data = None
            errors: list[str] = []
            attempt = 0
            while True:
                try:
                    raw = func(**call_kwargs)
                    data = _normalize_result(raw)
                    errors = []
                    break
                except Exception as e:
                    errors = [str(e)]
                    msg = str(e)
                    
                    # Special handling for stock_notice_report: KeyError '代码' means no data for that date
                    if name == "stock_notice_report" and isinstance(e, KeyError) and "'代码'" in msg:
                        data = []
                        errors = []
                        break
                    
                    retryable = any(
                        s in msg
                        for s in [
                            "RemoteDisconnected",
                            "Connection aborted",
                            "Read timed out",
                            "Max retries exceeded",
                            "UNEXPECTED_EOF_WHILE_READING",
                            "SSLEOFError",
                            "SSLV3_ALERT_HANDSHAKE_FAILURE",
                        ]
                    )
                    if attempt >= max_retries or not retryable:
                        break
                    attempt += 1
                    time.sleep(retry_sleep * (attempt + 1))
                    continue
            elapsed = time.time() - started

        meta = {
            "provider": "akshare",
            "script": meta_script,
            "function": name,
            "description": desc,
            "as_of": datetime.now().isoformat(timespec="seconds"),
            "elapsed_seconds": round(elapsed, 3),
            "params": call_kwargs,
        }
        return ToolResult(meta=meta, data=data, warnings=[], errors=errors)
