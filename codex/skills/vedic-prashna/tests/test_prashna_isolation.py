"""
Prashna 隔离回归测：确保沙箱化硬约束不被打破。
七条隔离断言 + 时间副层算例 + 标准层算例，任一红即禁止上线。每次 sync 前必跑。

对应 SKILL.md §隔离硬约束 与 resources/timing-layer.md。
"""
import os
import re
import sys
from pathlib import Path

# 从本文件位置推导 skills 根，不再硬编码机器路径（Mac 也要能跑）。
#   仓布局   <repo>/skills/vedic-prashna/tests/本文件
#   安装布局 ~/.claude/skills/vedic-prashna/tests/本文件
# 两种布局下 parents[2] 都是 skills 根。
# VEDIC_SKILLS_ROOT 可覆盖：consistency_lint 靠它对开源仓/Pro 仓各跑一遍——
# Pro 的 core 在仓里同样叫 vedic-core（不叫 vedic-core-pro），只跑开源仓根的话
# 断言2的 GUARDED_SKILLS 会 exists()==False 静默跳过 Pro，那是漏检不是通过。
SKILLS_ROOT = Path(os.environ.get("VEDIC_SKILLS_ROOT") or Path(__file__).resolve().parents[2])
PRASHNA_ROOT = SKILLS_ROOT / "vedic-prashna"


# ---------------------------------------------------------------------------
# 断言 1：共享 engine.py / formatter.py 输出字段无异体系 key
# ---------------------------------------------------------------------------
FORBIDDEN_ENGINE_KEYS = [
    "tajika",
    "ithasala",
    "kp_",
    "sub_lord",
    "sublord",
    "void_of_course",
    "kambula",
    "kamboola",
    "ishraga",
    "muthashila",
    "manau",
]


def test_engine_no_alien_fields() -> None:
    hits = []
    for fname in ("engine.py", "formatter.py"):
        path = SKILLS_ROOT / "vedic-calculator" / "scripts" / fname
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for key in FORBIDDEN_ENGINE_KEYS:
            if key in text:
                hits.append(f"{fname}: {key}")
    assert not hits, (
        "红灯：共享 engine 出现异体系 key —— 违反沙箱化硬约束 #1。\n"
        "engine.py/formatter.py 是所有 skill 共享的核心，异体系字段一旦进入即污染主系统。\n"
        "修复：把这些字段全部移回 vedic-prashna/scripts/calc_optional_*.py。\n"
        f"命中: {hits}"
    )


# ---------------------------------------------------------------------------
# 断言 2：主系统 skill 规则文件无 Prashna 异体系术语
# ---------------------------------------------------------------------------
GUARDED_SKILLS = [
    "vedic-core",
    "vedic-core-pro",
    "vedic-love",
    "vedic-career",
    "vedic-synastry",
    "vedic-rectifier",
    "vedic-reader",
]

FORBIDDEN_TERMS = [
    "prashna",
    "tajika",
    "ithasala",
    "sub-lord",
    "sub_lord",
    "sublord",
    "chandra kriya",
]


def test_shared_rules_no_prashna_terms() -> None:
    offenders = []
    for skill in GUARDED_SKILLS:
        skill_root = SKILLS_ROOT / skill
        if not skill_root.exists():
            continue
        for path in skill_root.rglob("*.md"):
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
            for term in FORBIDDEN_TERMS:
                if term in text:
                    rel = path.relative_to(SKILLS_ROOT)
                    offenders.append(f"{rel}: '{term}'")
    assert not offenders, (
        "红灯：主系统 skill 规则文件出现 Prashna/异体系术语 —— 违反沙箱化硬约束 #2。\n"
        "主系统 skill 应对 Prashna 零感知。这些术语必须完全存在于 vedic-prashna/ 内。\n"
        f"命中:\n  " + "\n  ".join(offenders)
    )


