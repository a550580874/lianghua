"""Download a small Tushare window after capability/credential checks."""
from __future__ import annotations
import os
from pathlib import Path

START, END = "20240101", "20240331"
OUT = Path(__file__).parent / "output" / "parquet"

def main() -> None:
    if not os.getenv("TUSHARE_TOKEN"):
        raise SystemExit("BLOCKED_CREDENTIAL: set TUSHARE_TOKEN in the environment")
    try:
        import tushare as ts
    except ImportError as exc:
        raise SystemExit("BLOCKED_DEPENDENCY: install official tushare package") from exc
    api = ts.pro_api(os.environ["TUSHARE_TOKEN"])
    OUT.mkdir(parents=True, exist_ok=True)
    # Keep raw source tables separate; no adjusted OHLC is generated here.
    calendar = api.trade_cal(exchange="SSE", start_date=START, end_date=END)
    calendar.to_parquet(OUT / "calendar.parquet", index=False)
    stocks = api.stock_basic(exchange="", list_status="L", fields="ts_code,symbol,name,area,industry,market,list_date,delist_date")
    stocks.to_parquet(OUT / "security_master.parquet", index=False)
    for code, method in (("daily_price_raw", "daily"), ("adj_factor", "adj_factor"), ("daily_basic", "daily_basic"), ("suspension", "suspend_d"), ("price_limit", "stk_limit")):
        frame = getattr(api, method)(start_date=START, end_date=END)
        frame.to_parquet(OUT / f"{code}.parquet", index=False)
    members = api.index_weight(index_code="000300.SZ", start_date=START, end_date=END)
    members.to_parquet(OUT / "index_membership.parquet", index=False)

if __name__ == "__main__": main()
