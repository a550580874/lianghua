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
| ROC20 | 0.012580 | 0.202961 | 0.061983 | 0.025283 | 0.121978 | 0.000497 | 0.207083 |
| STD20 | 0.012570 | 0.192729 | 0.065222 | -0.003309 | -0.015902 | 0.000566 | 0.100912 |
| MA20 | 0.018602 | 0.205873 | 0.090356 | 0.036078 | 0.170583 | 0.000755 | 0.219187 |
| VSTD20 | -0.000436 | 0.105737 | -0.004122 | 0.011256 | 0.097360 | 0.000128 | 0.380988 |
| CORR20 | -0.008072 | 0.130169 | -0.062008 | -0.013319 | -0.097868 | -0.000480 | 0.153683 |

## Validation Results

| Factor | IC mean | IC std | ICIR | Rank IC mean | Rank ICIR | Q5-Q1 | Top-Q turnover |
|---|---:|---:|---:|---:|---:|---:|---:|
| ROC20 | 0.031376 | 0.222447 | 0.141048 | 0.052344 | 0.230027 | 0.001683 | 0.213820 |
| STD20 | 0.010892 | 0.234133 | 0.046520 | -0.011873 | -0.045941 | -0.000131 | 0.093266 |
| MA20 | 0.032156 | 0.226570 | 0.141926 | 0.055889 | 0.242136 | 0.001584 | 0.218125 |
| VSTD20 | -0.008709 | 0.136957 | -0.063590 | 0.001631 | 0.010418 | -0.000513 | 0.347457 |
| CORR20 | -0.010258 | 0.135369 | -0.075781 | -0.015254 | -0.103955 | -0.000977 | 0.159348 |

## Test Results

| Factor | IC mean | IC std | ICIR | Rank IC mean | Rank ICIR | Q5-Q1 | Top-Q turnover |
|---|---:|---:|---:|---:|---:|---:|---:|
| ROC20 | -0.000633 | 0.197095 | -0.003209 | 0.015170 | 0.075550 | -0.000130 | 0.185663 |
| STD20 | 0.011752 | 0.184524 | 0.063691 | -0.002201 | -0.011287 | 0.000730 | 0.088074 |
| MA20 | -0.000520 | 0.199150 | -0.002610 | 0.019083 | 0.093546 | -0.000238 | 0.206774 |
| VSTD20 | -0.012712 | 0.103803 | -0.122458 | 0.000196 | 0.001583 | -0.000380 | 0.365435 |
| CORR20 | -0.016532 | 0.137418 | -0.120305 | -0.022799 | -0.152764 | -0.000934 | 0.142329 |

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

## Coverage

Coverage is defined as `valid_factor_and_label_observations / total_rows`; low coverage is reported, not used to remove a factor.

| Split | Factor | Total rows | Valid factor+label | Coverage ratio | Trading days | Avg cross-section | Median cross-section | Min | Max |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| train | ROC20 | 503999 | 471113 | 0.934750 | 1702 | 282.234430 | 283.000000 | 177 | 297 |
| train | STD20 | 503999 | 480112 | 0.952605 | 1702 | 287.657462 | 289.000000 | 186 | 298 |
| train | MA20 | 503999 | 480239 | 0.952857 | 1702 | 287.735605 | 289.000000 | 186 | 298 |
| train | VSTD20 | 503999 | 480112 | 0.952605 | 1702 | 287.657462 | 289.000000 | 186 | 298 |
| train | CORR20 | 503999 | 484719 | 0.961746 | 1702 | 293.065805 | 294.000000 | 283 | 299 |
| validation | ROC20 | 145275 | 132213 | 0.910088 | 488 | 273.487705 | 276.000000 | 142 | 289 |
| validation | STD20 | 145275 | 135783 | 0.934662 | 488 | 280.875000 | 283.000000 | 146 | 294 |
| validation | MA20 | 145275 | 135877 | 0.935309 | 488 | 281.118852 | 283.000000 | 146 | 295 |
| validation | VSTD20 | 145275 | 135783 | 0.934662 | 488 | 280.875000 | 283.000000 | 146 | 294 |
| validation | CORR20 | 145275 | 136319 | 0.938351 | 488 | 288.444672 | 289.000000 | 273 | 297 |
| test | ROC20 | 260722 | 249038 | 0.955186 | 867 | 288.935409 | 289.000000 | 153 | 300 |
| test | STD20 | 260722 | 251854 | 0.965987 | 869 | 291.539701 | 292.000000 | 157 | 300 |
| test | MA20 | 260722 | 251916 | 0.966225 | 869 | 291.612198 | 292.000000 | 157 | 300 |
| test | VSTD20 | 260722 | 251854 | 0.965987 | 869 | 291.539701 | 292.000000 | 157 | 300 |
| test | CORR20 | 260722 | 252538 | 0.968610 | 871 | 294.047072 | 294.000000 | 283 | 300 |

