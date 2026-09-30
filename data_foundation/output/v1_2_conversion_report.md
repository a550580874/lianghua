# Data Foundation v1.2 conversion report

Status: `PASS_QLIB_COMPATIBILITY` with `VOLUME_SEMANTICS_PARTIAL`.

- Runtime: existing project Qlib 0.9.7.
- Official source: `microsoft/qlib` tag `v0.9.7`, commit `da920b7f954f48ab1bb64117c976710de198373e`.
- `scripts/dump_bin.py dump_all` completed without modification.
- Intermediate input uses BaoStock raw flag 3, research adjusted flag 2, and factor = adjusted close / raw close.
- Binary output contains calendars, instruments, and features for `sh600000` and `sz000001`.
- `D.features`: PASS, non-empty 116×6 output for `$open,$high,$low,$close,$volume,$factor`.
- Alpha158: PASS, 116×158; `ROC20`, `STD20`, `MA20`, `VSTD20`, `CORR20` present with non-null warmup observations.
- Volume: raw BaoStock volume retained; volume-sensitive interpretation remains partial.
- 2020 overlap: not run.
