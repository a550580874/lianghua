"""Conservative Qlib compatibility probe for an already downloaded local table."""
from pathlib import Path
import pandas as pd

REQUIRED = {"instrument", "trade_date", "open", "high", "low", "close", "volume"}

def main():
    source = Path(__file__).parent / "output" / "parquet" / "daily_price_raw.parquet"
    report = Path(__file__).parent / "output" / "qlib_compatibility_report.md"
    if not source.exists():
        report.write_text("# Qlib compatibility\n\nStatus: `BLOCKED_INPUT` (downloaded canonical price table is absent).\n", encoding="utf-8"); return
    frame = pd.read_parquet(source)
    missing = sorted(REQUIRED - set(frame.columns))
    status = "PASS_SCHEMA_ONLY" if not missing else "FAIL_SCHEMA"
    report.write_text(f"# Qlib compatibility\n\nStatus: `{status}`\n\nMissing fields: {missing}\n\nNo Qlib binary or Alpha158 run is attempted until canonical data is available and explicitly converted.\n", encoding="utf-8")

if __name__ == "__main__": main()
