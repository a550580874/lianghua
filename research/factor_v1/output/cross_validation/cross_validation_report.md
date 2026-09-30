# Factor Research Cross-Validation

## Purpose

This report cross-validates the existing `research/factor_v1` descriptive implementation against an independent Alphalens Reloaded implementation. It is not a factor selection, profitability or strategy test.

## External Oracle

- Oracle: Alphalens Reloaded 0.4.6 (`alphalens-reloaded`), isolated Python 3.12.12 environment.
- API used: `get_clean_factor_and_forward_returns`, `factor_information_coefficient`, `mean_return_by_quantile(demeaned=False)`, and `quantile_turnover`.
- The upstream package was not forked or patched.

## Timing Alignment

- The custom factor is known at signal date `t`; the adapter maps it to the next observed trading date `entry_date=t+1` without changing its value.
- Alphalens horizon H then measures `close(entry_date+H) / close(entry_date) - 1`, equal to `close(t+1+H) / close(t+1) - 1`.
- A trading-calendar mapping is used; calendar-day arithmetic is not used. Signals without a complete exit inside their own split are excluded.

## Rank IC

- Rows: 60; status counts: DATA_ALIGNMENT_DIFFERENCE=60.
- `DATA_ALIGNMENT_DIFFERENCE` means the custom and Alphalens effective samples differ (typically because Alphalens price-forward-return/dropna handling differs from the custom close-based sample). Values are retained for diagnosis; no tolerance was widened.
- No Pearson IC, coverage, IC t-stat, rank autocorrelation or factor-factor correlation comparison is claimed here: those have `NO_DIRECT_ORACLE` in scope.

## Quantile Returns

- Rows: 300; status counts: DATA_ALIGNMENT_DIFFERENCE=300.
- Alphalens raw quantile means use `demeaned=False` and `by_date=True` before aggregation. Differences are classified as DATA_ALIGNMENT_DIFFERENCE when effective rows are not identical; duplicate/tie and missing-data behavior is not silently normalized.

## Turnover

- Rows: 15; status counts: SEMANTIC_DIFFERENCE=15.
- Custom turnover is `1 - overlap(previous Q5, current Q5) / previous Q5 size`.
- Alphalens uses current names not in the previous quantile divided by current quantile size. Its `quantile_turnover` also requires a regular date frequency; for this observed China sample it could not be applied consistently, so rows are marked SEMANTIC_DIFFERENCE rather than FAIL.

## Findings

- The adapter produced 60 split/factor/horizon alignment records and preserved factor values while shifting only the timestamp convention.
- The independent oracle ran successfully for the cross-validation matrix; observed status differences are implementation/data-alignment findings, not factor quality judgments.

## Unsupported Comparisons

- Pearson IC, coverage, IC t-stat, rank autocorrelation and factor correlation: NO_DIRECT_ORACLE.

## Limitations

- Alphalens Reloaded 0.4.6 requires pandas <3 and has date-frequency assumptions that do not fully match this sample's irregular observed calendar.
- This is implementation cross-validation only. It is not profitability validation, portfolio construction, transaction-cost analysis, walk-forward research or live trading.
