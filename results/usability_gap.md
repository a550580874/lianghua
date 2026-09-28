# Usability and reproducibility gap audit

审计对象：GitHub 仓库 `a550580874/lianghua` 的 `main`，基于 Documentation & Usability Phase 开始时的实际 tracked files。本文只记录仓库事实和后续工程建议，不修改三个框架或历史日志。

## 审计结论

当前仓库已经足够用于阅读三个 PoC 的版本、配置、能力证据和基线输出，但还不是新用户 clone 后可直接执行的项目。

```text
git clone → 阅读报告/日志/CSV/XLSX          可行
git clone → install → run 三个 PoC         当前不可行
```

三个框架均已完成人工验收并 PASS；这里的不可直接运行是发布与环境重建缺口，不否定原机器上的验收结果。

## 仓库内容分类

| 类别 | 当前 tracked files | 说明 |
|---|---|---|
| 官方源码 | 无 | `qlib-source/` 和各框架 `source/` 被 `.gitignore` 排除 |
| 官方 example | 无 | 报告记录上游路径和固定 tag/commit，但 example 文件本身未提交 |
| PoC 配置 | `configs/workflow_config_lightgbm_Alpha158.yaml`、`qlib/workflow_config_local.yaml` | 两者用于 Qlib；都含原机器路径或依赖未提交的 `qlib-source/` |
| 验证脚本 | `qlib/verify_data.py`、`scripts/verify_qlib_data.py` | 仅 Qlib；分别期待 `qlib/data/cn_data` 和根目录 `data/cn_data` |
| 验证结果 | `results/*.md`、RQAlpha pickle/CSV/XLSX | 记录版本、能力、结果和限制 |
| 日志 | `logs/`、`qlib/output/`、`rqalpha/output/*.log`、`akquant/output/` | 包含首次失败与成功重试，属于历史证据 |
| 依赖快照 | 三个 `output/requirements-freeze.txt`、根 `requirements.txt` | freeze 是原环境快照；根 requirements 只有 `pyqlib==0.9.7`，不是三框架统一安装文件 |

## 1. clone 后缺少什么

`.gitignore` 明确排除了：

- 根 `.venv/`、`rqalpha/.venv/`、`akquant/.venv/`；
- Qlib China sample data、RQAlpha bundle 和其他 `data/`；
- Qlib `mlruns/` 及其他 experiment stores；
- `qlib-source/` 和各框架 `source/` 上游 checkout；
- 因而也缺少 RQAlpha `buy_and_hold.py` 与 AKQuant `01_quickstart.py` 官方 example。

此外，`akquant/output/manual_acceptance.log` 在报告中被定义为人工验收日志位置，但 Git 中只有 Agent 基线 `akquant/output/01_quickstart.log`，没有提交该 manual log。人工验收数值已记录在 `results/akquant.md`。

## 2. 环境如何重建

需要三个隔离环境，不能只运行根目录的 `pip install -r requirements.txt`：

| 框架 | 已验收环境 | 当前手工重建依据 |
|---|---|---|
| Qlib | Python 3.12.12，`pyqlib==0.9.7`，LightGBM 需要 `libomp` | `environment.md`、`results/qlib.md`、`qlib/output/requirements-freeze.txt` |
| RQAlpha | Python 3.12.12，`rqalpha==6.4.0` | `environment.md`、`results/rqalpha.md`、`rqalpha/output/requirements-freeze.txt` |
| AKQuant | Python 3.12.12，`akquant==0.3.61`，`akshare==1.18.96` | `environment.md`、`results/akquant.md`、`akquant/output/requirements-freeze.txt` |

`README_ZH.md` 已把这些已验证命令整理成逐框架手工步骤。freeze 文件可以审计原环境，但未被验证为跨机器、跨时间的一键 lockfile。

## 3. 数据如何重建

### Qlib

`results/qlib.md` 记录了官方 CLI：

```bash
.venv/bin/python -m qlib.cli.data qlib_data \
  --name qlib_data_simple \
  --target_dir qlib/data/cn_data \
  --interval 1d \
  --region cn
```

实际下载依赖社区托管的 `SunsetWolf/qlib_dataset` snapshot，底层示例数据有 Yahoo Finance 质量警告，日历截止 2021-06-11。远端资源改变或不可用时无法仅靠本仓库恢复完全相同的数据字节。

### RQAlpha

`results/rqalpha.md` 记录：

```bash
rqalpha/.venv/bin/rqalpha download-bundle -d rqalpha/data --confirm
rqalpha/.venv/bin/rqalpha check-bundle -d rqalpha/data
```

这会从 RiceQuant 官方 CDN 下载当时可用的 bundle。仓库保存了 2026-09 bundle 的验证结论，但没有提交 bundle；未来下载内容或覆盖区间可能变化。

