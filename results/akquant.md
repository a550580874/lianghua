## Version

- Installed package: `akquant==0.3.61`
- Official release: tag `v0.3.61`, commit `b518accbcbc40c25b727f54a9067b4c2d8a9a283`
- Evaluation date: 2026-09-20

## Repository

- Official repository: <https://github.com/akfamily/akquant>
- Evaluated release: <https://github.com/akfamily/akquant/tree/v0.3.61>
- Official documentation: <https://akquant.akfamily.xyz/>

The PyPI current release and the repository's current tag both resolved to 0.3.61 on the evaluation date. The source checkout is detached at that tag so later `main` changes do not silently alter this PoC.

## Python version and platform

AKQuant 0.3.61 declares Python `>=3.10` and classifiers for Python 3.10 through 3.14. Python 3.12.12 was selected as the stable interpreter already used for the isolated framework PoCs; the host default Python 3.14.3 was not assumed. The official installation guide lists macOS, Linux and Windows. PyPI supplied the native `akquant-0.3.61-cp310-abi3-macosx_11_0_arm64.whl`, and import/example execution passed on macOS 15.6.1 / Apple M4 / arm64. This proves this host/release combination, not a general hardware certification.

Evidence: <https://github.com/akfamily/akquant/blob/v0.3.61/pyproject.toml>, <https://github.com/akfamily/akquant/blob/v0.3.61/docs/en/start/installation.md>

## Installation

Dedicated environment:

```bash
uv venv --python /Users/ming-shen/.local/bin/python3.12 --seed akquant/.venv
akquant/.venv/bin/python -m pip install akquant==0.3.61 akshare
```

Result: PASS. `import akquant` reported 0.3.61. AKShare 1.18.96 was installed because the unchanged official quickstart imports it. No Rust toolchain was needed because the official arm64 wheel was available. The package snapshot is `akquant/output/requirements-freeze.txt`. Qlib, RQAlpha and `a-share-quant` environments were not modified.

## Official data and example

- Example: `akquant/source/examples/01_quickstart.py`
- Upstream: <https://github.com/akfamily/akquant/blob/v0.3.61/examples/01_quickstart.py>
- Source diff: empty.
- Data path: the example calls the AKShare `stock_zh_a_daily` API for `sh600000`, `sh600004` and `sh600006`; no AKQuant bundle is involved.
- Requested range in the official file: 2000-01-01 through 2026-12-31; the backtest itself filters 2025-01-01 through 2025-01-05.
- Observed bars: 2025-01-02 and 2025-01-03, two cross-sectional timestamps for each of three symbols.

AKShare is a remote public-data dependency used by the official example. This PoC does not describe it as exchange-official, real-time, point-in-time, or production-quality data. Reproduction requires network access and is exposed to upstream revisions/outages. No local bundle or immutable input snapshot is provided by this example.

## Example command

From `quant-framework-poc/akquant/`:

```bash
set -o pipefail
.venv/bin/python source/examples/01_quickstart.py 2>&1 | tee output/01_quickstart.log
```

## Run result

PASS, exit code 0. The unchanged official strategy ran all three symbols through AKQuant's engine.

| Item | Observed value |
|---|---:|
| Total bars | 2 |
| Execution count | 3 |
| Filled orders | 3 |
| Open positions | 3 |
| Initial market value | 5,000,000.00 |
| End market value | 4,870,549.04 |
| Total PnL | -129,450.96 |
| Total return | -2.589019% |
| Total commission | 15.00 |
| Stream events | 24 |

Orders were filled on the next bar: `600000` BUY 162,882 @ 10.12, `600004` BUY 176,470 @ 9.33, and `600006` BUY 221,774 @ 7.36. Each incurred the example's CNY 5 minimum commission. The example holds all three positions, so closed-trade count is zero; that is not a missing-trade error. Its manual total-return, annualized-return, drawdown, R² and standard-error checks matched the Rust result. These historical outputs are reproducibility evidence only, not a strategy recommendation.

Artifacts:

- `akquant/output/01_quickstart.log`: raw successful run.
- `akquant/output/version.log`: environment identity.
- `akquant/output/requirements-freeze.txt`: installed packages.
- `akquant/output/capability-tests.log`: selected official tests, 58 passed.

