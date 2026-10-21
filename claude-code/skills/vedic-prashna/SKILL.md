---
name: vedic-prashna
description: "Cast and interpret a question-time Vedic Prashna chart for one concrete question using the exact asking time and place. The Shatpanchasika-rooted classical standard layer runs first; Tajika contact and KP 1-249 remain isolated optional stacks. Use for 'Prashna', 'horary chart', 'cast a chart for this question', 'will this specific matter work out'; Chinese triggers such as '即时盘', '时盘', '卜卦', and '起一卦'; Japanese triggers such as 'プラシュナで見て', '質問時刻図を立てて', and 'ホラリーで判断して'; or follow-ups about an existing Prashna result. Not for natal life-trend analysis. / 吠陀提问盘与时盘分析引擎。"
---

# Vedic Prashna

## Language contract / 语言契约

- Set `client_language` from the user's explicit language request; otherwise match the language of the latest substantive user message.
- Use `client_language` for all chat replies, intake questions, confirmations, progress updates, user-visible warnings, judgments, reports, and Q&A. Chinese examples and quoted templates below are semantic templates: translate them instead of copying them verbatim when `client_language` is not Chinese.
- Keep canonical filenames, CLI flags, JSON keys, `structured_prashna.md` and optional-stack schema headings, technical codes, and Sanskrit/English identifiers unchanged. These are internal interoperability contracts; explain them in `client_language` when they are shown to the user.
- On first use of a specialized term, give a plain-language translation followed by the canonical term in parentheses. Never translate canonical identifiers inside calculations or evidence citations.
- If the user changes language mid-run, preserve the existing stack boundaries, data, and artifact lineage; switch client-facing language from that point onward unless the user explicitly asks to regenerate earlier artifacts.
- When `client_language` is Japanese, read `resources/ja-prashna.md` completely before the first Japanese client-facing message. Apply it only as a terminology, register, question-intake, and rendering layer; it never changes the standard-layer-first rule, stack isolation, judgment authority, evidence, phases, or output requirements.

## 定位

用一个具体问题产生时的时间和地点建立独立提问盘。默认层是：

> *Shatpanchasika*-rooted classical Prashna，经 KN Rao／Bharatiya Vidya Bhavan
> 实践兼容性筛选。

不要把它写成“KN Rao 自创的完整 Prashna 体系”。KN Rao 的公开材料支持谨慎使用
Prashna、有限 snapshot 实例及其对 *Shatpanchasika* 的认可，但不支持把他的本命
Jaimini、Dasha、分盘或 SAV 工具自动迁入提问盘。

默认层回答：

- 事情怎么走：现在的局面、推动的力量、阻力、转机的信号、现在能做什么；
- 倾向必须讲明白：账本按占优断定出内部三档（偏成／持平／偏不成），只写在判读单核对区，
  给用户看的部分不出现档名；
- 偏成或持平时，一个有原典出处的大致时间（时间副层）。

时间副层不改三档；偏不成档不给时间，也不承诺精确到某天某时。

设计原则：让古老的提问盘适合现代人用，而不是逐字照搬古籍。规则必须有本土典籍出处
（*Shatpanchasika* 为主，*Prasna Marga* 有条件收入，见 `standard-layer.md` §1）；数法、
问法分流、输出形态属于执行口径，在资源文件里明写。

描述题（失物在哪、什么方向多远、是谁拿的）、雨季天气、胎儿性别、父亲是否在外地
只给原文查表结果，原文歧义两说并列，不出三档、不给时间。

---

## 每次执行必须读取

按顺序完整读取：

1. `resources/standard-layer.md`：来源标签、准入、白名单；
2. `resources/question-taxonomy.md`：单问与 A／B／C 支持级；
3. `resources/house-karaka-map.md`：一个主事项宫和专题入口；
4. `resources/judgment-rubric.md`：适用规则账本与按占优合判；
5. `resources/moon-policy.md`：Moon 当前事实的使用边界；
6. `resources/timing-layer.md`：时间副层（只在偏成／持平档运行）；
7. `resources/judgment-writing.md`：判读单写作指引（口吻、篇幅、含义来源、高频题型写作要点；不计分、不改档）。

