# Vedic Astro Skills

Eight coordinated AI skills for Vedic/Jyotish chart calculation, validation, full
natal analysis, career, relationships, birth-time rectification, two-person
synastry, and question-time Prashna.

The primary workflow starts from birth details. A user can provide a birth date,
exact time, and place; the calculator creates the canonical chart data and routes
it directly into validation and full analysis. A pre-generated PDF or screenshot
is supported, but it is not required.

[简体中文](README.md) · [日本語](README.ja.md)

## What is included

| Skill | Purpose | Example English request |
|---|---|---|
| `vedic-calculator` | Calculate a complete Vedic chart from birth details | “Calculate my Vedic chart from my birth date, time, and place.” |
| `vedic-reader` | Import, normalize, and validate a chart from PDF, image, or text | “Read and validate this JHora chart.” |
| `vedic-core` | Run the standard full natal audit and ten-area life analysis | “Give me a complete Vedic analysis of this chart.” |
| `vedic-career` | Analyze career direction, role fit, strengths, and timing | “What career direction does my Vedic chart support?” |
| `vedic-love` | Analyze relationship patterns, needs, and timing | “Analyze my relationship patterns and timing.” |
| `vedic-rectifier` | Refine an uncertain birth time from events and chart transitions | “Help me rectify my birth time.” |
| `vedic-synastry` | Compare two charts for mutual activation and shared timing | “Compare our two Vedic charts.” |
| `vedic-prashna` | Cast a separate chart for one concrete question | “Cast a Prashna chart for this question.” |

## Highlights

- Direct chart calculation from birth details; no external chart PDF is required.
- A shared, validated `structured_data.md` contract across the natal workflow.
- D1 and divisional-chart calculations, Vimshottari Dasha, native MD/AD/PD
  boundaries, Chara Dasha, Shadbala, SAV/BAV, dignity, house-lord, and yoga data.
- Separate standard natal, synastry, rectification, and Prashna workflows.
- English, Japanese, and Chinese client-facing conversations, questionnaires, reports, Q&A,
  warnings, and HTML report shells.
- Canonical filenames, schema headings, CLI flags, and technical identifiers remain
  stable across languages so calculation and analysis modules stay interoperable.
- Compatible distributions for Codex, Claude Code, and Antigravity.

## Installation

### Codex

```bash
git clone https://github.com/CNWU16/vedic-astro-skills.git
cp -r vedic-astro-skills/codex/skills/vedic-* ~/.codex/skills/
```

For the complete recommended Codex setup, also install the execution-rules patch.
It adds phase discipline, user-context evidence isolation, output routing,
birth-time-rectification safeguards, and client-facing rendering rules without
modifying any skill method file.

See [Codex patch installation](codex-patch/README.en.md).

### Claude Code

```bash
git clone https://github.com/CNWU16/vedic-astro-skills.git
cp -r vedic-astro-skills/claude-code/skills/vedic-* ~/.claude/skills/
```

### Antigravity

Copy all eight folders from `antigravity/skills/` into your Antigravity skills
directory. Install the complete suite: the calculator is the computational
foundation used by most downstream modules.

## Python environment

Supported Python versions: **3.8 through 3.13**. Python 3.14 is not currently
supported because of compiled astronomy dependencies.

Use the provided setup script instead of installing `requirements.txt` directly:

```bash
python path/to/vedic-calculator/scripts/setup_env.py
```

The setup script creates or repairs an isolated environment and verifies the
required astronomy and calculation packages.

## Quick start

### Start from birth details

```text
Calculate my Vedic chart.
Birth date: 1990-01-01
Birth time: 08:00
Birth place: London, United Kingdom
```

The calculator produces the canonical `structured_data.md`. Continue with:

```text
Run the standard full Vedic analysis in English.
```

### Start from an existing chart

Attach a JHora, Parashara's Light, or other Vedic chart PDF/image and say:

```text
Read and validate this Vedic chart in English.
```

### Two-person synastry

Provide one verified `structured_data.md` per person, or provide the second
person's birth details and let the calculator create it:

```text
Compare these two Vedic charts for a business partnership.
```

### Prashna

Prashna is independent from the natal workflow. Provide one concrete question,
the exact time it was asked, and the asking location:

```text
Cast a Prashna chart for this specific question.
```

The classical standard layer runs first. Optional Tajika and KP stacks remain
physically and logically isolated and are never merged into the standard vote.

## Language behavior

Each skill chooses the client-facing language from the user's explicit request;
otherwise it follows the latest substantive user message. This applies to chat,
intake, progress notices, reports, Q&A, warnings, and user-facing HTML.

Japanese runs additionally load a small per-skill localization resource that fixes
terminology, polite register, intake wording, and report labels without duplicating
or translating the calculation and judgment workflow. Japanese HTML uses
`report_builder.py --lang ja`.

Internal interoperability remains stable across languages:

- filenames and directory structure are not translated;
- `structured_data.md` schema headings stay canonical;
- CLI flags, JSON keys, candidate labels, technical codes, and Sanskrit/English
  identifiers are preserved;
- technical terms are explained in plain language on first use.

Changing language does not change chart calculations, evidence, phase state,
scores, report lineage, or conclusions.

## Repository layout

```text
antigravity/skills/   canonical published skill content
claude-code/skills/   Claude Code distribution
codex/skills/         Codex distribution with agents/openai.yaml metadata
codex-patch/          optional recommended Codex execution-rules patch
scripts/              repository consistency checks
```

`antigravity/skills/` is the content baseline. Claude Code must match it file for
file. Codex may additionally contain one `agents/openai.yaml` per skill. After any
skill change, run:

```bash
python scripts/check_skill_parity.py
```

## Scope and responsible use

This repository implements a traditional Vedic/Jyotish analysis workflow. Its
outputs are intended for cultural study, structured self-reflection, and research.
They are not medical, legal, financial, or safety-critical professional advice.

## License

AGPL-3.0. Personal use is unrestricted under the license. Commercial deployments
must comply with the repository license and [commercial notice](COMMERCIAL_NOTICE).
