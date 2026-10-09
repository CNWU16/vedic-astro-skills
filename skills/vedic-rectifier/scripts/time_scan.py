"""
Vedic Rectifier — Time Scanner (swisseph版)
=============================================
扫描出生时间±N分钟范围，输出每分钟的Lagna/D9/D10变化。
与 vedic-calculator engine.py 使用相同的天文引擎(swisseph)和Ayanamsa(True Chitra)，
确保 Lagna 度数和 D9/D10 边界完全一致。

用法:
  # 推荐：直接给本地出生时间，脚本按 --tz 自己换算 UTC（含跨零点的日期借位）
  python time_scan.py --local-date 1995-05-06 --local-time 02:30 --lat 31.23 --lon 121.47 --tz 8
  # 旧用法：调用方已换算好的 UTC
  python time_scan.py --date 2000-01-01 --time 10:30 --lat 28.61 --lon 77.21 --range 60 --tz 5.5

注意: --date/--time 是 UTC。手算时本地时:分小于时区偏移（中国即 08:00 前）要借位，
UTC 日期须退 1 天（例：本地 1995-05-06 02:30 UTC+8 → UTC 1995-05-05 18:30）。
手算出错会让整张表的 Lagna/D9/D10 系统性偏移，所以优先用 --local-date/--local-time。
表头同时打印 UTC 与换算回去的本地时间，供核对。

依赖: pip install pyswisseph
"""

import swisseph as swe
import argparse
import calendar
import sys
import os
from datetime import datetime, timedelta

# === 与 engine.py 一致的配置 ===
swe.set_sid_mode(swe.SIDM_TRUE_CITRA)
# 行星位置 flags，与 engine.PLANET_FLAGS / PyJHora drik.PLANET_FLAGS 同值(66386)。
# 此处内联而非 import engine，是为保住本文件"只依赖 pyswisseph"的独立可跑性；
# 改 engine 那个常量时必须同步改这里（Moon 的 Nakshatra 边界判定依赖同一基准）。
PLANET_FLAGS = (swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
                | swe.FLG_TRUEPOS | swe.FLG_NONUT | swe.FLG_NOGDEFL)

# === 复用 vedic-calculator 的精确 Vimsottari Dasha（两点法用；两 skill 目录平级）===
_HERE = os.path.dirname(os.path.abspath(__file__))
_CALC_SCRIPTS = os.path.normpath(os.path.join(_HERE, '..', '..', 'vedic-calculator', 'scripts'))
if os.path.isfile(os.path.join(_CALC_SCRIPTS, 'dasha_pyjhora.py')):
    sys.path.insert(0, _CALC_SCRIPTS)
try:
    from dasha_pyjhora import calculate_dasha_fixed
    _HAS_DASHA = True
    _DASHA_ERR = None
except Exception as _e:
    _HAS_DASHA = False
    _DASHA_ERR = str(_e)

SIGNS = ['Ar', 'Ta', 'Ge', 'Cn', 'Le', 'Vi', 'Li', 'Sc', 'Sg', 'Cp', 'Aq', 'Pi']
SIGNS_CN = ['白羊', '金牛', '双子', '巨蟹', '狮子', '处女', '天秤', '天蝎', '射手', '摩羯', '水瓶', '双鱼']

# 27 Nakshatra——Moon 跨界处 Vimsottari 大运起始主星跳变，段内 Dasha 不连续，必须在此切段
NAKSHATRAS = ['Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
              'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'P.Phalguni', 'U.Phalguni',
              'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha', 'Mula',
              'P.Ashadha', 'U.Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
              'P.Bhadra', 'U.Bhadra', 'Revati']


# === 核心计算函数（与 engine.py 完全一致） ===

def calc_sidereal_asc(jd, lat, lon):
    """
    计算恒星(sidereal)上升点度数。
    与 engine.py calc_lagna() 使用相同的 swe.houses_ex() 调用。
    
    参数:
        jd: Julian Day (UT)
        lat: 纬度
        lon: 经度
    返回: 恒星Lagna绝对度数 (0-360)
    """
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'W', swe.FLG_SIDEREAL)
    return ascmc[0]


