"""prashna_rules.py — 即时盘标准层判定：规则、事项登记、成事账、能力否决、行动链、限定语。

判档规则只在这里实现一份（2026-10-29 重建，PRASHNA_REBUILD_PLAN_20261029）。模型负责取象（写取象单），
本模块只读盘面事实与取象单计数，不读问题原文。skill 文本（judgment-rubric.md、matter-rules.md）讲方法与出处，
与本文件一一对应；dev 基础率与小工具都以本文件为准。

盘面事实取自共享 engine 的 chart（prashna_time.calculate_prashna_chart），吉凶标签、能力、连接、行动链
直接调用 format_prashna_standard 的同一函数，与 structured_prashna.md 同源。
"""
from __future__ import annotations

from dataclasses import dataclass, field

import format_prashna_standard as F

P7 = F.CLASSICAL_PLANETS
MOV, FIX = F.MOVABLE_SIGNS, F.FIXED_SIGNS
HEAD_I4 = {"Gemini", "Leo", "Virgo", "Libra", "Scorpio", "Aquarius"}  # P-I.4 头升
BACK_I4 = {"Aries", "Taurus", "Cancer", "Sagittarius", "Capricorn"}  # P-I.4 背升；Pisces 双升
HEAD_VI3 = {"Leo", "Virgo", "Libra", "Scorpio", "Aquarius"}  # P-VI.3 Ayer 注列表，无 Gemini（两说）
HUMAN_III3 = {"Gemini", "Virgo", "Libra", "Aquarius"}  # P-III.3 注
HUMAN_IV2 = {"Gemini", "Libra", "Aquarius"}  # P-IV.2 正文
KENDRA, TRIKONA = (1, 4, 7, 10), (5, 9)
FAV, UNF = ("fav", "fav_d"), ("unf", "unf_lean")
DIRECTION_TEXT = {"fav": "有利", "fav_d": "有利（吉占优，困难后成）", "unf": "不利", "unf_lean": "不利（凶占优）",
                  "mixed": "混合", "none": "无方向"}


def score(direction):
    return 1 if direction in FAV else -1 if direction in UNF else 0


def _d(good, bad):
    return "mixed" if good and bad else "fav" if good else "unf" if bad else "none"


def _count(good, bad):
    """rubric §4.1 偈内占优：吉多记有利（困难后成），凶多记不利，相等记混合。"""
    return "fav_d" if good > bad else "unf_lean" if bad > good else "mixed"


# ---------------------------------------------------------------------------
# 盘面事实
# ---------------------------------------------------------------------------
class Facts:
    """chart 的只读视图。吉凶标签按被占据／照射的星座起算（standard-layer §2.1，formatter 同一函数）。"""

    def __init__(self, chart, needed=()):
        self.chart = chart
        self.lsign = chart["lagna"]["sign"]
        self.ldeg = chart["lagna"]["degree"]
        self.house = {n: chart["planets"][n]["house"] for n in P7}
        self.basic = {n: chart["dignity"][n]["basic"] for n in P7}
        self.waxing = bool(chart["moon_phase"]["waxing"])
        self.needed = set(needed)  # D3：措辞点到的征象星，P-I.3 不按凶星计

    def sign(self, h):
        return self.chart["house_lords"][h]["sign"]

    def lord(self, h):
        return self.chart["house_lords"][h]["lord"]

    def role(self, planet, sign):
        return F._ayer_role(self.chart, planet, sign)

    def cls(self, planet, sign):
        r = self.role(planet, sign)
        return "B" if r.startswith("吉") else "M" if r.startswith("凶") else "U"

    def occ(self, h):
        return [(n, self.cls(n, self.sign(h))) for n in F._occupants(self.chart, h, P7)]

    def asp(self, h):
        return [(n, self.cls(n, self.sign(h))) for n in F._classical_aspecting_house(self.chart, h)]

    def both(self, h):
        return self.occ(h) + self.asp(h)

    def sees(self, a, b):
        return F._sees(self.chart, a, b)

    def mutual(self, a, b):
        return self.sees(a, b) and self.sees(b, a)

    def text(self, h, cols=("occ", "asp")):
        """证据文字：宫、星座、占据与照射之星及其标签。"""
        parts = []
        if "occ" in cols:
            o = F._occupants(self.chart, h, P7)
            parts.append("占据 " + (F._labelled(self.chart, o, self.sign(h)) if o else "—"))
        if "asp" in cols:
            a = F._classical_aspecting_house(self.chart, h)
            parts.append("照射 " + (F._labelled(self.chart, a, self.sign(h)) if a else "—"))
        return f"{h} 宫 {self.sign(h)}：" + "；".join(parts)


def _any(pairs, c):
    return any(k == c for _, k in pairs)


def _bm(pairs):
    return sum(k == "B" for _, k in pairs), sum(k == "M" for _, k in pairs)


def _half(f):
    """双体座：前半按固定座、后半按动座（P-II.1~2 注引 Bhattotpala）。"""
    if f.lsign in FIX:
        return "fixed"
    if f.lsign in MOV:
        return "movable"
    return "fixed" if f.ldeg < 15 else "movable"


# ---------------------------------------------------------------------------
# 条目
# ---------------------------------------------------------------------------
@dataclass
class Entry:
    rule_id: str
    level: str  # A／B／B（类比）／B（通用环境）
    reason: str  # 适用理由
    direction: str
    evidence: str
    alt: str | None = None  # 两说的第二读法方向（rubric §2.4）
    note: str = ""
    houses: frozenset = frozenset()  # 本条触发时读到的宫（D4 语境检验用）
    excluded: str = ""  # 不入账的原因（语境不合等）；非空时不计分

    @property
    def score(self):
        return 0 if self.excluded else score(self.direction)


# ---------------------------------------------------------------------------
# 规则（每条注明出处；执行口径见 judgment-rubric.md、matter-rules.md）
# ---------------------------------------------------------------------------
def p_i3(f, h):
    """P-I.3：事项宫受本宫主或吉星占照则增强，受凶星则减损。D3：措辞点到的征象星不按凶星计。"""
    pairs = [(n, k) for n, k in f.both(h) if not (k == "M" and n in f.needed)]
    b, m = _bm(pairs)
    skipped = [n for n, k in f.both(h) if k == "M" and n in f.needed]
    note = f"所需征象星 {'、'.join(skipped)} 不按凶星计（按问题读）" if skipped else ""
    return _d(b > 0, m > 0), f.text(h), note


def six_majority(f):
    good, bad, verdict = F._shadvarga_majority(f.chart, f.lsign, f.ldeg)
    return {"多吉": "B", "多凶": "M"}.get(verdict, "T"), f"六分盘座主 吉 {good}／凶 {bad}（{verdict}）"


