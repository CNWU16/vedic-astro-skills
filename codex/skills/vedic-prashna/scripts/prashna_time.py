#!/usr/bin/env python3
"""Second-precise time handling for the isolated Prashna stacks.

The shared natal engine remains read-only and minute-compatible.  This module
uses it as the seed calculation, then refreshes only the exact D1 facts that
the Prashna standard layer and Tajika overlay are allowed to consume.
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


def local_datetime_to_jd(dt_local: datetime, timezone: str) -> float:
    """Convert a local aware/naive datetime to Julian day with full precision."""
    naive = dt_local.replace(tzinfo=None)
    localized = pytz.timezone(timezone).localize(naive, is_dst=None)
    utc = localized.astimezone(pytz.utc)
    hour = (
        utc.hour
        + utc.minute / 60.0
        + utc.second / 3600.0
        + utc.microsecond / 3_600_000_000.0
    )
    return engine.swe.julday(
        utc.year, utc.month, utc.day, hour, engine.swe.GREG_CAL
    )


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


def _exact_planets(jd: float, lagna_sign_idx: int) -> dict:
    planets = {}
    for name, planet_id in engine.PLANETS_SWE.items():
        record = engine.calc_planet(jd, planet_id)
        record["deg_str"] = _format_degree(record["longitude"])
        record["house"] = engine.get_house(record["sign_idx"], lagna_sign_idx)
        record["nakshatra"] = engine.get_nakshatra(record["longitude"])
        planets[name] = record

    flags = engine.swe.FLG_SIDEREAL | engine.swe.FLG_SPEED
    node_result = engine.swe.calc_ut(jd, engine.swe.MEAN_NODE, flags)[0]
    rahu_longitude = node_result[0] % 360.0
    for name, longitude, speed in (
        ("Rahu", rahu_longitude, node_result[3]),
        ("Ketu", (rahu_longitude + 180.0) % 360.0, -node_result[3]),
    ):
        sign_idx = int(longitude / 30.0)
        planets[name] = {
            "longitude": longitude,
            "sign": engine.SIGNS[sign_idx],
            "sign_idx": sign_idx,
            "degree": longitude % 30.0,
            "deg_str": _format_degree(longitude),
            "retrograde": True,
            "speed": speed,
            "house": engine.get_house(sign_idx, lagna_sign_idx),
            "nakshatra": engine.get_nakshatra(longitude),
        }
    return planets


def _exact_dignity(planets: dict) -> dict:
    exaltation = {
        "Sun": "Aries",
        "Moon": "Taurus",
        "Mars": "Capricorn",
        "Mercury": "Virgo",
        "Jupiter": "Cancer",
        "Venus": "Pisces",
        "Saturn": "Libra",
    }
    debilitation = {
        "Sun": "Libra",
        "Moon": "Scorpio",
        "Mars": "Cancer",
        "Mercury": "Pisces",
        "Jupiter": "Capricorn",
        "Venus": "Virgo",
        "Saturn": "Aries",
    }
    own_signs = {
        "Sun": {"Leo"},
        "Moon": {"Cancer"},
        "Mars": {"Aries", "Scorpio"},
        "Mercury": {"Gemini", "Virgo"},
        "Jupiter": {"Sagittarius", "Pisces"},
        "Venus": {"Taurus", "Libra"},
        "Saturn": {"Capricorn", "Aquarius"},
    }
    natural_relations = {
        "Sun": {
            "friend": {"Moon", "Mars", "Jupiter"},
            "enemy": {"Venus", "Saturn"},
        },
        "Moon": {"friend": {"Sun", "Mercury"}, "enemy": set()},
        "Mars": {
            "friend": {"Sun", "Moon", "Jupiter"},
            "enemy": {"Mercury"},
        },
        "Mercury": {"friend": {"Sun", "Venus"}, "enemy": {"Moon"}},
        "Jupiter": {
            "friend": {"Sun", "Moon", "Mars"},
            "enemy": {"Mercury", "Venus"},
        },
        "Venus": {
            "friend": {"Mercury", "Saturn"},
            "enemy": {"Sun", "Moon"},
        },
        "Saturn": {
            "friend": {"Mercury", "Venus"},
            "enemy": {"Sun", "Moon", "Mars"},
        },
    }
    compound_table = {
        ("friend", "temp_friend"): "great_friend",
        ("friend", "temp_enemy"): "neutral",
        ("enemy", "temp_friend"): "neutral",
        ("enemy", "temp_enemy"): "great_enemy",
        ("neutral", "temp_friend"): "friend",
        ("neutral", "temp_enemy"): "enemy",
    }

    dignity = {}
    for name in engine.PLANETS_SWE:
        record = planets[name]
        sign = record["sign"]
        if exaltation[name] == sign:
            value = "exalted"
        elif debilitation[name] == sign:
            value = "debilitated"
        elif sign in own_signs[name]:
            value = "own_sign"
        else:
            lord = engine.SIGN_LORDS[record["sign_idx"]]
            relation = natural_relations[name]
            if lord in relation["friend"]:
                natural = "friend"
            elif lord in relation["enemy"]:
                natural = "enemy"
            else:
                natural = "neutral"
            lord_sign_idx = planets[lord]["sign_idx"]
            distance = (lord_sign_idx - record["sign_idx"]) % 12
            temporal = (
                "temp_friend"
                if distance in {1, 2, 3, 9, 10, 11}
                else "temp_enemy"
            )
            value = compound_table[(natural, temporal)]
        dignity[name] = {"basic": value, "compound": value}
    return dignity


def calculate_prashna_chart(
    dt_local: datetime,
    latitude: float,
    longitude: float,
    timezone: str,
) -> dict:
    """Return the shared chart with second-precise Prashna facts refreshed."""
    chart = engine.calculate_full_chart(
        dt_local.year,
        dt_local.month,
        dt_local.day,
        dt_local.hour,
        dt_local.minute,
        latitude,
        longitude,
        timezone,
    )
    jd = local_datetime_to_jd(dt_local, timezone)
    lagna = engine.calc_lagna(jd, latitude, longitude)
    lagna["deg_str"] = _format_degree(lagna["longitude"])
    lagna["nakshatra"] = engine.get_nakshatra(lagna["longitude"])
    lagna["house"] = 1
    planets = _exact_planets(jd, lagna["sign_idx"])

    chart["ayanamsa"] = engine.swe.get_ayanamsa_ut(jd)
    chart["lagna"] = lagna
    chart["planets"] = planets
    chart["dignity"] = _exact_dignity(planets)

    combustion = {}
    sun_longitude = planets["Sun"]["longitude"]
    for name in ("Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"):
        result = engine.check_combustion(
            name,
            planets[name]["longitude"],
            sun_longitude,
            planets[name]["retrograde"],
        )
        active = result if isinstance(result, bool) else result.get("is_combust", False)
        if active:
            distance = abs(planets[name]["longitude"] - sun_longitude)
            combustion[name] = {
                "distance": round(min(distance, 360.0 - distance), 2)
            }
    chart["combustion"] = combustion

    house_lords = engine.calc_house_lords(lagna["sign_idx"])
    for info in house_lords.values():
        info["lord_house"] = planets[info["lord"]]["house"]
    chart["house_lords"] = house_lords
    chart["graha_drishti"] = engine.calc_graha_drishti(planets)
    chart["mutual_drishti"] = engine.calc_mutual_drishti(chart["graha_drishti"])
    chart["parivartana"] = engine.calc_parivartana(house_lords, planets)

    moon_sun_difference = (
        planets["Moon"]["longitude"] - planets["Sun"]["longitude"]
    ) % 360.0
    chart["moon_phase"] = {
        "waxing": moon_sun_difference < 180.0,
        "sun_moon_diff": round(moon_sun_difference, 1),
    }

    d9_sign, d9_sign_idx = engine.calc_navamsha(lagna["longitude"])
    d9_degree = ((lagna["degree"] % (30.0 / 9.0)) * 9.0) % 30.0
    chart.setdefault("divisional_charts", {}).setdefault("D9", {})["Lagna"] = {
        "sign": d9_sign,
        "sign_idx": d9_sign_idx,
        "degree": d9_degree,
    }
    chart["prashna_input_precision"] = {
        "datetime": dt_local.isoformat(),
        "seconds_preserved": True,
    }
    return chart
