# Framework comparison snapshot

Qlib、RQAlpha 与 AKQuant 均已完成人工验收并通过。下表只汇总各自 PoC 已取得证据支持的事实；不同数据、区间、策略和输出口径不用于评分、排名或最终选型。

| 客观维度 | Qlib | RQAlpha | AKQuant |
| --- | --- | --- | --- |
| 验证状态 | PASS，人工验收已通过 | PASS，人工验收已通过 | PASS，人工验收已通过 |
| 实测版本 | 0.9.7 | 6.4.0 | 0.3.61（tag `v0.3.61`，commit `b518acc`） |
| Python / OS | 3.12.12 / macOS 15.6.1 arm64 | 3.12.12 / macOS 15.6.1 arm64 | 3.12.12 / macOS 15.6.1 arm64 |
| 官方安装路径可用 | 是 | 是 | 是；官方 arm64 wheel |
| 官方 sample / data 可用 | 是；China `qlib_data_simple` | 是；RiceQuant free bundle | 是；官方 quickstart 通过 AKShare 远程公共接口获取历史数据，无本地 bundle |
| 官方 example 完整运行 | 是；Alpha158 + CSI300 + LightGBM | 是；`buy_and_hold.py` | 是；未修改的 `01_quickstart.py`，exit code 0 |
| 数据来源说明 | 官方 downloader；上游提示 Yahoo Finance、质量可能不完美 | 官方 RiceQuant bundle CDN；免费日线 bundle | AKShare 远程公共数据依赖；不视为交易所官方、实时或 PIT 数据 |
| Universe / benchmark | CSI300 / SH000300 | `000001.XSHE` / `000300.XSHG` | `600000`、`600004`、`600006`；quickstart 未设置 benchmark |
| 测试区间 | 2017-01-01 至 2020-08-01 | 2016-06-01 至 2016-12-01 | 2025-01-02 至 2025-01-03，共 2 bars |
| 实测成交 | 工作流组合输出，详见 Qlib 报告 | 1 笔 BUY，9,500 股 `000001.XSHE` | 3 笔 filled BUY：162,882 @ 10.12；176,470 @ 9.33；221,774 @ 7.36 |
| 实测组合结果 | 详见 `results/qlib.md`，不跨框架比较收益 | end portfolio 111,253.852；total return 0.11253852 | initial 5,000,000；end 4,870,549.04；PnL -129,450.96；return -2.589019% |
| 实测费用 | 配置化 open/close/min costs；当前中国税费未独立验证 | example transaction cost 79.648；默认税费不得假定符合 2026 实际费用 | 每笔最低 commission 5，共 15；示例 percentage commission/stamp tax/transfer fee 为 0，不代表 2026 实际费率 |
| 输出类型 | 预测、IC/ICIR、组合回测、MLflow artifacts | trades、portfolio、account、positions、metrics；无独立 orders 表 | 控制台 `BacktestResult`、orders 与 metrics；官方 quickstart 不生成 report/plot/CSV |
| A 股规则边界 | T+1 强制执行未建立；固定 0.095 limit threshold 不等于完整规则 | 有 T+1、限价数据和停牌 validator 源码证据；transfer fee 仍 UNKNOWN | quickstart 未启用 T+1；日涨跌停 `NOT FOUND / NEEDS CURRENT-RULE VALIDATION`；停牌主要是 zero-volume / missing-slice 语义 |
| ETF 边界 | 本阶段未建立 ETF 专项证据 | 有 ETF 类型、bundle 记录与独立费率模型；未做 ETF 成交复现 | 有 `FUND` 类型和官方 ETF example；ETF 子类型规则不自动分类 |
| 主要兼容性问题 | MLflow file-store opt-out；Gym/NumPy 告警；样例数据 NaN | `venv` ensurepip 失败，用 `uv venv --seed`；pandas FutureWarning；默认税费需复核 | 依赖远程 AKShare；两日样本 Volatility Manual=`nan` / Rust=`0` 为已知可接受差异 |
| 手工改动 | provider 路径；MLflow opt-out 环境变量 | 无框架/示例/规则改动；仅输出目录和报告 | 无框架、示例、策略或规则改动；仅隔离环境、日志与事实文档 |
| 是否触及实盘 | 否 | 否 | 否 |
| 证据位置 | `results/qlib.md`, `qlib/output/` | `results/rqalpha.md`, `rqalpha/output/` | `results/akquant.md`, `akquant/output/` |

三项 PoC 均保持相同原则：优先官方安装、官方数据/推荐数据与官方示例；记录原始口径，不为追求 PASS 重写框架核心逻辑。当前性能、收益和成本数字的输入口径不同，不作横向优劣结论。

可用性说明：三项 PASS 均来自已重建环境中的 Agent 与人工验收，不等于 fresh clone 可直接运行。Git 未包含 virtualenv、下载数据/bundle、上游源码、官方 example 和 MLflow store；逐项重建路径与缺口见 `README_ZH.md` 和 `results/usability_gap.md`。