# ---------------------------------------------------------------------------
# 断言 3：Prashna 产物物理隔离
# ---------------------------------------------------------------------------
def test_prashna_products_in_isolated_dir() -> None:
    build_script = PRASHNA_ROOT / "scripts" / "build_prashna_data.py"
    if not build_script.exists():
        # 尚未实现，跳过（Task #2 才落地）
        return

    text = build_script.read_text(encoding="utf-8", errors="ignore")

    # 剥掉 # 注释与三引号 docstring/字符串块，只检查真实代码体。
    # 允许注释/docstring 自由说明"与本命 structured_data.md 严格区分"这类关系。
    code = re.sub(r'"""[\s\S]*?"""', '', text)
    code = re.sub(r"'''[\s\S]*?'''", '', code)
    code = re.sub(r'#[^\n]*', '', code)

    assert "prashna_" in code, (
        "红灯：build_prashna_data.py 代码体未见 'prashna_' 独立目录前缀 —— 违反沙箱化硬约束 #3。\n"
        "所有产物必须写 prashna_<yyyymmdd_HHMM>_<label>/ 独立子目录。"
    )

    assert "structured_prashna.md" in code, (
        "红灯：build_prashna_data.py 代码体未见产物名 'structured_prashna.md' —— 违反沙箱化硬约束 #3。\n"
        "Prashna 产物必须命名为 structured_prashna.md，与本命根 structured_data.md 严格区分。"
    )

    forbidden_writes = re.findall(r"structured_data\.md", code)
    assert not forbidden_writes, (
        "红灯：build_prashna_data.py 代码体(排除注释/docstring)中出现 structured_data.md —— "
        "违反沙箱化硬约束 #3。Prashna 产物名必须为 structured_prashna.md，"
        "代码路径不得写入或引用本命根 structured_data.md。"
    )


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# 断言 4：主系统 skill 的 scripts 不得反向 import vedic-prashna 沙箱模块
# ---------------------------------------------------------------------------
# 防呆：SAV / graha drishti 越权都是"未预见路径泄漏"栽的；
# 主 skill 会话 2026-07-12 复核建议加此断言。
PRASHNA_SANDBOX_MODULES = [
    "calc_moon_vedic",
    "calc_optional_tajika",
    "calc_optional_kp",
    "calc_timing",
    "build_prashna_data",
    "build_timing_overlay",
    "vedic_prashna",   # 目录名换 py 合法标识符的可能拼法
]


def test_no_reverse_import_from_prashna() -> None:
    guarded_skills = [
        "vedic-core", "vedic-core-pro", "vedic-love", "vedic-career",
        "vedic-synastry", "vedic-rectifier", "vedic-reader", "vedic-calculator",
    ]
    offenders = []
    for skill in guarded_skills:
        skill_root = SKILLS_ROOT / skill
        if not skill_root.exists():
            continue
        for path in skill_root.rglob("*.py"):
            if "__pycache__" in str(path):
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for mod in PRASHNA_SANDBOX_MODULES:
                # 匹配 `import <mod>` 或 `from <mod> import ...`(行首)
                pattern = rf"^\s*(?:from\s+{re.escape(mod)}\b|import\s+{re.escape(mod)}\b)"
                if re.search(pattern, text, re.MULTILINE):
                    rel = path.relative_to(SKILLS_ROOT)
                    offenders.append(f"{rel}: import '{mod}'")
            # 也扫路径字符串 `vedic-prashna/scripts` 出现在 sys.path 操作里
            if "vedic-prashna" in text and re.search(r"sys\.path|import", text):
                # 只在真的 import 上下文里报（避免注释误伤）
                for line in text.split("\n"):
                    line_lower = line.lower()
                    if "vedic-prashna" in line_lower and (
                        "sys.path" in line_lower or "importlib" in line_lower
                    ):
                        rel = path.relative_to(SKILLS_ROOT)
                        offenders.append(f"{rel}: sys.path/importlib refers 'vedic-prashna'")
                        break
    assert not offenders, (
        "红灯：主系统 skill 的 scripts 反向 import Prashna 沙箱模块 —— 违反沙箱化(防呆断言 #4)。\n"
        "主系统不应依赖 Prashna 沙箱代码；即便当前用途看似合理，也会让沙箱变成'半共享'、"
        "泄漏路径破防。修复：把该逻辑挪回 vedic-prashna/scripts/ 内、或改由主系统独立实现。\n"
        "命中:\n  " + "\n  ".join(offenders)
    )


# ---------------------------------------------------------------------------
# 断言 5/6/7：时间副层、标准层、Tajika、KP 互不导入
# ---------------------------------------------------------------------------
def _imports(path: Path, modules) -> list:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="ignore")
    return [
        f"{path.name}: import '{mod}'"
        for mod in modules
        if re.search(
            rf"^\s*(?:from\s+{re.escape(mod)}\b|import\s+{re.escape(mod)}\b)",
            text, re.MULTILINE,
        )
    ]


