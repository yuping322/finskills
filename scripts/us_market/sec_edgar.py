#!/usr/bin/env python3
"""
SEC EDGAR API Wrapper
=====================
Fetch insider trading data (Form 4), company filings, and CIK lookups.
No API key required — just a User-Agent header per SEC policy.

Usage:
    python sec_edgar.py insider AAPL                   # Recent insider trades
    python sec_edgar.py insider AAPL --days 90         # Last 90 days
    python sec_edgar.py filings AAPL --form-type 10-K  # Recent 10-K filings
    python sec_edgar.py cik AAPL                       # Lookup CIK number
"""
import argparse
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.utils import output_json, safe_float, error_exit
from common.config import get_config

BASE_URL = "https://efts.sec.gov/LATEST"
DATA_URL = "https://data.sec.gov"
EDGAR_FULL = "https://www.sec.gov/cgi-bin/browse-edgar"


def _headers() -> dict:
    cfg = get_config()
    ua = cfg.get("sec_edgar", {}).get("user_agent",
                                      "FinSkills research@example.com")
    return {"User-Agent": ua, "Accept": "application/json"}


def _rate_limited_get(url: str, params: dict | None = None) -> requests.Response:
    """GET with rate limiting (10 req/s per SEC policy)."""
    time.sleep(0.12)  # ~8 req/s to stay safely under limit
    resp = requests.get(url, headers=_headers(), params=params, timeout=30)
    resp.raise_for_status()
    return resp


# ---------------------------------------------------------------------------
# CIK Lookup
# ---------------------------------------------------------------------------

def lookup_cik(ticker: str) -> dict:
    """Resolve a ticker to a CIK number using SEC company tickers JSON."""
    url = f"{DATA_URL}/files/company_tickers.json"
    resp = _rate_limited_get(url)
    data = resp.json()

    ticker_upper = ticker.upper()
    for entry in data.values():
        if entry.get("ticker", "").upper() == ticker_upper:
            cik = str(entry["cik_str"]).zfill(10)
            return {
                "ticker": ticker_upper,
                "cik": cik,
                "name": entry.get("title", ""),
            }

    return {"ticker": ticker_upper, "error": "CIK not found"}


# ---------------------------------------------------------------------------
# Insider Trading (Form 4)
# ---------------------------------------------------------------------------

def fetch_insider_trades(ticker: str, days: int = 90) -> dict:
    """
    Fetch recent Form 4 insider trading filings for a company.
    Returns open-market purchases and sales by insiders.
    """
    # Step 1: Get CIK
    cik_info = lookup_cik(ticker)
    if "error" in cik_info:
        return cik_info

    cik = cik_info["cik"]
    company_name = cik_info["name"]

    # Step 2: Get recent filings via EDGAR full-text search
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    url = f"{BASE_URL}/submissions/CIK{cik}.json"

    try:
        resp = _rate_limited_get(url)
        data = resp.json()
    except Exception as e:
        return {"ticker": ticker, "error": f"EDGAR API error: {e}"}

    # Step 3: Extract Form 4 filings
    recent = data.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])
    accessions = recent.get("accessionNumber", [])
    primary_docs = recent.get("primaryDocument", [])

    form4_filings = []
    for i, form_type in enumerate(forms):
        if form_type != "4":
            continue
        filing_date = dates[i] if i < len(dates) else ""
        if filing_date < cutoff:
            continue

        form4_filings.append({
            "filing_date": filing_date,
            "accession_number": accessions[i] if i < len(accessions) else "",
            "document": primary_docs[i] if i < len(primary_docs) else "",
            "form_type": "4",
        })

    # Step 4: Parse transaction details from XBRL/XML
    # (For each Form 4, we'd ideally parse the XML for transaction details.
    #  Here we provide the filing metadata and a summary.)
    trades = []
    for filing in form4_filings[:20]:  # Limit to 20 most recent
        accession = filing["accession_number"].replace("-", "")
        xml_url = (
            f"{DATA_URL}/Archives/edgar/data/{cik.lstrip('0')}/"
            f"{accession}/{filing['document']}"
        )

        try:
            xml_resp = _rate_limited_get(xml_url)
            trade_info = _parse_form4_xml(xml_resp.text, filing["filing_date"])
            if trade_info:
                trades.extend(trade_info)
        except Exception:
            # If XML parsing fails, include filing metadata only
            trades.append({
                "filing_date": filing["filing_date"],
                "accession": filing["accession_number"],
                "parse_error": True,
            })

    # Step 5: Summarize
    buys = [t for t in trades if t.get("transaction_type") == "Purchase"]
    sells = [t for t in trades if t.get("transaction_type") == "Sale"]

    return {
        "ticker": ticker,
        "company": company_name,
        "cik": cik,
        "period": f"Last {days} days",
        "cutoff_date": cutoff,
        "total_form4_filings": len(form4_filings),
        "transactions_parsed": len(trades),
        "summary": {
            "total_purchases": len(buys),
            "total_sales": len(sells),
            "unique_buyers": len(set(t.get("insider_name", "") for t in buys)),
            "total_buy_value": sum(
                t.get("transaction_value", 0) or 0 for t in buys
            ),
            "total_sell_value": sum(
                t.get("transaction_value", 0) or 0 for t in sells
            ),
        },
        "transactions": trades,
    }


