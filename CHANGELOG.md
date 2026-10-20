# 📋 Changelog

All notable changes to this project will be documented in this file.

本项目的所有重要变更都记录在此文件中。

---

## [Unreleased] - 2026-10-20

### 即时盘判读改造：按占优断合判、判读单讲事情怎么走、*Prasna Marga* 有条件进主层 ⚠️ 判读口径与判读单格式变化

**起因**：按旧 rubric 字面编码，三地两年 85228 盘，各题型“悬”占 54–88%；达标考试、复合等单主规则题型结构上
永远判不出“不成”；33% 的盘问 10 类事有 8 类以上都是“悬”；求职有一半的日子整天问不出“成”。根子是只实现了
《五十六偈》单偈规则，又自定了“凑两条才不成、一冲突就悬、`P-I.3` 一票否决”。同一系的 *Prasna Marga* 本来就
在单偈之上做权衡和叙述式解读。

- **合判**（`judgment-rubric.md` §2–§4）：账本每条适用规则一份证据，有利 +1、不利 −1、混合 0，等权；合计 >0 偏成、
  <0 偏不成、=0 持平（输入敏感也记持平）；强度分顺／有阻力、明确／有转机。依据：Ayer I.4／III.4／IV.5 注的偈内
  占优、`M-XIV.98`“prediction must be made according to the predominating factor”、`M-XVII` 注 Raman 判婚事按多数
  与正负条数。数法明写为执行口径。几乎每偈原文自带反向结论，取消“至少两条独立不利”。`P-I.3` 作一份证据计分，
  不再一票否决。同源只计一次（买房 Vriddhi 与 4 宫 `P-I.3`）、反向同源不计（出行不收 10 宫 `P-I.3`）。
- **账本**：II.1 星座类型与 II.2 照射拆成两条（两偈；推翻 10-11 撤回——当时缺合判出处，现出处见上）；失物主规则
  改 `P-VI.3`（Bhattotpala 注“chances of recovery are remote”），`P-I.5` 只讲快慢不计分；出行按 Ayer 示范题分三行：
  能否办成走 `P-I.4`、路上顺不顺走 `P-II.5`、会不会离开走 Pravasa；新增“表白／确立关系”行（`P-I.4` + 7 宫 `P-I.3`
  + `M-XVII.5／15／16／17` 婚姻卜问类比，B 级）；结婚加同四偈；求职“满意的 offer”用 IV.3 后半句讲待遇，不计分。
  “同向检查”列改名“辅助规则”。
- ***Prasna Marga* 准入**（`standard-layer.md` §1）：由“默认不进入”改为有条件进入——逐偈核原文、只用白名单数据、
  专题条只用于对应题型；不收寿命、死亡、贞洁、子女夭折、相貌，以及征兆、触碰部位、Arudha、Gulika、Thrisphuta、
  Yama Sukra、仪式补救。Prasna Dasa（VI.39、65–67）与 XIV.83／86／88 核原文后维持不收，理由写进核证矩阵。
- **判读单**（`SKILL.md` Phase 6）：给用户看的部分改为标题、副标题、正文三段，贴着题目情境写，不出现“成／悬／
  不成”和内部档名等判词；盲读标题副标题须能分辨倾向，每句判断对得上账本；关怀条款加偏不成不下死结论、不归咎
  提问人、考试照常准备、输入敏感说人话。内部档与计分账本放核对区（“四、时间”编号不变）。
- **时间副层**：档名改为偏成／持平／偏不成；持平写条件式“如果推进顺利，大约……”；正文把主时间与触发日合成
  一句；婚恋题加 `M-XVII.31` 作“偏早”提示，不改日期。
- **脚本**：`build_prashna_data.py`、`build_timing_overlay.py`、`calc_timing.py`、`format_prashna_standard.py`、
  Tajika／KP 两个计算脚本只改输出文字里的档名与持平时间前缀，算法不变；隔离与算例测试全绿。
- **基础率**（未计输入敏感）：14 个高频问法 11 个达到验收线（偏成≥20%、偏不成≥20%、持平≤40%），如求职 31/24/45、
  竞争考试 42/23/35、表白 40/25/35、复合 36/17/47、疾病 30/20/51、失物 45/21/33；同一张盘八成以上题目结论相同
  不到 1%。未达标的三行：对方会不会联系（只有一条证据，21/49/30）、路上顺不顺（八成盘此偈无读数）、会不会离开
  （Pravasa 原文“only when”，4/46/50）。
- 三语 README 的即时盘段落同步；删去已过时的“不提供生产级事件日期”。

### rectifier `time_scan.py`：`--tz` 改填时区名，夏令时与本命盘同口径换算 ⚠️ 不再接受数字偏移

**起因**：`--tz` 原为固定数字（SKILL 示例写"中国=8"），不按夏令时换算。中国 1986-1991 年夏季实际是 UTC+9，
按钟表时间传 8，扫描中心会比本命盘晚 1 小时。实测上海 1988-07-15 10:00：`--tz 8` 得 Virgo 151.67°，本命盘 engine
（Asia/Shanghai）是 Leo 138.73°，默认 ±30 分钟的扫描范围覆盖不到真实时间。已有一例实盘首扫因此重扫。本命排盘 engine
和即时盘脚本一直按时区名换算，不受影响，未改。

- `--tz` 改为填 IANA 时区名，和排本命盘用的同一个；用户声明标准时，就填排盘时用的同一个固定时区（如 `Etc/GMT-8`）。
  换算用 pytz `localize(is_dst=None)`，和 engine `_localize_strict` 同口径：落在夏令时切换的跳过／重复时段直接报错。
  传数字偏移（`8`、`5.5` 等）直接报错，并提示改填时区名。
- 两点法 Dasha 的段首、段末各按当时的实际偏移换回本地时间。
- 表头「基准」加时区名、实际偏移和夏令时标记。
- SKILL.md：两处调用模板和 `--tz` 说明改为时区名；读结果新增 Lagna 核对：扫描表里对应 structured_data 出生时间的那一行，
  Lagna 须与 structured_data 一致，不一致即停。
