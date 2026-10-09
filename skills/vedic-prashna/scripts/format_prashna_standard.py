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
SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]
SIGN_LORDS = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
    "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn",
    "Pisces": "Jupiter",
}
KENDRA_FROM = {4, 7, 10}
TRIKONA_FROM = {5, 9}
STRONG_BASIC = {"exalted", "own_sign"}

# 描述题查表（P-VI.4、P-VII.13 注），只给查表事实，不生成结论。
PLANET_DIRECTIONS = {
    "Sun": "东", "Venus": "东南", "Mars": "南", "Rahu": "西南",
    "Saturn": "西", "Moon": "西北", "Mercury": "北", "Jupiter": "东北",
}
SIGN_DIRECTIONS = {
    "Aries": "东", "Leo": "东", "Sagittarius": "东",
    "Taurus": "南", "Virgo": "南", "Capricorn": "南",
    "Gemini": "西", "Libra": "西", "Aquarius": "西",
    "Cancer": "北", "Scorpio": "北", "Pisces": "北",
}
DREKKANA_PLACES = ["门槛", "中间部分", "后院"]
OBJECT_KINDS_ODD = ["Dhatu（金属矿物）", "Moola（植物）", "Jeeva（生物）"]
OBJECT_KINDS_EVEN = ["Jeeva（生物）", "Moola（植物）", "Dhatu（金属矿物）"]
NAVAMSA_SIZES = {
    "Aquarius": "短（含圆形）", "Pisces": "短（含圆形）",
    "Aries": "短（含圆形）", "Taurus": "短（含圆形）",
    "Gemini": "中", "Cancer": "中", "Sagittarius": "中", "Capricorn": "中",
    "Leo": "长", "Scorpio": "长", "Virgo": "长", "Libra": "长",
}
NIGHT_SIGNS = {"Aries", "Taurus", "Gemini", "Cancer", "Sagittarius", "Capricorn"}
HIDING_PLACES = {
    "Aries": "步道", "Taurus": "牛棚", "Gemini": "礼堂／剧场／战场",
    "Cancer": "近水", "Leo": "林区", "Virgo": "近港口", "Libra": "店铺",
    "Scorpio": "洞穴", "Sagittarius": "寺庙周边", "Capricorn": "近水",
    "Aquarius": "艺术环境或储藏室", "Pisces": "近水",
}
LORD_AGES = {
    "Moon": "儿童", "Mars": "四岁以上", "Mercury": "5–12 岁",
    "Venus": "至 23 岁的年轻人", "Jupiter": "中年", "Sun": "年长",
    "Saturn": "老年",
}
# P-VII.4 注：水象座两说并列，不择一。
WATERY_HORASARA = {"Cancer", "Capricorn", "Scorpio", "Pisces"}


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
    """Bhattotpala 自然吉凶，只在 Ayer 判据 F1～F3 都不命中时回落使用。"""
    if name in {"Jupiter", "Venus"}:
        return "吉"
    if name in {"Sun", "Mars", "Saturn"}:
        return "凶"
    if name == "Moon":
        phase = chart.get("moon_phase", {})
        return "盈月未定" if phase.get("waxing") else "凶"
    if name == "Mercury":
        malefics = {"Sun", "Mars", "Saturn"}
        mercury_house = chart["planets"]["Mercury"]["house"]
        joined = [
            planet
            for planet in malefics
            if chart["planets"][planet]["house"] == mercury_house
        ]
        return "凶" if joined else "吉"
    raise ValueError(name)


def _natural_role_text(chart, name):
    role = _natural_role(chart, name)
    if role == "盈月未定":
        return "盈月；原文只明确满月为吉"
    if name == "Mercury" and role == "凶":
        return "凶（与凶星同宫）"
    return role


def _houses_ruled_from(planet, sign):
    """planet 以 sign 为 1 宫时主管的宫位。"""
    base = SIGNS.index(sign)
    return {
        house
        for house in range(1, 13)
        if SIGN_LORDS[SIGNS[(base + house - 1) % 12]] == planet
    }


