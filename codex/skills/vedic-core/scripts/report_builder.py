"""
Vedic Report Builder — Universal MD → HTML Pipeline (v2)
=========================================================
Auto-detects open-source (vedic-core) vs Pro (vedic-core-pro) output files.
Dynamically numbers sections — no hardcoded "Part II" when Part I is missing.

Usage:
  python report_builder.py <folder> [--name "Name"] [--lagna "Cancer"] [--lang cn|en|ja]

Auto-detected file patterns:
  Identity:     p0_identity.md (Pro only)
  Planets:      p2a_planets.md ~ p2d_planets.md
  Divisional:   p3a_d9.md, p3b_divisional.md, p3c_yogas.md
  Houses:       p4a_houses.md, p4b_houses.md
  Prediction:   p5_prediction.md, p5c_topics.md (Pro only)
  Life:         p5a_life.md / p6a_life.md, p5b_life.md / p6b_life.md
  Blueprint:    p6c_blueprint.md (Pro only)
  Appendix:     appendix.md, rectification_report.md
  Career:       career_part1~3.md
  Love:         love_part1~2.md
  Q&A:          qa_*.md

Requirements:  pip install markdown
"""

import os
import sys
import re
import glob
import argparse

try:
    import markdown
except ImportError:
    print("Installing markdown...")
    os.system(f"{sys.executable} -m pip install markdown -q")
    import markdown

# ── CSS ──
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;600&family=Noto+Serif+JP:wght@400;500;600;700&family=Noto+Serif+SC:wght@400;500;600;700&family=Crimson+Pro:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap');

:root {
  --parchment: #f8f4ec; --parchment-deep: #f0eadb;
  --brown: #5a4636; --brown-light: #7a6652; --brown-muted: #9c8b7a;
  --gold: #b59540; --gold-soft: #d4c07a; --gold-line: #c9a94e;
  --text: #3d352c; --text-light: #5a4e42; --text-muted: #8a7d70;
  --border: #ddd3c2; --border-light: #e8e0d2;
  --table-head-bg: #ede6d8; --table-stripe: #f4efe5;
}
@page { size: A4; margin: 22mm 20mm 24mm 20mm; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, "Hiragino Kaku Gothic ProN", "Yu Gothic", "Noto Sans JP", "PingFang SC", "Microsoft YaHei", "Hiragino Sans GB", "Noto Sans SC", sans-serif;
  font-size: 14px; line-height: 1.85; color: var(--text);
  background: #e8e0d0;
  max-width: 780px; margin: 0 auto; padding: 48px 56px;
  background: var(--parchment);
  box-shadow: 0 1px 30px rgba(74,55,40,0.1);
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
}
@media print {
  body { background: var(--parchment); box-shadow: none; padding: 0; max-width: none; font-size: 10.5pt; }
  .no-print { display: none; }
  .section-header, thead th { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  table { font-size: 8pt !important; }
}

.cover {
  page-break-after: always; min-height: 100vh;
  display: flex; flex-direction: column; justify-content: center; align-items: center;
  position: relative; padding: 80px 20px 60px; text-align: center;
}
.cover-top {
  color: var(--gold); font-family: 'Inter', sans-serif;
  font-size: 10px; font-weight: 600;
  letter-spacing: 4px; text-transform: uppercase; margin-bottom: 40px;
}
.cover h1 {
  font-family: "Noto Serif JP", "Yu Mincho", "Hiragino Mincho ProN", "Noto Serif SC", "Songti SC", serif;
  font-size: 52px; font-weight: 700;
  color: var(--brown); line-height: 1.3; margin-bottom: 6px;
  border-bottom: none; padding-bottom: 0;
}
.cover .cover-accent {
  font-family: "Noto Serif JP", "Yu Mincho", "Noto Serif SC", serif;
  font-size: 28px; font-weight: 400; color: var(--gold);
  letter-spacing: 6px; margin-bottom: 12px;
}
.cover .cover-ornament {
  width: 60px; height: 1px; background: var(--gold-line); margin: 28px auto;
}
.cover .subtitle {
  font-size: 14px; color: var(--text-muted); font-weight: 400;
  letter-spacing: 1px; margin-bottom: 0;
}
.cover-meta {
  margin-top: auto; padding-top: 0; width: 100%; text-align: left;
  border-top: 1px solid var(--border-light); padding-top: 24px;
}
.cover-meta-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 6px 40px;
  font-size: 12px; color: var(--text-muted);
}
.cover-meta-grid div { display: flex; gap: 8px; align-items: baseline; padding: 4px 0; }
.cover-meta-grid dt { font-weight: 500; color: var(--brown-muted); font-size: 11px; min-width: 55px; flex-shrink: 0; }
.cover-meta-grid dd { margin: 0; color: var(--text-light); }

