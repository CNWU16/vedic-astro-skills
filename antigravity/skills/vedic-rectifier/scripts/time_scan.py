"""
Vedic Rectifier — Time Scanner (swisseph版)
=============================================
扫描出生时间±N分钟范围，输出每分钟的Lagna/D9/D10变化。
与 vedic-calculator engine.py 使用相同的天文引擎(swisseph)和Ayanamsa(True Chitra)，
确保 Lagna 度数和 D9/D10 边界完全一致。

用法:
  python time_scan.py --date 2000-01-01 --time 10:30 --lat 28.61 --lon 77.21
  python time_scan.py --date 2000-01-01 --time 10:30 --lat 28.61 --lon 77.21 --range 60

注意: --time 参数为 UTC 时间。中国(UTC+8)需减8小时。

依赖: pip install pyswisseph
"""

import swisseph as swe
import argparse
import sys
import os
from datetime import datetime, timedelta

# === 与 engine.py 一致的配置 ===
swe.set_sid_mode(swe.SIDM_TRUE_CITRA)

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


def scan(date_str, time_str, lat, lon, range_min=30, tz_offset=0.0):
    """
    扫描时间范围，输出每分钟的Lagna/D9/D10/Moon-Nakshatra变化 + 段首/段末两点 Dasha。

    参数:
        date_str: "YYYY-MM-DD"
        time_str: "HH:MM" (UTC)
        lat, lon: 出生地纬度/经度
        range_min: 扫描范围（±分钟）
        tz_offset: 出生地时区偏移(小时,如中国=8)——两点法 Dasha 的 AD 边界日期须用本地时区表示，
                   才能和用户按本地日期报的事件对齐（UTC 表示会差最多1天=边界事件误判）

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
    prev_nak = None

    for delta in range(-range_min, range_min + 1):
        jd = base_jd + delta / 1440.0  # 1分钟 = 1/1440天

        asc_deg = calc_sidereal_asc(jd, lat, lon)
        sign, sign_cn, deg_in_sign = deg_to_sign(asc_deg)
        d9, d9_cn = calc_d9(asc_deg)
        d10, d10_cn = calc_d10(asc_deg)
        # Moon sidereal 黄经 → Nakshatra（用绝对 jd，无 tz 问题）
        moon_lon = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)[0][0]
        nak_idx = int(moon_lon / (360.0 / 27)) % 27
        moon_nak = NAKSHATRAS[nak_idx]

        markers = []
        if prev_sign and sign != prev_sign:
            markers.append(f"★ LAGNA换座→{sign_cn}")
        if prev_d9 and d9 != prev_d9:
            markers.append(f"◆ D9换座→{d9_cn}")
        if prev_nak is not None and nak_idx != prev_nak:
            markers.append(f"⚠️Moon跨Nak→{moon_nak}【段内Dasha起始主星跳变，必须在此切段分别求交】")

        results.append({
            'delta': delta, 'asc_deg': asc_deg, 'sign': sign, 'sign_cn': sign_cn,
            'deg_in_sign': deg_in_sign, 'd9': d9, 'd9_cn': d9_cn,
            'd10': d10, 'd10_cn': d10_cn, 'moon_nak': moon_nak,
            'markers': ' '.join(markers),
        })

        prev_sign, prev_d9, prev_nak = sign, d9, nak_idx

    # 两点法：段首/段末各算一次完整 Vimsottari Dasha
    # 时间口径铁律：UTC → 本地(UTC+tz) 再传，tz_offset 照传 → AD 边界日期用本地时区，与用户本地事件对齐
    dasha_endpoints = {}
    if _HAS_DASHA:
        for label, dmin in [('段首(-%dmin)' % range_min, -range_min),
                            ('段末(+%dmin)' % range_min, range_min)]:
            utc_dt = base_utc + timedelta(minutes=dmin)
            local_dt = utc_dt + timedelta(hours=tz_offset)
            try:
                dasha_endpoints[label] = calculate_dasha_fixed(
                    local_dt.year, local_dt.month, local_dt.day,
                    local_dt.hour, local_dt.minute, lat, lon, tz_offset)
            except Exception as e:
                dasha_endpoints[label] = [{'error': str(e)}]
    else:
        dasha_endpoints['_error'] = 'calculate_dasha_fixed 未能导入: %s' % _DASHA_ERR

    return results, dasha_endpoints


def print_results(results, date_str, time_str, lat, lon):
    """格式化输出扫描结果"""
    print(f"# 时间扫描结果")
    print(f"# 基准: {date_str} {time_str} UTC | 坐标: ({lat}, {lon})")
    print(f"# 引擎: swisseph + True Chitra Ayanamsa (与calc engine一致)")
    print(f"# 范围: {results[0]['delta']:+d} ~ {results[-1]['delta']:+d} 分钟")
    print()
    print(f"{'偏移':>6} | {'Lagna度数':>10} | {'星座':>6} | {'座内度数':>8} | {'D9':>4} | {'D10':>4} | 标记")
    print("-" * 75)

    for r in results:
        marker_str = f"  {r['markers']}" if r['markers'] else ""
        is_base = " ← 原始" if r['delta'] == 0 else ""
        print(f"{r['delta']:+4d}min | {r['asc_deg']:8.2f}° | {r['sign']:>4}{r['sign_cn']} | {r['deg_in_sign']:6.2f}° | {r['d9']:>4} | {r['d10']:>4} |{marker_str}{is_base}")


def save_results(results, date_str, time_str, lat, lon, filepath, dasha_ep=None):
    """保存为Markdown表格（含两点法 Dasha——3c 段内定位的硬腿数据源，必须落盘）"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# 时间扫描结果\n\n")
        f.write(f"> 基准: {date_str} {time_str} UTC\n")
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

        # 两点法 Dasha 也落盘（3c 段内定位的硬腿数据源；此前只 print 到 stdout、读存盘文件的 agent 拿不到 → 会退化成纯结构匹配）
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