def _ayer_role(chart, planet, sign):
    """Ayer P-I.3 注的功能吉凶：planet 对它占据或照射的星座 sign 吉还是凶。

    F1 本宫主恒吉；F2 主 3、12 宫且落陷为凶（注例一 Jupiter/Capricorn）；
    F3 主角宫兼三方宫且强（exalted／own_sign）为吉（注例二 Mars/Leo）；
    其余回落 Bhattotpala 自然吉凶。
    """
    ruled = _houses_ruled_from(planet, sign)
    basic = chart.get("dignity", {}).get(planet, {}).get("basic")
    if 1 in ruled:
        return "吉(宫主)"
    if {3, 12} <= ruled and basic == "debilitated":
        return "凶(注例一)"
    if ruled & KENDRA_FROM and ruled & TRIKONA_FROM and basic in STRONG_BASIC:
        return "吉(注例二)"
    return f"{_natural_role(chart, planet)}(回落)"


def _labelled(chart, names, sign):
    return ", ".join(f"{name} {_ayer_role(chart, name, sign)}" for name in names)


def _navamsa_number(degree):
    return min(int(degree // (30 / 9)), 8) + 1


def tithi_facts(sun_longitude, moon_longitude):
    """tithi 用未舍入的经度差；满月窗按 P-I.5 注：白半月第 10 至黑半月第 5 tithi。"""
    elongation = (moon_longitude - sun_longitude) % 360.0
    tithi = int(elongation // 12.0) + 1
    return tithi, 10 <= tithi <= 20


def _house_from(start_house, target_house):
    return (target_house - start_house) % 12 + 1


def _watery_mantreswara(sign, degree):
    if sign in {"Cancer", "Pisces"}:
        return True
    return sign == "Capricorn" and degree >= 15


def _yes(flag):
    return "是" if flag else "否"


def _descriptive_facts(chart, d9_lagna):
    """描述题（P-VI.1～4、P-VII.13、P-I.7）与天气题（P-VII.3～4）的查表事实。"""
    lagna = chart["lagna"]
    planets = chart["planets"]
    sign = lagna["sign"]
    degree = lagna["degree"]
    lines = []

    lines.append("### 描述题与天气查表事实\n")
    lines.append(
        "> 只在 `question-taxonomy.md` §2.10 描述题、§2.11 天气题消费；描述输出不进成／悬／不成三档。"
        "原文歧义处两说并列，不择一。\n"
    )

    lines.append("**P-VI.1～2 失物是否在家、藏在何处**\n")
    if d9_lagna:
        d9_sign = d9_lagna["sign"]
        lines.append(
            f"- Lagna 固定座：{_yes(sign in FIXED_SIGNS)}；rising Navamsa 固定座："
            f"{_yes(d9_sign in FIXED_SIGNS)}；vargottama（Lagna 星座＝rising Navamsa 星座）："
            f"{_yes(sign == d9_sign)}"
        )
    else:
        lines.append(
            f"- Lagna 固定座：{_yes(sign in FIXED_SIGNS)}；rising Navamsa unavailable，"
            "VI.1 只能读 Lagna 一项"
        )
    drekkana = min(int(degree // 10), 2)
    lines.append(
        f"- Lagna 在第 {drekkana + 1} 个 drekkana（每 10°）→ 屋内藏处："
        f"{DREKKANA_PLACES[drekkana]}（只在 VI.1 读作“屋内”时用）"
    )
    lines.append("")

    lines.append("**P-VI.4 方向与距离**\n")
    kendra_planets = [
        name
        for name in CLASSICAL_PLANETS + ["Rahu"]
        if planets[name]["house"] in {1, 4, 7, 10}
    ]
    lagna_direction = SIGN_DIRECTIONS[sign]
    listed = ", ".join(
        f"{name}（{planets[name]['house']}宫，{PLANET_DIRECTIONS[name]}）"
        for name in kendra_planets
    )
    lines.append(
        f"- 角宫行星（含 Rahu；Ketu 原文未列方向，不计）：{listed or '无'}"
    )
    lines.append(f"- Lagna 星座方向：{lagna_direction}")
    if not kendra_planets:
        lines.append(f"- 方向读法：角宫无星，按 Lagna 星座 → {lagna_direction}")
    elif len(kendra_planets) == 1:
        only = kendra_planets[0]
        lines.append(
            f"- 方向读法：角宫仅 1 星，正文（In their absence, by the lagna）读作 "
            f"{PLANET_DIRECTIONS[only]}；注（Two or more planets in kendras）读作 "
            f"{lagna_direction}；两读并列"
        )
    else:
        directions = sorted({PLANET_DIRECTIONS[name] for name in kendra_planets})
        lines.append(
            f"- 方向读法：角宫 {len(kendra_planets)} 星，按行星方向 → "
            f"{'／'.join(directions)}（不止一个方向时并列）"
        )
    number = _navamsa_number(degree)
    first_half = degree < 15
    offset = number - 1 if first_half else number - 5
    lines.append(
        f"- Lagna 在本座{'前' if first_half else '后'}半，rising Navamsa 序号 {number}，"
        f"距{'第 1' if first_half else '中间第 5'} 个 Navamsa {offset} 格 → 距离读数 {offset}"
        "（0～4，只作相对远近；原文单位 yojana，注称按现代条件另定尺度）"
    )
    lines.append("")

    lines.append("**P-I.7、P-VII.13 物品与人**\n")
    odd_sign = SIGNS.index(sign) % 2 == 0
    kinds = OBJECT_KINDS_ODD if odd_sign else OBJECT_KINDS_EVEN
    lines.append(
        f"- 物品属性（I.7，Lagna {'奇' if odd_sign else '偶'}数座第 {number} 个 Navamsa）："
        f"{kinds[(number - 1) % 3]}"
    )
    if d9_lagna:
        lines.append(
            f"- 物品大小（VII.13 注，按 rising Navamsa {d9_lagna['sign']}）："
            f"{NAVAMSA_SIZES[d9_lagna['sign']]}"
        )
    lines.append(
        f"- 失窃时段（按 Lagna {sign}）：{'夜间' if sign in NIGHT_SIGNS else '白天'}"
    )
    lines.append(f"- 去向方向（按 Lagna {sign}）：{lagna_direction}")
    lines.append(f"- 藏放处（按 Lagna {sign}）：{HIDING_PLACES[sign]}")
    lagna_lord = SIGN_LORDS[sign]
    lines.append(
        f"- 拿走者或失踪者年龄（按 Lagna 主 {lagna_lord}）：{LORD_AGES[lagna_lord]}"
    )
    lines.append("")

    lines.append("**P-VII.3～4 天气（雨季前提由用户提供）**\n")
    moon_house = planets["Moon"]["house"]
    sun_house = planets["Sun"]["house"]
    venus_house = planets["Venus"]["house"]
    saturn_house = planets["Saturn"]["house"]
    lines.append(f"- 白半月（盈）：{_yes(chart.get('moon_phase', {}).get('waxing'))}")
    lines.append(
        f"- VII.3(a)：Venus 在 Moon 起第 {_house_from(moon_house, venus_house)} 宫；"
        f"Saturn 在 Moon 起第 {_house_from(moon_house, saturn_house)} 宫、"
        f"Sun 起第 {_house_from(sun_house, saturn_house)} 宫（注：Venus 不可能在 Sun 起第 7）"
    )
    lines.append(
        f"- VII.3(b)：Venus 在 Lagna 起第 {venus_house} 宫；Saturn 在第 {saturn_house} 宫"
    )
    rain_houses = (3, 2, 1, 4, 7, 10)
    rain_planets = [
        name
        for name in CLASSICAL_PLANETS
        if planets[name]["house"] in rain_houses
    ]
    if rain_planets:
        for name in rain_planets:
            planet = planets[name]
            lines.append(
                f"- VII.4(a)：{name} 在第 {planet['house']} 宫 {planet['sign']}，"
                f"{_ayer_role(chart, name, planet['sign'])}；水象 Horasara："
                f"{_yes(planet['sign'] in WATERY_HORASARA)}；Mantreswara："
                f"{_yes(_watery_mantreswara(planet['sign'], planet['degree']))}"
            )
    else:
        lines.append("- VII.4(a)：第 3、2 宫与角宫无七曜")
    moon = planets["Moon"]
    lines.append(
        f"- VII.4(b)：Moon 在 Lagna：{_yes(moon_house == 1)}；Moon 星座 {moon['sign']} 水象 "
        f"Horasara：{_yes(moon['sign'] in WATERY_HORASARA)}；Mantreswara："
        f"{_yes(_watery_mantreswara(moon['sign'], moon['degree']))}"
    )
    lines.append("")
    return lines


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
    gemini_note = (
        "；P-VI.3 注的头升列表无 Gemini，两说并列"
        if lagna["sign"] == "Gemini"
        else ""
    )
    lines.append(
        f"| Lagna | {lagna['sign']} {lagna['deg_str']} | "
        f"{_modality(lagna['sign'])}; {_rising_type(lagna['sign'])}{gemini_note} |"
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
        d9_lord = SIGN_LORDS[d9_lagna["sign"]]
        lines.append(
            f"| rising Navamsa | {d9_lagna['sign']} {d9_lagna['degree']:.4f}°"
            f"（本座第 {_navamsa_number(lagna['degree'])} 个 Navamsa） | "
            "仅用于 P-I.4、P-I.7、P-VI.1、P-VI.4、P-VII.13；禁止展开完整 D9 人生解读 |"
        )
        lines.append(
            f"| rising Navamsa 座主 | {d9_lord} "
            f"{_ayer_role(chart, d9_lord, lagna['sign'])} | "
            "对 Lagna 星座的功能吉凶标签，P-I.4 “falls in a benefic's varga” 用 |"
        )
    else:
        lines.append("| rising Navamsa | unavailable | 不得手推补造 |")
    lines.append("")

    lines.append("### D1 七曜\n")
    lines.append(
        "| 行星 | Sign | 度数 | 宫 | 月宿（描述） | 顺逆 | D1尊贵度 | 燃烧事实 | "
        "自然吉凶（Bhattotpala，回落用） |"
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
            f"{_natural_role_text(chart, name)} |"
        )
    lines.append("")

    lines.append("### Nodes 位置事实\n")
    lines.append(
        "> Rahu／Ketu 不贴 P-I.3 吉凶标签；默认层只保留位置，不赋予全局成败权重。\n"
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
    lines.append(
        "> 吉凶标签按 Ayer P-I.3 注的功能口径，相对本宫星座计算：吉(宫主)＝本宫主；"
        "凶(注例一)＝主 3、12 宫且落陷；吉(注例二)＝主角宫兼三方宫且 exalted／own_sign；"
        "其余为“(回落)”，即 Bhattotpala 自然吉凶。\n"
    )
    lines.append(
        "| 宫 | Sign | 宫主 | 宫主落宫 | 七曜占据（吉凶标签） | Nodes | 七曜照射本宫（吉凶标签） |"
    )
    lines.append("|---:|---|---|---:|---|---|---|")
    for house in range(1, 13):
        lord = chart["house_lords"][house]
        sign = lord["sign"]
        classical_here = (
            _labelled(chart, _occupants(chart, house, CLASSICAL_PLANETS), sign) or "—"
        )
        nodes_here = ", ".join(_occupants(chart, house, NODES)) or "—"
        aspects = _labelled(chart, _classical_aspecting_house(chart, house), sign) or "—"
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

    lines.extend(_descriptive_facts(chart, d9_lagna))

    lines.append("### 时间边界\n")
    lines.append(
        "> 本文件不含时间。标准层定为成或悬后，时间副层另写 timing_overlay.md"
        "（resources/timing-layer.md）；不成档不给时间。提问盘生成的120年 Vimshottari、"
        "Chara Dasha、当前过运均不作为 Prashna 时间。\n"
    )
    return "\n".join(lines)
