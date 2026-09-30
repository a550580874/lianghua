# Qlib BaoStock compatibility

Status: `BLOCKED_CONVERSION`. BaoStock raw parquet and an intermediate `daily_price_qlib.csv` are available for a two-security sample, but the official `scripts/dump_bin.py` and an installed Qlib package are absent from this checkout. No Qlib bin format was reimplemented or patched; `D.features()` and Alpha158 five-factor generation remain unvalidated.