def test_standard_builder_no_timing_import() -> None:
    offenders = []
    for name in ("build_prashna_data.py", "format_prashna_standard.py",
                 "calc_moon_vedic.py", "prashna_time.py"):
        offenders += _imports(PRASHNA_ROOT / "scripts" / name,
                              ("calc_timing", "build_timing_overlay"))
    assert not offenders, (
        "红灯：标准层脚本导入时间副层 —— 时间副层只在定档后单独运行，不得进入标准产物。\n"
        "命中:\n  " + "\n  ".join(offenders)
    )


def test_standard_builder_no_optional_stack_import() -> None:
    offenders = []
    for name in ("build_prashna_data.py", "format_prashna_standard.py",
                 "calc_moon_vedic.py", "prashna_time.py"):
        offenders += _imports(PRASHNA_ROOT / "scripts" / name,
                              ("calc_optional_tajika", "calc_optional_kp",
                               "build_tajika_overlay", "build_kp_horary"))
    for name in ("calc_optional_tajika.py", "build_tajika_overlay.py"):
        offenders += _imports(PRASHNA_ROOT / "scripts" / name,
                              ("calc_optional_kp", "build_kp_horary"))
    for name in ("calc_optional_kp.py", "build_kp_horary.py"):
        offenders += _imports(PRASHNA_ROOT / "scripts" / name,
                              ("calc_optional_tajika", "build_tajika_overlay",
                               "format_prashna_standard", "calc_moon_vedic"))
    assert not offenders, (
        "红灯：标准层导入 Tajika/KP，或 Tajika 与 KP 互相导入 —— 可选栈只能单独运行，"
        "KP 不得借用标准层的格式化或 Moon 段。\n"
        "命中:\n  " + "\n  ".join(offenders)
    )


def test_timing_no_optional_stack_import() -> None:
    offenders = []
    for name in ("calc_timing.py", "build_timing_overlay.py"):
        offenders += _imports(PRASHNA_ROOT / "scripts" / name,
                              ("calc_optional_tajika", "calc_optional_kp",
                               "build_tajika_overlay", "build_kp_horary"))
    assert not offenders, (
        "红灯：时间副层导入 Tajika/KP —— 时间副层来源只有 M/P，不得借用可选栈的时间。\n"
        "命中:\n  " + "\n  ".join(offenders)
    )


# ---------------------------------------------------------------------------
# 算例 7：时间副层对 Raman 注算例与 Moon 入座搜索
# ---------------------------------------------------------------------------
def test_timing_worked_examples() -> None:
    scripts = str(PRASHNA_ROOT / "scripts")
    if not (PRASHNA_ROOT / "scripts" / "calc_timing.py").exists():
        return
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    import calc_timing as ct

    # M-XIV.82 Raman 注：上升 Navamsa 为 Leo，Sun 在第 5 个 Navamsa → 5 × 6 = 30 个月
    t4 = ct.t4_navamsa_lord_period("Sun", 14.0)
    assert (t4["navamsa_ordinal"], t4["value"], t4["unit"]) == (5, 30, "个月"), t4
    assert ct.navamsa_ordinal(0.0) == 1 and ct.navamsa_ordinal(29.99) == 9

    # M-XIV.85 Raman 注：7 宫主 Sun 在 6 宫(不可见半球)，含首尾 12 宫 → 12 个月
    t2 = ct.t2_house_lord_count(7, "Sun", 6)
    assert (t2["count"], t2["unit"]) == (12, "个月"), t2
    assert ct.t2_house_lord_count(7, "Moon", 9)["unit"] == "天"

    # P-V.5：Lagna 有星算 1；Rahu/Ketu 不计
    assert ct.t1_return_days({"Rahu": 1, "Saturn": 3, "Sun": 5})["days"] == 36
    assert ct.t1_return_days({"Moon": 1})["days"] == 12

    # T3：匀速假 Moon(13.2°/日)，解析解对照；进入前 2 秒不在目标座
    lon0, rate = 100.0, 13.2
    lon_at = lambda jd: (lon0 + rate * jd) % 360.0  # noqa: E731
    for target in (4, 3, 2):   # 下一座 / 当前座(重新进入) / 上一座
        entry = ct.next_sign_entry(lon_at, 0.0, target)
        expected = ((target * 30.0 - lon0) % 360.0 or 360.0) / rate
        assert abs(entry - expected) < 2.0 / 86400.0, (target, entry, expected)
        assert int(lon_at(entry) / 30.0) == target
        assert int(lon_at(entry - 2.0 / 86400.0) / 30.0) != target


