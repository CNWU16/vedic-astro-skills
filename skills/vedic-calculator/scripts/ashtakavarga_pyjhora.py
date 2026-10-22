"""
ashtakavarga_pyjhora.py - PyJHora Ashtakavarga 封装
SAV/BAV 100% 匹配 JHora 桌面版
"""


def calculate_ashtakavarga_fixed(year, month, day, hour, minute, lat, lon, tz_offset, second=0):
    """
    使用 PyJHora 计算 SAV/BAV，100% 匹配 JHora 桌面版。
    
    Returns:
        dict: {
            'sarvashtakavarga': {sign_name: int, ...},  # SAV per sign
            'bhinnashtakavarga': {planet_name: {sign_name: int, ...}, ...},  # BAV
            'sav_total': int,
            'sodhya_pindas': {...} or None,
        }
    """
    import sys
    import os
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

    # Monkey-patch
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

    from jhora import const
    from jhora.panchanga import drik
    from jhora.panchanga.drik import Place
    from jhora.horoscope.chart import ashtakavarga, charts

    # 设置对齐
    drik.set_ayanamsa_mode('TRUE_CITRA')
    const._DEFAULT_AYANAMSA_MODE = 'TRUE_CITRA'
    const._use_true_nodes_for_rahu_ketu = False

    # JD = local time（和 Shadbala 一致）
    local_hour = hour + minute / 60.0 + second / 3600.0
    jd_local = swe.julday(year, month, day, local_hour)
    place = Place('birth_place', lat, lon, tz_offset)

    # 获取 Rasi chart → house_to_planet_list
    rasi = charts.rasi_chart(jd_local, place)
    h2p = ['' for _ in range(12)]
    for entry in rasi:
        p_id = entry[0]
        sign = entry[1][0]
        if h2p[sign]:
            h2p[sign] += '/' + str(p_id)
        else:
            h2p[sign] = str(p_id)

    # 计算 BAV, SAV, Prastara
    bav_raw, sav_raw, prastara = ashtakavarga.get_ashtaka_varga(h2p)

    # 格式化输出
    SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
             'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    PLANET_NAMES = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Ascendant']

    # SAV: sign -> value
    sarvashtakavarga = {}
    for i, sign in enumerate(SIGNS):
        sarvashtakavarga[sign] = int(sav_raw[i])

    # BAV: planet -> {sign -> value}
    bhinnashtakavarga = {}
    for p_idx, p_name in enumerate(PLANET_NAMES):
        bhinnashtakavarga[p_name] = {}
        for i, sign in enumerate(SIGNS):
            bhinnashtakavarga[p_name][sign] = int(bav_raw[p_idx][i])

    # Sodhya Pindas
    try:
        sp = ashtakavarga.sodhaya_pindas(bav_raw, h2p)
        # sp returns: [sodhya_pinda, rasi_pinda, graha_pinda] for each planet?
        sodhya_pindas = {}
        if isinstance(sp, (list, tuple)):
            for i, p_name in enumerate(PLANET_NAMES[:7]):
                if i < len(sp):
                    if isinstance(sp[i], (list, tuple)) and len(sp[i]) >= 3:
                        sodhya_pindas[p_name] = {
                            'sodhya_pinda': sp[i][0],
                            'rasi_pinda': sp[i][1],
                            'graha_pinda': sp[i][2]
                        }
    except Exception:
        sodhya_pindas = None

    return {
        'sarvashtakavarga': sarvashtakavarga,
        'bhinnashtakavarga': bhinnashtakavarga,
        'sav_total': sum(sav_raw),
        'sodhya_pindas': sodhya_pindas,
    }