只在用户显式启用时读取：

- Tajika：`resources/tajika-optional.md`
- KP：`resources/kp-optional.md`
- 本命矛盾裁决：`resources/cross-natal-policy.md`
- 既有盘追问：`resources/qa_rules.md`

---

## 隔离硬约束

1. 只读调用共享 `vedic-calculator/scripts/engine.py`；不向共享 engine 增加
   Prashna、Tajika、KP 或 Void 字段。
2. 默认输出必须由 `scripts/format_prashna_standard.py` 生成；禁止调用共享本命
   `formatter.py` 后再删段。
3. 不修改 core/love/career/synastry/rectifier 等其他 skill。
4. 标准产物只写入 `prashna_<yyyymmdd_HHMMSS>_<label>/`，文件名
   `structured_prashna.md` 和 `prashna_judgment_<label>.md`。时间副层只在该目录
   增加 `timing_overlay.md`；显式 Tajika overlay 只在该目录增加
   `tajika_overlay.md`。KP 只写入独立 `kp_horary_<yyyymmdd_HHMMSS>_<label>/`，文件名 `structured_kp.md`、
   `structured_kp.json` 和 `kp_judgment_<label>.md`。
5. 不读取或写入 `user_context.md`。
6. Tajika／KP 计算只存在本 skill；标准 builder 不导入两者，也不接受 optional
   flag。时间副层由独立 `scripts/build_timing_overlay.py` 生成：标准 builder 不导入
   它，它也不导入 Tajika／KP。
7. 不读取其他 `prashna_*` 目录；追问只沿用当前盘。

---

## 默认层禁入项

不得消费或输出：

- Chara Karaka、DK、UL、AL；
- SAV／BAV、Shadbala、Bhava Bala；
- 完整 D9、D10、D4、D5 等本命分盘；
- engine 的 functional P1 身份、natal yoga prescan（宫表的吉凶标签是 `P-I.3` 注的
  Ayer 功能吉凶，从被占据／照射的星座起算，不是 P1）；
- 120年 Vimshottari、Chara Dasha；
- transit、Sade Sati、double transit；
- Tajika orb／applying／separating；
- KP cusp／sub-lord。

只允许 rising Navamsa（星座与序号）、Lagna 所在 drekkana、Lagna 六分盘座主表三项有限数据，
因为 `P-I.4`（注：Lagna、Hora、Drekkana、Navamsa、Dwadasamsa、Trimsamsa 六分盘）、
`P-I.7`、`P-VI.1~2`、`P-VI.4`、`P-VII.13` 明确使用它们；禁止由此展开完整 D2、D3、D9、
D12、D30 解读。

---

## Phase 0：输入与问题门控

必收：

| 输入 | 规则 |
|---|---|
| 具体问题 | 一个可观察结果；不能同时问两个独立事项 |
| 提问时刻 | 显式时刻，或用户说“现在”；保留秒和可用的小数秒 |
| 提问地点 | 城市或经纬；必须能确定 IANA 时区 |

执行：

1. 用 `question-taxonomy.md` 澄清单问；
2. 判 A／B／C 支持级；
3. C级停止，不硬套宫位；
4. “现在”必须在提问地时区捕获，禁止在处理数分钟后另取整分钟；
5. 地点／时区未知时澄清，不用机器时区代替；
6. A/B 二选一不得机械起两张同刻盘；
7. 同一问题和现实状态未变化时沿用第一次清晰提问盘，不使用24小时／3个月阈值；
8. 复合／联系类按 `question-taxonomy.md` §2.7 归到一行，求职／考试类按 §2.8，
   房屋、出行、返回、疾病、名誉、谈判、投资、亏损、开庭、失物找回等按 §2.12；
   操控／打听类不判，一句话说明并给替代问法；
   描述题、天气按 §2.10／§2.11 查表；生死、寿命、读心、他人隐私按 §2.13 不判；
