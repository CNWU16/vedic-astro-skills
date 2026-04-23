"""
Vedic Report Builder — Universal MD → HTML Pipeline
=====================================================
Supports ALL Vedic skill outputs: Core, Career, Love, Q&A

Usage:
  python report_builder.py <folder> [--name "Name"] [--lagna "Cancer"] [--lang cn]

The script auto-detects which MD files exist and builds accordingly.
It checks both the folder itself and a 'parts/' subfolder.

Supported file patterns:
  Core:    p1_basics.md, p2_planets.md, p3_d9.md, p4_houses.md, p5a_life.md, p5b_life.md
           OR 01_core.md
  Career:  career_part1.md, career_part2.md, career_part3.md
           OR 02_career.md, career_phase*.md, career.md
  Love:    love_part1.md, love_part2.md
           OR 03_love.md, love.md
  Q&A:     qa_*.md (any file starting with qa_)

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
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

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
  font-family: -apple-system, "PingFang SC", "Microsoft YaHei", "Hiragino Sans GB", "Noto Sans SC", sans-serif;
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
  display: flex; flex-direction: column; justify-content: center;
  position: relative; padding: 60px 10px;
}
.cover::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0;
  height: 2px; background: linear-gradient(90deg, transparent 5%, var(--gold-line) 30%, var(--gold-soft) 50%, var(--gold-line) 70%, transparent 95%);
}
.cover-badge {
  color: var(--gold); font-family: 'Inter', sans-serif;
  font-size: 11px; font-weight: 600;
  letter-spacing: 3px; text-transform: uppercase; margin-bottom: 20px;
}
.cover h1 {
  font-family: "Noto Serif SC", "Songti SC", "SimSun", serif;
  font-size: 46px; font-weight: 700;
  color: var(--brown); line-height: 1.35; margin-bottom: 16px;
}
.cover h1 span { color: var(--gold); }
.cover .subtitle {
  font-size: 15px; color: var(--text-muted); font-weight: 400;
  margin-bottom: 50px; letter-spacing: 0.5px;
}
.cover-meta { margin-top: 50px; padding-top: 28px; border-top: 1px solid var(--border-light); }
.cover-meta-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 8px 40px;
  font-size: 13px; color: var(--text-muted);
}
.cover-meta-grid dt { font-weight: 600; color: var(--brown); font-size: 11px; letter-spacing: 0.5px; margin-top: 12px; }
.cover-meta-grid dd { margin: 2px 0 0; }

.toc { page-break-after: always; padding: 40px 0; }
.toc h2 {
  font-family: "Noto Serif SC", serif; font-size: 22px; color: var(--brown);
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
  font-family: "Noto Serif SC", serif; font-size: 21px; font-weight: 700;
  margin-top: 2px; border: none; color: var(--brown) !important; padding-bottom: 0;
}

h1 {
  font-family: "Noto Serif SC", serif; font-size: 22px; color: var(--brown);
  margin: 32px 0 14px; padding-bottom: 6px; border-bottom: 1px solid var(--border-light);
  font-weight: 600;
}
h2 {
  font-family: "Noto Serif SC", serif; font-size: 18px; color: var(--brown);
  margin: 28px 0 12px; font-weight: 600; padding-bottom: 0; border-bottom: none;
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

# ── Section definitions ──
# Each entry: (priority, canonical_key, en_title, cn_title, filename_patterns)
SECTION_REGISTRY = [
    (10, "core",      "Part I: Core Audit",                    "第一部分：核心审计",
     ["01_core.md", "p1_data.md", "p1_basics.md", "core.md"]),
    (15, "planets_a", "Part II-A: Planets (Sun/Moon/Mars)",    "第二部分A：行星审计 (日/月/火)",
     ["p2a_planets.md"]),
    (17, "planets_b", "Part II-B: Planets (Me/Ju/Ve)",         "第二部分B：行星审计 (水/木/金)",
     ["p2b_planets.md"]),
    (19, "planets_c", "Part II-C: Planets (Sa/Ra/Ke)",         "第二部分C：行星审计 (土/罗/计)",
     ["p2c_planets.md"]),
    (20, "planets",   "Part II: Planetary Audit (P1-P12)",     "第二部分：行星审计 (P1-P12)",
     ["02_planets.md", "p2_planets.md", "planets.md"]),
    (30, "d9",        "Part III: D9 Navamsha Calibration",     "第三部分：D9品质校准",
     ["03_d9.md", "p3_d9.md", "d9.md"]),
    (40, "houses",    "Part IV: House Diagnostics",            "第四部分：宫位诊断",
     ["04_houses.md", "p4_houses.md", "houses.md"]),
    (50, "life",      "Part V: Life Architecture",             "第五部分：人生架构总结",
     ["05_life.md", "p5a_life.md", "p5_life.md", "life.md"]),
    (55, "life2",     "Part V (cont.): Life Architecture",     "第五部分（续）：人生架构总结",
     ["05b_life.md", "p5b_life.md", "life2.md"]),
    # Career
    (60, "career1",   "Part VI: Career — Portrait & Narrative","第六部分：事业 — 画像与叙事",
     ["career_part1.md", "career_phase1_2.md"]),
    (65, "career2",   "Part VI (cont.): Career — Strategy",    "第六部分（续）：事业 — 战略决策",
     ["career_part2.md", "career_phase3.md"]),
    (68, "career3",   "Part VI (cont.): Career — Risk & Advice","第六部分（续）：事业 — 风险与箴言",
     ["career_part3.md", "career_phase4.md"]),
    (70, "career",    "Part VI: Career Architecture",           "第六部分：事业架构",
     ["02_career.md", "06_career.md", "career.md"]),
    # Love
    (80, "love1",     "Part VII: Love — System & Timeline",     "第七部分：感情 — 体质报告与时间轴",
     ["love_part1.md"]),
    (85, "love2",     "Part VII (cont.): Love — Advice & Risk", "第七部分（续）：感情 — 建议与风险",
     ["love_part2.md"]),
    (90, "love",      "Part VII: Love & Marriage",              "第七部分：感情与婚姻",
     ["03_love.md", "07_love.md", "love.md"]),
    # Q&A
    (100, "qa",       "Appendix: Q&A",                          "附录：追问答疑",
     []),  # handled separately via glob
]


def find_files(folder):
    """Auto-detect MD files using flexible naming."""
    found = {}  # canonical_key -> (priority, en_title, cn_title, content)

    for priority, key, en_title, cn_title, patterns in SECTION_REGISTRY:
        if not patterns:
            continue
        for pat in patterns:
            path = os.path.join(folder, pat)
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    found[key] = (priority, en_title, cn_title, f.read())
                print(f"  + {pat} -> {key}")
                break

    # Q&A: glob for qa_*.md
    qa_files = sorted(glob.glob(os.path.join(folder, "qa_*.md")))
    if qa_files:
        combined = []
        for qf in qa_files:
            with open(qf, "r", encoding="utf-8") as f:
                combined.append(f"<!-- {os.path.basename(qf)} -->\n{f.read()}")
            print(f"  + {os.path.basename(qf)} -> qa")
        found["qa"] = (100, "Appendix: Q&A", "附录：追问答疑", "\n\n---\n\n".join(combined))

    return found


def detect_package(found, lang="cn"):
    has_core = any(k in found for k in ["core", "planets", "d9", "houses", "life"])
    has_career = any(k in found for k in ["career", "career1", "career2", "career3"])
    has_love = any(k in found for k in ["love", "love1", "love2"])
    has_qa = "qa" in found

    parts = []
    if has_core:    parts.append("Core" if lang == "en" else "核心")
    if has_career:  parts.append("Career" if lang == "en" else "事业")
    if has_love:    parts.append("Love" if lang == "en" else "感情")
    if has_qa:      parts.append("Q&A" if lang == "en" else "答疑")

    if lang == "cn":
        return " + ".join(parts), " + ".join(parts) + " 完整报告"
    return " + ".join(parts), " + ".join(parts) + " Complete Reading"


def build_cover(name, lagna, gender, status, pkg, desc, lang="cn"):
    badge = "数据驱动吠陀占星" if lang == "cn" else "Data-Driven Vedic Astrology"
    h1 = "吠陀占星<br><span>完整解读</span>" if lang == "cn" else "Vedic Astrology<br><span>Complete Reading</span>"
    L = {
        "cn": ["客户", "上升星座", "基本信息", "套餐", "体系", "软件", "大运", "量化指标"],
        "en": ["Client", "Ascendant", "Profile", "Package", "Methodology", "Software", "Dasha", "Metrics"],
    }[lang]
    return f"""
