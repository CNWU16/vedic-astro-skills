# Japanese runtime layer: Standard Core

Read this file only when `client_language` is Japanese. It is the Japanese
localization layer for the standard Core. It does not add, remove, reorder, or
merge any P1-P12 audit, divisional check, house diagnosis, life-area section,
phase gate, file, score, evidence item, or report-lineage rule in `SKILL.md`.

## Register

- Use natural, composed `です・ます` prose. Sound like an experienced astrologer
  explaining a chart across a table, not a translated manual or a legal notice.
- Lead each client-facing section with the strongest chart-supported answer.
  Explain the chart basis afterward and name the material limitation once.
- Avoid repeated sentence openings such as `あなたは…人です`. Prefer
  `この出生図で最も強い軸は…`, `この配置は…として表れやすいです`, and
  `反対材料まで含めると…が残ります`.
- Preserve uncertainty without becoming evasive. Use `強く示されます`,
  `有力です`, `条件付きで出やすいです`, or `このデータ精度では時期をここまで
  絞れません` according to the evidence actually available.
- Do not use fatalistic wording such as `必ず起こる`, `運命で決まっている`, or
  `逃れられない` unless the source literally requires quotation; never introduce
  it as the model's own conclusion.

## Stable terminology

| Canonical term | Japanese client wording |
|---|---|
| Vedic astrology / Jyotish | ヴェーダ占星術（Jyotish） |
| natal chart | 出生図 |
| Lagna / Ascendant | ラグナ（Lagna／上昇点） |
| Rashi / sign | ラーシ（Rashi／サイン） |
| house / Bhava | ハウス（Bhava） |
| house lord | ハウス支配星 |
| Graha | 惑星（Graha） |
| dignity | 品位（dignity） |
| exaltation / debilitation | 高揚／減衰（exaltation／debilitation） |
| functional benefic / malefic | 機能的吉星／機能的凶星 |
| divisional chart / Varga | 分割図（Varga） |
| Navamsha / D9 | ナヴァーンシャ（D9） |
| yoga | ヨーガ（特定の惑星配置） |
| Dasha | ダシャー（時期体系） |
| transit / Gochar | トランジット（Gochar） |
| Shadbala | シャドバラ（惑星強度） |
| Ashtakavarga | アシュタカヴァルガ（SAV/BAV） |
| counterevidence | 反対材料 |
| confidence | 確信度 |

Keep `P1-P12`, `D1/D9/D10`, `MD/AD/PD`, `SAV/BAV`, technical codes, evidence
citations, filenames, schema headings, and table parameters unchanged.

## Client-facing section labels

Use Japanese labels around required technical content where the artifact permits:

- `出生図の中心テーマ`
- `惑星別監査`
- `分割図による照合`
- `ハウス別診断`
- `仕事と社会的役割`
- `恋愛・結婚・対人関係`
- `家族・住環境・基盤`
- `財務傾向と資源管理`
- `学習・信念・長期的成長`
- `健康に関わる生活傾向`
- `ダシャーと転機`
- `技術付録`

These are client labels only. Do not rename canonical artifact files or schema
headings.

## Interpretation pattern

For each explanatory block:

1. State the strongest conclusion in one natural paragraph.
2. Explain the two or three decision-relevant chart signals without hiding
   required audit tables elsewhere.
3. Name the strongest contrary signal and how it limits, redirects, or fails to
   overturn the conclusion.
4. Close with the observable life expression or practical implication authorized
   by the selected phase.

Do not invent a fixed paragraph count or evidence quota; the pattern is an order
of presentation, not a new scoring rule.

## Q&A and HTML

In valid Core Q&A, answer the question first, then show the smallest complete
evidence chain needed by the Core rules. Do not restart the full report or ask the
Standard/Pro selection again after lineage is locked.

For a Japanese client-facing HTML report, run `report_builder.py --lang ja`. The
builder localizes the cover, contents, section labels, footer, document language,
and Japanese font stack only. Markdown evidence and report lineage stay unchanged.