def print_dasha_endpoints(dasha_ep):
    """输出段首/段末两点 Dasha——两点法反推事件子窗的数据源"""
    print("\n## 两点法 Dasha（段首 / 段末；AD 日期=本地时区，与用户本地事件对齐）")
    print("   用法：对每个事件日期，在段首和段末两条时间线里各查它落哪个 MD/AD →")
    print("        反推该事件落进'正确 MD/AD'所需的段内出生子窗 → 各事件子窗取覆盖峰值(众数区)")
    print("   ⚠️ 若上方扫描出现【Moon跨Nak】标记 → 该段 Dasha 起始主星跳变，两点不连续，须在跨点切段后分别用两点法")
    if '_error' in dasha_ep:
        print("\n" + "=" * 60)
        print("⚠️⚠️⚠️ DASHA_UNAVAILABLE — 两点法 Dasha 不可用：" + dasha_ep['_error'])
        print("→ ❌ 硬腿数据源缺失！禁在无两点法 Dasha 下进 3c 段内定位/定盘")
        print("   （否则退化成纯结构匹配=过拟合风险）；请修复 Dasha 依赖后重跑。")
        print("=" * 60)
        return
    for label, dashas in dasha_ep.items():
        print(f"\n### {label}")
        print(_fmt_dasha(dashas))


def main():
    parser = argparse.ArgumentParser(description='Vedic Rectifier Time Scanner (swisseph)')
    parser.add_argument('--date', required=True, help='出生日期 YYYY-MM-DD')
    parser.add_argument('--time', required=True, help='预估出生时间 HH:MM (UTC)')
    parser.add_argument('--lat', required=True, type=float, help='出生地纬度')
    parser.add_argument('--lon', required=True, type=float, help='出生地经度')
    parser.add_argument('--range', type=int, default=30, help='扫描范围±分钟 (默认30)')
    parser.add_argument('--tz', type=float, default=0.0, help='出生地时区偏移(小时,中国=8)——两点法Dasha的AD日期本地对齐用')
    parser.add_argument('--save', type=str, help='保存结果到文件路径')

    args = parser.parse_args()

    results, dasha_ep = scan(args.date, args.time, args.lat, args.lon, args.range, args.tz)
    print_results(results, args.date, args.time, args.lat, args.lon)
    print_dasha_endpoints(dasha_ep)

    if args.save:
        save_results(results, args.date, args.time, args.lat, args.lon, args.save, dasha_ep)

    # 输出变化点摘要
    print("\n## 关键变化点（Lagna/D9换座 + Moon跨Nak）")
    for r in results:
        if r['markers']:
            print(f"  {r['delta']:+4d}min: {r['markers']}")


if __name__ == '__main__':
    main()
