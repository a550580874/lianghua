## Version

- Installed package: `rqalpha==6.4.0`
- Official source: tag `release/6.4.0`, commit `a5fb4e43879c381e61131399dcc094d495c7080a` (2026-09-07)
- Initial execution: 2026-09-18; evidence-completeness update: 2026-09-19

## Repository

- Official repository: <https://github.com/ricequant/rqalpha>
- Evaluated release: <https://github.com/ricequant/rqalpha/tree/release/6.4.0>

## Python version

Python 3.12.12 in the dedicated `rqalpha/.venv`. RQAlpha 6.4.0 declares Python `>=3.8` and classifiers for 3.8 through 3.14. Python 3.12 was selected as the stable, already available interpreter instead of blindly using the host default Python 3.14.3.

The package classifier is `Operating System :: OS Independent`, and the official installation guide contains macOS-specific guidance. Neither source claims a dedicated Apple Silicon/arm64 certification matrix. On this host, installation, import, bundle access, the unchanged official example, and report export all passed on macOS 15.6.1 / Apple M4 / arm64; that is empirical compatibility evidence, not a broader vendor support guarantee.

Key declared dependencies include Requests, version-conditional NumPy (NumPy >=2 for Python >=3.12), pandas >=1.0.5 and <3, Logbook, Click, rqrisk, h5py/hdf5plugin, Matplotlib, openpyxl, MethodTools, FileLock, and typing-extensions.

Evidence: <https://github.com/ricequant/rqalpha/blob/release/6.4.0/pyproject.toml>, <https://github.com/ricequant/rqalpha/blob/release/6.4.0/docs/source/intro/install.rst>

## Install command

```bash
uv venv --python /Users/ming-shen/.local/bin/python3.12 --clear --seed rqalpha/.venv
rqalpha/.venv/bin/python -m pip install rqalpha==6.4.0
```

## Install result

PASS. `import rqalpha` and `rqalpha version` both reported 6.4.0. The complete package snapshot is `rqalpha/output/requirements-freeze.txt`. No package was installed in `a-share-quant/.venv`.

## 人工验收记录

人工验收于 2026-09-20 完成并通过：

- Python 3.12.12；RQAlpha 6.4.0。
- 官方仓库 commit `a5fb4e43879c381e61131399dcc094d495c7080a`、tag `release/6.4.0`。
- 官方 `buy_and_hold.py` 的 `git diff` 为空，交易逻辑未修改。
- `rqalpha check-bundle` 输出 `good bundle's day bar`。
- 官方 `buy_and_hold` example 完整运行，`rqalpha_exit_code=0`。
- `rqalpha/output/manual_acceptance.pkl` 成功生成。
- `rqalpha/output/manual_report/` 成功生成 `portfolio.csv`、`positions_weight.csv`、`stock_account.csv`、`stock_positions.csv`、`summary.xlsx`、`trades.csv`。

人工执行出现 pandas `FutureWarning`，不影响本次 PoC 通过。运行同时提示 `base.capital_gain_tax_rate` 当前默认值为 0、未来版本将调整；因此本次通过只确认官方示例的可复现性，**不代表** RQAlpha 默认税费模型符合 2026 年 A 股实际费用。既有边界继续保留：Transfer fee 为 `UNKNOWN / NEEDS CURRENT-RULE VALIDATION`；停牌的 `IsTradingValidator` 有源码实现，但未找到专门官方 Golden Case。

## Official example source

- Local: `rqalpha/source/rqalpha/examples/buy_and_hold.py`
- Upstream: <https://github.com/ricequant/rqalpha/blob/release/6.4.0/rqalpha/examples/buy_and_hold.py>
- Tutorial: <https://github.com/ricequant/rqalpha/blob/release/6.4.0/docs/source/intro/tutorial.rst>

The example selects `000001.XSHE`, calls `update_universe`, and once calls `order_percent(context.s1, 1)`. It was run unchanged. No strategy was written for this PoC.

## Data source

Official RiceQuant free bundle, downloaded with the documented CLI:

