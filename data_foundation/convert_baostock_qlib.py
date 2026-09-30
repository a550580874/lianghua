"""Build provenance-preserving BaoStock research CSVs; does not implement Qlib bin format."""
from pathlib import Path
import baostock as bs
import pandas as pd

ROOT = Path(__file__).parent; OUT = ROOT / "output"; DATA = OUT / "parquet_baostock"; QOUT = OUT / "qlib_baostock_poc"
SAMPLE = ["sh.600000", "sz.000001"]; START, END = "2024-01-01", "2024-03-31"

def fetch(r):
    if str(r.error_code) != "0": raise RuntimeError(r.error_msg)
    return r.get_data()

def qcode(code): return code.replace(".", "").upper()

def main():
    QOUT.mkdir(parents=True, exist_ok=True)
    login = bs.login()
    if str(login.error_code) != "0": raise SystemExit("BLOCKED_SOURCE")
    try:
        frames = {}; report = ["# BaoStock adjustment report", "", "Raw OHLC uses `adjustflag=3`; adjusted research prices are kept separate.", ""]
        for flag in ("1", "2", "3"):
            rows=[]
            for code in SAMPLE:
                try: rows.append(fetch(bs.query_history_k_data_plus(code, "date,code,open,high,low,close,volume,amount,adjustflag,tradestatus,isST", start_date=START, end_date=END, frequency="d", adjustflag=flag)))
                except Exception: pass
            frame = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
            frames[flag] = frame
            report.append(f"- adjustflag={flag}: rows={len(frame)}; columns={list(frame.columns)}")
        raw = frames["3"].rename(columns={"code":"instrument", "date":"trade_date", "volume":"volume"})
        adj = frames["2"].rename(columns={"code":"instrument", "date":"trade_date"})
        if raw.empty or adj.empty:
            (OUT / "baostock_adjustment_report.md").write_text("\n".join(report+["", "Status: `BLOCKED_INPUT` (adjusted endpoint returned no rows).\n"]), encoding="utf-8"); return
        key=["instrument","trade_date"]; merged=raw.merge(adj[key+['open','high','low','close']], on=key, suffixes=("_raw","_adjusted"))
        for field in ("open","high","low","close"): merged[f"{field}_ratio"] = pd.to_numeric(merged[f"{field}_adjusted"])/pd.to_numeric(merged[f"{field}_raw"])
        ratios=[f"{x}_ratio" for x in ("open","high","low","close")]; merged["derived_factor"]=merged["close_ratio"]; merged["max_ratio_spread"]=merged[ratios].max(axis=1)-merged[ratios].min(axis=1); merged["status"]="PASS"; merged.loc[(merged["derived_factor"]<=0)|(merged["max_ratio_spread"]>1e-6),"status"]="REVIEW"
        merged[["instrument","trade_date","close_raw","close_adjusted","derived_factor","open_ratio","high_ratio","low_ratio","close_ratio","max_ratio_spread","status"]].to_csv(OUT/"adjustment_factor_validation.csv",index=False)
        research=raw.copy(); research["symbol"]=research["instrument"].map(qcode); research["factor"]=merged["derived_factor"].to_numpy(); research["date"]=pd.to_datetime(research["trade_date"]); research[["symbol","date","open","high","low","close","volume","factor"]].to_csv(QOUT/"daily_price_qlib.csv",index=False)
        (OUT / "baostock_adjustment_report.md").write_text("\n".join(report+["", "adjustflag=1/2/3 were queried; flag 2 is used as BaoStock adjusted research convention for this PoC.", "No claim is made that this adjustment matches Qlib sample or Tushare.", "Status: `INTERMEDIATE_READY`; official dump_bin.py still required for binary conversion.\n"]), encoding="utf-8")
    finally: bs.logout()

if __name__ == "__main__": main()
