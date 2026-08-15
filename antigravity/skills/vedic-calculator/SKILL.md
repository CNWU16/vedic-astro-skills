---
name: vedic-calculator
description: "Calculate a complete Vedic/Jyotish natal chart directly from birth date, exact time, and place, producing the canonical structured_data.md for downstream analysis. Use for requests such as 'calculate my Vedic chart', 'cast my birth chart', 'generate a chart from my birth details'; Chinese triggers including '直接排盘', '计算星盘', '快速排盘', and '算一下'; or Japanese triggers including '出生図を作って', 'ホロスコープを計算して', and 'ヴェーダ占星術で出生図を出して'. Also use when vedic-reader has birth details but no chart file. / 吠陀占星排盘计算引擎。"
---

# vedic-calculator: 吠陀占星排盘引擎

## Language contract / 语言契约

- Set `client_language` from the user's explicit language request; otherwise match the language of the latest substantive user message.
- Use `client_language` for all chat replies, intake questions, confirmations, progress updates, user-visible warnings, reports, and Q&A. Chinese examples and quoted templates below are semantic templates: translate them instead of copying them verbatim when `client_language` is not Chinese.
- Keep canonical filenames, CLI flags, JSON keys, `structured_data.md` schema headings, technical codes, and Sanskrit/English identifiers unchanged. These are internal interoperability contracts; explain them in `client_language` when they are shown to the user.
- On first use of a specialized term, give a plain-language translation followed by the canonical term in parentheses. Never translate canonical identifiers inside calculations or evidence citations.
- If the user changes language mid-run, preserve the existing data and artifact lineage; switch client-facing language from that point onward unless the user explicitly asks to regenerate earlier artifacts.
- When `client_language` is Japanese, read `resources/ja-calculator.md` completely before the first Japanese client-facing message. Apply it only as a terminology, register, intake, and rendering layer; it never changes calculations, schemas, evidence, phases, or output requirements.

> 基于pysweph天文引擎 + dashaflow算法模块，直接从出生时间计算完整星盘数据。
> 输出格式完全兼容vedic-reader的structured_data.md，可直接交给vedic-core分析。

## 前置条件

- Python 3.8 ~ 3.13（pysweph 为 C 扩展，**3.14 暂不支持**）
- 依赖: pysweph, dashaflow, PyJHora==4.8.6, pytz

> ⚠️ **不要直接 `pip install -r requirements.txt`！** dashaflow 声明依赖已停更的 pyswisseph，会导致冲突。
> 请使用 `setup_env.py` 自动安装（见下方）。

### 环境自动检测

```
运行前检查依赖是否可用（按优先级）：

  1. 检查 <skill目录> 或工作目录下是否有已有 venv/：
     - <skill目录>/venv/
     - <工作目录>/vedic-calc-env/
     - <工作目录>/venv/
     找到 → 用其 Python 运行 → 尝试 import swisseph → 成功 → 直接使用

  2. 尝试当前 Python import swisseph：
     - 成功且 swe.version 不是 '0.0.0' → 直接使用
     - 失败或空壳 → 继续

  3. 自动创建 venv（运行 setup_env.py）：
     <合适的Python> <skill目录>/scripts/setup_env.py
     脚本会自动：检测 Python 版本 → 创建 venv → 按正确顺序安装 → 验证 SAV=337
```

> ⚠️ `<skill目录>` = vedic-calculator skill 的安装路径，AI 根据实际环境自动填写。
> ⚠️ 如果系统默认 Python 是 3.14，setup_env.py 会自动查找 3.12/3.13 来创建 venv。

### ⚠️ 首次使用必须先跑环境诊断

```
在新机器/新环境首次使用 vedic-calculator 前，必须先运行：

  python <skill目录>/scripts/check_env.py

该脚本会自动检查：
  ✅ venv 位置和 Python 版本
  ✅ 4个核心依赖（pysweph/dashaflow/PyJHora/pytz）
  ✅ swisseph 空壳检测
  ✅ 星历表文件
  ✅ 最小计算测试（SAV=337）

如果输出 🎉 → 直接使用它报告的 Python 路径
如果输出 ⚠️ → 按提示运行 setup_env.py 修复

注意：check_env.py 本身可以用任何 Python 版本运行（包括3.14），
它会自动找到正确的 venv Python 来做依赖检查。
```

## 使用流程

### Step 1: 收集出生信息

向用户收集：
```
- 出生日期 (YYYY-MM-DD)
- 出生时间 (HH:MM，24小时制)
- 出生地点 (城市名)
- 性别
- 感情状态（可选）
- 时间精度（精确到分钟 / ±15分钟 / ±1小时 / 不确定）
- 时间来源（出生证 / 家人记忆 / 大概回忆 / 未追问）
```