def p_i4(f):
    """P-I.4：(1) Lagna 有吉星占或落吉 varga（六分盘多数）；(2) 头升座。两条同向定方向，否则按第 1 宫标签与六分盘
    合计一条数占优（rubric §4.1）。"""
    occ = f.occ(1)
    v, vtext = six_majority(f)
    c1 = _d(_any(occ, "B") or v == "B", _any(occ, "M") or v == "M")
    c2 = "fav" if f.lsign in HEAD_I4 else "unf" if f.lsign in BACK_I4 else "mixed"
    ev = f"Lagna {f.lsign} {f.ldeg:.2f}°（{'头升' if c2 == 'fav' else '背升' if c2 == 'unf' else '双升'}）；{f.text(1)}；{vtext}"
    if c1 == "fav" and c2 == "fav":
        return "fav", ev
    if c1 == "unf" and c2 == "unf":
        return "unf", ev
    b, m = _bm(f.both(1))
    return _count(b + (v == "B"), m + (v == "M")), ev


def p_iv1(f):
    """P-IV.1：吉星落角宫、三方宫且凶星不落角宫与 8 宫则兴；凶星落角宫与 8 宫、吉星落别处则衰。"""
    good = any(_any(f.occ(h), "B") for h in KENDRA + TRIKONA)
    bad = any(_any(f.occ(h), "M") for h in KENDRA + (8,))
    ev = "；".join(f.text(h, ("occ",)) for h in (1, 4, 7, 10, 5, 9, 8))
    return _d(good, bad) if good or bad else "none", ev


def p_iv3(f):
    """P-IV.3：吉星落 10、7 宫赐位置；凶星落 12、11 宫不吉；亏月 Moon 在 Lagna 不利，Moon 在 10 宫不论盈亏有利。"""
    fav = _any(f.occ(7), "B") or any(k == "B" for n, k in f.occ(10) if n != "Moon") or f.house["Moon"] == 10
    unf = _any(f.occ(11), "M") or _any(f.occ(12), "M") or (f.house["Moon"] == 1 and not f.waxing)
    ev = "；".join(f.text(h, ("occ",)) for h in (10, 7, 11, 12)) + f"；Moon {f.house['Moon']} 宫、{'盈' if f.waxing else '亏'}月"
    return _d(fav, unf), ev


def p_iv3_fame(f):
    """P-IV.3 后半：吉星落 2、5、1 宫得名利（名誉题辅助）。"""
    fav = any(_any(f.occ(h), "B") for h in (2, 5, 1))
    return ("fav" if fav else "none"), "；".join(f.text(h, ("occ",)) for h in (2, 5, 1))


II1_GOOD = {"位置": "fixed", "住处": "fixed", "名誉": "fixed", "失物": "fixed",
            "疾病": "movable", "出行": "movable", "归来": "movable", "变动": "movable"}
II1_NOTE = {"位置": "固定座得位，动座不得", "住处": "固定座得住处", "名誉": "固定座保全，动座受辱",
            "失物": "固定座一时找不到、未丢，动座难寻回", "疾病": "固定座难愈，动座易愈",
            "出行": "动座成行，固定座不行", "归来": "动座在途、记有利；固定座不来", "变动": "动座变动成立"}


def p_ii1(f, kind):
    """P-II.1~2 注：动／固座；变动座前半按固定座、后半按动座。"""
    like = _half(f)
    ev = f"Lagna {f.lsign} {f.ldeg:.2f}°（{F._modality(f.lsign)}{'，按' + ('前' if f.ldeg < 15 else '后') + '半' if f.lsign not in MOV | FIX else ''}）"
    return ("fav" if like == II1_GOOD[kind] else "unf"), ev, II1_NOTE[kind]


def p_ii2(f):
    """P-II.2：吉星照 Lagna 与 Moon-lagna 吉，凶星照则凶，吉凶同照为混合（只看照射列）。"""
    mh = f.house["Moon"]
    pairs = f.asp(1) + (f.asp(mh) if mh != 1 else [])
    b, m = _bm(pairs)
    return _d(b > 0, m > 0), f.text(1, ("asp",)) + ("" if mh == 1 else "；Moon-lagna " + f.text(mh, ("asp",)))


def p_ii5(f):
    """P-II.5：动座上升有吉星占利行人、凶星占害；固定座上升有凶星占，行人亦平安；都不满足不出方向。"""
    occ = f.occ(1)
    if f.lsign in MOV:
        return _d(_any(occ, "B"), _any(occ, "M")), f.text(1, ("occ",))
    if f.lsign in FIX and _any(occ, "M"):
        return "fav", f.text(1, ("occ",))
    return "none", f.text(1, ("occ",))


def p_ii9(f):
    """P-II.9：动座上升且 Sun／Saturn／Mercury／Venus 之一占据则很快出发；该星逆行则否（按点名）。
    两说：Sun 只免逆行判断（读法一），或整体不计入（读法二）。"""
    if f.lsign not in MOV:
        return "none", "none", f"Lagna {f.lsign} 非动座"
    def read(names):
        on = [n for n in names if f.house[n] == 1]
        if not on:
            return "none"
        return "unf" if all(f.chart["planets"][n].get("retrograde") for n in on) else "fav"
    on = [n for n in ("Sun", "Saturn", "Mercury", "Venus") if f.house[n] == 1]
    return read(("Sun", "Saturn", "Mercury", "Venus")), read(("Saturn", "Mercury", "Venus")), \
        f"Lagna {f.lsign}（动座）；落 Lagna 的点名星 {'、'.join(on) or '—'}"


def p_ii11(f):
    """P-II.11：Sun 与 Moon 落 4 宫则不来；Mercury、Jupiter 与 Venus 落 4 宫则很快来（按字面同落）。"""
    on = {n for n in P7 if f.house[n] == 4}
    d = "unf" if {"Sun", "Moon"} <= on else "fav" if {"Mercury", "Jupiter", "Venus"} <= on else "none"
    return d, f.text(4, ("occ",))


def p_iii1(f):
    """P-III.1：吉星落 10、1、7 宫则胜；9 宫按功能吉凶，凶败吉胜（注：点名只是象征）。"""
    fav = any(_any(f.occ(h), "B") for h in (10, 1, 7, 9))
    return _d(fav, _any(f.occ(9), "M")), "；".join(f.text(h, ("occ",)) for h in (10, 1, 7, 9))


def p_iii34(f):
    """P-III.3~4：人形座上升有吉星、吉星落 12／11 宫、吉星落角宫、人形 Lagna 受吉星照则和解；凶星落动座则冲突，
    凶星同样落位受凶星照则相反；吉凶混落按 1／4／7／10 宫数占优（III.4 注）。"""
    human = f.lsign in HUMAN_III3
    fav = (human and _any(f.occ(1), "B")) or any(_any(f.occ(h), "B") for h in (11, 12) + KENDRA) \
        or (human and _any(f.asp(1), "B"))
    unf = any(f.sign(h) in MOV and _any(f.occ(h), "M") for h in range(1, 13)) \
        or any(_any(f.occ(h), "M") and _any(f.asp(h), "M") for h in KENDRA + (11, 12))
    ev = f"Lagna {f.lsign}{'（人形座）' if human else ''}；" + "；".join(f.text(h) for h in (1, 4, 7, 10, 11, 12))
    used = frozenset(h for h in (11, 12) if _any(f.occ(h), "B"))
    if fav and unf:
        return _count(*_bm([x for h in KENDRA for x in f.both(h)])), ev, used
    return _d(fav, unf), ev, used