The official quickstart prints its result and orders but does not write a report, plot, pickle or CSV. None was fabricated for this PoC.

## A-share support

Status: **SUPPORTED AS CONFIGURABLE ENGINE BEHAVIOR; NOT AUTOMATIC CURRENT-RULE VALIDATION.**

- `AssetType.Stock`, `StockMatcher`, `ChinaStockConfig` and `Engine.use_china_market()` provide stock instruments, 0.01 tick validation, buy-side lot checks and a China market cost/T+1 model.
- The official quickstart fetched and ran three Shanghai A-share symbols.
- High-level `run_backtest` defaults are generic: `t_plus_one=False`, `lot_size` is not automatically forced to 100, and all fee rates default to zero. A caller must select/configure China behavior explicitly.

Evidence: <https://github.com/akfamily/akquant/blob/v0.3.61/src/market/stock.rs>, <https://github.com/akfamily/akquant/blob/v0.3.61/src/execution/stock.rs>, <https://github.com/akfamily/akquant/blob/v0.3.61/python/akquant/backtest/engine.py>

## ETF support

Status: **PARTIAL / CONFIGURABLE.**

- AKQuant models funds with `AssetType.Fund` / `InstrumentConfig(asset_type="FUND")`; the default fund tick is 0.001.
- The official repository contains `examples/59_akshare_etf_rotation.py`, which obtains ETF history with AKShare. It was inspected, not run, because this phase stops after the first successful official example.
- `FundConfig` implements commission, minimum commission, transfer fee and sellable-position delay, with no stamp tax in its calculation.
- `sellable_after_days` can express T+0 or T+1 per instrument. The enum/config does not automatically classify stock, bond, money, commodity or cross-border ETF rule variants, and no separate official subtype fee table was located.

Evidence: <https://github.com/akfamily/akquant/blob/v0.3.61/python/akquant/config.py>, <https://github.com/akfamily/akquant/blob/v0.3.61/src/market/fund.rs>, <https://github.com/akfamily/akquant/blob/v0.3.61/examples/59_akshare_etf_rotation.py>

## T+1

Status: **SUPPORTED WHEN ENABLED.**

`src/market/stock.rs::update_available_position` leaves a T+1 buy unavailable until the day-close release. `InstrumentConfig.sellable_after_days` accepts 0 or 1. The high-level helper's `t_plus_one` default is false; the low-level China stock/fund model defaults true, but `run_backtest` must explicitly enable/use it. Official `tests/test_t_plus_one.py` covers same-day lock, next-day unlock, oversell, no-position and same-cycle rejection. All five tests passed locally.

Evidence: <https://github.com/akfamily/akquant/blob/v0.3.61/tests/test_t_plus_one.py>, <https://github.com/akfamily/akquant/blob/v0.3.61/src/market/stock.rs>

## Limit up / down

Status: **NOT FOUND / NEEDS CURRENT-RULE VALIDATION.**

At v0.3.61, a repository-wide source/test search found no built-in `limit_up`/`limit_down` field, daily price-board calculation, ST/board/date rule table, or A-share daily-limit rejection path. `StockMatcher` validates tick alignment, lot size and ordinary limit/stop order matching; those are not daily涨跌停 rules. `tests/golden/gen_data.py` labels two synthetic bars “Limit Up/Down”, but the golden runner contains no dedicated assertion that orders are rejected because of an exchange daily limit. Generic documentation language about price-limit rejection is therefore insufficient to claim implementation. No patch was made.

## Suspension

Status: **SUPPORTED FOR ZERO-VOLUME / MISSING-SLICE SEMANTICS, WITH SCOPE LIMIT.**

The pipeline treats a bar with `volume <= 0` as non-tradable. A next-bar order whose slice is zero-volume becomes `Rejected` with a suspension/zero-volume reason; a wholly absent symbol gets a distinct missing-data reason. The two dedicated cases in `tests/test_suspension_zero_volume_gtc_terminal.py` passed. This is not an exchange suspension calendar or an independent validation of all partial-day cases.

Evidence: <https://github.com/akfamily/akquant/blob/v0.3.61/src/pipeline/stages/data.rs>, <https://github.com/akfamily/akquant/blob/v0.3.61/tests/test_suspension_zero_volume_gtc_terminal.py>

