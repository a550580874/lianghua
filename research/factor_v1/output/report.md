# Factor Research v1

本报告直接消费 Qlib 0.9.7 Alpha158 raw handler 输出；没有重新实现或修改任何因子公式，没有训练模型，也没有形成买卖策略。

## Data

- Framework: Qlib 0.9.7; frequency: `day`; provider: `qlib/data/cn_data`.
- The provider is the previously validated China sample dataset; its known provenance and cutoff are documented in `results/qlib.md`.

## Universe

- Instrument universe: `csi300` (CSI300).
- Splits: {'train': {'start': '2008-01-01', 'end': '2014-12-31'}, 'validation': {'start': '2015-01-01', 'end': '2016-12-31'}, 'test': {'start': '2017-01-01', 'end': '2020-08-01'}}

## Label

- Official Alpha158 label: `Ref($close, -2) / Ref($close, -1) - 1`.
- Interpretation: the target uses the T+1 to T+2 Chinese-stock time sequence documented by Qlib; it is not a claim that portfolio-level T+1 enforcement was validated here.
- Timing invariant: `information_cutoff <= signal_time <= forward_return_period`; configured here as `signal_time <= t <= t+1_to_t+2`.

## Factors

- Selected unchanged Alpha158 columns: `ROC20`, `STD20`, `MA20`, `VSTD20`, `CORR20`.
- Original factor direction is retained. No sign flip or parameter selection is performed.

## Train Results

| Factor | IC mean | IC std | ICIR | Rank IC mean | Rank ICIR | Q5-Q1 | Top-Q turnover |
|---|---:|---:|---:|---:|---:|---:|---:|
| ROC20 | 0.012580 | 0.202901 | 0.062001 | 0.025283 | 0.122014 | 0.000497 | 0.207083 |
| STD20 | 0.012570 | 0.192673 | 0.065241 | -0.003309 | -0.015907 | 0.000566 | 0.100912 |
| MA20 | 0.018602 | 0.205813 | 0.090383 | 0.036078 | 0.170633 | 0.000755 | 0.219187 |
| VSTD20 | -0.000436 | 0.105706 | -0.004123 | 0.011256 | 0.097389 | 0.000128 | 0.380988 |
| CORR20 | -0.008072 | 0.130130 | -0.062026 | -0.013319 | -0.097897 | -0.000480 | 0.153683 |

## Validation Results

| Factor | IC mean | IC std | ICIR | Rank IC mean | Rank ICIR | Q5-Q1 | Top-Q turnover |
|---|---:|---:|---:|---:|---:|---:|---:|
| ROC20 | 0.031376 | 0.222219 | 0.141193 | 0.052344 | 0.230263 | 0.001683 | 0.213820 |
| STD20 | 0.010892 | 0.233893 | 0.046567 | -0.011873 | -0.045988 | -0.000131 | 0.093266 |
| MA20 | 0.032156 | 0.226337 | 0.142072 | 0.055889 | 0.242385 | 0.001584 | 0.218125 |
| VSTD20 | -0.008709 | 0.136816 | -0.063656 | 0.001631 | 0.010429 | -0.000513 | 0.347457 |
| CORR20 | -0.010258 | 0.135230 | -0.075859 | -0.015254 | -0.104062 | -0.000977 | 0.159348 |

## Test Results

| Factor | IC mean | IC std | ICIR | Rank IC mean | Rank ICIR | Q5-Q1 | Top-Q turnover |
|---|---:|---:|---:|---:|---:|---:|---:|
| ROC20 | -0.000633 | 0.196981 | -0.003211 | 0.015170 | 0.075594 | -0.000130 | 0.185663 |
| STD20 | 0.011752 | 0.184418 | 0.063727 | -0.002201 | -0.011293 | 0.000730 | 0.088074 |
| MA20 | -0.000520 | 0.199035 | -0.002611 | 0.019083 | 0.093600 | -0.000238 | 0.206774 |
| VSTD20 | -0.012712 | 0.103744 | -0.122529 | 0.000196 | 0.001584 | -0.000380 | 0.365435 |
| CORR20 | -0.016532 | 0.137339 | -0.120374 | -0.022799 | -0.152852 | -0.000934 | 0.142329 |

## IC Stability

Annual IC and Rank IC are reported without selecting years or changing factor definitions.