```bash
rqalpha/.venv/bin/rqalpha download-bundle -d rqalpha/data --confirm
rqalpha/.venv/bin/rqalpha check-bundle -d rqalpha/data
```

Result: `good bundle's day bar`. The downloader obtained `rqbundle_202609.tar.bz2` from RiceQuant's official bundle CDN and extracted it to `rqalpha/data/bundle`.

The official guide describes free daily stock, common-index, exchange-traded-fund, and futures data updated monthly. Observed files include `stocks.h5`, `funds.h5`, `indexes.h5`, `futures.h5`, `instruments.pk`, `suspended_days.h5`, `st_stock_days.h5`, and `trading_dates.npy`. Read-only inspection found 5,574 `CS` and 1,831 `ETF` instruments. The calendar contains 5,587 dates from 2005-01-04 through 2027-12-31; future calendar entries do not imply future market observations.

A read-only smoke check through RQAlpha's own `BaseDataSource` completed with exit code 0. It loaded the CN trading calendar, resolved `000001.XSHE` as `INSTRUMENT_TYPE.CS` with `market_tplus=1`, and read its 2016-06-01 daily bar: open 10.51, high 10.55, low 10.44, close 10.48, volume 55,675,091, limit-up 11.61, and limit-down 9.50. The evidence log is `rqalpha/output/data_smoke.log`. This validates bundle readability; it does not assert that the bundle is real-time or exchange-official live data.

Evidence: <https://github.com/ricequant/rqalpha/blob/release/6.4.0/docs/source/intro/install.rst>, <https://github.com/ricequant/rqalpha/blob/release/6.4.0/rqalpha/cmds/bundle.py>, <https://github.com/ricequant/rqalpha/blob/release/6.4.0/rqalpha/data/base_data_source/data_source.py>

## Example command

From `quant-framework-poc/rqalpha`:

```bash
.venv/bin/rqalpha run \
  -f source/rqalpha/examples/buy_and_hold.py \
  -d data/bundle \
  -s 2016-06-01 \
  -e 2016-12-01 \
  --account stock 100000 \
  --benchmark 000300.XSHG \
  -o output/buy_and_hold.pkl
```

This is the official tutorial command with only the documented custom bundle path and output-file option added.

## Run result

PASS.

| Item | Value |
|---|---|
| Exit status | 0 |
| Strategy | Official `buy_and_hold.py`, unchanged |
| Instrument | `000001.XSHE` (Ping An Bank) |
| Benchmark | `000300.XSHG` (CSI 300) |
| Date range | 2016-06-01 through 2016-12-01 |
| Portfolio periods | 123 |
| Completed trades | 1 |
| Runtime | 17.80 seconds |
| Peak memory | 229,376,744 bytes (about 219 MiB) |

## Output

| Metric | Value |
|---|---:|
| Ending portfolio value | 111,253.852 |
| Ending cash | 1,813.852 |
| Total return | 0.11253852 |
| Annualized return | 0.24419767 |
| Benchmark total return | 0.12477323 |
| Sharpe | 1.72327278 |
| Information ratio | 0.68073256 |
| Maximum drawdown | 0.06504653 |
| Turnover | 0.47957070 |

Trade output:

| Date/time | Instrument | Side | Quantity | Price | Tax | Commission | Transaction cost |
|---|---|---|---:|---:|---:|---:|---:|
| 2016-06-01 15:00 | `000001.XSHE` | BUY | 9,500 | 10.48 | 0 | 79.648 | 79.648 |

The fill contains an `order_id`. However, the official 6.4.0 analyser exports `trades` and `portfolio`, not a standalone `orders` table. It collects order events internally for persistence/resume but omits them from the final `-o` dictionary. This PoC does not fabricate an order table or patch the analyser. Evidence: <https://github.com/ricequant/rqalpha/blob/release/6.4.0/rqalpha/mod/rqalpha_mod_sys_analyser/mod.py>

Artifacts:

