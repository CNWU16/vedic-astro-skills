"""Chara Dasha (K.N. Rao 变体) — 自研实现。

规则来源：JHora "Chara dasa of K.N.Rao" 双盘金标准对照钉死（2026-07-03，
同一出生数据 UT 1:30/2:30 两张盘共 24 个大运数据点 24/24 全中）：
  1. 起始 = Lagna 座；
  2. 方向 = 第9宫足性：奇足{Ar,Ta,Ge,Li,Sc,Sg}→顺行，偶足{Cn,Le,Vi,Cp,Aq,Pi}→逆行；
  3. 年数 = 从该座沿"该座自身足性方向"数到其宫主所在座，count−1；
     宫主在本座 = 12 年；
     双主座 Scorpio(Mars/Ketu)、Aquarius(Saturn/Rahu) 取二者中年数较大者；
  4. 年长 = 恒星太阳年（sidereal solar year ≈ 365.2564 天）。

注：PyJHora 的 KN_RAO duration 与 JHora 在 Sg/Aq/Pi 存在偏差（8/1/9 vs 7/2/8），
故弃用其年数函数；其 ascendant 亦与本系统 engine 存在口径差，本模块只接受
engine 计算的真值输入。v1 只输出 Mahadasha 级（双系统交叉验证足够）；
Antardasha 级待 JHora AD 金标准对照后再启用。
"""

SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

# 奇足(顺数)/偶足(逆数)分组
ODD_FOOTED = {0, 1, 2, 6, 7, 8}       # Ar Ta Ge Li Sc Sg
# 各座宫主（行星名与 engine 一致）；Sc/Aq 双主
SIGN_LORDS = {
    0: ['Mars'], 1: ['Venus'], 2: ['Mercury'], 3: ['Moon'],
    4: ['Sun'], 5: ['Mercury'], 6: ['Venus'], 7: ['Mars', 'Ketu'],
    8: ['Jupiter'], 9: ['Saturn'], 10: ['Saturn', 'Rahu'], 11: ['Jupiter'],
}
SIDEREAL_YEAR_DAYS = 365.256363


def _count(from_sign, to_sign, forward):
    """从 from 数到 to（含两端）的格数。"""
    if forward:
        return ((to_sign - from_sign) % 12) + 1
    return ((from_sign - to_sign) % 12) + 1


def _duration_years(sign, planet_signs):
    """单座年数（KN Rao）。planet_signs: {行星名: sign_idx}"""
    forward = sign in ODD_FOOTED
    years = []
    for lord in SIGN_LORDS[sign]:
        lord_sign = planet_signs[lord]
        if lord_sign == sign:
            years.append(12)
        else:
            years.append(_count(sign, lord_sign, forward) - 1)
    return max(years)


def calc_chara_dasha(lagna_sign_idx, planet_signs, birth_jd_ut):
    """KN Rao Chara Dasha 大运时间线（一个完整周期，12 座）。

    Args:
        lagna_sign_idx: engine 计算的 Lagna 星座索引（0=Aries）
        planet_signs: {行星名: 星座索引}，engine 真值（9 星含 Rahu/Ketu）
        birth_jd_ut: 出生时刻 UT 儒略日（engine to_jd 的产物）
    Returns:
        {'method': ..., 'direction': 'forward'/'reverse', 'mahadashas': [
            {'sign','start_jd','end_jd','years'} ...]}
    """
    ninth = (lagna_sign_idx + 8) % 12
    forward = ninth in ODD_FOOTED
    step = 1 if forward else -1

    seq = [(lagna_sign_idx + step * i) % 12 for i in range(12)]
    mds, jd = [], birth_jd_ut
    for s in seq:
        yrs = _duration_years(s, planet_signs)
        end = jd + yrs * SIDEREAL_YEAR_DAYS
        mds.append({'sign': SIGNS[s], 'sign_idx': s,
                    'start_jd': jd, 'end_jd': end, 'years': yrs})
        jd = end
    return {'method': 'Chara Dasha (K.N. Rao)',
            'direction': 'forward' if forward else 'reverse',
            'mahadashas': mds}


if __name__ == '__main__':
    # 金标准自测：JHora 双盘（1990-08-15 上海坐标）
    import swisseph as swe
    planet_signs_common = {'Sun': 3, 'Moon': 1, 'Mars': 0, 'Mercury': 4,
                           'Jupiter': 3, 'Venus': 3, 'Saturn': 8,
                           'Rahu': 9, 'Ketu': 3}
    # 盘A: UT 2:30 → Lagna Libra(6)；JHora: Li9 Sc8 Sg7 Cp1 Aq2 Pi8 Ar12 Ta2 Ge2 Cn2 Le1 Vi1
    # 盘B: UT 1:30 → Lagna Virgo(5)；JHora: Vi1 Li9 Sc8 Sg7 Cp1 Aq2 Pi8 Ar12 Ta2 Ge2 Cn2 Le1
    expects = {
        6: [('Libra',9),('Scorpio',8),('Sagittarius',7),('Capricorn',1),('Aquarius',2),
            ('Pisces',8),('Aries',12),('Taurus',2),('Gemini',2),('Cancer',2),('Leo',1),('Virgo',1)],
        5: [('Virgo',1),('Libra',9),('Scorpio',8),('Sagittarius',7),('Capricorn',1),('Aquarius',2),
            ('Pisces',8),('Aries',12),('Taurus',2),('Gemini',2),('Cancer',2),('Leo',1)],
    }
    jd = swe.julday(1990, 8, 15, 2.5)
    ok = 0
    for lagna, exp in expects.items():
        res = calc_chara_dasha(lagna, planet_signs_common, jd)
        got = [(m['sign'], m['years']) for m in res['mahadashas']]
        match = got == exp
        ok += match
        print(f"Lagna={SIGNS[lagna]} {res['direction']}: {'PASS 12/12' if match else 'FAIL'}")
        if not match:
            for g, e in zip(got, exp):
                print(' ', g, 'vs', e, '' if g == e else '<<<')
    print('金标准对照:', f'{ok}/2 盘通过')