9. 出现自伤或极端语句时先回应安全，不起盘（§2.9）。

进入下一阶段条件：问题唯一、支持级为A或B（或为查表题）、时间地点完整。

---

## Phase 1：起盘与输入敏感性

运行：

```bash
python scripts/build_prashna_data.py \
  --datetime "<YYYY-MM-DD HH:MM[:SS[.ffffff]]|now>" \
  --lat <lat> --lon <lon> --tz "<IANA>" \
  --question "<single observable question>" \
  --label "<kebab-case>" --out-parent "<parent>"
```

`build_prashna_data.py` 只读共享 engine，并用 Prashna 专用 formatter 输出白名单。

检查 `structured_prashna.md`：

- Lagna 距 sign 边界；
- Lagna 距 Navamsa 边界；
- 六分盘多数临界距离（本题账本用 `P-I.4` 时）；
- 时间／地点是否只是近似。

若输入误差可能改变 Lagna、六分盘多数或 rising Navamsa，标记 `输入敏感` 并取得更准确输入；
不能声称城市中心近似必然不影响结论。输入敏感性只影响实际消费该字段的规则；
若本题账本不使用该字段（六分盘多数只供 `P-I.4`，rising Navamsa 只供描述题与时间副层），须分别写
“该字段敏感”和“主结论所用 D1 结构是否稳定”，不得把两者合成一个模糊置信度。

进入下一阶段条件：产物存在、默认白名单无越权字段、敏感性已处理或明确降置信度。

---

## Phase 2：主事项宫与适用规则

1. 从 `house-karaka-map.md` 选择一个主事项宫；
2. A级定位题目专属 `P` rule_id；
3. B级只使用通用宫／宫主规则和明确匹配的 Bhavan 辅证；
4. 始终保留 Lagna 与 Lagna 主；
5. Moon 只在专题规则明确需要时成为主输入；
6. 不固定加入自然 Karaka、Moon 月宿主或 Chara Karaka；
7. 复合、求职、考试、走失宠物及 §2.12 各专项按 `question-taxonomy.md` §2.7／
   §2.8／§2.12 和 `house-karaka-map.md` 取 rule_id 与事项宫；
8. 吉星／凶星一律读 `structured_prashna.md` 宫表的 Ayer 功能吉凶标签
   （`standard-layer.md` §2.1）；正文点名行星的规则按点名读，不换标签；
9. 查表题（描述题、天气、胎儿性别、父亲下落）不建账本，跳到 Phase 6 按
   `judgment-rubric.md` §10 输出。

建立规则账本，在判读单核对区完整显示（聊天里在用户要看依据时展开）：

| rule_id | 支持级 | 适用理由 | 原始证据 | 方向 | 计分 | 冲突 |
|---|---|---|---|---|---|---|

规则账本只消费 `structured_prashna.md` 白名单。没有 rule_id 的解释不能进入结论。

进入下一阶段条件：至少一条适用主规则，所有规则有范围和原始字段，没有 `U/T/KP`
混入默认账本，`M` 只收 `standard-layer.md` §1 准入的条目。

---

## Phase 3：Moon 当前事实

读取 `moon-policy.md`：

- 专题规则使用 Moon：按该规则消费位置、月相或接触；
- 仅有 Bhavan 题意验证：月宿只作软验证；
- 其他题型：Moon 只列背景。

禁止：

- Moon 无接触＝空亡／不成；
- Moon 最高权重；
- 月宿主固定成为 significator；
- Chandra Kriya、Tajika Khallāsara 或西方 Void 混入；
- Moon ingress 承担 Dasha 或进入规则账本（Moon 入座触发日只在时间副层）。

进入下一阶段条件：Moon 每条判断都说明适用 rule_id，或明确标为背景。

---

## Phase 4：合判与内部档