## Commission

Status: **SUPPORTED AND USER-CONFIGURABLE.**

Commission policies support percent, fixed and per-unit forms plus minimum commission. `StockConfig` low-level defaults are 0.0003 with CNY 5 minimum, while `StrategyConfig` / `run_backtest` defaults are zero and override the engine when the helper is used. Therefore callers must not assume a current broker tariff. The official quickstart explicitly sets `commission_rate=0` and `min_commission=5`, producing CNY 5 on each fill.

Evidence: <https://github.com/akfamily/akquant/blob/v0.3.61/src/market/stock.rs>, <https://github.com/akfamily/akquant/blob/v0.3.61/python/akquant/config.py>, <https://github.com/akfamily/akquant/blob/v0.3.61/tests/test_cost_config_consolidation.py>

## Stamp tax

Status: **SUPPORTED, SELL SIDE, NOT DATE-AWARE.**

`src/market/stock.rs::calculate_commission` adds stamp tax only for sells. Low-level `StockConfig` defaults to 0.0005, while high-level `run_backtest` defaults to 0.0 and passes the caller's value into the model. No effective-date schedule was located. This must be explicitly validated/configured for 2026 rather than inferred from either default.

## Transfer fee

Status: **SUPPORTED EXPLICITLY, NOT DATE/MARKET-AWARE.**

Stock and fund calculations add `transaction_value * transfer_fee` on both sides. The low-level China stock/fund default is 0.00001; the high-level helper default is 0.0. The official quickstart explicitly uses 0.0. No exchange/date applicability schedule was located, so correct 2026 scope and rate remain `NEEDS CURRENT-RULE VALIDATION`.

Evidence: <https://github.com/akfamily/akquant/blob/v0.3.61/src/market/stock.rs>, <https://github.com/akfamily/akquant/blob/v0.3.61/src/market/fund.rs>

## Slippage

Status: **SUPPORTED.**

Rust implements zero (default), fixed-amount and percentage models. The Python configuration also accepts `ticks`, resolving it to a fixed amount from instrument tick size. Global, per-instrument, per-strategy and order-level policy surfaces exist; order-level parsing supports percent/fixed. No market-impact or queue model is implied.

Evidence: <https://github.com/akfamily/akquant/blob/v0.3.61/src/execution/slippage.rs>, <https://github.com/akfamily/akquant/blob/v0.3.61/python/akquant/backtest/engine.py>

## Walk-forward

Status: **IMPLEMENTED; NOT EXERCISED AS A STRATEGY RUN IN THIS STOP-GATED PHASE.**

`python/akquant/optimize.py::run_walk_forward` constructs rolling train/test windows, runs grid search in-sample and backtests the selected parameters out-of-sample. Official documentation describes the API. `tests/test_walk_forward_kwargs.py` passed, proving grid-only arguments do not leak into the out-of-sample backtest; it is not a full empirical WFO validation.

Evidence: <https://github.com/akfamily/akquant/blob/v0.3.61/python/akquant/optimize.py>, <https://github.com/akfamily/akquant/blob/v0.3.61/docs/en/guide/optimization.md>, <https://github.com/akfamily/akquant/blob/v0.3.61/tests/test_walk_forward_kwargs.py>

## Multi-symbol backtest

Status: **SUPPORTED AND EXERCISED.**

`run_backtest` accepts `Dict[str, DataFrame]` and symbol lists. The official quickstart ran three symbols and generated three fills. The selected official cross-section/multi-symbol suite also passed, including ordering invariance, incomplete timestamps, rotation, sell-before-buy sizing and callback/result consistency.

Evidence: <https://github.com/akfamily/akquant/blob/v0.3.61/tests/test_multisymbol_cross_section_consistency.py>

## Risk and execution policy

Status: **SUPPORTED, CONFIGURATION-DEPENDENT.**

- `RiskConfig` includes cash checks, order/position value and size limits, restricted symbols, concentration, drawdown, daily loss, equity stop, margin/short and forced-liquidation controls.
- Default fill policy is `NextOpen`; named alternatives are `NextClose`, `NextAverage`, `NextHighLowMid` and `CurrentClose`.
- Volume participation defaults to 25%; stock matcher enforces buy lot size and tick alignment.
- Selected official risk tests passed, including drawdown/daily-loss/stop-loss rejection and cash/margin behavior.

