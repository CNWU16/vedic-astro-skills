# Japanese runtime layer: Rectifier

Read this file only when `client_language` is Japanese. It localizes event intake,
questionnaire wording, candidate explanations, and the final report. It never
changes candidate generation, event and trait evidence roles, D1/D9/D10 transition
checks, scoring, thresholds, settlement, precision, files, or phase order in
`SKILL.md`.

## Register

- Use patient, precise `です・ます` language. Explain why a question separates
  candidates without exposing the user to unnecessary calculation noise.
- Keep `現在の最良推定`, `確認済み`, and `確信度` distinct. Do not translate a
  leading candidate into a confirmed exact time.
- Never promise minute-level accuracy beyond the actual divisional transition and
  astronomical resolution.
- Ask one discriminating question at a time when the workflow requires sequential
  questioning. Do not turn the intake into a generic biography interview.

## Stable terminology

| Canonical term | Japanese client wording |
|---|---|
| birth time rectification | 出生時刻修正 |
| candidate | 候補時刻 |
| scan interval | 探索区間 |
| transition boundary | 分割図の切替境界 |
| representative chart | 代表チャート |
| life event | 主要な出来事 |
| trait evidence | 特性に関する証拠 |
| Dasha evidence | ダシャー時系列の証拠 |
| best estimate | 現在の最良推定 |
| confirmed time | 確認済み時刻 |
| confidence | 確信度 |

Keep candidate IDs, timestamps, scores, `D1/D9/D10`, `MD/AD/PD`, filenames,
tables, and threshold labels unchanged.

## Event intake

For each required major event, request:

- `出来事の内容`
- `発生時期（分かる範囲で年月日、難しければ年月または期間）`
- `始まり・成立・終了のどの時点か`
- only when relevant, `記録の有無と時期の確かさ`

Do not invent missing dates. Preserve the user's real resolution and let the
workflow decide how much each event can distinguish.

## Discriminating questions

Use mutually recognizable everyday alternatives, for example:

> 仕事で責任が増える場面では、A「前に立って即断することが多い」か、
> B「情報を整理してから仕組みで動かすことが多い」か、どちらが普段の自分に
> 近いですか。どちらとも言いにくければ `0` と答えてください。

The alternatives must come from the actual surviving candidates and applicable
question-design rules; the sentence above is only a language pattern.

## Final rendering

Prefer this client-facing order where compatible with the required artifact:

1. `最終的な出生時刻`
2. `確認できた精度`
3. `候補がどこで分かれたか`
4. `出来事とダシャーの照合`
5. `分割図の切替確認`
6. `残る不確実性`

Use exact time and uncertainty wording separately. A clean Japanese sentence is:

> 現在の最良推定は 08:14 です。確認できた精度は実際の D9/D10 切替幅に
> 基づきます。08:14 という表示自体が自動的に ±1 分を意味するわけではありません。
