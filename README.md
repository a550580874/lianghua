# Quant Framework PoC

> **Chinese documentation:** [README_ZH.md](README_ZH.md) — start here for a plain-language project overview, honest clone-to-run instructions, framework concepts, and known limitations.

## Scope and status

This directory is an independent, evidence-first evaluation of open-source quant frameworks. It does not modify or import code from the adjacent `a-share-quant` project.

Current gate: **AKQuant PoC human acceptance passed.** Qlib, RQAlpha and AKQuant have all completed their gated PoC acceptance runs.

| Qlib 0.9.7 | RQAlpha 6.4.0 | AKQuant 0.3.61 |
|---|---|---|
| **PASS** | **PASS** | **PASS** |

This is not a framework selection, ranking, investment recommendation, live-trading integration, or validation for use with real funds.

## Layout

```text
.
├── README.md
├── README_ZH.md                 # Chinese learning and usage guide
├── environment.md
├── configs/                   # Qlib workflow configuration
├── logs/                      # compact Qlib execution evidence
├── results/                   # framework evidence reports and usability-gap audit
├── scripts/                   # read-only verification helpers
├── qlib/                      # Qlib config, verifier and compact logs
├── rqalpha/output/            # compact RQAlpha run/report artifacts
└── akquant/output/            # compact AKQuant run/test artifacts
```

Virtual environments, downloaded market data, MLflow stores and cloned upstream
framework repositories are intentionally excluded from Git. Their pinned versions,
official URLs and reproduction commands are recorded in `environment.md` and the
framework reports under `results/`.

Creating the assigned Multica issue automatically triggered a second C2 run during the earlier Qlib phase. Both Qlib runs used the same official Alpha158/CSI300 workflow and produced matching metrics. The `qlib/output/` set and `results/qlib.md` are the canonical tracked Qlib evidence; the earlier root `logs/` set is also preserved. MLflow stores are intentionally excluded from Git. Qlib, RQAlpha and AKQuant subsequently passed their human acceptance gates. AKQuant work remains isolated from the other accepted environments.

An important usability boundary: a fresh clone can inspect the committed reports, logs and RQAlpha exports, but cannot immediately rerun any full PoC because virtual environments, downloaded data/bundles, upstream source checkouts and official example files are not committed. See [README_ZH.md](README_ZH.md) and [results/usability_gap.md](results/usability_gap.md) before attempting reproduction.

## Qlib acceptance reproduction

From `quant-framework-poc/`:

```bash
.venv/bin/python qlib/verify_data.py
```

Expected success indicators:

- log line `qlib successfully initialized`
- `qlib_version=0.9.7`
- calendar first/last dates
- `csi300_instrument_count=300`
- a small `$close`/`$volume` table

Then run the official Alpha158/CSI300 workflow:

```bash
cd qlib
MLFLOW_ALLOW_FILE_STORE=true ../.venv/bin/qrun workflow_config_local.yaml \
  --experiment_name qlib-poc-alpha158 \
  --uri_folder output/mlruns
```

Success means the process exits with code 0 and prints/saves:

- prediction rows
- IC, ICIR, Rank IC and Rank ICIR
- benchmark and excess-return analysis with/without cost
- `Portfolio analysis record ... has been saved`
- `Indicator analysis record ... has been saved`

Output locations:

- `qlib/output/data_smoke.log`
- `qlib/output/alpha158_workflow_retry.log`
- `qlib/output/mlruns/`
- detailed report: `results/qlib.md`

## RQAlpha acceptance reproduction

From `quant-framework-poc/rqalpha/`:

```bash
.venv/bin/rqalpha check-bundle -d data

.venv/bin/rqalpha run \
  -f source/rqalpha/examples/buy_and_hold.py \
  -d data/bundle \
  -s 2016-06-01 \
  -e 2016-12-01 \
  --account stock 100000 \
  --benchmark 000300.XSHG \
  -o output/manual_acceptance.pkl
```

Expected success indicators:

- bundle check prints `good bundle's day bar`;
- the run logs `INFO: user_log: init` and exits with code 0;
- `output/manual_acceptance.pkl` exists;
- the unchanged official example creates one BUY trade for 9,500 shares of `000001.XSHE` on 2016-06-01 at 10.48, with commission and transaction cost of 79.648;
- the 123-period portfolio ends at 111,253.852 with total return 0.11253852.

To generate readable official exports:

```bash
mkdir -p output/manual_report
.venv/bin/rqalpha report output/manual_acceptance.pkl output/manual_report
```