def _parse_form4_xml(xml_text: str, filing_date: str) -> list[dict]:
    """Parse Form 4 XML to extract transaction details."""
    import xml.etree.ElementTree as ET

    trades = []
    try:
        # Form 4 can be XML or HTML; try XML first
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []

    # Extract insider name
    ns = ""  # namespace handling
    for prefix in [
        "{http://www.sec.gov/cgi-bin/viewer?action=view&cik=}",
        "",
    ]:
        reporting = root.find(f"{prefix}reportingOwner")
        if reporting is not None:
            ns = prefix
            break

    insider_name = ""
    insider_title = ""
    if reporting is not None:
        rid = reporting.find(f"{ns}reportingOwnerId")
        if rid is not None:
            name_el = rid.find(f"{ns}rptOwnerName")
            insider_name = name_el.text if name_el is not None else ""

        rel = reporting.find(f"{ns}reportingOwnerRelationship")
        if rel is not None:
            for title_tag in [
                "officerTitle", "isDirector", "isOfficer", "isTenPercentOwner"
            ]:
                el = rel.find(f"{ns}{title_tag}")
                if el is not None and el.text:
                    if title_tag == "officerTitle":
                        insider_title = el.text
                    elif el.text in ("1", "true"):
                        insider_title = title_tag.replace("is", "")

    # Extract non-derivative transactions
    for tx_table in [
        root.find(f"{ns}nonDerivativeTable"),
        root.find("nonDerivativeTable"),
    ]:
        if tx_table is None:
            continue
        for tx in tx_table:
            tag = tx.tag.replace(ns, "")
            if "Transaction" not in tag:
                continue

            coding = tx.find(f"{ns}transactionCoding") or tx.find("transactionCoding")
            amounts = tx.find(f"{ns}transactionAmounts") or tx.find("transactionAmounts")
            security = tx.find(f"{ns}securityTitle") or tx.find("securityTitle")

            tx_code = ""
            if coding is not None:
                code_el = coding.find(f"{ns}transactionCode") or coding.find("transactionCode")
                tx_code = code_el.text if code_el is not None else ""

            # P = Purchase, S = Sale, A = Grant/Award, M = Exercise
            if tx_code not in ("P", "S"):
                continue  # Only open-market purchases and sales

            shares = 0
            price = 0
            if amounts is not None:
                shares_el = (
                    amounts.find(f"{ns}transactionShares/{ns}value")
                    or amounts.find("transactionShares/value")
                )
                price_el = (
                    amounts.find(f"{ns}transactionPricePerShare/{ns}value")
                    or amounts.find("transactionPricePerShare/value")
                )
                if shares_el is not None:
                    shares = safe_float(shares_el.text, 0)
                if price_el is not None:
                    price = safe_float(price_el.text, 0)

            sec_title = ""
            if security is not None:
                val_el = security.find(f"{ns}value") or security.find("value")
                sec_title = val_el.text if val_el is not None else ""

            trades.append({
                "filing_date": filing_date,
                "insider_name": insider_name,
                "insider_title": insider_title,
                "transaction_type": "Purchase" if tx_code == "P" else "Sale",
                "transaction_code": tx_code,
                "security": sec_title,
                "shares": shares,
                "price_per_share": price,
                "transaction_value": round(shares * price, 2) if shares and price else None,
            })

    return trades


# ---------------------------------------------------------------------------
# Company Filings
# ---------------------------------------------------------------------------

def fetch_filings(ticker: str, form_type: str = "10-K",
                  count: int = 5) -> dict:
    """Fetch recent filings of a given type for a company."""
    cik_info = lookup_cik(ticker)
    if "error" in cik_info:
        return cik_info

    cik = cik_info["cik"]
    url = f"{BASE_URL}/submissions/CIK{cik}.json"

    try:
        resp = _rate_limited_get(url)
        data = resp.json()
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}

    recent = data.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])
    accessions = recent.get("accessionNumber", [])
    primary_docs = recent.get("primaryDocument", [])
    descriptions = recent.get("primaryDocDescription", [])

    filings = []
    for i, form in enumerate(forms):
        if form != form_type:
            continue
        if len(filings) >= count:
            break
        acc = accessions[i] if i < len(accessions) else ""
        doc = primary_docs[i] if i < len(primary_docs) else ""
        filings.append({
            "form_type": form,
            "filing_date": dates[i] if i < len(dates) else "",
            "accession_number": acc,
            "document": doc,
            "description": descriptions[i] if i < len(descriptions) else "",
            "url": (
                f"https://www.sec.gov/Archives/edgar/data/"
                f"{cik.lstrip('0')}/{acc.replace('-', '')}/{doc}"
            ),
        })

    return {
        "ticker": ticker,
        "company": cik_info["name"],
        "cik": cik,
        "form_type": form_type,
        "filings": filings,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="SEC EDGAR Data Fetcher (no API key required)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # insider
    p_ins = sub.add_parser("insider", help="Fetch insider trades (Form 4)")
    p_ins.add_argument("ticker", help="Stock ticker")
    p_ins.add_argument("--days", type=int, default=90,
                       help="Lookback period in days (default: 90)")

    # filings
    p_fil = sub.add_parser("filings", help="Fetch company filings")
    p_fil.add_argument("ticker", help="Stock ticker")
    p_fil.add_argument("--form-type", default="10-K",
                       help="Filing type (default: 10-K)")
    p_fil.add_argument("--count", type=int, default=5,
                       help="Number of filings (default: 5)")

    # cik
    p_cik = sub.add_parser("cik", help="Lookup CIK number for a ticker")
    p_cik.add_argument("ticker", help="Stock ticker")

    args = parser.parse_args()

    try:
        if args.command == "insider":
            data = fetch_insider_trades(args.ticker, args.days)
        elif args.command == "filings":
            data = fetch_filings(args.ticker, args.form_type, args.count)
        elif args.command == "cik":
            data = lookup_cik(args.ticker)
        else:
            error_exit(f"Unknown command: {args.command}")
            return

        output_json(data)

    except Exception as e:
        error_exit(f"Error: {e}")


if __name__ == "__main__":
    main()
