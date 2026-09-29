"""Minimal, credential-safe Tushare Pro capability probe."""
from __future__ import annotations

import json
import os
import platform
from datetime import date
from pathlib import Path

INTERFACES = ["trade_cal", "stock_basic", "daily", "adj_factor", "daily_basic", "suspend_d", "stk_limit", "index_weight", "index_classify", "index_member_all"]
OUT = Path(__file__).parent / "output"


def _safe_error(exc: Exception) -> dict:
    """Return diagnostics with any credential value removed."""
    message = str(exc)
    token = os.getenv("TUSHARE_TOKEN")
    if token:
        message = message.replace(token, "[REDACTED]")
    return {"error_type": type(exc).__name__, "message": message[:300]}


def _probe(api, name: str) -> dict:
    today = date.today().isoformat()
    kwargs = {"trade_date": "20240131"} if name in {"trade_cal", "daily", "adj_factor", "daily_basic", "suspend_d", "stk_limit"} else {}
    if name == "stock_basic": kwargs = {"exchange": "SSE", "list_status": "L"}
    if name == "index_weight": kwargs = {"index_code": "000300.SZ", "start_date": "20240101", "end_date": "20240331"}
    try:
        frame = getattr(api, name)(**kwargs)
        columns = [str(c) for c in frame.columns]
        result = {"status": "available" if len(frame) else "empty", "sample_row_count": int(len(frame)), "columns": columns}
        if len(frame):
            for col in ("trade_date", "cal_date", "list_date", "end_date", "start_date"):
                if col in frame:
                    result["earliest_date"] = str(frame[col].min())
                    result["latest_date"] = str(frame[col].max())
                    break
        return result
    except Exception as exc:  # API errors are evidence, not reasons to substitute a source.
        text = str(exc).lower()
        denied = any(word in text for word in ("权限", "permission", "token", "积分", "auth"))
        return {"status": "permission_denied" if denied else "error", **_safe_error(exc)}


def run_probe() -> dict:
    result = {"generated_at": date.today().isoformat(), "platform": platform.platform(), "credential_status": "present" if os.getenv("TUSHARE_TOKEN") else "missing", "interfaces": {}}
    if result["credential_status"] == "missing":
        result["status"] = "BLOCKED_CREDENTIAL"
        for name in INTERFACES:
            result["interfaces"][name] = {"status": "not_attempted", "reason": "TUSHARE_TOKEN is not set"}
        return result
    try:
        import tushare as ts
        api = ts.pro_api(os.environ["TUSHARE_TOKEN"])
    except Exception as exc:
        result["status"] = "ERROR"
        result.update(_safe_error(exc))
        return result
    result["interfaces"] = {name: _probe(api, name) for name in INTERFACES}
    statuses = {item["status"] for item in result["interfaces"].values()}
    result["status"] = "PARTIAL_PASS_PERMISSION_BLOCKED" if "permission_denied" in statuses else "PASS"
    return result


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    result = run_probe()
    (OUT / "capability_report.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Tushare Pro Capability Probe", "", f"Status: `{result['status']}`", f"Credential: `{result['credential_status']}`", "", "| Interface | Status | Rows | Columns |", "|---|---|---:|---|"]
    for name, item in result["interfaces"].items():
        lines.append(f"| {name} | {item.get('status')} | {item.get('sample_row_count', '')} | {', '.join(item.get('columns', []))} |")
    lines += ["", "No token value is written by this probe. A missing token is reported as BLOCKED_CREDENTIAL; no alternate data source is substituted."]
    (OUT / "capability_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(result["status"])


if __name__ == "__main__":
    main()