def deg_to_sign(deg):
    """绝对度数 → (星座缩写, 星座中文, 度数在星座内)"""
    sign_idx = int(deg / 30) % 12
    deg_in_sign = deg % 30
    return SIGNS[sign_idx], SIGNS_CN[sign_idx], deg_in_sign


def calc_d9(asc_deg):
    """
    Lagna绝对度数 → D9(Navamsa)星座
    与 engine.py calc_navamsha() 完全一致。
    
    Navamsha规则：每个星座30°分为9等份(3°20')
    起点取决于元素：
      火象(Ar/Le/Sg) → 从Aries(0)开始
      土象(Ta/Vi/Cp) → 从Capricorn(9)开始
      风象(Ge/Li/Aq) → 从Libra(6)开始
      水象(Cn/Sc/Pi) → 从Cancer(3)开始
    """
    sign = int(asc_deg / 30) % 12
    deg_in_sign = asc_deg % 30
    nav_part = int(deg_in_sign / (30.0 / 9))  # 0-8

    element = sign % 4  # 0=火, 1=土, 2=风, 3=水
    start_signs = [0, 9, 6, 3]  # Ar, Cp, Li, Cn
    d9_sign = (start_signs[element] + nav_part) % 12
    return SIGNS[d9_sign], SIGNS_CN[d9_sign]


def calc_d10(asc_deg):
    """
    Lagna绝对度数 → D10(Dashamsha)星座
    与 engine.py calc_dashamsha() 完全一致。
    
    Dashamsha规则：每个星座30°分为10等份(3°)
    起点取决于奇偶：
      奇数星座(Ar/Ge/Le/Li/Sg/Aq) → 从本星座开始
      偶数星座(Ta/Cn/Vi/Sc/Cp/Pi) → 从本星座+9开始
    """
    sign = int(asc_deg / 30) % 12
    deg_in_sign = asc_deg % 30
    das_part = int(deg_in_sign / 3.0)  # 0-9
    if das_part > 9:
        das_part = 9

    is_odd = (sign % 2 == 0)  # Ar=0(奇), Ta=1(偶)...
    if is_odd:
        d10_sign = (sign + das_part) % 12
    else:
        d10_sign = (sign + das_part + 8) % 12
    return SIGNS[d10_sign], SIGNS_CN[d10_sign]


