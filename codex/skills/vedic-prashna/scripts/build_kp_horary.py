#!/usr/bin/env python3
"""Build an independent KP 1–249 horary artifact."""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

from calc_optional_kp import (
    TOPIC_RULES,
    compute,
    format_kp_judgment,
    format_kp_section,
)
from prashna_time import datetime_slug, parse_local_datetime


LABEL_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,29}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build independent KP 1–249 horary")
    parser.add_argument(
        "--datetime",
        required=True,
        help='"YYYY-MM-DD HH:MM[:SS[.ffffff]]" or "now"',
    )
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)
    parser.add_argument("--tz", required=True)
    parser.add_argument("--number", type=int, required=True)
    parser.add_argument("--topic", choices=tuple(TOPIC_RULES), required=True)
    parser.add_argument("--question", required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--out-parent", default=".")
    args = parser.parse_args()

    if not math.isfinite(args.lat) or not -90.0 <= args.lat <= 90.0:
        parser.error("--lat must be a finite value between -90 and 90")
    if not math.isfinite(args.lon) or not -180.0 <= args.lon <= 180.0:
        parser.error("--lon must be a finite value between -180 and 180")
    if not 1 <= args.number <= 249:
        parser.error("--number must be between 1 and 249")
    if not args.question.strip():
        parser.error("--question must not be blank")
    if not LABEL_RE.match(args.label):
        parser.error(f"--label must match {LABEL_RE.pattern}")
    try:
        args.dt = parse_local_datetime(args.datetime, args.tz)
    except Exception as exc:
        parser.error(str(exc))
    return args


def main() -> None:
    args = parse_args()
    data = compute(
        args.dt,
        args.lat,
        args.lon,
        args.tz,
        args.number,
        args.topic,
    )
    data["question"] = args.question
    out_dir = (
        Path(args.out_parent).expanduser().resolve()
        / f"kp_horary_{datetime_slug(args.dt)}_{args.label}"
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    markdown_path = out_dir / "structured_kp.md"
    json_path = out_dir / "structured_kp.json"
    judgment_path = out_dir / f"kp_judgment_{args.label}.md"
    markdown_path.write_text(format_kp_section(data), encoding="utf-8")
    json_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    judgment_path.write_text(format_kp_judgment(data), encoding="utf-8")
    print(f"[OK] KP horary directory: {out_dir}")
    print(f"     Markdown: {markdown_path.name}")
    print(f"     JSON: {json_path.name}")
    print(f"     Judgment: {judgment_path.name}")


if __name__ == "__main__":
    main()
