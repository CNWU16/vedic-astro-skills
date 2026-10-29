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
# 能力层（M-XIV.39–40 Raman 注：强＝本座、入旺、友座，友指天然友；弱＝落陷；凶位＝6／8／12）。
# 天然友谊按 BPHS Naisargika 表，与 engine 同表。
NATURAL_FRIENDS = {
    "Sun": {"Moon", "Mars", "Jupiter"}, "Moon": {"Sun", "Mercury"},
    "Mars": {"Sun", "Moon", "Jupiter"}, "Mercury": {"Sun", "Venus"},
    "Jupiter": {"Sun", "Moon", "Mars"}, "Venus": {"Mercury", "Saturn"},
    "Saturn": {"Mercury", "Venus"},
}
DUSTHANA = {6, 8, 12}

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

# P-I.4 注的六分盘（Lagna、Hora、Drekkana、Navamsa、Dwadasamsa、Trimsamsa）。
# Hora 取传统 Sun／Moon Hora（奇数座前半 Leo、后半 Cancer，偶数座反之）；共享 engine
# 的 D2 是 Uma Shambhu Hora（同 JHora "D-2 (US)"，PyJHora 注释亦称 PVR parivritti），不是这一口径，不读。其余四分盘按 Parashara
# 公式算，并与 engine 分盘的 Lagna 逐一核对，不一致整表 unavailable。
# 公式核对样例：M-XVIII.148 注 Virgo 30° → Mercury、Sun、Venus、Mercury、Sun、Mars。
SHADVARGA_NAMES = {
    "D1": "Lagna 本座", "D2": "Hora（传统 Sun／Moon）", "D3": "Drekkana",
    "D9": "Navamsa", "D12": "Dwadasamsa", "D30": "Trimsamsa",
}
TRIMSAMSA_ODD = ((5, "Aries"), (10, "Aquarius"), (18, "Sagittarius"), (25, "Gemini"), (30, "Libra"))
TRIMSAMSA_EVEN = ((5, "Taurus"), (12, "Virgo"), (20, "Pisces"), (25, "Capricorn"), (30, "Scorpio"))


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


def _lord_ability(chart, house):
    """能力层事实：宫主的折损项、救应与结论。不进账本合计，只供否决与叙述。

    折损项（M-XIV.39–40；M-XIV.30 只取作用于宫主自身的几项，不取 6／8／12 宫主连接）：
    落陷、落 6／8／12 宫、燃烧、逆行、受凶星占照而无吉星。
    救应：吉星同宫或照射；宫主入旺、本座或落天然友座。
    结论：三项及以上，或两项而无救应 → 严重受损；一到两项 → 能力打折；无折损项时有力或正常。
    """
    planet = chart["house_lords"][house]["lord"]
    data = chart["planets"][planet]
    where, sign = data["house"], data["sign"]
    basic = chart.get("dignity", {}).get(planet, {}).get("basic")
    others = [name for name in _occupants(chart, where, CLASSICAL_PLANETS) if name != planet]
    others += [name for name in _classical_aspecting_house(chart, where) if name != planet]
    roles = [_ayer_role(chart, name, sign) for name in others]
    malefics = [name for name, role in zip(others, roles) if role.startswith("凶")]
    malefic = bool(malefics)
    benefic = any(role.startswith("吉") for role in roles)
    factors = []
    if basic == "debilitated":
        factors.append("落陷")
    if where in DUSTHANA:
        factors.append(f"落{where}宫")
    if planet in chart.get("combustion", {}):
        factors.append("燃烧")
    if data.get("retrograde"):
        factors.append("逆行")
    if malefic and not benefic:
        # 写出是哪几颗凶星：所问动作需要的征象星不计此项（judgment-rubric §2.1 按需减项）
        factors.append(f"受凶星占照（{'、'.join(malefics)}）、无吉星")
    strong = basic in STRONG_BASIC or SIGN_LORDS[sign] in NATURAL_FRIENDS[planet]
    rescue = []
    if benefic:
        rescue.append("吉星占照")
    if strong:
        rescue.append("入旺" if basic == "exalted" else "本座" if basic == "own_sign" else "天然友座")
    if len(factors) >= 3 or (len(factors) == 2 and not rescue):
        verdict = "严重受损"
    elif factors:
        verdict = "能力打折"
    else:
        verdict = "有力" if strong else "正常"
    return planet, factors, rescue, verdict