- `rqalpha/output/buy_and_hold.log`: raw run log
- `rqalpha/output/buy_and_hold.pkl`: official result
- `rqalpha/output/result_inspection.log`: read-only inspection
- `rqalpha/output/report/`: official report export (`trades.csv`, `portfolio.csv`, `stock_account.csv`, `stock_positions.csv`, `positions_weight.csv`, `summary.xlsx`)
- `rqalpha/output/bundle_download.log`: bundle log

These historical results are reproduction evidence only, not current strategy performance or investment advice.

## Warnings

- `base.capital_gain_tax_rate` currently defaults to 0 and is expected to become non-zero in a future version.
- Matplotlib built its font cache on first run.
- The analyser emitted pandas deprecation warnings for `mode.use_inf_as_na`, positional `Series.__getitem__`, and report downcasting.
- None caused the example to fail.

## Known limitations discovered

- This one-buy example does not exercise a sell, T+1 rejection, price-limit rejection, suspension rejection, ETF trade, or non-zero stamp tax.
- A-share rule support below is established from official source/docs, not custom test strategies, because this phase forbids designing strategies.
- Concrete limit percentages such as 10% are not hard-coded by the matcher. RQAlpha consumes bundle `limit_up`/`limit_down`, so board/ST/date-specific thresholds depend on data correctness.
- The free bundle's calendar does not establish the latest bar date for every instrument.
- The result pickle lacks a standalone `orders` table even though the analyser internally collects order events.
- PIT financial data are advertised for the separate RQData product; RQData was not installed, licensed, or tested.
- This is not independent exchange-rule validation or a production-readiness conclusion.

## A-share capability evidence

- The official overview states the freely available data are A-share daily data: <https://github.com/ricequant/rqalpha/blob/release/6.4.0/docs/source/intro/overview.rst>
- `INSTRUMENT_TYPE.CS` represents common stocks: <https://github.com/ricequant/rqalpha/blob/release/6.4.0/rqalpha/const.py>
- Instrument docs use `.XSHE` / `.XSHG`, state a 100-share A-share round lot, and expose `market_tplus`: <https://github.com/ricequant/rqalpha/blob/release/6.4.0/rqalpha/model/instrument.py>
- The official example ran successfully against `000001.XSHE` with CSI 300 as benchmark.

## ETF capability evidence

- `INSTRUMENT_TYPE.ETF` is first-class and included in stock-account instruments: <https://github.com/ricequant/rqalpha/blob/release/6.4.0/rqalpha/const.py>, <https://github.com/ricequant/rqalpha/blob/release/6.4.0/rqalpha/utils/__init__.py>
- The official guide says the bundle includes exchange-traded funds; the downloaded bundle contains `funds.h5` and 1,831 ETF records.
- Release 6.4.0 has default, bond-ETF, and money-ETF commission profiles. `ETFTransactionCostDecider` charges commission and returns zero tax: <https://github.com/ricequant/rqalpha/blob/release/6.4.0/rqalpha/mod/rqalpha_mod_sys_transaction_cost/deciders.py>
- ETF trading was not separately run before this mandatory acceptance stop.

## Execution-model evidence

### T+1

The account mod defaults `stock_t1` to true. `StockPosition.closable` subtracts `_non_closable`; opening trades with `market_tplus >= 1` add today's bought quantity to it. Instrument docs state A-share `market_tplus` is 1.

Evidence: <https://github.com/ricequant/rqalpha/blob/release/6.4.0/rqalpha/mod/rqalpha_mod_sys_accounts/README.rst>, <https://github.com/ricequant/rqalpha/blob/release/6.4.0/rqalpha/mod/rqalpha_mod_sys_accounts/position_model.py>, <https://github.com/ricequant/rqalpha/blob/release/6.4.0/rqalpha/model/instrument.py>

### Price limits

Simulation defaults `price_limit` to true. The matcher enforces upper/lower thresholds using the data source's price board and tick-size-aware comparison. Proportional slippage is capped within valid limit prices.

