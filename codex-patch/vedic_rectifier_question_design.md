# Rectifier Question Design Compatibility Pointer

This filename is retained so an update safely overwrites older Codex Patch
installations that contained a separate question-design method.

The canonical procedure now lives inside the selected `vedic-rectifier` skill:

```text
resources/calibration_quiz.md
```

Before constructing, replacing, sending, or interpreting a calibration
questionnaire, read that file completely and follow it exactly. In particular,
preserve its entry condition, real candidate-difference scan, opposing
predictions, question-type selection, `A/B/0` or match/no-match format, three
checks with notes, pre-feedback `rectification_quiz.md` lock, and returning
answers to the mapping table for re-judgment.

Do not combine the current skill with the retired three-category hard/soft
question rules from an older patch. This compatibility file adds no evidence
category, score, threshold, question quota, or fallback method.

If `resources/calibration_quiz.md` is missing, report the missing skill
resource once and continue only with the selected `SKILL.md`; do not reconstruct
the old patch procedure from memory.
