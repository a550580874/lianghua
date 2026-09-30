# Factor Research Workflow v4

This stage builds a full, snapshot-based Alpha158 panel without factor selection, model training, portfolio construction, or backtesting. The intended window is 2018-01-01..2024-03-31 with BaoStock raw flag 3 and research-adjusted flag 2. Because BaoStock exposes snapshots rather than verified effective intervals, the universe is named `SNAPSHOT_BASED_CSI300_RESEARCH_UNIVERSE`.

Run `build_dataset.py`, then `extract_alpha158.py` with the existing Qlib 0.9.7 environment. Large cache/parquet/bin files are gitignored.
