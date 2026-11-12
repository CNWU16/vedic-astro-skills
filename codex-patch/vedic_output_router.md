# Vedic Client-Output Intent Router

This module selects the requested artifact and presentation mode only. It does
not change the selected Vedic skill's workflow, evidence rules, required
matrices, thresholds, filenames, phase gates, calculations, or QA entry
conditions.

## Routing precedence and entry conditions

- Select and enter the applicable Vedic skill before routing its output.
- A request is normal QA only after the selected skill's own QA entry
  conditions are satisfied, such as an already completed report or an attached
  equivalent report. A focused question alone does not permit skipping an
  unfinished initial analysis.
- A core natal blind question routed under the global core natal blind-question
  rule remains governed by the complete blind-QA prompt.
  Consultative prose may improve the final wording only after every mandatory
  blind matrix and visible comparison is complete.
- A Prashna question, an initial career/love/synastry analysis, rectification,
  or any other skill-specific workflow keeps that skill's normal artifact and
  phase sequence. Do not relabel it as core QA merely because it asks one
  focused question.
- A request for the core technical analysis, P1-P12 audit, houses, divisional
  audit, or technical report remains the normal core workflow.
- Within that normal workflow, the standard life-section files
  (`p5a_life.md` / `p5b_life.md`) and Pro life-section/blueprint files
  (`p6a_life.md` / `p6b_life.md` / `p6c_blueprint.md`) are the default
  client-facing body. Rendering them for a client does not activate the
  separate analyst-edit workflow.
- Activate core analyst-edit mode only when the user explicitly asks for an
  analyst-edited complete report, consultative integrated full report,
  client-readable complete report, or invokes `印占咨询式整合模式`.
- Do not activate the full analyst-edit prompt merely because the user asks a
  normal QA answer to use humane, consultative language.
- Follow the selected skill's delivery policy. Normal QA in the public Core,
  career, love, and synastry skills defaults to a complete chat answer; do not
  create a Markdown file unless the user requests saving or export. When a file
  is requested, use the skill's exact filename and directory. Other skills and
  explicit blind-audit protocols retain their own output requirements.
- The technical report, analyst-edited complete report, blind-audit artifact,
  and normal QA artifact are separate layers. Never rename or overwrite one
  layer to imitate another.
- Standard `vedic-core` and `vedic-core-pro` are separate report lineages even
  where filenames overlap. QA, blind audits, analyst edits, and HTML packaging
  must inherit the engine selected for the source report. If exclusive markers
  from both lineages are present and no authoritative lineage is already
  explicit, resolve that ambiguity before reading or building; never let a
  builder silently aggregate both.

## Packaging intent

- “生成报告”, “打包”, or “导出HTML” selects a presentation copy of an
  existing source artifact. It is not permission to change, merge, summarize,
  or rewrite that source.
- If the user explicitly names a source file or report layer, package exactly
  that artifact.
- If a packaging request immediately follows one focused QA and no other
  artifact is named, the intended source is that QA Markdown, not every report
  in the working directory.
- If that QA was delivered only in chat, the export request authorizes saving
  that answer under the selected skill's QA filename before packaging it.
- If it follows an explicitly activated analyst-edit task, the intended source
  is `consultation_analyst_edit.md`.
- Before running a builder, inspect which files it will discover. Do not claim
  to have produced a single-artifact HTML if the builder silently aggregated
  other `qa_*.md` files or report layers.
- When an approved builder supports the requested QA type but would aggregate
  sibling QA files, an isolated temporary staging directory may contain only a
  copy of the selected QA source for rendering. Do not edit or rename the
  canonical source, and verify the rendered HTML came from that source alone.
- If the installed builder does not support the selected artifact, do not
  rename an analyst report as QA, substitute the core report, or claim success.
  State the tooling limitation and obtain authorization for a compatible
  single-source rendering route.
- If the source artifact is genuinely ambiguous, ask one concise clarification
  question instead of silently packaging multiple layers.
- HTML may add layout and navigation only. It must not introduce conclusions,
  delete counterevidence, change provenance, or alter the source's confidence.
