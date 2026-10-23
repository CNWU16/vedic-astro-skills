"""
vedic-calculator v1.0.1 - PyJHora 精确计算引擎
基于 pysweph 天文核心 + PyJHora 精确算法（含 9 项 Shadbala bug 修正）
输出完整的 structured_data 所需数据

v1.0.1: 附加项（Bhava Bala、特殊上升点、Vargeeya、Pushkara）各自捕获异常，一项出错不再连带跳过其余；
      出错项记 {'error': ...}，Chara Dasha 出错仍为 None；原因统一进新增的 calc_errors（此前两处
      except Exception: pass 静默留空）。数值零变化（24 盘基线只多 calc_errors 键）。
v1.0: ① 秒级瞬间：calculate_full_chart/to_jd 收 second（可带小数），整张盘只本地化一次，
      JD 与各 PyJHora 包装的时区偏移、时间都从它派生（此前包装各自用整分重建，秒级调用方只能
      下游补算，即时盘因此混用两个瞬间）。整分调用方输出逐字节不变（24 盘基线实测）。
      ② Lagna 基准＝视位置回归 Lagna − 与行星同口径的岁差，与桌面 JHora 一致（客户 JHora 打印盘
      实证差 0.004″）；PyJHora 分盘经 houses_ex 补丁统一到同一基准；chart["ayanamsa"] 报实际值。
      ⚠️ 本版有数值变化：Lagna 平均 ±14″（最大 ±39″），分界附近的盘分盘 Lagna 可能换座。
      ③ 极圈盘 Dig Bala 走 Placidus 无解时按 Swiss Ephemeris 文档改用 Porphyry（此前整盘报错）。
      ④ 当前大运标记按出生偏移比较带时区的 as_of（此前用机器本地时钟）；删除 calc_transits
      （本机时间当 UT，无消费者）；新增 calc_meta 溯源（引擎版本、UTC 瞬间、实际岁差）。
v0.9: D1 星历 flags 统一到 PyJHora 的 66386（真位置/无章动/无引力偏折），此前 engine 自算
      D1 用 65792（视位置），同一张盘的 D1 表与 SAV/D9/Dasha 分属两套基准，实测差 0~60″；
      Vimsottari year_duration 在 L1 前显式对齐（原先 L1 用平均恒星年或上一张盘的残留值，
      末 MD 结束点每张盘都偏，实测 21/26）；deg_str 加进位收敛（原会产出 "12°60'"）。
      ⚠️ 本版有数值变化：行星经度 0~60″、deg_str 偶尔 ±1′、末 MD end/end_time
v0.8: 去掉 dashaflow 依赖（燃烧/方位强宫两表内联）；sid_mode/ephe_path 改每线程重设；
      dasha 包装层猴补丁哨兵与其余包装层统一（修常驻进程约 490 盘后 RecursionError）
v0.7: 增加 D1/D9/D10/D4/D5 报时不确定区间边界审计，区分“算得出”与“输入稳定”
v0.6: Vimsottari 增加完整 Pratyantardasha 三级运，月级分析不再借用 AD 假精度
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
import threading
import pytz
import json

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
# 星历路径：显式指向 skill 自带 ephe（.se1），确保首次 calculate_full_chart 的 calc_ut 就用
# Swiss 星历。否则 engine 自身从不 set_ephe_path，首盘 calc_planet 在 PyJHora 模块（首次调用
# 中途才 set_ephe_path）之前跑 → 跌回 Moshier 近似，与后续盘差 ~0.5 角秒（PQ-02 同进程重复
# 排盘漂移的真根因；产品诊断的 sid_mode 修法经实测无效）。
_EPHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ephe')

# swisseph 的 sid_mode / ephe_path 都是线程局部状态：只在 import 线程设置一次，
# 其它线程（产品 API/worker 线程池）里 engine 自算的 D1/Lagna 会退回默认岁差(实测差 0.89°)
# 且星历退回 Moshier；而 PyJHora 包装层每次调用自带重设，于是同一张盘半盘中毒、看不出来。
# 故改为每线程首次进入计算时重设一次（threading.local 守门，重复调用零开销）。
_swe_state = threading.local()

def _ensure_swe_state():
    if getattr(_swe_state, 'ready', False):
        return
    swe.set_sid_mode(swe.SIDM_TRUE_CITRA)
    if os.path.isdir(_EPHE_DIR):
        swe.set_ephe_path(_EPHE_DIR)
    _swe_state.ready = True

_ensure_swe_state()   # import 线程

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

# 燃烧 orb（度）与方位强宫：原取自 dashaflow.dignity / dashaflow.constants（1.1.0），
# 为去掉 dashaflow 依赖（其声明依赖已停更的 pyswisseph，安装需 --no-deps 特殊步骤）逐字内联。
# 数值与判定逻辑与 dashaflow 完全一致，输出零变化。
COMBUSTION_ORBS = {
    'Moon': 12, 'Mars': 17, 'Mercury': {'direct': 14, 'retrograde': 12},
    'Jupiter': 11, 'Venus': {'direct': 10, 'retrograde': 8}, 'Saturn': 15
}
DIGBALA_HOUSES = {'Jupiter': 1, 'Mercury': 1, 'Sun': 10, 'Mars': 10, 'Saturn': 7, 'Moon': 4, 'Venus': 4}

def check_combustion(planet_name, planet_lon, sun_lon, is_retrograde=False):
    """行星是否燃烧（与太阳角距 ≤ orb）。Sun/Rahu/Ketu 不燃烧。"""
    orb = COMBUSTION_ORBS.get(planet_name)
    if orb is None:
        return False
    if isinstance(orb, dict):
        orb = orb['retrograde'] if is_retrograde else orb['direct']
    dist = abs(planet_lon - sun_lon)
    if dist > 180:
        dist = 360 - dist
    return dist <= orb

def get_digbala(planet_name, house):
    """行星是否落在其方位强宫。"""
    return DIGBALA_HOUSES.get(planet_name) == house

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


def local_instant(year, month, day, hour, minute, tz_str, second=0, fold=None):
    """出生／提问时刻的唯一本地化：返回带时区的本地 datetime。

    second 可带小数（微秒）。整张盘只在这里本地化一次，JD 与各子模块的时区偏移都从它派生，
    不再各自用整分重建（DST 交界处整分重建会给出另一个偏移）。
    fold：只给已知瞬间用（如带时区的“当下”）——夏令时回拨的重复时段按 fold 消歧
    （0＝第一次，1＝第二次）。手填的歧义时刻不传 fold，照旧明确报错。
    """
    tz = pytz.timezone(tz_str)
    whole = int(second)
    micro = int(round((second - whole) * 1_000_000))
    if micro == 1_000_000:
        whole, micro = whole + 1, 0
    naive = datetime(year, month, day, hour, minute) + timedelta(seconds=whole, microseconds=micro)
    if fold is not None:
        try:
            return tz.localize(naive, is_dst=None)
        except pytz.exceptions.AmbiguousTimeError:
            return tz.localize(naive, is_dst=(fold == 0))
        except pytz.exceptions.NonExistentTimeError:
            pass
    return _localize_strict(tz, naive)


def instant_to_jd(local_dt):
    """带时区的 datetime → UT 儒略日（含秒与微秒）。"""
    utc_dt = local_dt.astimezone(pytz.utc)
    ut_hour = (utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0
               + utc_dt.microsecond / 3_600_000_000.0)
    return swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, ut_hour)


def to_jd(year, month, day, hour, minute, tz_str, second=0):
    return instant_to_jd(local_instant(year, month, day, hour, minute, tz_str, second))

# 行星位置 flags：与 PyJHora 的 drik.PLANET_FLAGS 逐位一致（实测 66386）。
# 此前 engine 自算 D1 用 FLG_SIDEREAL|FLG_SPEED(65792)，即视位置(apparent)；
# 而 SAV/D9/Dasha 等走 PyJHora 的部分用真位置(TRUEPOS)+不含章动/引力偏折，
# 同一张盘的 D1 表与其余分盘因此分属两套基准，实测差 0~60″。
# 统一到 PyJHora 一侧：该侧是当年逐项对照桌面 JHora 验证过的那一半。
PLANET_FLAGS = (swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
                | swe.FLG_TRUEPOS | swe.FLG_NONUT | swe.FLG_NOGDEFL)

ENGINE_VERSION = "v1.0.1"


def ayanamsa_value(jd):
    """行星与 Lagna 实际使用的岁差（与 PLANET_FLAGS 同口径；桌面 JHora 打印的就是这个值）。"""
    return swe.get_ayanamsa_ex_ut(jd, PLANET_FLAGS)[1]


def _deg_min(degree):
    """星座内度数 → "D°MM'"，带进位收敛。

    直接 round 到分会在 x.9959°~x.99999° 区间产出 "12°60'" 这种非法值；
    进位到 30° 又会越出星座边界（sign 由 longitude 决定，不会跟着走），
    故末度只收敛到 29°59'。
    """
    d = int(degree)
    m = round((degree - d) * 60)
    if m == 60:
        if d >= 29:
            m = 59          # 星座末尾：进位会越界成 30°，退回截断
        else:
            d += 1
            m = 0
    return f"{d}°{m:02d}'"


def calc_planet(jd, planet_id):
    _ensure_swe_state()
    result = swe.calc_ut(jd, planet_id, PLANET_FLAGS)
    lon = result[0][0]
    speed = result[0][3]
    sign_idx = int(lon / 30)
    degree = lon % 30
    return {
        'longitude': lon, 'sign': SIGNS[sign_idx], 'sign_idx': sign_idx,
        'degree': degree, 'deg_str': _deg_min(degree),
        'retrograde': speed < 0, 'speed': speed
    }

def calc_lagna(jd, lat, lon):
    """Lagna = 视位置回归 Lagna − 与行星同口径的岁差（ayanamsa_value）。

    与桌面 JHora 一致（2026-10-23，客户 JHora 打印盘 2004-09-12 11:15:27 上海：差 0.004″）。
    旧口径 houses_ex(FLG_SIDEREAL) 内部用的岁差不含 TRUEPOS、含章动，True Chitra 下与行星
    口径差 ±39″；PyJHora 的 FLG_TRUEPOS 口径差 ±19″。PyJHora 分盘经 *_pyjhora.py 的
    houses_ex 补丁统一到这里的同一基准。
    """
    _ensure_swe_state()
    ascmc = swe.houses_ex(jd, lat, lon, b'W', 0)[1]
    asc_lon = (ascmc[0] - ayanamsa_value(jd)) % 360
    sign_idx = int(asc_lon / 30)
    degree = asc_lon % 30
    return {
        'longitude': asc_lon, 'sign': SIGNS[sign_idx], 'sign_idx': sign_idx,
        'degree': degree, 'deg_str': _deg_min(degree)
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

    分类出处 Mantreswara《Phaladeepika》VI.32-34，28+8+30=66=C(12,2) 完备划分、无第四档：
      Dainya = 6/8/12 任一宫主参与（**单侧即成立**，30 组）
      Khala  = 3宫主 与吉宫主互换（8 组）
      Maha   = 吉宫主之间互换（28 组）
    优先级 Dainya > Khala > Maha，故 3宫↔6/8/12 归 Dainya 而非 Khala。
    ⚠️ Dainya 曾被写成"6/8/12 彼此之间"的双侧条件，把 30 组压成 3 组，其余 27 组
       落进一个无释义的 'Mixed' 档（24 组）并把 3 组误判成 Khala。单侧是正确口径，
       改回后 'Mixed' 不再产生——规则正文见 vedic-core/resources/yogas.md 同名节。
    返回 [{houses,lords,type},...]。"""
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
                if x in DUS or y in DUS:
                    kind = 'Dainya(凶宫参与)'
                elif x == 3 or y == 3:
                    kind = 'Khala(3宫参与)'
                else:
                    kind = 'Maha(吉宫互溶)'  # 余下必为吉宫对：三类完备，无 fallback
                pairs.append({'houses': [x, y], 'lords': [lx, ly], 'type': kind})
    return pairs