def _lord_links(chart, house):
    """意愿层事实：宫主同宫、照射之星（及其从 Lagna 起所管宫），与 Lagna 主的连接。"""
    lagna_sign = chart["lagna"]["sign"]
    planets = chart["planets"]
    planet = chart["house_lords"][house]["lord"]
    where = planets[planet]["house"]

    def with_rule(names):
        return ", ".join(
            f"{name}（管{'、'.join(map(str, sorted(_houses_ruled_from(name, lagna_sign)))) or '—'}）"
            if name in CLASSICAL_PLANETS else name
            for name in names
        ) or "—"

    joined = [n for n in _occupants(chart, where, CLASSICAL_PLANETS + NODES) if n != planet]
    aspecting = [n for n in _classical_aspecting_house(chart, where) if n != planet]
    first_lord = chart["house_lords"][1]["lord"]
    if planet == first_lord:
        link = "即 Lagna 主"
    else:
        link = "、".join(_relation(chart, first_lord, planet)) or "无"
    return planet, with_rule(joined), with_rule(aspecting), link


def _sees(chart, a, b):
    """a 的 Graha Drishti 落在 b 所在的宫。"""
    where = chart["planets"][b]["house"]
    return where in chart["graha_drishti"].get(a, {}).get("aspected_houses", [])


def _relation(chart, a, b):
    """M-XIV.43 的连接：同宫；照射（单向即可，写明谁照谁）；互换；互为 4／10 宫（角宫关系）。"""
    if a == b:
        return ["同一颗星"]
    planets = chart["planets"]
    kinds = []
    if planets[a]["house"] == planets[b]["house"]:
        kinds.append("同宫")
    ab, ba = _sees(chart, a, b), _sees(chart, b, a)
    if ab and ba:
        kinds.append("互照")
    elif ab or ba:
        kinds.append(f"{a} 照 {b}" if ab else f"{b} 照 {a}")
    if SIGN_LORDS[planets[a]["sign"]] == b and SIGN_LORDS[planets[b]["sign"]] == a:
        kinds.append("互换")
    if (planets[b]["house"] - planets[a]["house"]) % 12 in (3, 9):
        kinds.append("互为4/10宫")
    return kinds


def _touches(chart, karaka, planet):
    """征象星串联（执行口径，B 级）：征象星与 planet 同宫，或由征象星照射 planet。"""
    if karaka == planet:
        return "即本星"
    if chart["planets"][karaka]["house"] == chart["planets"][planet]["house"]:
        return "同宫"
    return f"{karaka} 照 {planet}" if _sees(chart, karaka, planet) else ""


def _derived(actor, n):
    """以 actor 宫为命宫的第 n 宫（M-XVII.8–9：对方从 7 宫读；M-XIV.116 注：从 7 宫起算）。"""
    return (actor + n - 2) % 12 + 1


def _action_chain(chart, actor):
    """行动链（judgment-rubric §2.5，执行口径）：只回答"行动者会不会动"，不进账本合计。

    ① 起意：行动者起第 3 宫主与行动者宫主相连，或 Mars 触及行动者宫主（M-XIV.5、31、43）；
    ② 行动：行动者起第 10 宫主与行动者宫主相连或同星（M-XIV.12）；
    ③ 指向你：行动者宫主、起意宫主、行动宫主之一与 Lagna 主相连，或经 Mars 串联（M-XIV.43）；
    ④ 能力：行动者宫主或起意宫主严重受损（M-XIV.39）。
    Mercury、Venus、Sun 只有第七宫照射，它们串得起的两端必已直连，所以③只需另查 Mars。
    """
    lord = lambda house: chart["house_lords"][house]["lord"]
    rel = lambda a, b: "、".join(_relation(chart, a, b))
    first, doer = lord(1), lord(actor)
    starter, mover = lord(_derived(actor, 3)), lord(_derived(actor, 10))
    pair = lambda a, b: f"即行动者宫主 {b}" if a == b else (f"{a}–{b}：{rel(a, b)}" if rel(a, b) else "")
    start = [f"起意宫主 {pair(starter, doer)}"] if pair(starter, doer) else []
    if doer == "Mars":
        start.append("行动者宫主即 Mars")
    elif _touches(chart, "Mars", doer):
        start.append(f"Mars–{doer}：{_touches(chart, 'Mars', doer)}")
    move = pair(mover, doer)
    point = [f"{p} 即 Lagna 主" if p == first else f"{p}–{first}：{rel(p, first)}"
             for p in dict.fromkeys((doer, starter, mover)) if rel(p, first)]
    to_first, to_doer = _touches(chart, "Mars", first), _touches(chart, "Mars", doer)
    if to_first and to_doer and "Mars" not in (first, doer) and doer != first:
        point.append(f"经 Mars 串联（Mars–{first}：{to_first}；Mars–{doer}：{to_doer}）")
    weak = [f"{h}宫主" for h in dict.fromkeys((actor, _derived(actor, 3)))
            if _lord_ability(chart, h)[3] == "严重受损"]
    if not start:
        verdict = "盘面未见主动"
    elif not point:
        verdict = "有起意未指向你"
    elif weak:
        verdict = "有心无力"
    else:
        verdict = "偏会" if move else "偏会·停在念头或言语"
    return start, move, point, weak, verdict