| Split | Factor | Year | IC | Rank IC | Observations |
|---|---|---:|---:|---:|---:|
| train | ROC20 | 2008 | 0.031783 | 0.035924 | 65493 |
| train | ROC20 | 2009 | 0.018538 | 0.039532 | 67262 |
| train | ROC20 | 2010 | 0.005672 | 0.021141 | 66396 |
| train | ROC20 | 2011 | 0.005483 | 0.010843 | 65736 |
| train | ROC20 | 2012 | 0.015973 | 0.020558 | 68486 |
| train | ROC20 | 2013 | 0.010881 | 0.029162 | 68251 |
| train | ROC20 | 2014 | -0.000458 | 0.019795 | 69489 |
| train | STD20 | 2008 | 0.025390 | 0.013573 | 67196 |
| train | STD20 | 2009 | 0.017076 | 0.004278 | 68589 |
| train | STD20 | 2010 | 0.027061 | 0.015199 | 67788 |
| train | STD20 | 2011 | -0.006320 | -0.017389 | 67449 |
| train | STD20 | 2012 | 0.010506 | 0.000105 | 69422 |
| train | STD20 | 2013 | 0.001195 | -0.019541 | 69000 |
| train | STD20 | 2014 | 0.012807 | -0.019692 | 70668 |
| train | MA20 | 2008 | 0.029605 | 0.037571 | 67228 |
| train | MA20 | 2009 | 0.033546 | 0.059511 | 68604 |
| train | MA20 | 2010 | 0.013943 | 0.033878 | 67800 |
| train | MA20 | 2011 | 0.005644 | 0.015646 | 67462 |
| train | MA20 | 2012 | 0.018798 | 0.029766 | 69427 |
| train | MA20 | 2013 | 0.019345 | 0.041632 | 69019 |
| train | MA20 | 2014 | 0.009261 | 0.034625 | 70699 |
| train | VSTD20 | 2008 | 0.001824 | 0.014389 | 67196 |
| train | VSTD20 | 2009 | 0.013000 | 0.017605 | 68589 |
| train | VSTD20 | 2010 | 0.005517 | 0.021869 | 67788 |
| train | VSTD20 | 2011 | -0.015715 | 0.003231 | 67449 |
| train | VSTD20 | 2012 | -0.001348 | 0.005629 | 69422 |
| train | VSTD20 | 2013 | -0.001198 | 0.014559 | 69000 |
| train | VSTD20 | 2014 | -0.005105 | 0.001667 | 70668 |
| train | CORR20 | 2008 | -0.011570 | -0.012391 | 68137 |
| train | CORR20 | 2009 | 0.007295 | 0.005486 | 69437 |
| train | CORR20 | 2010 | -0.004931 | -0.010588 | 68672 |
| train | CORR20 | 2011 | -0.019047 | -0.024293 | 68516 |
| train | CORR20 | 2012 | -0.019993 | -0.027632 | 70017 |
| train | CORR20 | 2013 | -0.011301 | -0.018616 | 69132 |
| train | CORR20 | 2014 | 0.002928 | -0.005403 | 70808 |
| validation | ROC20 | 2015 | 0.034521 | 0.057011 | 64374 |
| validation | ROC20 | 2016 | 0.028231 | 0.047676 | 67839 |
| validation | STD20 | 2015 | 0.017178 | -0.004130 | 66632 |
| validation | STD20 | 2016 | 0.004605 | -0.019615 | 69151 |
| validation | MA20 | 2015 | 0.032115 | 0.058955 | 66689 |
| validation | MA20 | 2016 | 0.032197 | 0.052824 | 69188 |
| validation | VSTD20 | 2015 | -0.007481 | -0.005023 | 66632 |
| validation | VSTD20 | 2016 | -0.009937 | 0.008286 | 69151 |
| validation | CORR20 | 2015 | -0.017462 | -0.015854 | 67066 |
| validation | CORR20 | 2016 | -0.003055 | -0.014654 | 69253 |
| test | ROC20 | 2017 | -0.004982 | 0.011573 | 67375 |
| test | ROC20 | 2018 | 0.007548 | 0.014058 | 69105 |
| test | ROC20 | 2019 | 0.003327 | 0.023801 | 70710 |
| test | ROC20 | 2020 | -0.013984 | 0.008695 | 41848 |
| test | STD20 | 2017 | 0.010961 | -0.005792 | 68502 |
| test | STD20 | 2018 | 0.014143 | 0.009516 | 69899 |
| test | STD20 | 2019 | 0.003732 | -0.013327 | 71558 |
| test | STD20 | 2020 | 0.022731 | 0.002795 | 41895 |
| test | MA20 | 2017 | -0.004601 | 0.018093 | 68535 |
| test | MA20 | 2018 | 0.004143 | 0.013996 | 69927 |
| test | MA20 | 2019 | 0.006255 | 0.026113 | 71558 |
| test | MA20 | 2020 | -0.013114 | 0.017586 | 41896 |
| test | VSTD20 | 2017 | -0.016154 | -0.001648 | 68502 |
| test | VSTD20 | 2018 | -0.008162 | -0.003651 | 69899 |
| test | VSTD20 | 2019 | -0.012342 | 0.007679 | 71558 |
| test | VSTD20 | 2020 | -0.015243 | -0.002740 | 41895 |
| test | CORR20 | 2017 | -0.016072 | -0.025731 | 68699 |
| test | CORR20 | 2018 | -0.016627 | -0.023970 | 69991 |
| test | CORR20 | 2019 | -0.017167 | -0.018034 | 71943 |
| test | CORR20 | 2020 | -0.016076 | -0.023860 | 41905 |

