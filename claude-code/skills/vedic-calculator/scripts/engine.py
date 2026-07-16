"""
vedic-calculator v0.5 - PyJHora 精确计算引擎
基于 pysweph 天文核心 + PyJHora 精确算法（含 9 项 Shadbala bug 修正）
输出完整的 structured_data 所需数据

v0.5: 移除所有 dashaflow fallback（错误结果比无结果更糟），fail-fast
v0.4: Dasha 接入 PyJHora（≤2天）
v0.3: SAV/Shadbala fallback 显式 WARNING
"""
import os, sys
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")  # 受限环境(如Claude Code)免疫OpenBLAS线程探测

try:
    import swisseph as swe
except ImportError as e:                             # 用错python时给可执行纠正,不再含糊报错
    sys.stderr.write(
        "\n❌ swisseph 不可用—极可能用了系统 Python。\n"
        "  系统 Python 装的是空壳(只有 dist-info、无 .pyd),必须改用 skill 自带 venv:\n"
        "  Windows : vedic-calculator\\venv\\Scripts\\python.exe <脚本>\n"
        "  Linux/Mac: vedic-calculator/venv/bin/python <脚本>\n"
        f"  原始错误: {e}\n"
    )
    raise
from datetime import datetime, timedelta
import pytz
import json

# dashaflow — 仅用于 dignity/jaimini（这些无 PyJHora bug，不需要修正）
from dashaflow.dignity import get_dignity, get_compound_relationship, check_combustion, get_digbala
from dashaflow.jaimini import calculate_jaimini_karakas

# ── PyJHora 精确模块（必须全部加载，否则 fail-fast）──
_SETUP_HINT = (
    "\n╔══════════════════════════════════════════════════════╗\n"
    "║  PyJHora 未正确安装！请运行:                         ║\n"
    "║  python vedic-calculator/scripts/setup_env.py        ║\n"
    "╚══════════════════════════════════════════════════════╝"
)

_load_errors = []
try:
    from ashtakavarga_pyjhora import calculate_ashtakavarga_fixed as _av_pyjhora
except ImportError as e:
    _av_pyjhora = None
    _load_errors.append(f'ashtakavarga_pyjhora: {e}')
try:
    from shadbala_pyjhora import calculate_shadbala_fixed as _shadbala_pyjhora
except ImportError as e:
    _shadbala_pyjhora = None
    _load_errors.append(f'shadbala_pyjhora: {e}')
try:
    from dasha_pyjhora import calculate_dasha_fixed as _dasha_pyjhora
except ImportError as e:
    _dasha_pyjhora = None
    _load_errors.append(f'dasha_pyjhora: {e}')
try:
    from divisional_pyjhora import calculate_divisional_charts as _div_pyjhora
except ImportError as e:
    _div_pyjhora = None
    _load_errors.append(f'divisional_pyjhora: {e}')
try:
    from extras_pyjhora import (
        calculate_bhava_bala as _bhava_bala_pyjhora,
        calculate_special_lagnas as _special_lagnas_pyjhora,
        calculate_vargeeya_bala as _vargeeya_bala_pyjhora,
        calculate_pushkara as _pushkara_pyjhora,
    )
except ImportError as e:
    _bhava_bala_pyjhora = None
    _special_lagnas_pyjhora = None
    _vargeeya_bala_pyjhora = None
    _pushkara_pyjhora = None
    _load_errors.append(f'extras_pyjhora: {e}')
try:
    from chara_dasha import calc_chara_dasha as _chara_dasha
except ImportError as e:
    _chara_dasha = None
    _load_errors.append(f'chara_dasha: {e}')

# Fail-fast: 核心模块必须全部加载
_REQUIRED = {'SAV': _av_pyjhora, 'Shadbala': _shadbala_pyjhora, 'Dasha': _dasha_pyjhora}
_missing = [name for name, mod in _REQUIRED.items() if mod is None]
if _missing:
    print(f"\n❌ FATAL: 以下核心模块加载失败: {', '.join(_missing)}", file=sys.stderr)
    for err in _load_errors:
        print(f"   → {err}", file=sys.stderr)
    print(_SETUP_HINT, file=sys.stderr)
    raise ImportError(f"vedic-calculator 核心模块缺失: {', '.join(_missing)}. 请运行 setup_env.py")

# === 配置 ===
swe.set_sid_mode(swe.SIDM_TRUE_CITRA)
# 星历路径：显式指向 skill 自带 ephe（.se1），确保首次 calculate_full_chart 的 calc_ut 就用
# Swiss 星历。否则 engine 自身从不 set_ephe_path，首盘 calc_planet 在 PyJHora 模块（首次调用
# 中途才 set_ephe_path）之前跑 → 跌回 Moshier 近似，与后续盘差 ~0.5 角秒（PQ-02 同进程重复
# 排盘漂移的真根因；产品诊断的 sid_mode 修法经实测无效）。
_EPHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ephe')
if os.path.isdir(_EPHE_DIR):
    swe.set_ephe_path(_EPHE_DIR)

SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo',
         'Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
SIGN_ABBR = ['Ar','Ta','Ge','Cn','Le','Vi','Li','Sc','Sg','Cp','Aq','Pi']

PLANETS_SWE = {
    'Sun': swe.SUN, 'Moon': swe.MOON, 'Mars': swe.MARS,
    'Mercury': swe.MERCURY, 'Jupiter': swe.JUPITER,
    'Venus': swe.VENUS, 'Saturn': swe.SATURN
}

SIGN_LORDS = {
    0: 'Mars', 1: 'Venus', 2: 'Mercury', 3: 'Moon',
    4: 'Sun', 5: 'Mercury', 6: 'Venus', 7: 'Mars',
    8: 'Jupiter', 9: 'Saturn', 10: 'Saturn', 11: 'Jupiter'
}

NAKSHATRAS = [
    ('Ashwini','Ketu'), ('Bharani','Venus'), ('Krittika','Sun'),
    ('Rohini','Moon'), ('Mrigashira','Mars'), ('Ardra','Rahu'),
    ('Punarvasu','Jupiter'), ('Pushya','Saturn'), ('Ashlesha','Mercury'),
    ('Magha','Ketu'), ('Purva Phalguni','Venus'), ('Uttara Phalguni','Sun'),
    ('Hasta','Moon'), ('Chitra','Mars'), ('Swati','Rahu'),
    ('Vishakha','Jupiter'), ('Anuradha','Saturn'), ('Jyeshtha','Mercury'),
    ('Moola','Ketu'), ('Purva Ashadha','Venus'), ('Uttara Ashadha','Sun'),
    ('Shravana','Moon'), ('Dhanishta','Mars'), ('Shatabhisha','Rahu'),
    ('Purva Bhadrapada','Jupiter'), ('Uttara Bhadrapada','Saturn'), ('Revati','Mercury')
]