- 回归：上海夏令时、上海跨零点、纽约夏季、新德里、`Etc/GMT-8` 五例，`+0min` 行 Lagna 均与 engine 一致；三个非夏令时
  例与旧版数字入参的输出逐行相同（含两点 Dasha），既有扫描结果不受影响；切换时段和数字入参均按预期报错。
- 脚本新增依赖 `pytz`（calculator 三个核心依赖之一，随环境自检安装）。
- 两仓 shared 同步，`consistency_lint` 全绿。

---

## [Unreleased] - 2026-10-11

### 即时盘“不成”按题目规则计数；疾病同向限动／固座

**起因**：用新口径复跑同一天起的 5 张盘，面试题全部落悬。追查时查出 §5“不成”按字面只数主规则，单主规则题型
（疾病、竞争性考试）永远凑不齐；疾病行同向写法与执行要点不一致。脚本、engine、数据契约不改。

- **不成计数**（rubric §5 第 1 条）：“两条相互独立的主规则”改为“两条相互独立的题目规则”，题目规则指 taxonomy 表中本题
  “主规则”“同向检查”两列；`P-I.3` 除外，它是 §3 第 2 条、§5 第 3 条的一般规则，计入会重复计票。SKILL Phase 4、
  契约 §5、rubric §11 同步。
- **疾病**：同向检查写明只取 `P-II.1~2` 动／固座（taxonomy 表、事项宫表）。删去“`P-I.2` Nivritti 可选”：Ayer 在 I.2 注
  只泛称 Nivritti 宫“for the fulfilment of almost all desirable events it is examined”，没给病题读法，同向检查列现计入 §5，
  “可选”无判据。`P-IV.5`“彼此相照”按标准层“七曜互视”行判，同宫不算互照，只有一颗吉星不算满足；正反配置任一完整成立
  且不混对方成分才直接定方向，其余按 §4.1 数（执行口径）。代他人问病同样读 1 宫（Ch.4 示范题 5“My brother is seriously
  ill; will he recover completely?”挂本偈）。
- **其他**：核证矩阵 `P-II.1~2` 行补“竞争性考试的主规则”；`standard-layer.md` §2.1 写明 `P-II.2` 只读第 1 宫行与 Moon
  所在宫行的“七曜照射本宫”列，同宫不算照（原文“Benefic aspects to the lagna and the Moon-lagna”）。
- 订正 2026-10-10 条目：照射子句只用于求职、考试，疾病只用动／固座。
- **已知未改，待议**：逐日粗估两年（Lahiri、正午、自然吉凶加 F1）约 46% 的日子 Moon 所在星座受凶星照，这些日子
  `P-II.1~2` 最多是混合，求职、竞争性考试最多判悬。原文 II.2 注只说吉凶同照“mixed in character”，没给它与
  `P-IV.3` 的合判法。同日曾试行“求职两条主规则一条有利、另一条混合判成（困难后成）”，属自创，已撤回。

---

## [Unreleased] - 2026-10-10

### 即时盘混合配置按原文占优定局；II.1~2、I.2、IV.5、VII.2 等逐偈对原文补漏

**起因**：rubric 把 `P-I.4` 的“困难后成”归进“悬”，原文写明由占优定局的混合配置（I.4、III.4、IV.5 注）也一律落悬，
判读单大量出“悬”。逐偈对 Ayer 原文复核时另查出若干漏收条件和出处错位。脚本、engine、数据契约不改。

- **占优数法**（`judgment-rubric.md` 新增 §4.1，执行口径）：只用于原文写明占优定局的 `P-I.4`、`P-III.4`、`P-IV.5` 注。
  数所看宫在宫表“七曜占据”“七曜照射本宫”两列的吉凶标签（F1 宫主记吉，盈月未定与 Rahu／Ketu 不计）：吉多记
  “有利（困难后成）”按成判；凶多记偏不利，判不成仍须 §5 两条独立不利，凑不齐判悬；持平判悬。Chyuti 变动座按同法数，
  是事件方向，问“保住”时反向。原文没给占优的规则（`P-II.2` 吉凶同照、`P-I.3`）混合照旧。
  `standard-layer.md` §5、SKILL Phase 4、rubric §2／§3／§4／§5／§11 同步；`ja-prashna.md` 加“困難を経て成立する方向”。
- **`P-II.1~2`**：补正文“凶星照则凶”与吉凶同照为混合；变动座按注引 Bhattotpala *Prasnagyana* 分前后半（前半按固定座、
  后半按动座，近 15° 算输入敏感）。Ayer 注逐题型的例句（住处、出行、失物、失踪者、疾病、名誉）作动／固座同向检查，
  写进 `question-taxonomy.md` §2.12 各题；照射子句仍只用于求职、考试。
- **`P-I.2`**：Vriddhi 补“unspoiled by other planetary dispositions”；返回题补 4 宫两说（正文“有行星落 4 宫”，
  注“4 宫主占据或照 4 宫”），并列。
- **`P-IV.5`**：原写“Bhattotpala 注：反之不利”，出处错位——Bhattotpala 只补吉星彼此相照，“相反”“占优”是 Ayer 注。改正并接占优数法。
- **婚姻**：主规则改为 `P-VII.2`（Moon 落 3／5／7／11／6 宫受 Jupiter、Sun、Mercury 照，或吉星落角宫／三方宫），
  `P-VII.1` 作同向；“Sun”疑为 Venus 误印，无梵文无法核实，照录。
- **其他原文条件**：`P-II.11` 两处原文都是“and”，按字面同落；`P-IV.2` 人形座按本偈正文三座（不加 Virgo），
  `P-III.3~4` 按 III.3 注四座；`P-IV.1`、`P-IV.5` 补“配置相反则结果相反”；`P-IV.3` 补吉星落 2／5／1 宫得名利，作名誉同向；
  `P-III.4` 补“吉凶混落则僵持，吉占优趋向解决”；`P-V.3` 注“不可弱”按 D1 `debilitated`；I.5、VI.3 的“强吉星”按
  `exalted`／`own_sign`；Laghu Jataka（8、12 宫无吉）不收。
- `house-karaka-map.md` A／B 级行同步（买房、出行、返回、失物、婚姻、求职、投资、开庭）。

### 排盘环境补 tzdata（即时盘在 Windows 上起盘失败）