严格按 `judgment-rubric.md` §3 按占优断（依据 Ayer I.4／III.4／IV.5 注、`M-XIV.98`、
`M-XVII` 注）：

- 账本每条规则一份证据：有利 +1、不利 −1、混合 0，等权；同源证据只计一次，出行题不收
  10 宫 `P-I.3`；原文写明偈内由占优定局的（`P-I.4`、`P-III.4`、`P-IV.5`）先按 §4.1 定方向，
  吉占优记有利，正文按“困难后成”讲过程不顺、阻力在哪；
- 合计 >0 记**偏成**（顺／有阻力），<0 记**偏不成**（明确／有转机），=0 记**持平**；
- 持平须写明类型：吉凶相当，或输入敏感（不论合计）；
- 阻力、转机都要指到账本里具体的反向条目。

单一行星、单一宫位、单一缺失或单一强弱因素不是规则，不计分，不能单独决定倾向。
三档只写判读单核对区。查表题不出三档。

输入敏感只有在可能改变本题账本实际使用的 Lagna、六分盘多数、事项宫或宫主
结构时才能影响档次。未被本题规则消费的临界字段只报告，不改票。

成败档次与时间副层分开：时间远近不改档，给不出精确日期也不因此改记持平。

进入下一阶段条件：内部档可从核对区账本的计分与合计逐条复核。

---

## Phase 5：时间副层

读取 `timing-layer.md`。内部档为偏成或持平时运行：

```bash
python scripts/build_timing_overlay.py \
  --datetime "<与 Phase 1 完全相同>" \
  --lat <lat> --lon <lon> --tz "<IANA>" \
  --matter-house <1-12> --mode general|return \
  --verdict favorable|pending \
  --out-dir "<当前 prashna_* 目录>"
```

- 事项宫和 `--mode` 按 `timing-layer.md` §4 取；人的归来／到达题用 `return`；
  查表题不运行。
- 偏成写“约……”，持平写成条件式（如“如果推进顺利，大约……”）；偏不成不运行，判读单写明
  不给时间、什么变化之后可以再问。
- 几个候选结果不同时并列，不平均、不折中；判读单正文转述成一句话，明细放核对区。
- 婚恋题另看 `M-XVII.31`，满足时只加一句“偏早”提示（`timing-layer.md` §3）。
- 不使用提问盘生成的 120 年 Vimshottari、Chara Dasha 或过运；*Prasna Marga* 的
  一年／一月 Prasna Dasa 不收。

进入下一阶段条件：偏成／持平档已有 `timing_overlay.md`，或偏不成档已写明不给时间。

---

## Phase 6：输出

写入 `prashna_judgment_<label>.md`。聊天里显示给用户看的全部内容（标题到“现在能做什么”）；
用户要看依据时再展开核对区。

### 6.1 给用户看的部分：标题、简述、盘面解读

先读 `resources/judgment-writing.md`。写作指引只管怎么讲，不计分、不改档：倾向已在 Phase 4 由账本定好。

- **标题**：贴着这道题的情境写一句人话，让人一眼看出倾向；
- **简述**：一小段（3–5 句），讲倾向、关键在哪、大概什么时候；情感题的一次安抚放这里；
- **盘面怎么说**：照着盘讲故事。小标题用盘面特征命名；提问人这一侧、事情或对方那一侧、
  两边之间、心境、几条古法加起来，五件事都讲到；每个事实走“盘上是什么 → 古书怎么看 →
  现实里可能是什么样子”；
- **什么时候**（偏不成：什么变化之后可以再问）；
- **现在能做什么**。

内容契约（只定讲清什么，不定句式；版式和语气细节由使用方调整）：

1. 不用判词给结论：不写“成／悬／不成”和内部档名，也不写“能成”“成不了”“很难成”“一定”
   “注定”“没希望”这类断语。倾向在故事里讲明白，不准模棱两可。
2. 盲读检查：只看标题和简述，读者能分辨偏成、持平、偏不成；读完全文，对倾向的感受也必须
   与内部档一致。分辨不出或感受相反就重写。
