<p align="center">
  <h1 align="center">🔱 Vedic Astro Skills v8.0</h1>
  <p align="center">
    <strong>AI驱动的吠陀占星分析系统 | AI-Powered Vedic Astrology Analysis System</strong>
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/version-v8.0-blue" alt="Version">
    <img src="https://img.shields.io/badge/python-3.8~3.13-green" alt="Python">
    <img src="https://img.shields.io/badge/license-AGPL--3.0-orange" alt="License">
    <img src="https://img.shields.io/badge/skills-8-purple" alt="Skills">
  </p>
</p>

<p align="center">
  <a href="README.en.md"><strong>English documentation</strong></a> ·
  <a href="README.ja.md"><strong>日本語</strong></a> ·
  <a href="README.md">中文 / Bilingual</a>
</p>

---

> **八个专精 Skill 协同工作，从原生排盘到完整人生审计、双人合盘，再到即时卜卦（Prashna）。**
>
> Eight specialized skills working together — from native chart calculation to complete life audit and two-person synastry, plus moment-based Prashna (horary).

**兼容 Antigravity、Claude Code 和 Codex。** Compatible with Antigravity, Claude Code, and Codex.

> ⚠️ **Codex 完整推荐配置** — 本仓库的 `codex/skills/` 是 8 个 skill 引擎；
> `codex-patch/` 是 Codex 专用的执行规则补丁（防跳步 + UC 证据防火墙 + 表达/产物/
> 校准等模块）。Skill 本体可以独立加载；如果要获得本仓库承诺的 Codex 阶段纪律、
> UC 隔离、校准增强和客户成文保障，**强烈建议同时安装补丁**。
> 下载与说明见 [codex-patch/README.md](codex-patch/README.md)，不用改任何 skill 文件。
>
> **Recommended complete Codex setup.** `codex/skills/` are the 8 engines; `codex-patch/` is the
> Codex-only execution-rules patch (phase discipline + UC firewall + rendering/routing
> modules). The skills can load independently, but install both to get the documented Codex
> execution safeguards. See [codex-patch/README.md](codex-patch/README.md).

---

## 📖 目录 / Table of Contents

