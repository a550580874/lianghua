"""Reusable, deterministic statistics for Factor Research v2 diagnostics."""

from __future__ import annotations

from math import sqrt
from typing import Iterable

import numpy as np
import pandas as pd


def distribution_stats(values: Iterable[float]) -> dict[str, float | int]:
    series = pd.Series(list(values), dtype="float64").dropna()
    n = int(series.size)
    mean = float(series.mean()) if n else float("nan")
    std = float(series.std(ddof=1)) if n > 1 else float("nan")
    standard_error = float(std / sqrt(n)) if n > 1 else float("nan")
    return {
        "mean": mean,
        "std": std,
        "median": float(series.median()) if n else float("nan"),
        "positive_ratio": float((series > 0).mean()) if n else float("nan"),
        "negative_ratio": float((series < 0).mean()) if n else float("nan"),
        "standard_error": standard_error,
        "t_stat": float(mean / standard_error) if pd.notna(standard_error) and standard_error > 0 else float("nan"),
        "observations": n,
    }


def daily_ic_series(frame: pd.DataFrame, factor: str, label: str = "forward_return") -> tuple[pd.Series, pd.Series]:
    values = frame[["datetime", factor, label]].dropna()
    ic_values: list[float] = []
    rank_values: list[float] = []
    for _, day in values.groupby("datetime", sort=True):
        if len(day) < 2 or day[factor].nunique() < 2 or day[label].nunique() < 2:
            continue
        ic_values.append(day[factor].corr(day[label], method="pearson"))
        rank_values.append(day[factor].corr(day[label], method="spearman"))
    return pd.Series(ic_values, dtype="float64"), pd.Series(rank_values, dtype="float64")


def rank_autocorrelation_series(frame: pd.DataFrame, factor: str) -> pd.Series:
    values = frame[["datetime", "instrument", factor]].dropna().copy()
    dates = sorted(values["datetime"].unique())
    result: list[float] = []
    for previous_date, current_date in zip(dates, dates[1:]):
        previous = values[values["datetime"] == previous_date][["instrument", factor]].rename(columns={factor: "previous"})
        current = values[values["datetime"] == current_date][["instrument", factor]].rename(columns={factor: "current"})
        common = previous.merge(current, on="instrument", how="inner").dropna()
        if len(common) >= 2 and common["previous"].nunique() > 1 and common["current"].nunique() > 1:
            result.append(float(common["previous"].corr(common["current"], method="spearman")))
    return pd.Series(result, dtype="float64")


def factor_correlation_rows(frame: pd.DataFrame, factors: list[str], split: str) -> list[dict]:
    records: list[dict] = []
    for method in ("pearson", "spearman"):
        values: dict[tuple[str, str], list[float]] = {(a, b): [] for a in factors for b in factors}
        for _, day in frame[["datetime", *factors]].groupby("datetime", sort=True):
            matrix = day[factors].corr(method=method)
            for factor_a in factors:
                for factor_b in factors:
                    value = matrix.loc[factor_a, factor_b]
                    if pd.notna(value):
                        values[(factor_a, factor_b)].append(float(value))
        for (factor_a, factor_b), observations in values.items():
            records.append({
                "split": split,
                "method": method,
                "factor_a": factor_a,
                "factor_b": factor_b,
                "mean_correlation": float(np.mean(observations)) if observations else float("nan"),
                "observation_days": len(observations),
            })
    return records


def spread_stats(frame: pd.DataFrame, factor: str, quantile_count: int = 5) -> dict:
    daily_spreads: list[float] = []
    values = frame[["datetime", factor, "forward_return"]].dropna()
    for _, day in values.groupby("datetime", sort=True):
        if len(day) < quantile_count:
            continue
        ranks = day[factor].rank(method="first")
        quantiles = pd.qcut(ranks, quantile_count, labels=False) + 1
        grouped = day.assign(quantile=quantiles).groupby("quantile")["forward_return"].mean()
        if 1 in grouped and quantile_count in grouped:
            daily_spreads.append(float(grouped[quantile_count] - grouped[1]))
    stats = distribution_stats(daily_spreads)
    return {
        "spread_mean": stats["mean"],
        "spread_median": stats["median"],
        "spread_std": stats["std"],
        "spread_standard_error": stats["standard_error"],
        "spread_t_stat": stats["t_stat"],
        "positive_day_ratio": stats["positive_ratio"],
        "negative_day_ratio": stats["negative_ratio"],
        "observation_days": stats["observations"],
    }


def horizon_returns(frame: pd.DataFrame, split_start: str, split_end: str, horizon: int) -> pd.DataFrame:
    """Build H-day returns without using prices beyond the split boundary."""
    values = frame[["datetime", "instrument", "close", *[c for c in frame.columns if c not in {"datetime", "instrument", "close"}]]].copy()
    values = values.sort_values(["instrument", "datetime"])
    grouped = values.groupby("instrument", group_keys=False)
    values["entry_close"] = grouped["close"].shift(-1)
    values["exit_close"] = grouped["close"].shift(-(horizon + 1))
    values["exit_datetime"] = grouped["datetime"].shift(-(horizon + 1))
    values["forward_return_h"] = values["exit_close"] / values["entry_close"] - 1
    selected = values[values["datetime"].between(split_start, split_end)].copy()
    selected = selected[selected["exit_datetime"].le(pd.Timestamp(split_end))]
    return selected.dropna(subset=["forward_return_h"])