def p_iv2(f):
    """P-IV.2：吉星落 3／5／11／7 宫得益、凶星则损，照射等同占据；吉星落人形座（正文 Libra、Gemini、Aquarius）亦吉。"""
    hs = (3, 5, 11, 7)
    fav = any(_any(f.both(h), "B") for h in hs) or any(k == "B" and f.chart["planets"][n]["sign"] in HUMAN_IV2
                                                      for h in range(1, 13) for n, k in f.occ(h))
    unf = any(_any(f.both(h), "M") for h in hs)
    return _d(fav, unf), "；".join(f.text(h) for h in hs)


def p_iv5(f):
    """P-IV.5：吉星落 Lagna／7／8／5 宫且彼此相照、Moon 落 3／6／10／11 宫则愈；凶星落这些宫且 Moon 落别处则相反；
    配置不全看占优（注）。同宫不算互照，只有一颗吉星不算满足。"""
    hs = (1, 7, 8, 5)
    mg = f.house["Moon"] in (3, 6, 10, 11)
    occ = [x for h in hs for x in f.occ(h) if x[0] != "Moon"]
    ben = [n for n, k in occ if k == "B"]
    mutual = len(ben) >= 2 and all(f.mutual(a, b) for i, a in enumerate(ben) for b in ben[i + 1:])
    bo, mo = _any(occ, "B"), _any(occ, "M")
    ev = "；".join(f.text(h) for h in hs) + f"；Moon {f.house['Moon']} 宫"
    if bo and mutual and not mo and mg:
        return "fav", ev
    if mo and not bo and not mg:
        return "unf", ev
    b, m = _bm([x for h in hs for x in f.both(h)])
    return _count(b + mg, m + (not mg)), ev


def p_v1(f, person):
    """P-V.1：行星落 5／2／3 宫则离者返回；吉星落此则失物复得（不满足不出方向）。"""
    hs = (5, 2, 3)
    hit = any(f.occ(h) for h in hs) if person else any(_any(f.occ(h), "B") for h in hs)
    return ("fav" if hit else "none"), "；".join(f.text(h, ("occ",)) for h in hs)


def p_v2(f):
    """P-V.2：7 或 6 宫有星、Jupiter 落角宫、Mercury／Venus 落三方宫，离者返回（按点名）。
    两说：任一满足（或）／全部满足（且）。不满足不出方向。"""
    conds = [bool(f.occ(7) or f.occ(6)), f.house["Jupiter"] in KENDRA,
             f.house["Mercury"] in TRIKONA or f.house["Venus"] in TRIKONA]
    ev = f"6／7 宫有星 {'是' if conds[0] else '否'}；Jupiter {f.house['Jupiter']} 宫；Mercury {f.house['Mercury']}、Venus {f.house['Venus']} 宫"
    return ("fav" if any(conds) else "none"), ("fav" if all(conds) else "none"), ev


def p_v3(f):
    """P-V.3：Moon 落 8 宫且角宫无凶星则平安返回（注：Moon 不可弱，D1 debilitated 算弱）。"""
    ok = f.house["Moon"] == 8 and f.basic["Moon"] != "debilitated" and not any(_any(f.occ(h), "M") for h in KENDRA)
    return ("fav" if ok else "none"), f"Moon {f.house['Moon']} 宫（{f.basic['Moon']}）；角宫凶星占据 " \
        f"{'有' if any(_any(f.occ(h), 'M') for h in KENDRA) else '无'}", frozenset({8}) if ok else frozenset()


def p_iii5(f):
    """P-III.5：Jupiter 或 Venus 落 Lagna 起 2／3 宫，远方之人很快到来（按点名）。"""
    ok = f.house["Jupiter"] in (2, 3) or f.house["Venus"] in (2, 3)
    return ("fav" if ok else "none"), f"Jupiter {f.house['Jupiter']} 宫；Venus {f.house['Venus']} 宫"


def p_vi3(f):
    """P-VI.3：满月或吉星占 Lagna、头升座上升受吉星照、或强吉星落 11 宫则速得；皆无则渺茫。
    两说：Gemini 是否头升（Ayer 注列表无 Gemini）。"""
    strong11 = any(k == "B" and f.basic[n] in F.STRONG_BASIC for n, k in f.occ(11))
    fullwin = F.tithi_facts(f.chart["planets"]["Sun"]["longitude"], f.chart["planets"]["Moon"]["longitude"])[1]
    a = (fullwin and f.house["Moon"] == 1) or _any(f.occ(1), "B")
    rising = _any(f.asp(1), "B")
    read = lambda heads: "fav" if a or (f.lsign in heads and rising) or strong11 else "unf"
    ev = f"Lagna {f.lsign}；{f.text(1)}；11 宫强吉星 {'有' if strong11 else '无'}；满月窗 {'是' if fullwin else '否'}"
    alt = read(HEAD_VI3 | {"Gemini"}) if f.lsign == "Gemini" else None
    return read(HEAD_VI3), alt, ev


def p_vii1(f, asker):
    """P-VII.1：Saturn 落 Lagna 起奇数宫（不计 Lagna）兼示得新娘，否则得新郎；问娶看前者，问嫁看后者。"""
    bride = f.house["Saturn"] in (3, 5, 7, 9, 11)
    return ("fav" if bride == (asker == "男") else "unf"), f"Saturn {f.house['Saturn']} 宫"


def p_vii2(f):
    """P-VII.2：Moon 落 3／5／7／11／6 宫受吉星照，或吉星落角宫／三方宫，议婚能成；其余为否（按标签）。"""
    mh = f.house["Moon"]
    a = mh in (3, 5, 7, 11, 6) and _any(f.asp(mh), "B")
    b = any(_any(f.occ(h), "B") for h in KENDRA + TRIKONA)
    return ("fav" if a or b else "unf"), f"Moon {mh} 宫：" + f.text(mh, ("asp",)) + "；角宫、三方宫吉星占据 " + ("有" if b else "无")


def chyuti(f):
    """P-I.2 Chyuti（Lagna）：动座且受本宫主或吉星占照、无凶星则变动成立；固定座不变；变动座按吉凶多寡（§4.1）。"""
    b, m = _bm(f.both(1))
    if f.lsign in MOV:
        d = "fav" if b and not m else "unf"
    elif f.lsign in FIX:
        d = "unf"
    else:
        d = "fav" if b > m else "unf" if m > b else "mixed"
    return d, f"Lagna {f.lsign}（{F._modality(f.lsign)}）；{f.text(1)}"