## IC Distribution

The IC distribution uses daily cross-sectional observations. `ic_std` and standard error use sample ddof=1; t-stat is mean / standard error. Positive and negative ratios exclude zero.

| Split | Factor | IC median | IC positive ratio | IC negative ratio | IC SE | IC t-stat | IC days |
|---|---|---:|---:|---:|---:|---:|---:|
| train | ROC20 | 0.010171 | 0.521152 | 0.478848 | 0.004920 | 2.557134 | 1702 |
| train | STD20 | 0.006906 | 0.524089 | 0.475911 | 0.004672 | 2.690748 | 1702 |
| train | MA20 | 0.020692 | 0.541716 | 0.458284 | 0.004990 | 3.727680 | 1702 |
| train | VSTD20 | 0.000775 | 0.503525 | 0.496475 | 0.002563 | -0.170063 | 1702 |
| train | CORR20 | -0.007007 | 0.477086 | 0.522914 | 0.003155 | -2.558167 | 1702 |
| validation | ROC20 | 0.033908 | 0.551230 | 0.448770 | 0.010070 | 3.115852 | 488 |
| validation | STD20 | -0.008438 | 0.479508 | 0.520492 | 0.010599 | 1.027655 | 488 |
| validation | MA20 | 0.032785 | 0.553279 | 0.446721 | 0.010256 | 3.135247 | 488 |
| validation | VSTD20 | -0.009567 | 0.477459 | 0.522541 | 0.006200 | -1.404757 | 488 |
| validation | CORR20 | -0.008788 | 0.465164 | 0.534836 | 0.006128 | -1.674064 | 488 |
| test | ROC20 | -0.008210 | 0.475145 | 0.524855 | 0.006701 | -0.094388 | 865 |
| test | STD20 | 0.007846 | 0.520185 | 0.479815 | 0.006267 | 1.875362 | 867 |
| test | MA20 | -0.010086 | 0.480969 | 0.519031 | 0.006763 | -0.076841 | 867 |
| test | VSTD20 | -0.012547 | 0.448674 | 0.551326 | 0.003525 | -3.605770 | 867 |
| test | CORR20 | -0.014572 | 0.452765 | 0.547235 | 0.004664 | -3.544394 | 868 |

## Rank IC Distribution

Rank IC distribution statistics use the same daily sample definition as IC.

| Split | Factor | Rank IC median | Positive ratio | Negative ratio | SE | t-stat | Days |
|---|---|---:|---:|---:|---:|---:|---:|
| train | ROC20 | 0.023190 | 0.532902 | 0.467098 | 0.005024 | 5.032256 | 1702 |
| train | STD20 | -0.017392 | 0.463572 | 0.536428 | 0.005044 | -0.656040 | 1702 |
| train | MA20 | 0.037313 | 0.567568 | 0.432432 | 0.005126 | 7.037468 | 1702 |
| train | VSTD20 | 0.013150 | 0.546416 | 0.453584 | 0.002802 | 4.016630 | 1702 |
| train | CORR20 | -0.015232 | 0.455934 | 0.544066 | 0.003299 | -4.037576 | 1702 |
| validation | ROC20 | 0.057444 | 0.592213 | 0.407787 | 0.010301 | 5.081453 | 488 |
| validation | STD20 | -0.043277 | 0.436475 | 0.563525 | 0.011699 | -1.014871 | 488 |
| validation | MA20 | 0.055388 | 0.606557 | 0.393443 | 0.010449 | 5.348962 | 488 |
| validation | VSTD20 | -0.000124 | 0.497951 | 0.502049 | 0.007088 | 0.230151 | 488 |
| validation | CORR20 | -0.014826 | 0.467213 | 0.532787 | 0.006642 | -2.296442 | 488 |
| test | ROC20 | 0.007966 | 0.520231 | 0.479769 | 0.006827 | 2.221988 | 865 |
| test | STD20 | -0.002119 | 0.491349 | 0.508651 | 0.006622 | -0.332332 | 867 |
| test | MA20 | 0.018294 | 0.531719 | 0.468281 | 0.006928 | 2.754436 | 867 |
| test | VSTD20 | -0.006270 | 0.478662 | 0.521338 | 0.004205 | 0.046602 | 867 |
| test | CORR20 | -0.021366 | 0.440092 | 0.559908 | 0.005066 | -4.500708 | 868 |

## Factor Rank Autocorrelation