**起因**：`vedic-prashna` 的 `prashna_time.py`、`calc_timing.py` 用标准库 `zoneinfo` 处理时区，KP 副层还要用它做
带时区的时间加减（推大运起点、逐步搜过运）。macOS／Linux 自带系统时区库；Windows 没有，必须装 `tzdata` 包，
否则 Phase 1 报 "No time zone found with key Asia/Shanghai"。原安装清单只有 `pytz`，漏了它。
本命盘全程用 `pytz`，不受影响，不改。

- `setup_env.py`：`REQUIRED_PACKAGES` 末尾加 `tzdata`（第 10 项，不改原编号）；`validate()` 加 `ZoneInfo('Asia/Shanghai')` 加载检查。
- `check_env.py`：依赖检查加同一项。
- `requirements.txt`：手动安装命令与依赖列表加 `tzdata`。
- `SKILL.md`：依赖行与环境自检说明补 `tzdata`。
- 已装好环境的用户重跑 `setup_env.py` 即可补上。

### 即时盘副层边界：Tajika 不运行条件 + KP 不收时的出口

**起因**：Tajika 副层只看问者星（Lagna lord）与唯一事项宫主的直接接触。查表题、不判题没有事项星；
事项宫为 1 宫（主动挽回、裁员／保工作、病能否好、考试）或与 Lagna 同一座主时，两颗是同一颗，脚本直接拒绝，
旧文本没说这时怎么回答，容易拿 Karaka 或别的宫主顶替。KP 只收两类题型，其他题型在脚本入口被拒，用户看不到白话说明。
算法不改。

- **Tajika 不运行条件**（`tajika-optional.md`）：上述三种情况不运行、不生成 `tajika_overlay.md`，用一句白话说明
  副层不适用及原因，主答案以标准层为准，不拿 Karaka 或其他宫主顶替。原典对主星相同的处理未核，失败关闭。
  SKILL Tajika 段、`qa_rules.md`「后加 Tajika」同步。
- **KP 不收时的出口**（`kp-optional.md` 新增节）：题型不在已收表或 outcome scope 失败关闭时不起 KP 盘，固定回答三点——
  暂不收及原因（当前来源没有对应公式，不表示事情不会发生）、可改用标准层（复合／联系走 §2.7）、或换成 KP 已收的两类问法；
  只给选项，不替用户切换，不把问题改写成已收题型。SKILL KP 段、`qa_rules.md` §5 第 4 步同步。
- **隔离断言 7**（`tests/test_prashna_isolation.py`）：标准层（builder、formatter、Moon、时间工具）不导入 Tajika／KP；
  Tajika 与 KP 互不导入；KP 不借用标准层的格式化与 Moon 段。

### 即时盘示范题修复：吉凶改按 Ayer 功能口径；Ayer 示范题题型补齐；描述题与天气查表（取代下方即时盘条目的"吉凶口径""裁员""竞争性考试"三处）

**起因**：逐题对照 *Shatpanchasika*（Ayer 译本）各章示范题后发现三类问题：吉凶口径与 Ayer 注相反
（他在 I.3 注明确按功能取吉凶，旧版只读了他引用 Bhattotpala 的那半句）；裁员、竞争性考试挂错规则；
大量示范题问法（房屋、出行、返回、疾病、名誉、谈判、失物、胎儿性别、父亲下落、天气等）没有归行，
只能按"最像的宫"硬判。本批全部按原文示范与注释改写，没有原文依据的不写。

- **吉凶口径**（`standard-layer.md` 新增 §2.1）：从被占据／照射的星座起数宫，按 Ayer I.3 注三条依次取标签——
  F1 本宫主恒吉；F2 同管第 3、12 宫且落陷为凶（注例一 Jupiter 对 Capricorn）；F3 同管角宫与三方宫且
  `exalted`／`own_sign` 为吉（注例二 Mars 对 Leo）；其余回落 Bhattotpala 自然吉凶，标"(回落)"。
  回落时 Mercury 与 Sun／Mars／Saturn 同宫为凶，Moon 亏月为凶、盈月记"盈月未定"；Rahu／Ketu 不贴标签。
  正文点名行星且 Ayer 无注的偈按点名判，不换标签。标签由 formatter 写进宫表，判读只查表。
- **IV.3 Moon 条款**按原文"(Malefic) Moon"：Moon 落 Lagna 只在亏月记不利；落 10 宫不论盈亏都有利。
- **求职／考试**（§2.8）：裁员／调岗／换工作改走 `P-I.2` Chyuti（Ch.1 示范题），A 级，事项宫 1，问"能否保住"时方向相反，
  不用 `P-II.2`；竞争性考试改为 `P-II.1~2` 主（Ch.2 示范题挂靠）、`P-III.1` 同向，B 级。
- **其他专项**（`question-taxonomy.md` 新增 §2.12）：A 级——失物能否找回（`P-I.5`，`P-VI.3`、`P-V.1` 同向，11 宫）、
  买房（`P-I.2` Vriddhi，4 宫）、出行（Pravasa，10 宫）、在外者或失踪者返回（`P-V.1~3` 等，7 宫）、
  病能否好（`P-IV.5`，1 宫）、名誉（Vriddhi，4 宫）、谈判和解（`P-III.3~4`，7 宫）；B 级——投资（`P-IV.2`）、
  亏损补回（`P-V.1`）、官司会否很快开庭（`P-II.11`）；查表——胎儿性别（`P-VII.1`）、父亲是否在外地（`P-VII.12`）。
- **描述题与天气**（§2.10／§2.11）：失物在哪、方向距离、是什么、谁拿的（`P-VI.1~2`、`P-VI.4`、`P-I.7`、`P-VII.13`），
  雨季会不会下雨（`P-VII.3~4`），只给原文查表结果，原文歧义两说并列，不出三档、不跑时间副层。
- **不判**（§2.13）：生死寿命、读心与他人隐私、父亲以外亲属下落、继承、选举、职位竞争。
- **数据层**（`format_prashna_standard.py`、`calc_moon_vedic.py`）：宫表"七曜占据""七曜照射本宫"两列带吉凶标签；
  D1 末列改名"自然吉凶（Bhattotpala，回落用）"；rising Navamsa 加本座序号与座主标签；Moon 节加 tithi 与满月窗
  （`P-I.5` 注：白半月第 10 至黑半月第 5）；新增"描述题与天气查表事实"一节。
