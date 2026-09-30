# BaoStock Capability Probe

Status: `PARTIAL`

| Interface | Status | Rows | Date coverage | Columns |
|---|---|---:|---|---|
| login | AVAILABLE |  |  |  |
| query_trade_dates | AVAILABLE | 91 | 2024-01-01..2024-03-31 | calendar_date, is_trading_day |
| query_stock_basic | AVAILABLE | 1 | 1999-11-10..1999-11-10 | code, code_name, ipoDate, outDate, type, status |
| query_all_stock | EMPTY | 0 |  |  |
| query_history_k_data_plus | AVAILABLE | 58 | 2024-01-02..2024-03-29 | date, code, open, high, low, close, preclose, volume, amount, adjustflag, turn, tradestatus, pctChg, isST |
| query_adjust_factor | EMPTY | 0 |  |  |
| query_hs300_stocks | AVAILABLE | 300 | 2024-03-25..2024-03-25 | updateDate, code, code_name |
| query_stock_industry | AVAILABLE | 1 | 2024-03-25..2024-03-25 | updateDate, code, code_name, industry, industryClassification |
| corporate_action | UNSUPPORTED |  |  |  |

Raw prices use adjustflag=3 when the endpoint is available. Price limits and market value are not inferred.
