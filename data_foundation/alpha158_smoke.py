from pathlib import Path
import qlib
from qlib.config import REG_CN
from qlib.contrib.data.handler import Alpha158

def main():
    provider = Path(__file__).parent / "output" / "qlib_baostock_poc" / "bin"
    qlib.init(provider_uri=str(provider), region=REG_CN)
    report = Path(__file__).parent / "output" / "alpha158_compatibility_report.md"
    try:
        handler = Alpha158(instruments=["sh600000", "sz000001"], start_time="2024-01-01", end_time="2024-03-31", fit_start_time="2024-01-01", fit_end_time="2024-03-31")
        frame = handler.fetch(col_set="feature")
        requested = ["ROC20", "STD20", "MA20", "VSTD20", "CORR20"]
        present = [c for c in requested if c in frame.columns]
        report.write_text(f"# Alpha158 compatibility\n\nStatus: `PASS`\n\nshape={frame.shape}\nrequested_present={present}\nnon_null={frame[present].notna().sum().to_dict()}\n", encoding="utf-8")
        print(frame.shape, present)
    except Exception as exc:
        report.write_text(f"# Alpha158 compatibility\n\nStatus: `ERROR`\n\n{type(exc).__name__}: {str(exc)[:500]}\n", encoding="utf-8")
        raise

if __name__ == "__main__": main()