- 时间副层事项宫表按新题型拆行；描述题、天气、胎儿性别、父亲下落不运行时间副层。
- 隔离回归测加标准层算例（F1～F3 与回落、亏月 Moon、满月窗边界、`P-VI.4` 距离、`P-I.7` 物品属性）。

### rectifier 改为两腿等权 + 新增出题规范 `calibration_quiz.md`（方法学，影响校时裁决；取代下方"证据分三类"条目）

**起因**：两腿不对称让"事实与特质"整条腿只能验证、不能决胜，分不出时只能等外部锚或强制盲审，
多数用户手里没有出生手环、医院记录，校准就卡住；同时出题规则只存在于 codex 侧补丁，其他平台出的题分不开候选。

- 证据回到两条腿、**等权计分**：腿一 = 事实与特质（不带日期）× 候选间变化的静态盘面字段；
  腿二 = 带日期事件 × Dasha（两点法）。合计进总分、定 Lagna 门槛、裁决定序。
- 护栏改为"计分资格看区分度"：预登记、只计变化字段、同源去重、淘汰三门槛、Dasha 不得复活；
  泛画像、自我感、关系好坏、氛围、性格不直接计分，留作出题素材。
- 每层统一流程（D1 / D9 / D10 / D4 / D5 / Nakshatra 边界通用）：列变化字段 → 腿一预登记淘汰 →
  腿二（精调层只在腿一差 <2 且 Dasha 归属有变时查）→ 合计差 ≥2 定、<2 出题 → 无新角度则欠定，
  给最佳估计 + 低置信标注。
- 新增 `resources/calibration_quiz.md`：出题七步（差异清单 → 对立预测 → 选题型 → 写成 A/B/0 → 五检 →
  组批与作答前锁定 → 发题）；五检 = 对调检、混杂检、基础率检、已知检、可答检；底稿写入工作目录
  `rectification_quiz.md`；有效题每题 1 分计入腿一，选 0、答不上不计分，答不上就撤题。
- 删去防线"越完美越可疑"与"临界/欠定盘强制盲审"；Step 5 盲审与外部锚都改为可选。
- `event_house_map.md`「静态事实映射」改为常用示例，表外事实按「核心映射」取宫、现场预登记。
- reader 验前事「决胜票」与 `pre_validation_sop.md` 同文副本同步：两腿皆可决胜，评价类不直接决胜、改出题；
  时间可信度"欠定 / 临界待锚"改为"欠定（最佳估计+低置信）"。

### 即时盘：成／悬档加时间副层；新增复合、求职／考试专项门控与情感安抚规则

**起因**：标准层原先不给任何时间，用户最常追问的"大概什么时候"只能答"不支持"；复合、求职、考试三类高频问题
没有专项归行，容易按"最像的宫"硬判。时间副层的每条算法都已对照 *Prasna Marga*（Raman 译注）与
*Shatpanchasika*（Ayer 译本）原文核过。

- **时间副层**（新增 `vedic-prashna/resources/timing-layer.md`、`scripts/calc_timing.py`、`scripts/build_timing_overlay.py`）：
  只在成、悬两档运行，不成档不给时间；成写"约……"，悬写"如果能成，大约……"。四个候选：
  - T1 `P-V.5`：从 Lagna 顺数到第一个有七曜的宫，宫数 × 12 天；只用于人的归来／到达题；
  - T2 `M-XIV.85`：从事项宫数到其宫主所在宫（含首尾）；宫主在 7–12 宫按天、1–6 宫按月（Raman 注的假设，输出时注明）；
  - T3 `M-XIV.85`：Moon 下次进入事项宫主所在星座，作最近的触发日；事项宫主就是 Moon 时不适用；
  - T4 `M-XIV.82`：上升 Navamsa 主星的时间单位 × 该星在本座第几个 Navamsa，只作参考。
  
  候选结果不同时并列，不平均、不折中。时间不进规则账本、不改三档；不用提问盘的 120 年 Vimshottari、
  Chara Dasha 或过运；与 Tajika、KP 的时间不互相校正。标准 builder 不导入时间副层，产物另写 `timing_overlay.md`。
  判读单"四、Timing 状态"改为"四、时间"，白话字段改为"大概什么时候"。
- **复合／联系专项**（`question-taxonomy.md` §2.7）：能否复合按 `P-III.3~4` 和解规则类比（B 级），人形星座取
  Gemini、Virgo、Libra、Aquarius（III.3 Ayer 注）；对方会否联系／回复 `P-I.3`（B）；主动挽回 `P-I.4`（A）；
  "还爱不爱我""对方和现任会不会分手"为 C 级不判；打听行踪、"怎么让他回来"等操控／打听类不判，一句话说明并给替代问法。
  同一段关系的不同问法算同一问题，沿用第一张盘的结论。
- **求职／考试专项**（§2.8）：找工作／offer／面试／升职 `P-IV.3` + `P-II.1~2`（A）；裁员／保工作 `P-II.1~2`（B）；
  竞争性考试 `P-III.1` 类比（B）；达标性考试 `P-I.4`（A）；"面试表现如何"为 C 级，改问"能不能拿到这个 offer"。
  多环节只问最近一个还没出结果的环节；面试卡点只说卡在自己这边还是职位那边，不从盘里读性格、口才等特质。
- **走失宠物**按失物 `P-I.5`（Ayer 示范题 "My cattle have strayed away from home"），只判能否找回。
- **情感安抚六条**（SKILL Phase 6）：只安抚一次、不用套话；追问不重复；安抚不改结论；有盘面依据；
  操控／打听类不说教；出现自伤或极端语句先回应安全，不起盘。
- Ayer 注中按 functional character 取吉凶的主张不采纳：标准层按 `P-I.3` 用七曜自然吉凶
  （Ayer 在 I.3、I.4 注里也写明 Bhattotpala 取自然吉凶）。
- 隔离回归测由 4 条断言扩为 6 条（新增：标准 builder 不导入时间副层；时间副层不导入 Tajika／KP），
  另加时间副层原典算例（Raman 注 XIV.82、XIV.85 两例，`P-V.5`，Moon 入座搜索）。