<div class="cover">
  <div class="cover-badge">{badge}</div>
  <h1>{h1}</h1>
  <div class="subtitle">{desc}</div>
  <div class="cover-meta"><div class="cover-meta-grid">
    <div><dt>{L[0]}</dt><dd>{name}</dd></div>
    <div><dt>{L[1]}</dt><dd>{lagna}</dd></div>
    <div><dt>{L[2]}</dt><dd>{gender} | {status}</dd></div>
    <div><dt>{L[3]}</dt><dd>{pkg}</dd></div>
    <div><dt>{L[4]}</dt><dd>Parashari Jyotish | KN Rao School</dd></div>
    <div><dt>{L[5]}</dt><dd>Jagannatha Hora v8.0 | Lahiri Ayanamsha</dd></div>
    <div><dt>{L[6]}</dt><dd>Vimsottari (Mahadasha + Antardasha)</dd></div>
    <div><dt>{L[7]}</dt><dd>Shadbala, Ashtakavarga (SAV/BAV), D9 Navamsha</dd></div>
  </div></div>
</div>"""


def build_toc(sections, lang="cn"):
    toc_title = "目录" if lang == "cn" else "Table of Contents"
    items = []
    for _, _, en_title, cn_title, _ in sections:
        title = cn_title if lang == "cn" else en_title
        items.append(f'<li class="toc-part">{title}</li>')
    return f'<div class="toc"><h2>{toc_title}</h2><ul class="toc-list">{"".join(items)}</ul></div>'


def build_section(num, title, md_text):
    body = markdown.markdown(md_text, extensions=["tables", "fenced_code"])
    return f"""
