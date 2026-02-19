"""
Compatibility shim.

Prefer:
  cd view-service
  python -m view_service.backtests.block_deal --help
"""

from view_service.backtests.block_deal import main


if __name__ == "__main__":
    raise SystemExit(main())

