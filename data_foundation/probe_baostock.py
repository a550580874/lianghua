"""Credential-free BaoStock capability and schema probe."""
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd

OUT = Path(__file__).parent / "output"
DATE = "2024-03-31"

def call(name, fn):
    try:
        result = fn()
        error_code = getattr(result, "error_code", "0")
        error_msg = getattr(result, "error_msg", "")
        if str(error_code) != "0": return {"status": "ERROR", "error_code": str(error_code), "message": str(error_msg)[:300]}
        rows = result.get_data() if hasattr(result, "get_data") else pd.DataFrame()
        payload = {"status": "AVAILABLE" if len(rows) else "EMPTY", "sample_row_count": int(len(rows)), "columns": [str(c) for c in rows.columns]}
        # Keep only non-sensitive, reproducible date coverage metadata.
        for column in rows.columns:
            if str(column).lower() in {"date", "calendar_date", "updatedate", "ipodate", "outdate"}:
                parsed = pd.to_datetime(rows[column], errors="coerce").dropna()
                if len(parsed):
                    payload["earliest_date"] = parsed.min().date().isoformat()
                    payload["latest_date"] = parsed.max().date().isoformat()
                    break
        return payload
    except NotImplementedError:
        return {"status": "UNSUPPORTED"}
    except Exception as exc:
        return {"status": "ERROR", "error_type": type(exc).__name__, "message": str(exc)[:300]}

def run_probe():
    try:
        import baostock as bs
    except Exception as exc:
        return {"status": "ERROR", "package": "baostock", "message": f"package unavailable: {type(exc).__name__}"}
    login = bs.login()
    result = {"package": "baostock", "credential_status": "not_required", "login_error_code": str(login.error_code), "interfaces": {}}
    if str(login.error_code) != "0":
        result["status"] = "ERROR"; result["message"] = str(login.error_msg)[:300]; return result
    code = "sh.600000"
    result["interfaces"]["login"] = {"status": "AVAILABLE"}
    result["interfaces"]["query_trade_dates"] = call("query_trade_dates", lambda: bs.query_trade_dates(start_date="2024-01-01", end_date=DATE))
    result["interfaces"]["query_stock_basic"] = call("query_stock_basic", lambda: bs.query_stock_basic(code=code))
    result["interfaces"]["query_all_stock"] = call("query_all_stock", lambda: bs.query_all_stock(day=DATE))
    result["interfaces"]["query_history_k_data_plus"] = call("query_history_k_data_plus", lambda: bs.query_history_k_data_plus(code, "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST", start_date="2024-01-01", end_date=DATE, frequency="d", adjustflag="3"))
    result["interfaces"]["query_adjust_factor"] = call("query_adjust_factor", lambda: bs.query_adjust_factor(code, start_date="2024-01-01", end_date=DATE))
    result["interfaces"]["query_hs300_stocks"] = call("query_hs300_stocks", lambda: bs.query_hs300_stocks(date=DATE))
    snapshots = {}
    for snapshot_date in ("2020-03-31", "2022-03-31", "2024-03-31", DATE):
        item = call("query_hs300_stocks", lambda d=snapshot_date: bs.query_hs300_stocks(date=d))
        snapshots[snapshot_date] = {"status": item.get("status"), "rows": item.get("sample_row_count", 0)}
    result["historical_hs300_snapshots"] = snapshots
    result["historical_membership_status"] = "HISTORICAL_SNAPSHOT_AVAILABLE" if all(x["status"] == "AVAILABLE" for x in snapshots.values()) else "UNIVERSE_PIT_NOT_SUPPORTED"
    result["interfaces"]["query_stock_industry"] = call("query_stock_industry", lambda: bs.query_stock_industry(code=code, date=DATE))
    # BaoStock has no direct, stable price-limit/market-value endpoint in this PoC.
    result["interfaces"]["corporate_action"] = {"status": "UNSUPPORTED", "reason": "not exposed by the installed public API"}
    bs.logout()
    statuses = [v.get("status") for k, v in result["interfaces"].items() if k != "login"]
    result["status"] = "PASS" if all(x in {"AVAILABLE", "EMPTY"} for x in statuses) else "PARTIAL"
    return result

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    result = run_probe()
    (OUT / "baostock_capability_report.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# BaoStock Capability Probe", "", f"Status: `{result.get('status')}`", "", "| Interface | Status | Rows | Date coverage | Columns |", "|---|---|---:|---|---|"]
    for name, item in result.get("interfaces", {}).items():
        coverage = ""
        if item.get("earliest_date"):
            coverage = f"{item['earliest_date']}..{item['latest_date']}"
        lines.append(f"| {name} | {item.get('status')} | {item.get('sample_row_count', '')} | {coverage} | {', '.join(item.get('columns', []))} |")
    lines += ["", "Raw prices use adjustflag=3 when the endpoint is available. Price limits and market value are not inferred."]
    (OUT / "baostock_capability_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(result.get("status"))

if __name__ == "__main__": main()
