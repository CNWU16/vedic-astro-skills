# 📋 Changelog

All notable changes to this project will be documented in this file.

本项目的所有重要变更都记录在此文件中。

---

## [v8.0] - 2026-07-12

> 🔮 **vedic-prashna 卜卦/时盘上线** — 八Skill架构（独立生态位）

### ✨ 新增 vedic-prashna（卜卦/时盘）

求问者心中有一具体问题、在某刻提问，即以"提问那一刻的时间地点"起盘（Prashna Kundali）答那个问题。不需本命盘，独立生态位。

- **纯 Parashari 主判读**：Lagna / Moon / 相关宫 / Karaka 五步 + 三档结论 + Dasha/Moon Nakshatra 择时（KN Rao 路线）
- **独立生态位**：不接入本命 pipeline，不需 `structured_data.md`；触发后不激活 core/love/career/synastry/rectifier
- **Tajika/KP 沙箱可选层（默认关）**：Tajika 作可叠加副层、KP 作互斥独立栈；计算脚本物理隔离在 `vedic-prashna/scripts/`，engine.py 绝不加异体系字段，主系统 5 个分析 skill 零改动
- **本命交叉可选**：有本命盘时可开交叉，走"矛盾裁决"通道（本命=根盘不违、单向不逆升）
- **产物独立目录**：`prashna_<时间>_<label>/`，产物名 `structured_prashna.md`，与本命 `structured_data.md` 严格区分
- **回归断言**：consistency_lint 第 7 组 4 条隔离断言（engine 无异体系 key、主 skill 无 prashna 术语、产物物理隔离、主系统不反向 import 沙箱）

---

## [v7.0] - 2026-06-18

> 💞 **vedic-synastry 合盘上线** — 七Skill架构

### ✨ 新增 vedic-synastry（合盘）

比较两个人的星盘，回答两人如何互相触发、关系能否承载、何时步调对上。基于 KN Rao（Parashari）+ Ashtakoota 月宿筛查。

- **两段式入口**：先做不预设关系类型的中性平扫（性质指纹）→ intake 选框架 → 五层分析（双盘资格 → 月宿 → 方向性叠盘 → 时机共振 → 六维矩阵）
- **跨盘判据纯吠陀**：整宫落点 + Graha Drishti + 度数标注；无西方 orb / 相位角 / 合成盘
- **不给"匹配度 XX%"总分**：用六维矩阵 + 关系类型，吸引力与承载力分开看
- **支持 romantic / business / friendship / family** 四种关系框架（各有专属读法；非二元友好：A/B 方向，不套性别角色）
- **脚本纯标准库**：`build_synastry_data.py`（跨盘计算）+ `validate_synastry_data.py`（双盘自检），不依赖 calculator 的 venv
- **隐私隔离**：对方的盘与报告放独立子文件夹，不污染盘主个人目录
- 跨盘 DK 用 7K 主表，与 core/love 口径一致

---

## [Unreleased] - 2026-06-09

### Codex 原生支持

- 新增 `codex/skills/`，包含全部6个skill及 `agents/openai.yaml`
- 保持算法、资源和业务规则与Antigravity/Claude Code版本同步
- 仅替换Codex平台所需的文件读取、图片查看、文件写入和安装路径说明

### Calculator-first 数据优先级

- `structured_data.md` 默认以calculator结果为主数据
- PDF/截图/文本用于提取出生信息和交叉验证，不覆盖非Shadbala字段
- Shadbala始终先生成calc基准；无PDF时直接采用calc
- 有同一出生时间的有效PDF时逐行对照并展示PDF值
- 不一致时明确提示“calc与PDF不一致；当前采用PDF”，同时保留calc基准
- 出生时间校准后禁止复用旧PDF Shadbala

---

## [v6.1] - 2026-06-08

> 🎯 **精度修正 + 隐藏 bug 清除 + fail-fast 架构**

### 🔴 修复 formatter.py Shadbala 百分比全错

formatter 使用了不存在的 key `strength_ratio`，fallback 到 `rupas/6.0`（BPHS 每颗星要求不同：5~7）。导致 Mars 显示 99%（弱），实际 119%（中）。**直接误导分析判断。**

- 修复：使用 `strength_pct`（shadbala_pyjhora 直接计算的百分比）
- 新增：Ishta/Kashta Phala 列输出

### 🔴 修复 Sun Ishta/Kashta 计算

Sun 的 Ayana Bala 在 BPHS 中对 Sun 已做 ×2，但 Ishta/Kashta 需要原始值。修复前 Sun Kashta=0，修复后 33.74（PDF: 34.73）。

### 🔴 engine.py v0.5 — fail-fast，移除所有 fallback

- 删除 dashaflow SAV fallback（5/12 星座值不同）
- 删除 dashaflow Shadbala fallback（6 个子项全错）
- 删除自建 Dasha fallback（偏 6~9 天）
- 缺依赖 → `raise ImportError` + 显示 `setup_env.py` 修复指引
- **错误结果比无结果更糟**

### 📖 SKILL.md 大幅更新

- 新增 engine 返回数据结构文档（~90 行，每个 key 有说明）
- 新增 SAV 验证代码示例（防止 agent 用错 key）
- 新增规则：**禁止自己手写 print 来读取 chart 数据，必须用 formatter.py**
- 技术规格更新为 v0.5 实际架构

### 📊 精度验证（2 星盘三方对比）

| 项目 | Raw PyJHora | 修正版 (9-fix) | 改善 |
|---|---|---|---|
| Shadbala 总误差 | 3.75 rupas | 0.52 rupas | 7.2x |
| BAV 小项 | — | **84/84 完美匹配** | — |
| SAV 12 星座 | — | **12/12 完美匹配** | — |
| Dasha | — | **27/27 ≤2 天** | — |

