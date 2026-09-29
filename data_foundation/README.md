# Data Foundation v1

This is an isolated current-data PoC, not a replacement for the Qlib sample data and not a backtester. Tushare Pro is the only source in scope. The first command is a credential-safe capability probe:

```bash
python data_foundation/probe_tushare.py
```

Set `TUSHARE_TOKEN` in the process environment; never put the value in code, logs, reports, or Git. Without it the expected result is `BLOCKED_CREDENTIAL` and no API request is attempted. With credentials, the probe checks the requested interfaces and records permission failures without silently substituting another provider.

Raw OHLCV and `adj_factor` remain separate. Canonical schema is documented in `schema.md`; validation and Qlib conversion scripts are intentionally conservative and only operate on downloaded local files.