⚠️ 夏令时确认（出生日期落在当地夏令时期间时必做，如中国大陆 1986-1991 每年4月中~9月中）：
```
向用户输出一句确认（默认=墙上钟，绝大多数记录是当时钟表显示时间）：
"您出生时当地正实行夏令时。您提供的时间是当时钟表显示的时间吗？（通常是，直接回'是'即可）
 若家里记录的是未拨快的'标准时/北京时间'，请说明。"
→ 墙上钟（默认）→ 正常排盘（引擎 pytz 自动按夏令时换算 UTC，正确）
→ 用户声明标准时 → 用固定时区排盘（如中国用 'Etc/GMT-8' 替代 'Asia/Shanghai'——
   注意 Etc 时区符号反转，GMT-8 即 UTC+8），并在备注记录"用户声明标准时"
排盘后 structured_data 元信息会自动带"夏令时"标注行，供用户核对。
```

### Step 2: AI转换地理坐标

根据用户提供的城市名，AI直接填写：
- 纬度 (lat)
- 经度 (lon)  
- 时区字符串 (tz_str)

常用参考：
```
北京:     39.9042, 116.4074, "Asia/Shanghai"
上海:     31.2304, 121.4737, "Asia/Shanghai"
广州:     23.1291, 113.2644, "Asia/Shanghai"
成都:     30.5728, 104.0668, "Asia/Shanghai"
台北:     25.0330, 121.5654, "Asia/Taipei"
香港:     22.3193, 114.1694, "Asia/Hong_Kong"
新德里:   28.6139, 77.2090,  "Asia/Kolkata"
孟买:     19.0760, 72.8777,  "Asia/Kolkata"
```

> ⚠️ 中国全境使用 "Asia/Shanghai" (UTC+8)
> ⚠️ 印度全境使用 "Asia/Kolkata" (UTC+5:30)

### Step 3: 运行引擎

在工作目录下创建计算脚本并执行：

```python
import sys, os

# ⚠️ 动态路径：AI根据skill安装位置自动填写
# Antigravity 示例: C:\Users\用户名\.gemini\config\skills\vedic-calculator\scripts
# Claude Code 示例: ~/.claude/skills/vedic-calculator/scripts
SCRIPTS_DIR = r"<vedic-calculator skill 的 scripts 目录绝对路径>"
sys.path.insert(0, SCRIPTS_DIR)

from engine import calculate_full_chart
from transit import calc_transit
from formatter import format_structured_data

# 计算本命盘
chart = calculate_full_chart(
    year=YYYY, month=MM, day=DD, 
    hour=HH, minute=MM,
    lat=LAT, lon=LON, 
    tz_str="TIMEZONE",
    # 按“有效精度”传入：出生证分钟记录至少审计±1；家人明确记忆通常5；
    # ±15分钟报时传15。它审计输入稳定性，不改变报时本身。
    uncertainty_minutes=1
)

# 计算当前过运
transit = calc_transit(
    chart['lagna']['sign_idx'],
    chart['planets']['Moon']['sign_idx'],
    "TIMEZONE"
)

# 元信息
meta = {
    'dob': 'YYYY-MM-DD',
    'time': 'HH:MM',
    'place': '城市名',
    'lat': LAT, 'lon': LON,
    'time_precision': '精确到分钟',
    'time_source': '未追问'
}

# 用户信息
user_info = {
    'gender': '男/女',
    'relationship': '单身/恋爱中/已婚'
}

# 生成structured_data.md
md = format_structured_data(chart, transit, meta, user_info)
with open(r"WORKDIR\structured_data.md", 'w', encoding='utf-8') as f:
    f.write(md)

# ⚠️ 正确的 SAV 验证方式（不要自己猜 key！）
SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
sav_total = sum(chart['sav'].get(s, 0) for s in SIGNS)
print(f"✅ SAV total: {sav_total}")
assert sav_total == 337, f"SAV FAILED: {sav_total} != 337"
```

执行命令（AI 根据环境自动选择 Python）：
```
# 优先级：skill目录下的venv → 系统Python
# Windows:  <skill目录>\venv\Scripts\python.exe SCRIPT_PATH
# Linux/Mac: <skill目录>/venv/bin/python SCRIPT_PATH
# 都没有venv: python SCRIPT_PATH（需已全局安装依赖）
```

