# Factor Research Workflow v3.1 — Exact Oracle Alignment

## Purpose

This run separates statistical-oracle comparison from forward-return construction. The existing factor v1/v2/v3 baselines were not modified.

## Exact statistical layer

Alphalens Reloaded 0.4.6 `utils.get_clean_factor` consumed the same `(date, instrument)`, factor values, and custom 1D/5D/10D/20D returns as the custom diagnostics. Daily rank-IC comparisons are recorded in `rank_ic_exact_comparison.csv` and summarized in `rank_ic_exact_summary.csv`: all 60 split × factor × horizon groups are `MATCH` at tolerance `1e-10`; no implementation bug was found.

Quantile assignments are recorded in `quantile_assignment_comparison.csv`. The bounded detail extract contains 1,000 rows per group and matched on all retained rows. Quantile-return daily comparisons are in `quantile_return_exact_comparison.csv`: 302,215 `MATCH` rows and 390 `SEMANTIC_DIFFERENCE` rows. The non-matching rows are attributable to quantile/tie semantics rather than forward-return alignment.

## Turnover definition

`turnover_definition_analysis.csv` compares `1-overlap/previous_size` with Alphalens' `1-overlap/current_size`. Of 15,239 rows, 10,892 are `EFFECTIVELY_EQUIVALENT` and 4,347 are `SEMANTIC_DIFFERENCE`; the latter are explained by differing denominators.

## Forward-return alignment layer

`forward_return_alignment.csv` and its summary compare custom returns with Alphalens `compute_forward_returns` after mapping signal date `t` to the next trading entry date. The `factor=ALL` label is intentional: this layer depends only on the price calendar, not factor identity. Differences are classified as `DATA_ALIGNMENT_DIFFERENCE`; no statistical result is reclassified as an implementation bug.

## Outputs and limits

The detailed comparison files are deterministic bounded detail extracts (the aggregate summaries use the complete input). This is an implementation cross-check, not a profitability test, factor selection exercise, portfolio backtest, or trading recommendation. Unsupported v2 diagnostics remain without an Alphalens oracle.