.toc { page-break-after: always; padding: 40px 0; }
.toc h2 {
  font-family: "Noto Serif JP", "Yu Mincho", "Noto Serif SC", serif; font-size: 22px; color: var(--brown);
  margin-bottom: 24px; padding-bottom: 10px; border-bottom: 1px solid var(--border);
  font-weight: 600;
}
.toc-list { list-style: none; }
.toc-list li {
  padding: 8px 0; border-bottom: 1px dashed var(--border-light);
  display: flex; justify-content: space-between; align-items: center;
  font-size: 14px;
}
.toc-section { font-weight: 500; color: var(--brown); }
.toc-list li.toc-part {
  background: var(--parchment-deep); color: var(--brown); padding: 10px 16px;
  margin: 4px -16px; border-radius: 3px; border: none; border-bottom: none;
  font-weight: 600; font-size: 14px;
}

.section { page-break-before: always; }
.section:first-of-type { page-break-before: auto; }
.section-header {
  border-left: 3px solid var(--gold-line);
  color: var(--brown); padding: 12px 22px; margin: 0 0 28px;
}
.section-header .section-number {
  color: var(--gold); font-family: 'Inter', sans-serif;
  font-size: 10px; font-weight: 600; letter-spacing: 3px; text-transform: uppercase;
}
.section-header h2 {
  font-family: "Noto Serif JP", "Yu Mincho", "Noto Serif SC", serif; font-size: 21px; font-weight: 700;
  margin-top: 2px; border: none; color: var(--brown) !important; padding-bottom: 0;
}

h1 {
  font-family: "Noto Serif JP", "Yu Mincho", "Noto Serif SC", "Crimson Pro", serif; font-size: 22px; color: var(--brown);
  margin: 32px 0 14px; font-weight: 600;
}
h2 {
  font-family: "Noto Serif JP", "Yu Mincho", "Noto Serif SC", "Crimson Pro", serif; font-size: 18px; color: var(--brown);
  margin: 28px 0 12px; font-weight: 600;
}
h3 {
  font-size: 15px; font-weight: 600; color: var(--brown);
  margin: 22px 0 8px; padding-left: 10px;
  border-left: 2px solid var(--gold-line);
}
h4 { font-size: 14px; font-weight: 600; color: var(--brown-light); margin: 16px 0 6px; }
p { margin: 0 0 12px; text-align: justify; }

table {
  width: 100%; border-collapse: collapse; margin: 10px 0 20px;
  font-size: 12px; line-height: 1.5;
}
thead th {
  background: var(--table-head-bg); color: var(--brown);
  padding: 7px 10px; text-align: left;
  font-weight: 600; font-size: 11px;
  border-bottom: 1.5px solid var(--gold-line);
}
tbody td { padding: 6px 10px; border-bottom: 1px solid var(--border-light); vertical-align: top; }
tbody tr:nth-child(even) { background: var(--table-stripe); }

table:has(th:nth-child(10)) { font-size: 10px; }
table:has(th:nth-child(10)) th,
table:has(th:nth-child(10)) td { padding: 4px 3px; text-align: center; white-space: nowrap; }
table:has(th:nth-child(10)) th:first-child,
table:has(th:nth-child(10)) td:first-child { text-align: left; font-weight: 600; }

blockquote {
  border-left: 2px solid var(--gold-line);
  background: var(--parchment-deep);
  padding: 10px 16px; margin: 14px 0; border-radius: 0 3px 3px 0;
  color: var(--text-light); font-size: 13px;
}
blockquote strong { color: var(--brown); font-style: normal; }

ul, ol { margin: 6px 0 14px 22px; }
li { margin-bottom: 3px; }