Evidence: <https://github.com/ricequant/rqalpha/blob/release/6.4.0/rqalpha/mod/rqalpha_mod_sys_simulation/__init__.py>, <https://github.com/ricequant/rqalpha/blob/release/6.4.0/rqalpha/mod/rqalpha_mod_sys_simulation/matcher/base.py>, <https://github.com/ricequant/rqalpha/blob/release/6.4.0/rqalpha/mod/rqalpha_mod_sys_simulation/slippage.py>

### Suspension

`is_suspended` is an official API and the bundle has `suspended_days.h5`. `IsTradingValidator` rejects suspended common-stock orders. The bar matcher also cancels zero-volume-bar orders when the default `inactive_limit` is enabled.

Evidence: <https://github.com/ricequant/rqalpha/blob/release/6.4.0/docs/source/api/base_api.rst>, <https://github.com/ricequant/rqalpha/blob/release/6.4.0/rqalpha/mod/rqalpha_mod_sys_risk/validators/is_trading_validator.py>, <https://github.com/ricequant/rqalpha/blob/release/6.4.0/rqalpha/mod/rqalpha_mod_sys_simulation/matcher/bar_matcher.py>

### Commission and stamp tax

Stock commission defaults to 0.0008 with a CNY 5 minimum. Stock stamp tax is sell-side only: 0.001 before 2023-08-28 and 0.0005 afterward when PIT tax is enabled; otherwise the current default is 0.0005. Multipliers are configurable. ETFs use dedicated commission profiles and zero stamp tax.

Evidence: <https://github.com/ricequant/rqalpha/blob/release/6.4.0/rqalpha/mod/rqalpha_mod_sys_transaction_cost/README.rst>, <https://github.com/ricequant/rqalpha/blob/release/6.4.0/rqalpha/mod/rqalpha_mod_sys_transaction_cost/deciders.py>

### Slippage and matching

Built-in models are `PriceRatioSlippage`, `TickSizeSlippage`, and `LimitPriceSlippage`; default proportional slippage is 0. Official configuration documents daily current-bar/VWAP, minute current-bar/next-bar/VWAP, and several tick modes, plus volume, inactive, and price-limit controls.

Evidence: <https://github.com/ricequant/rqalpha/blob/release/6.4.0/rqalpha/mod/rqalpha_mod_sys_simulation/slippage.py>, <https://github.com/ricequant/rqalpha/blob/release/6.4.0/rqalpha/mod/rqalpha_mod_sys_simulation/README.rst>

### Transfer fee

**UNKNOWN / not explicitly modeled in the evaluated implementation.** A repository-wide search at commit `a5fb4e43879c381e61131399dcc094d495c7080a` found no `transfer_fee`, `transfer fee`, or `过户费` implementation, configuration, documentation, or test. `StockTransactionCostDecider.calc` returns only commission and tax and fixes `other_fees=0`; the ETF and futures deciders also set `other_fees=0`. There is no official evidence that A-share transfer fees are calculated separately or intentionally folded into the 0.0008 commission rate, so this report does not infer either behavior.

Evidence: <https://github.com/ricequant/rqalpha/blob/release/6.4.0/rqalpha/mod/rqalpha_mod_sys_transaction_cost/deciders.py>, <https://github.com/ricequant/rqalpha/blob/release/6.4.0/rqalpha/interface.py>

Status: `NEEDS CURRENT-RULE VALIDATION` before any production use. No core-code patch or fee override was made.

## Official test evidence

The following tests already exist in the official `release/6.4.0` repository. They were inspected only; this phase did not copy them into another backtester, design new Golden Cases, or expand the scope by executing the full upstream suite.