> ⚠️ **禁止自己手写 print 来读取 chart 数据！** 必须用 `formatter.py` 输出 structured_data.md。
> chart 的数据结构见下方「engine 返回数据结构」。

### Step 4: 校验输出

检查生成的structured_data.md：
1. SAV总计 = 337 ✅
2. 行星完整性 = 10颗 ✅
3. Ra-Ke差180° ✅
4. Lagna星座是否合理
5. Vimsottari = 9段MD、81段AD、729段PD，且每层 `[start,end)` 无缝连续 ✅
6. 分盘边界审计：读取`分盘可信度声明`，确认D1/D9/D10/D4/D5在有效精度
   区间内是“稳定”还是“边界敏感”。禁止因“出生证”或“直接计算”自动把全部
   分盘写成可信；二者分别表示记录来源和数学可复现性，不表示输入扰动下稳定。

分盘消费硬约束：
- `✅ 审计区间内稳定`：对应分盘可按当前Lagna正常使用；
- `⚠️ 边界敏感`：保留给定时刻的计算表，但分盘宫位、内部宫主和所有下游形态
  结论必须条件化或降级；
- 旧structured_data缺少边界审计：标“未验证”，不得补写成高可信；
- 出生证未写明记录的是啼哭、分娩、断脐还是事后录入时，时刻语义仍未知。

时间分辨率硬约束：
- 只读MD时，只输出背景趋势；
- 读到MD×AD时，最多输出阶段窗口；
- 用户要求月份或窄于AD的窗口时，必须读取MD×AD×PD；
- PD缺失或校验失败时停止月级判定，禁止用AD或365.25天近似制造月级精度。

### Step 4.5: 三级运渐进读取（不改canonical数据）

Calculator正常排盘仍必须一次性计算、校验并写入完整`9 MD + 81 AD + 729 PD`。
渐进读取优化的是下游模型上下文，不是删数据、少计算或改时间线。

下游reader/rectifier/core/core-pro/QA一律按三层消费：

1. **MD背景层**：先定人生大阶段；
2. **AD阶段层**：再定领域候选与事件阶段；
3. **PD微触发层**：只在用户要求月/日、实际输出窄于完整AD、
   或相邻AD/PD接力会改变结论时读取。

禁止默认把`structured_data.md`中729行PD整表送入模型上下文。使用确定性工具：

```bash
# 默认读盘：输出全部非PD数据与MD/AD，折叠729行PD
python <calculator>/scripts/dasha_query.py --file structured_data.md --overview

# 完整性校验：只输出校验结果，不展开PD
python <calculator>/scripts/dasha_query.py --file structured_data.md --check

# 月级下钻：只返回命中的PD与相邻上下文
python <calculator>/scripts/dasha_query.py --file structured_data.md --month 2023-06 --context 1

# 日级或自定义[start,end)窗口
python <calculator>/scripts/dasha_query.py --file structured_data.md --date 2023-06-15 --context 1
python <calculator>/scripts/dasha_query.py --file structured_data.md --start 2023-05-01 --end 2023-07-01 --context 1
```

候选比较时，先用同一方法完成所有候选的MD/AD矩阵，锁定**全部**仍需PD分辨的候选后再统一下钻。
禁止只给当前最喜欢的候选读PD，也禁止通读729行后反向挑一个最像答案的窗口。

### Step 5: 模式选择

structured_data.md 生成后，向用户输出：

```
✅ 排盘完成！所有数据已生成（行星/分盘/SAV/Dasha大运+小运+三级运/宫主表/尊贵度/过运…）

📊 Shadbala 精度说明：
   structured_data以calc为主数据源。
   Shadbala始终先写入calc基准值。如没有JHora PDF，直接采用calc。
   如有同一出生时间生成的JHora PDF，则逐行对照并展示PDF值；
   二者不一致时会明确提示"当前采用PDF"。其余PDF数据只用于交叉验证。

下一步：
  a) 直接进入验前事（推荐）
  b) 发送 JHora PDF 补充 Shadbala
```

排盘完成后不要把小火人资料导出插入上述正常 a/b 流程。先让用户按上面的流程继续，
只在消息最后补一句可选提示：“如果想把这张盘带到小火人里使用，可以再说‘整理一段可复制给小火人的资料’。”
用户明确提出“小火人资料”“可复制资料”“关系资料”或类似请求时，才进入导出分支；普通排盘用户不自动接收额外长资料。