ACTION_KARAKAS = [("Mars", "勇气"), ("Mercury", "言语、学识"), ("Venus", "情意"),
                  ("Sun", "君主、官方"), ("Jupiter", "智力")]


def _chain_lines(chart):
    lagna_sign = chart["lagna"]["sign"]
    lord = lambda house: chart["house_lords"][house]["lord"]
    lines = ["### 行动者视角（转宫）与行动链（行动型问题输入）\n"]
    lines.append(
        "> 以行动者所在的宫为命宫取第 n 宫（M-XVII.8–9、M-XIV.116 注）：起第 2 宫言语、第 3 宫起意、"
        "第 7 宫情意的对象、第 10 宫行动、第 11 宫落实。本盘该宫原来的宫义照常存在。"
        "行动链只回答“行动者会不会动”，不进账本合计（`judgment-rubric.md` §2.5）。\n"
    )
    lines.append("| 行动者 | 言语（起第2宫） | 起意（起第3宫） | 情意对象（起第7宫） | 行动（起第10宫） | 落实（起第11宫） |")
    lines.append("|---|---|---|---|---|---|")
    cell = lambda h: f"{h}宫（{lord(h)}·{_lord_ability(chart, h)[3]}）"
    for actor in range(2, 13):
        lines.append(
            f"| {actor}宫（{lord(actor)}） | "
            + " | ".join(cell(_derived(actor, n)) for n in (2, 3, 7, 10, 11)) + " |"
        )
    lines.append("")
    lines.append("| 行动者 | ① 起意 | ② 行动 | ③ 指向你（Lagna 主） | ④ 严重受损 | 行动链 |")
    lines.append("|---|---|---|---|---|---|")
    for actor in range(2, 13):
        start, move, point, weak, verdict = _action_chain(chart, actor)
        lines.append(
            f"| {actor}宫 | {'；'.join(start) or '—'} | {move or '—'} | "
            f"{'；'.join(point) or '—'} | {'、'.join(weak) or '—'} | {verdict} |"
        )
    lines.append("")
    lines.append(
        "> 征象星串联（执行口径，B 级）：征象星与两端都同宫或由它照射，算连上，写“经某星串联”。"
        "只认所问动作的征象星（`question-decomposition.md` 投射表）。Mercury、Venus、Sun 只有第七宫照射，"
        "它们串得起的两端必已直连；串联在这里说明“靠什么连上”。\n"
    )
    lines.append("| 征象星（象义） | 触及的宫主（同宫或由它照射） | 与 Lagna 主一起串起的宫 |")
    lines.append("|---|---|---|")
    first = lord(1)
    for karaka, meaning in ACTION_KARAKAS:
        touched = []
        for planet in dict.fromkeys(lord(h) for h in range(1, 13)):
            how = _touches(chart, karaka, planet)
            if how and how != "即本星":
                houses = "、".join(map(str, sorted(_houses_ruled_from(planet, lagna_sign))))
                touched.append(f"{planet}（管{houses}；{how}）")
        if karaka == first:
            bridged = "即 Lagna 主"
        elif not _touches(chart, karaka, first):
            bridged = "—（不触及 Lagna 主）"
        else:
            bridged = "、".join(
                f"{h}（{lord(h)}）" for h in range(2, 13)
                if lord(h) not in (first, karaka) and _touches(chart, karaka, lord(h))
            ) or "—"
        lines.append(f"| {karaka}（{meaning}） | {'、'.join(touched) or '—'} | {bridged} |")
    lines.append("")
    return lines