strong { color: var(--brown); }
code {
  background: var(--parchment-deep); padding: 1px 4px; border-radius: 2px;
  font-size: 12px; color: var(--brown-light);
  font-family: 'Inter', monospace;
}
pre {
  background: #3d352c; color: #ede6d8; padding: 14px 18px; border-radius: 4px;
  margin: 14px 0; font-size: 11px; line-height: 1.6; overflow-x: auto; white-space: pre-wrap;
}
pre code { background: transparent; border: none; color: inherit; padding: 0; }
hr { border: none; border-top: 1px dashed var(--border-light); margin: 24px 0; }

.page-break { page-break-before: always; }
.footer-note {
  margin-top: 30px; padding-top: 14px; border-top: 1px solid var(--border-light);
  font-size: 10px; color: var(--text-muted); text-align: center;
}
"""

# ── Section Registry ──
# Format: (priority, key, group, sub, cn_title, en_title, patterns)
#
# group: sections sharing the same group get the same "第X部分" number.
#   - "GN" groups → numbered as "第一部分", "第二部分"... dynamically
#   - "appendix" → titled "附录：XXX"
# sub: sub-label within group ("A"/"B"/"C"/"D"/"" for none)
#   - "cont" means continuation, shown as "（续）"
#
# Numbering is computed at build time based on which groups actually have files.
# This means: if p0_identity.md doesn't exist, planets become "第一部分" automatically.

SECTION_REGISTRY = [
    # ── Identity / Overview ──
    # Pro: p0_identity.md (身份定锚)
    # Open source: p1_overview.md (身份概览)
    (5,  "identity",    "G0", "",     "身份概览",                      "Identity Overview",
     ["p0_identity.md", "p1_overview.md"]),

    # ── Planets ──
    (15, "planets_a",   "G1", "A",   "行星审计（日/月）",              "Planets (Sun/Moon)",
     ["p2a_planets.md"]),
    (17, "planets_b",   "G1", "B",   "行星审计（火/水）",              "Planets (Mars/Mercury)",
     ["p2b_planets.md"]),
    (19, "planets_c",   "G1", "C",   "行星审计（木/金）",              "Planets (Jupiter/Venus)",
     ["p2c_planets.md"]),
    (21, "planets_d",   "G1", "D",   "行星审计（土/罗/计 + 总结）",    "Planets (Sa/Ra/Ke + Summary)",
     ["p2d_planets.md"]),
    (23, "planets",     "G1", "",    "行星审计（P1-P12）",             "Planetary Audit (P1-P12)",
     ["02_planets.md", "p2_planets.md", "planets.md"]),

    # ── Divisional / D9 / Yogas ──
    (28, "d9",          "G2", "A",   "D9盘深度审计",                   "D9 Navamsha Analysis",
     ["p3a_d9.md"]),
    (30, "divisional",  "G2", "B",   "分盘交叉分析",                   "Divisional Cross-Analysis",
     ["p3b_divisional.md", "p3_divisional.md", "03_d9.md"]),
    (32, "yogas",       "G2", "C",   "格局审计",                       "Yoga Audit",
     ["p3c_yogas.md"]),

    # ── Houses ──
    (38, "houses_a",    "G3", "A",   "宫位诊断（1-6宫）",             "House Diagnostics (1-6)",
     ["p4a_houses.md"]),
    (40, "houses_b",    "G3", "B",   "宫位诊断（7-12宫）",            "House Diagnostics (7-12)",
     ["p4b_houses.md"]),
    (42, "houses",      "G3", "",    "宫位诊断",                       "House Diagnostics",
     ["04_houses.md", "p4_houses.md", "houses.md"]),

    # ── Prediction (Pro only) ──
    (45, "prediction",  "G4", "",    "动态预测",                       "Dynamic Prediction",
     ["p5_prediction.md"]),
    (47, "topics",      "G4", "B",   "专题交叉审计",                   "Cross-Topic Audit",
     ["p5c_topics.md"]),

    # ── Life Architecture / Ten Themes ──
    (50, "life",        "G5", "",    "人生架构总结",                    "Life Architecture",
     ["p5a_life.md", "p6a_life.md", "05_life.md", "p5_life.md", "life.md"]),
    (55, "life2",       "G5", "cont","人生架构总结",                    "Life Architecture",
     ["p5b_life.md", "p6b_life.md", "05b_life.md", "life2.md"]),
    (57, "blueprint",   "G5", "",    "生命蓝图",                       "Life Blueprint",
     ["p6c_blueprint.md"]),

    # ── Appendix ──
    (58, "appendix",    "appendix", "",  "技术附录",                   "Technical Appendix",
     ["appendix.md"]),
    (59, "rectify",     "appendix", "",  "时间校准报告",               "Birth Time Rectification",
     ["rectification_report.md", "rectification_scan.md"]),

    # ── Career ──
    # SKILL outputs: career_phase12.md, career_phase3.md, career_phase4a/4b/4c.md
    # Legacy names: career_part1/2/3.md, career_phase1_2.md
    (60, "career1",     "G6", "",    "事业 — 画像与叙事",             "Career — Portrait & Narrative",
     ["career_part1.md", "career_phase12.md", "career_phase1_2.md"]),
    (65, "career2",     "G6", "cont","事业 — 战略决策",               "Career — Strategy",
     ["career_part2.md", "career_phase3.md"]),
    (67, "career3a",    "G6", "cont","事业 — 画像与叙事（精密合成）",  "Career — Precision Synthesis",
     ["career_phase4a.md"]),
    (68, "career3b",    "G6", "cont","事业 — 战略决策（终局）",       "Career — Final Strategy",
     ["career_part3.md", "career_phase4b.md", "career_phase4.md"]),
    (69, "career3c",    "G6", "cont","事业 — 风险与箴言",             "Career — Risk & Advice",
     ["career_phase4c.md"]),
    (70, "career",      "G6", "",    "事业架构",                       "Career Architecture",
     ["02_career.md", "06_career.md", "career.md"]),

    # ── Love ──
    # SKILL outputs: love_step1.md, love_step2.md, love_step3.md
    # Legacy names: love_part1/2.md
    (80, "love1",       "G7", "",    "感情 — 体质报告与配偶画像",     "Love — Pattern & Partner Profile",
     ["love_part1.md", "love_step1.md"]),
    (85, "love2",       "G7", "cont","感情 — 时间窗口",               "Love — Timing Windows",
     ["love_step2.md"]),
    (88, "love3",       "G7", "cont","感情 — 建议与风险",             "Love — Advice & Risk",
     ["love_part2.md", "love_step3.md"]),
    (90, "love",        "G7", "",    "感情与婚姻",                     "Love & Marriage",
     ["03_love.md", "07_love.md", "love.md"]),

    # ── Q&A (handled separately via glob) ──
    (100, "qa",         "appendix", "",  "追问答疑",                   "Q&A",
     []),
]

JA_SECTION_TITLES = {
    "identity": "出生図の中心テーマ",
    "planets_a": "惑星監査（太陽・月）",
    "planets_b": "惑星監査（火星・水星）",
    "planets_c": "惑星監査（木星・金星）",
    "planets_d": "惑星監査（土星・ラーフ・ケートゥ＋総括）",
    "planets": "惑星監査（P1-P12）",
    "d9": "ナヴァーンシャ（D9）の詳細監査",
    "divisional": "分割図のクロス分析",
    "yogas": "ヨーガ監査",
    "houses_a": "ハウス診断（第1～第6ハウス）",
    "houses_b": "ハウス診断（第7～第12ハウス）",
    "houses": "ハウス診断",
    "prediction": "運気の動的予測",
    "topics": "テーマ別クロス監査",
    "life": "人生全体の構造",
    "life2": "人生全体の構造",
    "blueprint": "人生設計図",
    "appendix": "技術付録",
    "rectify": "出生時刻修正レポート",
    "career1": "キャリア — 人物像と働き方",
    "career2": "キャリア — 戦略判断",
    "career3a": "キャリア — 精密な統合分析",
    "career3b": "キャリア — 最終戦略",
    "career3c": "キャリア — リスクと助言",
    "career": "キャリア構造",
    "love1": "恋愛 — 関係パターンと相手像",
    "love2": "恋愛 — 時期の窓",
    "love3": "恋愛 — 助言とリスク",
    "love": "恋愛と結婚",
    "qa": "質疑応答",
}

JA_GROUP_TITLES = {
    "G0": "出生図の中心テーマ",
    "G1": "惑星監査",
    "G2": "分割図分析",
    "G3": "ハウス診断",
    "G4": "運気の動的予測",
    "G5": "人生全体の構造",
    "G6": "キャリア分析",
    "G7": "恋愛分析",
    "appendix": "技術付録",
}


def localized_base_title(key, group, sub, cn_title, en_title, lang):
    """Return a client-facing title without changing artifact identities."""
    if lang == "cn":
        return cn_title
    if lang == "en":
        return en_title
    if key in JA_SECTION_TITLES:
        return JA_SECTION_TITLES[key]
    base = JA_GROUP_TITLES.get(group, en_title)
    return f"{base}（{sub}）" if sub and sub != "cont" else base


# ── Part numbering ──

CN_NUMS = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
           "十一", "十二", "十三", "十四", "十五"]

def cn_part_label(n):
    """第一部分, 第二部分, ..."""
    return f"第{CN_NUMS[n-1]}部分" if 1 <= n <= len(CN_NUMS) else f"第{n}部分"

EN_ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
            "XI", "XII", "XIII", "XIV", "XV"]

def en_part_label(n):
    """Part I, Part II, ..."""
    return f"Part {EN_ROMAN[n-1]}" if 1 <= n <= len(EN_ROMAN) else f"Part {n}"


def make_section_title(group, sub, base_title, part_num, lang):
    """Generate the display title for a section.

    Examples (cn):
      G1/A → "第一部分A：行星审计（日/月）"
      G1/cont → "第一部分（续）：行星审计"
      appendix → "附录：技术附录"
    """
    if group == "appendix":
        if lang == "cn":
            return f"附录：{base_title}"
        if lang == "ja":
            return f"付録：{base_title}"
        return f"Appendix: {base_title}"

    if lang == "cn":
        label = cn_part_label(part_num)
    elif lang == "ja":
        label = f"第{part_num}部"
    else:
        label = en_part_label(part_num)

    if sub == "cont":
        suffix = "（续）" if lang == "cn" else "（続き）" if lang == "ja" else " (cont.)"
        sep = "：" if lang in ("cn", "ja") else ": "
        return f"{label}{suffix}{sep}{base_title}"
    elif sub:
        sep = "：" if lang in ("cn", "ja") else ": "
        return f"{label}{sub}{sep}{base_title}"
    else:
        sep = "：" if lang in ("cn", "ja") else ": "
        return f"{label}{sep}{base_title}"


# ── File discovery ──

def find_files(folder):
    """Auto-detect MD files. Returns dict: key -> (priority, group, sub, cn_title, en_title, content)"""
    found = {}
    matched_files = set()

    # Pass 1: explicit pattern matches from registry
    for priority, key, group, sub, cn_title, en_title, patterns in SECTION_REGISTRY:
        if not patterns:
            continue
        for pat in patterns:
            path = os.path.join(folder, pat)
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    found[key] = (priority, group, sub, cn_title, en_title, f.read())
                matched_files.add(pat)
                print(f"  ✓ {pat} → {key}")
                break

    # Pass 2: dynamic scan for p*_*.md files not yet matched
    PREFIX_MAP = {
        "p0": ("G0", "身份定锚",         "Identity"),
        "p2": ("G1", "行星审计",          "Planetary Audit"),
        "p3": ("G2", "分盘分析",          "Divisional Analysis"),
        "p4": ("G3", "宫位诊断",          "House Diagnostics"),
        "p5": ("G5", "人生架构总结",      "Life Architecture"),
        "p6": ("G5", "人生架构总结",      "Life Architecture"),
    }

    all_md = sorted(glob.glob(os.path.join(folder, "p*_*.md")))
    for path in all_md:
        fname = os.path.basename(path)
        if fname in matched_files:
            continue
        m = re.match(r"(p\d)", fname)
        if not m:
            continue
        prefix = m.group(1)
        if prefix not in PREFIX_MAP:
            continue
        group, cn_base, en_base = PREFIX_MAP[prefix]
        # Extract sub-label: p2a → "A", p3c → "C"
        sub_m = re.match(r"p\d(\w?)_", fname)
        sub = sub_m.group(1).upper() if sub_m and sub_m.group(1) else ""
        key = f"dynamic_{fname}"
        # Compute priority: p2=20, p3=30, etc + sub offset
        base_pri = int(prefix[1]) * 10
        sub_offset = ord(sub) - 64 if sub else 0  # A=1, B=2...
        priority = base_pri + sub_offset

        with open(path, "r", encoding="utf-8") as f:
            sub_label = f"（{sub}）" if sub else ""
            found[key] = (priority, group, sub, f"{cn_base}{sub_label}", f"{en_base} ({sub})" if sub else en_base, f.read())
        print(f"  ✓ {fname} → {key} (dynamic)")

    # Pass 3: Q&A glob
    qa_files = sorted(glob.glob(os.path.join(folder, "qa_*.md")))
    if qa_files:
        combined = []
        for qf in qa_files:
            with open(qf, "r", encoding="utf-8") as f:
                combined.append(f"<!-- {os.path.basename(qf)} -->\n{f.read()}")
            print(f"  ✓ {os.path.basename(qf)} → qa")
        found["qa"] = (100, "appendix", "", "追问答疑", "Q&A", "\n\n---\n\n".join(combined))

    return found


def detect_package(found, lang="cn", brand=None):
    """Detect which skill packages are present."""
    has_core = any(v[1].startswith("G") for v in found.values() if v[1] in ("G0","G1","G2","G3","G4","G5"))
    has_career = any(v[1] == "G6" for v in found.values())
    has_love = any(v[1] == "G7" for v in found.values())
    has_qa = "qa" in found
    has_rectify = "rectify" in found

    # Detect version: --brand flag overrides auto-detect
    if brand == "pro":
        is_pro = True
    elif brand == "open":
        is_pro = False
    else:
        # 自动检测：只用 Pro 独有文件判定。
        # ❌ 不能用 "identity"——该 key 也映射开源版的 p1_overview.md，会把开源误判为 Pro。
        # ✅ prediction(p5_prediction.md) / blueprint(p6c_blueprint.md) 才是 Pro 专属。
        is_pro = "prediction" in found or "blueprint" in found
    if is_pro:
        version = "Pro"
    elif lang == "cn":
        version = "开源版"
    elif lang == "ja":
        version = "公開版"
    else:
        version = "Open Source"

    parts = []
    part_labels = {
        "cn": ("核心", "事业", "感情", "校准", "答疑"),
        "en": ("Core", "Career", "Love", "Rectification", "Q&A"),
        "ja": ("総合分析", "キャリア", "恋愛", "出生時刻修正", "質疑応答"),
    }[lang]
    if has_core:    parts.append(part_labels[0])
    if has_career:  parts.append(part_labels[1])
    if has_love:    parts.append(part_labels[2])
    if has_rectify: parts.append(part_labels[3])
    if has_qa:      parts.append(part_labels[4])

    pkg = " + ".join(parts)
    if lang == "cn":
        return pkg, f"{version} | {pkg} 完整报告", version
    if lang == "ja":
        return pkg, f"{version}｜{pkg} 総合鑑定レポート", version
    return pkg, f"{version} | {pkg} Complete Reading", version


# ── HTML builders ──

def build_cover(name, lagna, gender, status, pkg, desc, lang="cn"):
    top = {
        "cn": "数据驱动吠陀占星",
        "en": "DATA-DRIVEN VEDIC ASTROLOGY",
        "ja": "DATA-DRIVEN VEDIC ASTROLOGY",
    }[lang]
    title = {"cn": "吠陀占星", "en": "Vedic Astrology", "ja": "ヴェーダ占星術"}[lang]
    accent = {"cn": "完 整 解 读", "en": "Complete Reading", "ja": "総合鑑定"}[lang]
    L = {
        "cn": ["客户", "上升", "信息", "套餐", "体系", "软件", "大运", "量化"],
        "en": ["Client", "Lagna", "Profile", "Package", "System", "Software", "Dasha", "Metrics"],
        "ja": ["クライアント", "ラグナ", "基本情報", "レポート", "体系", "ソフトウェア", "ダシャー", "指標"],
    }[lang]
    return f"""