DASHA_ORDER = ['Ketu','Venus','Sun','Moon','Mars','Rahu','Jupiter','Saturn','Mercury']
DASHA_YEARS = {'Ketu':7,'Venus':20,'Sun':6,'Moon':10,'Mars':7,'Rahu':18,'Jupiter':16,'Saturn':19,'Mercury':17}

HOUSE_DOMAINS = {
    1:'自我', 2:'财富', 3:'兄弟', 4:'家庭', 5:'子女',
    6:'疾病', 7:'婚姻', 8:'变故', 9:'运势', 10:'事业',
    11:'收入', 12:'损耗'
}

# === 核心计算函数 ===

def _localize_strict(tz, dt):
    """DST-safe localize：出生时间落在夏令时切换时段时不静默猜（错1小时=上升/Dasha全错），明确报错。"""
    try:
        return tz.localize(dt, is_dst=None)
    except pytz.exceptions.AmbiguousTimeError:
        raise ValueError(
            f"出生时间 {dt} 落在夏令时结束的重复时段（当地钟表回拨，该时刻出现过两次）。"
            "请确认出生记录用的是夏令时还是标准时间的钟表时间，无法确认时建议用 rectifier 校准。")
    except pytz.exceptions.NonExistentTimeError:
        raise ValueError(
            f"出生时间 {dt} 落在夏令时开始的跳过时段（当地钟表拨快，该时刻不存在）。"
            "出生记录可能用的是标准时间——请核实后换算，或用 rectifier 校准。")


def to_jd(year, month, day, hour, minute, tz_str):
    tz = pytz.timezone(tz_str)
    local_dt = _localize_strict(tz, datetime(year, month, day, hour, minute))
    utc_dt = local_dt.astimezone(pytz.utc)
    ut_hour = utc_dt.hour + utc_dt.minute/60.0 + utc_dt.second/3600.0
    return swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, ut_hour)

def calc_planet(jd, planet_id):
    flags = swe.FLG_SIDEREAL | swe.FLG_SPEED
    result = swe.calc_ut(jd, planet_id, flags)
    lon = result[0][0]
    speed = result[0][3]
    sign_idx = int(lon / 30)
    degree = lon % 30
    deg_int = int(degree)
    min_int = round((degree - deg_int) * 60)
    return {
        'longitude': lon, 'sign': SIGNS[sign_idx], 'sign_idx': sign_idx,
        'degree': degree, 'deg_str': f"{deg_int}°{min_int:02d}'",
        'retrograde': speed < 0, 'speed': speed
    }

def calc_lagna(jd, lat, lon):
    flags = swe.FLG_SIDEREAL
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'W', flags)
    asc_lon = ascmc[0]
    sign_idx = int(asc_lon / 30)
    degree = asc_lon % 30
    deg_int = int(degree)
    min_int = round((degree - deg_int) * 60)
    return {
        'longitude': asc_lon, 'sign': SIGNS[sign_idx], 'sign_idx': sign_idx,
        'degree': degree, 'deg_str': f"{deg_int}°{min_int:02d}'"
    }

def get_nakshatra(longitude):
    nak_idx = int(longitude / (360/27))
    pada = int((longitude % (360/27)) / (360/108)) + 1
    name, lord = NAKSHATRAS[nak_idx]
    return {'name': name, 'pada': pada, 'lord': lord}

def get_house(planet_sign_idx, lagna_sign_idx):
    return ((planet_sign_idx - lagna_sign_idx) % 12) + 1

def calc_navamsha(longitude):
    """D9 Navamsha: each sign divided into 9 parts of 3°20'"""
    nav_part = int((longitude % 30) / (30/9))
    sign_idx = int(longitude / 30)
    # Navamsha starts from: Fire→Ar, Earth→Cp, Air→Li, Water→Cn
    element_start = [0, 9, 6, 3]  # Ar, Cp, Li, Cn
    element = sign_idx % 4  # 0=fire, 1=earth, 2=air, 3=water
    d9_sign_idx = (element_start[element] + nav_part) % 12
    return SIGNS[d9_sign_idx], d9_sign_idx

def calc_dashamsha(longitude):
    """D10 Dashamsha: each sign divided into 10 parts of 3°
    Odd signs: count from same sign
    Even signs: count from 9th sign (= +8 in 0-indexed)
    """
    part = int((longitude % 30) / 3)
    sign_idx = int(longitude / 30)
    if sign_idx % 2 == 0:  # Odd signs (Ar, Ge, Le...)
        d10_sign_idx = (sign_idx + part) % 12
    else:  # Even signs: 9th from sign = +8 (0-indexed)
        d10_sign_idx = (sign_idx + part + 8) % 12
    return SIGNS[d10_sign_idx], d10_sign_idx

def calc_chaturthamsha(longitude):
    """D4"""
    part = int((longitude % 30) / (30/4))
    sign_idx = int(longitude / 30)
    d4_sign_idx = (sign_idx + part * 3) % 12
    return SIGNS[d4_sign_idx], d4_sign_idx

def calc_panchamsha(longitude):
    """D5 Panchamsha: each sign divided into 5 parts of 6°
    BPHS lords:
      Odd signs:  Mars(Ar), Saturn(Aq), Jupiter(Sg), Mercury(Ge), Venus(Li)
      Even signs: Venus(Ta), Mercury(Vi), Jupiter(Pi), Saturn(Cp), Mars(Sc)
    """
    part = int((longitude % 30) / 6)
    sign_idx = int(longitude / 30)
    if sign_idx % 2 == 0:  # odd sign (0-indexed even = zodiac odd)
        starts = [0, 10, 8, 2, 6]    # Ar, Aq, Sg, Ge, Li
    else:  # even sign
        starts = [1, 5, 11, 9, 7]    # Ta, Vi, Pi, Cp, Sc
    d5_sign_idx = starts[part] if part < 5 else sign_idx
    return SIGNS[d5_sign_idx], d5_sign_idx

def calc_chara_karakas_7k8k(planets):
    """Calculate Chara Karakas (7K primary/KN Rao, 8K reference)"""
    # Effective degree = degree in sign (for Rahu: 30 - degree)
    karaka_data = []
    for name in ['Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn']:
        karaka_data.append((name, planets[name]['degree']))
    
    # 7K (primary/KN Rao): sort by degree descending, top 7
    sorted_7k = sorted(karaka_data, key=lambda x: x[1], reverse=True)
    karaka_names_7k = ['AK','AmK','BK','MK','PK','GK','DK']
    karakas_7k = [(karaka_names_7k[i], sorted_7k[i][0], sorted_7k[i][1]) 
                  for i in range(7)]
    
    # 8K (reference/Sanjay Rath): add Rahu (30 - degree)
    rahu_eff_deg = 30 - planets['Rahu']['degree']
    karaka_data_8k = karaka_data + [('Rahu', rahu_eff_deg)]
    sorted_8k = sorted(karaka_data_8k, key=lambda x: x[1], reverse=True)
    karaka_names_8k = ['AK','AmK','BK','MK','PiK','PK','GK','DK']
    karakas_8k = [(karaka_names_8k[i], sorted_8k[i][0], sorted_8k[i][1]) 
                  for i in range(8)]
    
    # DK: 7K为主，8K为参考
    dk_7k = karakas_7k[6][1]     # 7K DK（主）
    dk_8k = karakas_8k[7][1]     # 8K DK = 第8位（最低度数）
    
    return {
        '7k': karakas_7k,
        '8k': karakas_8k,
        'dk_7k': dk_7k,
        'dk_8k': dk_8k,
        'dk_note': f"7K(主)={dk_7k}, 8K(参考)={dk_8k}"
    }