def _lord_lines(chart):
    lines = ["### 宫主能力与连接（能力层、意愿层输入）\n"]
    lines.append(
        "> 能力层：按 M-XIV.39–40 与 M-XIV.30（只取作用于宫主自身的几项）列折损项与救应。"
        "燃烧、逆行只算折损，不单独算无力；只有多项叠加且无救应才记“严重受损”。"
        "本表不进账本合计，“严重受损”只用于 `judgment-rubric.md` 能力层否决。\n"
    )
    lines.append("| 宫 | 宫主 | 宫主落宫（星座） | D1尊贵度 | 折损项 | 救应 | 能力 |")
    lines.append("|---:|---|---|---|---|---|---|")
    dignity = chart.get("dignity", {})
    for house in range(1, 13):
        planet, factors, rescue, verdict = _lord_ability(chart, house)
        data = chart["planets"][planet]
        lines.append(
            f"| {house} | {planet} | {data['house']}（{data['sign']}） | "
            f"{dignity.get(planet, {}).get('basic', '—')} | {'、'.join(factors) or '—'} | "
            f"{'、'.join(rescue) or '—'} | {verdict} |"
        )
    lines.append("")
    lines.append(
        "> 意愿层：按 M-XIV.33／47／48 取象、M-XIV.43 看与 Lagna 主的连接。这里只列事实："
        "同宫与照射之星各管哪几宫（从 Lagna 起）；与 Lagna 主的连接按 M-XIV.43 列同宫、照射"
        "（单向即可，写明谁照谁）、互照、互换、互为4/10宫（角宫关系）。"
        "同宫、照射之星按“带来什么、这题要不要、有没有力送到”读（`house-meanings.md` §5）；"
        "本表不进账本合计。\n"
    )
    lines.append("| 宫 | 宫主 | 同宫之星（所管宫） | 照射宫主之星（所管宫） | 与 Lagna 主 |")
    lines.append("|---:|---|---|---|---|")
    for house in range(1, 13):
        planet, joined, aspecting, link = _lord_links(chart, house)
        lines.append(f"| {house} | {planet} | {joined} | {aspecting} | {link} |")
    lines.append("")
    return lines


