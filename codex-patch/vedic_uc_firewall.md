# Vedic UC Evidence Firewall

This module applies to every Vedic calculation, validation, analysis, report,
rectification, and Q&A task, not only to explicit blind tests. It supplements
the selected `SKILL.md` without replacing that skill's evidence rules, phase
transitions, calculations, filenames, or file permissions.

## Four operations that must stay separate

- **Capture/write**: storing a newly supplied fact in `user_context.md` is an
  administrative memory action, not an astrological inference and not evidence
  that the fact is chart-derived. Whether and when a skill may write that file
  is controlled only by the selected `SKILL.md`.
- **Read**: permission to read UC is phase-specific. Writing a fact does not
  grant permission to read it in the current phase, and reading one permitted
  field does not open the rest of the biography.
- **Chart inference**: chart conclusions, timing, weights, candidate ordering,
  and confidence must be built from the sources authorized by the selected
  skill. Permission to read UC is not permission to use it as chart evidence.
- **Consultation mapping**: after the chart-derived criteria or conclusion are
  locked, permitted UC may be used for ethical checks, wording, presentation,
  mapping real options to the locked criteria, and practical advice.

Do not collapse these operations. In particular, `readable` never means
`allowed to generate the chart conclusion`, and `written` never means
`available as evidence`.

## What counts as UC

- Treat as UC every biographical fact, event, trait, relationship status,
  concern, preference, outcome, correction, and answer supplied by the user.
- UC includes information in `user_context.md`, the current chat, earlier chat
  summaries, QA files, rectification records, feedback, report prose,
  archives, HTML/PDF reports, filenames, and screenshots. Avoiding the
  `user_context.md` file alone is not context isolation.
- A fact-bearing downstream report is not independent chart evidence. Trace
  every analytical claim back to the chart data or to an audit product that
  was derived under the selected skill's permitted evidence rules.
- Inputs that the selected skill explicitly requires to construct or scope the
  task are **authorized operational inputs**, not biographical evidence. This
  includes birth date/time/place, time source and precision, gender where the
  skill uses it, a Prashna question/time/place, a synastry relationship type,
  the user's requested topic/range, and the factual attributes of options being
  compared. Use each only for the function assigned by the skill; do not let it
  silently become evidence for another conclusion.

## Default evidence rule

- UC is not astrological evidence unless the selected `SKILL.md` explicitly
  assigns it an evidentiary role for the current phase.
- Outside a role in which the selected skill explicitly authorizes UC as
  evidence, do not use UC to generate or select a chart interpretation,
  candidate, predicted year, predicted event type, direction, stopping point,
  tie-breaker, confidence level, evidentiary emphasis within chart inference,
  evidentiary weight, or favorable/adverse reading. The user's question may
  still define the authorized subject and range.
- Do not start with a known fact and search the chart for a matching
  explanation. Derive from the authorized chart sources first; only then use
  UC in the narrow role the selected skill permits.
- Never repeat or paraphrase a user's known fact as though it were an
  independent prediction.
- For chart-derived judgments, the same chart and authorized chart sources must
  produce the same chart criteria and chart conclusion if the biography is
  removed or contradicted. This invariance rule does not apply to
  skill-authorized rectification evidence, required operational inputs, or the
  final mapping of real-world options to already-locked chart criteria. If the
  facts of Offer A and Offer B are swapped, the recommendation may correctly
  change; the chart criteria and weighting may not.

## Evidence construction

- Build the judgment from the sources authorized by the selected skill and
  current phase. For each material conclusion, identify the supporting chart
  signals, the strongest contrary chart signals, and the resulting confidence
  before using UC for any permitted consultation purpose.
- Keep the depth of this check proportional to the task. A full candidate
  matrix is required only when the selected skill, the user's requested
  comparison, or a ranking/superlative judgment requires one.
- Apply the same method, weights, thresholds, and depth of search to every
  candidate. UC may not decide which candidate receives deeper analysis.
- Search for counterevidence before locking a conclusion. A conclusion that
  survives only because it matches UC must be removed or recomputed.
- Whenever the phase permits UC reading and calls for a chart-derived judgment
  in which UC is not skill-authorized evidence, use a two-pass order:
  1. create a **chart-only lock** containing the conclusion or evaluation
     criteria, supporting signals, strongest contrary signals, confidence, and
     source files;
  2. apply the permitted UC and produce a separate consultation layer.
  Read UC at the point required by the selected skill. If the skill requires
  reading it before the chart-only lock for intake or ethical safety, quarantine
  it from pass 1; do not search the chart for matching explanations.
- Label material output by provenance when the distinction could be blurred:
  `chart-derived judgment`, `UC-tailored consultation`, or
  `post-feedback explanation`.