## Quantile Analysis

Each trading date is ranked cross-sectionally into five groups. Q5-Q1 is the mean of daily Q5 minus Q1 returns; no direction is inverted.

| Split | Factor | Quantile | Mean forward return | Observations | Q5-Q1 spread | Original-direction monotonic |
|---|---|---:|---:|---:|---:|---|
| train | ROC20 | 1 | -0.000168 | 94900 | 0.000497 | False |
| train | ROC20 | 2 | 0.000124 | 93886 | 0.000497 | False |
| train | ROC20 | 3 | 0.000091 | 93875 | 0.000497 | False |
| train | ROC20 | 4 | 0.000254 | 93886 | 0.000497 | False |
| train | ROC20 | 5 | 0.000329 | 94566 | 0.000497 | False |
| train | STD20 | 1 | -0.000148 | 96696 | 0.000566 | False |
| train | STD20 | 2 | 0.000039 | 95685 | 0.000566 | False |
| train | STD20 | 3 | 0.000144 | 95684 | 0.000566 | False |
| train | STD20 | 4 | 0.000097 | 95685 | 0.000566 | False |
| train | STD20 | 5 | 0.000418 | 96362 | 0.000566 | False |
| train | MA20 | 1 | -0.000334 | 96723 | 0.000755 | True |
| train | MA20 | 2 | 0.000011 | 95714 | 0.000755 | True |
| train | MA20 | 3 | 0.000223 | 95702 | 0.000755 | True |
| train | MA20 | 4 | 0.000230 | 95714 | 0.000755 | True |
| train | MA20 | 5 | 0.000421 | 96386 | 0.000755 | True |
| train | VSTD20 | 1 | -0.000043 | 96696 | 0.000128 | False |
| train | VSTD20 | 2 | 0.000166 | 95685 | 0.000128 | False |
| train | VSTD20 | 3 | 0.000238 | 95684 | 0.000128 | False |
| train | VSTD20 | 4 | 0.000108 | 95685 | 0.000128 | False |
| train | VSTD20 | 5 | 0.000084 | 96362 | 0.000128 | False |
| train | CORR20 | 1 | 0.000321 | 97642 | -0.000480 | False |
| train | CORR20 | 2 | 0.000161 | 96600 | -0.000480 | False |
| train | CORR20 | 3 | 0.000174 | 96601 | -0.000480 | False |
| train | CORR20 | 4 | 0.000004 | 96600 | -0.000480 | False |
| train | CORR20 | 5 | -0.000159 | 97276 | -0.000480 | False |
| validation | ROC20 | 1 | -0.000855 | 26634 | 0.001683 | False |
| validation | ROC20 | 2 | 0.000158 | 26356 | 0.001683 | False |
| validation | ROC20 | 3 | 0.000728 | 26333 | 0.001683 | False |
| validation | ROC20 | 4 | 0.001006 | 26356 | 0.001683 | False |
| validation | ROC20 | 5 | 0.000828 | 26534 | 0.001683 | False |
| validation | STD20 | 1 | 0.000558 | 27350 | -0.000131 | False |
| validation | STD20 | 2 | 0.000376 | 27056 | -0.000131 | False |
| validation | STD20 | 3 | 0.000343 | 27068 | -0.000131 | False |
| validation | STD20 | 4 | 0.000057 | 27056 | -0.000131 | False |
| validation | STD20 | 5 | 0.000427 | 27253 | -0.000131 | False |
| validation | MA20 | 1 | -0.000794 | 27371 | 0.001584 | False |
| validation | MA20 | 2 | 0.000466 | 27072 | 0.001584 | False |
| validation | MA20 | 3 | 0.000788 | 27089 | 0.001584 | False |
| validation | MA20 | 4 | 0.000492 | 27072 | 0.001584 | False |
| validation | MA20 | 5 | 0.000790 | 27273 | 0.001584 | False |
| validation | VSTD20 | 1 | 0.000493 | 27350 | -0.000513 | False |
| validation | VSTD20 | 2 | 0.000601 | 27056 | -0.000513 | False |
| validation | VSTD20 | 3 | 0.000462 | 27068 | -0.000513 | False |
| validation | VSTD20 | 4 | 0.000232 | 27056 | -0.000513 | False |
| validation | VSTD20 | 5 | -0.000019 | 27253 | -0.000513 | False |
| validation | CORR20 | 1 | 0.000700 | 27465 | -0.000977 | False |
| validation | CORR20 | 2 | 0.000543 | 27155 | -0.000977 | False |
| validation | CORR20 | 3 | 0.000578 | 27183 | -0.000977 | False |
| validation | CORR20 | 4 | 0.000460 | 27155 | -0.000977 | False |
| validation | CORR20 | 5 | -0.000277 | 27361 | -0.000977 | False |
| test | ROC20 | 1 | 0.000542 | 50113 | -0.000130 | False |
| test | ROC20 | 2 | 0.000539 | 49636 | -0.000130 | False |
| test | ROC20 | 3 | 0.000276 | 49648 | -0.000130 | False |
| test | ROC20 | 4 | 0.000364 | 49636 | -0.000130 | False |
| test | ROC20 | 5 | 0.000412 | 50005 | -0.000130 | False |
| test | STD20 | 1 | 0.000089 | 50649 | 0.000730 | True |
| test | STD20 | 2 | 0.000246 | 50240 | 0.000730 | True |
| test | STD20 | 3 | 0.000378 | 50190 | 0.000730 | True |
| test | STD20 | 4 | 0.000437 | 50240 | 0.000730 | True |
| test | STD20 | 5 | 0.000820 | 50535 | 0.000730 | True |
| test | MA20 | 1 | 0.000621 | 50660 | -0.000238 | False |
| test | MA20 | 2 | 0.000473 | 50255 | -0.000238 | False |
| test | MA20 | 3 | 0.000236 | 50200 | -0.000238 | False |
| test | MA20 | 4 | 0.000232 | 50255 | -0.000238 | False |
| test | MA20 | 5 | 0.000384 | 50546 | -0.000238 | False |
| test | VSTD20 | 1 | 0.000375 | 50649 | -0.000380 | False |
| test | VSTD20 | 2 | 0.000597 | 50240 | -0.000380 | False |
| test | VSTD20 | 3 | 0.000605 | 50190 | -0.000380 | False |
| test | VSTD20 | 4 | 0.000403 | 50240 | -0.000380 | False |
| test | VSTD20 | 5 | -0.000005 | 50535 | -0.000380 | False |
| test | CORR20 | 1 | 0.000898 | 50773 | -0.000934 | False |
| test | CORR20 | 2 | 0.000526 | 50401 | -0.000934 | False |
| test | CORR20 | 3 | 0.000308 | 50308 | -0.000934 | False |
| test | CORR20 | 4 | 0.000325 | 50401 | -0.000934 | False |
| test | CORR20 | 5 | -0.000036 | 50655 | -0.000934 | False |