- 用户选 a) 或说"直接分析"/"开始" → 触发 vedic-reader（精简模式：跳过提取，直接读 structured_data → 验前事）
- 用户发送 PDF → 核对出生信息一致性 → 从PDF文本层提取有效Shadbala
  → 与calc Shadbala逐行对照 → PDF存在的行展示PDF值，差异行标注并提示用户
  → PDF缺失行保留calc → 其余PDF数据仅交叉验证
  → 再触发reader验前事

- 用户明确请求小火人资料 → 保留已生成的 canonical `structured_data.md` 不变，运行
  `scripts/make_xiaohuo_person_card.py structured_data.md`，把 stdout 返回的一段
  `xiaohuo-person-v1` 纯文字直接发给用户；不要生成图片，不要求用户打开或理解文件，
  也不要把资料卡当作新的排盘结果。双人使用时，两个人分别排盘、分别生成一段个人资料，
  再在双人对话中标为 A/B 粘贴。导出包含明确的 `Lagna`、当前 MD/AD/PD 和带日期的
  慢行星过运快照；导出器不调用星历，也不把旧快照改成今天。若用户要求真实当日过运且
  源文件日期已过期，必须重新运行完整 Calc 后再导出，不得只重跑导出器或手改日期。


## engine 返回数据结构

> ⚠️ **必读！** 不要猜 key 名。以下是 `calculate_full_chart()` 返回的 dict 结构。

```python
chart = {
    # 基础天文
    'ayanamsa': 23.8982,           # float, True Chitra ayanamsa 度数（约23.9°，与Lahiri差<1′）
    'lagna': {
        'sign': 'Cancer',          # str, 英文星座名
        'sign_idx': 3,             # int, 0-indexed (Aries=0)
        'degree': 13.61,           # float, 绝对度数 (星座内)
        'deg_str': "13°36'",       # str, 格式化度分
        'longitude': 103.61,       # float, 黄道经度
        'nakshatra': {'name': 'Pushya', 'pada': 4, 'lord': 'Saturn'}
    },
    'planets': {
        'Sun': {
            'sign': 'Scorpio', 'sign_idx': 7,
            'degree': 25.41, 'deg_str': "25°24'",
            'longitude': 235.41,
            'house': 5,            # int, 1-indexed 从 Lagna 数
            'retrograde': False,
            'nakshatra': {'name': 'Jyeshtha', 'pada': 3, 'lord': 'Mercury'}
        },
        # ... Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu 同结构
    },

    # SAV — ⚠️ key 是英文星座名，不是 'by_sign'!
    'sav': {
        'Aries': 36, 'Taurus': 34, 'Gemini': 22, 'Cancer': 28,
        'Leo': 34, 'Virgo': 29, 'Libra': 29, 'Scorpio': 25,
        'Sagittarius': 32, 'Capricorn': 20, 'Aquarius': 26, 'Pisces': 22
    },
    'sav_by_house': {
        1: {'sign': 'Cancer', 'value': 28},  # 按宫位编号
        # ... 2-12 同结构
    },

    # BAV
    'bav': {
        'Sun': {'Aries': 6, 'Taurus': 5, ...},  # 12星座
        # ... Moon, Mars, Mercury, Jupiter, Venus, Saturn
    },

    # Shadbala — ⚠️ 用 strength_pct (不是 strength_ratio)!
    'shadbala': {
        'Sun': {
            'total_60ths': 288.6,  'total_rupas': 4.81,
            'sthana': 82.0, 'kaala': 55.0, 'dig': 6.7,
            'cheshta': 44.9, 'naisargika': 60.0, 'drik': 40.0,
            'strength_pct': 96.2,  # ⚠️ 百分比，直接用！
            'classification': '弱',
            'ishta_phala': 7.64,   # Ishta Phala
            'kashta_phala': 50.18  # Kashta Phala
        },
        # ... Moon, Mars, Mercury, Jupiter, Venus, Saturn 同结构
    },

    # Dasha
    'dashas': [
        {
            'planet': 'Jupiter', 'start': '1998-02', 'end': '2014-02',
            'years': 16, 'is_current': False,
            'antardashas': [
                {
                    'planet': 'Jupiter',
                    'start': '1998-02-11', 'end': '2000-04-01',
                    'start_time': '1998-02-11 12:34', 'end_time': '2000-04-01 08:20',
                    'is_current': False,
                    'pratyantardashas': [
                        {
                            'planet': 'Jupiter',
                            'start': '1998-02-11', 'end': '1998-05-26',
                            'start_time': '1998-02-11 12:34', 'end_time': '1998-05-26 04:15',
                            'is_current': False
                        },
                        # ... 每个AD共9个PD
                    ]
                },
                # ... 9个小运
            ]
        },
        # ... 共9段大运
    ],

    # 分盘 — (sign_name, sign_idx) tuple
    'd9':  {'Lagna': ('Scorpio', 7), 'Sun': ('Aquarius', 10), ...},
    'd10': {'Lagna': ('Cancer', 3),  'Sun': ('Pisces', 11), ...},
    'd4':  {'Lagna': ('Libra', 6),   'Sun': ('Leo', 4), ...},
    'd5':  {'Lagna': ('Pisces', 11), 'Sun': ('Scorpio', 7), ...},
    'vargottama': {'Sun': False, 'Moon': False, 'Rahu': True, ...},
    'divisional_charts': {'D2': ..., 'D3': ..., ...},  # 额外分盘

    # 预分析
    'karakas': {'7k': [...], '8k': [...], 'dk_7k': 'Saturn', 'dk_8k': 'Rahu', 'dk_note': '7K(主)=Saturn, 8K(参考)=Rahu'},
    'dignity': {'Sun': {'compound': 'great_friend', ...}, ...},
    'aspects': [{'p1':'Rahu','p2':'Ketu','type':'对冲(180°)','degree_diff':'180.0'}, ...],
    'house_lords': {1: {'lord':'Moon','domain':'自我','lord_house':8}, ...},
    'special_points': {'AL': {'sign':'Virgo','house':3}, 'UL': {'sign':'Pisces','house':9}},
    'combustion': {},
    'moon_phase': {'waxing': True, 'sun_moon_diff': 88.6},
}
```


