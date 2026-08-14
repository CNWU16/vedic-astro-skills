# Japanese runtime layer: Reader

Read this file only when `client_language` is Japanese. It localizes Japanese
intake, extraction notices, pre-validation wording, feedback labels, and report
prose. It never changes the data contract, validation rules, prediction-selection
procedure, feedback scoring, hit-rate calculation, or downstream routing in
`SKILL.md`.

## Register

- Use clear `です・ます` language. Distinguish extracted facts, calculated facts,
  validation results, and interpretation.
- Never present OCR uncertainty as chart uncertainty. State which field or source
  is unreadable and what replacement input is needed.
- When no chart file exists, make direct calculation from birth details the first
  and simplest route; PDF or screenshots remain optional.
- Keep pre-validation statements concrete and falsifiable. Do not soften or rewrite
  them after feedback.

## Stable terminology

| Canonical term | Japanese client wording |
|---|---|
| chart import | チャートの読み込み |
| extraction | データ抽出 |
| normalization | 形式の標準化 |
| validation | 整合性検証 |
| source field | 参照元の項目 |
| natal chart | 出生図 |
| Lagna / Ascendant | ラグナ（Lagna／上昇点） |
| Rashi / D1 | ラーシ図（D1） |
| divisional chart | 分割図 |
| structured_data.md | `structured_data.md`（標準チャートデータ） |
| verified | 検証済み |
| needs rectification | 出生時刻修正が必要 |

Keep schema headings, status markers, `A-H`, `R1`, feedback scores, hit-rate
formulas, filenames, CLI flags, and canonical planet or sign identifiers unchanged.

## Entry template

When the skill is triggered without chart data, use a natural Japanese menu:

> ヴェーダ占星術のチャートを準備します。いちばん簡単なのは、生年月日・
> 正確な出生時刻・出生地を送る方法です。内蔵計算器で出生図を作成し、
> そのまま検証と分析へ進めます。すでに JHora などの PDF、画像、テキストが
> ある場合は、そのファイルを読み込むこともできます。

Ask only for the chosen route's missing inputs.

## Progress and validation wording

Useful progress labels include:

- `参照元から惑星・ハウス・分割図データを抽出しています。`
- `標準 schema に合わせて項目を整理しています。`
- `時刻、ラグナ、惑星位置、ダシャーの整合性を確認しています。`

Validation result template:

> 抽出と整合性検証が完了しました。`structured_data.md` は下流分析に使用
> できます。未確定項目がある場合は、項目名・理由・影響範囲をここに明記します。

## Feedback labels

When the workflow requests feedback, render the allowed canonical categories as:

- `准` → `当てはまる`
- `部分准` → `一部当てはまる`
- `不准` → `当てはまらない`

Store and calculate with the canonical labels required by `SKILL.md`; Japanese is
only the client-facing label. User confirmation never retroactively raises the
original prediction confidence, and contradiction never authorizes post-hoc rescue.
