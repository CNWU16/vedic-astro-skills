#!/usr/bin/env python3
"""Second-precise time handling for the isolated Prashna stacks.

提问时刻（含秒、微秒）整个传给共享 engine：engine 只本地化一次，D1、各分盘、SAV、
Dasha 等全部出自同一个计算瞬间。本模块不再自己按秒补算一部分字段——那种做法让同一张
盘混用整分与秒级两个瞬间（2026-10-21 起六分盘表约 5% 的盘因此被隐藏）。
本模块只负责解析输入、秒级显示与 JD 换算。
"""
from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

import pytz

import engine


DATETIME_FORMATS = (
    "%Y-%m-%d %H:%M:%S.%f",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
)


def parse_local_datetime(value: str, timezone: str) -> datetime:
    """Parse a wall-clock time without discarding seconds or microseconds."""
    zone = ZoneInfo(timezone)
    if value.strip().lower() == "now":
        return datetime.now(zone)

    for fmt in DATETIME_FORMATS:
        try:
            naive = datetime.strptime(value, fmt)
            # Validate ambiguous/nonexistent local times with the same strict
            # policy used by the shared engine.
            pytz.timezone(timezone).localize(naive, is_dst=None)
            return naive.replace(tzinfo=zone)
        except ValueError:
            continue
    raise ValueError(
        '--datetime must be "YYYY-MM-DD HH:MM[:SS[.ffffff]]" or "now"'
    )


def _seconds(dt_local: datetime) -> float:
    return dt_local.second + dt_local.microsecond / 1_000_000


def _fold(dt_local: datetime):
    """带时区的已知瞬间传 fold（夏令时回拨时消歧）；无时区的手填时刻不传，歧义照旧报错。"""
    return dt_local.fold if dt_local.tzinfo is not None else None


def local_datetime_to_jd(dt_local: datetime, timezone: str) -> float:
    """Convert a local aware/naive datetime to Julian day with full precision."""
    instant = engine.local_instant(
        dt_local.year, dt_local.month, dt_local.day, dt_local.hour, dt_local.minute,
        timezone, _seconds(dt_local), fold=_fold(dt_local),
    )
    return engine.instant_to_jd(instant)


def format_wall_time(dt_local: datetime) -> str:
    """Render seconds and retain supplied fractional precision."""
    base = dt_local.strftime("%H:%M:%S")
    if not dt_local.microsecond:
        return base
    fraction = f"{dt_local.microsecond:06d}".rstrip("0")
    return f"{base}.{fraction}"


def datetime_slug(dt_local: datetime) -> str:
    """Stable directory timestamp; one-second resolution prevents collisions."""
    return dt_local.strftime("%Y%m%d_%H%M%S")


def _format_degree(longitude: float) -> str:
    degree = longitude % 30.0
    whole = int(degree)
    minute_float = (degree - whole) * 60.0
    minute = int(minute_float)
    second = (minute_float - minute) * 60.0
    return f"{whole}°{minute:02d}'{second:04.1f}\""


def calculate_prashna_chart(
    dt_local: datetime,
    latitude: float,
    longitude: float,
    timezone: str,
) -> dict:
    """Return the shared chart computed at the exact (second-precise) question instant."""
    chart = engine.calculate_full_chart(
        dt_local.year,
        dt_local.month,
        dt_local.day,
        dt_local.hour,
        dt_local.minute,
        latitude,
        longitude,
        timezone,
        second=_seconds(dt_local),
        fold=_fold(dt_local),
    )
    # 只改显示：Prashna 宫表按秒显示度数；经度本身就是 engine 的同一瞬间结果。
    chart["lagna"]["deg_str"] = _format_degree(chart["lagna"]["longitude"])
    for record in chart["planets"].values():
        record["deg_str"] = _format_degree(record["longitude"])
    chart["prashna_input_precision"] = {
        "datetime": dt_local.isoformat(),
        "seconds_preserved": True,
    }
    return chart