| Capability | Official test path and case | What the test establishes | Evidence status |
|---|---|---|---|
| T+1 / sellable | `tests/integration_tests/test_api/mod/sys_accounts/test_position_models.py::test_stock_sellable` | Buys 1,000 shares of `000001.XSHE`, then asserts same-day `sellable == 0`. | PRESENT |
| Limit up/down | `tests/integration_tests/test_api/test_api_stock.py::test_order_apis_reject_limit_band_prices` | Exercises safe versus blocked prices around bar `limit_up` / `limit_down`. | PRESENT |
| Matcher price limit | `tests/unittest/test_mod/test_sys_simulation/test_matcher.py::test_counterparty_offer_rejects_order_at_price_limit`; `::test_signal_matcher_rejects_order_at_price_limit` | Asserts no trade and rejected order at the supplied limit price. | PRESENT |
| Suspension rejection | No focused test case was found by searching official `tests/` for suspension/order rejection. | Source implementation exists in `IsTradingValidator`, but a dedicated Golden Case was not located. | UNKNOWN |
| Stock commission | `tests/integration_tests/test_api/mod/sys_transaction_cost/test_commission_multiplier.py::test_commission_multiplier` | Asserts calculated stock/futures transaction cost under configured multipliers. | PRESENT |
| Stamp tax | `tests/integration_tests/test_backtest_results/test_s_pit_tax.py::test_s_pit_tax`, with expected output under `tests/integration_tests/test_backtest_results/outs/` | Runs stock buys/sells across the 2023-08-28 tax-rate change with `pit_tax=True`. | PRESENT |
| ETF fees | `tests/integration_tests/test_api/mod/sys_transaction_cost/test_etf_commission_backtest.py::test_etf_commission_profiles_apply_to_backtest_trades`; `::test_etf_commission_profiles_apply_to_order_target_portfolio` | Verifies bond-ETF and money-ETF profiles affect actual backtest transactions and smart portfolio orders. | PRESENT |
| ETF fee selection/tax | `tests/unittest/test_mod/test_sys_transaction_cost/test_etf_commission.py::test_etf_profile_selection_tax_and_missing_metadata` | Verifies default/bond/money profiles and zero ETF tax, including missing metadata behavior. | PRESENT |
| Slippage | `tests/integration_tests/test_backtest_results/test_s_tick_size.py::test_s_tick_size`; `tests/integration_tests/test_backtest_results/test_f_tick_size.py::test_f_tick_size` | Verifies `TickSizeSlippage` changes trade price by the configured tick count. | PRESENT |
| Transfer fee | No implementation or official test located. | No basis to claim separate modeling or inclusion in commission. | UNKNOWN |

Official paths: <https://github.com/ricequant/rqalpha/tree/release/6.4.0/tests>

## Blocked and unknown items

- `UNKNOWN`: explicit A-share transfer-fee modeling; no official implementation/config/test evidence found.
- `UNKNOWN`: a dedicated upstream suspension-order Golden Case; source-level rejection behavior is present but a focused official test was not located.
- `UNKNOWN`: standalone final `orders` export. The analyser tracks order events internally but the official final result dictionary does not expose an `orders` table.
- `NOT TESTED`: sell-side T+1 rejection, suspension rejection, limit rejection, ETF execution, non-zero stamp tax, and transfer fee in the chosen one-buy official example. Evidence for supported behaviors is documentary/source/test-based.
- `NOT TESTED`: PIT financial data through the separate RQData product.
- `NEEDS CURRENT-RULE VALIDATION`: board/ST/date-specific limit data, stamp-tax policy, transfer fee, and all other exchange-rule assumptions before production use.
- No item above was patched or replaced with a local implementation to obtain PASS.

## Issues encountered

1. `python3.12 -m venv` failed during `ensurepip` for the available uv-managed Python. `uv venv --seed` created the isolated environment without changing RQAlpha.
2. `rqalpha report` requires its target directory to exist. The first export attempt failed; creating only the output directory and rerunning the same official command succeeded.
3. The final result does not export standalone orders. This remains documented, not patched.

## Any manual modifications

- No RQAlpha source, official example, strategy logic, bundle data, transaction rules, matcher, analyser, or backtester was modified.
- No custom strategy, factor, data provider, backtester, order reconstruction, or A-share rule implementation was created.
- Only PoC-local output directories, logs, reports, environment files, and factual documentation were added.
- The adjacent `a-share-quant` project was not modified or used.