3. 定档的理由就是故事的骨架：账本每条计分规则都要讲到，按推、拖、没有方向分组，故事的走向就是
   合计的方向；带判断的话都能在核对区账本里找到对应条目。写的时候发现账本读错，回 Phase 4 改账本、
   重新定档，再按新结论写，不在故事里改口。背景事实（不计分）只挂在某条账本条目旁边作补充，用背景的
   口气，不单独成段推出结论，在核对区列出；背景事实与内部档方向相反时，只能放在“不过”“转机”的位置并说明它不改变
   整体判断，不许加码。
4. 含义只取 `judgment-writing.md` §2 的六类来源；没有出处的含义不写。
5. 术语可以出现，第一次出现紧跟白话；不出现 `rule_id`、`mixed`、`promise`、`cusp`、
   `sub-lord`、`Itthasala` 或生产状态码；不能用“混合配置”“支持级 B”或“实验候选”代替事件说明。
6. 不给固定句式模板，用自己的话写；篇幅按 `judgment-writing.md` §1。
7. 偏成·有阻力、偏不成·有转机：说清阻力或转机具体在哪（对应账本里的反向条目）。
8. 持平：说清两边各是什么、该看哪个信号；输入敏感时用人话说明时间、地点再准一点会更清楚。
9. 偏不成：不下死结论；讲清卡点、现在能做什么、什么变化之后可以再问。
10. 不归咎提问人：卡点讲成条件（如“你这边的准备和时机”），不评判人，不从盘里读性格。
    考试题即使偏成，也提醒照常准备。
11. 时间：把主时间和最近的触发日合成一句，如“最可能在 X 前后，最近的一个节点是 Y 日”；
    偏不成不给时间。
12. 不使用极端或宿命化措辞。

### 6.2 判读单结构

```markdown
# Prashna 判读单：<问题>

## <标题>

<简述>

---

### 盘面怎么说

#### <以盘面特征命名的小标题>
<2–4 段，紧扣盘面事实>

<……提问人这一侧、事情或对方那一侧、两边之间、心境都讲到>

#### 几条古法加起来
<账本每条讲成一句人话；推几份、拖几份、几份没有方向>

### 什么时候
<偏成／持平：主时间与最近触发日合成一句；偏不成：不给时间，写什么变化之后可以再问>

### 现在能做什么
<可执行建议>

---

## 核对区

### 一、这张盘的范围
**提问时刻／地点**：
**来源支持级**：[A/B；说明这是来源覆盖，不是概率]
**输入稳定性**：[本题实际消费字段稳定/敏感及原因]
**体系状态**：[标准层/实验候选]

### 二、内部档
**档位**：[偏成·顺／偏成·有阻力／持平·吉凶相当／持平·输入敏感／偏不成·有转机／偏不成·明确]（合计 +N／−N／0）

### 三、适用规则账本
| rule_id | 支持级 | 适用理由 | 原始证据 | 方向 | 计分 | 冲突 |
合计：
**背景事实（不计分，只用于叙述）**：<正文用到的上升主星落宫、同宫星、宫义星义等>


### 四、时间
<偏成／持平：摘 `timing_overlay.md` 的主时间、最近的触发日和参考，及 `M-XVII.31` 提示；偏不成：不给时间及原因>

### 五、Moon 当前事实
<专题输入或背景；说明 rule_id>

### 六、体系边界
默认层不含 natal Dasha/Chara Karaka/SAV/完整分盘/Transit/Tajika/KP。
```

查表题的判读单：标题、简述、正文用白话写查表结果，两说都写；核对区只留“这张盘的
范围”和一张查表（`judgment-rubric.md` §10）；不写三档和时间。天气条件不满足时写
“原文无反面判据”，不写“不会下雨”。

### 6.3 安抚

情感类问题（复合、联系、分手后等）的安抚写在正文里，守六条：

1. 只安抚一次，要具体，引用用户原话；不用“一切都是最好的安排”“时间会治愈一切”
   “放下才能拥有”“你值得更好的”这类套话。
