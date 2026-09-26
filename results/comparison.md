# Framework comparison snapshot

当前已完成 Qlib 并达到 RQAlpha 人工验收点。AKQuant 栏位必须在其阶段按官方资料实测后填写；空白不表示能力缺失，也不构成最终选型。

| 客观维度 | Qlib | RQAlpha | AKQuant |
| --- | --- | --- | --- |
| 验证状态 | PASS，人工验收已通过 | PASS，已达人工验收点 | 未开始 |
| 实测版本 | 0.9.7 | 6.4.0 | — |
| Python / OS | 3.12.12 / macOS 15.6.1 arm64 | 3.12.12 / macOS 15.6.1 arm64 | — |
| 官方安装路径可用 | 是 | 是 | — |
| 官方 sample data 可用 | 是；China `qlib_data_simple` | 是；RiceQuant free bundle | — |
| 官方 example 完整运行 | 是；Alpha158 + CSI300 + LightGBM | 是；`buy_and_hold.py` | — |
| 数据来源与许可说明 | 官方 downloader；上游提示 Yahoo Finance、质量可能不完美 | 官方 RiceQuant bundle CDN；免费日线 bundle | — |
| Universe / benchmark | CSI300 / SH000300 | `000001.XSHE` / `000300.XSHG` | — |
| 测试区间 | 2017-01-01 至 2020-08-01 | 2016-06-01 至 2016-12-01 | — |
| 运行时 | 32.04 秒（成功工作流） | 17.80 秒（不含安装/下载） | — |
| 输出类型 | 预测、IC/ICIR、组合回测、MLflow artifacts | trades、portfolio、account、positions、metrics；无独立 orders 表 | — |
| 主要兼容性问题 | MLflow file-store opt-out；Gym/NumPy 告警；样例数据 NaN | `venv` ensurepip 失败，用 `uv venv --seed`；pandas deprecation warnings | — |
| 手工改动 | provider 路径；MLflow opt-out 环境变量 | 无框架/示例/规则改动；仅输出目录和报告 | — |
| 是否触及实盘 | 否 | 否 | — |
| 证据位置 | `results/qlib.md`, `qlib/output/` | `results/rqalpha.md`, `rqalpha/output/` | — |

后续比较应保持相同原则：优先官方安装、官方数据与官方示例；记录原始口径，不为追求 PASS 重写框架核心逻辑；性能数字只在数据、时间区间、费用与硬件口径一致时比较。
