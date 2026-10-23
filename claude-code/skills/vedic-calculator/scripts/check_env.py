"""
vedic-calculator 环境诊断脚本
用法: python check_env.py  (任何Python版本都能跑这个脚本本身)

这个脚本会：
1. 找到可用的 venv 或合适的 Python
2. 检查所有依赖是否安装
3. 跑一个最小计算验证 SAV=337
4. 输出明确的 ✅/❌ 结果和修复指令
"""
import os, sys, subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)

def find_venv_python():
    """按优先级查找 venv 的 Python"""
    candidates = [
        os.path.join(SKILL_DIR, "venv", "Scripts", "python.exe"),  # Windows
        os.path.join(SKILL_DIR, "venv", "bin", "python"),          # Linux/Mac
    ]
    # 也检查工作目录
    cwd = os.getcwd()
    candidates += [
        os.path.join(cwd, "vedic-calc-env", "Scripts", "python.exe"),
        os.path.join(cwd, "vedic-calc-env", "bin", "python"),
        os.path.join(cwd, "venv", "Scripts", "python.exe"),
        os.path.join(cwd, "venv", "bin", "python"),
    ]
    for p in candidates:
        if os.path.isfile(p):
            return p
    return None

def run_python(python_exe, code):
    """用指定Python执行代码，返回(成功, 输出)"""
    try:
        r = subprocess.run(
            [python_exe, "-c", code],
            capture_output=True, text=True, timeout=30
        )
        return r.returncode == 0, (r.stdout + r.stderr).strip()
    except Exception as e:
        return False, str(e)

def check_dependency(python_exe, name, import_code, version_code=None):
    """检查单个依赖"""
    ok, out = run_python(python_exe, import_code)
    if not ok:
        return False, f"❌ {name}: 未安装 ({out[:80]})"
    if version_code:
        ok2, ver = run_python(python_exe, version_code)
        if ok2:
            return True, f"✅ {name}: {ver}"
    return True, f"✅ {name}: OK"

