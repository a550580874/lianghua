"""Extract selected columns from Qlib's official Alpha158 handler.

This script does not implement or alter factor formulas. It asks Qlib 0.9.7
for the official Alpha158 feature/label output and selects five named columns.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
import qlib
import yaml
from qlib.constant import REG_CN
from qlib.contrib.data.handler import Alpha158
from qlib.data.dataset.handler import DataHandlerLP


ROOT = Path(__file__).resolve().parents[2]


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path(__file__).with_name("config.yaml"))
    parser.add_argument("--provider-uri", type=Path, help="Override the configured Qlib data path")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).with_name("output"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    provider_uri = args.provider_uri or Path(config["provider_uri"])
    if not provider_uri.is_absolute():
        provider_uri = ROOT / provider_uri
    if not provider_uri.exists():
        raise FileNotFoundError(
            f"Qlib provider not found: {provider_uri}. Rebuild China sample data first."
        )

    factors = list(config["factors"])
    splits = config["splits"]
    start = min(item["start"] for item in splits.values())
    end = max(item["end"] for item in splits.values())
    expected_label = config["label"]["expression"].replace(" ", "")

    qlib.init(provider_uri=str(provider_uri), region=REG_CN)
    handler = Alpha158(
        instruments=config["universe"],
        start_time=start,
        end_time=end,
        fit_start_time=splits["train"]["start"],
        fit_end_time=splits["train"]["end"],
    )
    official_label, label_names = handler.get_label_config()
    if official_label[0].replace(" ", "") != expected_label:
        raise ValueError(f"Configured label differs from Qlib Alpha158: {official_label[0]}")

    frame = handler.fetch(col_set=["feature", "label"], data_key=DataHandlerLP.DK_R)
    feature_frame = frame["feature"]
    missing = [factor for factor in factors if factor not in feature_frame.columns]
    if missing:
        raise KeyError(f"Alpha158 output is missing requested factors: {missing}")

    selected = feature_frame.loc[:, factors].copy()
    selected[config["label"]["name"]] = frame["label"][label_names[0]]
    selected = selected.reset_index()
    selected["datetime"] = pd.to_datetime(selected["datetime"]).dt.strftime("%Y-%m-%d")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_path = args.output_dir / "factors.csv.gz"
    selected.to_csv(output_path, index=False, compression="gzip")

    metadata = {
        "qlib_version": qlib.__version__,
        "universe": config["universe"],
        "frequency": config["frequency"],
        "factors": factors,
        "label_expression": official_label[0],
        "rows": int(len(selected)),
        "first_datetime": selected["datetime"].min(),
        "last_datetime": selected["datetime"].max(),
        "provider_uri": config["provider_uri"],
        "provider_uri_override_used": bool(args.provider_uri),
        "source": "Qlib Alpha158 raw handler output; no factor formula was reimplemented",
    }
    with (args.output_dir / "extract_metadata.json").open("w", encoding="utf-8") as handle:
        json.dump(metadata, handle, ensure_ascii=False, indent=2)
    print(f"wrote={output_path}")
    print(f"rows={len(selected)}")
    print(f"qlib_version={qlib.__version__}")
    print(f"label={official_label[0]}")


if __name__ == "__main__":
    main()
