#!/usr/bin/env python3
"""calc_timing.py — Prashna 时间副层纯函数(沙箱内，只依赖标准库)

四个原典时间候选，来源、适用题型与边界见 resources/timing-layer.md：

  T1  P-V.5     归来/到达题：Lagna 顺数到第一个有七曜的宫(Lagna 有星=1)，宫数 × 12 天
  T2  M-XIV.85  事项宫数到其宫主所在宫(含首尾)；宫主在 7–12 宫按天、1–6 宫按月
                (天/月分法是 Raman 注的假设，原文未定)
  T3  M-XIV.85  Moon 下次进入事项宫主所在星座
  T4  M-XIV.82  上升 Navamsa 主星的时间单位(XIV.81) × 该星在本座第几个 Navamsa，只作参考

本模块不导入 engine、Tajika 或 KP；行星数据由 build_timing_overlay.py 传入。
不生成成败结论；几个候选结果不同时并列，不平均、不投票。
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo


SEVEN_GRAHAS = ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn")
NAVAMSA_SPAN = 30.0 / 9.0

# M-XIV.81 Raman 注引 Brihat Jataka：(每单位数量, 单位, 原名)
PERIOD_UNITS = {
    "Sun": (6, "个月", "Ayana"),
    "Moon": (48, "分钟", "Kshana"),
    "Mars": (1, "周", "Vasara"),
    "Mercury": (2, "个月", "Rithu"),
    "Jupiter": (1, "个月", "Masa"),
    "Venus": (0.5, "个月", "Ardha"),
    "Saturn": (1, "年", "Sama"),
}

VERDICT_PREFIX = {"favorable": "约", "pending": "如果能成，大约"}

_J2000 = 2451545.0
_J2000_UTC = datetime(2000, 1, 1, 12, tzinfo=timezone.utc)


# ---------------------------------------------------------------------------
# T1–T4
# ---------------------------------------------------------------------------
def t1_return_days(planet_houses: dict) -> dict:
    """P-V.5：Lagna 顺数到第一个有七曜的宫，宫数 × 12 天。Rahu/Ketu 不计。"""
    for count in range(1, 13):
        names = [n for n in SEVEN_GRAHAS if planet_houses.get(n) == count]
        if names:
            return {
                "rule_id": "P-V.5",
                "count": count,
                "planets": names,
                "days": count * 12,
            }
    raise ValueError("七曜未落任何宫：planet_houses 缺数据")


def t2_house_lord_count(matter_house: int, lord: str, lord_house: int) -> dict:
    """M-XIV.85：事项宫数到宫主所在宫，含首尾。"""
    visible = lord_house >= 7
    return {
        "rule_id": "M-XIV.85",
        "matter_house": matter_house,
        "lord": lord,
        "lord_house": lord_house,
        "count": ((lord_house - matter_house) % 12) + 1,
        "unit": "天" if visible else "个月",
        "hemisphere": "可见半球(7–12 宫)" if visible else "不可见半球(1–6 宫)",
        "pace": "较快" if visible else "较慢",
    }


def navamsa_ordinal(degree_in_sign: float) -> int:
    """行星在本座第几个 Navamsa(1–9)。"""
    return min(int(degree_in_sign / NAVAMSA_SPAN), 8) + 1


def t4_navamsa_lord_period(lord: str, lord_degree_in_sign: float) -> dict:
    """M-XIV.82：上升 Navamsa 主星的单位 × 该星在本座第几个 Navamsa。"""
    ordinal = navamsa_ordinal(lord_degree_in_sign)
    amount, unit, name = PERIOD_UNITS[lord]
    return {
        "rule_id": "M-XIV.82",
        "lord": lord,
        "navamsa_ordinal": ordinal,
        "unit_name": name,
        "per_unit": amount,
        "unit": unit,
        "value": ordinal * amount,
    }


def next_sign_entry(
    longitude_at,
    jd_start: float,
    target_sign_idx: int,
    step_days: float = 0.25,
    max_days: float = 32.0,
    tolerance_days: float = 1.0 / 86400.0,
) -> float:
    """M-XIV.85 T3：Moon 下次进入 target sign 的 JD(UT)。

    longitude_at(jd) 返回恒星黄经。步长 0.25 天(Moon 约 3.3°)小于一个星座，
    不会跳座；找到进入区间后二分到 1 秒。提问时已在该座的，返回下一次重新进入。
    """
    def in_target(jd):
        return int((longitude_at(jd) % 360.0) / 30.0) == target_sign_idx

    prev_jd, prev_in = jd_start, in_target(jd_start)
    while prev_jd - jd_start < max_days:
        jd = prev_jd + step_days
        now_in = in_target(jd)
        if now_in and not prev_in:
            lo, hi = prev_jd, jd
            while hi - lo > tolerance_days:
                mid = (lo + hi) / 2.0
                if in_target(mid):
                    hi = mid
                else:
                    lo = mid
            return hi
        prev_jd, prev_in = jd, now_in
    raise ValueError(f"{max_days} 天内未找到进入 sign_idx={target_sign_idx}")


def jd_to_local(jd: float, tz: str) -> datetime:
    """JD(UT) → 提问地本地时间，取整到秒。"""
    utc = _J2000_UTC + timedelta(days=jd - _J2000)
    return (utc + timedelta(microseconds=500_000)).replace(microsecond=0).astimezone(ZoneInfo(tz))


# ---------------------------------------------------------------------------
# 格式化为 timing_overlay.md
# ---------------------------------------------------------------------------
def _fmt_number(value) -> str:
    return f"{value:g}"


def format_timing_section(data: dict) -> str:
    prefix = VERDICT_PREFIX[data["verdict"]]
    primary = data["primary"]
    t3 = data["t3"]
    t4 = data["t4"]

    if primary["rule_id"] == "P-V.5":
        primary_text = f"{prefix} {primary['days']} 天后回来/到达"
    else:
        primary_text = (
            f"{prefix} {primary['count']} {primary['unit']}内应事"
            f"（应事节奏{primary['pace']}）"
        )
    t4_text = f"{_fmt_number(t4['value'])} {t4['unit']}"
    if t4["lord"] == "Moon":
        t4_text += "（Moon 单位是 48 分钟，对需要过程的事项通常过短）"

    lines = ["# 时间副层（timing overlay）\n"]
    lines.append(f"> 提问时刻：{data['judgment_time']}（{data['judgment_timezone']}）")
    lines.append(f"> 标准层结论档：{'成' if data['verdict'] == 'favorable' else '悬'}"
                 "；本文件不改该结论\n")

    lines.append("## 先说人话\n")
    lines.append(f"- **主时间**：{primary_text}。")
    if t3:
        lines.append(f"- **最近的触发日**：{t3['local_time']} 前后。")
    lines.append(f"- **参考**：另一条算法给出 {t4_text}，只作参考。")
    lines.append("- 几条算法来自不同原典口径，结果不同时并列，不取平均。\n")

    lines.append("## 计算明细\n")
    lines.append("| 候选 | rule_id | 输入 | 结果 | 角色 |")
    lines.append("|---|---|---|---|---|")
    if primary["rule_id"] == "P-V.5":
        lines.append(
            f"| T1 | P-V.5 | Lagna 顺数到第一个有七曜的宫：{primary['count']} 宫"
            f"（{'、'.join(primary['planets'])}） | {primary['count']} × 12 = "
            f"{primary['days']} 天 | 主时间（归来/到达题） |"
        )
    else:
        lines.append(
            f"| T2 | M-XIV.85 | {primary['matter_house']} 宫主 {primary['lord']} 在 "
            f"{primary['lord_house']} 宫，{primary['hemisphere']}；含首尾 "
            f"{primary['count']} 宫 | {primary['count']} {primary['unit']}，"
            f"节奏{primary['pace']} | 主时间 |"
        )
    if t3:
        already = "；提问时 Moon 已在该座，取下一次重新进入" if t3["already_in"] else ""
        lines.append(
            f"| T3 | M-XIV.85 | Moon 下次进入 {t3['lord']} 所在 {t3['sign']}{already} | "
            f"{t3['local_time']} | 触发日 |"
        )
    else:
        lines.append(
            "| T3 | M-XIV.85 | 事项宫主就是 Moon，“Moon 进入宫主所在座”自指 | 不适用 | — |"
        )
    lines.append(
        f"| T4 | M-XIV.82 | 上升 Navamsa {t4['navamsa_sign']}，主星 {t4['lord']} 在本座第 "
        f"{t4['navamsa_ordinal']} 个 Navamsa；单位 {t4['unit_name']} = "
        f"{_fmt_number(t4['per_unit'])} {t4['unit']} | {t4['navamsa_ordinal']} × "
        f"{_fmt_number(t4['per_unit'])} = {t4_text} | 参考 |"
    )
    lines.append("")

    lines.append("## 边界\n")
    lines.append("- 只在标准层结论为成或悬时运行；不成档不给时间。")
    lines.append("- T2 的天/月分法是 Raman 注的假设（原文只说可见半球快、不可见半球慢）。")
    lines.append("- T4 只作参考，不与主时间折中。")
    lines.append(
        "- 不使用提问盘的 120 年 Vimshottari、Chara Dasha、过运；"
        "不导入 Tajika 或 KP 的时间。"
    )
    return "\n".join(lines) + "\n"
