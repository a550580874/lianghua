"""Exact-sample and forward-return-layer validation for Alphalens Reloaded."""

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
from adapter import aligned_inputs, split_dates  # noqa: E402


HORIZONS = (1, 5, 10, 20)
TOLERANCE = 1e-10
# Daily comparison files can contain millions of instrument rows.  Keep a
# deterministic bounded detail sample while all aggregate counters are
# computed over the complete input.
DETAIL_LIMIT = 100_000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "research/factor_v1/output/factors.csv.gz")
    parser.add_argument("--config", type=Path, default=ROOT / "research/factor_v1/config.yaml")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "research/factor_v1/output/cross_validation_exact")
    return parser.parse_args()


def custom_quantile(values: pd.Series) -> pd.Series:
    return pd.qcut(values.rank(method="first"), 5, labels=False) + 1


def exact_inputs(rows: pd.DataFrame, factor: str, horizon: int) -> tuple[pd.Series, pd.DataFrame]:
    rows = rows.dropna(subset=[factor, "forward_return_h"])
    index = pd.MultiIndex.from_frame(rows[["datetime", "instrument"]], names=["date", "asset"])
    factor_series = pd.Series(rows[factor].to_numpy(), index=index, name="factor")
    forward = pd.DataFrame({f"{horizon}D": rows["forward_return_h"].to_numpy()}, index=index)
    return factor_series, forward


def rank_ic_rows(clean: pd.DataFrame, split: str, factor: str, horizon: str) -> list[dict]:
    alpha = performance.factor_information_coefficient(clean)[horizon]
    rows: list[dict] = []
    for date, day in clean.groupby(level="date", sort=True):
        values = day[["factor", horizon]].dropna()
        custom = values["factor"].corr(values[horizon], method="spearman") if len(values) >= 2 else np.nan
        alpha_value = alpha.get(date, np.nan)
        difference = custom - alpha_value
        rows.append({"split": split, "factor": factor, "horizon": horizon, "date": date, "custom_rank_ic": custom, "alphalens_rank_ic": alpha_value, "difference": difference, "status": "MATCH" if pd.notna(difference) and abs(difference) <= TOLERANCE else "IMPLEMENTATION_BUG"})
    return rows


def quantile_rows(clean: pd.DataFrame, split: str, factor: str, horizon: str) -> tuple[list[dict], list[dict]]:
    work = clean[["factor", horizon, "factor_quantile"]].copy()
    work["custom_quantile"] = work.groupby(level="date")["factor"].transform(custom_quantile)
    assignment_frame = work.reset_index().rename(columns={"factor": "factor_value", "factor_quantile": "alphalens_quantile"})
    assignment_frame["split"], assignment_frame["factor"], assignment_frame["horizon"] = split, factor, horizon
    assignment_frame["match"] = assignment_frame["custom_quantile"] == assignment_frame["alphalens_quantile"]
    assignments = assignment_frame[["split", "factor", "horizon", "date", "asset", "factor_value", "custom_quantile", "alphalens_quantile", "match"]].rename(columns={"asset": "instrument"}).to_dict("records")
    custom_means = work.groupby([work.index.get_level_values("date"), "custom_quantile"])[horizon].mean().rename("custom_return").reset_index().rename(columns={"level_0": "date", "custom_quantile": "quantile"})
    alpha_means = work.groupby([work.index.get_level_values("date"), "factor_quantile"])[horizon].mean().rename("alphalens_return").reset_index().rename(columns={"level_0": "date", "factor_quantile": "quantile"})
    result = custom_means.merge(alpha_means, on=["date", "quantile"], how="outer")
    rows = []
    for _, row in result.iterrows():
        difference = row["custom_return"] - row["alphalens_return"]
        rows.append({"split": split, "factor": factor, "horizon": horizon, "date": row["date"], "quantile": int(row["quantile"]), "custom_return": row["custom_return"], "alphalens_return": row["alphalens_return"], "difference": difference, "status": "MATCH" if pd.notna(difference) and abs(difference) <= TOLERANCE else "SEMANTIC_DIFFERENCE"})
    return assignments, rows


def turnover_rows(clean: pd.DataFrame, split: str, factor: str) -> list[dict]:
    labels = clean["factor_quantile"]
    dates = sorted(labels.index.get_level_values("date").unique())
    rows: list[dict] = []
    for previous_date, current_date in zip(dates, dates[1:]):
        previous = set(labels.loc[previous_date][labels.loc[previous_date] == 5].index)
        current = set(labels.loc[current_date][labels.loc[current_date] == 5].index)
        overlap = len(previous & current)
        previous_size, current_size = len(previous), len(current)
        custom = 1 - overlap / previous_size if previous_size else np.nan
        alpha = 1 - overlap / current_size if current_size else np.nan
        rows.append({"split": split, "factor": factor, "date": current_date, "previous_size": previous_size, "current_size": current_size, "overlap": overlap, "custom_turnover": custom, "alphalens_formula_turnover": alpha, "difference": custom - alpha, "status": "EFFECTIVELY_EQUIVALENT" if previous_size == current_size else "SEMANTIC_DIFFERENCE"})
    return rows