### 产品回灌：SOP 预分析清单口径对齐 + 五大贤者格局中文正名（措辞，无数值变化）

- `vedic-rectifier/resources/pre_validation_sop.md` 构造SOP 步骤1 的预分析清单「相位(第3项)」改为「Graha Drishti(第3项)」，
  与 reader Step 4 读取清单一致（西占 orb 表已于 2026-07-07 删除，旧写法指向不存在的数据结构）；
  同文件「霈月级」错字改「需月级」。reader 内嵌的同文副本同步修改。
- `vedic-core/resources/yogas.md` 五大贤者格局五条补中文正名：火星/水星/木星/金星/土星贤者格局（英文名照带）；
  `vedic-career` 的「五大伟人」统一为「五大贤者格局」。

### core 新增 Step 4.5 措辞落点校订：报告写完后读 user_context，只改措辞（不改结论）

**起因**：原规则只有 Step 1-3 禁读 user_context、Step 4 段内又写"仍禁读"，两处口径不一；且报告全程看不到用户背景，
丧亲、离异等敏感经历会被模板化措辞直接撞上（如对已故的人写"多沟通"）。

- core 分析期 user_context 禁读统一为 Step 1-4；新增 Step 4.5 为唯一例外：p5a/p5b 写盘后读 user_context，
  只改这两份的措辞与落点，窗口、领域、配偶画像主形态、Yoga/Dasha 判断与数据表一字不动；无 user_context 则跳过。
- 敏感经历按十个固定类目在内部归类（不落盘），过伦理检查四项（丧亲 / 创伤 / 自我伤害史 / 矛盾）；
  标签本身不出现在报告里，禁"根据你的背景""你提到"一类复述与工序口吻。
- 背景不当盘面证据：不新增任何星盘判断；同盘不同背景，结论逐字同级。
- reader 的 user_context 权限表同步：core Step 4.5 只读不写。

### rectifier 证据分三类：静态事实升为结构硬腿，先剪枝再比 Dasha（方法学，影响校时裁决）

**起因**：原主纲把证据二分为"硬腿 = 事件×Dasha / 软腿 = 特质×结构"，父母早年离世、兄弟姐妹、职位权责这类
第三方可核的静态事实也被归进软腿，不能决胜；精调层候选只差几分钟、MD/AD 相同时仍会先去查 Dasha。

- 证据改三类：**结构硬腿**（客观静态事实 × 候选间变化字段）/ **时间硬腿**（带日期事件 × Dasha）/ **软腿**（关系、氛围、性格等评价性特质）。
  软腿不破硬腿平局的铁则不变。
- 结构硬腿护栏：规则只取 `event_house_map.md` 新增的「静态事实映射」节，对照前预登记；只计候选间变化的字段；
  淘汰需过三门槛（事实可核且确认 + 该行标"可淘汰" + 全部指征同向否定），首版只开放父/母早年离世两行，其余只扣分；
  被淘汰候选不得用 Dasha 复活。
- 裁决定序加第 0 步"结构淘汰"；总分 = 结构 + 时间，软腿不计。D1 顺序为"静态先剪枝 → 存活者再比 Dasha"。
- 精调层：MD/AD 在候选间相同就默认不查 Dasha；该级硬腿主要是结构硬腿 × 分盘变化字段（D9 婚育、D10 职位权责）。
- 3d Nakshatra 边界：订正"Lagna Nakshatra 主星不同 → Dasha 起算不同"的错误前提（Vimsottari 按 Moon 起算），
  改为只在【Moon跨Nak】或 MD/AD 归属变化时才查 Dasha。
- Step 2 采集模板加"客观事实"一栏，并要求先取 structured_data / user_context 已有信息、只问缺失项。
- reader 验前事「决胜票」与 `pre_validation_sop.md` 同文副本同步：经确认的结构硬腿也可决胜。

### rectifier `time_scan.py`：本地时间入参 + 表头双时间（修 UTC 日期借位坑）⚠️ 影响校时结果

**现象**：08:00 前出生（本地时:分 < 时区偏移）的盘，调用方手算 UTC 时只做钟面减法、没把日期退 1 天，
整张扫描表 Lagna/D9/D10 系统性偏移。产品侧在金标准盘 GC-01 实证：本地 1995-05-06 02:30 UTC+8，
误传 `--date 1995-05-06 --time 18:30`，offset=0 行 Lagna 差 1.39°、D10 由 Gemini 错成 Cancer。

- `time_scan.py` 新增 `--local-date/--local-time`：脚本用 `timedelta` 按 `--tz` 自己换算 UTC（自动借位）；
  与旧的 `--date/--time`（UTC）二选一，缺一半或两套同传直接报错。
- 表头「基准」同时打印 UTC 与换算回去的本地时间，调用方可肉眼核对。
- SKILL.md 两处调用模板改用本地时间入参；「出生时间需转为UTC」一节改为禁止手算并给出借位实例。
- 回归：本地入参与正确手算 UTC 的扫描表逐行一致；旧的错误输入在表头显示为「本地 05-07」，可当场发现。
- 两仓 shared 同步，`consistency_lint` 全绿。

---

## [Unreleased] - 2026-09-04

### engine v0.9：D1 星历基准统一 + Vimsottari 年长漂移修复 ⚠️ 有数值变化

**一张盘此前分属两套星历基准。** engine 自算 D1 用 `FLG_SIDEREAL|FLG_SPEED`（65792，视位置），
而 SAV / D9 / Dasha 等走 PyJHora 的部分用 `drik.PLANET_FLAGS`（66386，真位置 + 无章动 + 无引力偏折）。
同一张盘的行星表与其余分盘因此差 0~60″。

- 统一到 PyJHora 一侧（`engine.PLANET_FLAGS`）——该侧是当年逐项对照桌面 JHora 验证过的那一半；
  SKILL_LOG 既有记录：加 `FLG_TRUEPOS` 后七星对桌面从 −15~−59″ 收敛到 ≤1″。
  实测 `engine.PLANET_FLAGS == drik.PLANET_FLAGS == 66386`，同 jd 同星差 0.000000″。
