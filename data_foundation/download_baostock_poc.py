"""Download a small, provenance-labelled BaoStock canonical PoC."""
from pathlib import Path
import baostock as bs
import pandas as pd

OUT = Path(__file__).parent / "output" / "parquet_baostock"
START, END = "2024-01-01", "2024-03-31"
SAMPLE = ["sh.600000", "sz.000001"]

def fetch(result):
    if str(result.error_code) != "0": raise RuntimeError(result.error_msg)
    return result.get_data()

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    login = bs.login()
    if str(login.error_code) != "0": raise SystemExit("BLOCKED_SOURCE")
    try:
        cal = fetch(bs.query_trade_dates(start_date=START, end_date=END)).rename(columns={"calendar_date":"trade_date", "is_trading_day":"is_open"})
        cal.to_parquet(OUT / "calendar.parquet", index=False)
        masters = [fetch(bs.query_stock_basic(code=c)) for c in SAMPLE]
        master = pd.concat(masters, ignore_index=True).rename(columns={"code":"instrument", "ipoDate":"list_date", "outDate":"delist_date", "code_name":"name"})
        master.to_parquet(OUT / "security_master.parquet", index=False)
        prices, adjustments, industries = [], [], []
        for code in SAMPLE:
            prices.append(fetch(bs.query_history_k_data_plus(code, "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST", start_date=START, end_date=END, frequency="d", adjustflag="3")))
            adjustments.append(fetch(bs.query_adjust_factor(code, start_date=START, end_date=END)))
            industries.append(fetch(bs.query_stock_industry(code=code, date=END)))
        pd.concat(prices, ignore_index=True).to_parquet(OUT / "daily_price_raw.parquet", index=False)
        pd.concat(adjustments, ignore_index=True).to_parquet(OUT / "adjustment.parquet", index=False)
        pd.concat(industries, ignore_index=True).to_parquet(OUT / "industry.parquet", index=False)
        hs300 = fetch(bs.query_hs300_stocks(date=END)); hs300.to_parquet(OUT / "index_membership_raw.parquet", index=False)
        (OUT / "provenance.txt").write_text("source=baostock\nuniverse=fixed sample sh.600000,sz.000001; hs300 snapshot saved separately\nraw_adjustflag=3\nwindow=2024-01-01..2024-03-31\n", encoding="utf-8")
    finally: bs.logout()

if __name__ == "__main__": main()
