#!/usr/bin/env python3
"""build_prashna_data.py — Prashna 提问盘起盘链路

调共享 vedic-calculator/scripts/engine.py 的 calculate_full_chart(提问时刻)，再由
Prashna 专用白名单 formatter 组装 structured_prashna.md，写入
prashna_<yyyymmdd_HHMM>_<label>/ 独立目录。

沙箱化硬约束(vedic-prashna/SKILL.md §沙箱化硬约束):
  1. 只读复用共享 engine，不调用本命 formatter，不改任何共享代码。
  2. 产物名 structured_prashna.md(与本命 structured_data.md 严格区分)。
  3. 产物路径 prashna_<yyyymmdd_HHMM>_<label>/(独立子目录，不写本命根)。
  4. 不加任何 Tajika/KP/异体系字段。

默认标准层:
  - 仅输出 resources/standard-layer.md 的字段白名单。
  - 不输出本命 Dasha、Chara Karaka、SAV/BAV、分盘、Yoga 或过运。
  - 当前不提供生产级 Prashna 时间窗。

用法:
    python build_prashna_data.py \\
        --datetime "2026-07-11 15:30"  # 提问时刻(本地时区)，或 "now" \\
        --lat 30.667 --lon 104.067      # 提问地(度，正=北/东) \\
        --tz "Asia/Shanghai"            # 提问地时区 \\
        --question "这份 offer 该不该接?" \\
        --label offer-decide            # 问题短标签(a-z0-9-, 1-30) \\
        [--out-parent .]                # 独立子目录的父目录(默认 CWD)
"""
import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


# --- 复用共享 vedic-calculator(只读调用) ---
_HERE = Path(__file__).resolve().parent           # vedic-prashna/scripts/
_CALC_SCRIPTS = _HERE.parent.parent / "vedic-calculator" / "scripts"
if not _CALC_SCRIPTS.exists():
    raise RuntimeError(
        f"[FATAL] 未找到共享 vedic-calculator/scripts: {_CALC_SCRIPTS}\n"
        f"沙箱化硬约束 #1 要求 Prashna 复用共享 engine，请检查 skills 目录布局。"
    )
if str(_CALC_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_CALC_SCRIPTS))

from engine import calculate_full_chart      # noqa: E402
from format_prashna_standard import format_standard_layer  # noqa: E402

# 沙箱内 Moon 吠陀动向计算(不下沉 engine，见 calc_moon_vedic.py 顶注)
from calc_moon_vedic import compute as compute_moon_vedic  # noqa: E402
from calc_moon_vedic import format_moon_section            # noqa: E402

LABEL_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,29}$")


def parse_args():
    ap = argparse.ArgumentParser(description="Prashna 提问盘起盘")
    ap.add_argument("--datetime", required=True,
                    help='提问时刻，格式 "YYYY-MM-DD HH:MM"，或 "now"')
    ap.add_argument("--lat", type=float, required=True, help="提问地纬度(度，正=北)")
    ap.add_argument("--lon", type=float, required=True, help="提问地经度(度，正=东)")
    ap.add_argument("--tz", required=True, help='提问地时区，如 "Asia/Shanghai"')
    ap.add_argument("--question", required=True, help="具体问题(单一可判定)")
    ap.add_argument("--label", required=True,
                    help="问题短标签(kebab-case, 1-30 字符 [a-z0-9-])")
    ap.add_argument("--out-parent", default=".",
                    help="独立子目录的父目录(默认 CWD)")
    args = ap.parse_args()

    if not LABEL_RE.match(args.label):
        ap.error(f"--label 必须匹配 {LABEL_RE.pattern}: 收到 {args.label!r}")

    try:
        local_zone = ZoneInfo(args.tz)
    except ZoneInfoNotFoundError:
        ap.error(f"--tz 不是可用的 IANA 时区: {args.tz!r}")

    if args.datetime.strip().lower() == "now":
        dt = datetime.now(local_zone).replace(tzinfo=None)
    else:
        try:
            dt = datetime.strptime(args.datetime, "%Y-%m-%d %H:%M")
        except ValueError as e:
            ap.error(f"--datetime 格式应为 'YYYY-MM-DD HH:MM' 或 'now': {e}")

    args.dt = dt
    return args