def _navamsa_number(degree):
    return min(int(degree // (30 / 9)), 8) + 1


def _shadvarga_signs(sign, degree):
    """Lagna 落在 sign 的 degree 度时，六分盘各自的星座。"""
    si = SIGNS.index(sign)
    odd = si % 2 == 0
    trimsamsa = TRIMSAMSA_ODD if odd else TRIMSAMSA_EVEN
    return {
        "D1": sign,
        "D2": "Leo" if (degree < 15) == odd else "Cancer",
        "D3": SIGNS[(si + 4 * min(int(degree // 10), 2)) % 12],
        "D9": SIGNS[(si + (0, 8, 4)[si % 3] + _navamsa_number(degree) - 1) % 12],
        "D12": SIGNS[(si + min(int(degree // 2.5), 11)) % 12],
        "D30": next(s for bound, s in trimsamsa if degree < bound),
    }


def _shadvarga_cuts(sign):
    """六分盘各自在本座内的分界度数（不含 0° 与 30°）。"""
    trimsamsa = TRIMSAMSA_ODD if SIGNS.index(sign) % 2 == 0 else TRIMSAMSA_EVEN
    return {
        "D1": [],
        "D2": [15.0],
        "D3": [10.0, 20.0],
        "D9": [k * 30 / 9 for k in range(1, 9)],
        "D12": [k * 2.5 for k in range(1, 12)],
        "D30": [float(bound) for bound, _ in trimsamsa[:-1]],
    }


def _shadvarga_majority(chart, sign, degree):
    """座主对 Lagna 星座的功能吉凶计数：(吉, 凶, 多数)；“盈月未定”不计。"""
    roles = [_ayer_role(chart, SIGN_LORDS[s], sign) for s in _shadvarga_signs(sign, degree).values()]
    good = sum(role.startswith("吉") for role in roles)
    bad = sum(role.startswith("凶") for role in roles)
    return good, bad, "多吉" if good > bad else "多凶" if bad > good else "相等"


def _shadvarga_critical(chart, sign, degree):
    """Lagna 在本座内前后移动多少度，六分盘多数会变；本座内都不变时返回 None。"""
    base = _shadvarga_majority(chart, sign, degree)[2]
    cuts = sorted({c for values in _shadvarga_cuts(sign).values() for c in values})
    found = []
    for c in (c for c in cuts if c > degree):
        if _shadvarga_majority(chart, sign, c + 1e-9)[2] != base:
            found.append(c - degree)
            break
    for c in (c for c in reversed(cuts) if c <= degree):
        if _shadvarga_majority(chart, sign, c - 1e-9)[2] != base:
            found.append(degree - c)
            break
    return min(found) if found else None


def _shadvarga_lines(chart):
    lagna = chart["lagna"]
    sign, degree = lagna["sign"], lagna["degree"]
    signs = _shadvarga_signs(sign, degree)
    lines = ["### Lagna 六分盘座主（`P-I.4` 注）\n"]
    engine_charts = chart.get("divisional_charts", {})
    problems = []
    for key in ("D3", "D9", "D12", "D30"):
        entry = engine_charts.get(key)
        if not entry:
            problems.append(f"{key} 缺失（engine 未给出该分盘）")
        elif "error" in entry:
            problems.append(f"{key} 出错（{entry['error']}）")
        elif "Lagna" not in entry:
            problems.append(f"{key} 缺失 Lagna 行")
        elif entry["Lagna"]["sign"] != signs[key]:
            edge = min(abs(degree - c) for c in _shadvarga_cuts(sign)[key] + [0.0, 30.0])
            problems.append(
                f"{key} 不一致（engine {entry['Lagna']['sign']}／公式 {signs[key]}；"
                f"Lagna {sign} {degree:.4f}°，距本分盘分界 {edge:.4f}°）"
            )
    if problems:
        lines.append(
            f"- 六分盘 unavailable：{'；'.join(problems)}。凡与 engine 分盘不一致，不得手推补造；"
            "`P-I.4` 本盘不读 varga 一项，在输入栏写明。"
        )
        lines.append("")
        return lines
    lines.append("| 分盘 | 星座 | 座主 | 座主对 Lagna 星座的功能吉凶 | 距本分盘座内分界 |")
    lines.append("|---|---|---|---|---|")
    for key, cuts in _shadvarga_cuts(sign).items():
        lord = SIGN_LORDS[signs[key]]
        edge = f"{min(abs(degree - c) for c in cuts):.3f}°" if cuts else "见“Lagna 距 sign 边界”"
        lines.append(
            f"| {SHADVARGA_NAMES[key]} | {signs[key]} | {lord} | "
            f"{_ayer_role(chart, lord, sign)} | {edge} |"
        )
    good, bad, majority = _shadvarga_majority(chart, sign, degree)
    critical = _shadvarga_critical(chart, sign, degree)
    critical_text = (
        f"{critical:.3f}°" if critical is not None else "本座内不变（只看 Lagna 距 sign 边界）"
    )
    lines.append("")
    lines.append(f"- 合计：吉 {good}、凶 {bad}、不计 {6 - good - bad} → **{majority}**")
    lines.append(f"- 六分盘多数临界距离：{critical_text}（Lagna 前移或后移这么多，多数结论会变）")
    lines.append(
        "- 用途边界：只供 `P-I.4` “falls in a benefic's varga”：多吉＝落吉 varga，"
        "多凶＝落凶 varga，相等不计（数法见 `judgment-rubric.md` §4.1）；"
        "禁止由此展开 D2、D3、D9、D12、D30 解读。"
    )
    lines.append("")
    return lines


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
        "> 只在 `question-taxonomy.md` §2.10 描述题、§2.11 天气题消费；描述输出不进内部三档。"
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
        lines.append(
            f"| rising Navamsa | {d9_lagna['sign']} {d9_lagna['degree']:.4f}°"
            f"（本座第 {_navamsa_number(lagna['degree'])} 个 Navamsa） | "
            "仅用于 P-I.7、P-VI.1、P-VI.4、P-VII.13；座主吉凶见下表六分盘；"
            "禁止展开完整 D9 人生解读 |"
        )
    else:
        lines.append("| rising Navamsa | unavailable | 不得手推补造 |")
    lines.append("")
    lines.extend(_shadvarga_lines(chart))

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

    lines.extend(_lord_lines(chart))
    lines.extend(_chain_lines(chart))
    lines.extend(_descriptive_facts(chart, d9_lagna))

    lines.append("### 时间边界\n")
    lines.append(
        "> 本文件不含时间。标准层定为偏成或持平后，时间副层另写 timing_overlay.md"
        "（resources/timing-layer.md）；偏不成档不给时间。提问盘生成的120年 Vimshottari、"
        "Chara Dasha、当前过运均不作为 Prashna 时间。\n"
    )
    return "\n".join(lines)
