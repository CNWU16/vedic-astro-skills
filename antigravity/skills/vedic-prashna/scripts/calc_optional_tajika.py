#!/usr/bin/env python3
"""Tajika sambandha/contact overlay for Prashna.

This module deliberately implements a sourced subset of the sixteen Tajika yogas.
It does not claim to be a complete Tajika engine and never changes the Parashari
standard-layer verdict.

Implemented:
- Itthasala / Muthashila: the same applying relationship, not two yogas.
- Isharafa / Musharipha: separation after perfection.
- Nakta: transfer of light by a faster third planet.
- Manau: a Mars/Saturn prohibition candidate.
- Kamboola, Khallasara and Radda as modifiers of the primary relationship.

Deferred because the Tajika Nilakanthi definitions or transmission require their own
validated implementation: Ikkavala, Induvara, Yamaya, Gairikamboola,
Duphalikuttha, Dutthotthadivira, Tambira, Kuttha and Durapha.

Sources:
- Tajika Nilakanthi, Samjnatantra, Sodasayogadhyaya.
- M. Gansten and O. Wikander, "Sahl and the Tajika Yogas" (2011).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

_HERE = Path(__file__).resolve().parent
_CALC = _HERE.parent.parent / "vedic-calculator" / "scripts"
if str(_CALC) not in sys.path:
    sys.path.insert(0, str(_CALC))

from engine import calculate_full_chart  # noqa: E402


TAJIKA_PLANETS = ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn")
TAJIKA_ORBS = {
    "Sun": 15.0,
    "Moon": 12.0,
    "Mars": 8.0,
    "Mercury": 7.0,
    "Jupiter": 9.0,
    "Venus": 7.0,
    "Saturn": 9.0,
}

# A sextile, square and trine can perfect on either side of the slower planet.
_ASPECT_BRANCHES = (
    (0.0, 0, "conjunction", "hostile"),
    (60.0, 60, "sextile", "friendly"),
    (300.0, 60, "sextile", "friendly"),
    (90.0, 90, "square", "hostile"),
    (270.0, 90, "square", "hostile"),
    (120.0, 120, "trine", "friendly"),
    (240.0, 120, "trine", "friendly"),
    (180.0, 180, "opposition", "hostile"),
)

_DEFERRED_YOGAS = (
    "Ikkavala",
    "Induvara",
    "Yamaya",
    "Gairikamboola",
    "Duphalikuttha",
    "Dutthotthadivira",
    "Tambira",
    "Kuttha",
    "Durapha",
)


def _normalise_signed(angle: float) -> float:
    return (angle + 180.0) % 360.0 - 180.0


def _pair_key(a: str, b: str) -> tuple[str, str]:
    return tuple(sorted((a, b)))


def _nearest_aspect(relative_longitude: float) -> tuple[float, int, str, str, float]:
    candidates = []
    for branch, canonical, name, quality in _ASPECT_BRANCHES:
        error = _normalise_signed(relative_longitude - branch)
        candidates.append((abs(error), branch, canonical, name, quality, error))
    _, branch, canonical, name, quality, error = min(candidates, key=lambda item: item[0])
    return branch, canonical, name, quality, error


def _contact(planets: dict, a: str, b: str) -> dict | None:
    """Return the nearest in-orb Tajika contact for a pair.

    The trend uses the signed relative speed, so both aspect branches and
    retrograde motion are handled rather than discarded.
    """
    pa, pb = planets[a], planets[b]
    speed_a = float(pa.get("speed", 0.0))
    speed_b = float(pb.get("speed", 0.0))

    if abs(speed_a) >= abs(speed_b):
        faster, slower = a, b
        fast, slow = pa, pb
        fast_speed, slow_speed = speed_a, speed_b
    else:
        faster, slower = b, a
        fast, slow = pb, pa
        fast_speed, slow_speed = speed_b, speed_a

    relative_longitude = (float(fast["longitude"]) - float(slow["longitude"])) % 360.0
    branch, canonical, aspect_name, quality, error = _nearest_aspect(relative_longitude)
    distance = abs(error)
    orb_limit = (TAJIKA_ORBS[faster] + TAJIKA_ORBS[slower]) / 2.0
    if distance > orb_limit:
        return None

    relative_speed = fast_speed - slow_speed
    trend = error * relative_speed
    exact_tolerance = 1.0 / 60.0
    if distance <= exact_tolerance:
        motion_state = "perfected"
        yoga = "itthasala_perfected"
        eta_days = 0.0
    elif trend < -1e-8:
        motion_state = "applying"
        yoga = "itthasala"
        eta_days = -error / relative_speed if abs(relative_speed) > 1e-10 else None
    elif trend > 1e-8:
        motion_state = "separating"
        # Sahl/TNK distinguish the immediate perfected zone from separation
        # after the swifter planet has moved one degree beyond exact.
        yoga = "recent_perfection" if distance < 1.0 else "isharafa"
        eta_days = None
    else:
        motion_state = "stationary_relative"
        yoga = "indeterminate"
        eta_days = None

    return {
        "pair": [a, b],
        "faster": faster,
        "slower": slower,
        "aspect_angle": canonical,
        "aspect_branch": branch,
        "aspect_name": aspect_name,
        "quality": quality,
        "motion_state": motion_state,
        "yoga": yoga,
        "distance_from_exact_deg": round(distance, 6),
        "signed_error_deg": round(error, 6),
        "orb_limit_deg": round(orb_limit, 6),
        "relative_speed_deg_per_day": round(relative_speed, 9),
        "linear_eta_days": round(eta_days, 4) if eta_days is not None and eta_days >= 0 else None,
        "retrograde": {
            a: bool(pa.get("retrograde", speed_a < 0)),
            b: bool(pb.get("retrograde", speed_b < 0)),
        },
    }


def _all_contacts(planets: dict) -> dict[tuple[str, str], dict]:
    available = [planet for planet in TAJIKA_PLANETS if planet in planets]
    contacts: dict[tuple[str, str], dict] = {}
    for index, a in enumerate(available):
        for b in available[index + 1 :]:
            record = _contact(planets, a, b)
            if record:
                contacts[_pair_key(a, b)] = record
    return contacts


def _is_applying(record: dict | None) -> bool:
    return bool(record and record["yoga"] in {"itthasala", "itthasala_perfected"})


def _is_separating(record: dict | None) -> bool:
    return bool(record and record["yoga"] in {"recent_perfection", "isharafa"})


def _nakta_candidates(
    planets: dict,
    contacts: dict[tuple[str, str], dict],
    querent_lord: str,
    matter_lord: str,
    primary: dict | None,
) -> list[dict]:
    # TNK defines Nakta for two significators that lack mutual contact and
    # receive a transfer from a faster third planet. It must not be layered on
    # top of an already present primary sambandha.
    if primary is not None:
        return []

    candidates = []
    q_speed = abs(float(planets[querent_lord].get("speed", 0.0)))
    m_speed = abs(float(planets[matter_lord].get("speed", 0.0)))
    for mediator in TAJIKA_PLANETS:
        if mediator in {querent_lord, matter_lord} or mediator not in planets:
            continue
        mediator_speed = abs(float(planets[mediator].get("speed", 0.0)))
        if mediator_speed <= max(q_speed, m_speed):
            continue
        q_contact = contacts.get(_pair_key(querent_lord, mediator))
        m_contact = contacts.get(_pair_key(matter_lord, mediator))
        if (_is_separating(q_contact) and _is_applying(m_contact)) or (
            _is_separating(m_contact) and _is_applying(q_contact)
        ):
            candidates.append(
                {
                    "mediator": mediator,
                    "querent_contact": q_contact,
                    "matter_contact": m_contact,
                    "source_rule": "TNK-2.25 Nakta: transfer by a faster third planet",
                }
            )
    return candidates


def _manau_candidates(
    contacts: dict[tuple[str, str], dict],
    querent_lord: str,
    matter_lord: str,
    primary: dict | None,
) -> list[dict]:
    candidates = []
    primary_eta = primary.get("linear_eta_days") if primary else None
    for interferer in ("Mars", "Saturn"):
        if interferer in {querent_lord, matter_lord}:
            continue
        q_contact = contacts.get(_pair_key(querent_lord, interferer))
        m_contact = contacts.get(_pair_key(matter_lord, interferer))
        if not q_contact or not m_contact:
            continue
        hostile = [
            record
            for record in (q_contact, m_contact)
            if record["aspect_angle"] in {0, 90, 180}
            and record["yoga"] in {"itthasala", "itthasala_perfected", "recent_perfection"}
        ]
        applying = [record for record in (q_contact, m_contact) if _is_applying(record)]
        if not hostile or not applying:
            continue
        eta_values = [
            record["linear_eta_days"]
            for record in applying
            if record.get("linear_eta_days") is not None
        ]
        interference_eta = min(eta_values) if eta_values else 0.0
        precedes_primary = (
            primary_eta is None
            or interference_eta is None
            or interference_eta <= primary_eta
        )
        if precedes_primary:
            candidates.append(
                {
                    "interferer": interferer,
                    "querent_contact": q_contact,
                    "matter_contact": m_contact,
                    "source_rule": "TNK-2.31–33 Manau: Mars/Saturn prohibition",
                }
            )
    return candidates


def _radda_candidate(chart: dict, contact: dict | None, role: str) -> dict | None:
    if not _is_applying(contact):
        return None

    receiver = contact["slower"]
    planet = chart["planets"][receiver]
    reasons = []
    if planet.get("retrograde", float(planet.get("speed", 0.0)) < 0):
        reasons.append("receiver_retrograde")
    if receiver in chart.get("combustion", {}):
        reasons.append("receiver_combust")
    dignity = chart.get("dignity", {}).get(receiver, {}).get("basic")
    if dignity == "debilitated":
        reasons.append(f"receiver_dignity_{dignity}")
    if not reasons:
        return None
    return {
        "role": role,
        "contact_pair": contact["pair"],
        "receiver": receiver,
        "reasons": reasons,
        "source_rule": "TNK-2.62–63 Radda",
        "scope_note": "Only explicit available debilities are tested; full Tajika strength is deferred.",
    }


def compute(chart: dict, querent_lord: str, matter_lord: str) -> dict:
    """Compute the sourced Tajika contact subset for one primary pair."""
    if querent_lord == matter_lord:
        raise ValueError("querent_lord and matter_lord must be different planets")
    for planet in (querent_lord, matter_lord):
        if planet not in TAJIKA_PLANETS:
            raise ValueError(f"{planet!r} is not a supported Tajika planet")
        if planet not in chart.get("planets", {}):
            raise ValueError(f"{planet!r} is missing from chart data")

    planets = chart["planets"]
    contacts = _all_contacts(planets)
    primary = contacts.get(_pair_key(querent_lord, matter_lord))
    nakta = _nakta_candidates(
        planets,
        contacts,
        querent_lord,
        matter_lord,
        primary,
    )
    manau = _manau_candidates(contacts, querent_lord, matter_lord, primary)

    kamboola_contacts = []
    if "Moon" not in {querent_lord, matter_lord} and _is_applying(primary):
        for target in (querent_lord, matter_lord):
            record = contacts.get(_pair_key("Moon", target))
            if _is_applying(record):
                kamboola_contacts.append(record)

    radda_contacts = [("primary", primary)]
    for index, item in enumerate(nakta, start=1):
        radda_contacts.extend(
            [
                (f"nakta_{index}_querent_leg", item["querent_contact"]),
                (f"nakta_{index}_matter_leg", item["matter_contact"]),
            ]
        )
    for index, item in enumerate(manau, start=1):
        radda_contacts.extend(
            [
                (f"manau_{index}_querent_leg", item["querent_contact"]),
                (f"manau_{index}_matter_leg", item["matter_contact"]),
            ]
        )
    for index, record in enumerate(kamboola_contacts, start=1):
        radda_contacts.append((f"kamboola_{index}", record))

    radda_candidates = []
    seen_radda = set()
    for role, record in radda_contacts:
        candidate = _radda_candidate(chart, record, role)
        if not candidate:
            continue
        key = (
            tuple(sorted(candidate["contact_pair"])),
            candidate["receiver"],
            tuple(candidate["reasons"]),
        )
        if key not in seen_radda:
            seen_radda.add(key)
            radda_candidates.append(candidate)

    moon_relevant_contacts = []
    if "Moon" in planets:
        for planet in TAJIKA_PLANETS:
            if planet == "Moon" or planet not in planets:
                continue
            record = contacts.get(_pair_key("Moon", planet))
            if record and (_is_applying(record) or record["aspect_angle"] == 0):
                moon_relevant_contacts.append(record)

    return {
        "scope": "Tajika sambandha/contact subset; experimental until known-answer suite passes",
        "source_basis": [
            "Tajika Nilakanthi, Samjnatantra 2.15–72",
            "Gansten & Wikander (2011), Sahl and the Tajika Yogas",
        ],
        "primary_pair": {
            "querent_lord": querent_lord,
            "matter_lord": matter_lord,
            "contact": primary,
        },
        "nakta": nakta,
        "manau": manau,
        "kamboola": {
            "present": bool(kamboola_contacts),
            "moon_contacts": kamboola_contacts,
            "source_rule": "TNK-2.36–54 Kamboola",
            "grade": "ungraded",
        },
        "khallasara": {
            "present": not moon_relevant_contacts,
            "moon_contacts": moon_relevant_contacts,
            "source_rule": "TNK-2.61 Khallasara",
            "scope_note": "Tajika-only modifier; never a standard-layer global denial.",
        },
        "radda": {
            "present": bool(radda_candidates),
            "candidates": radda_candidates,
            "source_rule": "TNK-2.62–63 Radda",
        },
        "all_in_orb_contacts": list(contacts.values()),
        "config": {
            "planets": list(TAJIKA_PLANETS),
            "aspects_deg": [0, 60, 90, 120, 180],
            "orbs": TAJIKA_ORBS,
            "pair_orb_formula": "(deeptamsa_A + deeptamsa_B) / 2",
            "nodes": "excluded",
            "retrograde": "included in geometry; evaluated by yoga-specific rules",
        },
        "deferred_yogas": list(_DEFERRED_YOGAS),
        "timing": "disabled",
        "verdict_authority": "none; this overlay does not change the standard-layer verdict",
    }


def _format_contact(record: dict | None) -> str:
    if not record:
        return "无当前 deeptamsha 内接触"
    aliases = {
        "itthasala": "Itthasala / Muthashila（正在应用）",
        "itthasala_perfected": "Itthasala / Muthashila（已精确成相）",
        "recent_perfection": "刚过精确点（尚不足 1°，不直接写作完整 Isharafa）",
        "isharafa": "Isharafa / Musharipha（正在分离）",
        "indeterminate": "相对运动不确定",
    }
    quality = {
        "friendly": "友好相位（较利于顺畅接通）",
        "hostile": "敌意相位（接触存在但带阻力／冲突）",
    }[record["quality"]]
    return (
        f"{record['faster']}–{record['slower']} {record['aspect_name']} "
        f"({record['aspect_angle']}°)，{aliases[record['yoga']]}；{quality}；"
        f"距精确 {record['distance_from_exact_deg']:.3f}° / "
        f"deeptamsha 边界 {record['orb_limit_deg']:.3f}°"
    )


def format_tajika_section(data: dict) -> str:
    primary = data["primary_pair"]
    lines = [
        "# Tajika sambandha/contact overlay",
        "",
        "> 实验副层；只处理经原典核对的接触子集，不冒充完整 16 yoga。",
        "> 与 Parashari 标准结论分离，不改档次；当前不提供 timing。",
        "",
        "## 主星对",
        "",
        f"- 问者星：**{primary['querent_lord']}**",
        f"- 事项星：**{primary['matter_lord']}**",
        f"- 当前关系：{_format_contact(primary['contact'])}",
        "",
        "## 第三星条件",
        "",
    ]
    if data["nakta"]:
        for item in data["nakta"]:
            lines.append(f"- Nakta 候选：**{item['mediator']}** 传光")
    else:
        lines.append("- Nakta：无")
    if data["manau"]:
        for item in data["manau"]:
            lines.append(f"- Manau 候选：**{item['interferer']}** 可能先行阻断")
    else:
        lines.append("- Manau：无")

    lines.extend(
        [
            "",
            "## Moon 与接触修正",
            "",
            f"- Kamboola：{'有候选（未分级）' if data['kamboola']['present'] else '无'}",
            (
                "- Khallasara：有候选；仅表示本 Tajika 副层缺少 Moon 接触，"
                "不得写成标准层空亡或全局不成"
                if data["khallasara"]["present"]
                else "- Khallasara：无"
            ),
            (
                "- Radda："
                + "；".join(
                    f"{'/'.join(item['contact_pair'])} 的接收星 "
                    f"{item['receiver']}：{', '.join(item['reasons'])}"
                    for item in data["radda"]["candidates"]
                )
                if data["radda"]["present"]
                else "- Radda：当前未检出已实现范围内的退回条件"
            ),
            "",
            "## 体系边界",
            "",
            f"- 暂未实现：{', '.join(data['deferred_yogas'])}",
            "- Rahu/Ketu 不参与本副层。",
            "- Timing：未启用。",
            "- 本文件不产生“成／悬／不成”结论。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Tajika contact overlay calculator")
    parser.add_argument("--datetime", required=True, help='"YYYY-MM-DD HH:MM" or "now"')
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)
    parser.add_argument("--tz", required=True)
    parser.add_argument("--querent-lord", required=True, choices=TAJIKA_PLANETS)
    parser.add_argument("--matter-lord", required=True, choices=TAJIKA_PLANETS)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    zone = ZoneInfo(args.tz)
    if args.datetime.strip().lower() == "now":
        dt = datetime.now(zone)
    else:
        dt = datetime.strptime(args.datetime, "%Y-%m-%d %H:%M").replace(tzinfo=zone)
    chart = calculate_full_chart(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, args.lat, args.lon, args.tz
    )
    result = compute(chart, args.querent_lord, args.matter_lord)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_tajika_section(result), end="")


if __name__ == "__main__":
    main()
