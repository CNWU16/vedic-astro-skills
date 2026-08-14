# Codex Patch for Vedic Astro Skills

> Codex Patch v1.0.0. This package is independent from the Vedic Skill Suite
> version, Blind QA protocol version, and analyst-editing protocol version.

This is a Codex execution-compatibility layer, not a replacement for the Vedic
skills and not a claim that their methods are invalid. Each selected `SKILL.md`
remains the canonical workflow and can run independently in other capable agent
environments.

The patch addresses Codex-specific execution risks such as skipped phases,
user-context overfitting, mechanical scoring, mixed report lineages, artifact
routing, and client-facing rendering. It also provides a single language rule:
client-facing content follows the user's requested language while canonical data,
filenames, technical identifiers, evidence, and conclusions remain unchanged.

[日本語インストールガイド](README.ja.md) · [中文安装说明](README.md)

## Contents

- `AGENTS.md` — global Vedic execution router.
- `vedic_uc_firewall.md` — user-context evidence firewall for every Vedic task.
- `vedic_client_voice.md` — client-facing readability and voice rules.
- `vedic_core_life_rendering.md` — standard and Pro life-section rendering.
- `vedic_qa_rendering.md` — normal Vedic Q&A rendering after valid QA entry.
- `vedic_output_router.md` — QA/report/analyst-edit/HTML artifact routing.
- `vedic_blind_qa_prompt.md` — full-scan blind natal Q&A protocol.
- `vedic_consultative_integration_prompt.md` — optional analyst-edited complete
  natal report workflow.
- `vedic_rectifier_execution_overlay.md` — rectification execution router.
- `vedic_rectifier_settlement.md` — candidate settlement and counterevidence audit.
- `vedic_rectifier_question_design.md` — discriminating question design.
- `vedic_rectifier_interval_guard.md` — interval and representative-chart guards.

`PACKAGE_INTRO.md` explains the complete package positioning and boundaries. It is
documentation, not a runtime rules module.

## Installation

### 1. Locate the active Codex home

The default is `~/.codex`. If `CODEX_HOME` is set, use that actual directory for
every path below.

### 2. Install the skills first

Install the required `vedic-*` skills before this patch. `vedic-core-pro` is
optional; the standard `vedic-core` works without it.

### 3. Merge the Vedic router safely

Do not overwrite an existing global `AGENTS.md`.

- If `<CODEX_HOME>/AGENTS.md` does not exist, copy this package's `AGENTS.md` there.
- If it already exists, merge the complete section beginning with
  `# Vedic Skill Suite Execution Router` into the effective file.

If `<CODEX_HOME>/AGENTS.override.md` exists, it may override the global router.
Merge the Vedic section into the instruction file that actually takes effect.

### 4. Copy the routed modules

Copy these eleven files to the active `CODEX_HOME` root without renaming them:

```text
vedic_uc_firewall.md
vedic_client_voice.md
vedic_core_life_rendering.md
vedic_rectifier_execution_overlay.md
vedic_rectifier_settlement.md
vedic_rectifier_question_design.md
vedic_rectifier_interval_guard.md
vedic_blind_qa_prompt.md
vedic_consultative_integration_prompt.md
vedic_output_router.md
vedic_qa_rendering.md
```

### 5. Start a new Codex task

Global instructions may be loaded when a task starts. After installing or updating
the patch, create a new task and verify that the Vedic router and routed modules are
available. Do not assume an already-open task will reload changed global files.

## Standard and Pro core selection

Before a new natal core analysis writes its first core artifact:

- an explicit Standard request selects `vedic-core`;
- an explicit Pro request selects `vedic-core-pro`;
- if both are installed and the user did not specify a version, Codex asks once;
- if only one is installed, Codex uses it without advertising an unavailable option.

The selected engine becomes the report lineage. Continuations, normal Q&A, blind
questions, analyst editing, and packaging inherit it. Standard and Pro artifacts
must never be silently merged.

Pro does not require a separate patch. Both versions use this same user-context,
rendering, routing, rectification, and language layer while continuing to follow
their own selected `SKILL.md`.

## Language behavior

Client-facing language follows an explicit user request; otherwise it matches the
latest substantive user message. The rule applies to:

- chat and intake;
- questionnaires and confirmation prompts;
- progress notices and user-visible warnings;
- reports, normal Q&A, blind Q&A, and analyst-edited prose;
- client-facing HTML content.

Chinese or English wording inside a routed module is a semantic template, not a
forced output language. Translation must not alter canonical filenames, schema
headings, CLI flags, technical codes, Sanskrit/English identifiers, candidate
labels, scores, evidence citations, chart judgment, phase state, or report lineage.

For Japanese runs, each selected skill loads its own `resources/ja-*.md`
localization layer. The patch continues to control execution and evidence boundaries;
the Japanese resource controls terminology and client-facing rendering only.

## User-context boundary

User context includes facts visible in chat, summaries, reports, filenames,
screenshots, archives, and `user_context.md`. It is not chart evidence unless the
selected skill explicitly gives it an evidentiary role for the current phase.

Outside an authorized calibration phase, lock the chart-derived judgment before
using permitted context for ethics, wording, reality mapping, or practical advice.
Never package a known fact as an independent prediction.

## Updating

Update the router and all routed modules as one coherent package. Do not combine a
new router with an arbitrary subset of older modules. Start a new Codex task after
the update to verify the effective configuration.

The patch does not modify any Vedic `SKILL.md`. Removing the global router section
and the eleven routed modules returns Codex to the standalone skill behavior.
