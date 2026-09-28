"""Run Alphalens Reloaded cross-validation against Factor Research v1."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import numpy as np
import pandas as pd
import yaml
from alphalens import performance, utils

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research" / "factor_v1"))
from diagnostics import daily_ic_series, horizon_returns  # noqa: E402
from adapter import aligned_inputs  # noqa: E402


def args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "research/factor_v1/output/factors.csv.gz")
    parser.add_argument("--config", type=Path, default=ROOT / "research/factor_v1/config.yaml")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "research/factor_v1/output/cross_validation")
    return parser.parse_args()


def custom_quantiles(signal: pd.DataFrame, factor: str, horizon: int) -> pd.DataFrame:
    rows = []
    for date, day in signal.dropna(subset=[factor, "forward_return_h"]).groupby("datetime", sort=True):
        if len(day) < 5:
            continue
        day = day.copy()
        day["quantile"] = pd.qcut(day[factor].rank(method="first"), 5, labels=False) + 1
        grouped = day.groupby("quantile")["forward_return_h"].mean()
        for quantile, value in grouped.items():
            rows.append({"datetime": date, "quantile": int(quantile), "value": float(value)})
    if not rows:
        return pd.DataFrame(columns=["datetime", "quantile", "value"])
    return pd.DataFrame(rows)


def custom_turnover(signal: pd.DataFrame, factor: str) -> float:
    sets = []
    for _, day in signal.dropna(subset=[factor]).groupby("datetime", sort=True):
        if len(day) < 5:
            continue
        ranks = day[factor].rank(method="first")
        sets.append(set(day.loc[(pd.qcut(ranks, 5, labels=False) + 1) == 5, "instrument"]))
    values = [1 - len(previous & current) / max(len(previous), 1) for previous, current in zip(sets, sets[1:])]
    return float(np.mean(values)) if values else float("nan")


def status_for_difference(difference: float, sample_match: bool, tolerance: float = 1e-10) -> str:
    if not sample_match:
        return "DATA_ALIGNMENT_DIFFERENCE"
    return "MATCH" if np.isfinite(difference) and abs(difference) <= tolerance else "SEMANTIC_DIFFERENCE"


def main() -> None:
    cli = args()
    with cli.config.open(encoding="utf-8") as handle:
        config = yaml.safe_load(handle)
    data = pd.read_csv(cli.input, compression="gzip", parse_dates=["datetime"])
    data = data.rename(columns={config["label"]["name"]: "forward_return"})
    factors = list(config["factors"])
    rank_rows: list[dict] = []
    quantile_rows: list[dict] = []
    turnover_rows: list[dict] = []
    metadata: list[dict] = []
    for split, bounds in config["splits"].items():
        for factor in factors:
            for horizon in (1, 5, 10, 20):
                factor_series, prices, aligned = aligned_inputs(data, factor, bounds["start"], bounds["end"], horizon)
                custom = horizon_returns(data, bounds["start"], bounds["end"], horizon)
                custom = custom[custom["datetime"].isin(aligned["datetime"].unique())].copy()
                custom_h = custom.rename(columns={"forward_return_h": "h_return"})
                custom_ic, custom_rank_ic = daily_ic_series(custom_h, factor, label="h_return")
                custom_rank_mean = custom_rank_ic.mean()
                period = f"{horizon}D"
                try:
                    clean = utils.get_clean_factor_and_forward_returns(
                        factor_series, prices, quantiles=5, periods=(horizon,), max_loss=1.0, cumulative_returns=True
                    )
                    alpha_ic = performance.factor_information_coefficient(clean)[period].mean()
                    alpha_means, _ = performance.mean_return_by_quantile(clean, by_date=True, demeaned=False)
                    alpha_quantile = alpha_means.groupby("factor_quantile")[period].mean()
                    custom_quantile = custom_quantiles(custom, factor, horizon).groupby("quantile")["value"].mean()
                    sample_match = len(clean) == int(custom_h[[factor, "h_return"]].dropna().shape[0])
                    rank_diff = float(custom_rank_mean - alpha_ic)
                    rank_rows.append({"split": split, "factor": factor, "horizon": period, "custom_rank_ic_mean": custom_rank_mean, "alphalens_rank_ic_mean": alpha_ic, "absolute_difference": abs(rank_diff), "custom_observations": int(custom_rank_ic.notna().sum()), "alphalens_observations": int(performance.factor_information_coefficient(clean)[period].notna().sum()), "status": status_for_difference(rank_diff, sample_match)})
                    for quantile in range(1, 6):
                        custom_value = custom_quantile.get(quantile, np.nan)
                        alpha_value = alpha_quantile.get(quantile, np.nan)
                        difference = float(custom_value - alpha_value)
                        quantile_rows.append({"split": split, "factor": factor, "horizon": period, "quantile": quantile, "custom_value": custom_value, "alphalens_value": alpha_value, "difference": difference, "status": status_for_difference(difference, sample_match)})
                    metadata.append({"split": split, "factor": factor, "horizon": period, "aligned_rows": len(aligned), "clean_rows": len(clean), "dropped_rows": len(aligned) - len(clean)})
                    if horizon == 1:
                        custom_value = custom_turnover(aligned, factor)
                        try:
                            alpha_turnover = performance.quantile_turnover(clean["factor_quantile"], 5, period=1).mean()
                            turnover_rows.append({"split": split, "factor": factor, "custom_turnover": custom_value, "alphalens_turnover": alpha_turnover, "difference": abs(custom_value - alpha_turnover), "definition_match": True, "status": "MATCH" if abs(custom_value - alpha_turnover) <= 1e-10 else "SEMANTIC_DIFFERENCE", "error": ""})
                        except Exception as turnover_error:
                            turnover_rows.append({"split": split, "factor": factor, "custom_turnover": custom_value, "alphalens_turnover": np.nan, "difference": np.nan, "definition_match": False, "status": "SEMANTIC_DIFFERENCE", "error": repr(turnover_error)})
                except Exception as exc:  # preserve a machine-readable ERROR rather than hiding oracle failures
                    rank_rows.append({"split": split, "factor": factor, "horizon": period, "custom_rank_ic_mean": custom_rank_mean, "alphalens_rank_ic_mean": np.nan, "absolute_difference": np.nan, "custom_observations": int(custom_rank_ic.notna().sum()), "alphalens_observations": 0, "status": "ERROR", "error": repr(exc)})
                    for quantile in range(1, 6):
                        quantile_rows.append({"split": split, "factor": factor, "horizon": period, "quantile": quantile, "custom_value": np.nan, "alphalens_value": np.nan, "difference": np.nan, "status": "ERROR", "error": repr(exc)})
                    if horizon == 1:
                        turnover_rows.append({"split": split, "factor": factor, "custom_turnover": np.nan, "alphalens_turnover": np.nan, "difference": np.nan, "definition_match": False, "status": "ERROR", "error": repr(exc)})
    cli.output_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rank_rows).to_csv(cli.output_dir / "rank_ic_cross_validation.csv", index=False)
    pd.DataFrame(quantile_rows).to_csv(cli.output_dir / "quantile_return_cross_validation.csv", index=False)
    pd.DataFrame(turnover_rows).to_csv(cli.output_dir / "turnover_cross_validation.csv", index=False)
    pd.DataFrame(metadata).to_csv(cli.output_dir / "alignment_metadata.csv", index=False)
    print(f"rank_rows={len(rank_rows)} quantile_rows={len(quantile_rows)} turnover_rows={len(turnover_rows)}")


if __name__ == "__main__":
    main()
