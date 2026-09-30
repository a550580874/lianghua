## Host environment

Recorded on 2026-09-18 (Asia/Shanghai).

| Item | Value |
|---|---|
| macOS | 15.6.1 (Build 24G90) |
| Architecture | arm64 |
| CPU | Apple M4 |
| Default `python3` | 3.14.3 (`/opt/homebrew/bin/python3`) — not used |
| Qlib Python | 3.12.12 (uv-managed CPython) |
| Qlib virtualenv | `.venv/` (dedicated to this Qlib phase) |
| uv | 0.9.5 |
| Homebrew | 6.0.22 |
| libomp | 23.1.1, installed for LightGBM on Apple Silicon |

## Python selection basis

The Qlib official README and package metadata list Python 3.8–3.12 support. Python 3.14 is not listed. The available 3.11 interpreter is a 3.11.0 release candidate, so the stable uv-managed Python 3.12.12 was selected.

Official evidence:

- <https://github.com/microsoft/qlib/blob/main/README.md#installation>
- <https://github.com/microsoft/qlib/blob/main/pyproject.toml>
- <https://github.com/microsoft/qlib/blob/main/.github/workflows/test_qlib_from_pip.yml>

## Installed Qlib environment

Key versions observed after installation:

| Package | Version |
|---|---|
| pyqlib | 0.9.7 |
| LightGBM | 4.7.0 |
| NumPy | 2.5.3 |
| pandas | 3.0.6 |
| MLflow | 3.16.1 |
| joblib | 1.6.0 |

The full package snapshot is in `qlib/output/requirements-freeze.txt`.

## Isolation and existing project

- The PoC is at `outputs/quant-framework-poc`, alongside—not inside—`a-share-quant`.
- No package was installed into `a-share-quant/.venv`.
- `a-share-quant` is not a Git repository, so a Git before/after comparison is unavailable. No command in this PoC wrote to that directory.
- Qlib, RQAlpha and AKQuant have all passed human acceptance. AKQuant uses a third, independent environment and does not modify either accepted PoC.

## RQAlpha environment

Recorded on 2026-09-18 after Qlib human acceptance.

| Item | Value |
|---|---|
| RQAlpha | 6.4.0 |
| Source tag | `release/6.4.0` |
| Source commit | `a5fb4e43879c381e61131399dcc094d495c7080a` |
| Python | 3.12.12 (uv-managed CPython) |
| Virtualenv | `rqalpha/.venv/` |
| NumPy | 2.5.3 |
| pandas | 2.3.3 |

RQAlpha declares Python `>=3.8` and classifiers through Python 3.14. Python 3.12.12 was chosen as a stable available version. The full package snapshot is `rqalpha/output/requirements-freeze.txt`.

Isolation status:

- Qlib remains in the root `.venv/`.
- RQAlpha uses only `rqalpha/.venv/`.
- AKQuant uses only `akquant/.venv/`.
- No command wrote to `a-share-quant` or its `.venv`.

## AKQuant environment

Recorded on 2026-09-20 after RQAlpha human acceptance.

| Item | Value |
|---|---|
| AKQuant | 0.3.61 |
| Source tag | `v0.3.61` |
| Source commit | `b518accbcbc40c25b727f54a9067b4c2d8a9a283` |
| Python | 3.12.12 (uv-managed CPython) |
| Platform wheel | `cp310-abi3-macosx_11_0_arm64` |
| Virtualenv | `akquant/.venv/` |
| AKShare | 1.18.96 (official example dependency) |

AKQuant declares Python `>=3.10` and classifiers through Python 3.14. Python 3.12.12 was retained as the stable isolated interpreter. The full package snapshot is `akquant/output/requirements-freeze.txt`.

Isolation status:

- Qlib remains in the root `.venv/`.
- RQAlpha remains in `rqalpha/.venv/`.
- AKQuant uses only `akquant/.venv/`.
- No command wrote to `a-share-quant` or its `.venv`.