- [安装 / Installation](#-安装--installation)
- [八Skill架构 / Architecture](#-八skill架构--architecture)
- [快速开始 / Quick Start](#-快速开始--quick-start)
- [各Skill说明 / Skill Details](#-各skill说明--skill-details)
- [项目结构 / Project Structure](#-项目结构--project-structure)
- [技术体系 / Technical Stack](#-技术体系--technical-stack)
- [版本历史 / Version History](#-版本历史--version-history)
- [赞赏 / Support](#-赞赏--support)

---

## 📦 安装 / Installation

### Step 1: 安装 Skill 文件 / Install skill files

<details>
<summary><b>Codex</b></summary>

```bash
# 从 GitHub 安装全部 8 个 skill（缺一不可）
# Install all 8 skills from GitHub (all required)

git clone https://github.com/CNWU16/vedic-astro-skills.git
cp -r vedic-astro-skills/codex/skills/vedic-* ~/.codex/skills/
```

> ⚠️ **Codex 完整推荐配置（codex-patch）** — 上述仅安装 8 个 `vedic-*` skill；
> 建议再安装 `codex-patch/`（1 个全局路由器 + 11 个按需模块，其中包含 UC 防火墙
> 与表达、产物、校准模块），以获得完整的 Codex 执行保障。
> 安装方法见 [codex-patch/README.md](codex-patch/README.md)。
>
> **Recommended complete Codex setup.** The commands above only install the 8 `vedic-*`
> skills. For the documented Codex safeguards, also install `codex-patch/` (one global
> router + 11 on-demand modules, including the UC firewall and rendering/routing modules).
> See [codex-patch/README.md](codex-patch/README.md).

</details>

<details>
<summary><b>Claude Code</b></summary>

```bash
git clone https://github.com/CNWU16/vedic-astro-skills.git
cp -r vedic-astro-skills/claude-code/skills/vedic-* ~/.claude/skills/
```

> Claude Code 只安装 `skills/vedic-*`。仓库不再提供重复维护的
> `.claude/commands` 全量副本，以 `SKILL.md` 为唯一工作流来源。

</details>

<details>
<summary><b>Antigravity</b></summary>

将 `antigravity/skills/` 下的 8 个文件夹复制到你的 Antigravity skills 目录：

Copy all 8 folders from `antigravity/skills/` to your Antigravity skills directory:

```
vedic-reader/
vedic-calculator/    ← 计算基座，必装！/ Required foundation!
vedic-core/
vedic-career/
vedic-love/
vedic-rectifier/
vedic-synastry/      ← 合盘（需两份盘）/ Synastry (needs two charts)
vedic-prashna/       ← 卜卦/时盘（独立·不需本命）/ Prashna (standalone, no natal chart)
```

</details>

> ⚠️ **建议一次装全 8 个 skill。** vedic-calculator 是计算基座，多数分析 skill 都依赖它生成的 `structured_data.md`。其中 **vedic-synastry（合盘）是双人分析 skill**——需双方各一份盘；**vedic-prashna（卜卦/时盘）是独立生态位**——不需本命盘，以提问时刻起盘答一事，与本命分析路径分开。
>
> **Install all 8 skills.** vedic-calculator is the computational foundation that most analysis skills depend on. Among them, **vedic-synastry (synastry) is a two-person skill** (needs one chart per person); **vedic-prashna (Prashna/horary) is a standalone module** — it needs no natal chart and casts a chart for the moment of asking.

### 🔧 codex-patch 是什么？/ What is the codex-patch?（Codex 用户必读）

> **一句话**：`codex/skills/` 是 8 个「引擎」，负责排盘、分析、合盘等计算；
> `codex-patch/` 是 Codex 专用的「驾驶规则」补丁，保证引擎按正确顺序、用正确姿势跑起来。
> Skill 本体并不因此变成技术上的不可独立运行；但本仓库完整支持的 Codex 配置是
> **Skill + codex-patch 同时安装**。Claude Code / Antigravity 用户不需要此补丁。

补丁**不修改任何 skill 文件**，是一套复制到 `~/.codex/` 根目录的执行规则，解决 AI 跑
印占流程时最容易出的几类问题：

- **防跳步**：强制完整读取 `SKILL.md`、公开当前阶段，禁止 D1/D9/D10 跳步乱序；
- **证据防火墙**：用户聊天里说的经历（`user_context`）不能反向"造盘面结论"，判断必须能脱离用户经历独立复现；
- **按需加载**：校准、盲问、客户成文、普通 QA、产物路由等模块按触发条件读取，不混成一锅；
- **标准版/Pro版不混跑**：两版同名报告文件不会被静默拼接，切版必须先说明补充/覆盖/重置；
- **客户能看懂**：报告不堆术语、也不只剩短句，最终给出明确占星判断。

这不表示Vedic skill的方法本身失效。在能够正确执行 `SKILL.md` 的其他Agent环境中，
同一流程可能不需要这些 Codex 兼容规则。补丁的校准部分另外公开两项操作者政策：
事件×Dasha与特质×结构按平等证据腿结算；原始分领先者在标准门槛未确认时，
必须经过候选级专家综合才能成为当前最佳估计。它们是明确披露的 Codex 运行政策，
不会被冒充为 `SKILL.md` 原生规则。

**安装**：先装 8 个 skill（上方 Step 1），再按 [codex-patch/README.md](codex-patch/README.md)
把 `codex-patch/` 里 11 个 `vedic_*.md` 复制到 `~/.codex/`，并按其中说明合并 `AGENTS.md`。

### Step 2: 安装 Python 依赖 / Install Python dependencies

| 要求 Requirement | 说明 Details |
|:---|:---|
| **Python** | 3.8 ~ 3.13 （3.14 暂不支持 / not yet supported） |
| **安装 Install** | 运行 `setup_env.py`（见下方 / see below） |

```bash
# 推荐：使用自动安装脚本（处理依赖冲突 + 自动验证）
# Recommended: Use the auto-setup script (handles dependency conflicts + auto-validates)
python vedic-calculator/scripts/setup_env.py

# ⚠️ 不要直接 pip install -r requirements.txt（dashaflow 依赖冲突）
# ⚠️ Do NOT use pip install -r requirements.txt (dependency conflict with dashaflow)
```

> 💡 AI 首次运行时会自动检测环境并运行 `setup_env.py`。但 **请确保系统已安装 Python 3.8~3.13**。
>
> The AI agent will auto-detect and run `setup_env.py` on first use. But **make sure Python 3.8~3.13 is installed on your system**.
>
> 注：vedic-synastry 的脚本是纯标准库，不需要额外依赖。/ Note: vedic-synastry scripts use only the Python standard library.

---

## 🏛️ 八Skill架构 / Architecture

```
用户星盘 (PDF/截图/文本)          用户出生信息 (日期+时间+地点)
Chart file (PDF/image/text)      Birth info (date+time+place)
    │                                    │
    ▼                                    ▼
┌──────────────┐                ┌───────────────────┐
│ vedic-reader │                │ vedic-calculator   │
│ 提取 + 校验   │                │ 原生排盘引擎        │
│ Extract+Verify│                │ Native calc engine │
└──────┬───────┘                └────────┬──────────┘
       │                                 │
       │     structured_data.md          │
       └────────────┬────────────────────┘
                    ▼
             ┌─────────────┐      ┌────────────────┐
             │ vedic-core   │─────▶│ vedic-rectifier │
             │ P1-P12 审计   │      │ 时间校准 ±5min   │
             │ 宫位诊断      │      │ Time rectify     │
             │ 十大板块总结   │      └────────────────┘
             └──────┬──────┘
                    │
          ┌─────────┼──────────┐
          ▼         ▼          ▼
   ┌──────────┐ ┌────────┐ ┌──────────────────┐
   │vedic-career│ │vedic-love│ │ vedic-synastry   │
   │职业蓝图    │ │恋爱时机  │ │ 合盘（需两份盘）  │
   │Career      │ │Love      │ │ Synastry (2 charts)│
   └──────────┘ └────────┘ └──────────────────┘
                              ▲
              另一个人的 structured_data.md
              second person's chart

─── 独立生态位 / Standalone（不接入上面的数据流）───
┌──────────────────────────────────────┐
│ vedic-prashna — 卜卦/时盘 (Prashna)      │
│ 不需本命，以提问时刻起盘答一事            │
│ No natal chart; cast for the moment    │
└──────────────────────────────────────┘
```

| Skill | 功能 Function | 触发词 Trigger |
|:------|:------|:------|
| 🧮 **calculator** | 原生排盘引擎，给出生时间直接计算 / Native chart engine | “直接排盘” · “calculate my Vedic chart” · “cast my birth chart” |
| 📖 **reader** | 从 PDF/截图提取出生信息，以calc生成主数据并执行16条校验 / Extract birth data, calculate, and validate | “读盘” · “read my Vedic chart” · “import this JHora chart” |
| 🔬 **core** | P1-P12行星审计 + 宫位诊断 + 十大板块 / Planet audit + life summary | “开始分析” · “full Vedic chart analysis” · “complete birth chart reading” |
| 💼 **career** | 4Phase职业蓝图 / Career blueprint | “职业分析” · “Vedic career reading” · “career timing” |
| 💘 **love** | 3Step恋爱时机分析 / Love timing analysis | “感情分析” · “Vedic love reading” · “relationship timing” |
| 📐 **rectifier** | ≥5件重大事件 + 结构证据校准出生时间，目标精度 ±5min / Birth time rectification | “校准时间” · “birth time rectification” · “my birth time may be wrong” |
| 💞 **synastry** | 双人合盘：跨盘叠盘 + 六维矩阵关系分析 / Two-person synastry | “合盘” · “Vedic synastry” · “compare our birth charts” |
| 🔮 **prashna** | 卜卦/时盘：提问时刻起盘答一事，不需本命（独立生态位）/ Prashna horary | “即时盘” · “Prashna” · “cast a horary chart for this question” |

---

## ⚡ 快速开始 / Quick Start

> 💡 **只需说"读盘"或"占星"即可启动。** reader 是统一入口，会根据你提供的内容自动选择最佳路径。
>
> In English, say **“calculate my Vedic chart from my birth details”** to start from
> scratch, or **“read my Vedic chart”** when you already have a chart file. The
> suite matches the user's language for client-facing questions, reports, and Q&A
> while keeping its internal data contract stable.
>
> 日本語では **「この出生情報でヴェーダ占星術の出生図を作って」** から始められます。
> 各 Skill は日本語の専門用語、敬体、入力文、レポート見出しを必要なときだけ読み込み、
> 計算・証拠・フェーズ・内部データ契約は共通のまま保ちます。

### 用法示例 / Usage

```
场景1：只有出生时间
用户: 帮我排盘，1990年3月15日 14:30 北京
 AI: → reader 检测到出生信息 → 自动调用 calculator 排盘
    → 输出 structured_data.md

场景2：有 JHora PDF
用户: [发送PDF] 读盘
 AI: → reader 从 PDF 提取出生信息 → calculator生成主数据
    → PDF数据做交叉验证（Shadbala例外：有PDF则对照并展示PDF值）
    → 输出 structured_data.md

场景3：什么都没带
用户: 激活占星
 AI: → reader 弹出引导菜单，让你选择输入方式

后续（任何场景都一样）：
用户: 开始分析      → vedic-core 完整审计
用户: 分析事业      → vedic-career 职业蓝图
用户: 分析感情      → vedic-love 恋爱时机
用户: 合盘 / 我和XX合不合 → vedic-synastry 双人合盘（再提供对方出生信息即可）
用户: 卜卦 / 起一卦 / 占问一事 → vedic-prashna 即时起盘（独立·不需本命）
```

### reader 内部路由 / Internal Routing

```
用户输入
  │
  ├─ 提供了出生时间 ──→ 自动调用 vedic-calculator ──→ structured_data.md
  ├─ 提供了 PDF/截图 ──→ reader提取出生信息 ──→ calculator主数据 ──→ PDF交叉验证
  └─ 什么都没提供   ──→ 弹出引导菜单
```

> ⚠️ 不需要手动选择 skill。**说"占星"就行**——reader 会自动判断。
>
> You don't need to manually choose a skill. Just say "占星" — reader handles routing automatically.

> 💡 **关于 PDF 补充：** calculator 排盘完成后会提示：
> - **a) 直接进入分析**（推荐）— calc 精度 >97%，排序与 JHora 一致，可直接用
> - **b) 发送 JHora PDF 补充** — 可选；先与calc逐行对照，再展示PDF Shadbala值
> - 若二者不一致，报告会明确标注“calc与PDF不一致；当前采用PDF”，并保留calc基准
>
> 不补充也完全不影响分析质量。
>
> **About PDF supplement:** Calculator output is canonical. PDF data is used for cross-validation; valid Shadbala values are compared row by row and displayed from the PDF, with differences explicitly flagged and the calc baseline retained.

---

## 📋 各Skill说明 / Skill Details

### 🧮 vedic-calculator — 精确排盘引擎 / Precision Chart Engine

**v6.1 升级。** engine.py v0.5 — 基于 PyJHora 精确天文算法，fail-fast 架构。

*Updated in v6.1.* engine.py v0.5 — Built on PyJHora's precise astronomical algorithms, fail-fast architecture.

**计算架构 / Calculation Architecture:**

| 模块 Module | 算法来源 Algorithm Source | 说明 Notes |
|:---|:---|:---|
| 行星位置 Positions | pysweph (Swiss Ephemeris) | 天文核心，精度 < 0.01° |
| SAV / BAV | PyJHora 原生 | 12/12 星座完美匹配 JHora |
| Vimsottari Dasha | PyJHora 原生 (`dasha_pyjhora.py`) | ≤2 天偏差（含 1 个 0 天完美匹配）|
| 分盘 Divisional | PyJHora 原生 | 15 张分盘 (D1~D60) |
| Shadbala 六力 | PyJHora + **9 项 bug 修正** (`shadbala_pyjhora.py`) | 修正 Sthana/Kaala/Dig 等子项 |
| Dignity / Jaimini | dashaflow | 查表逻辑，无需修正 |
| Bhava Bala / Lagnas | PyJHora 原生 | 宫位力量 + 特殊 Lagna |

> ⚠️ **为什么 Shadbala 需要修正？** PyJHora 的 SAV/Dasha/分盘模块是正确的，但 Shadbala 的 3 个子项（Sthana/Kaala/Dig）有算法 bug（如 Hora chart method 硬编码错误、Dig Bala 基准点错误等）。`shadbala_pyjhora.py` 在 PyJHora 基础上修正了 9 个子项，使 7 星 rupas 与 JHora 桌面版偏差 < 0.1。
>
> **Why does Shadbala need fixes?** PyJHora's SAV/Dasha/divisional modules are correct, but Shadbala has algorithm bugs in 3 sub-components. `shadbala_pyjhora.py` applies 9 targeted fixes on top of PyJHora's internal functions.

**计算项 / Outputs:**
- 行星位置（经度、星座、Nakshatra）/ Planet positions
- Vimsottari Dasha（大运 + 小运，≤2天精度）/ Dasha periods (≤2 day accuracy)
- Chara Karakas（8K）/ Jaimini Karakas
- 15 张分盘 (D1~D60) / 15 divisional charts
- Shadbala 六力（含 9 项修正 + Ishta/Kashta Phala）/ Six strengths (9 fixes)
- SAV / BAV 吉凶值 / Ashtakavarga
- 尊贵度（Compound Relationship）/ Dignity
- 相位、宫主表 / Aspects, house lords

**精度验证 / Accuracy (tested against JHora, 2 charts):**

| 项目 Item | 结果 Result |
|:---|:---|
| 行星位置 Positions | ✅ 100% 一致 |
| Karakas | ✅ 8/8 |
| D9 Navamsa | ✅ 10/10 |
| Dasha Antardasha | ✅ 9/9 ≤2 天偏差（含 0 天完美匹配）|
| Shadbala Rupas | ✅ 7/7 偏差 < 0.1 rupas (总误差 0.52) |
| SAV 总计 | ✅ 337 (5 星盘验证，3 次重复一致) |

---

### 📖 vedic-reader — 读盘引擎 / Chart Reader

从 PDF/截图/文本中提取出生信息，以calculator生成主数据，再执行交叉验证和16条数学校验。

Extracts birth data from PDF/image/text, generates canonical calculator data, then cross-validates it with 16 mathematical checks.

---

### 🔬 vedic-core — 核心分析引擎 / Core Analysis

P1-P12行星逐一审计 → D9交叉验证 → 宫位诊断 → 十大板块人生总结。正反双审防偏见。

Planet-by-planet audit → D9 cross-validation → House diagnosis → Ten life domains. Double-blind audit against bias.

---

### 💼 vedic-career — 职业蓝图 / Career Blueprint

4Phase 分析：生态位 → 格局 → D9确认 → 全维合成。覆盖 D1/D9/D10 三盘。

4-Phase analysis: Ecological niche → Yogas → D9 confirmation → Full synthesis across D1/D9/D10.

---

### 💘 vedic-love — 恋爱时机 / Love Timing

3Step 分析：体质评估 → Dasha窗口 → 性质定性。婚姻三阶段模型（L7确立 → 9宫法律 → 11宫公开）。

3-Step analysis: Constitutional assessment → Dasha windows → Qualitative definition. Three-phase marriage model.

---

### 💞 vedic-synastry — 合盘 / Synastry

比较两个人的星盘：先中性平扫关系性质，再按 情感/合作/友谊/家人 四框架做五层分析（双盘资格 → 月宿 → 方向叠盘 → 时机 → 六维矩阵）。不给"匹配度%"总分，吸引与承载分开看；纯吠陀判据，需双方各一份盘。

Compares two charts: a neutral scan first, then a five-layer analysis under one of four frames (romantic/business/friendship/family) — dual-chart capacity → koota → directional overlay → timing → six-dimension matrix. No "match %" score; pure Vedic, needs one chart per person.

---

### 📐 vedic-rectifier — 时间校准 / Time Rectification

使用至少5件重大事件，并结合个人特质等结构证据校准出生时间，按分层候选与验证门推进，目标精度
±5分钟。不强制改时间——用户确认后才更新。

Uses at least five major events, together with structural evidence such as personal traits, to rectify birth time through staged
candidate and validation gates, targeting ±5-minute precision. Never forces a time change.

---

### 🔮 vedic-prashna — 卜卦/时盘 / Prashna (Horary)

独立生态位，不需本命盘。默认标准层以 *Shatpanchasika* 为主文本，并通过 KN Rao／Bharatiya Vidya Bhavan 兼容性筛选；以秒级提问时刻和地点起盘，用可审计规则账本回答一个可观察结果的当前成败倾向。Moon 无接触不再被误判为“空亡／不成”，标准层也不会用本命 Dasha、Moon ingress 或今日过运硬给日期。

Standalone module with no natal chart required. Its default layer is rooted in *Shatpanchasika* and compatibility-screened against KN Rao/Bharatiya Vidya Bhavan practice. It preserves the asking time to the second, answers one observable outcome through an auditable rule ledger, and does not treat an uncontacted Moon as an automatic denial or invent dates from natal-style timing tools.

Tajika 十六 Yoga 是默认关闭的过程副层；KP 是默认关闭、必须由用户亲给 1–249 数字的独立栈。两者拥有独立文件、判据和人话判读，不与标准层拼票。已实现路径可以测试使用，但在出版例盘门全部闭合前继续明确标为实验候选；标准层目前也不提供生产级事件日期。

The optional Tajika sixteen-yoga overlay and the separate KP 1–249 stack are off by default, file-isolated, and never vote with the standard judgment. KP requires a user-supplied number. Implemented paths are usable for testing, while both optional stacks remain explicitly experimental until their published-example gates are complete; the standard layer currently does not claim production-grade event dates.

KP 当前的恋情公式只回答“双方是否建立明确确认并持续推进的恋爱关系”。仅恢复
联系、互动回暖、恢复暧昧或秘密心意在起盘前失败关闭；这表示当前没有已核证公式，
不表示现实事件不会发生。

The current KP romance formula only answers whether a mutually acknowledged, continuing
relationship will materialize. Recontact, warmer interaction, renewed ambiguity/flirting, and
private feelings fail closed before casting; unsupported means no validated formula, not denial
of the real-world event.

---

## 📁 项目结构 / Project Structure

```
vedic-astro-skills/
├── README.md
├── CHANGELOG.md
├── LICENSE
├── antigravity/skills/              # Antigravity 版本
│   ├── vedic-calculator/
│   │   ├── SKILL.md                 # 排盘引擎指令
│   │   ├── requirements.txt         # Python 依赖
│   │   └── scripts/
│   │       ├── engine.py            # 主计算引擎 v0.5 (fail-fast)
│   │       ├── setup_env.py         # 环境自动搭建 (10依赖+SAV校验)
│   │       ├── formatter.py         # structured_data 输出
│   │       ├── transit.py           # 过运计算
│   │       ├── dasha_pyjhora.py     # Dasha 精确包装 (≤2天)
│   │       ├── shadbala_pyjhora.py  # Shadbala 修正层 (9项fix)
│   │       ├── divisional_pyjhora.py
│   │       ├── ashtakavarga_pyjhora.py
│   │       ├── extras_pyjhora.py
│   │       └── ephe/                # 星历数据 .se1 (bundled)
│   ├── vedic-reader/
│   │   ├── SKILL.md                 # 读盘引擎
│   │   └── resources/
│   ├── vedic-core/
│   │   ├── SKILL.md                 # 核心分析引擎
│   │   ├── resources/               # 参数/规则/框架
│   │   └── scripts/
│   │       └── report_builder.py    # HTML 报告生成
│   ├── vedic-career/
│   │   └── SKILL.md                 # 职业分析
│   ├── vedic-love/
│   │   └── SKILL.md                 # 恋爱分析
│   ├── vedic-synastry/              # 合盘
│   │   ├── SKILL.md                 # 合盘引擎指令（五层 + QA）
│   │   ├── resources/               # 跨盘相位/月宿/性质盲扫/六维矩阵规则
│   │   └── scripts/
│   │       ├── build_synastry_data.py    # 跨盘计算引擎（纯标准库）
│   │       └── validate_synastry_data.py # 双盘自检
│   ├── vedic-rectifier/
│   │   ├── SKILL.md                 # 时间校准
│   │   ├── requirements.txt
│   │   ├── resources/
│   │   └── scripts/
│   │       └── time_scan.py         # Lagna/D9 扫描器
│   └── vedic-prashna/               # 卜卦/时盘（独立·不需本命）
│       ├── SKILL.md                 # 标准层 + 隔离的 Tajika/KP 工作流
│       ├── resources/               # 来源、题型、规则账本、Moon、Q&A 与可选栈规范
│       └── scripts/
│           ├── build_prashna_data.py    # 标准层独立构建器
│           ├── prashna_time.py          # 秒级提问盘时间与 D1 刷新
│           ├── format_prashna_standard.py
│           ├── calc_moon_vedic.py       # Moon 当前事实（不生成空亡结论）
│           ├── build_tajika_overlay.py
│           ├── calc_optional_tajika.py  # Tajika 十六 Yoga（默认关）
│           ├── build_kp_horary.py
│           └── calc_optional_kp.py      # KP 1–249 独立栈（默认关）
├── claude-code/skills/              # Claude Code 版本 (同上)
├── codex/skills/                    # Codex 原生版本（含 agents/openai.yaml）
├── codex-patch/                     # Codex 执行兼容增强（不包含 skill）
└── scripts/check_skill_parity.py    # 三端逐文件一致性与遗留副本检查
```

---

### 三端一致性检查 / Cross-surface parity check

`antigravity/skills/` 是发布内容基准；Claude Code 必须逐文件一致，Codex 只允许额外
包含每个 Skill 的 `agents/openai.yaml`。修改或同步 Skill 后运行：

```bash
python scripts/check_skill_parity.py
```

The check compares all eight skills, resources, scripts, requirements, and binary ephemeris
assets. It also rejects the removed legacy Claude commands and root-level report builder.

---

## 🧪 技术体系 / Technical Stack

| 项目 Item | 说明 Details |
|:---|:---|
| **流派 School** | KN Rao 体系 (Parashari)，Jaimini 辅助 |
| **Ayanamsa** | TRUE_CITRA / Lahiri |
| **天文核心 Ephemeris** | Swiss Ephemeris via pysweph |
| **精确算法 Algorithms** | PyJHora 4.8.6 (SAV/Dasha/分盘) + 9项Shadbala修正 |
| **分盘 Divisions** | 15 张分盘 D1~D60 (PyJHora) |
| **合盘 Synastry** | 跨盘叠盘 + Ashtakoota 八项 + 六维矩阵（纯吠陀判据，不混西方占星）|
| **卜卦 Prashna** | 秒级提问盘；*Shatpanchasika* rooted 标准层 + 隔离的 Tajika 十六 Yoga／KP 1–249 可选栈 |
| **容错策略 Error Handling** | Fail-fast（不给错误结果）+ `setup_env.py` 自动修复 |
| **校验 Validation** | 16条数学校验（SAV=337、BAV行和常量、Ra-Ke对冲等）|
| **反偏见 Anti-bias** | 正反双审 — 禁止只挑用户想听的数据 |
| **执行引擎 Execution** | 各 Skill 独立阶段门控 + 文件化中间产物 |
| **跨平台 Cross-platform** | Windows / macOS / Linux，Python 3.8~3.13 |

---

## 📋 版本历史 / Version History

| 版本 | 日期 | 亮点 |
|:---|:---|:---|
| **v8.0** | 2026-07-12 | 🔮 **vedic-prashna 卜卦/时盘上线** — 独立生态位（不需本命）+ 纯 Parashari 主判读 + Tajika/KP 沙箱可选层（默认关）|
| **v7.0** | 2026-06-18 | 💞 **vedic-synastry 合盘上线** — 两段式入口（中性平扫 → 关系框架）+ 跨盘叠盘 + 六维矩阵（不给匹配度总分）|
| v6.1 | 2026-06-08 | 🎯 **PyJHora 精确引擎** — Dasha ≤2天 + Shadbala 9项fix + fail-fast + 无fallback |
| v6.0 | 2026-06-07 | 🧮 vedic-calculator 上线 — 原生排盘引擎 + 移植性改造 + 全系统接入 |
| v5.0 | 2026-05-22 | 三阶段执行引擎 + 动态报告打包 |
| v4.0 | 2026-05-10 | 双通道OCR + 时间精度联动 + Rectifier |
| v3.0 | 2026-05-06 | 五Skill架构确立 + 正反双审 |

详见 / See [CHANGELOG.md](CHANGELOG.md)

---

## ☕ 赞赏 / Support

如果这个项目对你有帮助，欢迎赞赏支持：

If this project helps you, consider buying me a coffee:

<p align="center">
  <img src="assets/wechat.jpg" width="200" alt="WeChat Pay">
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="assets/alipay.jpg" width="200" alt="Alipay">
</p>

<p align="center">
  <sub>WeChat Pay（微信支付） &nbsp;|&nbsp; Alipay（支付宝）</sub>
</p>

---

## License

**代码**: [AGPL-3.0](LICENSE) — 你可以自由使用、修改、学习。如果你基于本项目提供网络服务（SaaS），需要开源你的完整服务端代码。

**指令文件** (SKILL.md / prompt 模板 / resources): 附加商用限制 — 个人使用无限制；未经授权不得用于商业服务。详见 [COMMERCIAL_NOTICE](COMMERCIAL_NOTICE)。

简单说：**个人用随便用，拿去卖钱的请先联系我。**

Code: AGPL-3.0 — free to use, modify, study. Network services must open-source their full server code.
Prompt files: additional commercial restriction — personal use unlimited; commercial use requires written permission. See [COMMERCIAL_NOTICE](COMMERCIAL_NOTICE).
