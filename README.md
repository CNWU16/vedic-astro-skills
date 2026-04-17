# 🔱 Vedic Astro Skills

> AI-powered Vedic astrology analysis toolkit. Three specialized skills working together.
>
> 吠陀占星AI分析工具包。三个专业技能协同工作。

Works with **Antigravity** and **Claude Code**.

---

## Skills Overview | 技能概览

| Skill | Purpose | Trigger |
|-------|---------|---------|
| 🏛️ **core** | P1-P13 行星审计引擎 + 验前事校验 | "星盘审计"、"行星分析"、"完整分析" |
| 💼 **career** | 职业方向 + 事业时机 | "职业分析"、"事业方向"、"10宫" |
| 💘 **love** | 恋爱时机 + 感情分析 | "恋爱运势"、"桃花时机"、"感情分析" |

### Architecture | 架构

```
vedic-core (核心引擎)
├── 数据提取 + 验前事校验
├── P1-P13 行星审计
├── D9 校准
└── 宫位诊断函数
      │
      ├──→ vedic-career (事业层)
      └──→ vedic-love (感情层)
```

**core** runs first to establish the foundation. **career** and **love** can run standalone (fast mode) or inherit core's audit data (deep mode).

---

## Installation | 安装

### Antigravity

```bash
# Install all three
cp core/SKILL.md ~/.gemini/antigravity/skills/vedic-core/SKILL.md
cp career/SKILL.md ~/.gemini/antigravity/skills/vedic-career/SKILL.md
cp love/SKILL.md ~/.gemini/antigravity/skills/vedic-love/SKILL.md
```

Or install only what you need.

### Claude Code

```bash
cp claude-code/.claude/commands/*.md .claude/commands/
```

Commands: `/vedic-core`, `/vedic-career`, `/vedic-love`

---

## Usage | 使用

### Recommended Flow (Deep Mode)

```
1. Provide birth chart PDF
2. Run vedic-core → get P1-P13 audit + 验前事 validation
3. Run vedic-career or vedic-love → inherits core data automatically
```

### Quick Mode

Run career or love directly — they work standalone with simplified analysis.

### Input

- Jagannatha Hora exported PDF
- Or birth chart screenshots
- Python + PyMuPDF (`pip install pymupdf`) for PDF extraction

---

## Project Structure | 项目结构

```
vedic-astro-skills/
├── README.md
├── LICENSE
├── core/
│   └── SKILL.md          # 核心引擎 (P1-P13 + 验前事)
├── career/
│   └── SKILL.md          # 职业分析
├── love/
│   └── SKILL.md          # 恋爱时机
└── claude-code/
    └── .claude/commands/
        ├── vedic-core.md
        ├── vedic-career.md
        └── vedic-love.md
```

## License

MIT