def calc_vimsottari_dasha(moon_lon, birth_year, birth_month, birth_day, birth_hour, birth_minute):
    """Deprecated approximate entry point; Vimsottari must come from PyJHora.

    Keeping a fail-fast shim prevents older callers from silently reviving the former
    365.25-day MD/AD approximation, which cannot supply validated PD boundaries.
    Use ``calculate_full_chart``; it calls ``dasha_pyjhora.calculate_dasha_fixed``.
    """
    raise RuntimeError(
        "calc_vimsottari_dasha is disabled: use calculate_full_chart() so "
        "PyJHora supplies validated MD/AD/PD boundaries"
    )

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

# === 出生时刻边界审计 ===

def calc_divisional_boundary_audit(year, month, day, hour, minute, lat, lon,
                                    tz_str="Asia/Kolkata", uncertainty_minutes=1, second=0):
    """逐分钟扫描报时不确定区间内的 D1 与主要分盘 Lagna。

    “直接计算成功”只证明给定时刻的数学结果可复现；如果同一报时允许的分钟区间
    跨过分盘 Lagna 换座点，分盘宫位、分盘宫主和所有下游解释必须按条件分支处理。
    以精确出生时刻（含秒）为中心，前后各取整分钟偏移。
    """
    if _div_pyjhora is None:
        return {
            'status': 'unavailable',
            'reason': 'PyJHora divisional module unavailable',
        }

    try:
        span = max(0, int(uncertainty_minutes or 0))
    except (TypeError, ValueError):
        span = 1

    base_local = local_instant(year, month, day, hour, minute, tz_str, second).replace(tzinfo=None)
    factors = (4, 5, 9, 10)
    samples = []

    for offset in range(-span, span + 1):
        local_dt = base_local + timedelta(minutes=offset)
        localized = _localize_strict(pytz.timezone(tz_str), local_dt)
        tz_offset = localized.utcoffset().total_seconds() / 3600.0
        sec = local_dt.second + local_dt.microsecond / 1_000_000
        jd = instant_to_jd(localized)
        d1_lagna = calc_lagna(jd, lat, lon)['sign']
        charts = _div_pyjhora(
            local_dt.year, local_dt.month, local_dt.day,
            local_dt.hour, local_dt.minute, lat, lon, tz_offset,
            chart_factors=factors, second=sec,
        )
        row = {'offset_minutes': offset, 'D1': d1_lagna}
        for factor in factors:
            key = f'D{factor}'
            chart_data = charts.get(key, {})
            if 'error' in chart_data or 'Lagna' not in chart_data:
                row[key] = None
            else:
                row[key] = chart_data['Lagna']['sign']
        samples.append(row)

    result = {}
    for key in ('D1', 'D9', 'D10', 'D4', 'D5'):
        observed = []
        transitions = []
        previous = None
        for row in samples:
            sign = row.get(key)
            if sign is not None and sign not in observed:
                observed.append(sign)
            if previous is not None and sign is not None and sign != previous:
                transitions.append({
                    'offset_minutes': row['offset_minutes'],
                    'from': previous,
                    'to': sign,
                })
            if sign is not None:
                previous = sign
        base_sign = next((row.get(key) for row in samples
                          if row['offset_minutes'] == 0), None)
        result[key] = {
            'base_sign': base_sign,
            'stable': len(observed) == 1 and bool(observed),
            'observed_signs': observed,
            'transitions': transitions,
        }

    return {
        'status': 'ok',
        'uncertainty_minutes': span,
        'sample_step_minutes': 1,
        'charts': result,
        'samples': samples,
    }