# calc_aspects（西占度数 orb 相位：合/六合/刑/三合/冲）已删除——不属 KN Rao/Parashari 体系、
# 全体系无判定消费方、且是 love/career「相位关系表」命名歧义源。吠陀相位一律用 calc_graha_drishti（宫位照射）。

def calc_graha_drishti(planets):
    """Parashari graha drishti（行星宫位相位，P10 规则数据化，禁模型手推）。
    所有行星 → 第7宫；Mars +4/8；Jupiter +5/9；Saturn +3/10；Rahu/Ketu 仅第7（无特殊相位）。
    节点口径对齐底层 jhora const.graha_drishti（Rahu=[7]、Ketu=[7]）；Rahu 带 amplify=True（相位=放大/膨胀迷惑）。
    每颗星从其落宫数第 N 宫。返回 {planet: {from_house, aspected_houses, aspected_planets, amplify}}。
    （注：这是吠陀 graha drishti = 宫位照射；西占度数 orb 相位已废弃删除、不属本体系，勿混淆。）
    """
    special = {'Mars': [4, 8], 'Jupiter': [5, 9], 'Saturn': [3, 10]}
    # 含 Ketu：对齐底层 jhora const.graha_drishti（Rahu=[7]、Ketu=[7]），节点保留基础对宫第7、不给特殊相位
    drishti_planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
    house_occupants = {}
    for name in drishti_planets:
        p = planets.get(name)
        if p and 'house' in p:
            house_occupants.setdefault(p['house'], []).append(name)
    result = {}
    for name in drishti_planets:
        p = planets.get(name)
        if not p or 'house' not in p:
            continue
        h = p['house']
        angles = [7] + special.get(name, [])   # Rahu/Ketu 无 special → 仅第7
        aspected_houses = sorted(set(((h - 1 + (a - 1)) % 12) + 1 for a in angles))
        aspected_planets = sorted(set(pl for hh in aspected_houses
                                      for pl in house_occupants.get(hh, [])))
        result[name] = {'from_house': h,
                        'aspected_houses': aspected_houses,
                        'aspected_planets': aspected_planets,
                        'amplify': name == 'Rahu'}   # Rahu 相位=放大（膨胀/迷惑），下游按此加权、禁静默丢
    return result


def calc_house_lords(lagna_sign_idx):
    """Calculate house lord table"""
    lords = {}
    for house in range(1, 13):
        sign_idx = (lagna_sign_idx + house - 1) % 12
        lord = SIGN_LORDS[sign_idx]
        lords[house] = {'sign': SIGNS[sign_idx], 'lord': lord, 'domain': HOUSE_DOMAINS[house]}
    return lords

# 每颗星的 Moolatrikona 星座（Parashari 固定）——用于一星多宫主时定主身份，禁模型手推
MOOLATRIKONA_SIGN = {'Sun': 'Leo', 'Moon': 'Taurus', 'Mars': 'Aries', 'Mercury': 'Virgo',
                     'Jupiter': 'Sagittarius', 'Venus': 'Libra', 'Saturn': 'Aquarius'}

def _role_of_house(h):
    if h == 1: return 'Core-Driver'
    if h in (5, 9): return 'Faithful'
    if h in (8, 12): return 'Destroyer'
    if h in (2, 4, 7, 10): return 'Trader'
    return 'Growth-Hacker'  # 3/6/11

def calc_functional(lagna_sign_idx, planets):
    """P1 功能身份（B3：一星多宫主时以 Moolatrikona 宫定主身份，禁模型手推/双计）。
    返回 {planet: {lorded_houses, moolatrikona_house, primary_role, is_yogakaraka, is_dual_benefic_malefic}}。
    Rahu/Ketu 无宫可管，不产出。"""
    lords = calc_house_lords(lagna_sign_idx)
    ruled = {}
    for h in range(1, 13):
        ruled.setdefault(lords[h]['lord'], []).append(h)
    TRIKONA, KENDRA_NO1, DUS = {1, 5, 9}, {4, 7, 10}, {6, 8, 12}
    result = {}
    for name, houses in ruled.items():
        hs = set(houses)
        mt_sign = MOOLATRIKONA_SIGN.get(name)
        mt_house = get_house(SIGNS.index(mt_sign), lagna_sign_idx) if mt_sign else None
        is_yk = bool(hs & {5, 9}) and bool(hs & KENDRA_NO1)  # 同掌三角(5/9)+角宫(4/7/10)=Yogakaraka
        base = mt_house if (mt_house in hs) else min(houses)
        result[name] = {'lorded_houses': sorted(houses),
                        'moolatrikona_house': mt_house,
                        'primary_role': 'Yogakaraka' if is_yk else _role_of_house(base),
                        'is_yogakaraka': is_yk,
                        'is_dual_benefic_malefic': bool(hs & TRIKONA) and bool(hs & DUS)}
    return result