def main():
    print("=" * 50)
    print("  vedic-calculator 环境诊断")
    print("=" * 50)
    
    # 1. 定位
    print(f"\n📂 Skill目录: {SKILL_DIR}")
    print(f"📂 Scripts目录: {SCRIPT_DIR}")
    
    # 2. 找Python
    print(f"\n── Python 查找 ──")
    venv_python = find_venv_python()
    
    if venv_python:
        python_exe = venv_python
        ok, ver = run_python(python_exe, "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')")
        print(f"✅ 找到 venv: {venv_python}")
        print(f"   Python版本: {ver}")
    else:
        print(f"⬜ 未找到 venv")
        # 尝试系统Python
        python_exe = sys.executable
        ok, ver = run_python(python_exe, "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')")
        print(f"   系统Python: {python_exe} ({ver})")
        
        # 检查版本是否兼容
        ok2, ver_tuple = run_python(python_exe, "import sys; print(sys.version_info[:2])")
        if "(3, 14)" in ver_tuple or "(3, 15)" in ver_tuple:
            # 不兼容 + 无venv → 直接短路，后续检查必然全红，没有信息量
            print(f"\n{'=' * 50}")
            print(f"  ⚠️  无 venv + 系统 Python {ver} 不兼容")
            print(f"  pysweph 需要 Python 3.8~3.13，无法在 {ver} 上运行。")
            print(f"\n  修复方法（setup_env.py 会自动找 3.12/3.13 创建 venv）:")
            print(f"  {python_exe} {os.path.join(SCRIPT_DIR, 'setup_env.py')}")
            print(f"{'=' * 50}")
            return
    
    # 3. 检查依赖
    print(f"\n── 依赖检查 (使用: {python_exe}) ──")
    
    deps = [
        ("pysweph (swisseph)", 
         "import swisseph as swe",
         "import swisseph as swe; print(swe.version)"),
        ("PyJHora",
         "from jhora.panchanga import drik",
         None),
        ("pytz",
         "import pytz",
         "import pytz; print(pytz.__version__)"),
        ("zoneinfo 时区库（Windows 需 tzdata，vedic-prashna 用）",
         "from zoneinfo import ZoneInfo; ZoneInfo('Asia/Shanghai')",
         None),
    ]
    
    all_ok = True
    for name, imp, ver in deps:
        ok, msg = check_dependency(python_exe, name, imp, ver)
        print(f"  {msg}")
        if not ok:
            all_ok = False
    
    # 4. swisseph 空壳检测
    if all_ok:
        ok, out = run_python(python_exe, 
            "import swisseph as swe; v=swe.version; print(v); assert v != '0.0.0', 'empty shell'")
        if not ok:
            print(f"  ❌ swisseph 是空壳 (version=0.0.0)! 需要重装 pysweph")
            all_ok = False
    
    # 5. 星历表文件检查：查 engine 与 PyJHora 实际 set_ephe_path 的两个目录。
    #    旧版去 swisseph 的安装目录找 *.se1——那里本来就没有，于是每次都误报“未找到”。
    #    只出警告、不判失败：缺星历时 engine 仍能算（退回 Moshier 近似），不该卡住安装。
    print(f"\n── 星历表 (Ephemeris) ──")
    need = ("seas_18.se1", "semo_18.se1", "sepl_18.se1")
    ok, out = run_python(python_exe,
        "import jhora, os; print(os.path.join(os.path.dirname(jhora.__file__), 'data', 'ephe'))")
    jhora_ephe = out.splitlines()[-1].strip() if ok and out else None
    for label, ephe_dir in (("engine", os.path.join(SCRIPT_DIR, "ephe")), ("PyJHora", jhora_ephe)):
        if not ephe_dir:
            print(f"  ⚠️  {label} 星历目录无法定位")
            continue
        missing = [n for n in need if not os.path.isfile(os.path.join(ephe_dir, n))]
        if not missing:
            print(f"  ✅ {label} 星历齐全（{len(need)} 个 .se1）: {ephe_dir}")
        elif all(os.path.isfile(os.path.join(ephe_dir, n + ".txt")) for n in missing):
            print(f"  ⚠️  {label} 只有 .se1.txt（发布平台兼容名）: {ephe_dir}——运行 setup_env.py 会复制为 .se1")
        else:
            print(f"  ⚠️  {label} 缺 {'、'.join(missing)}: {ephe_dir}——会退回 Moshier 近似"
                  "（与 Swiss 星历差约 0.5″），运行 setup_env.py 补齐")
    
    # 6. 最小计算测试
    if all_ok:
        print(f"\n── 最小计算测试 (Gandhi 1869-10-02) ──")
        test_code = f"""
import sys
sys.path.insert(0, r"{SCRIPT_DIR}")
from engine import calculate_full_chart
chart = calculate_full_chart(1869, 10, 2, 7, 12, 21.6417, 69.6293, "Asia/Kolkata")
SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
sav = sum(chart['sav'].get(s,0) for s in SIGNS)
lagna = chart['lagna']['sign']
dk = chart['karakas']['dk_7k']
print(f"SAV={{sav}} Lagna={{lagna}} DK_7K={{dk}}")
assert sav == 337, f"SAV={{sav}} != 337"
print("PASS")
"""
        ok, out = run_python(python_exe, test_code)
        if ok and "PASS" in out:
            # 提取结果
            for line in out.split("\n"):
                if "SAV=" in line:
                    print(f"  ✅ {line.strip()}")
                    break
            print(f"  ✅ 计算引擎正常!")
        else:
            print(f"  ❌ 计算失败:")
            for line in out.split("\n")[-5:]:
                print(f"     {line}")
            all_ok = False
    
    # 7. 总结
    print(f"\n{'=' * 50}")
    if all_ok:
        print(f"  🎉 环境完全就绪!")
        print(f"  Python: {python_exe}")
        print(f"\n  AI调用时请使用:")
        print(f"  {python_exe} <your_script.py>")
    else:
        print(f"  ⚠️  环境有问题，修复方法:")
        print(f"  {python_exe} {os.path.join(SCRIPT_DIR, 'setup_env.py')}")
    print(f"{'=' * 50}")

if __name__ == "__main__":
    main()
