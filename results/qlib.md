## Version

- Installed package: `pyqlib==0.9.7`
- Source/example checkout: tag `v0.9.7`, commit `da920b7f954f48ab1bb64117c976710de198373e`
- Evaluation date: 2026-09-18

## Repository

- Official repository: <https://github.com/microsoft/qlib>
- Checked-out release: <https://github.com/microsoft/qlib/tree/v0.9.7>

## Python version

Python 3.12.12, selected because Qlib officially lists Python 3.8–3.12 and the host default Python 3.14.3 is not listed as supported.

## Install command

```bash
uv venv --python /Users/ming-shen/.local/bin/python3.12 .venv
uv pip install --python .venv/bin/python pyqlib==0.9.7
brew install libomp
```

`libomp` is the Apple Silicon LightGBM prerequisite explicitly called out by Qlib's official README.

## Install result

PASS.

- `import qlib` succeeded and reported `0.9.7`.
- `import lightgbm` initially failed because `libomp.dylib` was absent.
- After the documented `brew install libomp`, `import lightgbm` succeeded and reported `4.7.0`.

## Official example source

- Official workflow: `qlib-source/examples/benchmarks/LightGBM/workflow_config_lightgbm_Alpha158.yaml`
- Upstream source: <https://github.com/microsoft/qlib/blob/v0.9.7/examples/benchmarks/LightGBM/workflow_config_lightgbm_Alpha158.yaml>
- CLI implementation: <https://github.com/microsoft/qlib/blob/v0.9.7/qlib/cli/run.py>

The official configuration was used as a `BASE_CONFIG_PATH`. No factor, Alpha158 definition, model, strategy, fee parameter, universe, benchmark, or date range was changed. The local overlay changes only `qlib_init.provider_uri`.

## Data source

Command used from Qlib's official CLI:

```bash
.venv/bin/python -m qlib.cli.data qlib_data \
  --name qlib_data_simple \
  --target_dir qlib/data/cn_data \
  --interval 1d \
  --region cn
```

Important provenance qualification:

- Qlib's current official README says the Microsoft-hosted official dataset is temporarily disabled.
- The installed Qlib 0.9.7 downloader fetched `qlib_data_simple_cn_1d_0.9.zip` from the community-hosted `SunsetWolf/qlib_dataset` release endpoint.
- The downloader itself warns that example data was collected from Yahoo Finance and may be imperfect.
- Therefore this is an official Qlib CLI/sample-data path, but the dataset host and underlying market data are not Microsoft-owned official exchange data.

Observed data:

- Frequency: daily
- Calendar: 2005-01-04 through 2021-06-11
- Smoke-test universe: CSI300, 300 instruments on 2021-06-11
- Local size after extraction: approximately 145 MiB

Official evidence:

- <https://github.com/microsoft/qlib/blob/main/README.md#data-preparation>
- <https://github.com/microsoft/qlib/blob/v0.9.7/scripts/README.md>
- <https://github.com/microsoft/qlib/blob/v0.9.7/qlib/tests/data.py>

## Example command

Data initialization/read smoke test:

```bash
.venv/bin/python qlib/verify_data.py
```

Official Alpha158/CSI300 workflow:

```bash
cd qlib
MLFLOW_ALLOW_FILE_STORE=true ../.venv/bin/qrun workflow_config_local.yaml \
  --experiment_name qlib-poc-alpha158 \
  --uri_folder output/mlruns
```

## Run result

PASS after one documented compatibility retry.

- `qlib.init`: PASS
- Daily calendar read: PASS
- `$close` and `$volume` read for a trading day: PASS
- Official LightGBM + Alpha158 + CSI300 workflow: PASS
- Full official benchmark configuration was run; this was not a reduced smoke configuration.
- Wall-clock runtime for the successful workflow: 32.04 seconds
- Peak memory footprint reported by `/usr/bin/time`: approximately 2.57 GiB

Workflow facts from the official configuration:

| Item | Value |
|---|---|
| Universe | CSI300 |
| Benchmark | SH000300 |
| Handler | Alpha158, unchanged |
| Model | LightGBM `LGBModel` |
| Strategy | `TopkDropoutStrategy`, topk 50, n_drop 5 |
| Data span | 2008-01-01 to 2020-08-01 |
| Train | 2008-01-01 to 2014-12-31 |
| Validation | 2015-01-01 to 2016-12-31 |
| Test/backtest | 2017-01-01 to 2020-08-01 |
| Account | 100,000,000 |
| Deal price | close |
| Limit threshold | 0.095 |
| Open cost | 0.0005 |
| Close cost | 0.0015 |
| Minimum cost | 5 |

## Output

Signal metrics:

| Metric | Value |
|---|---:|
| IC | 0.0499900678 |
| ICIR | 0.4164238169 |
| Rank IC | 0.0522899578 |
| Rank ICIR | 0.4504209124 |

Portfolio analysis:

| Series | Annualized return | Information ratio | Max drawdown |
|---|---:|---:|---:|
| Benchmark return | 0.113561 | 0.598699 | -0.370479 |
| Excess return, no cost | 0.148390 | 1.758186 | -0.084029 |
| Excess return, with cost | 0.102262 | 1.212060 | -0.104339 |

Artifacts:

- Successful raw log: `qlib/output/alpha158_workflow_retry.log`
- Preserved first-failure log: `qlib/output/alpha158_workflow.log`
- Data smoke log: `qlib/output/data_smoke.log`
- MLflow run: `qlib/output/mlruns/487615195700432407/dbc4118211ac4e0ea64938c76db087f4/`
- Predictions: `artifacts/pred.pkl`
- IC/Rank IC series: `artifacts/sig_analysis/`
- Portfolio report, positions, indicators and analysis: `artifacts/portfolio_analysis/`

