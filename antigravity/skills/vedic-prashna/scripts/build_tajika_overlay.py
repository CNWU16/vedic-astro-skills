#!/usr/bin/env python3
"""Build a question-specific Tajika overlay after Prashna Phase 2."""
from __future__ import annotations

import argparse
import math
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from calc_optional_tajika import (
    TAJIKA_PLANETS,
    calculate_full_chart,
    compute,
    format_tajika_section,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a Tajika contact overlay for an existing prashna_* directory"
    )
    parser.add_argument("--datetime", required=True, help='"YYYY-MM-DD HH:MM" or "now"')
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)
    parser.add_argument("--tz", required=True)
    parser.add_argument("--querent-lord", required=True, choices=TAJIKA_PLANETS)
    parser.add_argument("--matter-lord", required=True, choices=TAJIKA_PLANETS)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    if not math.isfinite(args.lat) or not -90.0 <= args.lat <= 90.0:
        parser.error("--lat must be a finite value between -90 and 90")
    if not math.isfinite(args.lon) or not -180.0 <= args.lon <= 180.0:
        parser.error("--lon must be a finite value between -180 and 180")

    try:
        zone = ZoneInfo(args.tz)
    except ZoneInfoNotFoundError:
        parser.error(f"--tz is not a valid IANA timezone: {args.tz!r}")

    if args.datetime.strip().lower() == "now":
        args.dt = datetime.now(zone).replace(second=0, microsecond=0)
    else:
        try:
            args.dt = datetime.strptime(args.datetime, "%Y-%m-%d %H:%M").replace(
                tzinfo=zone
            )
        except ValueError:
            parser.error('--datetime must be "YYYY-MM-DD HH:MM" or "now"')

    out_dir = Path(args.out_dir).expanduser().resolve()
    if not out_dir.is_dir() or not out_dir.name.startswith("prashna_"):
        parser.error("--out-dir must be an existing prashna_* directory")
    if not (out_dir / "structured_prashna.md").is_file():
        parser.error("--out-dir must contain structured_prashna.md from the standard builder")
    args.out_dir = out_dir
    return args


def main() -> None:
    args = parse_args()
    chart = calculate_full_chart(
        args.dt.year,
        args.dt.month,
        args.dt.day,
        args.dt.hour,
        args.dt.minute,
        args.lat,
        args.lon,
        args.tz,
    )
    data = compute(chart, args.querent_lord, args.matter_lord)
    output = args.out_dir / "tajika_overlay.md"
    output.write_text(format_tajika_section(data), encoding="utf-8")
    print(f"[OK] Tajika overlay: {output}")


if __name__ == "__main__":
    main()
