# BaoStock adjustment report

Raw OHLC uses `adjustflag=3`; adjusted research prices are kept separate.

- adjustflag=1: rows=116; columns=['date', 'code', 'open', 'high', 'low', 'close', 'volume', 'amount', 'adjustflag', 'tradestatus', 'isST']
- adjustflag=2: rows=116; columns=['date', 'code', 'open', 'high', 'low', 'close', 'volume', 'amount', 'adjustflag', 'tradestatus', 'isST']
- adjustflag=3: rows=116; columns=['date', 'code', 'open', 'high', 'low', 'close', 'volume', 'amount', 'adjustflag', 'tradestatus', 'isST']

adjustflag=1/2/3 were queried. BaoStock README/API convention is `1=后复权`, `2=前复权`, `3=不复权` (see https://github.com/litttley/baostock/blob/master/README.md); this run empirically returned distinct series (sh.600000 raw 6.60, flag2 5.9002416, flag1 78.8685876; sz.000001 raw 9.21, flag2 7.56614394, flag1 965.9160648). Flag 2 is used as the research-adjusted convention for this PoC.
No claim is made that this adjustment matches Qlib sample or Tushare.
Status: `INTERMEDIATE_READY`; official dump_bin.py still required for binary conversion.
