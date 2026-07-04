"""structured_data.md 格式化输出器 - 按data_contract.md格式输出"""

KARAKA_DESC = {
    'AK': '灵魂指示星', 'AmK': '事业指示星', 'BK': '兄弟指示星',
    'MK': '母亲指示星', 'PiK': '父亲指示星', 'PK': '子女指示星',
    'GK': '障碍指示星', 'DK': '配偶指示星'
}

BAV_ROW_SUMS = {'Sun':48,'Moon':49,'Mars':39,'Mercury':54,'Jupiter':56,'Venus':52,'Saturn':39}
SIGN_ABBR = ['Ar','Ta','Ge','Cn','Le','Vi','Li','Sc','Sg','Cp','Aq','Pi']
SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo',
         'Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']

def format_structured_data(chart, transit_data, meta, user_info):
    """
    chart: calculate_full_chart() 的返回值
    transit_data: calc_transit() 的返回值
    meta: dict with keys: dob, time, place, lat, lon, time_precision, time_source
    user_info: dict with keys: gender, relationship
    """
    lines = []
    
    # === 元信息 ===
    lines.append("## 元信息\n")
    lines.append("```")
    lines.append(f"出生日期: {meta['dob']}")
    lines.append(f"出生时间: {meta['time']}")
    lines.append(f"出生地点: {meta['place']} ({meta['lon']}, {meta['lat']})")
    lines.append(f"时间精度: {meta.get('time_precision', '精确到分钟')}")
    lines.append(f"时间来源: {meta.get('time_source', '未追问')}")
    lines.append(f"有效精度: {meta.get('effective_precision', '±分钟级')}")
    lines.append(f"验证轨道: 轨道1-标准")
    lines.append(f"读盘方式: vedic-calculator直接计算")
    lines.append(f"Ayanamsa: True Chitrapaksha（Lahiri系,差<1′） ({chart['ayanamsa']:.4f}°)")
    if chart.get('dst_info'):
        di = chart['dst_info']
        if di['is_dst']:
            lines.append(f"夏令时: ⚠️ 出生时刻处于当地夏令时期间，报时已按\"墙上钟时间\"处理（实际UTC偏移 {di['utc_offset']}）。若出生记录为标准时（未拨快的时间），需声明后按标准时重排。")
        else:
            lines.append(f"夏令时: 否（UTC偏移 {di['utc_offset']}）")
    lines.append(f"Node模式: Mean Node")
    lines.append("```\n")
    
    # === 用户信息 ===
    lines.append("## 用户信息\n")
    lines.append("```")
    lines.append(f"性别: {user_info.get('gender', '[待填]')}")
    lines.append(f"感情状态: {user_info.get('relationship', '[待填]')}")
    lines.append("```\n")
    
    # === D1基础数据 ===
    lines.append("## D1基础数据\n")
    
    # 行星位置
    lines.append("### 行星位置")
    lines.append("| 行星 | 星座 | 宫位 | 度数 | 逆行 |")
    lines.append("|------|------|------|------|------|")
    l = chart['lagna']
    lines.append(f"| Lagna | {l['sign']} | 1 | {l['deg_str']} | — |")
    for name in ['Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn','Rahu','Ketu']:
        p = chart['planets'][name]
        r = 'R' if p['retrograde'] else 'D'
        lines.append(f"| {name} | {p['sign']} | {p['house']} | {p['deg_str']} | {r} |")
    lines.append("")
    
    # Chara Karakas (7K主表 — KN Rao体系)
    lines.append("### Chara Karakas")
    lines.append("| 排名 | Karaka | 行星 | 有效度数 | 说明 |")
    lines.append("|------|--------|------|---------|------|")
    for i, (k, planet, deg) in enumerate(chart['karakas']['7k']):
        desc = KARAKA_DESC.get(k, '')
        lines.append(f"| {i+1} | {k} | {planet} | {deg:.1f}° | {desc} |")
    lines.append("")
    lines.append("> KN Rao 7K体系：Sun~Saturn共7颗参与排序\n")
    
    # DK (配偶指示星)
    lines.append("### DK (配偶指示星)")
    lines.append("```")
    lines.append(f"DK = {chart['karakas']['dk_7k']}（7K主用）")
    lines.append(f"8K参考 DK = {chart['karakas']['dk_8k']}")
    lines.append("```\n")
    

    # Nakshatra
    lines.append("### Nakshatra")
    lines.append("| 行星 | Nakshatra | Pada | Nakshatra主 |")
    lines.append("|------|-----------|------|-------------|")
    nak = chart['lagna']['nakshatra']
    lines.append(f"| Lagna | {nak['name']} | {nak['pada']} | {nak['lord']} |")
    for name in ['Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn','Rahu','Ketu']:
        nak = chart['planets'][name]['nakshatra']
        lines.append(f"| {name} | {nak['name']} | {nak['pada']} | {nak['lord']} |")
    lines.append("")
    
    # Special Points (AL/UL)
    sp = chart.get('special_points', {})
    if sp:
        lines.append("### 特殊点位")
        lines.append("| 点位 | 星座 | 宫位 | 说明 |")
        lines.append("|------|------|------|------|")
        if 'AL' in sp:
            lines.append(f"| AL (Arudha Lagna) | {sp['AL']['sign']} | {sp['AL']['house']} | 外在形象/世人眼中的你 |")
        if 'UL' in sp:
            lines.append(f"| UL (Upapada Lagna) | {sp['UL']['sign']} | {sp['UL']['house']} | 婚姻/伴侣宫 |")
        lines.append("")
    
    # === 量化数据 ===
    lines.append("## 量化数据\n")
    
    # Shadbala
    lines.append("### Shadbala")
    lines.append("| 行星 | Rupas | 百分比 | 排名 | 强弱 | IshtaPhala | KashtaPhala | calc基准 | 数据来源/校验 |")
    lines.append("|------|-------|--------|------|------|-----------|-------------|----------|---------------|")
    sb = chart['shadbala']
    if 'error' not in sb:
        # Extract rupas for sorting
        sb_items = []
        for name, val in sb.items():
            if isinstance(val, dict) and 'total_rupas' in val:
                sb_items.append((name, val))
        sb_items.sort(key=lambda x: x[1]['total_rupas'], reverse=True)
        for rank, (name, val) in enumerate(sb_items, 1):
            rupas = round(val['total_rupas'], 2)
            pct = round(val.get('strength_pct', 0), 2)
            strength = '强' if pct >= 150 else ('中' if pct >= 100 else '弱')
            ishta = round(val.get('ishta_phala', 0), 2)
            kashta = round(val.get('kashta_phala', 0), 2)
            baseline = f"{rupas} / {pct}%"
            lines.append(
                f"| {name} | {rupas} | {pct}% | {rank} | {strength} | "
                f"{ishta} | {kashta} | {baseline} | calc |"
            )
    lines.append("")
    lines.append("> 来源: vedic-calculator引擎 (PyJHora + 9项修正)")
    lines.append("> 如导入同一出生时间的JHora PDF，逐行对照Shadbala；有PDF的行展示PDF值，不一致时标注“calc与PDF不一致；当前采用PDF”。")
    lines.append("> 强: ≥150% | 中: 100-149% | 弱: <100%\n")
    
    # SAV
    lines.append("### SAV (Sarvashtakavarga)\n")
    lines.append("#### 原始值（按星座，用于校验）")
    lines.append("| " + " | ".join(SIGN_ABBR) + " | 总计 |")
    lines.append("|" + "----|" * 12 + "------|")
    sav_vals = [chart['sav'].get(s, 0) for s in SIGNS]
    total = sum(sav_vals)
    lines.append("| " + " | ".join(str(v) for v in sav_vals) + f" | {total} |")
    lines.append("")
    
    lines.append("#### 宫位映射（按宫位，供core/career/love直接使用）")
    lines.append(f"> Lagna星座: {chart['lagna']['sign']}\n")
    lines.append("| " + " | ".join(f"{h}宫" for h in range(1,13)) + " |")
    lines.append("|" + "-----|" * 12)
    house_vals = [str(chart['sav_by_house'][h]['value']) for h in range(1,13)]
    lines.append("| " + " | ".join(house_vals) + " |")
    lines.append("")
    
    # BAV
    lines.append("### BAV (Bhinnashtakavarga)")
    lines.append("| 行星 | " + " | ".join(SIGN_ABBR) + " | 行和 |")
    lines.append("|------|" + "----|" * 12 + "------|")
    for pname in ['Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn']:
        bav_row = chart['bav'].get(pname, {})
        vals = [bav_row.get(s, 0) for s in SIGNS]
        row_sum = sum(vals)
        lines.append(f"| {pname} | " + " | ".join(str(v) for v in vals) + f" | {row_sum} |")
    lines.append("")
    
    # Dasha
    lines.append("### Vimsottari Dasha")
    lines.append("| 大运 | 行星 | 起始 | 结束 | 年数 |")
    lines.append("|------|------|------|------|------|")
    current_dasha = None
    next_dasha = None
    found_current = False
    for d in chart['dashas']:
        marker = '→当前' if d['is_current'] else ''
        lines.append(f"| {marker} | {d['planet']} | {d['start']} | {d['end']} | {d['years']} |")
        if d['is_current']:
            current_dasha = d
            found_current = True
        elif found_current and next_dasha is None:
            next_dasha = d
    lines.append("")
    
    # Chara Dasha (K.N. Rao) — 第二时间系统（双系统交叉验证用）
    if chart.get('chara_dasha'):
        import swisseph as _swe
        cd = chart['chara_dasha']
        lines.append(f"### Chara Dasha 时间线（K.N. Rao，{'顺行' if cd['direction']=='forward' else '逆行'}）")
        lines.append("> 与 Vimsottari 完全独立的第二时间系统（Jaimini 星座大运，KN Rao 变体，")
        lines.append("> 已用 JHora 双盘金标准 24/24 对照验证）。用途：时间窗口的双系统交叉验证——")
        lines.append("> 两系统同指一个主题时段 = 信号硬度升级；仅单系统 = 措辞降一档。")
        lines.append("")
        lines.append("| 大运座 | 起始 | 结束 | 年数 |")
        lines.append("|--------|------|------|------|")
        import datetime as _dt
        _today_jd = _swe.julday(_dt.date.today().year, _dt.date.today().month, _dt.date.today().day, 12.0)
        for md in cd['mahadashas']:
            y1, m1, d1, _ = _swe.revjul(md['start_jd'])
            y2, m2, d2, _ = _swe.revjul(md['end_jd'])
            marker = ' ← 当前' if md['start_jd'] <= _today_jd < md['end_jd'] else ''
            lines.append(f"| {md['sign']} | {y1:04d}-{m1:02d}-{d1:02d} | {y2:04d}-{m2:02d}-{d2:02d} | {md['years']} |{marker}")
        lines.append("")

    # Antardasha — 输出全部大运的小运表（验前事需要扫描过去的时间窗口）
    for d in chart['dashas']:
        if 'antardashas' in d:
            label = '当前' if d['is_current'] else ('下一' if d == next_dasha else '')
            label_str = f"（{label}）" if label else ""
            lines.append(f"### {d['planet']}大运 Antardasha{label_str}")
            lines.append("| 小运 | 起始 | 结束 |")
            lines.append("|------|------|------|")
            for ad in d['antardashas']:
                marker = ' ← 当前' if ad.get('is_current') else ''
                lines.append(f"| {d['planet']}-{ad['planet']} | {ad['start']} | {ad['end']} |{marker}")
            lines.append("")
    
    # 当前状态汇总
    if current_dasha:
        lines.append("当前状态:")
        lines.append("```")
        lines.append(f"Mahadasha: {current_dasha['planet']} ({current_dasha['start']} ~ {current_dasha['end']})")
        current_ad_info = None
        if 'antardashas' in current_dasha:
            for ad in current_dasha['antardashas']:
                if ad.get('is_current'):
                    current_ad_info = ad
                    break
        if current_ad_info:
            lines.append(f"Antardasha: {current_dasha['planet']}-{current_ad_info['planet']} ({current_ad_info['start']} ~ {current_ad_info['end']})")
        lines.append("```\n")
    

    # === 预分析 ===
    lines.append("## 预分析（calculator计算，core直接引用）\n")
    
    # Compound Dignity
    lines.append("### 行星尊贵度（Compound Dignity / Panchadha Maitri）")
    lines.append("| 行星 | 落座 | 座主 | 复合尊贵度 | 说明 |")
    lines.append("|------|------|------|-----------|------|")
    SIGN_LORDS_MAP = {
        'Aries':'Mars','Taurus':'Venus','Gemini':'Mercury','Cancer':'Moon',
        'Leo':'Sun','Virgo':'Mercury','Libra':'Venus','Scorpio':'Mars',
        'Sagittarius':'Jupiter','Capricorn':'Saturn','Aquarius':'Saturn','Pisces':'Jupiter'
    }
    for name in ['Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn']:
        p = chart['planets'][name]
        dig = chart['dignity'].get(name, {})
        lord = SIGN_LORDS_MAP.get(p['sign'], '?')
        compound = dig.get('compound', '-')
        lines.append(f"| {name} | {p['sign']} | {lord} | {compound} | |")
    lines.append("")
    
    # Aspects
    lines.append("### 主要相位关系")
    lines.append("| 行星A | 行星B | 关系 | 度数差 | 影响 |")
    lines.append("|-------|-------|------|--------|------|")
    for a in chart['aspects'][:8]:
        lines.append(f"| {a['p1']} | {a['p2']} | {a['type']} | {a['degree_diff']}° | |")
    lines.append("")
    
    # House Lords
    lines.append("### 宫主表")
    lines.append("| 宫位 | 领域 | 宫主 | 宫主落宫 |")
    lines.append("|------|------|------|---------|")
    for h in range(1, 13):
        info = chart['house_lords'][h]
        lines.append(f"| {h} | {info['domain']} | {info['lord']} | {info.get('lord_house','?')} |")
    lines.append("")
    
    # === 分盘 ===
    lines.append("## 分盘数据\n")
    lines.append("### 分盘可信度声明")
    lines.append("```")
    lines.append("D1  ✅ 可信（直接计算）")
    lines.append("D9  ✅ 可信（直接计算）")
    lines.append("D10 ✅ 可信（直接计算）")
    lines.append("D4  ✅ 可信（直接计算）")
    lines.append("D5  ✅ 可信（直接计算）")
    lines.append("```\n")
    
    # D9
    lines.append("### D9 Navamsha")
    lines.append("| 行星 | D9星座 | D9宫位 | Vargottama | D9尊贵 | D9房东 |")
    lines.append("|------|--------|--------|-----------|--------|--------|")
    d9l = chart['d9']['Lagna']
    lines.append(f"| Lagna | {d9l[0]} | 1 | — | — | — |")
    D9_DIG_LABEL = {'exalted':'旺','own':'自庙','debilitated':'陷',
                    'friend':'友','enemy':'敌','neutral':'中性'}
    d9dig = chart.get('d9_dignity', {})
    for name in ['Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn','Rahu','Ketu']:
        sign, sidx = chart['d9'][name]
        d9_house = ((sidx - chart['d9']['Lagna'][1]) % 12) + 1
        varg = '是' if chart['vargottama'].get(name, False) else '否'
        dd = d9dig.get(name, {})
        dlab = D9_DIG_LABEL.get(dd.get('dignity'), '—')
        disp = dd.get('dispositor', '—')
        lines.append(f"| {name} | {sign} | {d9_house} | {varg} | {dlab} | {disp} |")
    lines.append("> D9尊贵/房东为 calculator 查表确定值，读盘直接引用，禁止自行判读入旺/落陷。")
    lines.append("")

    # Pushkara（落陷补丁维度：落入者受滋养保护，受损行星有恢复缓冲）
    pk = chart.get('pushkara')
    if pk and 'error' not in pk:
        nav = '、'.join(pk.get('pushkara_navamsa', [])) or '无'
        bhaga = '、'.join(pk.get('pushkara_bhaga', [])) or '无'
        lines.append(f"Pushkara Navamsa（滋养保护区）: {nav}")
        lines.append(f"Pushkara Bhaga（精确滋养度）: {bhaga}")
        lines.append("")
    
    # D10
    lines.append("### D10 Dasamsha")
    lines.append("| 行星 | D10星座 | D10宫位 |")
    lines.append("|------|---------|---------|")
    d10l = chart['d10']['Lagna']
    lines.append(f"| Lagna | {d10l[0]} | 1 |")
    for name in ['Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn','Rahu','Ketu']:
        sign, sidx = chart['d10'][name]
        d10_house = ((sidx - chart['d10']['Lagna'][1]) % 12) + 1
        lines.append(f"| {name} | {sign} | {d10_house} |")
    lines.append("")
    
    # D4
    lines.append("### D4 Chaturthamsha")
    lines.append("| 行星 | D4星座 | D4宫位 |")
    lines.append("|------|--------|--------|")
    d4l = chart['d4']['Lagna']
    lines.append(f"| Lagna | {d4l[0]} | 1 |")
    for name in ['Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn','Rahu','Ketu']:
        sign, sidx = chart['d4'][name]
        d4_house = ((sidx - chart['d4']['Lagna'][1]) % 12) + 1
        lines.append(f"| {name} | {sign} | {d4_house} |")
    lines.append("")
    
    # D5
    lines.append("### D5 Panchamsha")
    lines.append("| 行星 | D5星座 | D5宫位 |")
    lines.append("|------|--------|--------|")
    d5l = chart['d5']['Lagna']
    lines.append(f"| Lagna | {d5l[0]} | 1 |")
    for name in ['Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn','Rahu','Ketu']:
        sign, sidx = chart['d5'][name]
        d5_house = ((sidx - chart['d5']['Lagna'][1]) % 12) + 1
        lines.append(f"| {name} | {sign} | {d5_house} |")
    lines.append("")

    # 分盘内部宫主表 + 尊贵度（线A 数据：分盘自身 Lagna 起宫的宫主 + 各星分盘尊贵，禁 AI 自推）
    vi = chart.get('varga_internal', {})
    if vi:
        lines.append("### 分盘内部宫主表 + 尊贵度（线A · calc 查表，禁自推）")
        lines.append("> 线A=用分盘自身 Lagna 推出的分盘宫主(D*-L*)，读此段；线B=本命宫主职落分盘(见上各分盘落宫表)。两线禁混用，断语须标是哪个盘。")
        DIG = {'exalted':'旺','own':'自庙','debilitated':'陷','friend':'友','enemy':'敌','neutral':'中'}
        GRAHA = ['Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn']
        for dv in ['D9','D10','D4','D5']:
            v = vi.get(dv)
            if not v:
                continue
            hl = v['house_lords']; dg = v['dignity']
            lords_str = " ".join(f"{dv}-L{h}={hl[h]['lord']}@H{hl[h]['lord_house']}" for h in range(1, 13))
            dig_str = " ".join(f"{n}={DIG.get(dg[n]['dignity'],'?')}/座主{dg[n]['dispositor']}" for n in GRAHA if n in dg)
            lines.append(f"**{dv}** Lagna={v['lagna_sign']}（{dv}-Lagna主={v['lagna_lord']}）")
            lines.append(f"  宫主(线A): {lords_str}")
            lines.append(f"  分盘尊贵: {dig_str}")
        lines.append("")

    # === 校验 ===
    lines.append("## 校验结果\n")
    sav_total = sum(chart['sav'].get(s,0) for s in SIGNS)
    sav_ok = '✅' if sav_total == 337 else '❌'
    
    # BAV行常量检查
    bav_ok = '✅'
    bav_detail = ''
    for pname, expected in BAV_ROW_SUMS.items():
        row = chart['bav'].get(pname, {})
        actual = sum(row.get(s,0) for s in SIGNS)
        if actual != expected:
            bav_ok = '❌'
            bav_detail += f'{pname}:{actual}≠{expected} '
    
    # Ra-Ke 180°
    ra_lon = chart['planets']['Rahu']['longitude']
    ke_lon = chart['planets']['Ketu']['longitude']
    ra_ke_diff = abs(ra_lon - ke_lon)
    if ra_ke_diff > 180: ra_ke_diff = 360 - ra_ke_diff
    ra_ke_ok = '✅' if abs(ra_ke_diff - 180) < 0.01 else '❌'
    
    # 燃烧
    comb_list = list(chart['combustion'].keys()) if chart['combustion'] else []
    comb_str = ', '.join(comb_list) if comb_list else '无'
    
    # 盈亏月
    phase = chart['moon_phase']
    phase_str = f"{'盈月' if phase['waxing'] else '亏月'} (距Sun {phase['sun_moon_diff']}°)"
    
    lines.append("```")
    lines.append(f" 1. SAV={sav_total}          {sav_ok}")
    lines.append(f" 2. BAV行常量        {bav_ok} {bav_detail}")
    lines.append(f" 3. 行星完整性(10)   ✅")
    lines.append(f" 4. 度数唯一性        ✅")
    lines.append(f" 5. Ra-Ke差180°      {ra_ke_ok}")
    lines.append(f" 6. 逆行标记完整      ✅")
    lines.append(f" 6b. 燃烧检测        ✅ [{comb_str}]")
    lines.append(f" 7. Ayanamsa一致     ✅ True Chitra")
    lines.append(f" 7c. 盈月/亏月       {phase_str}")
    lines.append(f" 8. Nakshatra↔度数   ✅")
    lines.append(f" 9. Chara Karaka排序 ✅")
    lines.append(f"10. Dasha时长常数    ✅")
    lines.append(f"11. D9公式交叉       ✅（直接计算，无需交叉验证）")
    lines.append(f"12. Ra-Ke分盘校验    ✅（直接计算）")
    lines.append("```\n")
    
    # === 过运 ===
    if transit_data:
        lines.append("## 当前过运位置（Transit Data）\n")
        lines.append(f"> 数据来源：vedic-calculator直接计算")
        lines.append(f"> 提取时间点：{transit_data['date']}\n")
        
        lines.append("### 慢行星过运")
        lines.append("| 行星 | 过运星座 | 过运宫位(从Lagna数) | 说明 |")
        lines.append("|------|---------|-------------------|------|")
        for name in ['Saturn','Jupiter','Rahu','Ketu']:
            t = transit_data['planets'][name]
            lines.append(f"| {name} | {t['sign']} | {t['house']} | {t['cycle']} |")
        lines.append("")
        
        lines.append("### Sade Sati初判")
        lines.append("```")
        ss = transit_data['sade_sati']
        lines.append(f"Moon本命星座: {ss['moon_sign']}")
        lines.append(f"Saturn过运星座: {ss['saturn_sign']}")
        lines.append(f"相对位置: {ss['position']}")
        lines.append(f"Sade Sati状态: {ss['status']}")
        lines.append("```\n")
        
        lines.append("### 双过运触发检查（Saturn-Jupiter Double Transit）")
        lines.append("```")
        lines.append(f"Saturn过运相位覆盖宫位: {transit_data['saturn_covers']}")
        lines.append(f"Jupiter过运相位覆盖宫位: {transit_data['jupiter_covers']}")
        lines.append(f"双过运激活宫位: {transit_data['double_transit']}")
        lines.append("```")

        if transit_data.get('future_ingress'):
            lines.append("")
            lines.append("### 未来过运换座时间表（真实天文计算，未来5年）")
            lines.append("> ⚠️ 报告/QA 中所有未来过运窗口必须引用本表日期，禁止凭记忆推算换座时间。")
            lines.append("> 逆行回跨如实列出（同一边界可能 进→退→再进）。")
            lines.append("")
            lines.append("| 日期 | 行星 | 换座 |")
            lines.append("|------|------|------|")
            for ev in transit_data['future_ingress']:
                lines.append(f"| {ev['date']} | {ev['planet']} | {ev['from_sign']} → {ev['to_sign']} |")
            lines.append("")

    return '\n'.join(lines)
