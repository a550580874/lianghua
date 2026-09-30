"""Deterministic checks for canonical local tables (no network access)."""
from __future__ import annotations
from pathlib import Path
import pandas as pd

def duplicate_keys(frame, keys=("instrument", "trade_date")):
    return int(frame.duplicated(list(keys)).sum())

def ohlc_violations(frame):
    return int(((frame.high < frame.low) | (frame.high < frame.open) | (frame.high < frame.close) | (frame.low > frame.open) | (frame.low > frame.close) | (frame.volume < 0) | (frame.amount < 0)).sum())

def validate_directory(path: Path) -> dict:
    result = {}
    price_path = path / "daily_price_raw.parquet"
    if not price_path.exists(): return {"status": "BLOCKED_INPUT", "reason": "daily_price_raw.parquet not found"}
    price = pd.read_parquet(price_path)
    result["daily_price_raw_duplicate_keys"] = duplicate_keys(price)
    result["daily_price_raw_ohlc_violations"] = ohlc_violations(price)
    if (path / "adj_factor.parquet").exists():
        adj = pd.read_parquet(path / "adj_factor.parquet")
        result["adj_factor_nonpositive"] = int((adj["adj_factor"] <= 0).sum()) if "adj_factor" in adj else None
    result["status"] = "PASS" if all(v in (0, None) for k, v in result.items() if k != "status") else "DATA_QUALITY_ISSUES"
    return result

def main():
    import json
    out = Path(__file__).parent / "output"; out.mkdir(exist_ok=True)
    result = validate_directory(out / "parquet")
    (out / "data_quality_report.md").write_text("# Data quality report\n\n```json\n" + json.dumps(result, indent=2) + "\n```\n", encoding="utf-8")
    print(result["status"])

if __name__ == "__main__": main()
