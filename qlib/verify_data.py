"""Minimal Qlib initialization/data-read smoke check from the official API docs."""

from pathlib import Path

import qlib
from qlib.constant import REG_CN
from qlib.data import D


def main() -> None:
    provider_uri = Path(__file__).resolve().parent / "data" / "cn_data"
    qlib.init(provider_uri=str(provider_uri), region=REG_CN)

    calendar = D.calendar(freq="day")
    sample_day = str(calendar[-1].date())
    instruments = D.list_instruments(
        D.instruments("csi300"), start_time=sample_day, end_time=sample_day, as_list=True
    )
    sample = D.features(instruments[:3], ["$close", "$volume"], sample_day, sample_day)

    print(f"qlib_version={qlib.__version__}")
    print(f"provider_uri={provider_uri}")
    print(f"calendar_first={calendar[0].date()}")
    print(f"calendar_last={calendar[-1].date()}")
    print(f"sample_day={sample_day}")
    print(f"csi300_instrument_count={len(instruments)}")
    print(sample.to_string())


if __name__ == "__main__":
    main()