Each value is a Spearman correlation of factor values on adjacent trading dates using only the common instruments; split boundaries are not crossed.

| Split | Factor | Mean | Median | Std | Min | Max | Pairs | Positive ratio |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| train | ROC20 | 0.934488 | 0.939367 | 0.028225 | 0.731012 | 0.986369 | 1701 | 1.000000 |
| train | STD20 | 0.978800 | 0.982272 | 0.014233 | 0.820302 | 0.998225 | 1701 | 1.000000 |
| train | MA20 | 0.908327 | 0.914347 | 0.037245 | 0.613304 | 0.997231 | 1701 | 1.000000 |
| train | VSTD20 | 0.664473 | 0.668146 | 0.078610 | 0.236448 | 0.860469 | 1701 | 1.000000 |
| train | CORR20 | 0.953757 | 0.958530 | 0.023299 | 0.755377 | 0.991628 | 1701 | 1.000000 |
| validation | ROC20 | 0.922917 | 0.932618 | 0.041208 | 0.738406 | 0.994853 | 487 | 1.000000 |
| validation | STD20 | 0.978759 | 0.982814 | 0.016368 | 0.863820 | 0.997309 | 487 | 1.000000 |
| validation | MA20 | 0.900230 | 0.911590 | 0.054819 | 0.565450 | 0.998927 | 487 | 1.000000 |
| validation | VSTD20 | 0.708848 | 0.714698 | 0.100753 | 0.056047 | 0.920971 | 487 | 1.000000 |
| validation | CORR20 | 0.945202 | 0.951427 | 0.031475 | 0.722172 | 0.992148 | 487 | 1.000000 |
| test | ROC20 | 0.935224 | 0.940312 | 0.031718 | 0.513234 | 0.983620 | 866 | 1.000000 |
| test | STD20 | 0.981411 | 0.984890 | 0.017032 | 0.758035 | 0.996503 | 868 | 1.000000 |
| test | MA20 | 0.910738 | 0.916271 | 0.035882 | 0.582932 | 0.976706 | 868 | 1.000000 |
| test | VSTD20 | 0.678631 | 0.685425 | 0.086356 | 0.223677 | 0.914390 | 868 | 1.000000 |
| test | CORR20 | 0.955695 | 0.961177 | 0.025643 | 0.687662 | 0.991588 | 870 | 1.000000 |

## Factor Decay

For horizon H, forward return is `Ref($close, -(H+1)) / Ref($close, -1) - 1`. Signals whose exit date exceeds their own split end are excluded; no next-split price fills the tail.