2. 追问时不重复安抚，除非用户表达了新的情绪。
3. 安抚不改结论。
4. 安慰要有盘面依据：持平只取卡点和最近的触发日；偏不成说明这张盘答不了什么，
   以及什么现实变化之后可以再问。
5. 操控／打听类问题：一句话说明为什么不判，再给替代问法，不说教。
6. 出现自伤或极端语句：先回应安全，不起盘。

---

## Tajika 可选副层

默认关闭。只有用户显式要求 Tajika／Itthasala／applying-separating 时才读取
`tajika-optional.md`。

先完成标准层 Phase 2，取得 Lagna lord 和唯一事项宫主，再运行独立
`scripts/build_tajika_overlay.py`。不得在标准 builder 上增加
`--enable-tajika`。查表题、不判题，以及问者星与事项星为同一颗（事项宫为 1 宫
或与 Lagna 同一座主）时不运行，按 `tajika-optional.md` 用一句白话说明，不拿
Karaka 或其他宫主顶替。

当前实现按 *Tajika Nilakanthi* 2.3–59 输出十六 Yoga 分类，并保留
Uttama／Madhyama／Sama／Adhama 的 Kamboola 16 档、严格 Shunyamarga、
Radda／Durapha 优先级及换座候选。它仍是实验候选，不能进入默认主结论。
只有主星直接 Itthasala 才可显示原典“度差 × 12 日”比例候选；这不是天文保证，
也不得进入标准层。它和标准层时间副层来自不同体系，不互相校正，主答案以判读单
§四 为准。全部出版例盘与边界测试完成前不得解除实验标签。
`tajika_overlay.md` 同时承担人类可读副层判读：必须先说直接接触、过程修正、
现实含义和 timing 状态，再显示十六 Yoga 明细；Yoga 名称第一次出现时必须紧跟
白话含义，不能把十六项布尔表当作判读；“先说人话”一节不得出现 deeptamsha、
Yoga 名称或原始状态码；仍不得生成标准层三档结论。

---

## KP 独立栈

默认关闭。只有用户明确要求 KP／sub-lord 时才读取 `kp-optional.md`。经典 KP
Horary 必须由用户给出 `1–249` 数字；不得从时刻、文字或随机数代取。
关系题必须先确认可观察结果范围：现有 `love-materialization` 只回答是否建立
明确、双方确认并持续推进的恋爱关系。仅恢复联系、互动回暖、恢复暧昧或秘密心意
不在该公式范围内，必须在起盘前失败关闭；不得擅自把低门槛问题改写成“关系落实”。
题型不收或范围失败关闭时，按 `kp-optional.md`“不收时的出口”回答：说明原因，
给出改用标准层或换成已收问法两个选项，不替用户切换。

KP 与 Tajika 在计算、文件和结论权限上互斥；用户可以显式要求分别查看两套结果，
但不得在任一栈内读取另一栈或拼票。只有 Q&A 的跨栈比较模式可以并列解释已经生成
的结果。KP 是独立判读栈，不运行标准 builder，也不与默认层拼票。
使用 `scripts/build_kp_horary.py` 生成独立 `kp_horary_*` 目录。当前已实现
Krishnamurti ayanamsa、number-derived Placidus cusps、A/B/C/D significator
chain、node constellation／sign-lord agent、Reader VI 已锁定的恋情落实／商业
合作题型宫组、Ruling Planets、边界距离，以及独立的 horary Moon 四级 period、
RP 交集与 Moon／Sun／Jupiter 过运 timing。婚姻重聚因原文存在多个不同语境而失败
关闭。Readers 未给 Rahu／Ketu 自身 orb，因此 node conjunction/aspect agency
继续失败关闭；任何 operative promise 路径穿过该缺口时，promise 与 timing 都不得
宣称完整。整栈在全部出版例盘套件完成前不能标“生产级”。
每次运行必须同时生成 `structured_kp.md/json` 与人类可读
`kp_judgment_<label>.md`；判读单只翻译 KP 自身 promise、门控与 timing，不换算成
标准层内部三档（偏成／持平／偏不成）。判读单必须先回答“当前偏向什么、为什么、能否给时间”，
并把命中的宫组翻译成该题型的现实支持或阻力；再把 cusp／sub-lord／RP／period
状态码放入技术核对区。

