#!/usr/bin/env python3
"""Prashna 默认标准层 formatter。

只消费 `resources/standard-layer.md` 白名单字段。共享 engine 即使计算了本命
Dasha、Chara Karaka、SAV、分盘、Yoga 或过运，本 formatter 也不读取、不输出。
"""

CLASSICAL_PLANETS = [
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"
]
NODES = ["Rahu", "Ketu"]
MOVABLE_SIGNS = {"Aries", "Cancer", "Libra", "Capricorn"}
FIXED_SIGNS = {"Taurus", "Leo", "Scorpio", "Aquarius"}
HEAD_RISING_SIGNS = {"Gemini", "Leo", "Virgo", "Libra", "Scorpio", "Aquarius"}
BACK_RISING_SIGNS = {"Aries", "Taurus", "Cancer", "Sagittarius", "Capricorn"}


def _modality(sign):
    if sign in MOVABLE_SIGNS:
        return "movable"
    if sign in FIXED_SIGNS:
        return "fixed"
    return "dual"


def _rising_type(sign):
    if sign in HEAD_RISING_SIGNS:
        return "Shirshodaya(head-rising)"
    if sign in BACK_RISING_SIGNS:
        return "Prishtodaya(back-rising)"
    return "Ubhayodaya(both-rising)"


def _distance_to_boundary(degree, span):
    remainder = degree % span
    return min(remainder, span - remainder)


def _occupants(chart, house, names):
    return [name for name in names if chart["planets"][name]["house"] == house]


def _classical_aspecting_house(chart, house):
    hits = []
    for name in CLASSICAL_PLANETS:
        data = chart["graha_drishti"].get(name, {})
        if house in data.get("aspected_houses", []):
            hits.append(name)
    return hits


def _simple_exchanges(chart):
    """返回宫主交换事实，不消费共享 engine 的 natal yoga 分类。"""
    pairs = []
    lords = chart["house_lords"]
    planets = chart["planets"]
    for first in range(1, 13):
        for second in range(first + 1, 13):
            first_lord = lords[first]["lord"]
            second_lord = lords[second]["lord"]
            if first_lord == second_lord:
                continue
            if (
                planets[first_lord]["house"] == second
                and planets[second_lord]["house"] == first
            ):
                pairs.append((first, second, first_lord, second_lord))
    return pairs


def _natural_role(chart, name):
    if name in {"Jupiter", "Venus"}:
        return "benefic [P-I.3]"
    if name in {"Sun", "Mars", "Saturn"}:
        return "malefic [P-I.3]"
    if name == "Moon":
        phase = chart.get("moon_phase", {})
        return (
            "waxing; P 仅明确 full Moon 为 benefic"
            if phase.get("waxing")
            else "waning malefic [P-I.3]"
        )
    if name == "Mercury":
        malefics = {"Sun", "Mars", "Saturn"}
        mercury_house = chart["planets"]["Mercury"]["house"]
        joined = [
            planet
            for planet in malefics
            if chart["planets"][planet]["house"] == mercury_house
        ]
        if joined:
            return f"malefic-associated with {','.join(sorted(joined))} [P-I.3]"
        return "benefic [P-I.3]"
    raise ValueError(name)


