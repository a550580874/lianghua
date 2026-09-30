from pathlib import Path
import json
import pandas as pd

OUT = Path(__file__).parent / "output"; DATA = OUT / "parquet_baostock"

def main():
    result = {"source": "BaoStock", "window": "2024-01-01..2024-03-31", "universe": "fixed sample sh.600000,sz.000001", "issues": []}
    price = pd.read_parquet(DATA / "daily_price_raw.parquet")
    result["rows"] = int(len(price)); result["columns"] = list(price.columns)
    result["duplicate_key_count"] = int(price.duplicated(["code", "date"]).sum())
    numeric = price.apply(pd.to_numeric, errors="coerce")
    result["ohlc_violations"] = int(((numeric.high < numeric.low) | (numeric.high < numeric.open) | (numeric.high < numeric.close) | (numeric.low > numeric.open) | (numeric.low > numeric.close)).sum())
    result["negative_volume_or_amount"] = int(((numeric.volume < 0) | (numeric.amount < 0)).sum())
    result["tradestatus_values"] = sorted(price["tradestatus"].dropna().astype(str).unique().tolist())
    result["isST_values"] = sorted(price["isST"].dropna().astype(str).unique().tolist())
    adj = pd.read_parquet(DATA / "adjustment.parquet")
    result["adjustment_rows"] = int(len(adj)); result["adjustment_status"] = "EMPTY_SOURCE" if len(adj) == 0 else "AVAILABLE"
    result["price_limit_status"] = "PRICE_LIMIT_SOURCE_MISSING"
    result["market_value_status"] = "MARKET_VALUE_SOURCE_MISSING"
    result["pit_status"] = "UNIVERSE_PIT_NOT_VALIDATED"
    result["status"] = "PASS_CORE_DATA" if result["rows"] and result["duplicate_key_count"] == 0 and result["ohlc_violations"] == 0 else "PARTIAL_PASS"
    (OUT / "data_quality_report.md").write_text("# BaoStock data quality\n\n```json\n" + json.dumps(result, ensure_ascii=False, indent=2) + "\n```\n", encoding="utf-8")
    print(result["status"])

if __name__ == "__main__": main()
