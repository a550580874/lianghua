"""Render the machine-readable Factor Research v1 outputs as Markdown."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path(__file__).with_name("config.yaml"))
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).with_name("output"))
    return parser.parse_args()


def fmt(value: object) -> str:
    if pd.isna(value):
        return "NA"
    if isinstance(value, float):
        return f"{value:.6f}"
    return str(value)


def main() -> None:
    args = parse_args()
    with args.config.open(encoding="utf-8") as handle:
        config = yaml.safe_load(handle)
    summary = pd.read_csv(args.output_dir / "factor_summary.csv")
    annual = pd.read_csv(args.output_dir / "factor_ic_by_year.csv")
    quantiles = pd.read_csv(args.output_dir / "quantile_returns.csv")
    turnover = pd.read_csv(args.output_dir / "turnover.csv")

    lines = [
        "# Factor Research v1",
        "",
        "本报告直接消费 Qlib 0.9.7 Alpha158 raw handler 输出；没有重新实现或修改任何因子公式，没有训练模型，也没有形成买卖策略。",
        "",
        "## Data",
        "",
        f"- Framework: Qlib 0.9.7; frequency: `{config['frequency']}`; provider: `{config['provider_uri']}`.",
        "- The provider is the previously validated China sample dataset; its known provenance and cutoff are documented in `results/qlib.md`.",
        "",
        "## Universe",
        "",
        f"- Instrument universe: `{config['universe']}` (CSI300).",
        f"- Splits: {config['splits']}",
        "",
        "## Label",
        "",
        f"- Official Alpha158 label: `{config['label']['expression']}`.",
        "- Interpretation: the target uses the T+1 to T+2 Chinese-stock time sequence documented by Qlib; it is not a claim that portfolio-level T+1 enforcement was validated here.",
        "- Timing invariant: `information_cutoff <= signal_time <= forward_return_period`; configured here as `signal_time <= t <= t+1_to_t+2`.",
        "",
        "## Factors",
        "",
        f"- Selected unchanged Alpha158 columns: {', '.join(f'`{x}`' for x in config['factors'])}.",
        "- Original factor direction is retained. No sign flip or parameter selection is performed.",
    ]
    for split in config["splits"]:
        lines.extend(["", f"## {split.title()} Results", "", "| Factor | IC mean | IC std | ICIR | Rank IC mean | Rank ICIR | Q5-Q1 | Top-Q turnover |", "|---|---:|---:|---:|---:|---:|---:|---:|"])
        for _, row in summary[summary["split"] == split].iterrows():
            lines.append("| " + " | ".join(fmt(row[key]) for key in ["factor", "ic_mean", "ic_std", "icir", "rank_ic_mean", "rank_icir", "q5_q1_spread", "top_quantile_turnover"]) + " |")

    lines.extend(["", "## IC Stability", "", "Annual IC and Rank IC are reported without selecting years or changing factor definitions.", "", "| Split | Factor | Year | IC | Rank IC | Observations |", "|---|---|---:|---:|---:|---:|"])
    for _, row in annual.iterrows():
        lines.append("| " + " | ".join(fmt(row[key]) for key in ["split", "factor", "year", "ic_mean", "rank_ic_mean", "observations"]) + " |")

    lines.extend(["", "## Quantile Analysis", "", "Each trading date is ranked cross-sectionally into five groups. Q5-Q1 is the mean of daily Q5 minus Q1 returns; no direction is inverted.", "", "| Split | Factor | Quantile | Mean forward return | Observations | Q5-Q1 spread | Original-direction monotonic |", "|---|---|---:|---:|---:|---:|---|"])
    for _, row in quantiles.iterrows():
        lines.append("| " + " | ".join(fmt(row[key]) for key in ["split", "factor", "quantile", "mean_forward_return", "observations", "q5_q1_spread", "monotonic_original_direction"]) + " |")

    lines.extend(["", "## Turnover", "", "Top-quantile turnover definition: `1 - overlap(previous top Q5, current top Q5) / previous top Q5 size`, averaged over adjacent trading dates within each split.", "", "| Split | Factor | Top-quantile turnover | Observations |", "|---|---|---:|---:|"])
    for _, row in turnover.iterrows():
        lines.append("| " + " | ".join(fmt(row[key]) for key in ["split", "factor", "top_quantile_turnover", "observations"]) + " |")

    lines.extend(
        [
            "",
            "## Observations",
            "",
            "- These are descriptive factor diagnostics, not a strategy, portfolio construction rule, or investment recommendation.",
            "- Train, validation and test rows are reported separately; test results are not used to alter factors or parameters.",
            "- Annual IC and Rank IC are included so a full-period average does not hide year-to-year instability.",
            "",
            "## Limitations",
            "",
            "- The Qlib sample data ends on 2021-06-11 and is not current-market data.",
            "- This workflow does not validate complete 2026 A-share settlement, suspension, price-limit or fee rules.",
            "- The label timing follows Qlib's official expression; it is not an independent point-in-time or production-data validation.",
            "- No OOS strategy, walk-forward optimization, cost sensitivity, paper trading or live trading was performed.",
        ]
    )
    report_path = args.output_dir / "report.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"report={report_path}")


if __name__ == "__main__":
    main()
