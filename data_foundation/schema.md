# Data Foundation canonical schema

The source layer keeps raw market observations separate from adjustment metadata. Every daily table uses `(instrument, trade_date)` as its key.

| Table | Required fields | Source semantics |
|---|---|---|
| calendar | `trade_date`, `is_open` | exchange calendar observation |
| security_master | `instrument`, `exchange`, `list_date`, `delist_date`, `name`, `market` | reference/static |
| daily_price_raw | `instrument`, `trade_date`, `open`, `high`, `low`, `close`, `volume`, `amount` | market-observed-at-close, unadjusted |
| adj_factor | `instrument`, `trade_date`, `adj_factor` | source adjustment metadata; never overwrites raw prices |
| daily_basic | `instrument`, `trade_date`, `total_mv`, `circ_mv`, `turnover_rate` | source daily snapshot |
| suspension | `instrument`, `trade_date`, `suspend_type`, `suspend_timing` | source suspension observation |
| price_limit | `instrument`, `trade_date`, `up_limit`, `down_limit` | source limit-price observation |
| index_membership | `index_code`, `instrument`, `source_date`, `weight` | source snapshot; no effective interval inferred |

The 2024-01-01 through 2024-03-31 range is a small PoC window. CSI300 PIT membership remains unresolved until `index_weight` permission and source semantics are confirmed.

BaoStock `query_hs300_stocks(date=...)` returned changing historical snapshots and an `updateDate`; this supports snapshot availability, not effective intervals. Raw snapshot rows are retained without deriving `effective_from`/`effective_to`.