def vriddhi(f):
    """P-I.2 Vriddhi（4 宫）：受本宫主或吉星占照且未受破坏则兴；同时有凶星记混合（执行口径）。"""
    b, m = _bm(f.both(4))
    return _d(b > 0, m > 0), f.text(4)


def pravasa(f):
    """P-I.2 Pravasa（10 宫）：动座且受凶星照才成行；受本宫主或吉星照则否（原文 only when）。"""
    b, m = _bm(f.asp(10))
    return ("fav" if f.sign(10) in MOV and m and not b else "unf"), f.text(10, ("asp",))


def nivritti(f):
    """P-I.2 Nivritti（7 宫）：动座且受本宫主或吉星照则返回，受凶星照则否；非动座不出方向。"""
    if f.sign(7) not in MOV:
        return "none", f"7 宫 {f.sign(7)} 非动座"
    b, m = _bm(f.asp(7))
    return _d(b > 0, m > 0), f.text(7, ("asp",))


def return_4th(f):
    """P-I.2 在外者返回另看 4 宫。两说：正文"有行星落 4 宫"／注"4 宫主占据或照 4 宫，否则不回"。"""
    lord = f.lord(4)
    a = "fav" if f.occ(4) else "none"
    b = "fav" if f.house[lord] == 4 or 4 in f.chart["graha_drishti"].get(lord, {}).get("aspected_houses", []) else "unf"
    return a, b, f.text(4) + f"；4 宫主 {lord} 落 {f.house[lord]} 宫"


def x5(f):
    """M-XVII.5：7 宫有吉星为好。"""
    return ("fav" if _any(f.occ(7), "B") else "none"), f.text(7, ("occ",))


def x15(f):
    """M-XVII.15：受克 Moon 落 Lagna 起偶数宫且亏月则不成；Moon 落 8 宫有阻。"""
    mh = f.house["Moon"]
    aff = any(k == "M" for n, k in f.occ(mh) if n != "Moon") or _any(f.asp(mh), "M")
    if mh == 8:
        return "unf", f"Moon 落 8 宫", frozenset({8})
    d = "unf" if aff and mh % 2 == 0 and not f.waxing else "none"
    return d, f"Moon {mh} 宫（{'偶' if mh % 2 == 0 else '奇'}数宫）、{'受克' if aff else '未受克'}、{'盈' if f.waxing else '亏'}月", frozenset()


def x16(f, with_link):
    """M-XVII.16：Lagna 主与 7 宫主、或与 Venus 互换、入旺、互照则成。
    with_link=False：去掉与 S4 连接同源的"Lagna 主与 7 宫主互换、互照"，只留入旺与 Venus 部分（D2）。"""
    l1, l7 = f.lord(1), f.lord(7)
    def swap(a, b):
        return f.chart["planets"][a]["sign"] in [s for s, q in F.SIGN_LORDS.items() if q == b] and \
            f.chart["planets"][b]["sign"] in [s for s, q in F.SIGN_LORDS.items() if q == a]
    ok, why = False, []
    for b in (l7, "Venus"):
        if b == l1:
            continue
        link = swap(l1, b) or f.mutual(l1, b)
        if link and (with_link or b == "Venus"):
            ok = True; why.append(f"{l1}–{b} 互换或互照")
        for p in (l1, b):
            if f.basic[p] == "exalted":
                ok = True; why.append(f"{p} 入旺")
    return ("fav" if ok else "none"), f"Lagna 主 {l1}，7 宫主 {l7}：" + ("、".join(dict.fromkeys(why)) or "不满足")


def x17(f):
    """M-XVII.17：8 宫凶星受凶星照且落陷或落敌座则不成；在 6 宫则因病或亲属争执告吹。"""
    for h in (8, 6):
        for n, k in f.occ(h):
            if k == "M" and f.basic[n] in ("debilitated", "enemy", "great_enemy") and _any(f.asp(h), "M"):
                return "unf", f.text(h) + f"（{n} {f.basic[n]}）", frozenset({h})
    return "none", "6、8 宫无受凶星照的落陷或敌座凶星", frozenset()


# ---------------------------------------------------------------------------
# 事项登记（matter-rules.md 的代码面；改这里必须同改文本）
# ---------------------------------------------------------------------------
@dataclass
class Matter:
    house: int | None  # None＝取取象单的 matter_house（见面题取行动者的宫、通用题由模型定）
    level: str
    rules: tuple  # 本事古法（S5）与已写明的辅助规则；P-I.3 已按同源规则列入或排除
    has_i4: bool = False  # 本事规则已含 P-I.4，不再加通用 P-I.4
    timing: str = "general"  # general／return／none