def calc_yoga_prescan(lagna_sign_idx, planets, house_lords, graha_drishti, mutual_drishti, parivartana):
    """结构格局预扫（机械可判的格局结构条件由 calc 核验，规则读字段禁自推/先验/越宫）。
    ⚠️ 只判"结构骨架成立=T/F + 参与星"；强度评估/污染修正/解除后语义/吉凶程度一律留模型。
    含 VRY / Dharma-Karma / Dhana / Raja / Chandra-Mangala / Guru-Chandala /
       Gajakesari / Adhi / Kemadruma / Shakata / Pancha-Mahapurusha。"""
    DUS, KENDRA, TRIKONA = {6, 8, 12}, {1, 4, 7, 10}, {1, 5, 9}
    MALEFIC_NAT = {'Saturn', 'Mars', 'Sun', 'Rahu', 'Ketu'}
    EXALT = {'Sun': 'Aries', 'Moon': 'Taurus', 'Mars': 'Capricorn', 'Mercury': 'Virgo',
             'Jupiter': 'Cancer', 'Venus': 'Pisces', 'Saturn': 'Libra'}
    OWN = {'Sun': ['Leo'], 'Moon': ['Cancer'], 'Mars': ['Aries', 'Scorpio'], 'Mercury': ['Gemini', 'Virgo'],
           'Jupiter': ['Sagittarius', 'Pisces'], 'Venus': ['Taurus', 'Libra'], 'Saturn': ['Capricorn', 'Aquarius']}
    ALL9 = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']

    def h_of(name):
        p = planets.get(name)
        return p['house'] if p and 'house' in p else None
    def nth_from(h, n):
        return (((h - 1 + (n - 1)) % 12) + 1) if h else None
    def rel(frm, to):
        return (((to - frm) % 12) + 1) if (frm and to) else None
    def occ(h, exclude=()):
        return [n for n in ALL9 if planets.get(n, {}).get('house') == h and n not in exclude]
    def lord(h):
        return house_lords[h]['lord']
    def exalt_or_own(name):
        s = planets.get(name, {}).get('sign')
        return s == EXALT.get(name) or s in OWN.get(name, [])
    def conj(a, b):
        ha = h_of(a)
        return ha is not None and ha == h_of(b)
    def mutual(a, b):
        return sorted([a, b]) in mutual_drishti
    def aspects(a, b):  # a 照 b（graha drishti 单向）
        return b in graha_drishti.get(a, {}).get('aspected_planets', [])
    def pariv(hx, hy):
        return any(sorted(pv['houses']) == sorted([hx, hy]) for pv in parivartana)
    def interact(hx, hy):  # 两宫主"互动"= 合相/互视/互溶
        la, lb = lord(hx), lord(hy)
        return (la != lb) and (conj(la, lb) or mutual(la, lb) or pariv(hx, hy))

    res = {}
    # VRY
    vry = {}
    for h, k in [(6, 'harsha'), (8, 'sarala'), (12, 'vimala')]:
        lh = h_of(lord(h))
        vry[k] = {'active': (lh in (DUS - {h})) if lh else False, 'lord': lord(h),
                  'lord_house': lh, 'rule': f'{h}宫主落其他凶宫{sorted(DUS - {h})}（自宫不算）'}
    res['vry'] = vry
    # A 类：宫主互动型（互动=合相/互视/互溶）
    res['dharma_karma'] = {'active': interact(9, 10), 'lords': [lord(9), lord(10)]}
    res['dhana'] = {'active': interact(2, 11), 'lords': [lord(2), lord(11)]}
    raja = [[t, k, lord(t), lord(k)] for t in TRIKONA for k in KENDRA if t != k and interact(t, k)]
    res['raja'] = {'active': len(raja) > 0, 'hits': raja}
    res['chandra_mangala'] = {'active': conj('Moon', 'Mars') or mutual('Moon', 'Mars')}
    res['guru_chandala'] = {'active': conj('Jupiter', 'Rahu')}
    # B 类：落宫/相对位置型
    mh, jh = h_of('Moon'), h_of('Jupiter')
    res['gajakesari'] = {'active': (rel(mh, jh) in KENDRA) if (mh and jh) else False,
                         'rule': 'Jup/Moon 互为角宫(相距1/4/7/10)'}
    adhi_h = [nth_from(mh, n) for n in (6, 7, 8)] if mh else []
    adhi_b = [b for b in ['Jupiter', 'Venus', 'Mercury'] if h_of(b) in adhi_h]
    res['adhi'] = {'active': len(adhi_b) > 0, 'benefics': adhi_b, 'from_moon_678': adhi_h,
                   'malefic_contam': any(any(o in MALEFIC_NAT for o in occ(h)) for h in adhi_h),
                   'rule': '吉星(Jup/Ven/Mer)落从Moon起6/7/8宫（无凶混杂更纯）'}
    if mh:
        h_next, h_prev = nth_from(mh, 2), nth_from(mh, 12)
        kbase = (len(occ(h_next, ('Moon',))) == 0 and len(occ(h_prev, ('Moon',))) == 0)
        cancel = (mh in KENDRA) or (len(occ(mh, ('Moon',))) > 0) or aspects('Jupiter', 'Moon')
        res['kemadruma'] = {'active': kbase, 'cancelled': cancel,
                            'rule': 'Moon 2/12宫(从Moon)无星；解除:Moon在Kendra/有合相/受Jup照'}
    else:
        res['kemadruma'] = {'active': False, 'cancelled': False}
    res['shakata'] = {'active': (rel(mh, jh) in {6, 8}) if (mh and jh) else False,
                      'cancelled': (jh in KENDRA) or (mh in KENDRA) or exalt_or_own('Jupiter'),
                      'rule': 'Jup/Moon 互为6/8宫；解除:Jup或Moon在Kendra/Jup入旺庙'}
    # C 类：Pancha Mahapurusha（在Kendra且入旺/入庙）
    maha = {}
    for gname, star in [('Ruchaka', 'Mars'), ('Bhadra', 'Mercury'), ('Hamsa', 'Jupiter'),
                        ('Malavya', 'Venus'), ('Shasha', 'Saturn')]:
        sh = h_of(star)
        maha[gname] = {'active': (sh in KENDRA) and exalt_or_own(star), 'star': star,
                       'house': sh, 'sign': planets.get(star, {}).get('sign')}
    res['mahapurusha'] = maha
    return res

def calc_mutual_drishti(graha_drishti):
    """互视对（mutual drishti，格局"互视"唯一口径）：A照B落宫 且 B照A落宫（双向），
    单向照射不算。基于 graha_drishti 的 aspected_planets 两两判双向。返回 [[A,B],...]。"""
    pairs = []
    names = list(graha_drishti.keys())
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            if b in graha_drishti[a]['aspected_planets'] and a in graha_drishti[b]['aspected_planets']:
                pairs.append(sorted([a, b]))
    return pairs

def calc_parivartana(house_lords, planets):
    """互溶对（parivartana，格局"互溶"唯一口径）：X宫主落Y宫 且 Y宫主落X宫（两宫主互换落座）。
    分类：凶宫(6/8/12)互换=Dainya、含3宫=Khala、吉宫互换=Maha。返回 [{houses,lords,type},...]。"""
    BENEFIC = {1, 2, 4, 5, 7, 9, 10, 11}
    DUS = {6, 8, 12}
    pairs = []
    for x in range(1, 13):
        for y in range(x + 1, 13):
            lx = house_lords[x]['lord']
            ly = house_lords[y]['lord']
            if lx == ly:
                continue  # 同一星管两宫，不构成互溶
            hx = planets.get(lx, {}).get('house')
            hy = planets.get(ly, {}).get('house')
            if hx == y and hy == x:
                if x in DUS and y in DUS:
                    kind = 'Dainya(凶宫互溶)'
                elif x == 3 or y == 3:
                    kind = 'Khala(3宫参与)'
                elif x in BENEFIC and y in BENEFIC:
                    kind = 'Maha(吉宫互溶)'
                else:
                    kind = 'Mixed'
                pairs.append({'houses': [x, y], 'lords': [lx, ly], 'type': kind})
    return pairs

