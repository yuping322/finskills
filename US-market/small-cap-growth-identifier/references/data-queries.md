# Data Queries (Shared Scripts)

Run commands from this skill directory. Shared scripts live in `../findata-toolkit/`. (Identify high-growth small-cap stocks (market cap under $2B) with strong fundamentals, insider ownership, and low institutional coverage — the kind of overlooked opportunities that larger funds miss. Use when the user asks to find small-cap growth stocks, discover under-the-radar companies, screen for founder-led small caps, identify emerging growth companies, find low-institutional-ownership stocks, or seek multi-bagger candidates with strong fundamentals.)


## Setup (One-Time)

```bash
# Activate repo-root venv (single .venv)
source ../../.venv/bin/activate

# Install US toolkit deps
python -m pip install -r ../findata-toolkit/requirements.txt
```

## Data Dependencies (What this skill uses)

| Script | Primary use |
| --- | --- |
| stock_data.py | Fundamentals / metrics / history via yfinance. |
| financial_calc.py | Quality metrics (Z/M/F scores, DuPont-style helpers). |

## Common Recipes

```bash
# Ensure venv is active
source ../../.venv/bin/activate

# Quotes / fundamentals / history
python ../findata-toolkit/scripts/stock_data.py AAPL
python ../findata-toolkit/scripts/stock_data.py AAPL --metrics
python ../findata-toolkit/scripts/stock_data.py AAPL --history --period 1y

# SEC EDGAR (insider trades / filings)
python ../findata-toolkit/scripts/sec_edgar.py insider AAPL --days 90
python ../findata-toolkit/scripts/sec_edgar.py filings AAPL --form-type 10-K

# Macro (FRED)
python ../findata-toolkit/scripts/macro_data.py --dashboard

# Financial calculators
python ../findata-toolkit/scripts/financial_calc.py AAPL --all
```

## Discover More

```bash
python ../findata-toolkit/scripts/stock_data.py --help
python ../findata-toolkit/scripts/sec_edgar.py --help
python ../findata-toolkit/scripts/macro_data.py --help
python ../findata-toolkit/scripts/financial_calc.py --help
python ../findata-toolkit/scripts/portfolio_analytics.py --help
python ../findata-toolkit/scripts/factor_screener.py --help
```