MATTERS = {
    "复合": Matter(7, "B", ("III34*", "PI3")),
    "表白": Matter(7, "B", ("I4", "PI3", "X5*", "X15*", "X16*", "X17*"), has_i4=True),
    "恢复往来": Matter(7, "B", ("III34*", "PI3")),
    "见面": Matter(None, "B", ("I4", "PI3"), has_i4=True),  # 恋爱语境另加 X5*、X15*、X16*、X17*
    "挽回": Matter(1, "A", ("I4", "PI3"), has_i4=True),
    "同住归来": Matter(7, "A", ("NIV", "R4", "V1P", "V2", "V3", "III5", "II1:归来"), timing="return"),
    "结婚": Matter(7, "A", ("VII2", "VII1", "PI3", "X5", "X15", "X16", "X17")),
    "求职": Matter(10, "A", ("IV3", "II1:位置", "II2", "PI3")),
    "裁员": Matter(1, "A", ("CHY", "II1:变动")),  # Chyuti 与 1 宫 P-I.3 同源，不另计；问"保住"反向
    "竞争考试": Matter(1, "B", ("II1:位置", "II2", "III1", "PI3")),
    "达标考试": Matter(1, "A", ("I4", "PI3"), has_i4=True),
    "失物": Matter(11, "A", ("VI3", "V1O", "II1:失物", "PI3")),  # P-I.5 只讲快慢，不计分
    "走失宠物": Matter(11, "B", ("VI3", "V1O", "II1:失物", "PI3")),
    "买房": Matter(4, "A", ("VRI", "II1:住处", "I4"), has_i4=True),  # Vriddhi 与 4 宫 P-I.3 同源
    "出行办成": Matter(1, "A", ("I4", "PI3"), has_i4=True),
    "路上顺不顺": Matter(1, "A", ("II5",), timing="none"),  # II.5 与 1 宫 P-I.3 同读 Lagna 占据，同源
    "离开": Matter(10, "A", ("PRA", "II1:出行")),  # Pravasa 与 10 宫 P-I.3 反向同源；早日出发另加 II9
    "归来": Matter(7, "A", ("V1P", "V2", "V3", "III5", "NIV", "R4", "II1:归来"), timing="return"),
    "疾病": Matter(1, "A", ("IV5", "II1:疾病", "PI3")),
    "名誉": Matter(4, "A", ("VRI", "II1:名誉", "IV3F")),  # Nivritti 定对方能否得逞，方向待核，暂只进叙述
    "谈判": Matter(7, "A", ("III34", "PI3")),
    "投资": Matter(11, "B", ("IV2", "PI3")),
    "亏损补回": Matter(11, "B", ("V1O", "PI3")),
    "开庭": Matter(4, "B", ("II11", "PI3")),
    "合作": Matter(7, "B", ("PI3",)),
    "财富": Matter(None, "B", ("PI3",)),  # 2 或 11，按问题动词，由取象单给
    "子女行动": Matter(5, "B", ("PI3",)),
    "通用": Matter(None, "B", ("PI3",)),  # 题型表外：模型按宫义与关键词选事项宫并写明出处（D8）
    "描述": Matter(None, "B", (), timing="none"),  # 描述型（D15）：相处、氛围、局面；出事实不建账、不定档
}
LOVE_EXTRA = ("X5*", "X15*", "X16*", "X17*")
ANALOGY = {"III34*", "X5*", "X15*", "X16*", "X17*"}  # 类比偈：过语境检验（D4）
RULE_NAMES = {
    "PI3": "P-I.3", "I4": "P-I.4", "II1": "P-II.1", "IV1": "P-IV.1", "IV3": "P-IV.3", "IV3F": "P-IV.3（2／5／1 宫）",
    "II2": "P-II.2", "II5": "P-II.5", "II9": "P-II.9", "II11": "P-II.11", "III1": "P-III.1", "III34": "P-III.3~4",
    "III5": "P-III.5", "IV2": "P-IV.2", "IV5": "P-IV.5", "V1P": "P-V.1", "V1O": "P-V.1", "V2": "P-V.2", "V3": "P-V.3",
    "VI3": "P-VI.3", "VII1": "P-VII.1", "VII2": "P-VII.2", "CHY": "P-I.2 Chyuti", "VRI": "P-I.2 Vriddhi",
    "PRA": "P-I.2 Pravasa", "NIV": "P-I.2 Nivritti", "R4": "P-I.2 归来 4 宫", "X5": "M-XVII.5", "X15": "M-XVII.15",
    "X16": "M-XVII.16", "X17": "M-XVII.17", "S4": "M-XIV.43",
}


# ---------------------------------------------------------------------------
# 取象单
# ---------------------------------------------------------------------------
@dataclass
class Plan:
    """模型写的取象单（question-decomposition.md 第 7 节）。脚本只读这里，不读问题原文。"""
    matter: str
    matter_house: int | None = None
    context: str = ""  # "恋爱"：见面题加 M-XVII 四偈；限定语显隐定序第 1 序位
    actor: int | None = None  # 行动型问题的行动者宫
    needed_planets: tuple = ()  # "事情成不成"本身需要的征象星（D9；如竞争、手术要 Mars，官方录用要 Sun）。
    # 行动型问题"会不会动"的起意星（Mars）由行动链自行处理，不写在这里：一个子问题一个出口，
    # 行动要的冲劲不能拿来改答"成不成"的 P-I.3 与能力层。
    keywords: tuple = ()  # ({"word","houses","planets","polarity","source"}, ...)
    qualifiers: tuple = ()  # ("私下"／"公开"／"在家"／"在外"／"主动"／关键词名, ...)
    location: str = "city"  # city＝只给城市名；exact＝精确经纬度（输入提示的检查窗口，不改档）
    asker: str = ""  # 结婚题：男／女
    direction: str = "发生"  # 裁员题"会不会被裁"＝发生；"能不能保住"＝避免
    early_departure: bool = False  # 离开题问"能否早日出发"时加 P-II.9

    @classmethod
    def from_dict(cls, d):
        p = cls(**{k: (tuple(v) if isinstance(v, list) else v) for k, v in d.items()})
        p.validate()
        return p

    def validate(self):
        if self.matter not in MATTERS:
            raise ValueError(f"取象单 matter 不在事项登记：{self.matter}；表外问题用 '通用' 并给 matter_house")
        if MATTERS[self.matter].house is None and not self.house_of_matter():
            raise ValueError(f"{self.matter} 须给 matter_house（或行动者宫 actor）")
        bad = [p for p in self.needed_planets if p not in P7]
        if bad:
            raise ValueError(f"needed_planets 只收七曜：{bad}")
        for k in self.keywords:
            if k.get("polarity") not in ("相合", "相反"):
                raise ValueError(f"关键词 {k.get('word')} 的 polarity 须为 相合／相反")
            if not k.get("source"):
                raise ValueError(f"关键词 {k.get('word')} 未写出处")
        if self.matter == "结婚" and self.asker not in ("男", "女"):
            raise ValueError("结婚题须给 asker（男／女）")
        if self.matter == "描述" and self.qualifiers:
            raise ValueError("描述型不检验限定语：带条件的问法拆出事件型子问题另走成事账")
        if "主动" in self.qualifiers and not self.actor:
            raise ValueError("限定语'主动'须给行动者宫 actor")
        if self.location not in ("city", "exact"):
            raise ValueError("location 须为 city 或 exact")

    def house_of_matter(self):
        return self.matter_house or MATTERS[self.matter].house or self.actor

    def role_houses(self):
        """措辞点到且方向相合的宫：这些宫在本题拆题里另有角色（D3 能力层、D4 语境检验）。"""
        return {h for k in self.keywords if k["polarity"] == "相合" for h in k.get("houses", ())}


# ---------------------------------------------------------------------------
# 成事账
# ---------------------------------------------------------------------------
@dataclass
class Options:
    """拍板开关（PRASHNA_REBUILD_PLAN §五）。默认全开；基础率脚本逐项关掉看影响。"""
    d2_link: bool = True  # 连接进成事账（S4）
    d3_need: bool = True  # P-I.3 与能力层按问题读
    d4_context: bool = True  # 类比偈语境检验