def calc_vimsottari_dasha(moon_lon, birth_year, birth_month, birth_day, birth_hour, birth_minute):
    """Calculate Vimsottari Dasha periods"""
    nak = get_nakshatra(moon_lon)
    nak_lord = nak['lord']
    start_idx = DASHA_ORDER.index(nak_lord)
    
    nak_span = 360/27
    elapsed_in_nak = moon_lon % nak_span
    remaining_fraction = 1 - (elapsed_in_nak / nak_span)
    
    birth_dt = datetime(birth_year, birth_month, birth_day, birth_hour, birth_minute)
    dashas = []
    # 第一个大运起始 = 出生日 - 已过大运年数（回溯到出生前）
    first_planet_years = DASHA_YEARS[DASHA_ORDER[start_idx]]
    elapsed_years = first_planet_years * (1 - remaining_fraction)
    current_dt = birth_dt - timedelta(days=elapsed_years * 365.25)
    
    for i in range(9):
        idx = (start_idx + i) % 9
        planet = DASHA_ORDER[idx]
        years = DASHA_YEARS[planet]
        days = years * 365.25
        end_dt = current_dt + timedelta(days=days)
        
        # Mark current
        now = datetime.now()
        is_current = current_dt <= now <= end_dt
        
        # Antardasha子期计算
        antardashas = []
        ad_start = current_dt
        for j in range(9):
            ad_idx = (idx + j) % 9
            ad_planet = DASHA_ORDER[ad_idx]
            ad_years = years * DASHA_YEARS[ad_planet] / 120
            ad_days = ad_years * 365.25
            ad_end = ad_start + timedelta(days=ad_days)
            ad_is_current = ad_start <= now <= ad_end
            antardashas.append({
                'planet': ad_planet,
                'start': ad_start.strftime('%Y-%m-%d'),
                'end': ad_end.strftime('%Y-%m-%d'),
                'is_current': ad_is_current
            })
            ad_start = ad_end
        
        dashas.append({
            'planet': planet,
            'start': current_dt.strftime('%Y-%m'),
            'end': end_dt.strftime('%Y-%m'),
            'years': round(years, 1),
            'is_current': is_current,
            'antardashas': antardashas
        })
        current_dt = end_dt
    
    return dashas

def calc_special_points(lagna, planets):
    """Calculate AL, UL and other special Jaimini points.
    Note: JHora may use different settings (Rahu/Ketu lord rules, dual-sign lords).
    Our implementation follows standard BPHS Jaimini method.
    """
    lagna_idx = lagna['sign_idx']
    
    def calc_arudha(house_num, lagna_idx):
        """Calculate Arudha Pada for a given house (BPHS standard)"""
        sign_idx = (lagna_idx + house_num - 1) % 12
        lord = SIGN_LORDS[sign_idx]
        lord_sign_idx = planets[lord]['sign_idx']
        # Count from house sign to lord (1-based: lord in same sign = 1st)
        dist = (lord_sign_idx - sign_idx) % 12
        # Arudha = same distance from lord's position
        arudha_idx = (lord_sign_idx + dist) % 12
        # BPHS Exception: arudha cannot be in 1st or 7th from house sign
        # If 1st → use 10th from house sign
        # If 7th → use 4th from house sign
        if arudha_idx == sign_idx:
            arudha_idx = (sign_idx + 9) % 12   # 10th from house sign
        elif arudha_idx == (sign_idx + 6) % 12:
            arudha_idx = (sign_idx + 3) % 12   # 4th from house sign
        return SIGNS[arudha_idx], arudha_idx
    
    al_sign, al_idx = calc_arudha(1, lagna_idx)
    al_house = get_house(al_idx, lagna_idx)
    
    ul_sign, ul_idx = calc_arudha(12, lagna_idx)
    ul_house = get_house(ul_idx, lagna_idx)
    
    return {
        'AL': {'sign': al_sign, 'sign_idx': al_idx, 'house': al_house},
        'UL': {'sign': ul_sign, 'sign_idx': ul_idx, 'house': ul_house},
    }

def calc_transits(lagna_sign_idx, moon_sign_idx):
    """Calculate current transit positions for slow planets.
    Used by core-pro for Sade Sati, BAV transit calibration, double transit.
    """
    now = datetime.now()
    jd_now = swe.julday(now.year, now.month, now.day, now.hour + now.minute/60)
    swe.set_sid_mode(swe.SIDM_TRUE_CITRA)
    flags = swe.FLG_SIDEREAL | swe.FLG_SPEED
    
    transits = {}
    # Slow planets: Saturn, Jupiter, Rahu, Ketu
    slow_planets = {'Saturn': swe.SATURN, 'Jupiter': swe.JUPITER}
    for name, pid in slow_planets.items():
        result = swe.calc_ut(jd_now, pid, flags)
        lon = result[0][0]
        sign_idx = int(lon / 30)
        house = get_house(sign_idx, lagna_sign_idx)
        transits[name] = {'sign': SIGNS[sign_idx], 'sign_idx': sign_idx, 'house': house}
    
    # Rahu (Mean Node)
    result = swe.calc_ut(jd_now, swe.MEAN_NODE, flags)
    rahu_lon = result[0][0]
    rahu_idx = int(rahu_lon / 30)
    transits['Rahu'] = {'sign': SIGNS[rahu_idx], 'sign_idx': rahu_idx, 
                        'house': get_house(rahu_idx, lagna_sign_idx)}
    ketu_idx = (rahu_idx + 6) % 12
    transits['Ketu'] = {'sign': SIGNS[ketu_idx], 'sign_idx': ketu_idx,
                        'house': get_house(ketu_idx, lagna_sign_idx)}
    
    # Sade Sati check
    saturn_idx = transits['Saturn']['sign_idx']
    sade_sati = 'inactive'
    if saturn_idx == (moon_sign_idx - 1) % 12:
        sade_sati = 'phase1_rising'
    elif saturn_idx == moon_sign_idx:
        sade_sati = 'phase2_peak'
    elif saturn_idx == (moon_sign_idx + 1) % 12:
        sade_sati = 'phase3_fading'
    transits['sade_sati'] = sade_sati
    
    # Double transit (Saturn-Jupiter intersection)
    sat_houses = {transits['Saturn']['house']}
    # Saturn aspects: 3rd, 7th, 10th
    sat_h = transits['Saturn']['house']
    for asp in [3, 7, 10]:
        sat_houses.add(((sat_h - 1 + asp - 1) % 12) + 1)
    
    jup_houses = {transits['Jupiter']['house']}
    # Jupiter aspects: 5th, 7th, 9th
    jup_h = transits['Jupiter']['house']
    for asp in [5, 7, 9]:
        jup_houses.add(((jup_h - 1 + asp - 1) % 12) + 1)
    
    double_transit = sorted(sat_houses & jup_houses)
    transits['double_transit_houses'] = double_transit
    transits['timestamp'] = now.strftime('%Y-%m-%d')
    
    return transits

# === 主计算函数 ===