Evidence: <https://github.com/akfamily/akquant/blob/v0.3.61/python/akquant/config.py>, <https://github.com/akfamily/akquant/blob/v0.3.61/python/akquant/backtest/fill_mode.py>, <https://github.com/akfamily/akquant/blob/v0.3.61/tests/test_account_risk_rules.py>

## Rejected-order behavior

Status: **SUPPORTED WITH OBSERVABLE REASONS.**

Validation/risk failures produce `OrderStatus.Rejected`, populate `reject_reason`, emit an execution report, and trigger class-style `on_order` plus `on_reject` once. T+1, lot/tick, cash/risk and suspension paths have official tests. The result exposes `orders_df`, including rejected rows/reasons. The official quickstart generated no rejection. Daily price-limit rejection remains unavailable as described above.

Evidence: <https://github.com/akfamily/akquant/blob/v0.3.61/src/execution/validation.rs>, <https://github.com/akfamily/akquant/blob/v0.3.61/docs/en/guide/strategy.md>, <https://github.com/akfamily/akquant/blob/v0.3.61/tests/test_t_plus_one.py>

## Official test evidence

The following unchanged official test files were run against the installed 0.3.61 wheel: 58 tests passed, with five strategy-parameter migration warnings and no failures.

| Capability | Official evidence | Local result |
|---|---|---|
| T+1 / rejection | `tests/test_t_plus_one.py` (5 cases) | PASS |
| Suspension | `tests/test_suspension_zero_volume_gtc_terminal.py` (2 cases) | PASS |
| Tick validation | `tests/test_stock_tick_validation.py` (3 cases) | PASS; not daily price limits |
| Cost configuration | `tests/test_cost_config_consolidation.py` (7 cases) | PASS; configuration persistence, not current rates |
| Walk-forward plumbing | `tests/test_walk_forward_kwargs.py` | PASS |
| Multi-symbol | `tests/test_multisymbol_cross_section_consistency.py` (18 cases) | PASS |
| Account risk | `tests/test_account_risk_rules.py` (18 cases) | PASS |
| Order API return values | `tests/test_order_api_return_values.py` (4 cases) | PASS |
| Daily price limit | No dedicated implementation/test located | UNKNOWN / NOT FOUND |
| ETF subtype fees/rules | No dedicated stock/bond/money ETF matrix test located | UNKNOWN |

## Warnings and known limitations

- The official example depends on a live remote AKShare endpoint and has no immutable data bundle.
- The example explicitly disables percentage commission, stamp tax and transfer fee, uses `lot_size=1`, and leaves `t_plus_one` at its false default. It proves engine/example reproducibility, not A-share rule correctness.
- High-level defaults do not automatically equal low-level `ChinaMarket` defaults; neither should be assumed to match 2026 fees.
- A-share daily price-limit enforcement was not found.
- ETF subtypes and their different T+0/T+1/fee rules are not automatically classified.
- Suspension support is based on zero-volume/missing slices, not an authoritative suspension calendar.
- Five selected-test warnings report older test strategy classes using constructor parameters instead of 0.3.x inline parameter declarations; tests still passed.
- The example's two-day period makes several annualized metrics statistically uninformative.

## Issues encountered

The first pip invocation was interrupted after downloads before installation completed. Re-running the same official installation command completed successfully; no source or package patch was used. No example failure occurred.

## Manual modifications

- No AKQuant source, official example, strategy logic, matcher, risk rule or cost implementation was modified.
- No custom strategy, backtester, data provider or A-share/ETF rule was created.
- Only the isolated environment, source checkout, logs and factual documentation were added.
- Qlib, RQAlpha and `a-share-quant` were not modified by AKQuant work.

## Blocked / unknown items

- `NOT FOUND / NEEDS CURRENT-RULE VALIDATION`: built-in A-share daily limit-up/down rules and rejection.
- `UNKNOWN / NEEDS CURRENT-RULE VALIDATION`: automatic stock/bond/money/cross-border ETF rule classification.
- `NEEDS CURRENT-RULE VALIDATION`: all default/example commission, stamp-tax and transfer-fee rates for 2026.
- `NOT TESTED`: a full walk-forward optimization run; only official API/source and focused test evidence were collected.
- `NOT TESTED`: live trading, QMT/PTrade, real accounts, real holdings and real funds; all are out of scope.