def build_prashna_header(
    dt, lat, lon, tz, question, label, chart_ayanamsa, dst_info
):
    lines = []
    lines.append("## 元信息\n")
    lines.append("```")
    lines.append("盘类型: Prashna(提问盘/时盘) — 独立生态位，不与本命混")
    lines.append(f"提问日期: {dt.strftime('%Y-%m-%d')}")
    lines.append(f"提问时间: {dt.strftime('%H:%M')}")
    lines.append(f"提问地点: ({lon:.3f}, {lat:.3f})")
    lines.append(f"时区: {tz}")
    lines.append("时间精度: 精确到分钟(用户报时或本机时刻)")
    lines.append("读盘方式: vedic-calculator 直接起 Prashna Kundali")
    lines.append(f"Ayanamsa: True Chitrapaksha(Lahiri 系) ({chart_ayanamsa:.4f}°)")
    if dst_info and dst_info.get('is_dst'):
        lines.append(
            f"夏令时: ⚠️ 提问时刻处于当地夏令时期间(UTC 偏移 {dst_info['utc_offset']})"
        )
    lines.append("Node模式: Mean Node")
    lines.append("默认标准层: Shatpanchasika-rooted + KN Rao/Bhavan compatibility")
    lines.append("生产级择时: 未启用")
    lines.append("```\n")

    lines.append("## 提问信息\n")
    lines.append("```")
    lines.append(f"具体问题: {question}")
    lines.append(f"问题短标签: {label}")
    lines.append("求问者背景: [Prashna 分析阶段禁读盘主背景，此处留空]")
    lines.append("占卜类别: [由判读时依据 question 映射，见 resources/house-karaka-map.md]")
    lines.append("```\n")
    return "\n".join(lines)


def main():
    args = parse_args()

    # 1. 起盘(复用共享 engine，只读调用)
    chart = calculate_full_chart(
        args.dt.year, args.dt.month, args.dt.day,
        args.dt.hour, args.dt.minute,
        args.lat, args.lon, args.tz,
    )

    # 2. 由 Prashna 专用 formatter 输出白名单字段；不消费共享 natal formatter。
    data_section = format_standard_layer(chart)

    # 3. 组装 Prashna 专用头部
    head = build_prashna_header(
        args.dt, args.lat, args.lon, args.tz, args.question, args.label,
        chart['ayanamsa'], chart.get('dst_info'),
    )

    # 4. Moon 当前事实(沙箱内计算，不生成全局成败或时间窗)
    moon_data = compute_moon_vedic(chart, args.dt, args.tz)
    moon_section = format_moon_section(moon_data)

    final_md = head + "\n" + data_section + "\n\n---\n\n" + moon_section

    # 5. 写入独立子目录。Tajika 与 KP 不在标准 builder 中导入或追加：
    #    Tajika 由 build_tajika_overlay.py 在 Phase 2 选定主星后生成；
    #    KP 由独立的 build_kp_horary.py 生成。
    subdir_name = f"prashna_{args.dt.strftime('%Y%m%d_%H%M')}_{args.label}"
    out_dir = Path(args.out_parent).resolve() / subdir_name
    out_dir.mkdir(parents=True, exist_ok=True)
    # 产物名严格区分本命根 structured_data.md
    out_path = out_dir / "structured_prashna.md"
    out_path.write_text(final_md, encoding='utf-8')

    print(f"[OK] Prashna 盘已生成:")
    print(f"     目录: {out_dir}")
    print(f"     文件: structured_prashna.md")
    print(f"     提问时刻: {args.dt.strftime('%Y-%m-%d %H:%M')} ({args.tz})")
    print(f"     具体问题: {args.question}")


if __name__ == "__main__":
    main()