| Split | Factor | Horizon | IC mean | IC std | ICIR | Rank IC mean | Rank IC std | Rank ICIR | IC days | Rank IC days |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| train | ROC20 | 1D | 0.013277 | 0.202274 | 0.065638 | 0.024996 | 0.207182 | 0.120648 | 1700 | 1700 |
| train | ROC20 | 5D | 0.024255 | 0.190252 | 0.127488 | 0.031715 | 0.197320 | 0.160729 | 1696 | 1696 |
| train | ROC20 | 10D | 0.022696 | 0.179278 | 0.126596 | 0.032373 | 0.190200 | 0.170207 | 1691 | 1691 |
| train | ROC20 | 20D | 0.030641 | 0.177507 | 0.172619 | 0.038515 | 0.186244 | 0.206799 | 1681 | 1681 |
| train | STD20 | 1D | 0.013314 | 0.192240 | 0.069255 | -0.003066 | 0.208109 | -0.014735 | 1700 | 1700 |
| train | STD20 | 5D | 0.015493 | 0.179651 | 0.086241 | -0.001154 | 0.199572 | -0.005784 | 1696 | 1696 |
| train | STD20 | 10D | 0.014876 | 0.171230 | 0.086879 | -0.001192 | 0.194485 | -0.006131 | 1691 | 1691 |
| train | STD20 | 20D | 0.018094 | 0.170775 | 0.105952 | 0.004020 | 0.192297 | 0.020906 | 1681 | 1681 |
| train | MA20 | 1D | 0.019393 | 0.205052 | 0.094576 | 0.035732 | 0.211248 | 0.169148 | 1700 | 1700 |
| train | MA20 | 5D | 0.027218 | 0.189504 | 0.143627 | 0.035100 | 0.198322 | 0.176985 | 1696 | 1696 |
| train | MA20 | 10D | 0.015676 | 0.177906 | 0.088115 | 0.023509 | 0.191090 | 0.123027 | 1691 | 1691 |
| train | MA20 | 20D | 0.025795 | 0.170743 | 0.151075 | 0.034066 | 0.181689 | 0.187493 | 1681 | 1681 |
| train | VSTD20 | 1D | -0.000842 | 0.105463 | -0.007983 | 0.011048 | 0.115485 | 0.095669 | 1700 | 1700 |
| train | VSTD20 | 5D | -0.006654 | 0.103691 | -0.064175 | 0.001041 | 0.114922 | 0.009062 | 1696 | 1696 |
| train | VSTD20 | 10D | -0.009006 | 0.102023 | -0.088275 | -0.003731 | 0.116927 | -0.031912 | 1691 | 1691 |
| train | VSTD20 | 20D | -0.003808 | 0.099105 | -0.038420 | 0.000535 | 0.114458 | 0.004674 | 1681 | 1681 |
| train | CORR20 | 1D | -0.008264 | 0.129945 | -0.063593 | -0.013255 | 0.136219 | -0.097308 | 1700 | 1700 |
| train | CORR20 | 5D | -0.023773 | 0.136293 | -0.174428 | -0.031153 | 0.141224 | -0.220590 | 1696 | 1696 |
| train | CORR20 | 10D | -0.033000 | 0.141141 | -0.233807 | -0.040966 | 0.144233 | -0.284026 | 1691 | 1691 |
| train | CORR20 | 20D | -0.047391 | 0.131385 | -0.360703 | -0.055397 | 0.133146 | -0.416060 | 1681 | 1681 |
| validation | ROC20 | 1D | 0.030905 | 0.222610 | 0.138830 | 0.052106 | 0.228006 | 0.228527 | 486 | 486 |
| validation | ROC20 | 5D | 0.059275 | 0.212505 | 0.278933 | 0.077888 | 0.216532 | 0.359707 | 482 | 482 |
| validation | ROC20 | 10D | 0.083764 | 0.205631 | 0.407349 | 0.095490 | 0.214018 | 0.446176 | 477 | 477 |
| validation | ROC20 | 20D | 0.125666 | 0.201191 | 0.624614 | 0.126190 | 0.209667 | 0.601857 | 467 | 467 |
| validation | STD20 | 1D | 0.010817 | 0.233888 | 0.046248 | -0.012357 | 0.258788 | -0.047748 | 486 | 486 |
| validation | STD20 | 5D | -0.006045 | 0.215842 | -0.028006 | -0.035695 | 0.244807 | -0.145808 | 482 | 482 |
| validation | STD20 | 10D | -0.014077 | 0.204014 | -0.068998 | -0.044182 | 0.234854 | -0.188126 | 477 | 477 |
| validation | STD20 | 20D | -0.031616 | 0.223891 | -0.141211 | -0.065505 | 0.246846 | -0.265367 | 467 | 467 |
| validation | MA20 | 1D | 0.031359 | 0.226417 | 0.138499 | 0.055391 | 0.231050 | 0.239735 | 486 | 486 |
| validation | MA20 | 5D | 0.055463 | 0.213206 | 0.260137 | 0.074846 | 0.216284 | 0.346055 | 482 | 482 |
| validation | MA20 | 10D | 0.068023 | 0.193487 | 0.351564 | 0.079179 | 0.203690 | 0.388722 | 477 | 477 |
| validation | MA20 | 20D | 0.101636 | 0.195051 | 0.521077 | 0.097131 | 0.207452 | 0.468212 | 467 | 467 |
| validation | VSTD20 | 1D | -0.008722 | 0.137141 | -0.063596 | 0.001659 | 0.156891 | 0.010571 | 486 | 486 |
| validation | VSTD20 | 5D | -0.014737 | 0.124802 | -0.118087 | -0.012248 | 0.144502 | -0.084761 | 482 | 482 |
| validation | VSTD20 | 10D | -0.019149 | 0.124556 | -0.153737 | -0.018510 | 0.142132 | -0.130234 | 477 | 477 |
| validation | VSTD20 | 20D | -0.018156 | 0.130890 | -0.138714 | -0.032939 | 0.155798 | -0.211419 | 467 | 467 |
| validation | CORR20 | 1D | -0.010434 | 0.135644 | -0.076919 | -0.015321 | 0.147150 | -0.104115 | 486 | 486 |
| validation | CORR20 | 5D | -0.018746 | 0.128497 | -0.145884 | -0.031694 | 0.142576 | -0.222295 | 482 | 482 |
| validation | CORR20 | 10D | -0.020551 | 0.139031 | -0.147819 | -0.037498 | 0.152229 | -0.246326 | 477 | 477 |
| validation | CORR20 | 20D | -0.027184 | 0.130996 | -0.207520 | -0.046432 | 0.142661 | -0.325469 | 467 | 467 |
| test | ROC20 | 1D | -0.000277 | 0.196397 | -0.001411 | 0.014890 | 0.200774 | 0.074163 | 863 | 863 |
| test | ROC20 | 5D | 0.001072 | 0.182934 | 0.005861 | 0.016428 | 0.195134 | 0.084186 | 858 | 858 |
| test | ROC20 | 10D | -0.001057 | 0.173926 | -0.006075 | 0.015364 | 0.186667 | 0.082310 | 853 | 853 |
| test | ROC20 | 20D | -0.002694 | 0.166176 | -0.016213 | 0.012626 | 0.179330 | 0.070406 | 843 | 843 |
| test | STD20 | 1D | 0.012050 | 0.183768 | 0.065574 | -0.002079 | 0.194981 | -0.010665 | 865 | 865 |
| test | STD20 | 5D | 0.014963 | 0.164940 | 0.090719 | 0.001782 | 0.181210 | 0.009835 | 860 | 860 |
| test | STD20 | 10D | 0.015725 | 0.160307 | 0.098093 | 0.006144 | 0.179244 | 0.034276 | 855 | 855 |
| test | STD20 | 20D | 0.029760 | 0.160951 | 0.184903 | 0.023811 | 0.179719 | 0.132488 | 845 | 845 |
| test | MA20 | 1D | -0.000210 | 0.198453 | -0.001060 | 0.018662 | 0.203978 | 0.091491 | 865 | 865 |
| test | MA20 | 5D | 0.000403 | 0.185351 | 0.002176 | 0.012946 | 0.199458 | 0.064908 | 860 | 860 |
| test | MA20 | 10D | -0.007758 | 0.174083 | -0.044563 | 0.004284 | 0.190242 | 0.022517 | 855 | 855 |
| test | MA20 | 20D | -0.003321 | 0.169800 | -0.019559 | 0.006763 | 0.181958 | 0.037168 | 845 | 845 |
| test | VSTD20 | 1D | -0.012796 | 0.103050 | -0.124174 | -0.000194 | 0.123647 | -0.001569 | 865 | 865 |
| test | VSTD20 | 5D | -0.022385 | 0.103302 | -0.216696 | -0.014763 | 0.122553 | -0.120463 | 860 | 860 |
| test | VSTD20 | 10D | -0.028208 | 0.105413 | -0.267598 | -0.019632 | 0.123592 | -0.158848 | 855 | 855 |
| test | VSTD20 | 20D | -0.031952 | 0.104023 | -0.307159 | -0.022953 | 0.121494 | -0.188925 | 845 | 845 |
| test | CORR20 | 1D | -0.017161 | 0.137044 | -0.125221 | -0.023139 | 0.149253 | -0.155034 | 866 | 866 |
| test | CORR20 | 5D | -0.039969 | 0.135251 | -0.295514 | -0.050315 | 0.150178 | -0.335036 | 861 | 861 |
| test | CORR20 | 10D | -0.055222 | 0.141485 | -0.390299 | -0.070443 | 0.155679 | -0.452488 | 856 | 856 |
| test | CORR20 | 20D | -0.071702 | 0.148786 | -0.481918 | -0.088552 | 0.158023 | -0.560371 | 846 | 846 |

