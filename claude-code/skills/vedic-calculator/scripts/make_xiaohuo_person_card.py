#!/usr/bin/env python3
"""Export a compact, copyable Xiaohuo personal chart card.

This adapter reads an already-generated ``structured_data.md`` and only
selects fields that are useful to the Xiaohuo text skills.  It never calls an
ephemeris library and never calculates a chart.  The canonical structured
data file remains unchanged.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys


PLANETS = (
    "Sun",
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
    "Rahu",
    "Ketu",
)


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().strip("`"))


def cells(line: str) -> list[str]:
    line = line.strip()
    if not line.startswith("|"):
        return []
    return [clean(part) for part in line.strip("|").split("|")]


def table_rows(body: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in body.splitlines():
        row = cells(line)
        if row and not all(re.fullmatch(r":?-{3,}:?", item) for item in row):
            rows.append(row)
    return rows


def section(text: str, pattern: str) -> str:
    match = re.search(
        rf"(?ms)^\s*{pattern}\s*$\n(.*?)(?=^\s*#{{2,}}\s|\Z)",
        text,
    )
    return match.group(1) if match else ""


def metadata(text: str) -> dict[str, str]:
    body = section(text, r"##\s*元信息")
    fence = re.search(r"(?ms)```(?:text|yaml|markdown)?\s*\n?(.*?)```", body)
    source = fence.group(1) if fence else body
    result: dict[str, str] = {}
    for line in source.splitlines():
        match = re.match(r"^\s*([^:：]+?)\s*[:：]\s*(.+?)\s*$", line.strip("`"))
        if match:
            result[clean(match.group(1))] = clean(match.group(2))
    return result


def meta_value(meta: dict[str, str], *names: str) -> str:
    folded = {key.casefold(): value for key, value in meta.items()}
    for name in names:
        if name.casefold() in folded:
            return folded[name.casefold()]
    compact = {re.sub(r"[\s_-]", "", key.casefold()): value for key, value in meta.items()}
    for name in names:
        key = re.sub(r"[\s_-]", "", name.casefold())
        if key in compact:
            return compact[key]
    return ""


def canonical_planet(value: str) -> str | None:
    value = clean(value).casefold()
    aliases = {
        "上升": "Lagna",
        "asc": "Lagna",
        "ascendant": "Lagna",
        "太阳": "Sun",
        "月亮": "Moon",
        "火星": "Mars",
        "水星": "Mercury",
        "木星": "Jupiter",
        "金星": "Venus",
        "土星": "Saturn",
        "罗喉": "Rahu",
        "计都": "Ketu",
    }
    if value in aliases:
        return aliases[value]
    for name in ("Lagna",) + PLANETS:
        if value == name.casefold() or value.startswith(name.casefold() + " "):
            return name
    if "north node" in value:
        return "Rahu"
    if "south node" in value:
        return "Ketu"
    return None


def parse_planets(text: str) -> dict[str, list[str]]:
    body = section(text, r"###\s*行星位置")
    result: dict[str, list[str]] = {}
    for row in table_rows(body):
        if not row:
            continue
        name = canonical_planet(row[0])
        if name:
            result[name] = row[1:5]
    return result


def parse_moon_nakshatra(text: str) -> tuple[str, str]:
    body = section(text, r"###\s*Nakshatra")
    for row in table_rows(body):
        if row and canonical_planet(row[0]) == "Moon":
            return (row[1] if len(row) > 1 else "", row[2] if len(row) > 2 else "")
    match = re.search(
        r"(?im)^\s*Moon\s+Nakshatra(?:/Pada)?\s*[:：]\s*([^;/；]+?)\s*(?:[/；,]\s*(?:Pada\s*[:：]?\s*)?(\d+))?\s*$",
        text,
    )
    return (match.group(1).strip(), (match.group(2) or "").strip()) if match else ("", "")


def parse_ul(text: str) -> tuple[str, str]:
    body = section(text, r"###\s*特殊点位")
    for row in table_rows(body):
        if row and row[0].casefold().startswith("ul"):
            return (row[1] if len(row) > 1 else "", row[2] if len(row) > 2 else "")
    match = re.search(
        r"(?im)^\s*UL(?:\s*\([^\n)]*\))?\s*[:：]\s*([A-Za-z\u4e00-\u9fff]+)(?:\s*[；;,]\s*(\d+)\s*宫?)?",
        text,
    )
    return (match.group(1), match.group(2) or "") if match else ("", "")


def parse_dk(text: str) -> str:
    match = re.search(r"(?im)^\s*DK\s*=\s*([^\n]+)", text)
    if match:
        return clean(match.group(1))
    body = section(text, r"###\s*Chara Karakas")
    for row in table_rows(body):
        if len(row) > 2 and row[1].casefold() == "dk":
            return row[2]
    return ""


def parse_current_dasha(text: str) -> tuple[str, str]:
    # The formatter emits an explicit current-status block.  Prefer it over
    # table heuristics: the AD table's heading contains “当前”, so scanning
    # every marked line can accidentally reuse the MD row as the AD value.
    status = re.search(r"(?ms)^当前状态\s*[:：]\s*\n?```(.*?)```", text)
    if status:
        body = status.group(1)
        md_match = re.search(
            r"(?im)^\s*Mahadasha\s*:\s*([^\n]+?)\s*$", body
        )
        ad_match = re.search(
            r"(?im)^\s*Antardasha\s*:\s*([^\n]+?)\s*$", body
        )
        md = clean(md_match.group(1)) if md_match else ""
        ad = clean(ad_match.group(1)) if ad_match else ""
        if md or ad:
            return md, ad

    md_body = section(text, r"###\s*Vimsottari Dasha")
    md = ""
    for row in table_rows(md_body):
        if len(row) >= 4 and "当前" in " ".join(row[:2]):
            md = f"{row[1]}（{row[2]} 至 {row[3]}）"
            break
    ad = ""
    # Current AD rows are marked in the relevant Antardasha table.  Keep the
    # first explicitly current row and do not infer a date from today's date.
    for line in text.splitlines():
        if not line.startswith("|") or "当前" not in line:
            continue
        row = cells(line)
        if len(row) >= 4 and ("←" in line or "当前" in row[0]):
            ad = f"{row[1]}（{row[2]} 至 {row[3]}）"
            break
    return md, ad


def parse_current_transit(text: str) -> tuple[str, list[tuple[str, str, str]]]:
    """Read the dated slow-planet transit table when the source contains it."""

    # This is a level-2 section containing level-3 subsections; the generic
    # ``section`` helper intentionally stops at any level-2-or-deeper heading,
    # so use a level-2-only boundary here.
    match = re.search(
        r"(?ms)^\s*##\s*当前过运位置.*?\s*$\n(.*?)(?=^\s*##\s|\Z)",
        text,
    )
    body = match.group(1) if match else ""
    date_match = re.search(
        r"(?im)^\s*>?\s*提取时间点\s*[:：]\s*(\d{4}-\d{2}-\d{2})",
        body,
    )
    date = date_match.group(1) if date_match else ""
    slow = re.search(
        r"(?ms)^\s*###\s*慢行星过运\s*$\n(.*?)(?=^\s*###\s|\Z)", body
    )
    if not slow:
        return date, []
    rows: list[tuple[str, str, str]] = []
    for row in table_rows(slow.group(1)):
        if len(row) >= 3 and row[0] in {"Saturn", "Jupiter", "Rahu", "Ketu"}:
            rows.append((row[0], row[1], row[2]))
    return date, rows


def infer_house_system(planets: dict[str, list[str]]) -> str:
    signs = {
        "aries": 0, "taurus": 1, "gemini": 2, "cancer": 3,
        "leo": 4, "virgo": 5, "libra": 6, "scorpio": 7,
        "sagittarius": 8, "capricorn": 9, "aquarius": 10, "pisces": 11,
    }
    lagna = planets.get("Lagna", [""])[0].casefold()
    if lagna not in signs:
        return "未确认（原资料未标明）"
    comparable = matches = 0
    for name in PLANETS:
        row = planets.get(name, [])
        if len(row) < 2 or row[0].casefold() not in signs:
            continue
        house_match = re.search(r"\d+", row[1])
        if not house_match:
            continue
        comparable += 1
        expected = (signs[row[0].casefold()] - signs[lagna]) % 12 + 1
        matches += expected == int(house_match.group(0))
    if comparable >= 5 and matches / comparable >= 0.8:
        return "整宫制（按 D1 星座/宫位映射确认）"
    return "未确认（原资料未标明）"


def display_row(name: str, row: list[str] | None) -> str:
    row = row or []
    values = [(row[index] if len(row) > index else "—") or "—" for index in range(4)]
    if values[3].casefold() in {"r", "逆行", "retrograde"}:
        values[3] = "逆行"
    return f"{name}：" + "；".join(values[:3]) + (f"；{values[3]}" if values[3] != "—" else "")


def build_card(text: str, label: str, include_birth: bool = False) -> str:
    meta = metadata(text)
    planets = parse_planets(text)
    moon_name, moon_pada = parse_moon_nakshatra(text)
    ul_sign, ul_house = parse_ul(text)
    md, ad = parse_current_dasha(text)
    transit_date, transits = parse_current_transit(text)
    ayanamsa = meta_value(meta, "Ayanamsa", "岁差", "Ayanamsa方法") or "未提供"
    precision = meta_value(meta, "有效精度", "时间精度") or "未提供"
    source = meta_value(meta, "读盘方式", "数据来源") or "已计算盘面资料"
    lines = [
        "盘面资料卡版本：xiaohuo-person-v1",
        f"资料归属：{label}",
        f"黄道口径：恒星黄道；Ayanamsa：{ayanamsa}",
        f"宫制：{infer_house_system(planets)}",
        f"数据精度：{precision}",
        f"数据来源：{source}",
    ]
    if include_birth:
        date = meta_value(meta, "出生日期", "birth date")
        time = meta_value(meta, "出生时间", "birth time")
        place = meta_value(meta, "出生地点", "地点", "birth place")
        if date or time or place:
            lines.append("出生资料：" + "；".join(value for value in (date, time, place) if value))
    lines.append("")
    lines.append(display_row("Lagna（上升）", planets.get("Lagna")))
    for name in PLANETS:
        lines.append(display_row(name, planets.get(name)))
    lines.append(f"Moon Nakshatra/Pada：{moon_name or '未提供'} / {moon_pada or '未提供'}")
    ul = ul_sign or "未提供"
    if ul_house:
        ul += f"；{ul_house}宫"
    lines.append(f"UL：{ul}")
    lines.append(f"DK：{parse_dk(text) or '未提供'}")
    lines.append(f"当前 MD/AD：{md or '未提供'} / {ad or '未提供'}")
    if transits:
        lines.append(f"当前过运（提取时间：{transit_date or '未提供'}）：")
        lines.extend(f"{planet}：{sign}；{house}" for planet, sign, house in transits)
    lines.append("备注：这是一段由已计算盘面整理出的可复制资料，不是新的排盘结果。")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="把 structured_data.md 整理成 Xiaohuo 个人资料卡。只读，不排盘。")
    parser.add_argument("structured_data", type=Path)
    parser.add_argument("--label", default="本人", help="资料归属名称，默认：本人")
    parser.add_argument("--include-birth", action="store_true", help="同时输出出生日期、时间和地点")
    parser.add_argument("-o", "--output", type=Path, help="输出文件；不填则打印到屏幕")
    args = parser.parse_args(argv)
    try:
        text = args.structured_data.read_text(encoding="utf-8-sig")
    except OSError as exc:
        print(f"错误：无法读取 {args.structured_data}: {exc}", file=sys.stderr)
        return 2
    card = build_card(text, args.label, include_birth=args.include_birth)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(card, encoding="utf-8")
    else:
        sys.stdout.write(card)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