<div class="section">
  <div class="section-header">
    <div class="section-number">Section {num}</div>
    <h2>{title}</h2>
  </div>
  {body}
</div>"""


def main():
    parser = argparse.ArgumentParser(
        description="Vedic Astrology Report Builder — MD → HTML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python report_builder.py ./client_folder --name "John" --lang en
  python report_builder.py ./analysis --name "测试" --lagna "天蝎座" --lang cn
        """)
    parser.add_argument("folder", help="Folder with MD files (checks 'parts/' subfolder too)")
    parser.add_argument("--name", default="Client", help="Client name")
    parser.add_argument("--lagna", default="—", help="Ascendant")
    parser.add_argument("--gender", default="—", help="Gender")
    parser.add_argument("--status", default="—", help="Current status")
    parser.add_argument("--lang", default="cn", choices=["cn", "en"], help="Language (default: cn)")
    parser.add_argument("--output", default=None, help="Output HTML path")
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
        print("  Expected files like: p1_basics.md, career_part1.md, love_part1.md, qa_*.md")
        sys.exit(1)

    lang = args.lang
    pkg, desc = detect_package(found, lang)
    print(f"\n  Package: {pkg} | Language: {lang}")

    # Sort sections by priority
    ordered = []
    sec_num = 1
    for priority, key, en_title, cn_title, _ in SECTION_REGISTRY:
        if key in found:
            p, et, ct, content = found[key]
            title = ct if lang == "cn" else et
            ordered.append((sec_num, key, en_title, cn_title, content))
            sec_num += 1

    # Build HTML
    cover = build_cover(args.name, args.lagna, args.gender, args.status, pkg, desc, lang)
    toc = build_toc(ordered, lang)

    sections_html = []
    for num, key, en_title, cn_title, content in ordered:
        title = cn_title if lang == "cn" else en_title
        num_str = f"{num:02d}"
        sections_html.append(build_section(num_str, title, content))

    footer_cn = """<div class="footer-note">
  本报告基于传统吠陀占星方法（Parashari Jyotish | KN Rao School）。<br>
  每项结论均有量化行星指标支撑。仅供自我反思与战略思考参考。<br>
  &copy; Data-Driven Vedic Astrology</div>"""
    footer_en = """<div class="footer-note">
  Generated using traditional Vedic astrological methods (Parashari Jyotish | KN Rao School).<br>
  Every claim backed by quantified planetary metrics. For self-reflection purposes only.<br>
  &copy; Data-Driven Vedic Astrology</div>"""
    footer = footer_cn if lang == "cn" else footer_en

    html_lang = "zh-CN" if lang == "cn" else "en"
    html = f"""<!DOCTYPE html>
<html lang="{html_lang}"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Vedic Astrology Reading — {args.name}</title>
<style>{CSS}</style></head>
<body>{cover}{toc}{"".join(sections_html)}{footer}</body></html>"""

    out = args.output or os.path.join(folder, "report.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)

    size = os.path.getsize(out) / 1024
    print(f"\n  [OK] Output: {out} ({size:.0f} KB)")
    print(f"  -> Open in browser -> Ctrl+P -> Save as PDF")


if __name__ == "__main__":
    main()