## Factor Correlation

Pearson and Spearman factor correlations are computed cross-sectionally per day and then averaged in long format. No factor is removed based on correlation.

| Split | Method | Factor A | Factor B | Mean correlation | Days |
|---|---|---|---|---:|---:|
| train | pearson | ROC20 | ROC20 | 1.000000 | 1702 |
| train | pearson | ROC20 | STD20 | -0.026603 | 1702 |
| train | pearson | ROC20 | MA20 | 0.839005 | 1702 |
| train | pearson | ROC20 | VSTD20 | -0.041425 | 1702 |
| train | pearson | ROC20 | CORR20 | -0.262349 | 1702 |
| train | pearson | STD20 | ROC20 | -0.026603 | 1702 |
| train | pearson | STD20 | STD20 | 1.000000 | 1702 |
| train | pearson | STD20 | MA20 | 0.011177 | 1702 |
| train | pearson | STD20 | VSTD20 | 0.121183 | 1702 |
| train | pearson | STD20 | CORR20 | -0.052968 | 1702 |
| train | pearson | MA20 | ROC20 | 0.839005 | 1702 |
| train | pearson | MA20 | STD20 | 0.011177 | 1702 |
| train | pearson | MA20 | MA20 | 1.000000 | 1702 |
| train | pearson | MA20 | VSTD20 | 0.081650 | 1702 |
| train | pearson | MA20 | CORR20 | -0.277416 | 1702 |
| train | pearson | VSTD20 | ROC20 | -0.041425 | 1702 |
| train | pearson | VSTD20 | STD20 | 0.121183 | 1702 |
| train | pearson | VSTD20 | MA20 | 0.081650 | 1702 |
| train | pearson | VSTD20 | VSTD20 | 1.000000 | 1702 |
| train | pearson | VSTD20 | CORR20 | 0.120191 | 1702 |
| train | pearson | CORR20 | ROC20 | -0.262349 | 1702 |
| train | pearson | CORR20 | STD20 | -0.052968 | 1702 |
| train | pearson | CORR20 | MA20 | -0.277416 | 1702 |
| train | pearson | CORR20 | VSTD20 | 0.120191 | 1702 |
| train | pearson | CORR20 | CORR20 | 1.000000 | 1702 |
| train | spearman | ROC20 | ROC20 | 1.000000 | 1702 |
| train | spearman | ROC20 | STD20 | -0.003425 | 1702 |
| train | spearman | ROC20 | MA20 | 0.820309 | 1702 |
| train | spearman | ROC20 | VSTD20 | -0.052668 | 1702 |
| train | spearman | ROC20 | CORR20 | -0.239784 | 1702 |
| train | spearman | STD20 | ROC20 | -0.003425 | 1702 |
| train | spearman | STD20 | STD20 | 1.000000 | 1702 |
| train | spearman | STD20 | MA20 | 0.044354 | 1702 |
| train | spearman | STD20 | VSTD20 | 0.125118 | 1702 |
| train | spearman | STD20 | CORR20 | -0.000175 | 1702 |
| train | spearman | MA20 | ROC20 | 0.820309 | 1702 |
| train | spearman | MA20 | STD20 | 0.044354 | 1702 |
| train | spearman | MA20 | MA20 | 1.000000 | 1702 |
| train | spearman | MA20 | VSTD20 | 0.081488 | 1702 |
| train | spearman | MA20 | CORR20 | -0.237513 | 1702 |
| train | spearman | VSTD20 | ROC20 | -0.052668 | 1702 |
| train | spearman | VSTD20 | STD20 | 0.125118 | 1702 |
| train | spearman | VSTD20 | MA20 | 0.081488 | 1702 |
| train | spearman | VSTD20 | VSTD20 | 1.000000 | 1702 |
| train | spearman | VSTD20 | CORR20 | 0.174350 | 1702 |
| train | spearman | CORR20 | ROC20 | -0.239784 | 1702 |
| train | spearman | CORR20 | STD20 | -0.000175 | 1702 |
| train | spearman | CORR20 | MA20 | -0.237513 | 1702 |
| train | spearman | CORR20 | VSTD20 | 0.174350 | 1702 |
| train | spearman | CORR20 | CORR20 | 1.000000 | 1702 |
| validation | pearson | ROC20 | ROC20 | 1.000000 | 488 |
| validation | pearson | ROC20 | STD20 | -0.170420 | 488 |
| validation | pearson | ROC20 | MA20 | 0.816275 | 488 |
| validation | pearson | ROC20 | VSTD20 | -0.017673 | 488 |
| validation | pearson | ROC20 | CORR20 | -0.101757 | 488 |
| validation | pearson | STD20 | ROC20 | -0.170420 | 488 |
| validation | pearson | STD20 | STD20 | 1.000000 | 488 |
| validation | pearson | STD20 | MA20 | -0.087238 | 488 |
| validation | pearson | STD20 | VSTD20 | 0.118153 | 488 |
| validation | pearson | STD20 | CORR20 | 0.087773 | 488 |
| validation | pearson | MA20 | ROC20 | 0.816275 | 488 |
| validation | pearson | MA20 | STD20 | -0.087238 | 488 |
| validation | pearson | MA20 | MA20 | 1.000000 | 488 |
| validation | pearson | MA20 | VSTD20 | 0.157006 | 488 |
| validation | pearson | MA20 | CORR20 | -0.151546 | 488 |
| validation | pearson | VSTD20 | ROC20 | -0.017673 | 488 |
| validation | pearson | VSTD20 | STD20 | 0.118153 | 488 |
| validation | pearson | VSTD20 | MA20 | 0.157006 | 488 |
| validation | pearson | VSTD20 | VSTD20 | 1.000000 | 488 |
| validation | pearson | VSTD20 | CORR20 | 0.114955 | 488 |
| validation | pearson | CORR20 | ROC20 | -0.101757 | 488 |
| validation | pearson | CORR20 | STD20 | 0.087773 | 488 |
| validation | pearson | CORR20 | MA20 | -0.151546 | 488 |
| validation | pearson | CORR20 | VSTD20 | 0.114955 | 488 |
| validation | pearson | CORR20 | CORR20 | 1.000000 | 488 |
| validation | spearman | ROC20 | ROC20 | 1.000000 | 488 |
| validation | spearman | ROC20 | STD20 | -0.118697 | 488 |
| validation | spearman | ROC20 | MA20 | 0.793648 | 488 |
| validation | spearman | ROC20 | VSTD20 | -0.027175 | 488 |
| validation | spearman | ROC20 | CORR20 | -0.092070 | 488 |
| validation | spearman | STD20 | ROC20 | -0.118697 | 488 |
| validation | spearman | STD20 | STD20 | 1.000000 | 488 |
| validation | spearman | STD20 | MA20 | -0.033646 | 488 |
| validation | spearman | STD20 | VSTD20 | 0.106806 | 488 |
| validation | spearman | STD20 | CORR20 | 0.161389 | 488 |
| validation | spearman | MA20 | ROC20 | 0.793648 | 488 |
| validation | spearman | MA20 | STD20 | -0.033646 | 488 |
| validation | spearman | MA20 | MA20 | 1.000000 | 488 |
| validation | spearman | MA20 | VSTD20 | 0.178122 | 488 |
| validation | spearman | MA20 | CORR20 | -0.107664 | 488 |
| validation | spearman | VSTD20 | ROC20 | -0.027175 | 488 |
| validation | spearman | VSTD20 | STD20 | 0.106806 | 488 |
| validation | spearman | VSTD20 | MA20 | 0.178122 | 488 |
| validation | spearman | VSTD20 | VSTD20 | 1.000000 | 488 |
| validation | spearman | VSTD20 | CORR20 | 0.177216 | 488 |
| validation | spearman | CORR20 | ROC20 | -0.092070 | 488 |
| validation | spearman | CORR20 | STD20 | 0.161389 | 488 |
| validation | spearman | CORR20 | MA20 | -0.107664 | 488 |
| validation | spearman | CORR20 | VSTD20 | 0.177216 | 488 |
| validation | spearman | CORR20 | CORR20 | 1.000000 | 488 |
| test | pearson | ROC20 | ROC20 | 1.000000 | 867 |
| test | pearson | ROC20 | STD20 | -0.046801 | 867 |
| test | pearson | ROC20 | MA20 | 0.845288 | 867 |
| test | pearson | ROC20 | VSTD20 | 0.077404 | 867 |
| test | pearson | ROC20 | CORR20 | -0.288642 | 867 |
| test | pearson | STD20 | ROC20 | -0.046801 | 867 |
| test | pearson | STD20 | STD20 | 1.000000 | 869 |
| test | pearson | STD20 | MA20 | -0.002657 | 869 |
| test | pearson | STD20 | VSTD20 | 0.139456 | 869 |
| test | pearson | STD20 | CORR20 | -0.028779 | 869 |
| test | pearson | MA20 | ROC20 | 0.845288 | 867 |
| test | pearson | MA20 | STD20 | -0.002657 | 869 |
| test | pearson | MA20 | MA20 | 1.000000 | 869 |
| test | pearson | MA20 | VSTD20 | 0.157734 | 869 |
| test | pearson | MA20 | CORR20 | -0.280739 | 869 |
| test | pearson | VSTD20 | ROC20 | 0.077404 | 867 |
| test | pearson | VSTD20 | STD20 | 0.139456 | 869 |
| test | pearson | VSTD20 | MA20 | 0.157734 | 869 |
| test | pearson | VSTD20 | VSTD20 | 1.000000 | 869 |
| test | pearson | VSTD20 | CORR20 | 0.158940 | 869 |
| test | pearson | CORR20 | ROC20 | -0.288642 | 867 |
| test | pearson | CORR20 | STD20 | -0.028779 | 869 |
| test | pearson | CORR20 | MA20 | -0.280739 | 869 |
| test | pearson | CORR20 | VSTD20 | 0.158940 | 869 |
| test | pearson | CORR20 | CORR20 | 1.000000 | 871 |
| test | spearman | ROC20 | ROC20 | 1.000000 | 867 |
| test | spearman | ROC20 | STD20 | -0.055970 | 867 |
| test | spearman | ROC20 | MA20 | 0.822386 | 867 |
| test | spearman | ROC20 | VSTD20 | 0.061471 | 867 |
| test | spearman | ROC20 | CORR20 | -0.266282 | 867 |
| test | spearman | STD20 | ROC20 | -0.055970 | 867 |
| test | spearman | STD20 | STD20 | 1.000000 | 869 |
| test | spearman | STD20 | MA20 | 0.001750 | 869 |
| test | spearman | STD20 | VSTD20 | 0.129245 | 869 |
| test | spearman | STD20 | CORR20 | 0.026016 | 869 |
| test | spearman | MA20 | ROC20 | 0.822386 | 867 |
| test | spearman | MA20 | STD20 | 0.001750 | 869 |
| test | spearman | MA20 | MA20 | 1.000000 | 869 |
| test | spearman | MA20 | VSTD20 | 0.164402 | 869 |
| test | spearman | MA20 | CORR20 | -0.230532 | 869 |
| test | spearman | VSTD20 | ROC20 | 0.061471 | 867 |
| test | spearman | VSTD20 | STD20 | 0.129245 | 869 |
| test | spearman | VSTD20 | MA20 | 0.164402 | 869 |
| test | spearman | VSTD20 | VSTD20 | 1.000000 | 869 |
| test | spearman | VSTD20 | CORR20 | 0.200321 | 869 |
| test | spearman | CORR20 | ROC20 | -0.266282 | 867 |
| test | spearman | CORR20 | STD20 | 0.026016 | 869 |
| test | spearman | CORR20 | MA20 | -0.230532 | 869 |
| test | spearman | CORR20 | VSTD20 | 0.200321 | 869 |
| test | spearman | CORR20 | CORR20 | 1.000000 | 871 |

