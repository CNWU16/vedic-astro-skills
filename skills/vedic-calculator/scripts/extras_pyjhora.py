"""
extras_pyjhora.py - PyJHora 额外功能封装
包含: Bhava Bala, Special Lagnas, Vimsopaka/Vargeeya Bala
"""


def _setup():
    """Common setup for PyJHora"""
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
    drik.set_ayanamsa_mode('TRUE_CITRA')
    const._DEFAULT_AYANAMSA_MODE = 'TRUE_CITRA'
    const._use_true_nodes_for_rahu_ketu = False
    
    return swe, const, drik


def calculate_bhava_bala(year, month, day, hour, minute, lat, lon, tz_offset, second=0):
    """
    使用 PyJHora 计算 Bhava Bala (宫位力量)。
    
    Returns:
        dict: house_num (1-12) -> {
            'total': float (shashtiamshas),
            'adhipathi': float,
            'dig': float, 
            'drik': float,
        }
    """
    swe, const, drik = _setup()
    from jhora.panchanga.drik import Place
    from jhora.horoscope.chart import strength
    
    local_hour = hour + minute / 60.0 + second / 3600.0
    jd_local = swe.julday(year, month, day, local_hour)
    place = Place('birth_place', lat, lon, tz_offset)
    
    try:
        bb = strength.bhava_bala(jd_local, place)
        # bb returns list of 12 values (one per house)
        result = {}
        if isinstance(bb, (list, tuple)):
            # May be a list of totals or a tuple of sub-lists
            if isinstance(bb[0], (list, tuple)):
                # Multiple components: (adhipathi, dig, drik, total) or similar
                for h in range(12):
                    result[h + 1] = {
                        'total': round(bb[-1][h], 2) if len(bb) > 3 else round(sum(b[h] for b in bb), 2),
                    }
                    for i, name in enumerate(['component_' + str(i) for i in range(len(bb))]):
                        result[h + 1][name] = round(bb[i][h], 2)
            else:
                for h in range(12):
                    result[h + 1] = {'total': round(bb[h], 2)}
        return result
    except Exception as e:
        return {'error': str(e)}


def calculate_pushkara(year, month, day, hour, minute, lat, lon, tz_offset, second=0):
    """
    计算 Pushkara Navamsa / Pushkara Bhaga（落陷补丁维度，S3-07）。
    行星落在 Pushkara Navamsa 区段 = 受滋养保护，受损行星有恢复力缓冲。

    Returns:
        dict: {'pushkara_navamsa': ['Mars', ...], 'pushkara_bhaga': ['Venus', ...]}
        失败时 {'error': str}
    """
    swe, const, drik = _setup()
    from jhora.panchanga.drik import Place, Date
    from jhora.horoscope.chart import charts
    from jhora import utils

    _PLANETS = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter',
                'Venus', 'Saturn', 'Rahu', 'Ketu']
    try:
        jd = utils.julian_day_number(Date(year, month, day), (hour, minute, second))
        place = Place('birth_place', lat, lon, tz_offset)
        pp = charts.rasi_chart(jd, place)
        nav_idx, bhaga_idx = charts.planets_in_pushkara_navamsa_bhaga(pp)
        to_names = lambda idxs: [_PLANETS[i] for i in idxs
                                 if isinstance(i, int) and 0 <= i < len(_PLANETS)]
        return {'pushkara_navamsa': to_names(nav_idx),
                'pushkara_bhaga': to_names(bhaga_idx)}
    except Exception as e:
        return {'error': str(e)}


def calculate_special_lagnas(year, month, day, hour, minute, lat, lon, tz_offset, second=0):
    """
    计算特殊 Lagna: Hora Lagna, Ghati Lagna, Sree Lagna, Indu Lagna, 
    Pranapada Lagna, Bhava Lagna.
    
    Returns:
        dict: lagna_name -> {'sign': str, 'sign_idx': int, 'degree': float, 'longitude': float}
    """
    swe, const, drik = _setup()
    from jhora.panchanga.drik import Place
    
    SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
             'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    
    local_hour = hour + minute / 60.0 + second / 3600.0
    jd_local = swe.julday(year, month, day, local_hour)
    place = Place('birth_place', lat, lon, tz_offset)
    
    result = {}
    lagna_funcs = {
        'hora_lagna': drik.hora_lagna,
        'ghati_lagna': drik.ghati_lagna,
        'sree_lagna': drik.sree_lagna,
        'bhava_lagna': drik.bhava_lagna,
        'pranapada_lagna': drik.pranapada_lagna,
        'indu_lagna': drik.indu_lagna,
        'vighati_lagna': drik.vighati_lagna,
    }
    
    for name, func in lagna_funcs.items():
        try:
            raw = func(jd_local, place)
            # Return format: (sign_idx, degree_in_sign)
            if isinstance(raw, (list, tuple)) and len(raw) >= 2:
                sign_idx = int(raw[0]) % 12
                degree = float(raw[1])
            else:
                lon_val = float(raw)
                sign_idx = int(lon_val / 30) % 12
                degree = lon_val % 30
            
            result[name] = {
                'sign': SIGNS[sign_idx],
                'sign_idx': sign_idx,
                'degree': round(degree, 2),
                'longitude': round(sign_idx * 30 + degree, 4),
            }
        except Exception as e:
            result[name] = {'error': str(e)}
    
    return result


def calculate_vargeeya_bala(year, month, day, hour, minute, lat, lon, tz_offset, second=0):
    """
    计算 Pancha Vargeeya Bala 和 Dwadhasa Vargeeya Bala。
    
    Returns:
        dict: {
            'pancha_vargeeya': {planet: float, ...},
            'dwadhasa_vargeeya': {planet: float, ...},
        }
    """
    swe, const, drik = _setup()
    from jhora.panchanga.drik import Place
    from jhora.horoscope.chart import strength
    
    PLANETS = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
    
    local_hour = hour + minute / 60.0 + second / 3600.0
    jd_local = swe.julday(year, month, day, local_hour)
    place = Place('birth_place', lat, lon, tz_offset)
    
    result = {}
    
    try:
        pvb = strength.pancha_vargeeya_bala(jd_local, place)
        if isinstance(pvb, dict):
            result['pancha_vargeeya'] = {
                PLANETS[k]: round(v, 2) for k, v in pvb.items() if k < 7
            }
        elif isinstance(pvb, (list, tuple)):
            result['pancha_vargeeya'] = {
                PLANETS[i]: round(pvb[i], 2) for i in range(min(7, len(pvb)))
            }
    except Exception as e:
        result['pancha_vargeeya'] = {'error': str(e)}
    
    try:
        dvb = strength.dwadhasa_vargeeya_bala(jd_local, place)
        if isinstance(dvb, dict):
            result['dwadhasa_vargeeya'] = {
                PLANETS[k]: round(v, 2) for k, v in dvb.items() if k < 7
            }
        elif isinstance(dvb, (list, tuple)):
            result['dwadhasa_vargeeya'] = {
                PLANETS[i]: round(dvb[i], 2) for i in range(min(7, len(dvb)))
            }
    except Exception as e:
        result['dwadhasa_vargeeya'] = {'error': str(e)}
    
    return result
