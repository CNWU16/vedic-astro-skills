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
    ]
    if all(results):
        print("\n[GREEN] 七条隔离断言、时间副层算例与标准层算例全绿。")
        sys.exit(0)
    else:
        print("\n[RED] 隔离断言未全绿，禁止上线。")
        sys.exit(1)