def scan(
    date_str,
    time_str,
    lat,
    lon,
    range_min=30,
    tz_offset=0.0,
    endpoint_start=None,
    endpoint_end=None,
    include_pd=False,
):
    """
    扫描时间范围，输出每分钟的Lagna/D9/D10/Moon-Nakshatra变化 + 段首/段末两点 Dasha。

    参数:
        date_str: "YYYY-MM-DD"
        time_str: "HH:MM" (UTC)
        lat, lon: 出生地纬度/经度
        range_min: 扫描范围（±分钟）
        tz_offset: 出生地时区偏移(小时,如中国=8)——两点法 Dasha 的 AD 边界日期须用本地时区表示，
                   才能和用户按本地日期报的事件对齐（UTC 表示会差最多1天=边界事件误判）
        endpoint_start/end: 只为一个已锁定候选段生成两端Dasha。不传时用全局扫描两端。
        include_pd: 有可靠月/日事件需要PD差异审计时才开启。粗扫默认只算MD/AD。

    返回: (results: list of dict, dasha_endpoints: dict)
    """
    parts = date_str.split('-')
    year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
    h, m = map(int, time_str.split(':'))

    ut_hour = h + m / 60.0
    base_jd = swe.julday(year, month, day, ut_hour)
    base_utc = datetime(year, month, day, h, m)

    results = []
    prev_sign = None
    prev_d9 = None
    prev_d10 = None
    prev_nak = None

    for delta in range(-range_min, range_min + 1):
        jd = base_jd + delta / 1440.0  # 1分钟 = 1/1440天

        asc_deg = calc_sidereal_asc(jd, lat, lon)
        sign, sign_cn, deg_in_sign = deg_to_sign(asc_deg)
        d9, d9_cn = calc_d9(asc_deg)
        d10, d10_cn = calc_d10(asc_deg)
        # Moon sidereal 黄经 → Nakshatra（用绝对 jd，无 tz 问题）
        moon_lon = swe.calc_ut(jd, swe.MOON, PLANET_FLAGS)[0][0]
        nak_idx = int(moon_lon / (360.0 / 27)) % 27
        moon_nak = NAKSHATRAS[nak_idx]

        markers = []
        if prev_sign and sign != prev_sign:
            markers.append(f"★ LAGNA换座→{sign_cn}")
        if prev_d9 and d9 != prev_d9:
            markers.append(f"◆ D9换座→{d9_cn}")
        if prev_d10 and d10 != prev_d10:
            markers.append(f"◇ D10换座→{d10_cn}")
        if prev_nak is not None and nak_idx != prev_nak:
            markers.append(f"⚠️Moon跨Nak→{moon_nak}【段内Dasha起始主星跳变，必须在此切段分别求交】")

        results.append({
            'delta': delta, 'asc_deg': asc_deg, 'sign': sign, 'sign_cn': sign_cn,
            'deg_in_sign': deg_in_sign, 'd9': d9, 'd9_cn': d9_cn,
            'd10': d10, 'd10_cn': d10_cn, 'moon_nak': moon_nak,
            'markers': ' '.join(markers),
        })

        prev_sign, prev_d9, prev_d10, prev_nak = sign, d9, d10, nak_idx

    # 两点法：段首/段末各算一次 Vimsottari Dasha。
    # 粗扫只需 MD/AD；有可靠月/日事件时才补 PD，避免候选分钟×729的嵌套读取。
    # 时间口径铁律：UTC → 本地(UTC+tz) 再传，tz_offset 照传 → AD 边界日期用本地时区，与用户本地事件对齐
    dasha_endpoints = {}
    if _HAS_DASHA:
        first_offset = -range_min if endpoint_start is None else endpoint_start
        last_offset = range_min if endpoint_end is None else endpoint_end
        labels_and_offsets = [
            ('段首(%+dmin)' % first_offset, first_offset),
            ('段末(%+dmin)' % last_offset, last_offset),
        ]
        for label, dmin in labels_and_offsets:
            utc_dt = base_utc + timedelta(minutes=dmin)
            local_dt = utc_dt + timedelta(hours=tz_offset)
            try:
                dasha_endpoints[label] = calculate_dasha_fixed(
                    local_dt.year, local_dt.month, local_dt.day,
                    local_dt.hour, local_dt.minute, lat, lon, tz_offset,
                    include_pd=include_pd)
            except Exception as e:
                dasha_endpoints[label] = [{'error': str(e)}]
    else:
        dasha_endpoints['_error'] = 'calculate_dasha_fixed 未能导入: %s' % _DASHA_ERR

    return results, dasha_endpoints


def local_to_utc(local_date, local_time, tz_offset):
    """本地出生时间 → UTC（"YYYY-MM-DD", "HH:MM"）。用 timedelta 换算，跨零点自动借位改日期。"""
    local_dt = datetime.strptime(f"{local_date} {local_time}", "%Y-%m-%d %H:%M")
    utc_dt = local_dt - timedelta(hours=tz_offset)
    return utc_dt.strftime("%Y-%m-%d"), utc_dt.strftime("%H:%M")


def _base_label(date_str, time_str, tz_offset):
    """表头基准：UTC 与换算回去的本地时间并列，调用方可肉眼核对日期有没有借错。"""
    label = f"{date_str} {time_str} UTC"
    if tz_offset is None:
        return label
    local_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M") + timedelta(hours=tz_offset)
    return f"{label}（= 本地 {local_dt.strftime('%Y-%m-%d %H:%M')}，UTC{tz_offset:+g}）"


