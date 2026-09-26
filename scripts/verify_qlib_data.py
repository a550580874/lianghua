"""Minimal verification of the official Qlib China sample data."""

from pathlib import Path

import qlib
from qlib.config import REG_CN
from qlib.data import D


ROOT = Path(__file__).resolve().parents[1]
PROVIDER_URI = ROOT / "data" / "cn_data"

qlib.init(provider_uri=str(PROVIDER_URI), region=REG_CN)

calendar = D.calendar(start_time="2020-07-01", end_time="2020-07-10", freq="day")
features = D.features(
    ["SH000300"],
    ["$close", "$volume"],
    start_time="2020-07-01",
    end_time="2020-07-10",
    freq="day",
)

print(f"provider_uri={PROVIDER_URI}")
print(f"calendar_count={len(calendar)}")
print(f"calendar_first={calendar[0]}")
print(f"calendar_last={calendar[-1]}")
print(f"feature_rows={len(features)}")
print(features.to_string())
