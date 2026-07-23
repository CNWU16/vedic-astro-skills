#!/usr/bin/env python3
"""Independent KP horary data engine using the classical 1–249 mode.

The module is intentionally separate from the Parashari Prashna builder. It uses:
- Krishnamurti ayanamsa;
- a 1–249 querent number to set the nirayana Ascendant;
- Placidus cusps derived from that Ascendant and the judgment-place latitude;
- planets at the judgment time;
- the KP significator order documented in K.S. Krishnamurti's Readers;
- question-specific house groups rather than a blanket 6/8/12 rule.

Timing remains disabled until an independent Dasha/Ruling-Planet/transit suite has
published-reference tests.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

_HERE = Path(__file__).resolve().parent
_CALC = _HERE.parent.parent / "vedic-calculator" / "scripts"
if str(_CALC) not in sys.path:
    sys.path.insert(0, str(_CALC))

from engine import (  # noqa: E402
    DASHA_ORDER,
    DASHA_YEARS,
    NAKSHATRAS,
    SIGNS,
    to_jd,
)
import swisseph as swe  # noqa: E402


NAK_SPAN = 360.0 / 27.0
TOTAL_YEARS = float(sum(DASHA_YEARS.values()))
PLANET_IDS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
}
SEVEN_PLANETS = tuple(PLANET_IDS)
NODES = ("Rahu", "Ketu")
ALL_KP_PLANETS = SEVEN_PLANETS + NODES
SIGN_LORDS = {
    "Aries": "Mars",
    "Taurus": "Venus",
    "Gemini": "Mercury",
    "Cancer": "Moon",
    "Leo": "Sun",
    "Virgo": "Mercury",
    "Libra": "Venus",
    "Scorpio": "Mars",
    "Sagittarius": "Jupiter",
    "Capricorn": "Saturn",
    "Aquarius": "Saturn",
    "Pisces": "Jupiter",
}
WEEKDAY_LORDS = {
    0: "Moon",
    1: "Mars",
    2: "Mercury",
    3: "Jupiter",
    4: "Venus",
    5: "Saturn",
    6: "Sun",
}
WEEKDAY_NAMES = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}

# Reader VI explicitly excludes Rahu and Ketu from the horary retrograde
# rejection rule. Their normal zodiacal motion is opposite to that of the
# seven visible planets; it is not treated as a temporary retrograde station.
RETROGRADE_FILTER_PLANETS = frozenset(
    {"Mars", "Mercury", "Jupiter", "Venus", "Saturn"}
)

TOPIC_RULES = {
    "love-materialization": {
        "judgment_cusp": 5,
        "positive_houses": (7, 11),
        "negative_houses": (6, 12),
        "source": (
            "KSK Reader VI, 'Will my Love Affairs Materialise?': "
            "5th cusp sub-lord's star lord; 7/11 promise, 6/12 deny"
        ),
    },
    "business-partnership-continuity": {
        "judgment_cusp": 7,
        "positive_houses": (5, 11),
        "negative_houses": (6, 12),
        "source": (
            "KSK Reader VI, number 156 'Business and Partnership': "
            "7th cusp sub-lord; 5/11 continue, 6/12 break"
        ),
    },
}

_SIGN_BOUNDARIES = tuple(index * 30.0 for index in range(12))
_STAR_BOUNDARIES = tuple(index * NAK_SPAN for index in range(27))
SIGNIFICATOR_LEVEL_RANK = {
    "A_star_of_occupant": 1,
    "A_star_of_node_agent": 1,
    "B_occupant": 2,
    "C_star_of_owner": 3,
    "D_owner": 4,
}


def _normalise_signed(angle: float) -> float:
    return (angle + 180.0) % 360.0 - 180.0


def _circular_distance(a: float, b: float) -> float:
    return abs(_normalise_signed(a - b))


def _sign_of(longitude: float) -> str:
    return SIGNS[int((longitude % 360.0) / 30.0) % 12]


def _sign_lord(longitude: float) -> str:
    return SIGN_LORDS[_sign_of(longitude)]


def _star_index(longitude: float) -> int:
    return min(26, int((longitude % 360.0) / NAK_SPAN))


def _star_lord(longitude: float) -> str:
    return NAKSHATRAS[_star_index(longitude)][1]


def _sub_boundaries() -> tuple[float, ...]:
    boundaries = []
    for nak_index, (_, star_lord) in enumerate(NAKSHATRAS):
        current = nak_index * NAK_SPAN
        boundaries.append(current)
        start_index = DASHA_ORDER.index(star_lord)
        for offset in range(9):
            lord = DASHA_ORDER[(start_index + offset) % 9]
            current += NAK_SPAN * DASHA_YEARS[lord] / TOTAL_YEARS
            boundaries.append(current % 360.0)
    return tuple(sorted(set(round(value % 360.0, 12) for value in boundaries)))


_SUB_BOUNDARIES = _sub_boundaries()


def _sub_lord(longitude: float) -> str:
    longitude %= 360.0
    nak_index = _star_index(longitude)
    star_lord = NAKSHATRAS[nak_index][1]
    offset_in_nak = longitude - nak_index * NAK_SPAN
    start_index = DASHA_ORDER.index(star_lord)
    cumulative = 0.0
    for offset in range(9):
        lord = DASHA_ORDER[(start_index + offset) % 9]
        span = NAK_SPAN * DASHA_YEARS[lord] / TOTAL_YEARS
        if offset_in_nak < cumulative + span - 1e-10:
            return lord
        cumulative += span
    return DASHA_ORDER[(start_index + 8) % 9]


def _distance_to_boundaries(longitude: float, boundaries: tuple[float, ...]) -> float:
    return min(_circular_distance(longitude, boundary) for boundary in boundaries)


def _format_degree(longitude: float) -> str:
    within_sign = longitude % 30.0
    degree = int(within_sign)
    minutes_float = (within_sign - degree) * 60.0
    minute = int(minutes_float)
    second = int(round((minutes_float - minute) * 60.0))
    if second == 60:
        second = 0
        minute += 1
    if minute == 60:
        minute = 0
        degree += 1
    return f"{degree}°{minute:02d}'{second:02d}\""


def build_number_table() -> list[dict]:
    """Build the 249 sign/star/sub segments described in Reader III/VI."""
    segments = []
    for nak_index, (nak_name, star_lord) in enumerate(NAKSHATRAS):
        current = nak_index * NAK_SPAN
        start_index = DASHA_ORDER.index(star_lord)
        for offset in range(9):
            sub_lord = DASHA_ORDER[(start_index + offset) % 9]
            sub_end = current + NAK_SPAN * DASHA_YEARS[sub_lord] / TOTAL_YEARS
            split_points = [current]
            sign_boundary = (math.floor(current / 30.0) + 1) * 30.0
            while sign_boundary < sub_end - 1e-10:
                split_points.append(sign_boundary)
                sign_boundary += 30.0
            split_points.append(sub_end)
            for start, end in zip(split_points, split_points[1:]):
                segments.append(
                    {
                        "number": len(segments) + 1,
                        "start_lon": start % 360.0,
                        "end_lon": end % 360.0 if end < 360.0 else 360.0,
                        "sign": _sign_of(start),
                        "sign_lord": _sign_lord(start),
                        "nakshatra": nak_name,
                        "star_lord": star_lord,
                        "sub_lord": sub_lord,
                    }
                )
            current = sub_end
    if len(segments) != 249:
        raise RuntimeError(f"KP number table must contain 249 segments, got {len(segments)}")
    return segments


NUMBER_TABLE = build_number_table()


def _ayanamsa_for_mode(jd: float, mode: int) -> float:
    swe.set_sid_mode(mode)
    value = swe.get_ayanamsa_ut(jd)
    # The shared Parashari engine uses True Citra. Restore it so importing this
    # independent module cannot silently mutate the standard stack.
    swe.set_sid_mode(swe.SIDM_TRUE_CITRA)
    return value


def _asc_for_armc(armc: float, latitude: float, obliquity: float) -> float:
    return swe.houses_armc(armc % 360.0, latitude, obliquity, b"P")[1][0] % 360.0


def _solve_armc_for_asc(target_asc: float, latitude: float, obliquity: float) -> float:
    """Solve ARMC for a requested tropical Ascendant."""
    best = min(
        range(360),
        key=lambda armc: _circular_distance(
            _asc_for_armc(float(armc), latitude, obliquity), target_asc
        ),
    )
    armc = float(best)
    for _ in range(20):
        current = _asc_for_armc(armc, latitude, obliquity)
        error = _normalise_signed(current - target_asc)
        if abs(error) < 1e-9:
            break
        step = 1e-4
        next_asc = _asc_for_armc(armc + step, latitude, obliquity)
        derivative = _normalise_signed(next_asc - current) / step
        if abs(derivative) < 1e-8:
            raise RuntimeError("Could not solve Placidus ARMC for requested KP Ascendant")
        armc = (armc - error / derivative) % 360.0
    solved = _asc_for_armc(armc, latitude, obliquity)
    if _circular_distance(solved, target_asc) > 1e-6:
        raise RuntimeError("KP Ascendant solver did not converge")
    return armc


def _house_of(longitude: float, cusps: list[float]) -> int:
    longitude %= 360.0
    for index, start in enumerate(cusps):
        end = cusps[(index + 1) % 12]
        span = (end - start) % 360.0
        offset = (longitude - start) % 360.0
        if offset < span or math.isclose(offset, 0.0, abs_tol=1e-9):
            return index + 1
    raise RuntimeError(f"Could not assign longitude {longitude} to a Placidus house")


def _position_record(name: str, longitude: float, speed: float | None = None) -> dict:
    record = {
        "name": name,
        "longitude": longitude % 360.0,
        "position": _format_degree(longitude),
        "sign": _sign_of(longitude),
        "sign_lord": _sign_lord(longitude),
        "nakshatra": NAKSHATRAS[_star_index(longitude)][0],
        "star_lord": _star_lord(longitude),
        "sub_lord": _sub_lord(longitude),
        "boundary_distance_arcmin": {
            "sign": round(_distance_to_boundaries(longitude, _SIGN_BOUNDARIES) * 60.0, 4),
            "star": round(_distance_to_boundaries(longitude, _STAR_BOUNDARIES) * 60.0, 4),
            "sub": round(_distance_to_boundaries(longitude, _SUB_BOUNDARIES) * 60.0, 4),
        },
    }
    if speed is not None:
        record["speed"] = speed
        record["retrograde"] = speed < 0
    return record


def _planet_positions(jd: float, ayanamsa: float) -> list[dict]:
    positions = []
    flags = swe.FLG_SWIEPH | swe.FLG_SPEED
    for name, planet_id in PLANET_IDS.items():
        tropical = swe.calc_ut(jd, planet_id, flags)[0]
        positions.append(
            _position_record(name, tropical[0] - ayanamsa, speed=float(tropical[3]))
        )
    rahu = swe.calc_ut(jd, swe.MEAN_NODE, flags)[0]
    rahu_lon = (rahu[0] - ayanamsa) % 360.0
    positions.append(_position_record("Rahu", rahu_lon, speed=float(rahu[3])))
    positions.append(_position_record("Ketu", rahu_lon + 180.0, speed=float(rahu[3])))
    return positions


def _node_agents(records: dict[str, dict], node_name: str) -> list[str]:
    """Return only the source-stable sign-lord agency for a node.

    Reader VI also uses conjunction/aspect agency in examples, but the current
    source audit has not established a production-grade conjunction orb or
    aspect policy. The previous 3° proximity rule was an implementation choice,
    so it is removed from operative significations rather than allowed to alter
    a promise result.
    """
    node = records[node_name]
    return [node["sign_lord"]]


def _add_signification(
    target: dict,
    house: int,
    level: str,
    via: str,
    *,
    rank: int | None = None,
    represented_level: str | None = None,
) -> None:
    key = str(house)
    target.setdefault(key, [])
    if rank is None:
        rank = SIGNIFICATOR_LEVEL_RANK[level]
    item = {"level": level, "rank": rank, "via": via}
    if represented_level is not None:
        item["represented_level"] = represented_level
    if item not in target[key]:
        target[key].append(item)


def _build_significators(
    planet_records: list[dict], cusps: list[dict]
) -> tuple[dict[str, dict], dict[str, list[dict]]]:
    records = {record["name"]: record for record in planet_records}
    owners = {cusp["house"]: cusp["sign_lord"] for cusp in cusps}
    owned_houses = {
        planet: [house for house, owner in owners.items() if owner == planet]
        for planet in SEVEN_PLANETS
    }
    significations: dict[str, dict] = {planet: {} for planet in ALL_KP_PLANETS}

    for planet in ALL_KP_PLANETS:
        record = records[planet]
        star_lord = record["star_lord"]
        star_record = records[star_lord]
        _add_signification(
            significations[planet],
            star_record["house"],
            "A_star_of_occupant",
            f"star lord {star_lord} occupies house {star_record['house']}",
        )
        _add_signification(
            significations[planet],
            record["house"],
            "B_occupant",
            f"{planet} occupies house {record['house']}",
        )
        for house in owned_houses.get(star_lord, []):
            _add_signification(
                significations[planet],
                house,
                "C_star_of_owner",
                f"star lord {star_lord} owns house {house}",
            )
        for house in owned_houses.get(planet, []):
            _add_signification(
                significations[planet],
                house,
                "D_owner",
                f"{planet} owns house {house}",
            )

    for node in NODES:
        agents = _node_agents(records, node)
        records[node]["agent_planets"] = agents
        records[node]["contact_agent_policy"] = (
            "disabled pending a sourced conjunction-orb and aspect policy; "
            "only sign-lord agency is operative"
        )
        for agent in agents:
            for house, evidence in significations[agent].items():
                for item in evidence:
                    _add_signification(
                        significations[node],
                        int(house),
                        "NODE_AGENT",
                        f"{node} represents {agent}: {item['via']}",
                        rank=item["rank"],
                        represented_level=item["level"],
                    )

    # A planet deposited in a node's star must receive the results represented
    # by that node. Reader VI explicitly judges Sun in Rahu's star through the
    # planet represented by Rahu. The previous implementation stopped at the
    # node's occupied house and silently dropped the represented houses.
    for planet in ALL_KP_PLANETS:
        star_lord = records[planet]["star_lord"]
        if star_lord not in NODES:
            continue
        represented = [
            (house, dict(item))
            for house, evidence in list(significations[star_lord].items())
            for item in list(evidence)
            if item["level"] == "NODE_AGENT"
        ]
        for house, item in represented:
            _add_signification(
                significations[planet],
                int(house),
                "A_star_of_node_agent",
                (
                    f"star lord {star_lord} acts through its agent: "
                    f"{item['via']}"
                ),
                rank=1,
                represented_level=item.get("represented_level"),
            )

    by_house: dict[str, list[dict]] = {str(house): [] for house in range(1, 13)}
    for planet, houses in significations.items():
        for house, evidence in houses.items():
            best = min(item["rank"] for item in evidence)
            by_house[house].append(
                {
                    "planet": planet,
                    "best_rank": best,
                    "evidence": evidence,
                }
            )
    for items in by_house.values():
        items.sort(key=lambda item: (item["best_rank"], item["planet"]))
    return significations, by_house


def _ruling_planets(
    dt_local: datetime,
    jd: float,
    latitude: float,
    longitude: float,
    timezone: str,
    ayanamsa: float,
    records: dict[str, dict],
) -> dict:
    tropical_cusps, tropical_ascmc = swe.houses(jd, latitude, longitude, b"P")
    del tropical_cusps
    judgment_asc = (tropical_ascmc[0] - ayanamsa) % 360.0
    moon = records["Moon"]
    civil_midnight_jd = to_jd(
        dt_local.year,
        dt_local.month,
        dt_local.day,
        0,
        0,
        timezone,
    )
    sunrise_result, sunrise_times = swe.rise_trans(
        civil_midnight_jd,
        swe.SUN,
        swe.CALC_RISE,
        (longitude, latitude, 0.0),
        0.0,
        0.0,
        swe.FLG_SWIEPH,
    )
    if sunrise_result != 0:
        raise ValueError(
            "KP day lord requires a local sunrise, but no sunrise was found "
            "for the judgment date and location"
        )
    sunrise_jd = sunrise_times[0]
    before_sunrise = jd < sunrise_jd
    effective_weekday = (dt_local.weekday() - int(before_sunrise)) % 7

    ordered = [
        {"planet": _star_lord(judgment_asc), "role": "Asc_star_lord"},
        {"planet": _sign_lord(judgment_asc), "role": "Asc_sign_lord"},
        {"planet": moon["star_lord"], "role": "Moon_star_lord"},
        {"planet": moon["sign_lord"], "role": "Moon_sign_lord"},
        {"planet": WEEKDAY_LORDS[effective_weekday], "role": "day_lord"},
    ]
    base_planets = {item["planet"] for item in ordered}
    for node in NODES:
        if records[node]["sign_lord"] in base_planets:
            ordered.append(
                {
                    "planet": node,
                    "role": f"node_agent_of_{records[node]['sign_lord']}",
                }
            )

    deduplicated = []
    seen = set()
    for item in ordered:
        if item["planet"] not in seen:
            seen.add(item["planet"])
            deduplicated.append(item)

    accepted = []
    rejected = []
    for item in deduplicated:
        planet_record = records[item["planet"]]
        star_lord = planet_record["star_lord"]
        if (
            star_lord in RETROGRADE_FILTER_PLANETS
            and records[star_lord].get("retrograde", False)
        ):
            rejected.append(
                {
                    **item,
                    "reason": f"deposited in retrograde star lord {star_lord}",
                }
            )
        else:
            accepted.append(item)
    return {
        "judgment_ascendant": _position_record("Judgment Asc", judgment_asc),
        "ordered": deduplicated,
        "accepted": accepted,
        "rejected": rejected,
        "day_rule": {
            "basis": "local sunrise to next local sunrise",
            "civil_date_sunrise_jd_ut": sunrise_jd,
            "judgment_before_sunrise": before_sunrise,
            "effective_weekday": WEEKDAY_NAMES[effective_weekday],
            "day_lord": WEEKDAY_LORDS[effective_weekday],
        },
        "retrograde_filter_scope": sorted(RETROGRADE_FILTER_PLANETS),
        "node_retrograde_policy": (
            "Rahu/Ketu are not rejected as retrograde star lords"
        ),
        "node_ruling_agent_scope": (
            "sign-lord agency active; conjunction/aspect agency deferred"
        ),
        "source": "KSK Reader VI, Ruling Planets",
    }


def _evaluate_topic(
    topic: str,
    cusps: list[dict],
    planet_records: list[dict],
    significations: dict[str, dict],
) -> dict:
    rule = TOPIC_RULES[topic]
    cusp = cusps[rule["judgment_cusp"] - 1]
    records = {record["name"]: record for record in planet_records}
    cusp_sub_lord = cusp["sub_lord"]
    cusp_sub_lord_record = records[cusp_sub_lord]

    # Reader VI's rule is not "let every A/B/C/D house of the cusp sub-lord
    # vote." It asks whether the cusp sub-lord is deposited in the
    # constellation of a planet which signifies the topic houses. Therefore
    # the operative source is that constellation lord's significator chain.
    source_significator = cusp_sub_lord_record["star_lord"]
    source_significations = significations[source_significator]
    houses = {int(house) for house in source_significations}
    positive = sorted(houses.intersection(rule["positive_houses"]))
    negative = sorted(houses.intersection(rule["negative_houses"]))
    if positive and not negative:
        directional_status = "positive_only"
    elif negative and not positive:
        directional_status = "negative_only"
    elif positive and negative:
        directional_status = "mixed"
    else:
        directional_status = "unsupported"

    position_sub_lord = cusp_sub_lord_record["sub_lord"]
    retrograde_checks = []
    blocked_by = []
    for role, planet in (
        ("cusp_sub_lord", cusp_sub_lord),
        ("constellation_lord", source_significator),
        ("position_sub_lord", position_sub_lord),
    ):
        record = records[planet]
        temporary_retrograde_applies = planet in RETROGRADE_FILTER_PLANETS
        is_blocking = temporary_retrograde_applies and record.get(
            "retrograde", False
        )
        retrograde_checks.append(
            {
                "role": role,
                "planet": planet,
                "temporary_retrograde_applies": temporary_retrograde_applies,
                "retrograde": bool(record.get("retrograde", False)),
                "blocking": is_blocking,
            }
        )
        if is_blocking and planet not in blocked_by:
            blocked_by.append(planet)

    # A node in any operative star/agent link can represent
    # conjoined/aspecting planets as well as its sign lord. Until that contact
    # policy is source-locked, a directional result traversing such a node is
    # incomplete rather than a safe promise/denial.
    node_agency_incomplete = (
        source_significator in NODES
        or records[source_significator]["star_lord"] in NODES
        or any(
            item["level"] in {"NODE_AGENT", "A_star_of_node_agent"}
            for evidence in source_significations.values()
            for item in evidence
        )
    )
    if node_agency_incomplete:
        status = "incomplete_node_agency"
    elif directional_status == "positive_only":
        status = (
            "positive_indication_blocked"
            if blocked_by
            else "promised_candidate"
        )
    elif directional_status == "negative_only":
        status = (
            "negative_indication_blocked"
            if blocked_by
            else "denied_candidate"
        )
    elif directional_status == "mixed":
        status = "mixed_with_retrograde_block" if blocked_by else "mixed"
    else:
        status = "unsupported"

    relevant_evidence = {
        str(house): source_significations[str(house)]
        for house in sorted(set(positive + negative))
    }
    return {
        "topic": topic,
        "judgment_cusp": rule["judgment_cusp"],
        "cusp_sub_lord": cusp_sub_lord,
        "cusp_sub_lord_star_lord": source_significator,
        "star_lord_signifies": sorted(houses),
        "directional_evidence": relevant_evidence,
        "position_sub_lord": position_sub_lord,
        "position_sub_lord_house": records[position_sub_lord]["house"],
        "positive_hits": positive,
        "negative_hits": negative,
        "directional_status": directional_status,
        "retrograde_gate": {
            "checks": retrograde_checks,
            "blocked_by": blocked_by,
            "status": "blocked" if blocked_by else "clear",
        },
        "node_agency_incomplete": node_agency_incomplete,
        "status": status,
        "source_rule": rule["source"],
        "scope_note": (
            "Source-scoped mechanical candidate. Node contact agency is "
            "fail-closed and final KP judgment remains experimental."
        ),
    }


def compute(
    dt_local: datetime,
    latitude: float,
    longitude: float,
    timezone: str,
    number: int,
    topic: str,
) -> dict:
    if not math.isfinite(latitude) or not -90.0 <= latitude <= 90.0:
        raise ValueError("latitude must be a finite value between -90 and 90")
    if not math.isfinite(longitude) or not -180.0 <= longitude <= 180.0:
        raise ValueError("longitude must be a finite value between -180 and 180")
    if not 1 <= number <= 249:
        raise ValueError("KP horary number must be between 1 and 249")
    if topic not in TOPIC_RULES:
        raise ValueError(f"Unsupported KP topic: {topic}")

    jd = to_jd(
        dt_local.year,
        dt_local.month,
        dt_local.day,
        dt_local.hour,
        dt_local.minute,
        timezone,
    )
    kp_ayanamsa = _ayanamsa_for_mode(jd, swe.SIDM_KRISHNAMURTI)
    true_citra = _ayanamsa_for_mode(jd, swe.SIDM_TRUE_CITRA)
    number_record = dict(NUMBER_TABLE[number - 1])
    nirayana_asc = number_record["start_lon"]
    tropical_asc = (nirayana_asc + kp_ayanamsa) % 360.0
    obliquity = swe.calc_ut(jd, swe.ECL_NUT)[0][0]
    armc = _solve_armc_for_asc(tropical_asc, latitude, obliquity)
    tropical_cusps = swe.houses_armc(armc, latitude, obliquity, b"P")[0]
    cusp_longitudes = [
        (tropical_cusps[house] - kp_ayanamsa) % 360.0 for house in range(1, 13)
    ]

    cusp_records = []
    for house, cusp_longitude in enumerate(cusp_longitudes, start=1):
        record = _position_record(f"Cusp {house}", cusp_longitude)
        record["house"] = house
        if house == 1:
            record["number_boundary_policy"] = (
                "The 1–249 number selects the following segment at its exact start; "
                "this is deterministic, not input sensitivity."
            )
        cusp_records.append(record)

    planet_records = _planet_positions(jd, kp_ayanamsa)
    for record in planet_records:
        record["house"] = _house_of(record["longitude"], cusp_longitudes)

    significations, significators_by_house = _build_significators(
        planet_records, cusp_records
    )
    records_by_name = {record["name"]: record for record in planet_records}
    ruling_planets = _ruling_planets(
        dt_local,
        jd,
        latitude,
        longitude,
        timezone,
        kp_ayanamsa,
        records_by_name,
    )
    topic_result = _evaluate_topic(
        topic,
        cusp_records,
        planet_records,
        significations,
    )

    sensitive_points = []
    for record in cusp_records + planet_records:
        if record.get("house") == 1 and record["name"] == "Cusp 1":
            continue
        if min(record["boundary_distance_arcmin"].values()) <= 5.0:
            sensitive_points.append(
                {
                    "name": record["name"],
                    "boundary_distance_arcmin": record["boundary_distance_arcmin"],
                }
            )

    return {
        "mode": "KP classical horary 1–249",
        "number": number,
        "number_segment": number_record,
        "judgment_time": dt_local.isoformat(),
        "judgment_timezone": timezone,
        "judgment_location": {"latitude": latitude, "longitude": longitude},
        "ayanamsa": {
            "mode": "Swiss Ephemeris SIDM_KRISHNAMURTI",
            "value_deg": kp_ayanamsa,
            "true_citra_difference_arcmin": round(
                _circular_distance(kp_ayanamsa, true_citra) * 60.0, 6
            ),
        },
        "house_system": "Placidus; number-derived nirayana Ascendant",
        "node_mode": (
            "Mean Node; sign-lord agency active; conjunction/aspect agency "
            "disabled pending a sourced policy"
        ),
        "horary_ascendant": _position_record("Horary Asc", nirayana_asc),
        "house_cusps": cusp_records,
        "planets": planet_records,
        "significations_by_planet": significations,
        "significators_by_house": significators_by_house,
        "topic_result": topic_result,
        "ruling_planets": ruling_planets,
        "sensitivity": {
            "threshold_arcmin": 5.0,
            "sensitive_points": sensitive_points,
            "all_points_include_raw_boundary_distances": True,
        },
        "timing": {
            "status": "disabled",
            "reason": (
                "KP Dasha/Bhukti/Antara plus Ruling-Planet and transit timing "
                "still lacks the required published-reference test suite."
            ),
        },
        "production_status": "experimental",
    }


def format_kp_section(data: dict) -> str:
    topic = data["topic_result"]
    question_lines = [f"- 问题：{data['question']}"] if data.get("question") else []
    lines = [
        "# KP Horary 独立栈（1–249）",
        "",
        "> 本文件不属于 Parashari 标准盘，也不与标准结论拼票。",
        "> 当前仍为实验栈；Timing 未启用。",
        "",
        "## 输入与技术口径",
        "",
        *question_lines,
        f"- Horary number：**{data['number']}**",
        (
            f"- Number Asc：{data['number_segment']['sign']} "
            f"{_format_degree(data['number_segment']['start_lon'])}；"
            f"{data['number_segment']['star_lord']} star / "
            f"{data['number_segment']['sub_lord']} sub"
        ),
        f"- Ayanamsa：{data['ayanamsa']['mode']}",
        f"- House：{data['house_system']}",
        f"- Node：{data['node_mode']}",
        "",
        "## 题型专属 promise 检查",
        "",
        f"- 题型：**{topic['topic']}**",
        f"- 判断 cusp：{topic['judgment_cusp']}",
        f"- Cusp sub-lord：**{topic['cusp_sub_lord']}**",
        (
            f"- Cusp sub-lord 所落 star lord："
            f"**{topic['cusp_sub_lord_star_lord']}**"
        ),
        f"- Star-lord significator houses：{topic['star_lord_signifies']}",
        (
            f"- Position sub-lord：{topic['position_sub_lord']}；"
            f"位于第 {topic['position_sub_lord_house']} 宫"
        ),
        f"- 正向命中：{topic['positive_hits']}",
        f"- 反向命中：{topic['negative_hits']}",
        f"- 方向状态：{topic['directional_status']}",
        (
            f"- 逆行 materialization gate："
            f"{topic['retrograde_gate']['status']}"
            + (
                f"（{topic['retrograde_gate']['blocked_by']}）"
                if topic["retrograde_gate"]["blocked_by"]
                else ""
            )
        ),
        (
            "- Node agency 完整性："
            + (
                "不完整；合相／相位代理未启用，本题失败关闭"
                if topic["node_agency_incomplete"]
                else "本题 operative promise 路径未穿过 node agency"
            )
        ),
        f"- 机械状态：**{topic['status']}**",
        f"- 来源规则：{topic['source_rule']}",
        "",
        "## 12 Cusps",
        "",
        "| 宫 | 位置 | Sign | Star lord | Sub lord | 最近 sub 边界 |",
        "|---|---|---|---|---|---|",
    ]
    for cusp in data["house_cusps"]:
        lines.append(
            f"| {cusp['house']} | {cusp['position']} | {cusp['sign']} | "
            f"{cusp['star_lord']} | **{cusp['sub_lord']}** | "
            f"{cusp['boundary_distance_arcmin']['sub']:.2f}' |"
        )

    lines.extend(
        [
            "",
            "## Ruling Planets",
            "",
            (
                f"- Day lord：{data['ruling_planets']['day_rule']['effective_weekday']} / "
                f"{data['ruling_planets']['day_rule']['day_lord']}；按当地日出换日"
            ),
            "- 接受："
            + (
                " / ".join(item["planet"] for item in data["ruling_planets"]["accepted"])
                or "无"
            ),
            "- 因逆行星宿主过滤："
            + (
                " / ".join(item["planet"] for item in data["ruling_planets"]["rejected"])
                or "无"
            ),
            "- Node 逆行政策：Rahu/Ketu 的正常逆向运动不触发 star-lord 剔除。",
            "- Node agent：当前只启用 sign-lord agency；合相／相位 agency 暂停。",
            "",
            "## 边界与 Timing",
            "",
            (
                f"- True Citra 与 KP ayanamsa 差值："
                f"{data['ayanamsa']['true_citra_difference_arcmin']:.3f}'"
            ),
            (
                "- 5′ 内敏感点："
                + (
                    " / ".join(
                        item["name"] for item in data["sensitivity"]["sensitive_points"]
                    )
                    or "无"
                )
            ),
            "- Timing：未启用；不得借用标准层 Moon ingress 或 natal Dasha。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Independent KP 1–249 horary engine")
    parser.add_argument("--datetime", required=True, help='"YYYY-MM-DD HH:MM" or "now"')
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)
    parser.add_argument("--tz", required=True)
    parser.add_argument("--number", type=int, required=True)
    parser.add_argument("--topic", choices=tuple(TOPIC_RULES), required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    zone = ZoneInfo(args.tz)
    if args.datetime.strip().lower() == "now":
        dt = datetime.now(zone).replace(second=0, microsecond=0)
    else:
        dt = datetime.strptime(args.datetime, "%Y-%m-%d %H:%M").replace(tzinfo=zone)
    data = compute(dt, args.lat, args.lon, args.tz, args.number, args.topic)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(format_kp_section(data), end="")


if __name__ == "__main__":
    main()
