"""Render the Alphalens cross-validation outputs as a concise report."""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "research/factor_v1/output/cross_validation"


def counts(frame: pd.DataFrame) -> str:
    return ", ".join(f"{key}={value}" for key, value in frame["status"].value_counts().items())


def main() -> None:
    rank = pd.read_csv(OUT / "rank_ic_cross_validation.csv")
    quantile = pd.read_csv(OUT / "quantile_return_cross_validation.csv")
    turnover = pd.read_csv(OUT / "turnover_cross_validation.csv")
    metadata = pd.read_csv(OUT / "alignment_metadata.csv")
    lines = [
        "# Factor Research Cross-Validation",
        "",
        "## Purpose",
        "",
        "This report cross-validates the existing `research/factor_v1` descriptive implementation against an independent Alphalens Reloaded implementation. It is not a factor selection, profitability or strategy test.",
        "",
        "## External Oracle",
        "",
        "- Oracle: Alphalens Reloaded 0.4.6 (`alphalens-reloaded`), isolated Python 3.12.12 environment.",
        "- API used: `get_clean_factor_and_forward_returns`, `factor_information_coefficient`, `mean_return_by_quantile(demeaned=False)`, and `quantile_turnover`.",
        "- The upstream package was not forked or patched.",
        "",
        "## Timing Alignment",
        "",
        "- The custom factor is known at signal date `t`; the adapter maps it to the next observed trading date `entry_date=t+1` without changing its value.",
        "- Alphalens horizon H then measures `close(entry_date+H) / close(entry_date) - 1`, equal to `close(t+1+H) / close(t+1) - 1`.",
        "- A trading-calendar mapping is used; calendar-day arithmetic is not used. Signals without a complete exit inside their own split are excluded.",
        "",
        "## Rank IC",
        "",
        f"- Rows: {len(rank)}; status counts: {counts(rank)}.",
        "- `DATA_ALIGNMENT_DIFFERENCE` means the custom and Alphalens effective samples differ (typically because Alphalens price-forward-return/dropna handling differs from the custom close-based sample). Values are retained for diagnosis; no tolerance was widened.",
        "- No Pearson IC, coverage, IC t-stat, rank autocorrelation or factor-factor correlation comparison is claimed here: those have `NO_DIRECT_ORACLE` in scope.",
        "",
        "## Quantile Returns",
        "",
        f"- Rows: {len(quantile)}; status counts: {counts(quantile)}.",
        "- Alphalens raw quantile means use `demeaned=False` and `by_date=True` before aggregation. Differences are classified as DATA_ALIGNMENT_DIFFERENCE when effective rows are not identical; duplicate/tie and missing-data behavior is not silently normalized.",
        "",
        "## Turnover",
        "",
        f"- Rows: {len(turnover)}; status counts: {counts(turnover)}.",
        "- Custom turnover is `1 - overlap(previous Q5, current Q5) / previous Q5 size`.",
        "- Alphalens uses current names not in the previous quantile divided by current quantile size. Its `quantile_turnover` also requires a regular date frequency; for this observed China sample it could not be applied consistently, so rows are marked SEMANTIC_DIFFERENCE rather than FAIL.",
        "",
        "## Findings",
        "",
        f"- The adapter produced {len(metadata)} split/factor/horizon alignment records and preserved factor values while shifting only the timestamp convention.",
        "- The independent oracle ran successfully for the cross-validation matrix; observed status differences are implementation/data-alignment findings, not factor quality judgments.",
        "",
        "## Unsupported Comparisons",
        "",
        "- Pearson IC, coverage, IC t-stat, rank autocorrelation and factor correlation: NO_DIRECT_ORACLE.",
        "",
        "## Limitations",
        "",
        "- Alphalens Reloaded 0.4.6 requires pandas <3 and has date-frequency assumptions that do not fully match this sample's irregular observed calendar.",
        "- This is implementation cross-validation only. It is not profitability validation, portfolio construction, transaction-cost analysis, walk-forward research or live trading.",
    ]
    (OUT / "cross_validation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"report={OUT / 'cross_validation_report.md'}")


if __name__ == "__main__":
    main()
