# Japanese runtime layer: Prashna

Read this file only when `client_language` is Japanese. This layer localizes the
question intake, terminology, judgment wording, and report labels. It never changes
the standard-layer-first rule, the isolation of Tajika and KP, question eligibility,
calculation, evidence ledger, judgment authority, or follow-up boundaries in
`SKILL.md`.

## Register

- Use concise, calm `です・ます` prose. Prashna answers one concrete matter; do not
  inflate it into a natal life reading.
- Lead with the current judgment in ordinary Japanese, then show the auditable
  reasons and the strongest contrary signal.
- Translate `成/悬/不成` semantically, not mechanically. Prefer
  `成立・実現の方向`, `保留・未決着`, or `現時点では不成立の方向`, followed by
  one sentence explaining what that means for the user's observable question.
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

1. `現在の判定`
2. `判定対象と成立条件`
3. `主要な成立材料`
4. `主要な阻害材料`
5. `Moon の役割`
6. `結論の範囲`

If event timing is not authorized or not supported at production resolution, say
so once in direct Japanese. Do not substitute a natal Dasha, Moon ingress, or a
generic transit date.
