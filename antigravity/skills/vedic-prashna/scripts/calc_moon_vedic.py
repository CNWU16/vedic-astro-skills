#!/usr/bin/env python3
"""calc_moon_vedic.py — Prashna Moon 吠陀动向计算(沙箱内)

计算默认标准层需要的三块 Moon 当前事实(整宫 Parashari 口径，无 orb)：
- moon_position: Moon 当前落点与月宿位置
- moon_contacts: 当前整宫合宫与 Graha Drishti 接触
- moon_strength_factors: 月相与 D1 尊贵度等已知强弱事实

本脚本不输出成败结论或事件时间窗。Moon 当前无直接接触不能被命名为“空亡”，
也不能独立触发全局拒绝。月宿主只作描述／题意软验证候选，不是固定 significator。

沙箱化硬约束(vedic-prashna/SKILL.md §沙箱化硬约束):
- 本脚本只存在于 vedic-prashna/scripts/，绝不下沉共享 vedic-calculator/scripts/engine.py。
- 只读复用共享 engine 的 calculate_full_chart/get_house 等基础工具。
- 输出仅由 build_prashna_data.py 追加到 prashna_*/structured_prashna.md。

对应 SKILL.md §主判读方法论 · Step 3 消费入口。
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

# --- 复用共享 vedic-calculator(只读) ---
_HERE = Path(__file__).resolve().parent            # vedic-prashna/scripts/
_CALC = _HERE.parent.parent / "vedic-calculator" / "scripts"
if str(_CALC) not in sys.path:
    sys.path.insert(0, str(_CALC))

# 导入 engine 会顺带 set_sid_mode(SIDM_TRUE_CITRA)，与主排盘一致
from engine import (                                # noqa: E402
    calculate_full_chart, get_house,
)


# Prashna Moon 判读用 SPECIAL_DRISHTI(承 engine.calc_graha_drishti 口径)
SPECIAL_DRISHTI = {'Mars': [4, 8], 'Jupiter': [5, 9], 'Saturn': [3, 10]}
DRISHTI_PLANETS = [
    'Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'
]


# ---------------------------------------------------------------------------
# 接触判定(整宫落点 + Graha Drishti，禁 orb)
# ---------------------------------------------------------------------------
def _planets_aspecting_sign(planets, lagna_sign_idx, target_sign_idx):
    """哪些行星通过 graha drishti 触及 target sign(不含 Moon 本身、不含合宫)。"""
    target_house = get_house(target_sign_idx, lagna_sign_idx)
    hits = []
    for name in DRISHTI_PLANETS:
        p = planets.get(name)
        if not p or name == 'Moon':
            continue
        src_house = p['house']
        angles = [7] + SPECIAL_DRISHTI.get(name, [])
        for a in angles:
            if ((src_house - 1 + (a - 1)) % 12) + 1 == target_house:
                hits.append({
                    'planet': name, 'from_sign': p['sign'],
                    'from_house': src_house, 'aspect_angle': a,
                })
                break
    return hits


def _planets_colocated_with(planets, target_sign_idx):
    """与 target sign 合宫的行星(不含 Moon 本身)。"""
    hits = []
    for name in DRISHTI_PLANETS:
        p = planets.get(name)
        if not p or name == 'Moon':
            continue
        if p['sign_idx'] == target_sign_idx:
            hits.append({'planet': name, 'sign': p['sign'], 'house': p['house']})
    return hits


# ---------------------------------------------------------------------------
# 核心 compute
# ---------------------------------------------------------------------------
def compute(chart, dt_local, tz_str):
    """给定 chart(engine 返回) + 提问 datetime + tz，输出 Moon 观察数据。"""
    moon = chart['planets']['Moon']
    planets = chart['planets']
    lagna_sign_idx = chart['lagna']['sign_idx']
    moon_sign_idx = moon['sign_idx']
    moon_house = moon['house']
    moon_nak = moon['nakshatra']

    # ---- Moon 当前接触：只记录事实，不在计算层生成成败结论 ----
    conj = _planets_colocated_with(planets, moon_sign_idx)
    aspecting = _planets_aspecting_sign(planets, lagna_sign_idx, moon_sign_idx)

    moon_position = {
        'moon_sign': moon['sign'],
        'moon_nakshatra': moon_nak['name'],
        'moon_pada': moon_nak['pada'],
        'moon_nakshatra_lord': moon_nak['lord'],
        'moon_house': moon_house,
    }
    moon_contacts = {
        'conjunctions': conj,
        'graha_drishti_planets': [h['planet'] for h in aspecting],
        'graha_drishti_details': aspecting,
    }
    moon_strength_factors = {
        'paksha': chart.get('moon_phase', {}),
        'dignity': chart.get('dignity', {}).get('Moon', {}),
        'house': moon_house,
    }

    return {
        'moon_position': moon_position,
        'moon_contacts': moon_contacts,
        'moon_strength_factors': moon_strength_factors,
    }


# ---------------------------------------------------------------------------
# 格式化为 markdown 段(供 build_prashna_data.py 追加到 structured_prashna.md)
# ---------------------------------------------------------------------------
def format_moon_section(moon_data):
    position = moon_data['moon_position']
    contacts = moon_data['moon_contacts']
    strength = moon_data['moon_strength_factors']
    lines = []

    lines.append("## Moon 当前事实（默认标准层输入）\n")

    lines.append("### Moon 当前落点与强弱事实\n")
    lines.append("```")
    lines.append(
        f"Moon 当前: {position['moon_sign']} · "
        f"{position['moon_nakshatra']}(pada {position['moon_pada']}) · "
        f"宫 {position['moon_house']}"
    )
    lines.append(
        f"Nakshatra 主: {position['moon_nakshatra_lord']}"
        "（只作描述／题意软验证候选，不是固定 significator）"
    )
    phase = strength.get('paksha', {})
    dignity = strength.get('dignity', {})
    phase_text = "waxing" if phase.get('waxing') else "waning"
    lines.append(
        f"月相: {phase_text} · Sun–Moon 距离 "
        f"{phase.get('sun_moon_diff', 'n/a')}°"
    )
    lines.append(
        f"D1 尊贵度: basic={dignity.get('basic', 'n/a')} · "
        f"compound={dignity.get('compound', 'n/a')}"
    )
    lines.append("```\n")

    lines.append("**当前接触集合**（吠陀口径：整宫合宫 + Graha Drishti 触及，无 orb）\n")
    if contacts['conjunctions']:
        for c in contacts['conjunctions']:
            lines.append(f"- 合宫: **{c['planet']}** (同 sign, 宫 {c['house']})")
    else:
        lines.append("- 合宫: 无")
    if contacts['graha_drishti_details']:
        for a in contacts['graha_drishti_details']:
            lines.append(f"- Graha Drishti: **{a['planet']}** (from 宫 {a['from_house']}, {a['aspect_angle']}th 相位)")
    else:
        lines.append("- Graha Drishti 触及: 无")
    lines.append("")

    if not contacts['conjunctions'] and not contacts['graha_drishti_details']:
        lines.append(
            "> **判读边界**：当前无直接接触不单独决定成败；"
            "必须回到本题适用的题目规则与事项宫／宫主证据综合判断。\n"
        )
    else:
        lines.append(
            "> **判读边界**：接触只说明 Moon 当前获得哪些行星连接；"
            "是否有题目意义取决于适用规则，不独立定成败。\n"
        )

    lines.append("### 判读时消费入口\n")
    lines.append(
        "详细语义映射见 `resources/moon-policy.md`。默认层不计算 Moon ingress，"
        "也不由 Moon 当前事实生成事件时间窗。\n"
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI(独立 demo，可用于快速核对某个提问盘的 Moon 动向)
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Prashna Moon 吠陀动向独立 CLI")
    ap.add_argument("--datetime", required=True, help='"YYYY-MM-DD HH:MM" 或 "now"')
    ap.add_argument("--lat", type=float, required=True)
    ap.add_argument("--lon", type=float, required=True)
    ap.add_argument("--tz", required=True)
    ap.add_argument("--json", action="store_true", help="输出 JSON 而非 markdown")
    args = ap.parse_args()

    try:
        local_zone = ZoneInfo(args.tz)
    except ZoneInfoNotFoundError:
        ap.error(f"--tz 不是可用的 IANA 时区: {args.tz!r}")
    dt = (
        datetime.now(local_zone).replace(tzinfo=None)
        if args.datetime.strip().lower() == "now"
        else datetime.strptime(args.datetime, "%Y-%m-%d %H:%M")
    )

    chart = calculate_full_chart(dt.year, dt.month, dt.day, dt.hour, dt.minute,
                                 args.lat, args.lon, args.tz)
    data = compute(chart, dt, args.tz)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(format_moon_section(data))


if __name__ == "__main__":
    main()