## Turnover

Top-quantile turnover definition: `1 - overlap(previous top Q5, current top Q5) / previous top Q5 size`, averaged over adjacent trading dates within each split.

| Split | Factor | Top-quantile turnover | Observations |
|---|---|---:|---:|
| train | ROC20 | 0.207083 | 1701 |
| train | STD20 | 0.100912 | 1701 |
| train | MA20 | 0.219187 | 1701 |
| train | VSTD20 | 0.380988 | 1701 |
| train | CORR20 | 0.153683 | 1701 |
| validation | ROC20 | 0.213820 | 487 |
| validation | STD20 | 0.093266 | 487 |
| validation | MA20 | 0.218125 | 487 |
| validation | VSTD20 | 0.347457 | 487 |
| validation | CORR20 | 0.159348 | 487 |
| test | ROC20 | 0.185663 | 866 |
| test | STD20 | 0.088074 | 868 |
| test | MA20 | 0.206774 | 868 |
| test | VSTD20 | 0.365435 | 868 |
| test | CORR20 | 0.142329 | 870 |

## Observations

- These are descriptive factor diagnostics, not a strategy, portfolio construction rule, or investment recommendation.
- Train, validation and test rows are reported separately; test results are not used to alter factors or parameters.
- Annual IC and Rank IC are included so a full-period average does not hide year-to-year instability.

## Limitations

- The Qlib sample data ends on 2021-06-11 and is not current-market data.
- This workflow does not validate complete 2026 A-share settlement, suspension, price-limit or fee rules.
- The label timing follows Qlib's official expression; it is not an independent point-in-time or production-data validation.
- No OOS strategy, walk-forward optimization, cost sensitivity, paper trading or live trading was performed.
