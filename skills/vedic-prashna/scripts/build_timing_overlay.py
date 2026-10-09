#!/usr/bin/env python3
"""build_timing_overlay.py — Prashna 时间副层(标准层定档为成/悬后运行)

在已有 prashna_* 目录写 timing_overlay.md，不改 structured_prashna.md 和三档结论。
算法、题型事项宫与边界见 resources/timing-layer.md，纯函数在 calc_timing.py。

隔离：标准 builder 不导入本脚本；本脚本不导入 Tajika/KP。

用法:
    python build_timing_overlay.py \\
        --datetime "2026-07-11 15:30:24" --lat 30.667 --lon 104.067 \\
        --tz "Asia/Shanghai" --matter-house 7 --mode general \\
        --verdict favorable --out-dir prashna_20260711_153024_reunion
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

# --- 复用共享 vedic-calculator(只读) ---
_HERE = Path(__file__).resolve().parent            # vedic-prashna/scripts/
_CALC = _HERE.parent.parent / "vedic-calculator" / "scripts"
if str(_CALC) not in sys.path:
    sys.path.insert(0, str(_CALC))

import engine  # noqa: E402
from calc_timing import (  # noqa: E402
    format_timing_section,
    jd_to_local,
    next_sign_entry,
    t1_return_days,
    t2_house_lord_count,
    t4_navamsa_lord_period,
)
from prashna_time import (  # noqa: E402
    calculate_prashna_chart,
    format_wall_time,
    local_datetime_to_jd,
    parse_local_datetime,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the Prashna timing overlay for an existing prashna_* directory"
    )
    parser.add_argument(
        "--datetime",
        required=True,
        help='"YYYY-MM-DD HH:MM[:SS[.ffffff]]" or "now"',
    )
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)
    parser.add_argument("--tz", required=True)
    parser.add_argument(
        "--matter-house", type=int, required=True, choices=range(1, 13),
        help="题型事项宫，见 resources/timing-layer.md",
    )
    parser.add_argument(
        "--mode", choices=("general", "return"), default="general",
        help="return=人的归来/到达题(T1 为主时间)；其余 general(T2 为主时间)",
    )
    parser.add_argument(
        "--verdict", required=True, choices=("favorable", "pending"),
        help="标准层结论档：favorable=成，pending=悬；不成档不运行本脚本",
    )
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    if not math.isfinite(args.lat) or not -90.0 <= args.lat <= 90.0:
        parser.error("--lat must be a finite value between -90 and 90")
    if not math.isfinite(args.lon) or not -180.0 <= args.lon <= 180.0:
        parser.error("--lon must be a finite value between -180 and 180")

    try:
        args.dt = parse_local_datetime(args.datetime, args.tz)
    except Exception as exc:
        parser.error(str(exc))

    out_dir = Path(args.out_dir).expanduser().resolve()
    if not out_dir.is_dir() or not out_dir.name.startswith("prashna_"):
        parser.error("--out-dir must be an existing prashna_* directory")
    if not (out_dir / "structured_prashna.md").is_file():
        parser.error("--out-dir must contain structured_prashna.md from the standard builder")
    args.out_dir = out_dir
    return args


def main() -> None:
    args = parse_args()
    chart = calculate_prashna_chart(args.dt, args.lat, args.lon, args.tz)
    planets = chart["planets"]

    if args.mode == "return":
        primary = t1_return_days({n: p["house"] for n, p in planets.items()})
    else:
        lord = chart["house_lords"][args.matter_house]["lord"]
        primary = t2_house_lord_count(args.matter_house, lord, planets[lord]["house"])

    # T3：事项宫主所在星座；Moon 用 engine 同一套 flags 逐点计算。
    # 宫主就是 Moon 时"Moon 进入 Moon 所在座"自指，不取。
    matter_lord = chart["house_lords"][args.matter_house]["lord"]
    t3 = None
    if matter_lord != "Moon":
        target_sign_idx = planets[matter_lord]["sign_idx"]
        moon_id = engine.PLANETS_SWE["Moon"]
        jd = local_datetime_to_jd(args.dt, args.tz)
        entry_jd = next_sign_entry(
            lambda j: engine.calc_planet(j, moon_id)["longitude"], jd, target_sign_idx
        )
        t3 = {
            "rule_id": "M-XIV.85",
            "lord": matter_lord,
            "sign": engine.SIGNS[target_sign_idx],
            "already_in": planets["Moon"]["sign_idx"] == target_sign_idx,
            "local_time": jd_to_local(entry_jd, args.tz).strftime("%Y-%m-%d %H:%M"),
        }

    d9_lagna = chart["divisional_charts"]["D9"]["Lagna"]
    d9_lord = engine.SIGN_LORDS[d9_lagna["sign_idx"]]
    t4 = t4_navamsa_lord_period(d9_lord, planets[d9_lord]["degree"])
    t4["navamsa_sign"] = d9_lagna["sign"]

    data = {
        "verdict": args.verdict,
        "primary": primary,
        "t3": t3,
        "t4": t4,
        "judgment_time": f"{args.dt.strftime('%Y-%m-%d')} {format_wall_time(args.dt)}",
        "judgment_timezone": args.tz,
    }
    output = args.out_dir / "timing_overlay.md"
    output.write_text(format_timing_section(data), encoding="utf-8")
    print(f"[OK] Timing overlay: {output}")


if __name__ == "__main__":
    main()