def forward_alignment_multi(data: pd.DataFrame, horizon_cache: dict[int, pd.DataFrame], split: str, bounds: dict) -> tuple[list[dict], list[dict]]:
    # Alignment depends only on the price calendar, not on factor identity.
    factor_series, prices, _ = aligned_inputs(data, "ROC20", bounds["start"], bounds["end"], 1)
    alpha = utils.compute_forward_returns(factor_series, prices, periods=HORIZONS, cumulative_returns=True).reset_index()
    alpha = alpha.rename(columns={"date": "entry_date", "asset": "instrument"})
    dates = split_dates(data, bounds["start"], bounds["end"])
    previous = {dates[i + 1]: dates[i] for i in range(len(dates) - 1)}
    alpha["datetime"] = alpha["entry_date"].map(previous)
    all_rows, all_summaries = [], []
    for horizon in HORIZONS:
        period = f"{horizon}D"
        custom = horizon_cache[horizon].dropna(subset=["forward_return_h"])
        custom = custom.rename(columns={"forward_return_h": "custom_forward_return"})
        merged = custom[["datetime", "instrument", "custom_forward_return"]].merge(alpha[["datetime", "instrument", period]].rename(columns={period: "alphalens_forward_return"}), on=["datetime", "instrument"], how="outer", indicator=True)
        merged["difference"] = merged["custom_forward_return"] - merged["alphalens_forward_return"]
        merged["status"] = np.where(merged["_merge"].eq("both") & merged["difference"].abs().le(TOLERANCE), "MATCH", "DATA_ALIGNMENT_DIFFERENCE")
        merged["split"], merged["factor"], merged["horizon"] = split, "ALL", period
        detail = merged.rename(columns={"datetime": "date"})[["split", "factor", "horizon", "date", "instrument", "custom_forward_return", "alphalens_forward_return", "difference", "status"]]
        all_rows.extend(detail.head(DETAIL_LIMIT).to_dict("records"))
        summary = {"split": split, "factor": "ALL", "horizon": period, "common_rows": int((merged["_merge"] == "both").sum()), "custom_only_rows": int((merged["_merge"] == "left_only").sum()), "alphalens_only_rows": int((merged["_merge"] == "right_only").sum())}
        common = merged[merged["_merge"] == "both"].copy()
        summary["max_abs_difference"] = float((common["custom_forward_return"] - common["alphalens_forward_return"]).abs().max()) if len(common) else np.nan
        summary["mean_abs_difference"] = float((common["custom_forward_return"] - common["alphalens_forward_return"]).abs().mean()) if len(common) else np.nan
        summary["missing_rows"] = summary["custom_only_rows"] + summary["alphalens_only_rows"]
        summary["mismatch_rows"] = int(((common["custom_forward_return"] - common["alphalens_forward_return"]).abs() > TOLERANCE).sum()) if len(common) else 0
        all_summaries.append(summary)
    return all_rows, all_summaries
def main() -> None:
    cli = parse_args()
    with cli.config.open(encoding="utf-8") as handle:
        config = yaml.safe_load(handle)
    data = pd.read_csv(cli.input, compression="gzip", parse_dates=["datetime"])
    rank_exact: list[dict] = []
    rank_summary: list[dict] = []
    assignments: list[dict] = []
    quantile_exact: list[dict] = []
    turnover: list[dict] = []
    alignment: list[dict] = []
    alignment_summary: list[dict] = []
    for split, bounds in config["splits"].items():
        horizon_cache = {horizon: horizon_returns(data, bounds["start"], bounds["end"], horizon) for horizon in HORIZONS}
        for factor in config["factors"]:
            one_day_clean = None
            for horizon in HORIZONS:
                factor_series, forward = exact_inputs(horizon_cache[horizon], factor, horizon)
                clean = utils.get_clean_factor(factor_series, forward, quantiles=5, max_loss=1.0)
                period = f"{horizon}D"
                daily = rank_ic_rows(clean, split, factor, period)
                rank_exact.extend(daily)
                diffs = pd.Series([abs(row["difference"]) for row in daily if pd.notna(row["difference"])])
                rank_summary.append({"split": split, "factor": factor, "horizon": period, "rows": len(daily), "max_abs_difference": diffs.max() if len(diffs) else np.nan, "mean_abs_difference": diffs.mean() if len(diffs) else np.nan, "exact_match_days": int(sum(row["status"] == "MATCH" for row in daily)), "mismatch_days": int(sum(row["status"] != "MATCH" for row in daily)), "status": "MATCH" if all(row["status"] == "MATCH" for row in daily) else "IMPLEMENTATION_BUG"})
                assignment, qreturns = quantile_rows(clean, split, factor, period)
                assignments.extend(assignment[:DETAIL_LIMIT])
                quantile_exact.extend(qreturns[:DETAIL_LIMIT])
                if horizon == 1:
                    one_day_clean = clean
            turnover.extend(turnover_rows(one_day_clean, split, factor))
        if config["factors"]:
            forward_rows, forward_stats = forward_alignment_multi(data, horizon_cache, split, bounds)
            alignment.extend(forward_rows)
            alignment_summary.extend(forward_stats)
    out = cli.output_dir
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rank_exact).to_csv(out / "rank_ic_exact_comparison.csv", index=False)
    pd.DataFrame(rank_summary).to_csv(out / "rank_ic_exact_summary.csv", index=False)
    pd.DataFrame(assignments).to_csv(out / "quantile_assignment_comparison.csv", index=False)
    pd.DataFrame(quantile_exact).to_csv(out / "quantile_return_exact_comparison.csv", index=False)
    pd.DataFrame(turnover).to_csv(out / "turnover_definition_analysis.csv", index=False)
    pd.DataFrame(alignment).to_csv(out / "forward_return_alignment.csv", index=False)
    pd.DataFrame(alignment_summary).to_csv(out / "forward_return_alignment_summary.csv", index=False)
    print(f"rank_rows={len(rank_exact)} assignment_rows={len(assignments)} quantile_rows={len(quantile_exact)} turnover_rows={len(turnover)} alignment_rows={len(alignment)}")


if __name__ == "__main__":
    main()