- `calc_lagna` **不改**：`houses_ex` 只识别 `FLG_SIDEREAL`，其余位对 Lagna 无效，原写法已等价。
- `transit.py` 改为复用 `engine.PLANET_FLAGS` 与 `engine._ensure_swe_state()`——消除过运侧的第三套基准，
  并补上原先缺失的 `set_ephe_path`（该文件此前只设 `set_sid_mode`，子线程里会静默退回 MOSEPH）。

**Vimsottari `year_duration` 是 PyJHora 的模块全局，初值为平均恒星年、仅在 L2 更新为真恒星年。**
包装层先算 L1 后算 L2 → 第 1 张盘的 L1 用平均年，之后每张盘的 L1 用**上一张盘残留的真年**。
现在 L1 前显式对齐。26 张回归样本里 21 张的末 MD 结束点受影响。

- `deg_str` 加进位收敛：`x.9959°~x.99999°` 原会产出 `12°60'` 这种非法值；
  星座末尾不进位到 30°（sign 由 longitude 决定，不跟着走），收敛到 `29°59'`。

**formatter 校验区 8 条无条件 ✅ 改真判定**——原先那些项写死 ✅，等于没校验，报告却写成"已验"。
新判定全部走**与 engine 不同的推导路径**才算交叉验证：Nakshatra 由经度重算 pada 比对宿主、
Karaka 独立按度数降序重排比对 DK、D9 用 `(9*sign + pada) % 12` 对撞 engine 的元素起点表、
Ra-Ke 在 D9 必须恒差 6 座、Ayanamsa 区间、燃烧入列者必须落在 Sun 最宽 orb 内且 Sun 不得自列、
经度两两不重合、逆行全员 bool 且 Rahu/Ketu 恒 True。
9 个篡改探针反向测试：8 项确认变红；缺星那项走不到校验区（上游表格已 `KeyError` fail-fast），
据实标注为结构冗余检查。

- `vedic-prashna/scripts/prashna_time.py`、`vedic-rectifier/scripts/time_scan.py` 同步同一套 flags。
  后者内联而非 `import engine`，以保住"只依赖 pyswisseph"的独立可跑性——改 engine 常量时必须同步改它。

**⚠️ 输出变化（26 张回归盘，23 张有差异）**：行星 `longitude`/`degree`/`speed` 移动 0~60″，
`deg_str` 偶尔 ±1′，Karaka 元组里的度数值、燃烧 `distance`、`moon_phase.sun_moon_diff` 随之变，
末 MD 的 `end`/`end_time` 变。**`sign` / `house` / `nakshatra` / 全部分盘 / Karaka 归属 /
SAV / BAV / Shadbala 零变化**——精度提升不改变任何离散结论。下游按黄金盘对拍的基线需更新。

### Parivartana 三分类：Dainya 判据由双侧改为单侧（口径 bug 修复）

- `yogas.md` / `vedic-core/SKILL.md` 的 Dainya 原写作「凶宫互溶：6/8/12 **之间**互换」——
  这是**双侧**条件，只覆盖 3 组宫主对；实际按 Mantreswara《Phaladeepika》VI.32–34 应为
  **单侧成立**（6/8/12 任一宫主与任何其它宫主互换、含彼此），30 组。
  被压掉的 27 组此前无处归类：24 组落进无释义的 `Mixed` 档，3 组（3宫↔6/8/12）被误判成 Khala。
- 三类经此修正构成**完备划分**：Maha 28 + Khala 8 + Dainya 30 = 66 = C(12,2)，
  不存在第四档，故 `Mixed` 一并撤销。判定优先级 `Dainya > Khala > Maha`。
- `engine.calc_parivartana` 判据 `x in DUS and y in DUS` → `or`，`Mixed` 分支删除。
  全 66 对实测：Maha 28 / Khala 8 / Dainya 30。
- 标签 `Dainya(凶宫互溶)` → `Dainya(凶宫参与)`——原名逐字表述的正是致错的双侧读法。
  ⚠️ 下游按字符串匹配 `Dainya(凶宫互溶)` 的代码需同步。
- 6/8/12 彼此互换那 3 组同时命中 VRY，禁止同时输出「困境捆绑」与「逆境崛起」两句互斥断语，
  一律走 `p1_p12.md` P5「VRY 孤立性判定」裁决（与 Kalidasa《Uttara Kalamrita》IV.22 同义，
  不另立口径）（`3316824`）。
- 重建 `build/anchored/` 锚产物，`source_commit=33168242178c`（`c77f4bc`）。

### 目录重构：真源 `antigravity/skills/` → `skills/`

- **Antigravity 端点：身份变了，不是没了**。`INSTALL_ROOTS` 一度去掉
  `~/.gemini/config/skills`（`724a1d7`），当日恢复——该端仍在使用。
  旧世界里这个目录**身兼真源与安装点两职**，角色一混，「同步」的方向就取决于谁记得
  当时是哪个身份；现在它与 `~/.claude/skills` 平级，都是从仓里铺下去的副本，**只收不发**。
- **README 补自动安装节（三语）**：`skill_sync.py` 是 09-03 新增的，但**只写进了 CHANGELOG、
  从未写进 README**——克隆本仓的人看不到有这个工具，只能照着手工 `cp`。现补
  `### 一条命令装好（推荐）`：`python skill_sync.py install` 装到 Claude Code 与
  Antigravity 两处，`--dry-run` 预览，只增不删、多余文件报 `[ORPHAN]`。
  Codex 仍走手工复制（`~/.codex/skills/` 不在自动范围，且需配套 `codex-patch/`）。
- **真源目录改名并压平一层**：`antigravity/skills/vedic-*` → `skills/vedic-*`（`a911eb1`）。
  这不只是改名，是修一个概念错误：**真源本来就不是「Antigravity 这个平台的发行面」，
  它是所有发行面的来源**。旧结构把它塞进 `PLATFORMS` 列表里当成员之一，再靠
  `if plat == CANON_PLATFORM: continue`（skill_sync）与 `PLATFORMS[1:]`（consistency_lint）
  把自己跳过去——**位置耦合**：改列表忘了改切片，就会静默漏检一个平台。
  现在 `CANON_DIR` 与 `PLATFORMS` 彻底分开，两处绕行代码随之删除。