def _entry(code, f, plan, h, opts):
    """按登记码生成一条账本条目。"""
    base = code.rstrip("*")
    kind = code.split(":")[1] if ":" in code else ""
    level = "B（类比）" if code in ANALOGY else MATTERS[plan.matter].level
    name = RULE_NAMES.get(base.split(":")[0], base)
    houses, alt, note = frozenset(), None, ""
    if base == "PI3":
        d, ev, note = p_i3(f, h)
        reason = f"事项宫 {h} 宫扶压"
    elif base == "I4":
        d, ev = p_i4(f); reason = "一般所谋之事能否达成"
    elif base == "IV3":
        d, ev = p_iv3(f); reason = "位置（10、7 宫吉星；11、12 宫凶星；Moon）"
    elif base == "IV3F":
        d, ev = p_iv3_fame(f); reason = "名利（2、5、1 宫吉星）"
    elif base.startswith("II1"):
        d, ev, note = p_ii1(f, kind); reason = f"动／固座（{kind}）"
        if kind == "变动" and plan.direction == "避免":
            d = {"fav": "unf", "unf": "fav"}.get(d, d); note += "；问保住，方向相反"
    elif base == "II2":
        d, ev = p_ii2(f); reason = "吉凶星照 Lagna 与 Moon-lagna"
    elif base == "II5":
        d, ev = p_ii5(f); reason = "路上顺不顺"
    elif base == "II9":
        d, alt, ev = p_ii9(f); reason = "能否早日出发"; note = "两说：Sun 是否计入" if alt != d else ""
    elif base == "II11":
        d, ev = p_ii11(f); reason = "开庭快慢（按点名）"
    elif base == "III1":
        d, ev = p_iii1(f); reason = "竞争胜负"
    elif base == "III34":
        d, ev, houses = p_iii34(f); reason = "和解（王者和解，Ayer 注扩到 settlement of scores）"
    elif base == "III5":
        d, ev = p_iii5(f); reason = "远方之人很快到来（按点名）"
    elif base == "IV2":
        d, ev = p_iv2(f); reason = "投资得失"
    elif base == "IV5":
        d, ev = p_iv5(f); reason = "疾病康复"
    elif base == "V1P":
        d, ev = p_v1(f, True); reason = "离者返回（行星落 5、2、3 宫）"
    elif base == "V1O":
        d, ev = p_v1(f, False); reason = "失物复得（吉星落 5、2、3 宫）"
    elif base == "V2":
        d, alt, ev = p_v2(f); reason = "离者返回（6／7 宫有星、Jupiter 角宫、Mercury／Venus 三方宫）"
        note = "两说：且／或" if alt != d else ""
    elif base == "V3":
        d, ev, houses = p_v3(f); reason = "Moon 落 8 宫平安返回"
    elif base == "VI3":
        d, alt, ev = p_vi3(f); reason = "失物能否找回"; note = "两说：Gemini 是否头升" if alt not in (None, d) else ""
    elif base == "VII1":
        d, ev = p_vii1(f, plan.asker); reason = f"得新娘或新郎（{plan.asker}问）"
    elif base == "VII2":
        d, ev = p_vii2(f); reason = "议婚能否成"
    elif base == "CHY":
        d, ev = chyuti(f); reason = "变动（裁员、调岗、换工作）"
        if plan.direction == "避免":
            d = {"fav": "unf", "unf": "fav"}.get(d, d); note = "问保住，方向相反"
    elif base == "VRI":
        d, ev = vriddhi(f); reason = "兴旺（4 宫）"
    elif base == "PRA":
        d, ev = pravasa(f); reason = "会不会离开（10 宫）"
    elif base == "NIV":
        d, ev = nivritti(f); reason = "返回（7 宫）"
    elif base == "R4":
        d, alt, ev = return_4th(f); reason = "在外者返回另看 4 宫"; note = "两说：正文／注" if alt != d else ""
    elif base == "X5":
        d, ev = x5(f); reason = "7 宫有吉星为好"
    elif base == "X15":
        d, ev, houses = x15(f); reason = "Moon 受克落偶数宫且亏月、或落 8 宫"
    elif base == "X16":
        d, ev = x16(f, with_link=not opts.d2_link); reason = "Lagna 主与 7 宫主或 Venus 互换、入旺、互照"
        if opts.d2_link:
            note = "Lagna 主–7 宫主互换、互照与 M-XIV.43 连接同源，已归入连接一条"
    elif base == "X17":
        d, ev, houses = x17(f); reason = "8、6 宫受克凶星"
    else:
        raise KeyError(code)
    if alt == d:
        alt = None
    e = Entry(name, level, reason, d, ev, alt=alt, note=note, houses=houses)
    if opts.d4_context and code in ANALOGY and score(d) != 0:
        clash = (houses - {1, h}) & plan.role_houses()
        if clash:
            e.excluded = f"语境不合：本偈读的 {'、'.join(map(str, sorted(clash)))} 宫在本题另有角色（措辞点到）"
    return e


def link_entry(f, h):
    """S4 连接（M-XIV.43，D2）：Lagna 主与事项宫主同宫、照射、互换或互为 4／10 宫记有利；未连上不记不利。"""
    l1, lm = f.lord(1), f.lord(h)
    if h == 1 or l1 == lm:
        return None
    kinds = F._relation(f.chart, l1, lm)
    return Entry("M-XIV.43", "B（通用）", f"事项宫主与 Lagna 主有无关系（{h} 宫主 {lm}）",
                 "fav" if kinds else "none", f"{l1}–{lm}：{'、'.join(kinds) or '无'}")


def build_ledger(chart, plan, opts=Options()):
    f = Facts(chart, plan.needed_planets if opts.d3_need else ())
    m = MATTERS[plan.matter]
    h = plan.house_of_matter()
    codes = list(m.rules)
    if plan.matter == "见面" and plan.context == "恋爱":
        codes += list(LOVE_EXTRA)
    if plan.matter == "离开" and plan.early_departure:
        codes.append("II9")
    entries = [_entry(c, f, plan, h, opts) for c in codes]
    if not m.has_i4:
        d, ev = p_i4(f)
        entries.append(Entry("P-I.4", "B（通用环境）", "一般所谋之事能否达成", d, ev))
    d, ev = p_iv1(f)
    entries.append(Entry("P-IV.1", "B（通用环境）", "角宫、三方宫吉凶布局（omnibus solution）", d, ev))
    if opts.d2_link:
        e = link_entry(f, h)
        if e:
            entries.append(e)
    return entries


def _tier(entries, reading=0):
    """reading=0 用第一读法，1 用两说的第二读法。返回（档、强度、合计）。"""
    dirs = [(e.alt if reading and e.alt else e.direction) for e in entries if not e.excluded]
    s = sum(score(x) for x in dirs)
    nz = [x for x in dirs if score(x)]
    if not nz and "mixed" not in dirs:
        return "持平", "盘面未给方向", 0
    if s == 0:
        return "持平", "吉凶相当", 0
    pos, neg = any(score(x) > 0 for x in dirs), any(score(x) < 0 for x in dirs)
    if len(nz) == 1:
        return ("偏成" if s > 0 else "偏不成"), "单条证据", s
    if s > 0:
        return "偏成", "有阻力" if neg else "顺", s
    return "偏不成", "有转机" if pos else "明确", s