### AKQuant

官方 quickstart 在运行时通过 AKShare 远程接口获取 `sh600000`、`sh600004`、`sh600006` 历史数据，没有本地 bundle 或不可变数据快照。接口不可用或数据修订会影响复现。

## 4. 上游源码如何获取

报告固定了以下来源：

| 框架 | Repository | Tag / commit | 期望本地目录 |
|---|---|---|---|
| Qlib | `https://github.com/microsoft/qlib` | `v0.9.7` / `da920b7...` | `qlib-source/` |
| RQAlpha | `https://github.com/ricequant/rqalpha` | `release/6.4.0` / `a5fb4e4...` | `rqalpha/source/` |
| AKQuant | `https://github.com/akfamily/akquant` | `v0.3.61` / `b518acc...` | `akquant/source/` |

当前没有 submodule、vendor copy 或脚本自动获取这些 checkout。新用户必须手工 clone 固定 tag，并可再用报告中的完整 commit 校验。

## 5. 依赖本机绝对路径的命令与文件

审计找到以下机器绑定：

- `configs/workflow_config_lightgbm_Alpha158.yaml` 的 `provider_uri` 指向原机器的根 `data/cn_data`。
- `qlib/workflow_config_local.yaml` 的 `provider_uri` 指向原机器的 `qlib/data/cn_data`。
- `results/qlib.md`、`results/rqalpha.md`、`results/akquant.md` 的环境创建或人工验收命令包含 `/Users/ming-shen/...` 路径；这些是历史记录，不应原样复制到其他机器。
- `qlib/workflow_config_local.yaml` 的 `BASE_CONFIG_PATH` 依赖未提交的 `qlib-source/`。

`qlib/verify_data.py` 自身使用相对脚本位置构造数据路径，重建 `qlib/data/cn_data` 后具备可移植性。`scripts/verify_qlib_data.py` 则期待另一处根 `data/cn_data`，两个 verifier 不是同一路径。

## 6. 目前无法一键复现的步骤

- 不能用一个 requirements/lockfile 同时建立三个隔离环境。
- 不能自动下载并校验三个固定版本的上游源码。
- 不能自动下载、校验和定位 Qlib/RQAlpha 数据。
- 不能自动把 Qlib YAML 的绝对 provider 路径改成当前 clone。
- 不能通过一个入口依次运行 smoke test、example、report 和结果断言。
- Qlib MLflow artifacts 被排除，clone 后只能看日志中的指标，不能直接浏览原 experiment store。
- RQAlpha 可查看已提交报告，但重新运行仍需要 bundle 和官方 example。
- AKQuant 可查看基线日志，但重新运行需要官方 example 和远程 AKShare。

## 7. 后续是否值得增加 bootstrap/setup 脚本

**值得，但不在本阶段实现。** 理由是三套环境、三个固定上游版本、两种下载数据和一个远程数据依赖已经形成重复且容易出错的人工步骤。

建议未来脚本至少做到：

- 明确支持的平台和 Python 版本；
- 分框架创建隔离环境，默认不一次安装全部框架；
- clone 固定 tag 并校验完整 commit；
- 下载数据后记录来源、日期、hash/元数据；
- 生成本机相对或动态路径配置，不把开发者绝对路径写入 tracked YAML；
- 支持 `--dry-run`，不触及真实账户或实盘组件。

在实现前需先决定远端数据变化时的可复现策略，以及是否允许保存数据快照。

## 8. 后续是否值得增加统一 CLI

**在 Research Workflow Phase 明确工作流后再决定。** 当前立即做统一 CLI 容易把三个独立 PoC 误包装成已经集成的产品。

若后续确有统一入口，建议只做编排和证据收集，例如：

```text
quant-poc doctor
quant-poc setup qlib|rqalpha|akquant
quant-poc run qlib-smoke|rqalpha-example|akquant-quickstart
quant-poc verify
```

CLI 不应自行实现交易规则、策略或 backtester，也不应隐藏框架原生配置和原始输出。

## 当前用户真正可以做什么

- 阅读三个能力报告和客观对照表。
- 阅读 Qlib/AKQuant 原始日志、RQAlpha 日志与 CSV/XLSX 报告。
- 检查依赖快照和 Qlib PoC 配置/验证脚本。
- 按 `README_ZH.md` 手工重建单个框架，再运行对应 smoke test 或官方 example。

## 当前用户还不能做什么

- clone 后无需准备就直接运行任一完整 PoC。
- 通过统一命令安装、下载、运行和验证全部框架。
- 从仓库恢复被排除的 MLflow artifacts 或完全相同的远端数据快照。
- 把当前 PASS 当作盈利、2026 A 股全规则合规或实盘就绪证明。