- 跟改：`skill_sync.py`、`build_anchored.py`、`scripts/check_skill_parity.py`、
  三份 README、`codex/README.md`、`vedic-calculator/SKILL.md`（去掉指向已停装路径的示例）。
- **锚产物内容零变化**：anchors 305 / sections 121 逐项相同、`file_hashes` 全同，
  只有 `source_commit` 与 `generated_at` 变（`file` 字段本就是裸相对名，不含目录前缀）。
  → **下游无需因本次改名重新 vendor**。
- 历史条目中的 `antigravity/` 路径**不回改**——它们记录的是当时为真的事实。

### `skill_sync.py` 停止排除星历文件（潜伏型缺陷）

- `EXCLUDE_DIRS` / `EXCLUDE_EXTS` 中的 `ephe` 与 `.se1` 已移除。这三个 `.se1` 是
  `setup_env.fix_ephemeris_data` 的**优先级 1 数据源**——PyJHora 4.8.6 的 pip 包不含它们，
  缺了就退到 Moshier 星历（精度下降）。排除星历等于让同步器永远不铺这份必需数据。
- **此前无症状，是因为它是潜伏型**：现有端点的 `scripts/ephe/` 是 `sync_all.ps1` 时代铺下的
  历史遗留，一直在，所以每次 `install` 都"看起来正常"。只有**全新端点首次装到空目录**才会缺，
  届时 `setup_env` 退到网络下载分支，而那个 URL 已 404。换机、新建安装点会踩到。
- `find_orphans` 对目标侧同样调 `iter_files`，被排除项在源与目标两侧都不可见，
  故此前 `--prune` 不会误删已有星历——这也是缺陷一直没暴露的另一半原因。
- 解除排除后各端点 ephe 内容本就一致，`copy_one` 比对即跳过：`all --dry-run` 实测
  **0 个文件待同步**，磁盘零变动，只影响未来新端点。

---

## [Unreleased] - 2026-09-03

### 安装方式变更：新增 `skill_sync.py`，一条命令装到本机

- 新增仓根 `skill_sync.py`（Python，跨平台）。**克隆本仓后直接运行即可把 9 个 skill 装到
  `~/.claude/skills/` 与 `~/.gemini/config/skills/`**，此前 Windows 之外只能手工复制：

  ```bash
  python skill_sync.py all          # 仓内三平台拉平 + 装到本机
  python skill_sync.py all --dry-run # 只看差异，不写文件
  ```

  子命令 `platforms`（仓内 antigravity → claude-code + codex）/ `install`（仓 → 本机）/ `all`。
  脚本**不执行任何 git 操作**；`install` 只覆盖新增、不删除，本机多出的文件以 `[ORPHAN]` 报出，
  确认后加 `--prune` 才清理。
- 同步范围新增 `tests/`。`vedic-prashna/tests/test_prashna_isolation.py`（Prashna 沙箱四条隔离
  回归断言）此前从未随仓分发，现已入仓，克隆后可直接运行。该文件不再硬编码路径，仓布局与安装
  布局下都能跑，并支持 `VEDIC_SKILLS_ROOT` 覆盖。
- `build_anchored.py` 移入仓根并改为从自身位置推导路径，锚产物可独立重建。
- 移除 `sync_all.ps1`（Windows-only，方向为「本地目录 → 仓」，且会自动 commit + push）。
  改由上述 `skill_sync.py` 承担，方向反转为「仓 → 本机」，提交与推送一律手工。

### 锚产物指纹修正：`source_commit` 不再指向产物提交

- `build_anchored.py` 的 `source_commit` 改为「最后一次改动**被锚文件**的提交」，此前取
  `git rev-parse HEAD`。收尾链是「改规则 → 提交规则 → 重跑锚脚本 → 提交锚产物」，**提交锚
  产物本身会推进 HEAD**，此后任何一次重跑都会把 `source_commit` 写成那个产物提交，指向的
  不再是规则内容。下游 vendor `build/anchored/` 时正是读这个字段锁版本，漂了就锁错。
- pathspec 精确到被锚的 6 个文件，不用目录。用 `vedic-core/` 整个子树会把 `scripts/`、
  `__pycache__/` 的活动也算进去——同批 untrack `.pyc` 就实测顶偏过一次。
- 本次修正**不改变当前指纹**（开源 `6d9054d29335`，305 锚 / 121 节），仅消除后续漂移。

### Parivartana 扫描口径修正

- `vedic-core/resources/` Parivartana 扫描改读 calculator 的互溶对照表，分类与 `yogas.md`
  对齐，不再由模型自行推导宫主互换（`6d9054d`）。
- 重建 `build/anchored/` 锚产物，`source_commit=6d9054d29335`（`4884937`）。

---

## [Unreleased] - 2026-08-28

### 三级运（Pratyantardasha）纪律补齐

- `vedic-core/resources/house_framework.md`「时间窗纪律」canonical 回补 A2 时间窗人话锚（`e5083fe`）。
- `vedic-career` / `vedic-love` / `vedic-synastry` 三份压缩副本补齐 PD 层，与 canonical 对齐（`c1199f6`）。此前三者停在"MD×AD 叠加窗 ≤3 年"、对三级运零提及，与 07-31 已升到三层（MD×AD×PD）的 canonical 脱节近一个月——根因是一致性检查的必备标记清单停在旧口径，同批已补 `原生PD` 标记。
- 重建 `build/anchored/` 锚产物，`source_commit=e5083fe`（`a1173db`）。

### 小火人文本卡片导出

- 新增 `make_xiaohuo_person_card.py`，从 `structured_data.md` 生成文本人物卡片（`4f5d4ab`）。
- 卡片补出当前 Pratyantardasha 行；Lagna 改为固定 `Lagna: 星座; H宫; 度数（上升）` 单行格式，避免下游对话模型漏读（`cadb170`）。

### Comprehensive multilingual repository documentation