def calculate_full_chart(year, month, day, hour, minute, lat, lon, tz_str="Asia/Kolkata"):
    """计算完整星盘数据"""
    jd = to_jd(year, month, day, hour, minute, tz_str)
    ayanamsa = swe.get_ayanamsa_ut(jd)
    
    # 1. Lagna
    lagna = calc_lagna(jd, lat, lon)
    lagna['nakshatra'] = get_nakshatra(lagna['longitude'])
    lagna['house'] = 1
    
    # 2. Planets (7 main)
    planets = {}
    for name, pid in PLANETS_SWE.items():
        p = calc_planet(jd, pid)
        p['house'] = get_house(p['sign_idx'], lagna['sign_idx'])
        p['nakshatra'] = get_nakshatra(p['longitude'])
        planets[name] = p
    
    # 3. Rahu & Ketu
    flags = swe.FLG_SIDEREAL | swe.FLG_SPEED
    result = swe.calc_ut(jd, swe.MEAN_NODE, flags)
    rahu_lon = result[0][0]
    rahu_sign_idx = int(rahu_lon / 30)
    rahu_deg = rahu_lon % 30
    planets['Rahu'] = {
        'longitude': rahu_lon, 'sign': SIGNS[rahu_sign_idx],
        'sign_idx': rahu_sign_idx, 'degree': rahu_deg,
        'deg_str': f"{int(rahu_deg)}°{round((rahu_deg%1)*60):02d}'",
        'retrograde': True, 'speed': result[0][3],
        'house': get_house(rahu_sign_idx, lagna['sign_idx']),
        'nakshatra': get_nakshatra(rahu_lon)
    }
    ketu_lon = (rahu_lon + 180) % 360
    ketu_sign_idx = int(ketu_lon / 30)
    ketu_deg = ketu_lon % 30
    planets['Ketu'] = {
        'longitude': ketu_lon, 'sign': SIGNS[ketu_sign_idx],
        'sign_idx': ketu_sign_idx, 'degree': ketu_deg,
        'deg_str': f"{int(ketu_deg)}°{round((ketu_deg%1)*60):02d}'",
        'retrograde': True, 'speed': -result[0][3],
        'house': get_house(ketu_sign_idx, lagna['sign_idx']),
        'nakshatra': get_nakshatra(ketu_lon)
    }
    
    # 4. SAV/BAV (PyJHora — no fallback)
    tz = pytz.timezone(tz_str)
    _tz_dt = _localize_strict(tz, datetime(year, month, day, hour, minute))
    _tz_offset = _tz_dt.utcoffset().total_seconds() / 3600.0
    ashtak = _av_pyjhora(year, month, day, hour, minute, lat, lon, _tz_offset)
    
    # Map SAV to houses
    sav_by_house = {}
    for h in range(1, 13):
        sign_idx = (lagna['sign_idx'] + h - 1) % 12
        sign_name = SIGNS[sign_idx]
        sav_by_house[h] = {'sign': sign_name, 'value': ashtak['sarvashtakavarga'].get(sign_name, 0)}
    
    # 5. Divisional charts (PyJHora: 15 charts)
    if _div_pyjhora is not None:
        divisional_charts = _div_pyjhora(
            year, month, day, hour, minute, lat, lon, _tz_offset
        )
    else:
        divisional_charts = {}
    
    # Extract d9/d10/d4/d5 in legacy (sign_name, sign_idx) format for backward compat
    if divisional_charts:
        def _legacy_fmt(chart_key):
            ch = divisional_charts.get(chart_key, {})
            return {p: (ch[p]['sign'], ch[p]['sign_idx']) for p in ch if 'error' not in ch}
        d9 = _legacy_fmt('D9')
        d10 = _legacy_fmt('D10')
        d4 = _legacy_fmt('D4')
        d5 = _legacy_fmt('D5')
    else:
        d9, d10, d4, d5 = {}, {}, {}, {}
    
    # Vargottama check
    vargottama = {}
    for name in planets:
        d9_sign = d9.get(name, (None, None))
        d9_sign_name = d9_sign[0] if isinstance(d9_sign, tuple) else d9_sign.get('sign', None) if isinstance(d9_sign, dict) else None
        vargottama[name] = planets[name]['sign'] == d9_sign_name
    
    # 6. Dignity & Compound Relationship (自建，不依赖dashaflow)
    # BPHS Panchadha Maitri 算法
    
    # Step 1: 旺/入庙/陷检测
    EXALTATION = {'Sun':'Aries','Moon':'Taurus','Mars':'Capricorn',
                  'Mercury':'Virgo','Jupiter':'Cancer','Venus':'Pisces','Saturn':'Libra'}
    DEBILITATION = {'Sun':'Libra','Moon':'Scorpio','Mars':'Cancer',
                    'Mercury':'Pisces','Jupiter':'Capricorn','Venus':'Virgo','Saturn':'Aries'}
    OWN_SIGNS = {'Sun':['Leo'],'Moon':['Cancer'],'Mars':['Aries','Scorpio'],
                 'Mercury':['Gemini','Virgo'],'Jupiter':['Sagittarius','Pisces'],
                 'Venus':['Taurus','Libra'],'Saturn':['Capricorn','Aquarius']}
    
    # Step 2: 自然关系表 (Naisargika Maitri) - BPHS标准
    NATURAL_REL = {
        'Sun':     {'friend':['Moon','Mars','Jupiter'], 'enemy':['Venus','Saturn'], 'neutral':['Mercury']},
        'Moon':    {'friend':['Sun','Mercury'], 'enemy':[], 'neutral':['Mars','Jupiter','Venus','Saturn']},
        'Mars':    {'friend':['Sun','Moon','Jupiter'], 'enemy':['Mercury'], 'neutral':['Venus','Saturn']},
        'Mercury': {'friend':['Sun','Venus'], 'enemy':['Moon'], 'neutral':['Mars','Jupiter','Saturn']},
        'Jupiter': {'friend':['Sun','Moon','Mars'], 'enemy':['Mercury','Venus'], 'neutral':['Saturn']},
        'Venus':   {'friend':['Mercury','Saturn'], 'enemy':['Sun','Moon'], 'neutral':['Mars','Jupiter']},
        'Saturn':  {'friend':['Mercury','Venus'], 'enemy':['Sun','Moon','Mars'], 'neutral':['Jupiter']},
    }
    
    def get_natural_rel(planet, lord):
        """查自然关系: friend/enemy/neutral"""
        if planet == lord:
            return 'own'
        rel = NATURAL_REL.get(planet, {})
        if lord in rel.get('friend', []): return 'friend'
        if lord in rel.get('enemy', []): return 'enemy'
        return 'neutral'
    
    def get_temporal_rel(planet_sign_idx, lord_sign_idx):
        """查临时关系: 座主落在行星的2/3/4/10/11/12宫=临时友"""
        dist = (lord_sign_idx - planet_sign_idx) % 12
        # 距离2,3,4,10,11,12宫 = dist值1,2,3,9,10,11 (0-indexed)
        return 'temp_friend' if dist in {1,2,3,9,10,11} else 'temp_enemy'
    
    # Step 4: Panchadha合成表
    COMPOUND_TABLE = {
        ('friend', 'temp_friend'):   'great_friend',
        ('friend', 'temp_enemy'):    'neutral',
        ('enemy',  'temp_friend'):   'neutral',
        ('enemy',  'temp_enemy'):    'great_enemy',
        ('neutral','temp_friend'):   'friend',
        ('neutral','temp_enemy'):    'enemy',
    }
    
    dignity_data = {}
    for name in ['Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn']:
        p = planets[name]
        sign = p['sign']
        lord = SIGN_LORDS[p['sign_idx']]
        
        # Step 1: 旺/入庙/陷直接确定
        if EXALTATION.get(name) == sign:
            compound = 'exalted'
        elif DEBILITATION.get(name) == sign:
            compound = 'debilitated'
        elif sign in OWN_SIGNS.get(name, []):
            compound = 'own_sign'
        else:
            # Step 2+3+4: 自然+临时→合成
            natural = get_natural_rel(name, lord)
            if natural == 'own':
                compound = 'own_sign'
            else:
                # 找座主的实际位置
                lord_sign_idx = planets[lord]['sign_idx'] if lord in planets else p['sign_idx']
                temporal = get_temporal_rel(p['sign_idx'], lord_sign_idx)
                compound = COMPOUND_TABLE.get((natural, temporal), 'neutral')
        
        dignity_data[name] = {'basic': compound, 'compound': compound}

    # 6b. D9 自然尊贵度 (PQ-01: 纯查表补算，禁模型通识判读 D9 入旺/落陷/座主链)
    #     只用自然尊贵 (旺exalted/庙own/陷debilitated/友friend/敌enemy/中性neutral)
    #     不含临时/合成关系——D9 尊贵直接查表，答案确定。
    d9_dignity = {}
    for name in ['Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn']:
        d9_entry = d9.get(name)
        if not d9_entry:
            continue
        d9_sign, d9_sign_idx = d9_entry[0], d9_entry[1]
        dispositor = SIGN_LORDS[d9_sign_idx]  # D9 房东星
        if EXALTATION.get(name) == d9_sign:
            d9_dig = 'exalted'
        elif DEBILITATION.get(name) == d9_sign:
            d9_dig = 'debilitated'
        elif d9_sign in OWN_SIGNS.get(name, []):
            d9_dig = 'own'
        else:
            d9_dig = get_natural_rel(name, dispositor)  # friend/enemy/neutral
        d9_dignity[name] = {'sign': d9_sign, 'dignity': d9_dig, 'dispositor': dispositor}

    # 6c. 分盘内部宫主表 + 分盘尊贵度（D9/D10/D4/D5——线A"分盘内部宫主"数据化，禁 AI 自推）
    #     house_lords：以【分盘自身 Lagna】起宫，H1~H12 各座主 + 该座主在本分盘落宫。
    #     dignity：每星在本分盘座的自然尊贵（同 D9 查表）。消灭"D10-L10 是谁"自推出错的土壤。
    varga_internal = {}
    for dv in ['D9', 'D10', 'D4', 'D5']:
        ch = divisional_charts.get(dv) if divisional_charts else None
        if not ch or 'error' in ch or 'Lagna' not in ch:
            continue
        v_lag = ch['Lagna']['sign_idx']
        v_lords = {}
        for house in range(1, 13):
            s_idx = (v_lag + house - 1) % 12
            lord = SIGN_LORDS[s_idx]
            le = ch.get(lord)
            lord_house = ((le['sign_idx'] - v_lag) % 12) + 1 if le else None
            v_lords[house] = {'sign': SIGNS[s_idx], 'lord': lord, 'lord_house': lord_house}
        v_dig = {}
        for name in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
            e = ch.get(name)
            if not e:
                continue
            s, sidx = e['sign'], e['sign_idx']
            disp = SIGN_LORDS[sidx]
            if EXALTATION.get(name) == s:
                dg = 'exalted'
            elif DEBILITATION.get(name) == s:
                dg = 'debilitated'
            elif s in OWN_SIGNS.get(name, []):
                dg = 'own'
            else:
                dg = get_natural_rel(name, disp)
            v_dig[name] = {'sign': s, 'house': ((sidx - v_lag) % 12) + 1,
                           'dignity': dg, 'dispositor': disp}
        varga_internal[dv] = {'lagna_sign': SIGNS[v_lag], 'lagna_lord': SIGN_LORDS[v_lag],
                              'house_lords': v_lords, 'dignity': v_dig}

    # 7. Combustion check
    sun_lon = planets['Sun']['longitude']
    combustion = {}
    for name in ['Moon','Mars','Mercury','Jupiter','Venus','Saturn']:
        is_retro = planets[name]['retrograde']
        comb_result = check_combustion(name, planets[name]['longitude'], sun_lon, is_retro)
        is_combust = comb_result if isinstance(comb_result, bool) else comb_result.get('is_combust', False)
        if is_combust:
            diff = abs(planets[name]['longitude'] - sun_lon)
            if diff > 180: diff = 360 - diff
            combustion[name] = {'distance': round(diff, 2)}
    
    # 8. Chara Karakas (7K primary)
    karakas = calc_chara_karakas_7k8k(planets)
    
    # 9. Graha drishti（吠陀宫位照射）——西占 orb 相位表已废弃删除：不属 KN Rao 体系、无判定消费方
    graha_drishti = calc_graha_drishti(planets)  # P10 Parashari graha drishti（宫位照射，禁手推）
    functional = calc_functional(lagna['sign_idx'], planets)      # B3 P1主身份（一星多宫主MT定主，禁手推）

    # 10. House lords
    house_lords = calc_house_lords(lagna['sign_idx'])
    # Add planet positions to house lords
    for h, info in house_lords.items():
        planet = info['lord']
        if planet in planets:
            info['lord_house'] = planets[planet]['house']
    mutual_drishti = calc_mutual_drishti(graha_drishti)   # 互视对（双向，格局"互视"唯一口径，单向不算）
    parivartana = calc_parivartana(house_lords, planets)  # 互溶对（两宫主互换落座，格局"互溶"唯一口径）
    yoga_prescan = calc_yoga_prescan(lagna['sign_idx'], planets, house_lords, graha_drishti, mutual_drishti, parivartana)  # 全11格局结构预扫（禁自推/越宫）

    # 11. Vimsottari Dasha (PyJHora — no fallback)
    dashas = _dasha_pyjhora(year, month, day, hour, minute, lat, lon, _tz_offset)
    
    # 12. Shadbala (PyJHora + 9 bug fixes — no fallback)
    shadbala_data = _shadbala_pyjhora(
        year, month, day, hour, minute, lat, lon, _tz_offset
    )
    
    # 13. Moon phase
    moon_sun_diff = (planets['Moon']['longitude'] - planets['Sun']['longitude']) % 360
    is_waxing = moon_sun_diff < 180
    
    # 14. Digbala
    digbala = {}
    for name in ['Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn']:
        digbala[name] = get_digbala(name, planets[name]['house'])
    
    # 15. Special Points (AL, UL)
    special_points = calc_special_points(lagna, planets)
    
    # 16. Transit positions (current slow planet positions)
    transits = calc_transits(lagna['sign_idx'], planets['Moon']['sign_idx'])
    
    # 17. Bhava Bala, Special Lagnas, Vargeeya Bala (via PyJHora)
    bhava_bala = None
    special_lagnas = None
    vargeeya_bala = None
    pushkara = None
    if any([_bhava_bala_pyjhora, _special_lagnas_pyjhora, _vargeeya_bala_pyjhora]):
        try:
            tz = pytz.timezone(tz_str)
            _tz_dt = _localize_strict(tz, datetime(year, month, day, hour, minute))
            _tz_offset = _tz_dt.utcoffset().total_seconds() / 3600.0
            if _bhava_bala_pyjhora:
                bhava_bala = _bhava_bala_pyjhora(year, month, day, hour, minute, lat, lon, _tz_offset)
            if _special_lagnas_pyjhora:
                special_lagnas = _special_lagnas_pyjhora(year, month, day, hour, minute, lat, lon, _tz_offset)
            if _vargeeya_bala_pyjhora:
                vargeeya_bala = _vargeeya_bala_pyjhora(year, month, day, hour, minute, lat, lon, _tz_offset)
            if _pushkara_pyjhora:
                pushkara = _pushkara_pyjhora(year, month, day, hour, minute, lat, lon, _tz_offset)
        except Exception:
            pass
    
    # DST 透明标注：出生时刻是否处于当地夏令时（pytz 默认把报时当墙上钟时间处理）
    try:
        _tzd = pytz.timezone(tz_str)
        _dtd = _localize_strict(_tzd, datetime(year, month, day, hour, minute))
        dst_info = {'is_dst': bool(_dtd.dst()), 'utc_offset': str(_dtd.utcoffset())}
    except Exception:
        dst_info = None

    # Chara Dasha (K.N. Rao) — engine 真值输入（JHora 双盘金标准 24/24 验证）
    chara_dasha = None
    if _chara_dasha:
        try:
            _sign_idx = {s: i for i, s in enumerate(SIGNS)}
            _psigns = {p: _sign_idx[planets[p]['sign']] for p in planets}
            chara_dasha = _chara_dasha(_sign_idx[lagna['sign']], _psigns, jd)
        except Exception:
            pass

    return {
        'ayanamsa': ayanamsa,
        'lagna': lagna,
        'planets': planets,
        'sav': ashtak['sarvashtakavarga'],
        'sav_by_house': sav_by_house,
        'bav': ashtak['bhinnashtakavarga'],
        'd9': d9, 'd10': d10, 'd4': d4, 'd5': d5,
        'divisional_charts': divisional_charts,
        'vargottama': vargottama,
        'dignity': dignity_data,
        'd9_dignity': d9_dignity,
        'varga_internal': varga_internal,
        'combustion': combustion,
        'karakas': karakas,
        'graha_drishti': graha_drishti,
        'functional': functional,
        'yoga_prescan': yoga_prescan,
        'mutual_drishti': mutual_drishti,
        'parivartana': parivartana,
        'house_lords': house_lords,
        'dashas': dashas,
        'shadbala': shadbala_data,
        'moon_phase': {'waxing': is_waxing, 'sun_moon_diff': round(moon_sun_diff, 1)},
        'digbala': digbala,
        'special_points': special_points,
        'transits': transits,
        'bhava_bala': bhava_bala,
        'special_lagnas': special_lagnas,
        'vargeeya_bala': vargeeya_bala,
        'pushkara': pushkara,
        'chara_dasha': chara_dasha,
        'dst_info': dst_info,
    }