Expect `trades.csv`, `portfolio.csv`, `stock_account.csv`, `stock_positions.csv`, `positions_weight.csv`, and `summary.xlsx`. RQAlpha 6.4.0 does not export a standalone orders table in its final result; the trade record retains its `order_id`. Detailed evidence is in `results/rqalpha.md`.

## AKQuant acceptance reproduction

See `results/akquant.md` for the copy-ready command block, exact expected output and PASS/FAIL/BLOCKED criteria. The acceptance run uses the unchanged `akquant/source/examples/01_quickstart.py` and writes only `akquant/output/manual_acceptance.log`; the official example does not generate a report or plot.

Human acceptance passed with exit code 0. The reproduced run matched the Agent baseline: two bars, three filled BUY orders, three open positions, CNY 15 total commission, end market value 4,870,549.04 and total return -2.589019%. This confirms reproducibility of the official quickstart only; the A-share-rule, fee, ETF subtype, suspension and remote-data boundaries documented in `results/akquant.md` remain unchanged.

## Objective comparison table

No total score, rank, or winner is assigned. “Not established” or “not tested” means that capability was outside the evidence collected by the corresponding PoC; it does not mean a framework-wide absence.

| Framework | Installability | Maintenance | A-share support | ETF support | PIT | Factor research | ML | Portfolio | Backtest | Execution | T+1 | Limit handling | Suspension | Cost model | Transfer fee | Documentation | Complexity |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Qlib 0.9.7 | PASS on macOS arm64/Python 3.12 after installing `libomp` | Latest evaluated stable tag is v0.9.7 (2025-08-15); main/release cadence not scored | CN region + CSI300 official workflow ran successfully | Not established; no ETF-specific official run in this phase | PIT provider/source exists; not exercised by this run | Alpha158 official handler and workflow ran unchanged | Official LightGBM workflow ran | `TopkDropoutStrategy` + portfolio analysis artifacts | Official daily backtest ran | Simulator/exchange and separate RL order-execution modules exist; only daily simulator tested | Docs encode Alpha158 T+1→T+2 label rationale; enforcement not established | Fixed `limit_threshold: 0.095` tested; full board/ST/date rules not established | Docs map suspended-stock fields to NaN; dedicated scenario not tested | Configurable open/close/min costs and with-cost metrics; China tax schedule not independently validated | Not established in Qlib phase | Extensive official README/docs/examples; compatibility warnings encountered | Full workflow is config-driven but dependency/data/MLflow setup is non-trivial |
| RQAlpha 6.4.0 | PASS on macOS arm64/Python 3.12; official bundle/example ran | `release/6.4.0`; evaluated commit dated 2026-09-07 | Official A-share daily bundle and unchanged `000001.XSHE` example ran | First-class ETF type, bundle records and separate ETF fee model; no ETF trade run | Free bundle did not establish PIT; separate RQData advertises PIT financial data, not tested | Trading/data APIs present; no official factor workflow tested | No ML workflow tested | Stock account, positions and portfolio outputs generated | Official daily event-driven backtest ran for 123 periods | Bar/minute/tick modes documented; current-bar daily execution exercised | Default stock T+1 and `market_tplus` enforcement in source; rejection not run | Matcher consumes bundle `limit_up`/`limit_down`; exact thresholds data-dependent | Suspension API/data/validator exist; rejection not run | Stock commission/minimum, sell-side stamp tax and ETF commission; example charged 79.648 | UNKNOWN: no explicit implementation/config/test; `other_fees=0` | Official install/tutorial/API/mod docs; tutorial result-key example appears stale | CLI/config/mod architecture; isolated installation straightforward after environment creation |
| AKQuant 0.3.61 | PASS on macOS arm64/Python 3.12 using official wheel; unchanged example ran | v0.3.61 / `b518acc`; current evaluated release | Stock/China-market models exist; official 3-symbol A-share example ran, but helper defaults are generic | `FUND` type and official ETF example exist; subtype rules are not automatic | Not established; remote AKShare history was used | Indicators/factors APIs exist; no factor workflow run | ML/WFO APIs exist; no ML example run | Multi-symbol portfolio and order outputs generated | Official two-day, three-symbol backtest ran | Default NextOpen plus named modes, tick/lot/volume checks | Supported when explicitly enabled; focused official tests passed | NOT FOUND for exchange daily limits; ordinary limit orders/tick checks are separate | Zero-volume/missing-slice rejection and focused tests present | Configurable commission/minimum and sell-side stamp tax; example uses zero rates + CNY 5 minimum | Explicit configurable model; helper/example default zero; current applicability not validated | Official docs/examples/source/tests; some generic claims exceed located implementation evidence | Rust/Python wheel installs cleanly; behavior is highly configuration-dependent |
