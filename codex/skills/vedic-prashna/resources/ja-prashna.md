# Japanese runtime layer: Prashna

Read this file only when `client_language` is Japanese. This layer localizes the
question intake, terminology, judgment wording, and report labels. It never changes
the standard-layer-first rule, the isolation of Tajika and KP, question eligibility,
calculation, evidence ledger, judgment authority, or follow-up boundaries in
`SKILL.md`.

## Register

- Use concise, calm `です・ます` prose. Prashna answers one concrete matter; do not
  inflate it into a natal life reading.
- Lead with the story in ordinary Japanese: a headline written for this specific matter
  that makes the direction unmistakable, a short summary paragraph, then a chart-based
  reading that follows `judgment-writing.md` (classical terms such as Lagna, Bhava,
  Graha, Drishti, Kendra are welcome, each glossed in Japanese on first use), then the
  auditable reasons. The writing guide never changes the tier set by the ledger.
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
2. 要約（方向、鍵になる点、時期の目安を短い一段落で）
3. 盤面の読み（盤面の特徴で小見出しを立て、質問者の側・事柄や相手の側・両者の間・心境・
   古法の合算を、それぞれ盤の事実に沿って数段落で）
4. 時期（偏不成なら、どんな変化があれば改めて問えるか）
5. 今できること
6. 確認欄（範囲、内部区分、判定根拠表と背景事実、時期、Moon の事実、体系の境界）

Render the standard timing overlay (`timing_overlay.md`) only for `偏成` or `持平`:
use `目安として…` for `偏成` and a conditional such as `順調に進めば、目安として…`
for `持平`. For `偏不成`, give no timing; say once in direct Japanese what change
would make the question worth asking again. Do not substitute a natal Dasha, a
generic transit date, or a Tajika/KP date for it.
