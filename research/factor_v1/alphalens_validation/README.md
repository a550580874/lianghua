# Alphalens Reloaded cross-validation

This directory contains an independent oracle adapter for Factor Research v1. It does not replace the Qlib pipeline and does not add factors or strategies.

The adapter maps a factor known at signal date `t` to the next observed trading date `entry_date=t+1`. Alphalens' H-day return then uses `close(entry_date+H) / close(entry_date) - 1`, matching the v2 diagnostic definition without calendar-day arithmetic. Signals whose exit is outside their split are excluded.

Create the isolated environment and install the unmodified release:

```bash
uv venv research/factor_v1/alphalens_validation/.venv --python 3.12 --seed
research/factor_v1/alphalens_validation/.venv/bin/python -m pip install alphalens-reloaded==0.4.6 pyyaml
```

Run from the repository root:

```bash
research/factor_v1/alphalens_validation/.venv/bin/python research/factor_v1/alphalens_validation/validate.py
research/factor_v1/alphalens_validation/.venv/bin/python research/factor_v1/alphalens_validation/report.py
research/factor_v1/alphalens_validation/.venv/bin/python -m unittest discover -s research/factor_v1/alphalens_validation/tests -q
```

`MATCH` means the effective sample and statistic agree within strict floating-point tolerance. `DATA_ALIGNMENT_DIFFERENCE` records different effective observations or timestamp/price handling. `SEMANTIC_DIFFERENCE` records a documented definition/calendar difference. `NO_DIRECT_ORACLE` is used for metrics Alphalens does not directly implement.