## 人工验收命令

```bash
cd '/Users/ming-shen/Desktop/金融/2026-09-13/files-pasted-by-the-user-a/outputs/quant-framework-poc/akquant'

.venv/bin/python --version
.venv/bin/python -c 'import akquant, akshare; print("akquant", akquant.__version__); print("akshare", akshare.__version__)'

git -C source rev-parse HEAD
git -C source describe --tags --exact-match
git -C source diff --exit-code -- examples/01_quickstart.py

set -o pipefail
.venv/bin/python source/examples/01_quickstart.py 2>&1 | tee output/manual_acceptance.log
akquant_exit_code=$?
echo "akquant_exit_code=$akquant_exit_code"
test "$akquant_exit_code" -eq 0
```

## 预期输出

- Python 3.12.12, AKQuant 0.3.61, AKShare 1.18.96.
- Commit `b518accbcbc40c25b727f54a9067b4c2d8a9a283`, tag `v0.3.61`, and empty example diff.
- Log begins with `Running backtest via run_backtest()` and prints `BacktestResult`.
- Date range 2025-01-02 through 2025-01-03, `total_bars=2`, `execution_count=3`, `open_position_count=3`.
- Three `filled` BUY orders for `600000`, `600004`, `600006`; CNY 5 commission each.
- `end_market_value=4870549.04`, `total_return_pct=-2.589019` (display rounding may vary), `total_commission=15.0`, `stream_events=24`.
- Manual/Rust return, annualized return, drawdown, R² and standard error agree; two-day volatility may print `nan` in the manual pandas calculation while Rust reports 0.
- `akquant_exit_code=0`.

Because the remote historical-data endpoint can revise or fail, network/data errors are `BLOCKED`, not a reason to patch the framework. A material change in dates, symbols, order count/status, fills or portfolio result is `FAIL` pending investigation; display-only float rounding is acceptable.

## 结果位置与成功判定

- Manual log: `output/manual_acceptance.log`.
- Baseline run log: `output/01_quickstart.log`.
- Evidence report: `../results/akquant.md`.
- Official source/example: `source/examples/01_quickstart.py`.
- Report/plot/data output: none; the official quickstart does not create these artifacts.

`PASS` requires correct versions/commit/tag, an empty official-example diff, a complete exit-0 run, three filled orders and the expected portfolio summary. `FAIL` means the engine runs but outputs materially differ or an order is rejected/errored. `BLOCKED` means installation/import or the remote official-example data dependency prevents the run; retain the complete log and do not patch core code.

## 人工验收记录

状态：**PASS（人工验收已完成）**。

人工复现与 Agent 基线一致：官方 quickstart 完整运行，最终 `akquant_exit_code=0`；观察到 `total_bars=2`、`execution_count=3`、`open_position_count=3` 和 `stream_events=24`。

| Symbol | Side | Quantity | Fill price | Commission | Status |
|---|---|---:|---:|---:|---|
| `600000` | BUY | 162,882 | 10.12 | 5.00 | `filled` |
| `600004` | BUY | 176,470 | 9.33 | 5.00 | `filled` |
| `600006` | BUY | 221,774 | 7.36 | 5.00 | `filled` |

人工验收组合结果：`initial_market_value=5000000.0`、`end_market_value=4870549.04`、`total_pnl=-129450.96`、`total_return_pct=-2.589019`、`total_commission=15.0`。Manual 与 Rust 的 total return、annualized return、max drawdown、R²、standard error 一致；两日样本下 Volatility 的 Manual=`nan`、Rust=`0` 为本次已知且接受的差异。

该 PASS 仅确认本报告所述安装、官方 quickstart 和输出可复现，不扩大能力结论：quickstart 不是完整 A 股规则验收，未启用 T+1，示例税费不代表 2026 实际费率；A 股日涨跌停仍为 `NOT FOUND / NEEDS CURRENT-RULE VALIDATION`，ETF 子类型规则不自动分类，停牌主要是 zero-volume / missing-slice 语义，且 AKShare 仍是远程公共数据依赖。
