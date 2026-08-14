# Japanese runtime layer: Calculator

Read this file only when `client_language` is Japanese. This is a localization
layer, not a calculation specification. `SKILL.md`, scripts, schemas, validation
rules, and artifact names remain authoritative.

## Register

- Use natural Japanese polite style (`です・ます`). Sound calm and technically
  confident, not ceremonial or mystical.
- Ask only for missing inputs. Keep dates in `YYYY-MM-DD` and time in 24-hour
  notation when confirming data, even if the user wrote another format.
- State the strongest supported result first. Do not turn an astronomy or data
  limitation into generic fortune-telling language.
- Do not infer gender, nationality, calendar system, time zone, or daylight-saving
  status from a name or place name.

## Stable terminology

| Canonical term | Japanese client wording |
|---|---|
| Vedic astrology / Jyotish | ヴェーダ占星術（Jyotish） |
| natal chart | 出生図 |
| Lagna / Ascendant | ラグナ（Lagna／上昇点） |
| Rashi / D1 | ラーシ図（Rashi／D1） |
| divisional chart / Varga | 分割図（Varga） |
| Navamsha / D9 | ナヴァーンシャ（Navamsha／D9） |
| Dasha | ダシャー（Dasha／時期体系） |
| Vimshottari Dasha | ヴィムショッタリ・ダシャー |
| Nakshatra | ナクシャトラ（月宿） |
| Ayanamsa | アヤナーンシャ（歳差補正） |
| structured_data.md | `structured_data.md`（標準チャートデータ） |

Keep `MD/AD/PD`, `SAV/BAV`, `Shadbala`, planet codes, filenames, JSON keys, and
schema headings unchanged. Explain them once in Japanese when client-visible.

## Intake templates

When birth data are missing, ask in this order:

1. `生年月日（西暦）`
2. `出生時刻（できれば母子手帳などに記録された時刻）`
3. `出生地（市区町村・国）`
4. only when needed, `時刻の情報源と確かさ`

Confirmation example:

> 次の出生情報で計算します。日付：1990-01-01、時刻：08:00、出生地：
> Tokyo, Japan。時刻または場所に修正があれば、計算前にお知らせください。

Progress wording should describe the real operation, for example:

- `出生地とタイムゾーンを確認しています。`
- `ラーシ図と分割図を計算しています。`
- `ダシャー、Shadbala、SAV/BAV の整合性を検証しています。`

## Completion template

Lead with whether calculation and validation succeeded, then give the saved
artifact and the next valid route:

> 出生図の計算と検証が完了しました。標準データは
> `structured_data.md` に保存されています。続けて総合分析を行う場合は、
> このデータを `vedic-reader` の検証または選択済み Core に渡します。

If the exact birth time is materially uncertain, say `出生時刻の精度が分割図に影響する
可能性があります` once and route according to `SKILL.md`; do not invent a usable
precision range.

## HTML

When this run later enters the core HTML builder, Japanese client-facing reports
must use `report_builder.py --lang ja`. This changes the HTML shell only, never the
underlying Markdown artifacts or chart data.