- Before delivery, run this counterfactual audit:
  1. Would the conclusion stay the same if all UC sentences were deleted?
  2. Would it stay the same if the user had reported the opposite outcome?
  3. Can every material judgment be reproduced from permitted non-UC sources?
  These questions apply to chart-derived judgments, not to practical advice
  or option mapping, required operational inputs, or rectification evidence
  explicitly authorized by the selected skill.
  If any applicable answer is no, recompute before delivery.
- Evidence-source discipline is an execution safeguard, not a replacement for
  the selected skill's astrology thresholds, candidate rules, output format,
  or phase transitions.

## UC permissions by mode

- Chart calculation and chart-only analysis: use the operational inputs
  explicitly required by the skill, but do not use biographical outcomes or
  feedback as chart evidence.
- Reader pre-validation: follow `vedic-reader` exactly, including every role it
  explicitly assigns to gender, relationship status, concern, time source, and
  feedback. Do not add a stricter UC ban, and do not extend those permissions
  beyond the role and phase defined by the skill.
- In `vedic-reader` pre-validation, `relationship status` includes single,
  dating, married, divorced, separated, widowed, and equivalent states. First
  derive and lock any F-class relationship window and its chart-supported
  direction from chart-only sources. Known status may then orient lifecycle
  wording among meanings already supported by that locked result; it must not
  move the window, promote a weak signal, or create a formation, formalization,
  restructuring, or dissolution claim unsupported by the chart.
- A known relationship status suppresses only an H-class prediction of the
  current status itself. It never suppresses the required scan or possible
  selection of an otherwise eligible chart-derived F-class relationship event.
  If only the status or existence of a relationship transition is known but
  its timing is not, the locked window may be tested as a timing prediction;
  the test claim is the timing, not discovery of the event's existence, and
  existing reader feedback rules remain unchanged. If the specific event and
  date are already known, show them only as a `known-fact cross-check` and do
  not count them as an independent R1 hit.
- Rectification: use UC only as explicit calibration evidence in the manner
  allowed by `vedic-rectifier`. Apply the same scoring method to every
  candidate and keep calibration evidence separate from sample-out
  validation; do not use unscored biography as an interpretive hint. In
  skill-authorized calibration questions, UC may identify known facts, anchor
  a lived scenario, and expose an unrecorded discriminator. The answer mapping
  remains chart-derived; a known fact is not a new independent evidence row.
- Standard `vedic-core` Steps 1-4, Pro Steps 0-6, and any other skill phase
  that prohibits `user_context.md`: treat both that file and visible chat facts
  as prohibited inference inputs except for the narrower confirmed-fact sources
  that the selected skill explicitly authorizes in Step 4 or Step 6.
- Standard `vedic-core` Step 4 may use only the confirmed facts that its skill
  permits, and only after the chart-derived conclusion is locked. In
  `vedic-core-pro` Step 6, use only the factual material from
  `structured_data.md` that the Pro skill permits; `user_context.md` remains
  prohibited. In either lineage, corroboration may not change the locked
  chart-derived direction, evidentiary weight, or confidence.
- Standard `vedic-core` Step 4.5 and `vedic-core-pro` Step 6.5 may read
  `user_context.md` only for the skill-defined wording and real-life placement
  pass after all chart judgments are locked. This is read-only access: do not
  ask new questions or write UC. Do not change ratings, windows, domains,
  spouse-portrait primary/secondary forms or source direction, Yoga or Dasha
  judgments, tables, confidence, or upstream technical artifacts. Standard may
  edit only `p5a_life.md` and `p5b_life.md`; Pro may edit only
  `p5_prediction.md`, the cross-diagnostic prose/title in `p5c_topics.md`, and
  `p6a_life.md` / `p6b_life.md` / `p6c_blueprint.md`, exactly as its skill
  permits.
- In that wording-only pass, keep the skill's sensitive-category labels
  internal. Do not repeat the label, object, or note, do not use procedural
  wording such as “based on your background,” and do not repackage a known UC
  fact as a prediction or chart finding. Non-sensitive facts may refine the
  real-life landing only where genuinely relevant and without changing the
  conclusion's strength.
- Normal consultation Q&A: read UC at the point required by the skill, but
  quarantine it while locking the chart-derived judgment, timing, or evaluation
  criteria. Then apply UC for ethics, wording, presentation order, concrete
  mapping, and practical advice. Keep the two layers visibly separable.
- Choice and comparison Q&A: option descriptions are required operational
  inputs. After locking the chart criteria, score every option against the same
  criteria. The option recommendation may depend on the option facts; the chart
  criteria, weights, and timing may not be rewritten to favor a known outcome.
- Career, love, synastry, Prashna, or any other skill with its own UC rule:
  follow the exact scope of that rule. A ban on `user_context.md` does not
  cancel intake fields that the same skill explicitly requires, and an allowed
  intake field does not authorize reading unrelated biography.
- File-writing permissions remain exactly those of the selected skill.
  This module neither expands nor narrows them. When writing is permitted,
  append neutral user-supplied facts without converting them into chart
  conclusions; writing alone never grants read or inference permission.