---

## 本命交叉与追问

本命交叉默认关闭。用户明确要求时读取 `cross-natal-policy.md`；当前版本因旧裁决
规则未完成来源重审而失败关闭，不能调用不存在的 build 参数，也不能用 SAV、
本命 Dasha 或分盘升降 Prashna 结论。

已有盘追问不重起，读取 `qa_rules.md`，且只访问当前 `prashna_*` 目录。
若追问对象是 KP，则只访问当前 `kp_horary_*` 目录，不读取或拼接
`prashna_*`。

### Phase 7：Q&A 追问

1. 先判定是同一可观察结果的澄清／细化／拓展，还是新问题；
2. 标准追问只读当前 `prashna_*` 的标准产物；
3. Tajika 追问可在同目录额外读取 `tajika_overlay.md`，但不改标准结论；
4. KP 追问只读当前 `kp_horary_*`；
5. 用户明确问“整体／三层怎么看／为什么不同”时，进入跨栈比较：只读用户或当前
   对话明确关联的目录，分栏显示标准、Tajika、KP 的结论、一致点和冲突点，不投票；
6. 同一问题和现实状态未变时沿用原盘；新对象、新目标、新行动或新事实改变结果语义
   时才回 Phase 0；只换问法不算新问题；
7. 追问时不重复安抚，除非用户表达了新的情绪；
8. 回答口吻与含义来源同 Phase 6（`judgment-writing.md`）；追问不改档，发现账本读错按纠错回 Phase 4
   （`qa_rules.md` §4）。

进入完成条件：每条回答能回查对应栈文件，未跨目录偷读，未给偏不成档补时间，
也未把跨栈比较写成一个新的混合占星结论。

---

## 最终自检

- [ ] 已完整读取七个默认资源？
- [ ] 支持级为A或B，且只选一个主事项宫？
- [ ] 默认产物由专用 formatter 生成？
- [ ] 规则账本在核对区完整可见，每条有计分与合计，没有 `U/T/KP` 越界，`M` 只收已准入条目？
- [ ] 未使用 Chara Karaka、SAV、完整分盘、本命 Dasha 或过运？
- [ ] Moon 无接触未被写成空亡或全局负分？
- [ ] 吉星／凶星是否读宫表 Ayer 标签，点名行星的规则是否按点名？
- [ ] 查表题是否只给查表结果、两说并列，没有出三档和时间？
- [ ] 成败与时间副层分开，偏不成档没有给时间？
- [ ] 给用户看的部分没有判词和档名，标题简述与全文盲读都与内部档同向，每句判断对得上账本，
      背景事实没有反向加码？
- [ ] 盘面解读是否照着盘讲，五件事都讲到，含义都出自 `judgment-writing.md` §2？
- [ ] 情感类安抚只出现一次、有盘面依据、没有改结论？
- [ ] 输入敏感性已处理？
- [ ] 提问时刻是否保留秒级，且没有用处理时刻替代用户提问时刻？
- [ ] 标准／Tajika 产物是否只写入当前 `prashna_*`，KP 是否只写入独立
      `kp_horary_*`？
- [ ] 标准 builder 是否完全未导入 Tajika／KP？
- [ ] 若启用 KP，是否由用户给了 1–249 数字并使用独立 `kp_horary_*` 目录？
- [ ] KP 题型是否与用户确认的可观察结果一致，且未把回暖／联系改写成关系落实？
- [ ] Tajika／KP 是否都有可读判读，且未进入标准账本？
- [ ] 追问是否沿用当前盘；跨栈比较是否只并列、不拼票？
