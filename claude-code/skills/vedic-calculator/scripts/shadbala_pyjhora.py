"""
shadbala_pyjhora.py v4 - 逐项修正版
基于 JHora 桌面版子项拆分数据精确对标修正。

已识别的 3 大差异根因:
  1. Hora Bala: PyJHora 的 _hora_bala 给错了行星 → 需要修正 hora 计算
  2. Dig Bala: PyJHora 两个 method 都不对 → 需要自建 dig bala
  3. Paksha Bala: Moon 差 36.8 → PyJHora 公式可能有 bug

已确认精确的子项（无需修正）:
  - Naisargika Bala: 7/7 完美
  - Cheshta Bala: Mars~Saturn 5/5 完美 (<1%)
  - Tribhaga/Abda/Masa/Vaara/Ayana/Yuddha: 全部匹配
"""


def calculate_shadbala_fixed(year, month, day, hour, minute, lat, lon, tz_offset, second=0):
    import sys
    import os
    import datetime
    import swisseph as swe

    pyjhora_path = None
    try:
        import jhora as _jh
        pyjhora_path = os.path.dirname(os.path.dirname(_jh.__file__))
    except ImportError:
        import site
        for sp in site.getsitepackages():
            if os.path.exists(os.path.join(sp, 'jhora')):
                pyjhora_path = sp
                break
    if pyjhora_path is None:
        raise ImportError("jhora package not found")
    if pyjhora_path not in sys.path:
        sys.path.insert(0, pyjhora_path)
    swe.set_ephe_path(os.path.join(pyjhora_path, 'jhora', 'data', 'ephe'))

    for fn_name in ['calc_ut', 'calc']:
        orig = getattr(swe, fn_name)
        if not hasattr(orig, '_patched'):
            def make_patch(o):
                def p(jd, planet, flags=0):
                    r = o(jd, planet, flags=flags)
                    return (r[0], r[1]) if len(r) == 3 else r
                p._patched = True
                return p
            setattr(swe, fn_name, make_patch(orig))
    if hasattr(swe, 'houses_ex'):
        orig_he = swe.houses_ex
        if not hasattr(orig_he, '_patched'):
            def patch_he(*a, **kw):
                # (1) PyJHora drik.ascendant() 不传 hsys → pyswisseph 默认落到 Placidus，极圈内(|lat|>66°33')
                #     无解。补 b'W'(整宫制)：asc 值与宫制无关(实测 W/E/O/C/B 返回同一 asc)。
                # (2) 显式传 Placidus/Koch 的调用(Shadbala Dig Bala 的 bhaava_madhya)在极圈内同样无解：
                #     按 Swiss Ephemeris 文档的做法改用 Porphyry(swe_houses 遇此情形自己也改算 Porphyry 并报 ERR)。
                # (3) 恒星盘请求统一到 engine.calc_lagna 的 Lagna 基准(=桌面 JHora，2026-10-23 客户 JHora
                #     打印盘实证差 0.004″)：视位置回归宫位 − 与行星同口径的岁差(TRUEPOS|NONUT)。
                #     PyJHora 自带的 FLG_TRUEPOS 只改 houses_ex 内部岁差，与行星口径差约 9″。
                #     ARMC 与占位元素不减岁差，按与 FLG_SIDEREAL 原生结果比对识别后原样保留。
                if len(a) < 4 and 'hsys' not in kw:
                    a = a + (b'W',)
                jd, lat, lon = a[0], a[1], a[2]
                hsys = a[3] if len(a) > 3 else kw.get('hsys', b'W')
                flags = a[4] if len(a) > 4 else kw.get('flags', 0)
                def _he(hs, fl):
                    try:
                        r = orig_he(jd, lat, lon, hs, fl)
                    except swe.Error:
                        if hs not in (b'P', b'K'):
                            raise
                        r = orig_he(jd, lat, lon, b'O', fl)
                    return r[0], r[1]
                if not flags & swe.FLG_SIDEREAL:
                    return _he(hsys, flags)
                trop_c, trop_a = _he(hsys, 0)
                sid_c, sid_a = _he(hsys, swe.FLG_SIDEREAL)
                ay = swe.get_ayanamsa_ex_ut(jd, swe.FLG_TRUEPOS | swe.FLG_NONUT)[1]
                def _fix(trop, sid):
                    return tuple((t - ay) % 360 if abs((t - s + 180) % 360 - 180) > 1 else t
                                 for t, s in zip(trop, sid))
                return _fix(trop_c, sid_c), _fix(trop_a, sid_a)
            patch_he._patched = True
            swe.houses_ex = patch_he

    from jhora import const, utils
    from jhora.panchanga import drik
    from jhora.panchanga.drik import Place
    from jhora.horoscope.chart import strength, charts, house

    drik.set_ayanamsa_mode('TRUE_CITRA')
    const._DEFAULT_AYANAMSA_MODE = 'TRUE_CITRA'
    const._use_true_nodes_for_rahu_ketu = False

    local_hour = hour + minute / 60.0 + second / 3600.0
    jd = swe.julday(year, month, day, local_hour)
    place = Place('birth_place', lat, lon, tz_offset)

    planets_list = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']

    # ========== 1. STHANA BALA (修正: Saptavargaja 用 Hora Method 1) ==========
    # PyJHora 的 Saptavargaja 硬编码用 hora chart_method=2 (Traditional Parasara)
    # 但 JHora 的 Shadbala 实际用 method=1 (PVR/Parasara parivritti)
    # Uchcha/OjaYugma/Kendra/Drekkana 子项完美匹配，无需修改
    
    from jhora import utils as jhora_utils
    
    sv_factors = const.sapthavargaja_factors  # [1, 2, 3, 7, 9, 12, 30]
    pp_rasi = charts.rasi_chart(jd, place)[:const._pp_count_upto_ketu]
    pp_sv = {}
    for dcf in sv_factors:
        if dcf != 2:
            pp_sv[dcf] = charts.divisional_chart(jd, place, divisional_chart_factor=dcf)[:const._pp_count_upto_ketu]
        else:
            # Hora method=1 (PVR/parivritti) gives Sthana ALL MATCH
            # Note: JHora's HoraPreference=6 is for DISPLAY D2, not for Saptavargaja
            pp_sv[dcf] = charts.hora_chart(pp_rasi, chart_method=1)[:const._pp_count_upto_ketu]
    
    # Uchcha, OjaYugma, Kendra, Drekkana — use PyJHora (100% match)
    ub = strength._uchcha_bala(pp_sv[1])
    ob = strength._ojayugama_bala(pp_sv[1], pp_sv[9])
    kb = strength._kendra_bala(pp_sv[1])
    db = strength._dreshkon_bala(pp_sv[1])
    
    # Saptavargaja — rebuild with corrected D2
    h_to_p = jhora_utils.get_house_planet_list_from_planet_positions(pp_rasi)
    cr = house._get_compound_relationships_of_planets(h_to_p)
    sb_fac = {
        const._ADHISATHRU_GREATENEMY - 1: 1.875,
        const._SATHRU_ENEMY - 1: 3.75,
        const._SAMAM_NEUTRAL - 1: 7.5,
        const._MITHRA_FRIEND - 1: 15,
        const._ADHIMITRA_GREATFRIEND - 1: 22.5
    }
    
    svb_sum = [0.0] * 7
    mt_ranges = const.moola_trikona_range_of_planets  # {planet: (sign, start_deg, end_deg)}
    for dcf in sv_factors:
        for p_idx in range(7):
            pd = pp_sv[dcf][p_idx + 1]
            h = int(pd[1][0] if isinstance(pd[1], (list, tuple)) else pd[0])
            p_deg = pd[1][1] if isinstance(pd[1], (list, tuple)) else pd[1]
            owner = const._house_owners_list[h]
            
            # FIX: MoolaTrikona requires both sign match AND degree within range
            is_mt = False
            if dcf == 1 and p_idx in mt_ranges:
                mt_sign, mt_start, mt_end = mt_ranges[p_idx]
                if h == mt_sign and mt_start <= p_deg <= mt_end:
                    is_mt = True
            
            if is_mt:
                svb_sum[p_idx] += 45
            elif const.house_strengths_of_planets[p_idx][h] == const._OWNER_RULER:
                svb_sum[p_idx] += 30
            else:
                svb_sum[p_idx] += sb_fac[cr[p_idx][owner]]
    
    sthana = [round(ub[i] + svb_sum[i] + ob[i] + kb[i] + db[i], 2) for i in range(7)]

    # ========== 2. KAALA BALA (fix Hora Bala) ==========
    # Good sub-items: use PyJHora directly
    nath = strength._nathonnath_bala(jd, place)
    paksha_raw = strength._paksha_bala(jd, place)
    # FIX: Paksha Bala - PyJHora has TWO bugs:
    # Bug 1: abs(sun_long - moon_long) can exceed 180°, should use shortest arc
    # Bug 2: Moon formula (60-pb)*2 not always applied
    # Rewrite from scratch using BPHS formula
    pp_temp = drik.dhasavarga(jd, place, divisional_chart_factor=1)
    sun_l = pp_temp[const.SUN_ID][1][0] * 30 + pp_temp[const.SUN_ID][1][1]
    moon_l = pp_temp[const.MOON_ID][1][0] * 30 + pp_temp[const.MOON_ID][1][1]
    # Shortest arc between Sun and Moon (0-180°)
    raw_dist = abs(sun_l - moon_l) % 360
    if raw_dist > 180:
        raw_dist = 360 - raw_dist
    pb_base = round(raw_dist / 3.0, 2)  # 0-60 shashtiamshas
    # Mercury classification: conjunction + aspect check (JHora standard)
    # PyJHora's benefics_and_malefics() only checks conjunction (same sign).
    # But JHora also checks aspects: if Mercury is aspected by malefics, it becomes malefic.
    # Algorithm (PVR method=2, from BPHS Ch.3 Shloka 11):
    #   - Mercury is BENEFIC when alone/with benefics AND not aspected by malefics
    #   - Mercury is MALEFIC when conjunct OR aspected by malefics (Sun/Mars/Saturn/waning Moon)
    #   - Moon is malefic when Krishna paksha (tithi > 15)
    cht_benefics, cht_malefics = charts.benefics_and_malefics(jd, place, exclude_rahu_ketu=True)
    mercury_is_malefic = 3 in cht_malefics
    
    # Additional check: if Mercury is BENEFIC by conjunction, verify aspects
    if not mercury_is_malefic:
        me_sign = int(pp_rasi[4][1][0])
        # Check if any malefic (excluding Mercury) aspects Mercury's sign
        # Malefics for this check: Sun(0), Mars(2), Saturn(6), waning Moon(1 if malefic)
        aspect_malefics = {0, 2, 6}  # Sun, Mars, Saturn always
        if 1 in cht_malefics:
            aspect_malefics.add(1)  # Waning Moon
        
        mal_aspect_count = 0
        ben_aspect_count = 0
        for mal_idx in aspect_malefics:
            p_sign = int(pp_rasi[mal_idx + 1][1][0])
            # 7th aspect (all planets)
            if (p_sign + 6) % 12 == me_sign:
                mal_aspect_count += 1
            # Mars special: 4th and 8th
            if mal_idx == 2:
                if (p_sign + 3) % 12 == me_sign or (p_sign + 7) % 12 == me_sign:
                    mal_aspect_count += 1
            # Saturn special: 3rd and 10th
            if mal_idx == 6:
                if (p_sign + 2) % 12 == me_sign or (p_sign + 9) % 12 == me_sign:
                    mal_aspect_count += 1
        
        # Benefic aspects on Mercury (Jupiter 5th/9th, Venus 7th)
        for ben_idx in [4, 5]:  # Jupiter, Venus
            p_sign = int(pp_rasi[ben_idx + 1][1][0])
            if (p_sign + 6) % 12 == me_sign:
                ben_aspect_count += 1
            if ben_idx == 4:  # Jupiter 5th and 9th
                if (p_sign + 4) % 12 == me_sign or (p_sign + 8) % 12 == me_sign:
                    ben_aspect_count += 1
        
        # Mercury alone + aspected by more malefics than benefics → malefic
        if mal_aspect_count > ben_aspect_count:
            mercury_is_malefic = True
    
    benefic_planets = set(cht_benefics)
    malefic_planets = set(cht_malefics)
    if mercury_is_malefic and 3 in benefic_planets:
        benefic_planets.discard(3)
        malefic_planets.add(3)
    paksha = [0.0] * 7
    for i in range(7):
        if i == 1:  # Moon: always takes the LARGER of the two formulas
            paksha[i] = round(max(pb_base, 60.0 - pb_base) * 2, 2)
        elif i in benefic_planets:
            paksha[i] = pb_base
        else:  # malefic
            paksha[i] = round(60.0 - pb_base, 2)
    tri = strength._tribhaga_bala(jd, place)
    # FIX: Abda/Masa - PyJHora uses calendar date, but JHora uses sunrise-adjusted date
    # If birth is before sunrise, the astrological date is the PREVIOUS day
    # This shifts Ahargana by -1, which can change Abda lord and Masa lord
    _sunrise = drik.sunrise(jd, place)
    _birth_hour = local_hour
    _before_sunrise = _birth_hour < _sunrise[0]
    if _before_sunrise:
        # Use previous day's JD for Abda/Masa calculation
        _jd_adjusted = jd - 1.0
    else:
        _jd_adjusted = jd
    abda = strength._abdadhipathi(_jd_adjusted, place)
    masa = strength._masadhipathi(_jd_adjusted, place)
    vaara = strength._vaaradhipathi(jd, place)
    # FIX: Ayana Bala - PyJHora's declination_of_planets has mod 360 bug
    # In declination_of_planets: p_long = h*30 + long + ayanamsa (can exceed 360)
    # But North/South check at L16 uses p_long WITHOUT mod 360
    # When planet is near end of zodiac + ayanamsa, p_long > 360 → wrong hemisphere
    # Example: Mars sidereal 347.17 + ayan 23.71 = 370.88 → should be 10.88 (North)
    # Rewrite declination with proper mod 360
    _ayan_val = drik.get_ayanamsa_value(jd)
    pp_ayana = drik.dhasavarga(jd, place, divisional_chart_factor=1)[:7]
    _bd = [0, 362/60.0, 703/60.0, 1002/60.0, 1238/60.0, 1388/60.0, 1440/60.0]
    _bx = [i * 15 for i in const.SUN_TO_SATURN]
    fixed_decl = [0.0] * 7
    for _p, (_h, _long) in pp_ayana:
        p_long = (_h * 30 + _long + _ayan_val) % 360  # FIX: mod 360
        # Bhuja
        if p_long < 90: bhuja = p_long
        elif p_long < 180: bhuja = 180 - p_long
        elif p_long < 270: bhuja = p_long - 180
        else: bhuja = 360 - p_long
        # North/South sign (BPHS)
        if p_long < 180:  # Northern hemisphere
            ns = -1
            if _p in [const.SUN_ID, const.MARS_ID, const.JUPITER_ID, const.VENUS_ID]:
                ns = 1
        else:  # Southern hemisphere
            ns = -1
            if _p in [const.MOON_ID, const.SATURN_ID]:
                ns = 1
        if _p == const.MERCURY_ID: ns = 1
        fixed_decl[_p] = ns * utils.inverse_lagrange(_bd, _bx, round(bhuja, 2))
    ayana = [0.0] * 7
    for _p in const.SUN_TO_SATURN:
        ayana[_p] = round((24.0 + fixed_decl[_p]) * 1.25, 2)
        if _p == const.SUN_ID:
            ayana[_p] *= 2
    # FIX: Yuddha Bala - PyJHora doesn't check separation < 1°
    # It finds ANY closest pair and declares war, even at 16° separation
    # Rewrite with proper distance threshold
    pp_yuddha = drik.dhasavarga(jd, place, divisional_chart_factor=1)
    yuddha = [0.0] * 7
    # Only Mars-Saturn (indices 2-6) can have planetary war (not Sun/Moon)
    mars_to_sat = list(range(2, 7))
    min_sep = 999; war_pair = None
    for idx_a in range(len(mars_to_sat)):
        pa = mars_to_sat[idx_a]
        la = pp_yuddha[pa][1][0]*30 + pp_yuddha[pa][1][1]
        for idx_b in range(idx_a+1, len(mars_to_sat)):
            pb2 = mars_to_sat[idx_b]
            lb = pp_yuddha[pb2][1][0]*30 + pp_yuddha[pb2][1][1]
            sep = abs(la - lb) % 360
            if sep > 180: sep = 360 - sep
            if sep < min_sep:
                min_sep = sep; war_pair = (pa, pb2)
    # Only trigger war if separation < 1 degree
    if min_sep < 1.0 and war_pair:
        p_a, p_b = war_pair
        # Compute bala difference for yuddha
        sb_y = strength._sthana_bala(jd, place)
        dgb_y = strength._dig_bala(jd, place)
        nb_y = strength._nathonnath_bala(jd, place)
        pb_y = strength._paksha_bala(jd, place)
        tb_y = strength._tribhaga_bala(jd, place)
        hb_y = strength._hora_bala(jd, place)
        bala_a = sb_y[p_a]+dgb_y[p_a]+nb_y[p_a]+pb_y[p_a]+tb_y[p_a]+hb_y[p_a]
        bala_b = sb_y[p_b]+dgb_y[p_b]+nb_y[p_b]+pb_y[p_b]+tb_y[p_b]+hb_y[p_b]
        b_diff = abs(bala_a - bala_b)
        dia_diff = abs(const.planets_disc_diameters[p_a]-const.planets_disc_diameters[p_b])
        if dia_diff > 0:
            y_bala = round(b_diff / dia_diff, 2)
            yuddha[p_a] = y_bala; yuddha[p_b] = -y_bala

    # FIX: Hora Bala - 重建
    # JHora 使用 WeekdayDefinitionKaala=1 (日出制星期)
    # Hora 序列: Sun→Venus→Mercury→Moon→Saturn→Jupiter→Mars (按行星时序)
    hora_lords_order = [0, 5, 3, 1, 6, 4, 2]  # Sun=0, Venus=5, Mercury=3, Moon=1, Saturn=6, Jupiter=4, Mars=2
    
    # 获取日出时间
    try:
        sunrise_data = drik.sunrise(jd, place)
        if isinstance(sunrise_data, (list, tuple)):
            sunrise_hour = sunrise_data[0] if isinstance(sunrise_data[0], (int, float)) else local_hour - 6
        else:
            sunrise_hour = local_hour - 6
    except:
        sunrise_hour = 6.0  # fallback
    
    # 日出制星期 (WeekdayDefinitionKaala=1)
    # 如果出生在日出之前，算前一天的星期
    dt = datetime.date(year, month, day)
    py_weekday = dt.weekday()  # Mon=0...Sun=6
    jh_weekday = (py_weekday + 1) % 7  # Sun=0, Mon=1, ..., Sat=6
    if local_hour < sunrise_hour:
        jh_weekday = (jh_weekday - 1) % 7
    
    # 从日出算过了几个 hora
    hours_since_sunrise = local_hour - sunrise_hour
    if hours_since_sunrise < 0:
        hours_since_sunrise += 24
    hora_number = int(hours_since_sunrise)  # 0-based hora index
    
    # 每天第一个 hora 的主星 = 该日星期名对应的行星
    # Sun=0→Sun, Mon=1→Moon, Tue=2→Mars, Wed=3→Mercury, Thu=4→Jupiter, Fri=5→Venus, Sat=6→Saturn
    day_lord_index = jh_weekday  # 0=Sun,...,6=Saturn
    
    # 在 hora_lords_order 中找到日主的位置
    start_pos = hora_lords_order.index(day_lord_index)
    
    # 当前 hora 的主星
    current_hora_lord = hora_lords_order[(start_pos + hora_number) % 7]
    
    hora_fixed = [0.0] * 7
    hora_fixed[current_hora_lord] = 60.0

    kaala = [
        nath[i] + paksha[i] + tri[i] + abda[i] + masa[i] + vaara[i] +
        hora_fixed[i] + ayana[i] + yuddha[i]
        for i in range(7)
    ]

    # ========== 3. DIG BALA (修正：用精确 Lagna 度数) ==========
    # JHora 使用 equal house system 的精确 Lagna 度数作为基准
    # 零点 = Lagna度数 + powerless_house * 30°
    # 公式: dig_bala = angular_dist_to_zero_point / 3
    
    pp = charts.rasi_chart(jd, place)[:const._pp_count_upto_ketu]
    
    # Get exact lagna degree
    lagna_data = pp[0]
    if isinstance(lagna_data[1], (list, tuple)):
        lagna_full = lagna_data[1][0] * 30 + lagna_data[1][1]
    else:
        lagna_full = lagna_data[0] * 30 + lagna_data[1]
    
    # Zero-point (powerless point) for each planet, using exact lagna
    powerless_house = const.dig_bala_powerless_houses_of_planets  # [3, 9, 3, 6, 6, 9, 0]
    
    dig = [0.0] * 7
    for p_idx in range(7):
        p_data = pp[p_idx + 1]
        if isinstance(p_data[1], (list, tuple)):
            p_long = p_data[1][0] * 30 + p_data[1][1]
        else:
            p_long = p_data[0] * 30 + p_data[1]
        
        zero_point = (lagna_full + powerless_house[p_idx] * 30) % 360
        diff = abs(p_long - zero_point) % 360
        if diff > 180:
            diff = 360 - diff
        dig[p_idx] = round(diff / 3.0, 2)

    # ========== 4. CHESHTA BALA (修正: PyJHora 缺少 >180° 规范化) ==========
    # PyJHora bug: abs(seegrocha - ave_long) 可以超过 180°
    # 正确做法: cheshta_kendra 应该取最短弧 (0-180°)，否则 cb > 60
    # 重写 cheshta 计算，添加规范化
    pp_cheshta = drik.dhasavarga(jd, place, divisional_chart_factor=1)
    sun_mean = strength.get_planet_mean_longitude(jd, place, drik.planet_list[const._SUN])
    cheshta = [0.0] * 7  # Sun=0, Moon=0 (already in Kaala)
    for p in [const._MARS, const._MERCURY, const._JUPITER, const._VENUS, const._SATURN]:
        p_id = drik.planet_list[p]
        mean_long = strength.get_planet_mean_longitude_using_epoch_table(jd, place, p_id)
        seegrocha = sun_mean
        if p in [const._MERCURY, const._VENUS]:
            seegrocha = mean_long
            mean_long = sun_mean
        true_long = pp_cheshta[p_id][1][0] * 30 + pp_cheshta[p_id][1][1]
        ave_long = 0.5 * (true_long + mean_long)
        ck = abs(seegrocha - ave_long)
        # FIX: normalize to shortest arc (0-180°)
        if ck > 180:
            ck = 360 - ck
        cheshta[p_id] = round(ck / 3, 2)

    # ========== 5. NAISARGIKA BALA (PyJHora perfect) ==========
    naisargika = strength._naisargika_bala(jd, place)

    # ========== 6. DRIK BALA (修正: benefic/malefic 分类) ==========
    # JHora 的 Drik 使用不同于 chart-specific 的分类规则:
    #   Jupiter(4), Venus(5) = always benefic
    #   Sun(0), Mars(2), Saturn(6) = always malefic
    #   Moon(1) = benefic when shortest_arc > 90° (pb_base > 30)
    #   Mercury(3) = chart-specific (PyJHora method=2)
    # Verified: Chart1(pb=20.79<30)→Moon=M err=7.5, Chart2(pb=33.87>30)→Moon=B err=2.6
    import numpy as np
    pp_drik = charts.rasi_chart(jd, place)[:const._pp_count_upto_ketu]
    pp7_drik = pp_drik[1:-2]  # Sun to Saturn
    dk_raw = [[0] * 7 for _ in range(7)]
    for p1 in range(7):
        p1l = pp7_drik[p1][1][0] * 30 + pp7_drik[p1][1][1]
        for p2 in range(7):
            if p1 == p2: continue
            p2l = pp7_drik[p2][1][0] * 30 + pp7_drik[p2][1][1]
            angle = round((360.0 + p1l - p2l) % 360, 2)
            # FIX: Cap aspect at 60 (JHora setting: AspectValueMax=60.000000)
            dk_raw[p1][p2] = min(60, round(strength.__drik_bala_calc_1(angle, p2, p1), 2))
    dk_t = np.array(dk_raw).T.tolist()
    # Benefic/Malefic classification
    drik_benefics = [4, 5]  # Jupiter, Venus always
    drik_malefics = [0, 2, 6]  # Sun, Mars, Saturn always
    # Moon: benefic if pb_base > 30 (moon more than 90° from sun)
    if pb_base > 30:
        drik_benefics.append(1)
    else:
        drik_malefics.append(1)
    # Mercury: same rule as Paksha
    if mercury_is_malefic:
        drik_malefics.append(3)
    else:
        drik_benefics.append(3)
    dkp = [0.0] * 7; dkm = [0.0] * 7
    for row in range(7):
        for col in range(7):
            if row in drik_benefics:
                dkp[col] += dk_t[row][col]
            if row in drik_malefics:
                dkm[col] += dk_t[row][col]
    drik_b = [round((dkp[i] - dkm[i]) / 4, 2) for i in range(7)]

    # ========== TOTAL ==========
    totals = [
        sthana[i] + kaala[i] + dig[i] + cheshta[i] + naisargika[i] + drik_b[i]
        for i in range(7)
    ]
    # ========== ISHTA PHALA / KASHTA PHALA (BPHS standard) ==========
    # Ishta = sqrt(Uchcha_Bala * Cheshta_Bala)
    # Kashta = sqrt((60 - Uchcha_Bala) * (60 - Cheshta_Bala))
    # For Sun: cheshta = ayana_bala / 2 (ayana already ×2 for Sun in BPHS, undo for Ishta)
    # For Moon: cheshta = Moon's special value (paksha-derived, capped at 60)
    import math
    ayana_raw = strength._ayana_bala(jd, place)
    cheshta_for_ishta = list(cheshta)  # copy
    cheshta_for_ishta[0] = ayana_raw[0] / 2.0  # Sun: undo the ×2 applied in ayana_bala
    cheshta_for_ishta[1] = pb_base  # Moon: Cheshta Rashmi = pb_base (0-60)
    ishta = [0.0] * 7
    kashta = [0.0] * 7
    for i in range(7):
        u = ub[i]
        c = cheshta_for_ishta[i]
        ishta[i] = round(math.sqrt(abs(u * c)), 2)
        kashta[i] = round(math.sqrt(abs((60 - u) * (60 - c))), 2)

    bphs_required = const.shad_bala_factors  # [6.5, 6, 5, 7, 6.5, 5.5, 5]

    result = {}
    for i, name in enumerate(planets_list):
        total = round(totals[i], 2)
        rupas = round(total / 60.0, 2)
        pct = round(rupas / bphs_required[i] * 100, 1)
        if pct >= 150:
            classification = 'strong'
        elif pct >= 100:
            classification = 'medium'
        else:
            classification = 'weak'

        result[name] = {
            'total_60ths': total,
            'total_rupas': rupas,
            'sthana': round(sthana[i], 2),
            'kaala': round(kaala[i], 2),
            'dig': round(dig[i], 2),
            'cheshta': round(cheshta[i], 2),
            'naisargika': round(naisargika[i], 2),
            'drik': round(drik_b[i], 2),
            'strength_pct': pct,
            'classification': classification,
            'ishta_phala': round(ishta[i], 2),
            'kashta_phala': round(kashta[i], 2),
        }

    return result
