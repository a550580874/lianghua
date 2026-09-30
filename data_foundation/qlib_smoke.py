from pathlib import Path
import qlib
from qlib.config import REG_CN
from qlib.data import D

def main():
    provider = Path(__file__).parent / "output" / "qlib_baostock_poc" / "bin"
    qlib.init(provider_uri=str(provider), region=REG_CN)
    frame = D.features(["sh600000", "sz000001"], ["$open", "$high", "$low", "$close", "$volume", "$factor"], start_time="2024-01-01", end_time="2024-03-31")
    report = Path(__file__).parent / "output" / "qlib_features_smoke_report.md"
    report.write_text(f"# Qlib features smoke report\n\nStatus: `PASS`\n\nshape={frame.shape}\nnon_null={frame.notna().sum().to_dict()}\n", encoding="utf-8")
    print(frame.shape)

if __name__ == "__main__": main()