# === TEST ===
if __name__ == '__main__':
    print("=== vedic-calculator v0.2 Full Test ===\n")
    
    # Gandhi: 1869-10-02, 07:12, Porbandar
    chart = calculate_full_chart(1869, 10, 2, 7, 12, 21.6417, 69.6293, "Asia/Kolkata")
    
    print(f"Ayanamsa (True Chitra): {chart['ayanamsa']:.4f}°")
    print(f"Lagna: {chart['lagna']['sign']} {chart['lagna']['deg_str']}")
    
    print(f"\n--- Planets ---")
    print(f"  {'Planet':<10} {'Sign':<12} {'Deg':>8} {'H':>3} {'R':>2} {'Dignity':<16} {'Compound'}")
    for name in ['Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn','Rahu','Ketu']:
        p = chart['planets'][name]
        r = 'R' if p['retrograde'] else ''
        dig = chart['dignity'].get(name, {})
        basic = dig.get('basic', '-')
        compound = dig.get('compound', '-')
        print(f"  {name:<10} {p['sign']:<12} {p['deg_str']:>8} {p['house']:>3} {r:>2} {str(basic):<16} {compound}")
    
    print(f"\n--- SAV by House ---")
    total = 0
    for h in range(1, 13):
        s = chart['sav_by_house'][h]
        total += s['value']
        print(f"  {h}宫({s['sign'][:2]}): {s['value']}", end='  ')
        if h % 6 == 0: print()
    print(f"  Total: {total}")
    
    print(f"\n--- Chara Karakas (7K) ---")
    for k, planet, deg in chart['karakas']['7k']:
        print(f"  {k}: {planet} ({deg:.1f}°)")
    print(f"  DK: 7K(主)={chart['karakas']['dk_7k']}, 8K(参考)={chart['karakas']['dk_8k']}")
    
    print(f"\n--- Dasha ---")
    for d in chart['dashas']:
        marker = '→' if d['is_current'] else ' '
        print(f"  {marker} {d['planet']:<10} {d['start']} ~ {d['end']}  ({d['years']}yr)")
    
    print(f"\n--- D9 Navamsha ---")
    for name in ['Lagna','Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn','Rahu','Ketu']:
        sign = chart['d9'][name][0]
        varg = ' ★V' if chart['vargottama'].get(name, False) else ''
        print(f"  {name:<10} → {sign}{varg}")
    
    print(f"\n--- Shadbala ---")
    if 'error' in chart['shadbala']:
        print(f"  Error: {chart['shadbala']['error']}")
    else:
        for name, data in chart['shadbala'].items():
            if isinstance(data, dict):
                total = data.get('total_rupas', data.get('total', '?'))
                print(f"  {name:<10} {total}")
    
    print(f"\n--- Moon Phase ---")
    phase = chart['moon_phase']
    print(f"  {'盈月(Shukla)' if phase['waxing'] else '亏月(Krishna)'}, 距Sun {phase['sun_moon_diff']}°")
    
    print(f"\n--- Combustion ---")
    if chart['combustion']:
        for name, data in chart['combustion'].items():
            print(f"  {name}: {data}")
    else:
        print("  无燃烧行星")
    
    print(f"\n--- House Lords ---")
    for h in range(1, 13):
        info = chart['house_lords'][h]
        print(f"  {h}宫({info['domain']}): {info['lord']} → {info.get('lord_house','?')}宫")
    
    print(f"\n✅ 全部14个数据板块计算完成!")