### 🔧 formatter 输出全量 Antardasha

之前只输出当前+下一大运的 Antardasha（2×9=18 条），纯 calc 用户缺少过去大运的时间窗口，无法做验前事时间扫描。现在输出全部 9 段大运的 Antardasha（9×9=81 条）。

### 📋 验前事 SOP 强制展示

之前 agent 在内部思考中完成信号池筛选，只输出最终 3-5 条推断。现在强制要求完整展示：
- 8 项预分析数据汇总表
- 候选池 A-H 逐项多维评估（P1/P1.3/P5 + 选入/跳过原因）
- 最终选择表（信号强度评级）
- 检查清单结果

### 🧠 四通道 AD 时间事件分析（基于 xiaobo 盘教训）

之前只用通道1（宫主身份）选 Antardasha，导致验前事时间事件命中率低。基于实际误判案例引入四通道：
- 通道1: 宫主身份（谁管那个宫）
- 通道2: 落宫激活（坐在哪个宫 → 该宫被激活）
- 通道3: 天然象征（Rahu=异地、Jupiter=扩张等）
- 通道4: Chara Karaka（8K 身份）

新增大运语境原则：AD 信号要在 Mahadasha 语境下解读。

---

## [v6.0] - 2026-06-07

> 🧮 **vedic-calculator 原生排盘引擎上线** — 六Skill架构完成

### ✨ 新增 vedic-calculator

**从零到一的原生排盘引擎。** 给出出生日期、时间、地点，直接计算完整星盘。无需安装 JHora 或任何第三方占星软件。

- **engine.py** — 主计算引擎，基于 pysweph + PyJHora + dashaflow
- **行星位置**：经度、星座、度数、Nakshatra（含 pada 和 lord）
- **Vimsottari Dasha**：9段大运 + 当前大运的9段小运
- **Chara Karakas**：8K 体系，含 DK 7K/8K 差异标注
- **分盘计算**：15 张 D1~D60（PyJHora 原生）
- **Shadbala 六力**：含9项修正的修正层（shadbala_pyjhora.py, 494行）
  - 修正 Hora Bala、Dig Bala、Paksha Bala、Tribhaga Bala 等 PyJHora 已知缺陷
- **SAV / BAV**：Ashtakavarga 吉凶值（SAV 总和恒等于 337）
- **尊贵度**：Compound Relationship（via dashaflow）
- **相位、宫主表、过运**
- **formatter.py** — 输出 structured_data.md，与 reader 格式完全兼容

### 🔧 移植性改造

- **setup_env.py**：跨平台环境自动搭建（Win/Mac/Linux）+ SAV=337 校验
- **路径动态检测**：全部硬编码路径改为 `import jhora` → `__file__` 动态发现
- **Python 3.8~3.13 全面支持**：pysweph 有 cp38~cp313 预编译 wheel

### 🔄 全系统接入

- **vedic-reader**：当 calculator 已安装时，reader 自动调用 calc 补充数据
- **vedic-core**：所有 Shadbala/SAV/BAV 引用统一走 calculator 计算
- **vedic-rectifier**：requirements.txt 同步更新
- **README**：全面重写为双语版（中/英），架构图更新为六Skill

---

## [v5.0.1] - 2026-05-24

> **社区反馈修复** — BOM修复 + Nakshatra校验 + Ayanamsa检测

### Reader
- 修复 SKILL.md UTF-8 BOM 导致 Claude Code frontmatter 解析失败
- 新增 Ayanamsa 被动提醒 + 主动检测（搜索 Lahiri/KP/Raman/Pushya）

### Rectifier
- 新增 Step 3d Nakshatra 边界校验（D9精调后检查 ±2° 边界）

---

## [v5.0] - 2026-05-22

> **执行阶段化重构** — 三阶段引擎 + 动态报告打包

### Reader
- 执行阶段化：连续 Steps 拆分为3个独立执行阶段，每阶段独立思考链
- 渐进写入：structured_data.md 分3次写入，防超长思考崩溃
- SAV铁规：只接受用户主动粘贴，不从 PDF 自行提取

### Report Builder
- 动态文件发现：3轮扫描（精确匹配→前缀分组→QA glob）
- 支持任意分段文件后缀

---

## [v4.9] - 2026-05-14

> **验前事定版** — SOP多维评估 + SAV映射铁规

- SAV→Bhava 映射公式明确化
- 验前事 SOP：候选池 A-H 多维评估 → P1/P5工具箱 → 3-5条
- 分盘提取门控(Path B)：D10/D4/D5 必须用户截屏确认
- 校验规则扩展至16条

---

## [v4.0] - 2026-05-10

> **工程化重构** — 双通道OCR + 时间精度联动

- 强制双通道 PDF 提取（文本层 + AI视觉交叉验证）
- 时间精度→分盘启用矩阵
- 校验规则 12→16条（燃烧、行星战争、Sandhi/Gandanta、盈月亏月）
- Rectifier 防过度校准规则

---

## [v3.0] - 2026-05-06

> **五Skill架构确立**

- reader / core / career / love / rectifier 五Skill上线
- 正反双审 (Double Blind Audit) 机制
- D9身份继承矩阵五维分析
- Badhaka/Maraka 审计模块

---

## [v2.x] - 2026-05-05

- Q&A规则外置 (qa_rules.md)
- HTML报告生成脚本 (report_builder.py)

---

## [v1.x] - 2026-05-04

- 初始三Skill架构（core / career / love）
- 验前事反转：AI先预测，用户确认
- 十大板块白话文总结模板