# ---------------------------------------------------------------------------
# 算例 8：标准层 Ayer 功能吉凶、tithi 与描述题查表（P-I.3 注两例、P-I.5 注、P-VI.4、P-I.7）
# ---------------------------------------------------------------------------
def test_standard_worked_examples() -> None:
    scripts = str(PRASHNA_ROOT / "scripts")
    if not (PRASHNA_ROOT / "scripts" / "format_prashna_standard.py").exists():
        return
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    import format_prashna_standard as fs

    def chart(basic, waxing=True):
        planets = {name: {"house": 1} for name in fs.CLASSICAL_PLANETS}
        return {
            "planets": planets,
            "moon_phase": {"waxing": waxing},
            "dignity": {name: {"basic": value} for name, value in basic.items()},
        }

    # 注例一：Jupiter 对 Capricorn 主 3、12 且落陷 → 凶；不落陷时回落自然吉
    assert fs._ayer_role(chart({"Jupiter": "debilitated"}), "Jupiter", "Capricorn") == "凶(注例一)"
    assert fs._ayer_role(chart({"Jupiter": "exalted"}), "Jupiter", "Capricorn") == "吉(回落)"
    # 注例二：Mars 对 Leo 主 4、9，须强才吉；入旺从 Capricorn 照 Leo → 吉，友座不强 → 回落凶
    assert fs._ayer_role(chart({"Mars": "exalted"}), "Mars", "Leo") == "吉(注例二)"
    assert fs._ayer_role(chart({"Mars": "friend"}), "Mars", "Leo") == "凶(回落)"
    # Saturn 入旺于 Libra：对 Libra 主 4、5 → 吉
    assert fs._ayer_role(chart({"Saturn": "exalted"}), "Saturn", "Libra") == "吉(注例二)"
    # 本宫主恒吉，凶星也一样；亏月回落为凶
    assert fs._ayer_role(chart({"Saturn": "debilitated"}), "Saturn", "Aquarius") == "吉(宫主)"
    assert fs._ayer_role(chart({"Moon": "neutral"}, waxing=False), "Moon", "Aries") == "凶(回落)"

    # tithi 满月窗：白半月第 10 至黑半月第 5（108° ≤ 距离 < 240°）
    for diff, expected in ((107.9, (9, False)), (108.0, (10, True)),
                           (239.9, (20, True)), (240.0, (21, False))):
        assert fs.tithi_facts(350.0, (350.0 + diff) % 360.0) == expected, diff

    # P-VI.4 距离：前半距第 1 个 Navamsa，后半距中间第 5 个
    assert fs._navamsa_number(0.0) == 1 and fs._navamsa_number(14.9) == 5
    assert fs._navamsa_number(15.0) == 5 and fs._navamsa_number(29.99) == 9
    # P-I.7：奇数座 1/4/7 Dhatu，偶数座 1/4/7 Jeeva
    assert fs.OBJECT_KINDS_ODD[0].startswith("Dhatu")
    assert fs.OBJECT_KINDS_EVEN[0].startswith("Jeeva")

    # P-I.4 注六分盘：M-XVIII.148 注 Virgo 30° → Mercury、Sun、Venus、Mercury、Sun、Mars
    signs = fs._shadvarga_signs("Virgo", 29.99)
    lords = [fs.SIGN_LORDS[signs[k]] for k in ("D1", "D2", "D3", "D9", "D12", "D30")]
    assert lords == ["Mercury", "Sun", "Venus", "Mercury", "Sun", "Mars"], signs
    # 传统 Hora：奇数座前半 Sun（Leo），偶数座前半 Moon（Cancer）
    assert fs._shadvarga_signs("Aries", 3.0)["D2"] == "Leo"
    assert fs._shadvarga_signs("Taurus", 3.0)["D2"] == "Cancer"
    # 多数临界距离：两侧在临界距离以内多数不变，越过一侧即变
    ch = chart({})
    base = fs._shadvarga_majority(ch, "Aries", 0.5)[2]
    crit = fs._shadvarga_critical(ch, "Aries", 0.5)
    assert crit is not None and crit > 0
    inside = [fs._shadvarga_majority(ch, "Aries", x)[2] for x in (0.5 + crit - 1e-6, max(0.0, 0.5 - crit + 1e-6))]
    outside = [fs._shadvarga_majority(ch, "Aries", x)[2] for x in (0.5 + crit + 1e-6, 0.5 - crit - 1e-6) if 0 <= x < 30]
    assert inside == [base, base], (base, crit, inside)
    assert any(v != base for v in outside), (base, crit, outside)

    # 能力层与意愿层事实（2026-10-28 杭州私下见面盘的结构，Pisces 上升）。期望值手算：
    # 7 宫主 Mercury 落 8 宫 Libra、逆行，同宫 Venus 是 Libra 宫主（吉）且 Libra 为天然友座 → 两项、有救应 → 能力打折；
    # 3 宫主 Venus 本座但落 8 宫、燃烧、逆行、同宫 Sun 与照射的 Mars 皆凶且无吉 → 四项 → 严重受损。
    order = fs.SIGNS[11:] + fs.SIGNS[:11]
    lords = {h: {"sign": order[h - 1], "lord": fs.SIGN_LORDS[order[h - 1]]} for h in range(1, 13)}
    where = {"Sun": (8, "Libra"), "Moon": (3, "Taurus"), "Mars": (5, "Cancer"),
             "Mercury": (8, "Libra"), "Jupiter": (5, "Cancer"), "Venus": (8, "Libra"),
             "Saturn": (1, "Pisces"), "Rahu": (12, "Aquarius"), "Ketu": (6, "Leo")}
    retro = {"Mercury", "Venus", "Saturn"}
    sight = {"Sun": [2], "Moon": [9], "Mars": [8, 11, 12], "Mercury": [2],
             "Jupiter": [9, 11, 1], "Venus": [2], "Saturn": [3, 7, 10]}
    pisces = {
        "lagna": {"sign": "Pisces"},
        "house_lords": lords,
        "planets": {n: {"house": h, "sign": s, "retrograde": n in retro} for n, (h, s) in where.items()},
        "dignity": {n: {"basic": b} for n, b in {
            "Sun": "debilitated", "Moon": "exalted", "Mars": "debilitated", "Mercury": "neutral",
            "Jupiter": "exalted", "Venus": "own_sign", "Saturn": "enemy"}.items()},
        "combustion": {"Venus": {"distance": 7.0}},
        "graha_drishti": {n: {"from_house": where[n][0], "aspected_houses": hs} for n, hs in sight.items()},
        "moon_phase": {"waxing": False},
    }
    planet, factors, rescue, verdict = fs._lord_ability(pisces, 7)
    assert (planet, verdict) == ("Mercury", "能力打折"), (factors, rescue, verdict)
    assert factors == ["落8宫", "逆行"] and "天然友座" in rescue and "吉星占照" in rescue, (factors, rescue)
    assert fs._lord_ability(pisces, 3)[3] == "严重受损"
    # 8 宫主 Venus 坐本宫（Libra 8 宫）：不记"落8宫"（M-XIV.42）；3 宫主同一颗 Venus 不在本宫，仍记
    _, f8, _, v8 = fs._lord_ability(pisces, 8)
    assert "落8宫" not in f8 and f8[:2] == ["燃烧", "逆行"] and v8 == "严重受损", (f8, v8)
    assert "落8宫" in fs._lord_ability(pisces, 3)[1]
    # Lagna 主 Jupiter 被 Mars 同宫：能力表写出凶星名，供按需减项（rubric §2.1）
    assert fs._lord_ability(pisces, 1)[1] == ["受凶星占照（Mars）、无吉星"]
    # M-XIV.43：Jupiter（5 宫）与 Mercury（8 宫）互为 4／10 宫 → 已连上
    assert fs._lord_links(pisces, 7)[3] == "互为4/10宫"
    assert fs._lord_links(pisces, 2)[3] == "同宫"  # Mars 与 Lagna 主 Jupiter 同落 5 宫
    assert fs._relation(pisces, "Mars", "Mercury") == ["Mars 照 Mercury", "互为4/10宫"]
    # 行动链（对方 7 宫）：起意宫主＝7 起第 3 宫＝9 宫主 Mars，照 Mercury；行动宫主＝4 宫主 Mercury 即本星；
    # 指向：Mercury 与 Jupiter 互为 4／10 宫，另经 Mars 串联 → 偏会
    start, move, point, weak, verdict = fs._action_chain(pisces, 7)
    assert fs._derived(7, 3) == 9 and fs._derived(7, 10) == 4 and fs._derived(7, 11) == 5
    assert start == ["起意宫主 Mars–Mercury：Mars 照 Mercury、互为4/10宫", "Mars–Mercury：Mars 照 Mercury"], start
    assert move == "即行动者宫主 Mercury" and not weak and verdict == "偏会", (move, weak, verdict)
    assert point == ["Mercury–Jupiter：互为4/10宫", "Mars–Jupiter：同宫",
                     "经 Mars 串联（Mars–Jupiter：同宫；Mars–Mercury：Mars 照 Mercury）"], point