# ---------------------------------------------------------------------------
# 能力层（rubric §2.1）
# ---------------------------------------------------------------------------
def ability(chart, house, plan, opts=Options()):
    """formatter 能力表结论，再按需减项：所需征象星不算"受凶星占照"；措辞点到且相合的宫，"落该宫"不算折损。"""
    planet, factors, rescue, verdict = F._lord_ability(chart, house)
    out, dropped = [], []
    needed = set(plan.needed_planets) if opts.d3_need else set()
    roles = plan.role_houses() if opts.d3_need else set()
    for x in factors:
        if x.startswith("受凶星占照（"):
            names = [n for n in x[len("受凶星占照（"):x.index("）")].split("、") if n not in needed]
            if not names:
                dropped.append(x + "（所需征象星，改记供给）"); continue
            if len(names) < len(x[len("受凶星占照（"):x.index("）")].split("、")):
                x = f"受凶星占照（{'、'.join(names)}）、无吉星"
        if x.startswith("落") and x.endswith("宫") and int(x[1:-1]) in roles:
            dropped.append(x + "（措辞点到的宫，应象）"); continue
        out.append(x)
    if len(out) >= 3 or (len(out) == 2 and not rescue):
        v = "严重受损"
    elif out:
        v = "能力打折"
    else:
        v = "有力" if {"入旺", "本座", "天然友座"} & set(rescue) else "正常"
    return {"house": house, "planet": planet, "factors": out, "dropped": dropped, "rescue": rescue,
            "verdict": v, "formatter_verdict": verdict}


# ---------------------------------------------------------------------------
# 限定语（rubric §2.3；house-meanings 第 4 节）
# ---------------------------------------------------------------------------
WATERY = {"Cancer", "Scorpio", "Pisces", "Capricorn"}  # Horasara；Mantreswara 另读，见 _watery


def hidden_or_public(chart, h, context):
    """显隐定序：① 两性、私会语境看 XXVIII.19；② 指标星落入 10 宫或 4、8、12 宫即定，不落入再看与这些宫主的连接；③ 半球。"""
    f = Facts(chart)
    steps = []
    planets = chart["planets"]
    lord = f.lord(h)
    if context == "恋爱":
        moon, saturn = "Moon", "Saturn"
        dark = (planets[moon]["sign"] in ("Capricorn", "Aquarius") or f.sees(saturn, moon)
                or f.house[moon] == f.house[saturn] or f.house[moon] == 4 or planets[moon]["sign"] in WATERY)
        lit = f.sees("Sun", moon) or f.house["Sun"] == f.house[moon]
        steps.append(("M-XXVIII.19", "公开" if lit else "私下" if dark else None,
                      f"Moon {planets[moon]['sign']} {f.house[moon]} 宫；Saturn {'照' if f.sees(saturn, moon) else '不照'} Moon；"
                      f"Sun {'照或同 Moon' if lit else '不照不同 Moon'}"))
    # 第 2 步：先看落入（M-XIV.47：卜卦按所落之处取象义），落 10 宫主公开，落 4、8、12 宫主私密；
    # 都不落入，再看与这些宫主的连接，两边都有则本步不定。
    where = f.house[lord]
    if where == 10 or where in (4, 8, 12):
        s2 = "公开" if where == 10 else "私下"
        basis = f"指标星 {lord} 落 {where} 宫"
    else:
        pub = f.lord(10) != lord and bool(F._relation(chart, lord, f.lord(10)))
        priv_h = [x for x in (4, 8, 12) if f.lord(x) != lord and F._relation(chart, lord, f.lord(x))]
        s2 = "公开" if pub and not priv_h else "私下" if priv_h and not pub else None
        basis = f"指标星 {lord} 落 {where} 宫；与 10 宫主{'有' if pub else '无'}连接；与 {'、'.join(map(str, priv_h)) or '—'} 宫主连接"
    steps.append(("M-XIV.47；宫义", s2, basis))
    steps.append(("M-XIV.118–120", "公开" if f.house[lord] >= 7 else "私下", f"指标星落 {f.house[lord]} 宫"))
    decided = next((s for s in steps if s[1]), steps[-1])
    return decided[1], steps


def at_home(chart):
    """XXVIII.5（执行口径）：照 Lagna 的行星落本座 → 在自己家；落他星之座 → 在外。"""
    f = Facts(chart)
    hits = F._classical_aspecting_house(chart, 1)
    own = [n for n in hits if F.SIGN_LORDS[chart["planets"][n]["sign"]] == n]
    other = [n for n in hits if n not in own]
    res = "在家" if own and not other else "在外" if other and not own else ("两说" if own else None)
    return res, f"照 Lagna：本座 {'、'.join(own) or '—'}；他座 {'、'.join(other) or '—'}"


def keyword_qualifier(chart, h, kw):
    """一般限定语：指标星与对应宫主或对应星连上，或落入对应宫 → 成立；对应宫主严重受损 → 成立但无力；都没有 → 不成立。"""
    f = Facts(chart)
    lord = f.lord(h)
    links = []
    for x in kw.get("houses", ()):
        if f.house[lord] == x:
            links.append(f"指标星落 {x} 宫")
        elif f.lord(x) != lord and F._relation(chart, lord, f.lord(x)):
            links.append(f"{lord}–{f.lord(x)}（{x} 宫主）：{'、'.join(F._relation(chart, lord, f.lord(x)))}")
    for p in kw.get("planets", ()):
        if p != lord and F._relation(chart, lord, p):
            links.append(f"{lord}–{p}：{'、'.join(F._relation(chart, lord, p))}")
    if not links:
        return "不成立", "无连接"
    weak = [x for x in kw.get("houses", ()) if F._lord_ability(chart, x)[3] == "严重受损"]
    return ("成立但无力" if weak else "成立"), "；".join(links) + (f"；{'、'.join(map(str, weak))} 宫主严重受损" if weak else "")


def qualifiers(chart, plan, chain):
    h = plan.house_of_matter()
    out = []
    kws = {k["word"]: k for k in plan.keywords}
    for q in plan.qualifiers:
        if q in ("私下", "公开"):
            res, steps = hidden_or_public(chart, h, plan.context)
            out.append({"name": q, "result": "成立" if res == q else "不成立",
                        "basis": "；".join(f"{s[0]}：{s[2]} → {s[1] or '未定'}" for s in steps)})
        elif q in ("在家", "在外"):
            res, ev = at_home(chart)
            out.append({"name": q, "result": "成立" if res == q else "两说" if res == "两说" else "不成立", "basis": ev})
        elif q == "主动":
            v = chain["verdict"] if chain else None
            r = {"偏会": "成立", "偏会·停在念头或言语": "成立", "有心无力": "成立但无力"}.get(v, "不成立")
            out.append({"name": q, "result": r, "basis": f"行动链（行动者 {plan.actor} 宫）：{v}"})
        elif q in kws:
            r, ev = keyword_qualifier(chart, h, kws[q])
            out.append({"name": q, "result": r, "basis": ev})
        else:
            raise ValueError(f"限定语 {q} 既非内置（私下／公开／在家／在外／主动）也不在 keywords")
    return out


