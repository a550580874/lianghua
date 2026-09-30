"""Align signal-date factors with Alphalens' entry-date convention."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from pandas.tseries.offsets import CustomBusinessDay


def split_dates(frame: pd.DataFrame, start: str, end: str) -> pd.DatetimeIndex:
    return pd.DatetimeIndex(sorted(frame.loc[frame["datetime"].between(start, end), "datetime"].dropna().unique()))


def aligned_inputs(frame: pd.DataFrame, factor: str, start: str, end: str, horizon: int) -> tuple[pd.Series, pd.DataFrame, pd.DataFrame]:
    """Return (factor at entry date, prices, signal rows) for one split/horizon."""
    dates = split_dates(frame, start, end)
    positions = {date: index for index, date in enumerate(dates)}
    signal = frame[frame["datetime"].isin(dates)].copy()
    signal["_position"] = signal["datetime"].map(positions)
    signal = signal[signal["_position"] + 1 + horizon < len(dates)].copy()
    signal["entry_date"] = signal["datetime"].map(lambda date: dates[positions[date] + 1])
    signal["exit_date"] = signal["datetime"].map(lambda date: dates[positions[date] + 1 + horizon])
    signal = signal.dropna(subset=[factor, "close"])
    factor_series = signal.set_index(["entry_date", "instrument"])[factor].sort_index()
    prices = frame[frame["datetime"].isin(dates)].pivot(index="datetime", columns="instrument", values="close").sort_index()
    # Alphalens assigns a frequency to its date MultiIndex. Preserve the
    # observed trading calendar by representing missing weekdays as holidays;
    # this avoids treating a calendar day as a synthetic trading session.
    weekdays = pd.date_range(dates.min(), dates.max(), freq="B")
    holidays = weekdays.difference(dates)
    calendar = pd.date_range(dates.min(), dates.max(), freq=CustomBusinessDay(holidays=holidays))
    prices = prices.reindex(calendar)
    # Alphalens assigns the inferred calendar frequency to the factor date
    # level. Include the complete observed calendar (with NaN factor rows) so
    # holiday gaps do not make that assignment invalid; clean_factor drops
    # those NaNs before analysis.
    assets = pd.Index(sorted(signal["instrument"].unique()), name="instrument")
    full_index = pd.MultiIndex.from_product([calendar, assets], names=["entry_date", "instrument"])
    factor_series = factor_series.reindex(full_index)
    return factor_series, prices, signal


def build_prices_from_csv(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path, compression="gzip", parse_dates=["datetime"])
    return frame