# ---------------------------------------------------------------------------
# 算例 9：秒级整盘一个瞬间（2026-10-22 外部报告的原始失败盘）
#   旧版先用整分起 engine、再按秒补算一部分字段，D3/D12/D30 留在整分 → 六分盘表被隐藏
#   （随机秒数下约 5%）。期望值为 Parashara 手算，不取被测公式。
# ---------------------------------------------------------------------------
def test_exact_second_chart() -> None:
    calc = SKILLS_ROOT / "vedic-calculator" / "scripts"
    scripts = PRASHNA_ROOT / "scripts"
    if not (calc / "engine.py").exists() or not (scripts / "prashna_time.py").exists():
        return
    for p in (str(calc), str(scripts)):
        if p not in sys.path:
            sys.path.insert(0, p)
    import io
    import contextlib
    from datetime import datetime, timedelta
    from zoneinfo import ZoneInfo
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            import engine
            import prashna_time as pt
            import format_prashna_standard as fs
    except ImportError as e:
        raise AssertionError(f"依赖缺失（用 vedic-calculator 的 venv 跑）：{e}")

    zone, lat, lon = ZoneInfo("Asia/Shanghai"), 22.555, 113.883

    def chart(dt):
        with contextlib.redirect_stdout(io.StringIO()):
            return pt.calculate_prashna_chart(dt, lat, lon, "Asia/Shanghai")

    c = chart(datetime(2026, 10, 21, 14, 0, 50, tzinfo=zone))
    # Capricorn 20.02°（偶数、土象）：D3 第 3 段＝第 9 座 Virgo；D9 自 Capricorn 起第 7 段＝Cancer；
    # D12 第 9 段＝Virgo；D30 偶数座 20–25° 属 Saturn＝Capricorn
    got = tuple(c["divisional_charts"][k]["Lagna"]["sign"] for k in ("D3", "D9", "D12", "D30"))
    assert got == ("Virgo", "Cancer", "Virgo", "Capricorn"), got
    meta = c.get("calc_meta") or {}
    assert meta.get("instant_utc") == "2026-10-21T06:00:50.000000Z", meta
    text = "\n".join(fs._shadvarga_lines(c))
    assert "unavailable" not in text and "合计" in text, text

    # 20° 分界两侧各 0.2 s：表都显示（公式与 engine 分盘同一瞬间、同一 Lagna 基准）
    lo = datetime(2026, 10, 21, 14, 0, 0, tzinfo=zone)
    hi = datetime(2026, 10, 21, 14, 1, 30, tzinfo=zone)

    def degree(t):
        return engine.calc_lagna(pt.local_datetime_to_jd(t, "Asia/Shanghai"), lat, lon)["degree"]

    assert degree(lo) < 20.0 < degree(hi)
    for _ in range(30):
        mid = lo + (hi - lo) / 2
        if degree(mid) < 20.0:
            lo = mid
        else:
            hi = mid
    for t in (hi - timedelta(seconds=0.2), hi + timedelta(seconds=0.2)):
        text = "\n".join(fs._shadvarga_lines(chart(t)))
        assert "unavailable" not in text, (t, text)