<div class="cover">
  <div class="cover-top">{top}</div>
  <h1>{title}</h1>
  <div class="cover-accent">{accent}</div>
  <div class="cover-ornament"></div>
  <div class="subtitle">{desc}</div>
  <div class="cover-meta"><div class="cover-meta-grid">
    <div><dt>{L[0]}</dt><dd>{name}</dd></div>
    <div><dt>{L[1]}</dt><dd>{lagna}</dd></div>
    <div><dt>{L[2]}</dt><dd>{gender} | {status}</dd></div>
    <div><dt>{L[3]}</dt><dd>{pkg}</dd></div>
    <div><dt>{L[4]}</dt><dd>Parashari Jyotish | KN Rao School</dd></div>
    <div><dt>{L[5]}</dt><dd>Jagannatha Hora v8.0 | True Chitrapaksha (Lahiri系, 差<1′)</dd></div>
    <div><dt>{L[6]}</dt><dd>Vimsottari (Mahadasha + Antardasha)</dd></div>
    <div><dt>{L[7]}</dt><dd>Shadbala, Ashtakavarga (SAV/BAV), D9 Navamsha</dd></div>
  </div></div>
</div>"""


def build_toc(sections, lang="cn"):
    toc_title = {"cn": "目录", "en": "Table of Contents", "ja": "目次"}[lang]
    items = []
    for title, _ in sections:
        items.append(f'<li class="toc-part">{title}</li>')
    return f'<div class="toc"><h2>{toc_title}</h2><ul class="toc-list">{"".join(items)}</ul></div>'


def _fix_table_spacing(text):
    """确保 markdown 表格前有空行，否则解析器会把它当普通文本。"""
    lines = text.split('\n')
    fixed = []
    for i, line in enumerate(lines):
        if line.strip().startswith('|') and i > 0 and fixed and fixed[-1].strip() and not fixed[-1].strip().startswith('|'):
            fixed.append('')
        fixed.append(line)
    return '\n'.join(fixed)


def build_section(num, title, md_text, lang="cn"):
    md_text = _fix_table_spacing(md_text)
    body = markdown.markdown(md_text, extensions=["tables", "fenced_code"])
    section_label = "セクション" if lang == "ja" else "Section"
    return f"""