## Quantile Spread Statistics

Daily spread is mean forward return of Q5 minus mean forward return of Q1. Standard deviation is sample ddof=1 and t-stat uses daily spread observations.

| Split | Factor | Mean | Median | Std | SE | t-stat | Positive ratio | Negative ratio | Days |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| train | ROC20 | 0.000497 | 0.000484 | 0.012675 | 0.000307 | 1.617790 | 0.517626 | 0.482374 | 1702 |
| train | STD20 | 0.000566 | 0.000348 | 0.012132 | 0.000294 | 1.926183 | 0.513514 | 0.486486 | 1702 |
| train | MA20 | 0.000755 | 0.000989 | 0.012981 | 0.000315 | 2.400311 | 0.534665 | 0.465335 | 1702 |
| train | VSTD20 | 0.000128 | 0.000298 | 0.006989 | 0.000169 | 0.753026 | 0.519389 | 0.480611 | 1702 |
| train | CORR20 | -0.000480 | -0.000506 | 0.008228 | 0.000199 | -2.409125 | 0.468860 | 0.531140 | 1702 |
| validation | ROC20 | 0.001683 | 0.001152 | 0.016963 | 0.000768 | 2.191944 | 0.538934 | 0.461066 | 488 |
| validation | STD20 | -0.000131 | -0.000153 | 0.018295 | 0.000828 | -0.157592 | 0.495902 | 0.504098 | 488 |
| validation | MA20 | 0.001584 | 0.001216 | 0.017253 | 0.000781 | 2.028382 | 0.538934 | 0.461066 | 488 |
| validation | VSTD20 | -0.000513 | -0.000281 | 0.012480 | 0.000565 | -0.907886 | 0.467213 | 0.532787 | 488 |
| validation | CORR20 | -0.000977 | -0.000690 | 0.010711 | 0.000485 | -2.015623 | 0.446721 | 0.553279 | 488 |
| test | ROC20 | -0.000130 | -0.000316 | 0.010969 | 0.000373 | -0.347766 | 0.477457 | 0.522543 | 865 |
| test | STD20 | 0.000730 | 0.000911 | 0.010144 | 0.000345 | 2.119610 | 0.531719 | 0.468281 | 867 |
| test | MA20 | -0.000238 | -0.000304 | 0.010920 | 0.000371 | -0.641113 | 0.484429 | 0.515571 | 867 |
| test | VSTD20 | -0.000380 | -0.000383 | 0.006638 | 0.000225 | -1.686465 | 0.467128 | 0.532872 | 867 |
| test | CORR20 | -0.000934 | -0.001066 | 0.008523 | 0.000289 | -3.230179 | 0.435484 | 0.564516 | 868 |

## Observations

- These are descriptive factor diagnostics, not a strategy, portfolio construction rule, or investment recommendation.
- Train, validation and test rows are reported separately; test results are not used to alter factors or parameters.
- Annual IC and Rank IC are included so a full-period average does not hide year-to-year instability.
- V2 robustness diagnostics are descriptive only; they do not select, rank, drop or reweight factors.

## Limitations

- The Qlib sample data ends on 2021-06-11 and is not current-market data.
- This workflow does not validate complete 2026 A-share settlement, suspension, price-limit or fee rules.
- The label timing follows Qlib's official expression; it is not an independent point-in-time or production-data validation.
- No OOS strategy, walk-forward optimization, cost sensitivity, paper trading or live trading was performed.
