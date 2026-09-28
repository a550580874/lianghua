"""Compute split, annual IC, quantile-return and top-quantile turnover summaries."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import yaml


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path(__file__).with_name("config.yaml"))
    parser.add_argument("--input", type=Path, default=Path(__file__).parent / "output" / "factors.csv.gz")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).with_name("output"))
    return parser.parse_args()


def daily_correlations(frame: pd.DataFrame, factor: str) -> tuple[pd.Series, pd.Series]:
    values = frame[["datetime", factor, "forward_return"]].dropna()
    ic_values: list[float] = []
    rank_values: list[float] = []
    for _, day in values.groupby("datetime", sort=True):
        if len(day) < 2 or day[factor].nunique() < 2 or day["forward_return"].nunique() < 2:
            continue
        ic_values.append(day[factor].corr(day["forward_return"], method="pearson"))
        rank_values.append(day[factor].corr(day["forward_return"], method="spearman"))
    return pd.Series(ic_values, dtype="float64"), pd.Series(rank_values, dtype="float64")


def ratio(mean: float, std: float) -> float:
    return float(mean / std) if pd.notna(std) and std > 0 else float("nan")


def quantile_rows(frame: pd.DataFrame, factor: str, split: str, quantile_count: int) -> tuple[list[dict], float, bool]:
    values = frame[["datetime", "instrument", factor, "forward_return"]].dropna()
    daily: list[pd.DataFrame] = []
    top_sets: list[tuple[pd.Timestamp, set[str]]] = []
    for date, day in values.groupby("datetime", sort=True):
        if len(day) < quantile_count:
            continue
        ranked = day[factor].rank(method="first")
        day = day.assign(quantile=pd.qcut(ranked, quantile_count, labels=False) + 1)
        daily.append(
            day.groupby("quantile", as_index=False)["forward_return"]
            .agg(mean_forward_return="mean", observations="count")
            .assign(datetime=date)
        )
        top_sets.append((date, set(day.loc[day["quantile"] == quantile_count, "instrument"])))

    if not daily:
        return [], float("nan"), False
    quantile_frame = pd.concat(daily, ignore_index=True)
    aggregate = quantile_frame.groupby("quantile")["mean_forward_return"].mean()
    q1 = aggregate.get(1, np.nan)
    q5 = aggregate.get(quantile_count, np.nan)
    spread = float(q5 - q1) if pd.notna(q1) and pd.notna(q5) else float("nan")
    ordered = aggregate.reindex(range(1, quantile_count + 1)).dropna()
    monotonic = bool(ordered.is_monotonic_increasing or ordered.is_monotonic_decreasing)
    rows = []
    for _, row in quantile_frame.groupby("quantile", as_index=False).agg(
        mean_forward_return=("mean_forward_return", "mean"),
        observations=("observations", "sum"),
    ).iterrows():
        rows.append(
            {
                "split": split,
                "factor": factor,
                "quantile": int(row["quantile"]),
                "mean_forward_return": row["mean_forward_return"],
                "observations": int(row["observations"]),
                "q5_q1_spread": spread,
                "monotonic_original_direction": monotonic,
            }
        )
    return rows, spread, monotonic


def turnover(values: pd.DataFrame, factor: str, quantile_count: int) -> tuple[float, int]:
    top_sets: list[set[str]] = []
    for _, day in values[["datetime", "instrument", factor]].dropna().groupby("datetime", sort=True):
        if len(day) < quantile_count:
            continue
        ranks = day[factor].rank(method="first")
        top_sets.append(set(day.loc[(pd.qcut(ranks, quantile_count, labels=False) + 1) == quantile_count, "instrument"]))
    changes = []
    for previous, current in zip(top_sets, top_sets[1:]):
        changes.append(1.0 - (len(previous & current) / max(len(previous), 1)))
    return (float(np.mean(changes)) if changes else float("nan"), len(changes))


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    data = pd.read_csv(args.input, compression="gzip", parse_dates=["datetime"])
    factors = list(config["factors"])
    label = config["label"]["name"]
    data = data.rename(columns={label: "forward_return"})
    quantile_count = int(config["quantiles"])
    summary: list[dict] = []
    annual: list[dict] = []
    quantiles: list[dict] = []

    for split, bounds in config["splits"].items():
        split_data = data[data["datetime"].between(bounds["start"], bounds["end"])].copy()
        for factor in factors:
            ic, rank_ic = daily_correlations(split_data, factor)
            quantile_data, spread, monotonic = quantile_rows(split_data, factor, split, quantile_count)
            quantiles.extend(quantile_data)
            turnover_mean, turnover_obs = turnover(split_data, factor, quantile_count)
            summary.append(
                {
                    "split": split,
                    "factor": factor,
                    "observations": int(split_data[[factor, "forward_return"]].dropna().shape[0]),
                    "ic_mean": ic.mean(),
                    "ic_std": ic.std(ddof=0),
                    "icir": ratio(ic.mean(), ic.std(ddof=0)),
                    "rank_ic_mean": rank_ic.mean(),
                    "rank_ic_std": rank_ic.std(ddof=0),
                    "rank_icir": ratio(rank_ic.mean(), rank_ic.std(ddof=0)),
                    "q5_q1_spread": spread,
                    "quantile_monotonic_original_direction": monotonic,
                    "top_quantile_turnover": turnover_mean,
                    "turnover_observations": turnover_obs,
                }
            )
            dated = split_data[["datetime", factor, "forward_return"]].dropna().assign(
                year=lambda frame: frame["datetime"].dt.year
            )
            for year, year_data in dated.groupby("year", sort=True):
                year_ic, year_rank_ic = daily_correlations(year_data, factor)
                annual.append(
                    {
                        "split": split,
                        "factor": factor,
                        "year": int(year),
                        "ic_mean": year_ic.mean(),
                        "rank_ic_mean": year_rank_ic.mean(),
                        "observations": int(len(year_data)),
                    }
                )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(summary).to_csv(args.output_dir / "factor_summary.csv", index=False)
    pd.DataFrame(annual).to_csv(args.output_dir / "factor_ic_by_year.csv", index=False)
    pd.DataFrame(quantiles).to_csv(args.output_dir / "quantile_returns.csv", index=False)
    # Keep a dedicated, explicit turnover table even though the summary also carries its mean.
    turnover_summary = pd.DataFrame(
        [
            {
                "split": row["split"],
                "factor": row["factor"],
                "top_quantile_turnover": row["top_quantile_turnover"],
                "observations": row["turnover_observations"],
                "definition": "1 - overlap(previous top Q5, current top Q5) / previous top Q5 size",
            }
            for row in summary
        ]
    )
    turnover_summary.to_csv(args.output_dir / "turnover.csv", index=False)
    print(f"splits={len(config['splits'])}")
    print(f"factors={len(factors)}")
    print(f"summary={args.output_dir / 'factor_summary.csv'}")


if __name__ == "__main__":
    main()