<div class="section">
  <div class="section-header">
    <div class="section-number">{section_label} {num}</div>
    <h2>{title}</h2>
  </div>
  {body}
</div>"""


# ── Main ──

def main():
    parser = argparse.ArgumentParser(
        description="Vedic Astrology Report Builder — MD → HTML (v2, auto-detect version)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python report_builder.py ./client_folder --name "John" --lang en
  python report_builder.py ./client_folder --name "山田" --lang ja
  python report_builder.py ./analysis --name "测试" --lagna "天蝎座" --lang cn
        """)
    parser.add_argument("folder", help="Folder with MD files (checks 'parts/' subfolder too)")
    parser.add_argument("--name", default="Client", help="Client name")
    parser.add_argument("--lagna", default="—", help="Ascendant")
    parser.add_argument("--gender", default="—", help="Gender")
    parser.add_argument("--status", default="—", help="Current status")
    parser.add_argument("--lang", default="cn", choices=["cn", "en", "ja"], help="Language (default: cn)")
    parser.add_argument("--output", default=None, help="Output HTML path")
    parser.add_argument("--include", default=None,
                        help="Comma-separated sections to include: core,career,love,qa,rectify (default: all)")
    parser.add_argument("--brand", default=None, choices=["pro", "open"],
                        help="Force brand: 'pro' or 'open' (default: auto-detect)")
    args = parser.parse_args()

    folder = args.folder.rstrip("/\\")
    if not os.path.isdir(folder):
        print(f"Error: {folder} is not a directory")
        sys.exit(1)

    # Check for 'parts/' subfolder
    parts_dir = os.path.join(folder, "parts")
    search_dir = parts_dir if os.path.isdir(parts_dir) else folder
    print(f"  Scanning: {search_dir}\n")

    found = find_files(search_dir)

    if not found:
        print(f"\nError: No MD files found in {search_dir}")
        sys.exit(1)

    # --include filter
    if args.include:
        include_set = set(args.include.lower().split(","))
        group_map = {
            "core":    {"G0", "G1", "G2", "G3", "G4", "G5"},
            "career":  {"G6"},
            "love":    {"G7"},
            "rectify": set(),  # handled by key name
            "qa":      set(),  # handled by key name
        }
        allowed_groups = set()
        allowed_keys = set()
        for g in include_set:
            g = g.strip()
            if g in group_map:
                allowed_groups |= group_map[g]
            if g == "rectify":
                allowed_keys.add("rectify")
            if g == "qa":
                allowed_keys.add("qa")
        # Always include appendix if core is included
        if "core" in include_set:
            allowed_groups.add("appendix")
        found = {k: v for k, v in found.items()
                 if v[1] in allowed_groups or k in allowed_keys}
        print(f"  Filter: --include {args.include} → {len(found)} sections")

    lang = args.lang
    pkg, desc, version = detect_package(found, lang, brand=args.brand)
    print(f"\n  Version: {version}")
    print(f"  Package: {pkg} | Language: {lang}")

    # Sort sections by priority
    ordered_items = sorted(found.items(), key=lambda x: x[1][0])

    # Assign dynamic part numbers based on groups
    group_to_part = {}  # group_id -> part_number
    next_part = 1
    for key, (priority, group, sub, cn_title, en_title, content) in ordered_items:
        if group == "appendix":
            continue  # appendix doesn't get a part number
        if group not in group_to_part:
            group_to_part[group] = next_part
            next_part += 1

    # Build ordered sections with titles
    sections = []  # [(display_title, html_content)]
    sec_num = 1
    for key, (priority, group, sub, cn_title, en_title, content) in ordered_items:
        base = localized_base_title(key, group, sub, cn_title, en_title, lang)
        part_num = group_to_part.get(group, 0)
        title = make_section_title(group, sub, base, part_num, lang)
        sections.append((title, content))
        sec_num += 1

    # Build HTML
    cover = build_cover(args.name, args.lagna, args.gender, args.status, pkg, desc, lang)
    toc = build_toc(sections, lang)

    sections_html = []
    for i, (title, content) in enumerate(sections, 1):
        num_str = f"{i:02d}"
        sections_html.append(build_section(num_str, title, content, lang))

    footer_cn = """<div class="footer-note">
  本报告基于传统吠陀占星方法（Parashari Jyotish | KN Rao School）。<br>
  每项结论均有量化行星指标支撑。仅供自我反思与战略思考参考。<br>
  &copy; Data-Driven Vedic Astrology</div>"""
    footer_en = """<div class="footer-note">
  Generated using traditional Vedic astrological methods (Parashari Jyotish | KN Rao School).<br>
  Every claim backed by quantified planetary metrics. For self-reflection purposes only.<br>
  &copy; Data-Driven Vedic Astrology</div>"""
    footer_ja = """<div class="footer-note">
  伝統的なヴェーダ占星術（Parashari Jyotish | KN Rao School）に基づいて作成しています。<br>
  判断はチャート指標と監査可能な根拠に基づきます。自己理解と文化的研究を目的としたレポートです。<br>
  &copy; Data-Driven Vedic Astrology</div>"""
    footer = {"cn": footer_cn, "en": footer_en, "ja": footer_ja}[lang]

    html_lang = {"cn": "zh-CN", "en": "en", "ja": "ja"}[lang]
    html_title = {
        "cn": f"吠陀占星完整解读 — {args.name}",
        "en": f"Vedic Astrology Reading — {args.name}",
        "ja": f"ヴェーダ占星術 総合鑑定 — {args.name}",
    }[lang]
    html = f"""<!DOCTYPE html>
<html lang="{html_lang}"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_title}</title>
<style>{CSS}</style></head>
<body>{cover}{toc}{"".join(sections_html)}{footer}</body></html>"""

    out = args.output or os.path.join(folder, "report.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)

    size = os.path.getsize(out) / 1024
    print(f"\n  [OK] Output: {out} ({size:.0f} KB)")
    print(f"  -> Open in browser -> Ctrl+P -> Save as PDF")
    print(f"\n  Sections: {len(sections)}")
    for title, _ in sections:
        print(f"    • {title}")


if __name__ == "__main__":
    main()
