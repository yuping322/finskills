#!/bin/bash
# FinSkills Script Setup
# ======================
# Install Python dependencies for FinSkills scripts.
# All primary data sources are FREE and require NO API keys.
#
# Usage:
#   cd finskills/scripts
#   bash setup.sh
#
# Optional: Create a virtual environment first:
#   python3 -m venv .venv
#   source .venv/bin/activate
#   bash setup.sh

set -e

echo "=== FinSkills Script Setup ==="
echo ""

# Check Python version
PYTHON=${PYTHON:-python3}
PY_VERSION=$($PYTHON --version 2>&1)
echo "Using: $PY_VERSION"

# Install dependencies
echo ""
echo "Installing dependencies..."
$PYTHON -m pip install -r requirements.txt --quiet

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Quick test commands:"
echo ""
echo "  # US Market: Fetch stock metrics (no API key needed)"
echo "  $PYTHON us_market/stock_data.py AAPL --metrics"
echo ""
echo "  # US Market: Check insider trading via SEC EDGAR (no API key needed)"
echo "  $PYTHON us_market/sec_edgar.py insider AAPL --days 90"
echo ""
echo "  # US Market: Financial analysis (DuPont, Z-Score, etc.)"
echo "  $PYTHON us_market/financial_calc.py AAPL --all"
echo ""
echo "  # US Market: Portfolio health check"
echo "  $PYTHON us_market/portfolio_analytics.py --holdings 'AAPL:30,MSFT:25,GOOGL:20,AMZN:15,META:10'"
echo ""
echo "  # US Market: Multi-factor screening"
echo "  $PYTHON us_market/factor_screener.py --sp500-sample --top 5"
echo ""
echo "  # US Market: Macro dashboard"
echo "  $PYTHON us_market/macro_data.py --dashboard"
echo ""
echo "  # China Market: Fetch A-share data (no API key needed)"
echo "  $PYTHON china_market/stock_data.py 600519 --metrics"
echo ""
echo "  # China Market: Macro dashboard"
echo "  $PYTHON china_market/macro_data.py --dashboard"
echo ""
echo "All primary data sources are FREE and require NO API keys."
echo "See config/data_sources.yaml for optional API key configuration."