# ---------------------------------------------------------------------------
# 判定
# ---------------------------------------------------------------------------
def action_chain(chart, actor):
    start, move, point, weak, verdict = F._action_chain(chart, actor)
    return {"actor": actor, "start": start, "move": move, "point": point, "weak": weak, "verdict": verdict}


def _core(chart, plan, opts):
    """账本、能力层、档（含两说与否决），不含输入敏感。"""
    entries = build_ledger(chart, plan, opts)
    ab = ability(chart, plan.house_of_matter(), plan, opts)
    tier, strength, total = _tier(entries)
    branches = []
    if any(e.alt for e in entries if not e.excluded):
        t2 = _tier(entries, 1)
        if t2[:2] != (tier, strength):
            branches = [f"{tier}·{strength}", f"{t2[0]}·{t2[1]}"]
            tier, strength = "持平", "两说"
    if ab["verdict"] == "严重受损":
        tier, strength = "偏不成", "能力不足"
    return entries, ab, tier, strength, total, branches


# ---------------------------------------------------------------------------
# 描述型（D15；question-decomposition 第 2 节）：只出事实，不建账本、不定档、不给时间
# ---------------------------------------------------------------------------
def influences(chart, plan, h):
    """事项宫与指标星所在宫的同宫、照射之星，逐颗列影响者三问要的事实（house-meanings 第 7 节）：
    所管的宫、对该星座的吉凶标签、D1 尊贵度、燃烧逆行，以及措辞点没点到（关键词的星或宫）。"""
    f = Facts(chart)
    lord = f.lord(h)
    places = [(h, f"{h} 宫")]
    if f.house[lord] != h:
        places.append((f.house[lord], f"指标星 {lord} 所在 {f.house[lord]} 宫"))
    rows = []
    for x, at in places:
        for how, names in (("同宫", F._occupants(chart, x, P7 + F.NODES)), ("照射", F._classical_aspecting_house(chart, x))):
            for n in names:
                if n == lord:
                    continue
                rules = sorted(F._houses_ruled_from(n, f.lsign)) if n in P7 else []
                hits = [f"{k['word']}（{k['polarity']}）" for k in plan.keywords
                        if n in k.get("planets", ()) or set(rules) & set(k.get("houses", ()))]
                rows.append({"at": at, "how": how, "planet": n, "rules": rules,
                             "label": F._ayer_role(chart, n, f.sign(x)) if n in P7 else "不贴标签",
                             "dignity": f.basic.get(n, "—"), "combust": n in chart.get("combustion", {}),
                             "retro": n in P7 and bool(chart["planets"][n].get("retrograde")),
                             "hits": hits or ["没点到"]})
    return rows


def quarrel_117(chart):
    """M-XIV.117：Moon 或 Venus 与凶星同落 7 宫或 4 宫，与女性起争执。凶星按该宫星座的吉凶标签。"""
    f = Facts(chart)
    hits = []
    for x in (4, 7):
        occ = dict(f.occ(x))
        bad = [n for n, k in occ.items() if k == "M" and n not in ("Moon", "Venus")]
        who = [n for n in ("Moon", "Venus") if n in occ]
        if who and bad:
            hits.append(f"{'、'.join(who)} 与 {'、'.join(bad)} 同落 {x} 宫")
    return ("成立", "；".join(hits)) if hits else ("不成立", "4、7 宫无 Moon／Venus 与凶星同落")


def describe(chart, plan):
    h = plan.house_of_matter()
    f = Facts(chart)
    l1, lm = f.lord(1), f.lord(h)
    link = "即 Lagna 主" if l1 == lm else "、".join(F._relation(chart, l1, lm)) or "无"
    return {
        "matter": "描述", "matter_house": h, "level": "B", "ledger": [], "sum": 0,
        "tier": "描述", "strength": "不定档", "branches": [], "sensitive": [],
        "ability": ability(chart, h, plan), "chain": action_chain(chart, plan.actor) if plan.actor else None,
        "qualifiers": [], "condition_failed": [], "timing": "none",
        "describe": {"link": f"{l1}–{lm}：{link}", "influences": influences(chart, plan, h),
                     "keywords": [dict(zip(("word", "result", "basis"), (k["word"], *keyword_qualifier(chart, h, k))))
                                  for k in plan.keywords],
                     "M-XIV.117": dict(zip(("result", "basis"), quarrel_117(chart)))},
    }


def _signature(entries, ab):
    return [(e.rule_id, e.direction, e.alt, bool(e.excluded)) for e in entries], ab["verdict"] == "严重受损"


def judge(chart, plan, opts=Options(), variants=()):
    """一张盘的判定，档只按用户给的提问时刻与地点定（创始人 2026-10-29：时间地点由提问人负责）。
    variants：前后窗口两端的 (标签, chart)，只用来记录本题账本或否决是否随之改变（核对区"输入提示"），
    不改档，也不进给用户看的部分（10-29 创始人与测试用户定：用户看不懂、徒增烦恼）。"""
    if plan.matter == "描述":
        return describe(chart, plan)
    entries, ab, tier, strength, total, branches = _core(chart, plan, opts)
    base = _signature(entries, ab)
    sensitive = []
    for label, vc in variants:
        ve, vab, vt, vs, _, _ = _core(vc, plan, opts)
        if base[1] and vab["verdict"] == "严重受损":
            continue  # 两端都被能力层否决，账本怎么变都不改档
        if _signature(ve, vab) != base:
            names = {e.rule_id for e in entries} | {e.rule_id for e in ve}
            changed = sorted(n for n in names
                             if [(e.direction, e.alt, bool(e.excluded)) for e in entries if e.rule_id == n]
                             != [(e.direction, e.alt, bool(e.excluded)) for e in ve if e.rule_id == n])
            if (vab["verdict"] == "严重受损") != (ab["verdict"] == "严重受损"):
                changed.append("能力层否决")
            sensitive.append({"at": label, "rules": changed, "tier": f"{vt}·{vs}"})
    chain = action_chain(chart, plan.actor) if plan.actor else None
    m = MATTERS[plan.matter]
    qs = qualifiers(chart, plan, chain)
    # D13：取象单的限定语都来自问题措辞的明确要求（必要条件）；有一条不成立，答"按这个条件不能"，不给时间
    failed = [q["name"] for q in qs if q["result"] == "不成立"]
    return {
        "matter": plan.matter, "matter_house": plan.house_of_matter(), "level": m.level,
        "ledger": [e.__dict__ | {"score": e.score, "houses": sorted(e.houses)} for e in entries],
        "sum": total, "tier": tier, "strength": strength, "branches": branches, "sensitive": sensitive,
        "ability": ab, "chain": chain, "qualifiers": qs, "condition_failed": failed,
        "timing": "none" if tier == "偏不成" or strength == "盘面未给方向" or m.timing == "none" or failed
        else m.timing,
    }
