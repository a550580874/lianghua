# Data Foundation v1

This is an isolated current-data PoC, not a replacement for the Qlib sample data and not a backtester. Tushare Pro remains a permission-gated candidate; its denied capability report is preserved. BaoStock is evaluated as a free source without silently declaring it a production source.

```bash
python data_foundation/probe_tushare.py
```

Set `TUSHARE_TOKEN` in the process environment; never put the value in code, logs, reports, or Git. Without it the expected result is `BLOCKED_CREDENTIAL` and no API request is attempted. With credentials, the probe checks the requested interfaces and records permission failures without silently substituting another provider.

BaoStock probe/download (no token required):

```bash
data_foundation/.venv/bin/python data_foundation/probe_baostock.py
data_foundation/.venv/bin/python data_foundation/download_baostock_poc.py
data_foundation/.venv/bin/python data_foundation/validate_baostock.py
```

The downloaded sample uses raw `adjustflag=3` prices and stores adjustment metadata separately. The fixed two-security sample is not a PIT CSI300 universe; historical `query_hs300_stocks(date=...)` snapshots are retained as raw observations and no effective intervals are inferred. BaoStock does not provide a validated price-limit or market-value field in this PoC.

Raw OHLCV and `adj_factor` remain separate. Canonical schema is documented in `schema.md`; validation and Qlib conversion scripts are intentionally conservative and only operate on downloaded local files.
