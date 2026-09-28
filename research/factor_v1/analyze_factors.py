"""Compute Factor Research v1 summaries and v2 robustness diagnostics."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from diagnostics import (
    daily_ic_series,
    distribution_stats,
    factor_correlation_rows,
    horizon_returns,
    rank_autocorrelation_series,
    spread_stats,
)


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path(__file__).with_name("config.yaml"))
    parser.add_argument("--input", type=Path, default=Path(__file__).parent / "output" / "factors.csv.gz")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).with_name("output"))
    return parser.parse_args()


def ratio(mean: float, std: float) -> float:
    return float(mean / std) if pd.notna(std) and std > 0 else float("nan")


def quantile_rows(frame: pd.DataFrame, factor: str, split: str, quantile_count: int) -> tuple[list[dict], float, bool]:
    values = frame[["datetime", "instrument", factor, "forward_return"]].dropna()
    daily: list[pd.DataFrame] = []
    for date, day in values.groupby("datetime", sort=True):
        if len(day) < quantile_count:
            continue
        ranked = day[factor].rank(method="first")
        day = day.assign(quantile=pd.qcut(ranked, quantile_count, labels=False) + 1)
        daily.append(day.groupby("quantile", as_index=False)["forward_return"].agg(
            mean_forward_return="mean", observations="count"
        ).assign(datetime=date))
    if not daily:
        return [], float("nan"), False
    quantile_frame = pd.concat(daily, ignore_index=True)
    aggregate = quantile_frame.groupby("quantile")["mean_forward_return"].mean()
    q1, q5 = aggregate.get(1, np.nan), aggregate.get(quantile_count, np.nan)
    spread = float(q5 - q1) if pd.notna(q1) and pd.notna(q5) else float("nan")
    ordered = aggregate.reindex(range(1, quantile_count + 1)).dropna()
    monotonic = bool(ordered.is_monotonic_increasing or ordered.is_monotonic_decreasing)
    rows = []
    for _, row in quantile_frame.groupby("quantile", as_index=False).agg(
        mean_forward_return=("mean_forward_return", "mean"), observations=("observations", "sum")
    ).iterrows():
        rows.append({
            "split": split, "factor": factor, "quantile": int(row["quantile"]),
            "mean_forward_return": row["mean_forward_return"], "observations": int(row["observations"]),
            "q5_q1_spread": spread, "monotonic_original_direction": monotonic,
        })
    return rows, spread, monotonic


def turnover(values: pd.DataFrame, factor: str, quantile_count: int) -> tuple[float, int]:
    top_sets: list[set[str]] = []
    for _, day in values[["datetime", "instrument", factor]].dropna().groupby("datetime", sort=True):
        if len(day) < quantile_count:
            continue
        ranks = day[factor].rank(method="first")
        top_sets.append(set(day.loc[(pd.qcut(ranks, quantile_count, labels=False) + 1) == quantile_count, "instrument"]))
    changes = [1.0 - len(previous & current) / max(len(previous), 1) for previous, current in zip(top_sets, top_sets[1:])]
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
    coverage: list[dict] = []
    autocorrelation: list[dict] = []
    decay: list[dict] = []
    correlations: list[dict] = []
    spread_summaries: list[dict] = []

    for split, bounds in config["splits"].items():
        split_data = data[data["datetime"].between(bounds["start"], bounds["end"])].copy()
        correlations.extend(factor_correlation_rows(split_data, factors, split))
        horizon_frames = {
            horizon: horizon_returns(data, bounds["start"], bounds["end"], horizon)
            for horizon in (1, 5, 10, 20)
        }
        for factor in factors:
            total_rows = len(split_data)
            valid_factor = split_data[factor].notna()
            valid_both = valid_factor & split_data["forward_return"].notna()
            coverage.append({
                "split": split, "factor": factor, "total_rows": total_rows,
                "valid_factor_observations": int(valid_factor.sum()),
                "valid_factor_and_label_observations": int(valid_both.sum()),
                "missing_factor_observations": int((~valid_factor).sum()),
                "missing_label_observations": int((~split_data["forward_return"].notna()).sum()),
                "coverage_ratio": float(valid_both.sum() / total_rows) if total_rows else float("nan"),
                "unique_factor_values": int(split_data.loc[valid_factor, factor].nunique()),
                "trading_days": int(split_data.loc[valid_factor, "datetime"].nunique()),
                "average_daily_cross_section": float(split_data.loc[valid_factor].groupby("datetime").size().mean()),
                "median_daily_cross_section": float(split_data.loc[valid_factor].groupby("datetime").size().median()),
                "min_daily_cross_section": int(split_data.loc[valid_factor].groupby("datetime").size().min()),
                "max_daily_cross_section": int(split_data.loc[valid_factor].groupby("datetime").size().max()),
            })
            ic, rank_ic = daily_ic_series(split_data, factor)
            ic_stats, rank_stats = distribution_stats(ic), distribution_stats(rank_ic)
            quantile_data, spread, monotonic = quantile_rows(split_data, factor, split, quantile_count)
            quantiles.extend(quantile_data)
            turnover_mean, turnover_obs = turnover(split_data, factor, quantile_count)
            summary.append({
                "split": split, "factor": factor,
                "observations": int(split_data[[factor, "forward_return"]].dropna().shape[0]),
                "ic_mean": ic_stats["mean"], "ic_std": ic_stats["std"], "icir": ratio(ic_stats["mean"], ic_stats["std"]),
                "rank_ic_mean": rank_stats["mean"], "rank_ic_std": rank_stats["std"], "rank_icir": ratio(rank_stats["mean"], rank_stats["std"]),
                "q5_q1_spread": spread, "quantile_monotonic_original_direction": monotonic,
                "top_quantile_turnover": turnover_mean, "turnover_observations": turnover_obs,
                "ic_median": ic_stats["median"], "ic_positive_ratio": ic_stats["positive_ratio"], "ic_negative_ratio": ic_stats["negative_ratio"],
                "ic_standard_error": ic_stats["standard_error"], "ic_t_stat": ic_stats["t_stat"], "ic_observation_days": ic_stats["observations"],
                "rank_ic_median": rank_stats["median"], "rank_ic_positive_ratio": rank_stats["positive_ratio"], "rank_ic_negative_ratio": rank_stats["negative_ratio"],
                "rank_ic_standard_error": rank_stats["standard_error"], "rank_ic_t_stat": rank_stats["t_stat"], "rank_ic_observation_days": rank_stats["observations"],
            })
            auto_series = rank_autocorrelation_series(split_data, factor)
            auto_stats = distribution_stats(auto_series)
            autocorrelation.append({"split": split, "factor": factor, "mean": auto_stats["mean"], "median": auto_stats["median"], "std": auto_stats["std"], "min": auto_series.min(), "max": auto_series.max(), "observation_pairs": auto_stats["observations"], "positive_ratio": auto_stats["positive_ratio"]})
            spread_summaries.append({"split": split, "factor": factor, **spread_stats(split_data, factor, quantile_count)})
            dated = split_data[["datetime", factor, "forward_return"]].dropna().assign(year=lambda frame: frame["datetime"].dt.year)
            for year, year_data in dated.groupby("year", sort=True):
                year_ic, year_rank_ic = daily_ic_series(year_data, factor)
                annual.append({"split": split, "factor": factor, "year": int(year), "ic_mean": year_ic.mean(), "rank_ic_mean": year_rank_ic.mean(), "observations": int(len(year_data))})

            for horizon in (1, 5, 10, 20):
                horizon_data = horizon_frames[horizon]
                h_ic, h_rank_ic = daily_ic_series(horizon_data.rename(columns={"forward_return_h": "h_return"}), factor, label="h_return")
                h_stats, h_rank_stats = distribution_stats(h_ic), distribution_stats(h_rank_ic)
                definition = f"Ref($close, -{horizon + 1}) / Ref($close, -1) - 1"
                decay.append({"split": split, "factor": factor, "horizon": f"{horizon}D", "horizon_days": horizon, "forward_return_definition": definition, "ic_mean": h_stats["mean"], "ic_std": h_stats["std"], "icir": ratio(h_stats["mean"], h_stats["std"]), "rank_ic_mean": h_rank_stats["mean"], "rank_ic_std": h_rank_stats["std"], "rank_icir": ratio(h_rank_stats["mean"], h_rank_stats["std"]), "ic_observation_days": h_stats["observations"], "rank_ic_observation_days": h_rank_stats["observations"]})

    args.output_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(summary).to_csv(args.output_dir / "factor_summary.csv", index=False)
    pd.DataFrame(annual).to_csv(args.output_dir / "factor_ic_by_year.csv", index=False)
    pd.DataFrame(quantiles).to_csv(args.output_dir / "quantile_returns.csv", index=False)
    pd.DataFrame(coverage).to_csv(args.output_dir / "factor_coverage.csv", index=False)
    pd.DataFrame(autocorrelation).to_csv(args.output_dir / "factor_rank_autocorrelation.csv", index=False)
    pd.DataFrame(decay).to_csv(args.output_dir / "factor_decay.csv", index=False)
    pd.DataFrame(correlations).to_csv(args.output_dir / "factor_correlation.csv", index=False)
    pd.DataFrame(spread_summaries).to_csv(args.output_dir / "quantile_spread_stats.csv", index=False)
    pd.DataFrame([{"split": row["split"], "factor": row["factor"], "top_quantile_turnover": row["top_quantile_turnover"], "observations": row["turnover_observations"], "definition": "1 - overlap(previous top Q5, current top Q5) / previous top Q5 size"} for row in summary]).to_csv(args.output_dir / "turnover.csv", index=False)
    print(f"splits={len(config['splits'])}")
    print(f"factors={len(factors)}")
    print(f"summary={args.output_dir / 'factor_summary.csv'}")
    print("diagnostics=coverage,rank_autocorrelation,decay,correlation,quantile_spread_stats")


if __name__ == "__main__":
    main()