# === 主计算函数 ===

def calculate_full_chart(year, month, day, hour, minute, lat, lon,
                         tz_str="Asia/Kolkata", uncertainty_minutes=1, second=0, as_of=None,
                         fold=None):
    """计算完整星盘数据。

    second：秒（可带小数），默认 0，整分调用方结果不变。整张盘只有一个计算瞬间：
    本地化一次，JD 与各 PyJHora 包装的时区偏移、时间都从它派生。
    as_of：判“当前大运／小运”用的带时区时刻，默认当下 UTC。
    fold：见 local_instant，只给已知瞬间用。
    """
    _ensure_swe_state()
    _instant = local_instant(year, month, day, hour, minute, tz_str, second, fold=fold)
    jd = instant_to_jd(_instant)
    _tz_offset = _instant.utcoffset().total_seconds() / 3600.0
    ayanamsa = ayanamsa_value(jd)
    
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
    result = swe.calc_ut(jd, swe.MEAN_NODE, PLANET_FLAGS)
    rahu_lon = result[0][0]
    rahu_sign_idx = int(rahu_lon / 30)
    rahu_deg = rahu_lon % 30
    planets['Rahu'] = {
        'longitude': rahu_lon, 'sign': SIGNS[rahu_sign_idx],
        'sign_idx': rahu_sign_idx, 'degree': rahu_deg,
        'deg_str': _deg_min(rahu_deg),
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
        'deg_str': _deg_min(ketu_deg),
        'retrograde': True, 'speed': -result[0][3],
        'house': get_house(ketu_sign_idx, lagna['sign_idx']),
        'nakshatra': get_nakshatra(ketu_lon)
    }
    
    # 4. SAV/BAV (PyJHora — no fallback)
    ashtak = _av_pyjhora(year, month, day, hour, minute, lat, lon, _tz_offset, second=second)
    
    # Map SAV to houses
    sav_by_house = {}
    for h in range(1, 13):
        sign_idx = (lagna['sign_idx'] + h - 1) % 12
        sign_name = SIGNS[sign_idx]
        sav_by_house[h] = {'sign': sign_name, 'value': ashtak['sarvashtakavarga'].get(sign_name, 0)}
    
    # 5. Divisional charts (PyJHora: 15 charts)
    if _div_pyjhora is not None:
        divisional_charts = _div_pyjhora(
            year, month, day, hour, minute, lat, lon, _tz_offset, second=second
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

    divisional_boundary_audit = calc_divisional_boundary_audit(
        year, month, day, hour, minute, lat, lon, tz_str,
        uncertainty_minutes=uncertainty_minutes, second=second,
    )
    
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
        if check_combustion(name, planets[name]['longitude'], sun_lon, is_retro):
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

    # 11. Vimsottari Dasha MD/AD/PD (PyJHora — no fallback)
    dashas = _dasha_pyjhora(year, month, day, hour, minute, lat, lon, _tz_offset,
                            second=second, as_of=as_of)

    # 12. Shadbala (PyJHora + 9 bug fixes — no fallback)
    shadbala_data = _shadbala_pyjhora(
        year, month, day, hour, minute, lat, lon, _tz_offset, second=second
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
    
    # 16. 过运：engine 不再给（旧 calc_transits 把本机墙上时间当 UT，且 skill 内无消费者）；
    #     过运一律走 transit.py。

    # 17. Bhava Bala, Special Lagnas, Vargeeya Bala, Pushkara (via PyJHora)
    #     各项单独捕获：一项出错不再连带跳过后面几项；出错项记成 {'error': ...}（与包装函数自己的
    #     出错约定一致），原因同时进 calc_errors，不再静默留空。
    calc_errors = {}
    _extra = (year, month, day, hour, minute, lat, lon, _tz_offset)
    _extra_results = {}
    for _name, _fn in (('bhava_bala', _bhava_bala_pyjhora), ('special_lagnas', _special_lagnas_pyjhora),
                       ('vargeeya_bala', _vargeeya_bala_pyjhora), ('pushkara', _pushkara_pyjhora)):
        if _fn is None:
            _extra_results[_name] = None
            continue
        try:
            _extra_results[_name] = _fn(*_extra, second=second)
        except Exception as e:
            _extra_results[_name] = {'error': f'{type(e).__name__}: {e}'}
            calc_errors[_name] = _extra_results[_name]['error']
    bhava_bala = _extra_results['bhava_bala']
    special_lagnas = _extra_results['special_lagnas']
    vargeeya_bala = _extra_results['vargeeya_bala']
    pushkara = _extra_results['pushkara']

    # DST 透明标注：出生时刻是否处于当地夏令时（pytz 默认把报时当墙上钟时间处理）
    dst_info = {'is_dst': bool(_instant.dst()), 'utc_offset': str(_instant.utcoffset())}

    # Chara Dasha (K.N. Rao) — engine 真值输入（JHora 双盘金标准 24/24 验证）
    #     出错时 chara_dasha 仍为 None（formatter 据此不出该节），原因进 calc_errors。
    chara_dasha = None
    if _chara_dasha:
        try:
            _sign_idx = {s: i for i, s in enumerate(SIGNS)}
            _psigns = {p: _sign_idx[planets[p]['sign']] for p in planets}
            chara_dasha = _chara_dasha(_sign_idx[lagna['sign']], _psigns, jd)
        except Exception as e:
            calc_errors['chara_dasha'] = f'{type(e).__name__}: {e}'

    return {
        'ayanamsa': ayanamsa,
        'lagna': lagna,
        'planets': planets,
        'sav': ashtak['sarvashtakavarga'],
        'sav_by_house': sav_by_house,
        'bav': ashtak['bhinnashtakavarga'],
        'd9': d9, 'd10': d10, 'd4': d4, 'd5': d5,
        'divisional_charts': divisional_charts,
        'divisional_boundary_audit': divisional_boundary_audit,
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
        'bhava_bala': bhava_bala,
        'special_lagnas': special_lagnas,
        'vargeeya_bala': vargeeya_bala,
        'pushkara': pushkara,
        'chara_dasha': chara_dasha,
        'dst_info': dst_info,
        # 没算出来的附加项及原因（空字典＝全部算出）
        'calc_errors': calc_errors,
        # 溯源：以后改了 engine，看这三项就知道旧产物是哪一版、哪个瞬间、用什么岁差算的
        'calc_meta': {
            'engine_version': ENGINE_VERSION,
            'instant_utc': _instant.astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'ayanamsa': ayanamsa,
        },
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