def print_results(results, date_str, time_str, lat, lon, tz_offset=None):
    """格式化输出扫描结果"""
    print(f"# 时间扫描结果")
    print(f"# 基准: {_base_label(date_str, time_str, tz_offset)} | 坐标: ({lat}, {lon})")
    print(f"# 引擎: swisseph + True Chitra Ayanamsa (与calc engine一致)")
    print(f"# 范围: {results[0]['delta']:+d} ~ {results[-1]['delta']:+d} 分钟")
    print()
    print(f"{'偏移':>6} | {'Lagna度数':>10} | {'星座':>6} | {'座内度数':>8} | {'D9':>4} | {'D10':>4} | 标记")
    print("-" * 75)

    for r in results:
        marker_str = f"  {r['markers']}" if r['markers'] else ""
        is_base = " ← 原始" if r['delta'] == 0 else ""
        print(f"{r['delta']:+4d}min | {r['asc_deg']:8.2f}° | {r['sign']:>4}{r['sign_cn']} | {r['deg_in_sign']:6.2f}° | {r['d9']:>4} | {r['d10']:>4} |{marker_str}{is_base}")


def save_results(results, date_str, time_str, lat, lon, filepath, dasha_ep=None, event_dates=None,
                 tz_offset=None):
    """保存为Markdown表格（含两点法 Dasha——3c 段内定位的腿二数据源，必须落盘）"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# 时间扫描结果\n\n")
        f.write(f"> 基准: {_base_label(date_str, time_str, tz_offset)}\n")
        f.write(f"> 坐标: ({lat}, {lon})\n")
        f.write(f"> 引擎: swisseph + True Chitra Ayanamsa\n\n")
        f.write(f"| 偏移 | Lagna度数 | 星座 | D9 | D10 | 标记 |\n")
        f.write(f"|------|----------|------|-----|------|------|\n")

        for r in results:
            base = " ← 原始" if r['delta'] == 0 else ""
            marker = r['markers'] + base
            f.write(f"| {r['delta']:+4d}min | {r['asc_deg']:.2f}° | "
                    f"{r['sign']} {r['deg_in_sign']:.1f}° | "
                    f"{r['d9']} | {r['d10']} | {marker} |\n")

        # 两点法 Dasha 也落盘（3c 段内定位的腿二数据源；此前只 print 到 stdout、读存盘文件的 agent 拿不到 → 会退化成纯结构匹配）
        f.write("\n## 两点法 Dasha（段首 / 段末；AD 日期=本地时区）\n")
        f.write("> 对每个事件日期在段首/段末两条时间线各查落哪个 MD/AD → 反推所需段内出生子窗 → 各事件子窗取覆盖峰值(众数区)。\n")
        f.write("> ⚠️ 若上表有【Moon跨Nak】标记 → 该段 Dasha 起始主星跳变、两点不连续，须在跨点切段后分别用两点法。\n\n")
        if dasha_ep is None or '_error' in (dasha_ep or {}):
            err = (dasha_ep or {}).get('_error', '未传入两点法 Dasha')
            f.write("⚠️⚠️ **DASHA_UNAVAILABLE**：" + err + "\n")
            f.write("→ ❌ 禁在无两点法 Dasha 下进 3c 段内定位/定盘（会退化成纯结构=过拟合风险）；请修复 Dasha 依赖后重跑。\n")
        else:
            for label, dashas in dasha_ep.items():
                f.write(f"\n### {label}\n")
                f.write(_fmt_dasha(dashas) + "\n")

        if event_dates:
            f.write("\n## 事件日期 MD/AD/PD 差异审计\n")
            f.write("> 只用于事件时间归属与候选差异审计；不改写标准评分，不参与出生分钟夹逼。\n\n")
            f.write(_fmt_event_date_audit(dasha_ep or {}, event_dates) + "\n")

    print(f"\n已保存: {filepath}")


def _fmt_dasha(dashas):
    """格式化一条 Dasha 时间线：MD(起-止) + 当前MD的AD边界"""
    if not dashas or (isinstance(dashas, list) and dashas and isinstance(dashas[0], dict) and 'error' in dashas[0]):
        return "  [Dasha 计算失败: %s]" % (dashas[0].get('error') if dashas else '空')
    lines = []
    for d in dashas:
        cur = ' ←当前' if d.get('is_current') else ''
        lines.append(f"  {d['planet']:<8} {d['start']} ~ {d['end']}{cur}")
        if d.get('is_current'):
            for a in d.get('antardashas', []):
                lines.append(f"      └ AD {a['planet']:<8} 起 {a['start']}")
    return '\n'.join(lines)


def _parse_period_date(value):
    """解析 Dasha 边界日期；计算器的 AD/PD 使用 YYYY-MM-DD。"""
    return datetime.strptime(value[:10], '%Y-%m-%d').date()


def _event_probe_dates(value):
    """事件精确到日时只查该日；只到月时查月首+月末，防止隐藏月内PD边界。"""
    value = value.strip()
    if len(value) == 10:
        return [datetime.strptime(value, '%Y-%m-%d').date()]
    if len(value) == 7:
        year, month = map(int, value.split('-'))
        last = calendar.monthrange(year, month)[1]
        return [datetime(year, month, 1).date(), datetime(year, month, last).date()]
    raise ValueError(f'事件日期必须是 YYYY-MM-DD 或 YYYY-MM：{value}')


def _active_triplet(dashas, probe_date):
    """在原生 [start,end) PD 时间线中查找某日的 MD/AD/PD。"""
    for md in dashas or []:
        for ad in md.get('antardashas', []):
            for pd in ad.get('pratyantardashas', []):
                if _parse_period_date(pd['start']) <= probe_date < _parse_period_date(pd['end']):
                    return f"{md['planet']}/{ad['planet']}/{pd['planet']}"
    return '未找到（日期超出时间线或PD缺失）'


def _fmt_event_date_audit(dasha_ep, event_dates):
    if not dasha_ep or '_error' in dasha_ep:
        return '⚠️ PD_AUDIT_UNAVAILABLE：两点法 Dasha 不可用，禁止伪造PD归属。'
    labels = list(dasha_ep.keys())
    if len(labels) < 2:
        return '⚠️ PD_AUDIT_UNAVAILABLE：缺少段首/段末两条时间线。'
    rows = [
        '| 事件日期 | 段首MD/AD/PD | 段末MD/AD/PD | 稳定性 |',
        '|----------|----------------|----------------|--------|',
    ]
    for raw in event_dates:
        probes = _event_probe_dates(raw)
        endpoint_values = []
        for label in labels[:2]:
            values = [_active_triplet(dasha_ep[label], probe) for probe in probes]
            endpoint_values.append(values[0] if len(set(values)) == 1 else f"{values[0]} → {values[-1]}")
        stable = '整段一致' if endpoint_values[0] == endpoint_values[1] and '→' not in endpoint_values[0] else '边界敏感/候选有差'
        rows.append(f"| {raw} | {endpoint_values[0]} | {endpoint_values[1]} | {stable} |")
    return '\n'.join(rows)


def print_dasha_endpoints(dasha_ep, event_dates=None):
    """输出段首/段末两点 Dasha——两点法反推事件子窗的数据源"""
    print("\n## 两点法 Dasha（段首 / 段末；AD 日期=本地时区，与用户本地事件对齐）")
    print("   用法：对每个事件日期，在段首和段末两条时间线里各查它落哪个 MD/AD →")
    print("        反推该事件落进'正确 MD/AD'所需的段内出生子窗 → 各事件子窗取覆盖峰值(众数区)")
    print("   ⚠️ 若上方扫描出现【Moon跨Nak】标记 → 该段 Dasha 起始主星跳变，两点不连续，须在跨点切段后分别用两点法")
    if '_error' in dasha_ep:
        print("\n" + "=" * 60)
        print("⚠️⚠️⚠️ DASHA_UNAVAILABLE — 两点法 Dasha 不可用：" + dasha_ep['_error'])
        print("→ ❌ 腿二数据源缺失！禁在无两点法 Dasha 下进 3c 段内定位/定盘")
        print("   （否则退化成纯结构匹配=过拟合风险）；请修复 Dasha 依赖后重跑。")
        print("=" * 60)
        return
    for label, dashas in dasha_ep.items():
        print(f"\n### {label}")
        print(_fmt_dasha(dashas))
    if event_dates:
        print("\n## 事件日期 MD/AD/PD 差异审计")
        print(_fmt_event_date_audit(dasha_ep, event_dates))


def main():
    parser = argparse.ArgumentParser(description='Vedic Rectifier Time Scanner (swisseph)')
    parser.add_argument('--date', help='出生日期 YYYY-MM-DD (UTC)；与 --time 同传')
    parser.add_argument('--time', help='预估出生时间 HH:MM (UTC)；与 --date 同传')
    parser.add_argument('--local-date', help='本地出生日期 YYYY-MM-DD；与 --local-time 同传，脚本按 --tz 换算 UTC（推荐）')
    parser.add_argument('--local-time', help='本地预估出生时间 HH:MM；与 --local-date 同传')
    parser.add_argument('--lat', required=True, type=float, help='出生地纬度')
    parser.add_argument('--lon', required=True, type=float, help='出生地经度')
    parser.add_argument('--range', type=int, default=30, help='扫描范围±分钟 (默认30)')
    parser.add_argument('--tz', type=float, required=True,
                        help='出生地时区偏移(小时,中国=8)——两点法Dasha的AD日期本地对齐用')
    parser.add_argument('--event-date', action='append', default=[],
                        help='事件日期 YYYY-MM-DD 或 YYYY-MM；可重复。只做两点MD/AD/PD差异审计，不定位出生分钟')
    parser.add_argument('--endpoint-start', type=int,
                        help='已锁定候选段的起点偏移（分钟）；必须与 --endpoint-end 同传')
    parser.add_argument('--endpoint-end', type=int,
                        help='已锁定候选段的终点偏移（分钟）；必须与 --endpoint-start 同传')
    parser.add_argument('--save', type=str, help='保存结果到文件路径')

    args = parser.parse_args()
    has_utc = args.date is not None or args.time is not None
    has_local = args.local_date is not None or args.local_time is not None
    if has_utc == has_local:
        parser.error('二选一：--local-date/--local-time（本地，推荐）或 --date/--time（UTC）')
    if has_local:
        if args.local_date is None or args.local_time is None:
            parser.error('--local-date 与 --local-time 必须同时传入')
        try:
            args.date, args.time = local_to_utc(args.local_date, args.local_time, args.tz)
        except ValueError as exc:
            parser.error(f'本地时间格式不对：{exc}')
    elif args.date is None or args.time is None:
        parser.error('--date 与 --time 必须同时传入')
    if args.range < 1:
        parser.error('--range 必须至少为1分钟')
    for raw_event_date in args.event_date:
        try:
            _event_probe_dates(raw_event_date)
        except ValueError as exc:
            parser.error(str(exc))

    if (args.endpoint_start is None) != (args.endpoint_end is None):
        parser.error('--endpoint-start 与 --endpoint-end 必须同时传入')
    if args.endpoint_start is not None:
        if args.endpoint_start >= args.endpoint_end:
            parser.error('--endpoint-start 必须小于 --endpoint-end')
        if args.endpoint_start < -args.range or args.endpoint_end > args.range:
            parser.error('候选段两端必须位于 --range 扫描范围内')
    if args.event_date and args.endpoint_start is None:
        parser.error(
            '--event-date 只能在候选段锁定后使用；请同时传入 '
            '--endpoint-start 与 --endpoint-end'
        )

    results, dasha_ep = scan(
        args.date,
        args.time,
        args.lat,
        args.lon,
        args.range,
        args.tz,
        endpoint_start=args.endpoint_start,
        endpoint_end=args.endpoint_end,
        include_pd=bool(args.event_date),
    )
    print_results(results, args.date, args.time, args.lat, args.lon, args.tz)
    print_dasha_endpoints(dasha_ep, args.event_date)

    if args.save:
        save_results(results, args.date, args.time, args.lat, args.lon, args.save, dasha_ep, args.event_date,
                     tz_offset=args.tz)

    # 输出变化点摘要
    print("\n## 关键变化点（Lagna/D9/D10换座 + Moon跨Nak）")
    for r in results:
        if r['markers']:
            print(f"  {r['delta']:+4d}min: {r['markers']}")


if __name__ == '__main__':
    main()