def format_standard_layer(chart):
    lagna = chart["lagna"]
    planets = chart["planets"]
    d9_lagna = chart.get("divisional_charts", {}).get("D9", {}).get("Lagna")
    lines = []

    lines.append("## Prashna 默认标准层数据\n")
    lines.append(
        "> 来源契约：Shatpanchasika-rooted classical Prashna，经 KN Rao／"
        "Bhavan 兼容性筛选。这里只给事实，不在数据层生成成败结论。"
    )
    lines.append(
        "> 判读前必须读取 `resources/standard-layer.md`，按题型支持级和适用规则账本消费。\n"
    )

    lines.append("### Lagna 与 rising Navamsa\n")
    lines.append("| 项 | 值 | 用途边界 |")
    lines.append("|---|---|---|")
    lines.append(
        f"| Lagna | {lagna['sign']} {lagna['deg_str']} | "
        f"{_modality(lagna['sign'])}; {_rising_type(lagna['sign'])} |"
    )
    lines.append(
        f"| Lagna 距 sign 边界 | {_distance_to_boundary(lagna['degree'], 30):.3f}° | "
        "时间／地点粗略时据此标敏感，不自动判盘无效 |"
    )
    lines.append(
        f"| Lagna 距 Navamsa 边界 | "
        f"{_distance_to_boundary(lagna['degree'], 30 / 9):.3f}° | "
        "仅作输入敏感性事实 |"
    )
    if d9_lagna:
        lines.append(
            f"| rising Navamsa | {d9_lagna['sign']} {d9_lagna['degree']:.4f}° | "
            "仅用于 P-I.4；禁止展开完整 D9 人生解读 |"
        )
    else:
        lines.append("| rising Navamsa | unavailable | 不得手推补造 |")
    lines.append("")

    lines.append("### D1 七曜\n")
    lines.append(
        "| 行星 | Sign | 度数 | 宫 | 月宿（描述） | 顺逆 | D1尊贵度 | 燃烧事实 | P自然角色 |"
    )
    lines.append("|---|---|---:|---:|---|---|---|---|---|")
    combustion = chart.get("combustion", {})
    dignity = chart.get("dignity", {})
    for name in CLASSICAL_PLANETS:
        planet = planets[name]
        nak = planet.get("nakshatra", {})
        combustion_text = (
            f"yes, Sun距 {combustion[name]['distance']}°"
            if name in combustion
            else "no"
        )
        lines.append(
            f"| {name} | {planet['sign']} | {planet['deg_str']} | {planet['house']} | "
            f"{nak.get('name', '—')} p{nak.get('pada', '—')} | "
            f"{'R' if planet.get('retrograde') else 'D'} | "
            f"{dignity.get(name, {}).get('basic', '—')} | {combustion_text} | "
            f"{_natural_role(chart, name)} |"
        )
    lines.append("")

    lines.append("### Nodes 位置事实\n")
    lines.append(
        "> Rahu／Ketu 不进入 P-I.3 的七曜自然吉凶表；默认层只保留位置，不赋予全局成败权重。\n"
    )
    lines.append("| Node | Sign | 度数 | 宫 | 月宿（描述） |")
    lines.append("|---|---|---:|---:|---|")
    for name in NODES:
        planet = planets[name]
        nak = planet.get("nakshatra", {})
        lines.append(
            f"| {name} | {planet['sign']} | {planet['deg_str']} | {planet['house']} | "
            f"{nak.get('name', '—')} p{nak.get('pada', '—')} |"
        )
    lines.append("")

    lines.append("### 12宫、宫主与扶压事实\n")
    lines.append(
        "> 本表是 P-I.3 的核心输入。第6宫等位置必须按题目语义解释，禁止套用"
        "“3／6／8／12一律不利”。\n"
    )
    lines.append("| 宫 | Sign | 宫主 | 宫主落宫 | 七曜占据 | Nodes | 七曜照射本宫 |")
    lines.append("|---:|---|---|---:|---|---|---|")
    for house in range(1, 13):
        lord = chart["house_lords"][house]
        classical_here = ", ".join(_occupants(chart, house, CLASSICAL_PLANETS)) or "—"
        nodes_here = ", ".join(_occupants(chart, house, NODES)) or "—"
        aspects = ", ".join(_classical_aspecting_house(chart, house)) or "—"
        lines.append(
            f"| {house} | {lord['sign']} | {lord['lord']} | {lord['lord_house']} | "
            f"{classical_here} | {nodes_here} | {aspects} |"
        )
    lines.append("")

    lines.append("### 七曜 Graha Drishti\n")
    lines.append(
        "> 整宫 Parashari Graha Drishti；不使用西方 orb，也不在默认层计算 "
        "applying／separating。\n"
    )
    lines.append("| 行星 | 从宫 | 照射宫 | 照射七曜 |")
    lines.append("|---|---:|---|---|")
    for name in CLASSICAL_PLANETS:
        data = chart["graha_drishti"][name]
        aspected_planets = [
            other
            for other in CLASSICAL_PLANETS
            if planets[other]["house"] in data["aspected_houses"]
        ]
        lines.append(
            f"| {name} | {data['from_house']} | "
            f"{', '.join(map(str, data['aspected_houses']))} | "
            f"{', '.join(aspected_planets) or '—'} |"
        )
    lines.append("")

    mutual = [
        pair
        for pair in chart.get("mutual_drishti", [])
        if all(name in CLASSICAL_PLANETS for name in pair)
    ]
    exchanges = _simple_exchanges(chart)
    lines.append("### 派生结构事实\n")
    lines.append(
        f"- 七曜互视：{'; '.join(' ↔ '.join(pair) for pair in mutual) or '无'}"
    )
    if exchanges:
        for first, second, first_lord, second_lord in exchanges:
            lines.append(
                f"- 宫主交换：{first}宫主 {first_lord} ↔ "
                f"{second}宫主 {second_lord}"
            )
    else:
        lines.append("- 宫主交换：无")
    lines.append(
        "- 边界：这里只记录连接结构；不得自动套用 natal Raja／Dhana／"
        "Dainya／Khala Yoga 分类。\n"
    )

    lines.append("### 默认择时边界\n")
    lines.append(
        "> 默认标准层不输出生产级事件时间窗。提问盘生成的120年 Vimshottari、"
        "Chara Dasha、当前过运和 Moon ingress 均不作为 Prashna timing。"
        "未来 timing 模块必须另有来源、题型范围、例盘和边界测试。\n"
    )
    return "\n".join(lines)