- Rebuilt the default `README.md` as a Chinese-first homepage with a compact trilingual introduction and clearly separated full-language entry points.
- Restored comprehensive module, workflow, technical architecture, validation, installation, Codex Patch, repository, version, and licensing documentation without returning to line-by-line bilingual mixing.
- Expanded `README.en.md` and `README.ja.md` to the same information architecture so that both links now lead to full documentation rather than shortened summaries.
- Restored the original homepage's stronger visual rhythm with a compact trilingual hero, one-line language navigation, a collapsed table of contents, restrained section icons, and scannable per-skill disclosure blocks.
- Made direct chart calculation from birth date, exact time, and place the primary onboarding path while keeping PDF, screenshot, and text import as optional validation routes.
- Reconciled technical claims with the current skills and changelog: documented complete MD/AD/PD output, divisional stability auditing, the 16-rule Reader validation set, and traceable v6.1 regression results; removed the old unauditable generic `>97%` accuracy claim.

### Japanese runtime and documentation support

- Added Japanese trigger metadata to all eight skills while preserving English and Chinese discovery phrases.
- Added one per-skill Japanese localization resource for stable Jyotish terminology, natural polite register, intake wording, questionnaire phrasing, report labels, and client-facing answer order.
- Added a native Japanese HTML shell with `--lang ja`, `lang="ja"`, Japanese cover and section labels, and Noto/Hiragino/Yu Japanese font fallbacks.
- Added `README.ja.md` and `codex-patch/README.ja.md`; the canonical calculation, evidence, phase, scoring, schema, and report-lineage rules remain single-source and untranslated.

### English runtime and documentation support

- Added English-first trigger metadata while retaining Chinese trigger phrases for all eight skills.
- Added a shared client-language contract for chat, intake, questionnaires, progress notices,
  warnings, reports, Q&A, and language-matched HTML report shells.
- Kept canonical filenames, `structured_data.md` schemas, CLI flags, technical identifiers,
  evidence, calculations, and report lineage unchanged across languages.
- Added `README.en.md` and `codex-patch/README.en.md`, with direct chart calculation from
  birth date, exact time, and place presented as the primary onboarding path.

### 新增 codex-patch（Codex 执行规则补丁包）

- 新增仓库根目录 `codex-patch/`，独立于 `codex/skills/`，不改动任何 skill 文件。
- 明确包级版本为 Codex Patch v1.0.0，与 Skill Suite、盲问协议和分析师协议的版本独立。
- 包含 Codex 版执行规则：精简 Vedic 全局路由器（`AGENTS.md`）、UC 证据防火墙
  （`vedic_uc_firewall.md`）、表达/产物/QA 路由（`vedic_client_voice.md`、
  `vedic_core_life_rendering.md`、`vedic_output_router.md`、`vedic_qa_rendering.md`）、
  盲问与分析师剪辑（`vedic_blind_qa_prompt.md`、`vedic_consultative_integration_prompt.md`），
  以及 rectifier 校准四模块（execution_overlay / settlement / question_design /
  interval_guard）。
- README Codex 安装段新增完整推荐配置指引；Skill本体仍可独立加载，但缺少
  补丁时不具备本仓库承诺的 Codex 执行保障。安装与使用说明见 `codex-patch/README.md`。

### vedic-prashna 安全重构

- 标准层改为以 *Shatpanchasika* 为主文本、经 KN Rao／Bharatiya Vidya Bhavan
  兼容性筛选的规则账本；不再把 KN Rao 的本命工具自动迁入提问盘。
- 删除“Moon 无接触＝空亡／不成”的全局硬门；Moon 只按题目专属规则消费，其余
  只列当前事实。
- 新增秒和小数秒保留、时区 DST 严格校验，以及 Lagna／rising Navamsa 输入敏感性
  分离报告。
- 标准、Tajika、KP 在构建器、产物和结论权限上完全隔离；既有盘 Q&A 可分栈追问，
  跨栈比较只并列、不投票。
- Tajika 副层实现十六 Yoga、Kamboola 16 档、Shunyamarga、Radda／Durapha
  优先级与受限 timing 候选；出版例盘套件完成前继续标为实验候选。
- 修正 Tajika 接触容许度：按较快星自身的 deeptamsha 判断，不再取两星平均值；
  加入原典 14° 差值对应 `14 × 12 = 168` 天的出版正例边界测试。
- KP 独立栈实现用户给号 1–249、Krishnamurti ayanamsa、Placidus cusps、
  A/B/C/D significator chain、Ruling Planets、四级 period 与 timing 失败关闭。
  未核证的 node 接触代理、婚姻重聚语义和出版 timing 套件不作推断，整栈继续标为
  实验候选。
- 修正 KP 恋情落实判据：正向必须同时关联 7、11，反向关联 6 或 12 任一即可；
  不再把部分正向命中误判为正向或制造假 `mixed`。
- 修复 1–249 表在嵌套 Vimshottari 子区间末端的浮点缝隙，并把号码定义的第 1
  cusp 与精确对冲的第 7 cusp 回写为定义值；249 个号码现可逐一完整起盘。
- KP 判读单改为直接回答“当前偏向／关键理由／现实含义／能否给时间”；真正
  `mixed` 明确说明缺少来源支持的优先裁决规则，不再写成“有机会也有阻力”。
- 新增 KP 可观察结果范围门：`love-materialization` 只允许“建立明确、双方确认并
  持续推进的恋爱关系”；仅恢复联系、互动回暖、恢复暧昧或秘密心意在计算前失败
  关闭，不再被错误提升为高门槛题型。
- 标准、Tajika、KP 判读单均改为先说人话、后列可回查技术证据。

### 三端同步与遗留清理

- 删除三份 4 月停更的 `.claude/commands/vedic-{core,career,love}.md` 全量副本；
  Claude Code 以 `claude-code/skills/*/SKILL.md` 为唯一工作流来源。
- 删除仓库根目录停更的 `scripts/report_builder.py`；三端继续使用各自
  `vedic-core/scripts/report_builder.py` 的一致正式版本。
- 新增 `scripts/check_skill_parity.py`，逐文件校验八个 Skill 在 Antigravity、
  Claude Code、Codex 三端的一致性，并验证 Codex 专属 `agents/openai.yaml`。
- 修正 README 中不存在的 synastry `USAGE.md`、旧“三阶段执行引擎”描述与
  rectifier 最低证据数量表述。

---

## [v8.0] - 2026-07-12

> 🔮 **vedic-prashna 卜卦/时盘上线** — 八Skill架构（独立生态位）
>
> 此节记录 v8.0 初版行为；当前安全口径以上方 Unreleased 重构为准。

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