# ---------------------------------------------------------------------------
# 算例 10：判定脚本（2026-10-29 重建：模型取象、脚本计数）
#   10-28 杭州私下见面原盘。期望值逐条手核：账本见 HANDOFF 20.5；D2 连接（Jupiter 与 Mercury 互为
#   4／10 宫）记有利；D4 语境检验：XVII.17 读 8 宫，8 宫被"私下"点到，不入账；D3 按需：Mercury
#   "落8宫"是应象、不算折损。三项都关时账本必须复现冻结版（prashna-20261029）。
#   档只按所给时刻定（10-29 创始人定：时间地点由提问人负责）；前后 60 秒的变化只记"输入提示"。
# ---------------------------------------------------------------------------
def test_judge_worked_example() -> None:
    calc = SKILLS_ROOT / "vedic-calculator" / "scripts"
    scripts = PRASHNA_ROOT / "scripts"
    if not (scripts / "prashna_rules.py").exists():
        raise AssertionError("缺 prashna_rules.py")
    for p in (str(calc), str(scripts)):
        if p not in sys.path:
            sys.path.insert(0, p)
    import io
    import contextlib
    from datetime import datetime, timedelta
    from zoneinfo import ZoneInfo
    with contextlib.redirect_stdout(io.StringIO()):
        import prashna_time as pt
        import prashna_rules as pr

    dt = datetime(2026, 10, 28, 15, 24, 0, 696168, tzinfo=ZoneInfo("Asia/Shanghai"))
    def chart(x):
        with contextlib.redirect_stdout(io.StringIO()):
            return pt.calculate_prashna_chart(x, 30.27, 120.15, "Asia/Shanghai")
    base = chart(dt)
    variants = [("−60 秒", chart(dt - timedelta(seconds=60))), ("+60 秒", chart(dt + timedelta(seconds=60)))]
    plan = pr.Plan.from_dict({
        "matter": "见面", "matter_house": 7, "context": "恋爱", "actor": 7,
        "keywords": [{"word": "私下", "houses": [8, 12, 4], "polarity": "相合", "source": "M-XIV.20"},
                     {"word": "对方主动", "houses": [9], "planets": ["Mars"], "polarity": "相合", "source": "M-XIV.5"}],
        "qualifiers": ["私下", "主动"], "location": "city"})
    v = pr.judge(base, plan, variants=variants)
    got = [(e["rule_id"], e["direction"], bool(e["excluded"])) for e in v["ledger"]]
    assert got == [("P-I.4", "mixed", False), ("P-I.3", "unf", False), ("M-XVII.5", "none", False),
                   ("M-XVII.15", "none", False), ("M-XVII.16", "fav", False), ("M-XVII.17", "unf", True),
                   ("P-IV.1", "mixed", False), ("M-XIV.43", "fav", False)], got
    assert v["sum"] == 1 and (v["tier"], v["strength"]) == ("偏成", "有阻力"), (v["sum"], v["tier"], v["strength"])
    assert v["branches"] == [] and v["sensitive"][0]["rules"] == ["P-I.4"], v["sensitive"]
    assert v["chain"]["verdict"] == "偏会"
    assert [(q["name"], q["result"]) for q in v["qualifiers"]] == [("私下", "成立"), ("主动", "成立")], v["qualifiers"]
    ab = v["ability"]
    assert (ab["planet"], ab["factors"], ab["verdict"]) == ("Mercury", ["逆行"], "能力打折"), ab
    assert ab["dropped"] == ["落8宫（措辞点到的宫，应象）"], ab["dropped"]

    # 三项拍板全关＝冻结版账本：合计 −1（HANDOFF 19.5）；档按所给时刻为偏不成·有转机，
    # −60 秒 P-I.4 转有利、合计 0（持平·吉凶相当）：只记输入提示，不改档
    off = pr.judge(base, plan, pr.Options(d2_link=False, d3_need=False, d4_context=False), variants)
    assert off["sum"] == -1 and (off["tier"], off["strength"]) == ("偏不成", "有转机"), (off["sum"], off["tier"])
    assert off["sensitive"][0]["tier"] == "持平·吉凶相当", off["sensitive"]
    assert off["ability"]["factors"] == ["落8宫", "逆行"], off["ability"]

    # 测试用户例："对方会公开我们的关系吗"，7 宫主飞 8 宫、8 宫主坐 8 宫 → 取隐藏之意，"公开"不成立。
    # 显隐第 2 步落入优先于连接（M-XIV.47）：Mercury 落 8 宫即定私密，不因它与 10 宫主互为 4／10 宫而打平落到半球
    pub = pr.Plan.from_dict({"matter": "通用", "matter_house": 7, "context": "恋爱", "qualifiers": ["公开"],
                             "keywords": [{"word": "公开", "houses": [10], "polarity": "相合", "source": "M-XIV.12"}]})
    pv = pr.judge(base, pub)
    q = pv["qualifiers"][0]
    assert (q["name"], q["result"]) == ("公开", "不成立") and "指标星 Mercury 落 8 宫 → 私下" in q["basis"], q
    # D13：必要条件不成立，按这个条件不能，不给时间；私下见面盘条件都成立，照常给
    assert pv["condition_failed"] == ["公开"] and pv["timing"] == "none", (pv["condition_failed"], pv["timing"])
    assert v["condition_failed"] == [] and v["timing"] == "general", (v["condition_failed"], v["timing"])

    # 根本三角归本座（10-30 engine v1.0.2）：Venus 天秤 0–15° 为 moolatrikona，8 宫主坐本宫的救应仍是"本座"
    import format_prashna_standard as F
    assert base["dignity"]["Venus"]["basic"] == "moolatrikona", base["dignity"]["Venus"]
    assert F._lord_ability(base, 8)[2] == ["本座"], F._lord_ability(base, 8)
    # M-XIV.40 弱而落吉位：2 宫主 Mars 落陷落 5 宫记救应、落陷照记；6 宫主 Sun 落陷落 8 宫不记。
    # D18：Mars 落陷巨蟹（Moon 天然友）不再记"天然友座"
    mars = F._lord_ability(base, 2)
    assert mars[1] == ["落陷"] and mars[2] == ["吉星占照", "弱而落吉位（5宫）"], mars
    assert not any(r.startswith("弱而落吉位") for r in F._lord_ability(base, 6)[2])

    # 描述型（D15）："我们相处会不会吵"：只出事实，不建账、不定档、不给时间
    desc = pr.Plan.from_dict({"matter": "描述", "matter_house": 7, "context": "恋爱",
                              "keywords": [{"word": "争吵", "houses": [6], "planets": ["Mars"], "polarity": "相合",
                                            "source": "M-XIV.117；6 宫争斗"}]})
    dv = pr.judge(base, desc, variants=variants)
    assert dv["ledger"] == [] and (dv["tier"], dv["timing"], dv["sensitive"]) == ("描述", "none", []), dv
    inf = [(r["at"], r["how"], r["planet"], r["hits"]) for r in dv["describe"]["influences"]]
    assert inf == [("7 宫", "照射", "Saturn", ["没点到"]), ("指标星 Mercury 所在 8 宫", "同宫", "Sun", ["争吵（相合）"]),
                   ("指标星 Mercury 所在 8 宫", "同宫", "Venus", ["没点到"]),
                   ("指标星 Mercury 所在 8 宫", "照射", "Mars", ["争吵（相合）"])], inf
    assert dv["describe"]["M-XIV.117"]["result"] == "不成立", dv["describe"]["M-XIV.117"]

    # 取象单校验：关键词要写出处；限定语"主动"要给行动者；描述型不收限定语
    for bad in ({"matter": "见面", "matter_house": 7, "keywords": [{"word": "私下", "houses": [8], "polarity": "相合"}]},
                {"matter": "见面", "matter_house": 7, "qualifiers": ["主动"]},
                {"matter": "描述", "matter_house": 7, "qualifiers": ["私下"]},
                {"matter": "不存在的题型"}):
        try:
            pr.Plan.from_dict(bad)
        except ValueError:
            continue
        raise AssertionError(f"取象单应被拒：{bad}")