These figures reproduce one local run of sample data and are not investment advice or a product benchmark.

## Warnings

- The Qlib downloader warns that Yahoo Finance-derived example data may be imperfect.
- The sample contains missing `$close` values; exchange construction emitted two NaN warnings.
- Qlib reported `common_infra` not set on `SimulatorExecutor`.
- NumPy emitted `Mean of empty slice` during portfolio analysis.
- Gym emitted its upstream unmaintained/NumPy 2.0 warning.
- Optional CatBoost, XGBoost and PyTorch models were unavailable and skipped; they are not used by this LightGBM workflow.
- The PoC working directory is not a Git repository, so Qlib's recorder could not capture `git diff`/`git status`.
- MLflow emitted repeated assistant hint messages; these did not affect results.

## 人工验收记录

人工验收于 2026-09-18 通过：Qlib 0.9.7 初始化、CSI300 数据读取，以及官方 Alpha158 + LightGBM workflow 均由用户复现成功；prediction、IC、Rank IC、portfolio backtest 与 transaction-cost analysis 均成功生成。871 个 backtest period 完整执行，用户人工运行结果与 Agent 运行结果一致。

以下仅作为验收观察记录，不对 Qlib 做修复或核心代码修改：

1. 当前 PoC 目录不是 Git repository，因此 Qlib Recorder 无法记录 `git diff` / `git status`。
2. CatBoost、XGBoost、PyTorch 是 optional dependency warning，不影响本次 LightGBM PoC。
3. Sample data 存在 `$close` NaN，backtest 中出现 `Mean of empty slice` warning。
4. 当前数据 calendar 截止 2021-06-11，因此本次收益指标不得解释为当前可交易策略表现。

## Known limitations discovered

- The official Microsoft dataset is currently disabled; reproducibility depends on a community-hosted snapshot.
- The simple dataset ends on 2021-06-11 and is not suitable for current-market evaluation.
- This phase did not validate data correctness against an independent A-share source.
- ETF behavior was not demonstrated by official data or example in this phase.
- PIT infrastructure exists in source, but this example did not use or validate PIT fundamentals.
- The example's 9.5% price-limit threshold is a single fixed threshold and does not by itself prove complete board/ST/date-specific A-share limit handling.
- Suspension data are represented by NaNs, but no dedicated suspension scenario was separately validated.
- A-share settlement/T+1 enforcement was not established by this example. Official docs explain the Alpha158 label's T+1-to-T+2 timing rationale; that is not equivalent to validating portfolio-level sell restrictions.
- Cost fields are configurable generic open/close/minimum costs, not a proof of a complete China commission/stamp-tax schedule.

## A-share capability evidence

- Official CN region and CSI300 sample/workflow: <https://github.com/microsoft/qlib/blob/v0.9.7/examples/benchmarks/LightGBM/workflow_config_lightgbm_Alpha158.yaml>
- Official data documentation states suspended-stock OHLCV/money/factor values are set to NaN: <https://github.com/microsoft/qlib/blob/v0.9.7/docs/component/data.rst>
- The same document explains Alpha158's China-stock label timing from T+1 to T+2.
- Local run proved the CSI300 workflow can execute on the provided CN sample; it did not prove all exchange rules.

## ETF capability evidence

NOT ESTABLISHED in this phase. Qlib's instrument abstraction may represent securities generally, but no official ETF-specific sample, rule model, or successful ETF run was identified or tested. No recommendation is inferred.

## Execution-model evidence

- The official workflow uses `TopkDropoutStrategy`, `SimulatorExecutor`, an exchange with `limit_threshold`, `deal_price`, `open_cost`, `close_cost`, and `min_cost`, and produces cost-aware portfolio reports.
- Backtest source: <https://github.com/microsoft/qlib/tree/v0.9.7/qlib/backtest>
- Workflow documentation: <https://github.com/microsoft/qlib/blob/v0.9.7/docs/component/workflow.rst>
- RL/order-execution documentation exists, but was not run in this phase: <https://github.com/microsoft/qlib/tree/v0.9.7/docs/component/rl>

## Issues encountered

1. LightGBM import failed on Apple Silicon due to missing `libomp.dylib`; resolved exactly as documented with `brew install libomp`.
2. The first custom data smoke harness lacked a macOS multiprocessing main guard. The harness—not Qlib—was corrected with `if __name__ == "__main__"`; the data read then passed.
3. The first official workflow launch failed because installed MLflow 3.16.1 rejects filesystem tracking by default. The exception explicitly instructed setting `MLFLOW_ALLOW_FILE_STORE=true`; the retry with that compatibility flag passed.
4. Creating the assigned Multica issue automatically triggered a parallel C2 issue run. It independently completed the same Qlib workflow (reported runtime 37 seconds and identical metrics) and created the preserved root-level `configs/`, `data/`, `logs/`, `mlruns/`, `scripts/`, and `requirements.txt` artifacts. The chat run's canonical artifacts are under `qlib/output/`. Neither run entered RQAlpha or AKQuant.

## Any manual modifications

- No Qlib package source, Alpha158 definition, official example core logic, model, strategy, or backtester was modified.
- `qlib/workflow_config_local.yaml` is an officially supported `BASE_CONFIG_PATH` overlay that changes only the local `provider_uri`.
- `MLFLOW_ALLOW_FILE_STORE=true` was set for the successful run per MLflow's own exception message.
- `qlib/verify_data.py` is a minimal initialization/read test harness, not a strategy or backtester; it was updated once to add the standard macOS multiprocessing main guard.
- Homebrew `libomp` 23.1.1 was installed.
