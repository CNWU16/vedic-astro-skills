#!/usr/bin/env python3
"""judge_prashna_standard.py — 即时盘标准层判定（读取象单，出成事账、内部档、能力层、行动链、限定语）

模型取象、脚本计数（2026-10-29 重建）：模型按 question-decomposition.md 写取象单 prashna_plan.json，
本脚本读盘面事实与取象单，写 prashna_verdict.json 与 prashna_verdict.md（判读单核对区直接引用）。
规则只在 prashna_rules.py 实现一份；本脚本不读问题原文，不读其他 prashna 目录。

档只按所给的提问时刻与地点定（产品取消息到达服务器的时刻）。另在前后各取一盘（只给城市名 ±60 秒，
精确经纬度 ±30 秒），本题账本随之改变的只在核对区"输入提示"记一行，不改档，不进给用户看的部分。

用法:
    python judge_prashna_standard.py \\
        --datetime "2026-10-28 15:24:00.696168" --lat 30.27 --lon 120.15 --tz "Asia/Shanghai" \\
        --plan prashna_20261028_152400_private-meeting/prashna_plan.json \\
        --out-dir prashna_20261028_152400_private-meeting
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
from datetime import timedelta
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_CALC = _HERE.parent.parent / "vedic-calculator" / "scripts"
if str(_CALC) not in sys.path:
    sys.path.insert(0, str(_CALC))

from prashna_rules import DIRECTION_TEXT, Plan, judge  # noqa: E402
from prashna_time import calculate_prashna_chart, format_wall_time, parse_local_datetime  # noqa: E402

WINDOW = {"city": 60, "exact": 30}


def charts(dt, lat, lon, tz, location):
    with contextlib.redirect_stdout(io.StringIO()):
        base = calculate_prashna_chart(dt, lat, lon, tz)
        w = WINDOW[location]
        variants = [(f"−{w} 秒", calculate_prashna_chart(dt - timedelta(seconds=w), lat, lon, tz)),
                    (f"+{w} 秒", calculate_prashna_chart(dt + timedelta(seconds=w), lat, lon, tz))]
    return base, variants


def render(v, plan, dt):
    """核对区引用的 markdown：取象、账本、内部档、能力层、限定语、行动链、输入提示。"""
    L = ["## 判定（judge_prashna_standard.py）\n", f"提问时刻 {format_wall_time(dt)}；事项 {v['matter']}，"
         f"事项宫 {v['matter_house']}，支持级 {v['level']}。\n"]
    if plan.keywords:
        L.append("**取象**：" + "；".join(
            f"{k['word']} → {'、'.join(map(str, k.get('houses', ()))) or '—'} 宫"
            f"{'；' + '、'.join(k.get('planets', ())) if k.get('planets') else ''}（{k['polarity']}，{k['source']}）"
            for k in plan.keywords) + (f"；所需征象星 {'、'.join(plan.needed_planets)}" if plan.needed_planets else "") + "\n")
    if v["matter"] == "描述":
        return "\n".join(L + render_describe(v))
    L.append("| rule_id | 支持级 | 适用理由 | 原始证据 | 方向 | 计分 |")
    L.append("|---|---|---|---|---|---:|")
    for e in v["ledger"]:
        d = DIRECTION_TEXT[e["direction"]] + (f"；第二读法 {DIRECTION_TEXT[e['alt']]}" if e["alt"] else "")
        extra = "；".join(x for x in (e["note"], e["excluded"]) if x)
        L.append(f"| `{e['rule_id']}` | {e['level']} | {e['reason']} | {e['evidence']}{'（' + extra + '）' if extra else ''} | "
                 f"{'不入账' if e['excluded'] else d} | {e['score']:+d} |")
    L.append(f"\n**合计**：{v['sum']:+d}\n")
    L.append(f"**内部档**：{v['tier']}·{v['strength']}" + (f"（两支：{'／'.join(v['branches'])}）" if v["branches"] else "") + "\n")
    ab = v["ability"]
    L.append(f"**能力层**：指标星 {ab['planet']}（{ab['house']} 宫主），折损项 {'、'.join(ab['factors']) or '无'}，"
             f"救应 {'、'.join(ab['rescue']) or '无'} → {ab['verdict']}"
             + (f"；按需减项：{'；'.join(ab['dropped'])}" if ab["dropped"] else "") + "\n")
    for q in v["qualifiers"]:
        L.append(f"**限定语·{q['name']}**：{q['result']}（{q['basis']}）\n")
    if v["chain"]:
        c = v["chain"]
        L.append(f"**行动链**：行动者 {c['actor']} 宫；① 起意 {'；'.join(c['start']) or '—'}；② 行动 {c['move'] or '—'}；"
                 f"③ 指向你 {'；'.join(c['point']) or '—'}；④ 严重受损 {'、'.join(c['weak']) or '—'} → {c['verdict']}"
                 "（不进合计）\n")
    if v["sensitive"]:
        L.append("**输入提示**（不改档）：" + "；".join(f"{s['at']} 时 {'、'.join(s['rules'])} 改变，档为 {s['tier']}"
                                              for s in v["sensitive"])
                 + "。只记在这里，判读单不提。\n")
    why = f"（必要条件 {'、'.join(v['condition_failed'])} 不成立，按这个条件不能）" if v["condition_failed"] else ""
    L.append(f"**时间副层**：{'不运行' + why if v['timing'] == 'none' else '运行，--mode ' + v['timing']}\n")
    return "\n".join(L)


def render_describe(v):
    """描述型：指标星能力与连接、影响者逐颗事实、关键词落点、M-XIV.117；不建账、不定档、不给时间。"""
    d, ab = v["describe"], v["ability"]
    L = ["**描述型**：不建成事账、不定档、不给时间；判读单讲局面与相处的样子，不预言结果（`judgment-writing.md` 第 4 节）。\n",
         f"**指标星**：{ab['planet']}（{ab['house']} 宫主），折损项 {'、'.join(ab['factors']) or '无'}，"
         f"救应 {'、'.join(ab['rescue']) or '无'} → {ab['verdict']}；与 Lagna 主 {d['link']}\n",
         "| 位置 | 方式 | 行星 | 从 Lagna 所管 | 吉凶标签 | D1 尊贵度 | 燃烧／逆行 | 措辞点到 |",
         "|---|---|---|---|---|---|---|---|"]
    for r in d["influences"]:
        cr = "、".join(x for x, on in (("燃烧", r["combust"]), ("逆行", r["retro"])) if on) or "—"
        L.append(f"| {r['at']} | {r['how']} | {r['planet']} | {'、'.join(map(str, r['rules'])) or '—'} | {r['label']} | "
                 f"{r['dignity']} | {cr} | {'；'.join(r['hits'])} |")
    if not d["influences"]:
        L.append("| — | — | 无同宫、照射之星 | — | — | — | — | — |")
    for k in d["keywords"]:
        L.append(f"\n**关键词落点·{k['word']}**：{k['result']}（{k['basis']}）")
    m = d["M-XIV.117"]
    L.append(f"\n**`M-XIV.117`**（Moon 或 Venus 与凶星同落 7、4 宫，与女性起争执；问相处时读）：{m['result']}（{m['basis']}）\n")
    if v["chain"]:
        c = v["chain"]
        L.append(f"**行动链**：行动者 {c['actor']} 宫；① 起意 {'；'.join(c['start']) or '—'}；② 行动 {c['move'] or '—'}；"
                 f"③ 指向你 {'；'.join(c['point']) or '—'}；④ 严重受损 {'、'.join(c['weak']) or '—'} → {c['verdict']}\n")
    L.append("**时间副层**：不运行（描述型）\n")
    return L


def main():
    ap = argparse.ArgumentParser(description="Prashna 标准层判定")
    ap.add_argument("--datetime", required=True)
    ap.add_argument("--lat", type=float, required=True)
    ap.add_argument("--lon", type=float, required=True)
    ap.add_argument("--tz", required=True)
    ap.add_argument("--plan", required=True, help="取象单 prashna_plan.json")
    ap.add_argument("--out-dir", required=True, help="当前 prashna_* 目录")
    a = ap.parse_args()
    out = Path(a.out_dir)
    if not (out / "structured_prashna.md").exists():
        ap.error(f"{out} 下没有 structured_prashna.md；先运行 build_prashna_data.py")
    plan = Plan.from_dict(json.loads(Path(a.plan).read_text(encoding="utf-8")))
    dt = parse_local_datetime(a.datetime, a.tz)
    base, variants = charts(dt, a.lat, a.lon, a.tz, plan.location)
    v = judge(base, plan, variants=variants)
    (out / "prashna_verdict.json").write_text(json.dumps(v, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "prashna_verdict.md").write_text(render(v, plan, dt), encoding="utf-8")
    if v["matter"] == "描述":
        print(f"[OK] 描述型：不定档，只出事实\n     {out / 'prashna_verdict.md'}")
        return
    print(f"[OK] 判定：{v['tier']}·{v['strength']}（合计 {v['sum']:+d}）"
          + (f"；行动链 {v['chain']['verdict']}" if v["chain"] else "")
          + f"\n     {out / 'prashna_verdict.md'}")


if __name__ == "__main__":
    main()
