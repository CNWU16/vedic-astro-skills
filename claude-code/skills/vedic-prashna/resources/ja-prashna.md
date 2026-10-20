# Japanese runtime layer: Prashna

Read this file only when `client_language` is Japanese. This layer localizes the
question intake, terminology, judgment wording, and report labels. It never changes
the standard-layer-first rule, the isolation of Tajika and KP, question eligibility,
calculation, evidence ledger, judgment authority, or follow-up boundaries in
`SKILL.md`.

## Register

- Use concise, calm `です・ます` prose. Prashna answers one concrete matter; do not
  inflate it into a natal life reading.
- Lead with the story in ordinary Japanese: a headline and subtitle written for this
  specific matter that make the direction unmistakable, then the body (current
  situation → driving forces → obstacles → signs of a turn → rough timing → what the
  user can do now), then the auditable reasons.
- Do not show the internal tier names `偏成/持平/偏不成` or verdict words such as
  `成立する／しない`, `必ず`, `絶対`, `見込みなし` in the headline, subtitle, or body.
  In the audit section translate the tiers as `成立寄り`, `拮抗`, `不成立寄り`, with
  strength `順調／抵抗あり` and `明確／転機あり`. When a favourable direction came from
  rubric §4.1 preponderance, describe it as `困難を経て進む方向` and name where the
  resistance lies.
- Do not use divinatory theatrics, fear language, or absolute guarantees.

## Stable terminology

| Canonical term | Japanese client wording |
|---|---|
| Prashna | プラシュナ（質問時刻図） |
| horary chart | 質問時刻図 |
| querent | 質問者 |
| quesited | 質問対象 |
| significator | 表示体（significator） |
| house lord | ハウス支配星 |
| applying contact | 接近中のコンタクト |
| separating contact | 分離後のコンタクト |
| judgment ledger | 判定根拠表 |
| Tajika | タージカ（Tajika） |
| KP 1-249 | KP 1–249 独立方式 |

Keep filenames, stack names, rule IDs, chart codes, JSON keys, timestamps, scores,
and evidence citations unchanged.

## Question intake

Ask for the minimum required operational inputs:

1. `判断したい具体的な質問を一つ`
2. `その質問が確定した日時（秒まで分かれば秒まで）`
3. `その時にいた市区町村・国`

Eligibility clarification example:

> この質問で「成立」とみなす観察可能な結果を一つに絞ります。単なる連絡、
> 交渉開始、契約成立のどれを判定したいですか。

Do not request a KP number unless the selected optional KP path is validly activated.
Do not imply that Tajika or KP can revise the classical standard result by voting
with it.

## Judgment rendering

Use this order where the required artifact permits:

1. 見出し（この件に即した一文）
2. サブ見出し（鍵になる点と時期の目安）
3. 本文（現状 → 推進力 → 阻害要因 → 転機の兆し → 時期の目安 → 今できること）
4. 確認欄（範囲、内部区分、判定根拠表、時期、Moon の事実、体系の境界）

Render the standard timing overlay (`timing_overlay.md`) only for `偏成` or `持平`:
use `目安として…` for `偏成` and a conditional such as `順調に進めば、目安として…`
for `持平`. For `偏不成`, give no timing; say once in direct Japanese what change
would make the question worth asking again. Do not substitute a natal Dasha, a
generic transit date, or a Tajika/KP date for it.
