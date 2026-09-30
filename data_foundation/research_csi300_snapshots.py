"""Collect BaoStock CSI300 membership snapshots (raw, no PIT interval inference).

This utility deliberately preserves the requested date and BaoStock's updateDate;
it does not forward-fill snapshots or claim effective membership intervals.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import pandas as pd

OUT = Path(__file__).parent / "output"


def month_end_dates(start: str = "2017-12-01", end: str = "2024-03-31") -> list[str]:
    return [d.strftime("%Y-%m-%d") for d in pd.date_range(start, end, freq="ME")]


def snapshot_rows(bs, requested_date: str) -> tuple[pd.DataFrame, str | None]:
    result = bs.query_hs300_stocks(date=requested_date)
    if str(result.error_code) != "0":
        raise RuntimeError(f"query_hs300_stocks({requested_date}) failed: {result.error_msg}")
    frame = result.get_data()
    if frame.empty:
        return frame, None
    required = {"updateDate", "code", "code_name"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"unexpected BaoStock schema; missing {sorted(missing)}")
    update_date = str(frame["updateDate"].iloc[0])
    return frame, update_date


def collect() -> tuple[pd.DataFrame, list[dict]]:
    import baostock as bs

    login = bs.login()
    if str(login.error_code) != "0":
        raise RuntimeError(f"BaoStock login failed: {login.error_msg}")
    records: list[dict] = []
    summary: list[dict] = []
    previous_codes: set[str] | None = None
    try:
        for requested in month_end_dates():
            try:
                frame, update_date = snapshot_rows(bs, requested)
            except RuntimeError as exc:
                # BaoStock public sessions can expire during a long snapshot sweep.
                if "未登录" not in str(exc):
                    raise
                bs.login()
                frame, update_date = snapshot_rows(bs, requested)
            codes = set(frame["code"].astype(str))
            digest = hashlib.sha256("\n".join(sorted(codes)).encode()).hexdigest()
            changed = None if previous_codes is None else len(codes.symmetric_difference(previous_codes))
            summary.append({
                "requested_date": requested,
                "updateDate": update_date or "",
                "constituent_count": len(codes),
                "constituent_hash": digest,
                "changed_constituents_vs_previous": changed,
            })
            for row in frame.itertuples(index=False):
                records.append({
                    "requested_date": requested,
                    "updateDate": update_date or "",
                    "code": str(row.code),
                    "code_name": str(row.code_name),
                })
            previous_codes = codes
    finally:
        bs.logout()
    return pd.DataFrame(records), summary


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    history, summary = collect()
    history_path = OUT / "csi300_snapshot_history.csv"
    history.to_csv(history_path, index=False)
    report = OUT / "csi300_snapshot_analysis.md"
    available = len(summary)
    distinct_hashes = len({x["constituent_hash"] for x in summary})
    updates = len({x["updateDate"] for x in summary if x["updateDate"]})
    lines = [
        "# CSI300 Snapshot Analysis", "",
        "Source: BaoStock `query_hs300_stocks(date=...)`.",
        "The requested date and API `updateDate` are retained as source observations.",
        "No effective_from/effective_to interval is inferred and no snapshot is forward-filled.", "",
        f"- Requested month-end snapshots: {available}",
        f"- Rows in raw history: {len(history)}",
        f"- Distinct constituent hashes: {distinct_hashes}",
        f"- Distinct API updateDate values: {updates}",
        f"- Date range: {summary[0]['requested_date']} .. {summary[-1]['requested_date']}", "",
        "## Observed semantics", "",
        "BaoStock returns a constituent list for each requested date and an `updateDate` (observed as the latest constituent update associated with that query). This is a monthly snapshot observation, not proof of the constituent set's effective trading interval.",
        "", "Status: `SNAPSHOT_BASED_CSI300_RESEARCH_UNIVERSE` / `UNIVERSE_PIT_NOT_VALIDATED`.", "",
        "| requested_date | updateDate | count | changed vs previous | hash |",
        "|---|---|---:|---:|---|",
    ]
    for row in summary:
        lines.append(f"| {row['requested_date']} | {row['updateDate']} | {row['constituent_count']} | {row['changed_constituents_vs_previous'] if row['changed_constituents_vs_previous'] is not None else ''} | `{row['constituent_hash'][:12]}` |")
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {history_path} ({len(history)} rows) and {report}")


if __name__ == "__main__":
    main()