## 输出规格

输出的structured_data.md包含以下数据板块（完全匹配data_contract.md）：

| 板块 | 内容 |
|------|------|
| 元信息 | 出生时间、地点、Ayanamsa、读盘方式 |
| 行星位置 | 10颗行星+Lagna，星座/宫位/度数/逆行 |
| Nakshatra | 全部行星的Nakshatra+Pada |
| Chara Karakas | 7K主表（KN Rao）+ 8K参考 |
| Shadbala | 7颗行星的Rupas/百分比/排名/强弱/Ishta/Kashta |
| SAV | 原始值(按星座) + 宫位映射(按宫位) |
| BAV | 7颗行星×12星座矩阵 |
| Vimsottari Dasha | 9段大运 + 81段Antardasha + 729段Pratyantardasha；当前MD/AD/PD |
| 特殊点位 | AL(Arudha Lagna) + UL(Upapada Lagna) |
| Compound Dignity | Panchadha Maitri（旺/入庙/陷直接确定） |
| Graha Drishti | 吠陀行星相位（宫位照射：星→7th 等；西占 orb 相位表已废弃删除） |
| 宫主表 | 12宫完整 |
| 分盘 | D9/D10/D4/D5 + Vargottama + 报时不确定区间边界审计 |
| 校验 | 12项自动校验 |
| 过运 | 慢行星过运 + Sade Sati + 双过运 |

## 技术规格

- Ayanamsa: **True Chitrapaksha (TRUE_CITRA)**（固定，不可更改；属Lahiri系，差<1′）
- Node模式: **Mean Node**
- 天文核心: pysweph (Swiss Ephemeris C binding)
- SAV/BAV: **PyJHora 原生** (ashtakavarga_pyjhora.py)
- Dasha: **PyJHora 原生 MD/AD/PD** (dasha_pyjhora.py)；区间统一按`[start,end)`，禁止自行近似补三级运
- Shadbala: **PyJHora + 9项修正** (shadbala_pyjhora.py)
- 分盘: **PyJHora 原生** (divisional_pyjhora.py) — 15张 D1~D60
- 分盘稳定性: 在调用方传入的`uncertainty_minutes`内逐分钟重算D1/D9/D10/D4/D5
  Lagna；数学正确性与输入稳定性分别报告
- Dignity: dashaflow + 旺/入庙/陷前置判断
- Chara Karakas: 7K（KN Rao）+ 8K参考
- 容错策略: **fail-fast**（缺依赖直接报错，不给错误结果）

## 与其他skill的关系

```
路径1（纯calc，推荐）：
  用户给出生信息 → vedic-calculator → structured_data.md → vedic-reader(验前事) → vedic-core

路径2（PDF + calc主数据）：
  用户给PDF → reader提取出生信息 → calculator生成canonical structured_data
  → PDF交叉验证（仅有效Shadbala可覆盖）→ reader(验前事) → core

路径3（兜底）：
  用户材料无法提供完整出生信息 → reader提取模式（标注降级）→ reader(验前事) → core
```

所有路径输出的 structured_data.md 格式完全一致，core 无需区分数据来源。