def _run(name, fn):
    try:
        fn()
        print(f"[PASS] {name}")
        return True
    except AssertionError as e:
        print(f"[FAIL] {name}\n{e}\n")
        return False


if __name__ == "__main__":
    results = [
        _run("engine_no_alien_fields", test_engine_no_alien_fields),
        _run("shared_rules_no_prashna_terms", test_shared_rules_no_prashna_terms),
        _run("prashna_products_in_isolated_dir", test_prashna_products_in_isolated_dir),
        _run("no_reverse_import_from_prashna", test_no_reverse_import_from_prashna),
        _run("standard_builder_no_timing_import", test_standard_builder_no_timing_import),
        _run("timing_no_optional_stack_import", test_timing_no_optional_stack_import),
        _run("standard_builder_no_optional_stack_import",
             test_standard_builder_no_optional_stack_import),
        _run("timing_worked_examples", test_timing_worked_examples),
        _run("standard_worked_examples", test_standard_worked_examples),
        _run("exact_second_chart", test_exact_second_chart),
        _run("judge_worked_example", test_judge_worked_example),
    ]
    if all(results):
        print("\n[GREEN] 七条隔离断言、时间副层算例、标准层算例、秒级整盘算例与判定算例全绿。")
        sys.exit(0)
    else:
        print("\n[RED] 隔离断言未全绿，禁止上线。")
        sys.exit(1)
