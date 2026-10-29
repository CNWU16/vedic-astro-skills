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

用一个具体问题产生时的时间和地点建立独立提问盘。默认层是 *Shatpanchasika*-rooted classical Prashna，经 KN Rao／Bharatiya Vidya Bhavan
实践兼容性筛选，有条件收入同一系的 *Prasna Marga*。不要把它写成"KN Rao 自创的完整 Prashna 体系"，也不把他的本命 Jaimini、Dasha、分盘或
SAV 工具迁入提问盘。

**分工**：模型取象，脚本计数。模型拆题、抓关键词、定事项宫与行动者，写成取象单；判定脚本按古法规则计成事账、能力否决、行动链与限定语，
定出内部三档（偏成／持平／偏不成，只写核对区）；模型照着判定结果和盘面写判读单，讲事情怎么走。偏成或持平时附一个有原典出处的大致时间
（时间副层）；时间副层不改三档，偏不成不给时间，不承诺精确到某天某时。

设计原则：让古老的提问盘适合现代人用，而不是逐字照搬古籍。规则必须有本土典籍出处（`standard-layer.md` §1）；拆题是主流程，古法给出处，
不单独否决；数法、问法分流、输出形态属执行口径，在资源文件里明写。

---

## 读什么

每次执行按顺序完整读取：

1. `resources/question-decomposition.md`：拆题、三型、子问题出口、转宫、抓关键词、取象单格式、澄清与门控；
2. `resources/house-meanings.md`：宫义、星义、星座性质、行动者与关键词库、按问题读、连接口径、限定语检验；
3. `resources/matter-rules.md`：事项登记（事项宫与本事古法）、查表题、不判；
4. `resources/judgment-rubric.md`：判定脚本怎么定档，怎样读判定结果；
5. `resources/judgment-writing.md`：判读单怎么写；
6. `resources/moon-policy.md`：Moon 的使用边界。

按情况再读：时间副层运行时读 `timing-layer.md`；只给城市名、需要查经纬度或时区时读 `locations.md`；追问读 `qa_rules.md`；问出处、维护规则时读
`standard-layer.md`；用户显式启用时读 `tajika-optional.md`、`kp-optional.md`、`cross-natal-policy.md`。

---

## 隔离硬约束

1. 只读调用共享 `vedic-calculator/scripts/engine.py`；不向共享 engine 增加 Prashna、Tajika、KP 或 Void 字段。
2. 默认输出必须由 `scripts/format_prashna_standard.py` 生成；禁止调用共享本命 `formatter.py` 后再删段。
3. 不修改 core/love/career/synastry/rectifier 等其他 skill。
4. 标准产物只写入 `prashna_<yyyymmdd_HHMMSS>_<label>/`（同名目录已有盘时 builder 另开 `_2`、`_3`……，不覆盖旧盘；后续产物写进 builder
   实际打印的那个目录）：`structured_prashna.md`、`prashna_plan.json`、`prashna_verdict.json`、`prashna_verdict.md`、`prashna_judgment_<label>.md`；
   时间副层只增加 `timing_overlay.md`；显式 Tajika overlay 只增加 `tajika_overlay.md`。KP 只写入独立 `kp_horary_<yyyymmdd_HHMMSS>_<label>/`，
   文件名 `structured_kp.md`、`structured_kp.json` 和 `kp_judgment_<label>.md`。
5. 不读取或写入 `user_context.md`。
6. Tajika／KP 计算只存在本 skill；标准 builder 与判定脚本不导入两者，也不接受 optional flag。时间副层由独立 `scripts/build_timing_overlay.py`
   生成：标准 builder 不导入它，它也不导入 Tajika／KP。
7. 不读取其他 `prashna_*` 目录；追问只沿用当前盘。

---

## 默认层禁入项

不得消费或输出：

- Chara Karaka、DK、UL、AL；
- SAV／BAV、Shadbala、Bhava Bala；
- 完整 D9、D10、D4、D5 等本命分盘；
- engine 的 functional P1 身份、natal yoga prescan（宫表的吉凶标签是 `P-I.3` 注的 Ayer 功能吉凶，从被占据／照射的星座起算，不是 P1）；
- 120年 Vimshottari、Chara Dasha；
- transit、Sade Sati、double transit；
- Tajika orb／applying／separating；
- KP cusp／sub-lord。

本命专用的尊贵度结算不进即时盘：落陷解除（Neecha Bhanga 档位）、落陷 Vargottama 三分类、Pushkara 补丁。即时盘的落陷、逆行只按能力层的
折损与救应读（`M-XIV.39–40` Raman 注，`judgment-rubric.md` §5），根本三角归本座。

只允许 rising Navamsa（星座与序号）、Lagna 所在 drekkana、Lagna 六分盘座主表三项有限数据，因为 `P-I.4`（注：Lagna、Hora、Drekkana、Navamsa、
Dwadasamsa、Trimsamsa 六分盘）、`P-I.7`、`P-VI.1~2`、`P-VI.4`、`P-VII.13` 明确使用它们；禁止由此展开完整 D2、D3、D9、D12、D30 解读。

---

## Phase 0：输入与门控

| 输入 | 规则 |
|---|---|
| 具体问题 | 一个可观察结果，或一个描述对象（相处、局面）；一句多问先拆、先选一个（`question-decomposition.md` 第 8 节） |
| 提问时刻 | 用户说"现在"或直接发问时，取用户这条消息到达的时刻（提问地时区，保留秒和小数秒）；不在处理数分钟后另取整分钟。用户给了显式时刻就用它 |
| 提问地点 | 城市或经纬度；必须能确定 IANA 时区。只给城市名时查 `locations.md`；地点、时区未知时澄清，不用机器时区代替 |

时间地点由提问人负责：按所给的起盘，不因精度追问用户，也不在判读里谈输入精度（`judgment-rubric.md` §13）。

门控：模糊、假设、已发生、A／B 二选一按 `question-decomposition.md` 第 8 节澄清；不判与操控、打听类按 `matter-rules.md` 第 6 节一句话说明并给替代问法；
同一问题和现实状态未变化时沿用第一次清晰提问盘（`qa_rules.md` §1），不使用 24 小时、3 个月阈值；出现自伤或极端语句时先回应安全，不起盘。

进入下一阶段条件：问题可拆出一个可观察结果或描述对象，时间地点完整。

---

## Phase 1：起盘

```bash
python scripts/build_prashna_data.py \
  --datetime "<YYYY-MM-DD HH:MM[:SS[.ffffff]]|now>" \
  --lat <lat> --lon <lon> --tz "<IANA>" \
  --question "<single observable question>" \
  --label "<kebab-case>" --out-parent "<parent>"
```

`build_prashna_data.py` 只读共享 engine，并用 Prashna 专用 formatter 输出白名单。进入下一阶段条件：产物存在，默认白名单无越权字段。

---

## Phase 2：拆题与取象

按 `question-decomposition.md`：

1. 拆出行动者、动作、对象、结果、限定语；判型（事件型、行动型、描述型），定每个子问题的出口；
2. 别人的动作以那个人的宫为命宫转宫（对方主动＝本盘 9 宫，不是本盘 3 宫）；
3. 逐句抓关键词，查 `house-meanings.md` 关键词库，记下宫与星、相合还是相反、出处；
4. "事情成不成"查 `matter-rules.md` 登记表取 `matter`；表外取 `通用`，按宫义选事项宫并写明出处；描述型取 `描述`（只出事实、不定档）；查表题跳到 Phase 5 按 `matter-rules.md`
   第 5 节输出；
5. 写取象单 `prashna_plan.json` 到当前 `prashna_*` 目录。

进入下一阶段条件：取象单每个关键词有出处，每个子问题有唯一出口。

---

## Phase 3：判定

```bash
python scripts/judge_prashna_standard.py \
  --datetime "<与 Phase 1 完全相同>" \
  --lat <lat> --lon <lon> --tz "<IANA>" \
  --plan "<当前 prashna_* 目录>/prashna_plan.json" \
  --out-dir "<当前 prashna_* 目录>"
```

读 `prashna_verdict.md`：成事账（每条规则、方向、计分、合计）、内部档与强度、能力层、限定语、行动链、输入提示。判读按它写，**不手算、不改档**。描述型只有事实表，没有档。
写的时候发现取象错了（关键词、事项宫、行动者），改取象单重跑；发现规则本身读错，按 `qa_rules.md` §4 纠错。

进入下一阶段条件：`prashna_verdict.md` 存在，与取象单一致。

---

## Phase 4：时间副层

`prashna_verdict.json` 的 `timing` 不为 `none` 时运行（偏成、持平且非盘面未给方向）：

```bash
python scripts/build_timing_overlay.py \
  --datetime "<与 Phase 1 完全相同>" \
  --lat <lat> --lon <lon> --tz "<IANA>" \
  --matter-house <判定的事项宫> --mode <timing 字段：general|return> \
  --verdict favorable|pending \
  --out-dir "<当前 prashna_* 目录>"
```

偏成写"约……"，持平写成条件式（"如果推进顺利，大约……"）；偏不成不运行，判读单写明不给时间、什么变化之后可以再问。几个候选并列，不平均、
不折中；婚恋题另看 `M-XVII.31` 偏早提示；问题自带日期时只说盘面节奏与最近触发日，判断不了是否恰好落在那天（`timing-layer.md`）。

---

## Phase 5：判读单

写入 `prashna_judgment_<label>.md`，按 `judgment-writing.md`（结构、内容契约、安抚、高频题型要点）。聊天里显示给用户看的部分（标题到
"现在能做什么"）；用户要看依据时再展开核对区（直接引用 `prashna_verdict.md`）。给用户看的部分不出现档名、`rule_id` 和输入精度；行动型问题
标题与简述各用一句分别答"会不会动"和"事情成不成"。

查表题的判读单：标题、简述、正文用白话写查表结果，两说都写；核对区只留"这张盘的范围"和一张查表；不写三档和时间。
描述型的判读单：讲局面与相处的样子，约 1,500 字，不写成败与时间；核对区引用事实表（`judgment-writing.md` 第 7 节）。

---

## Phase 6：追问

已有盘追问不重起，读取 `qa_rules.md`，只访问当前 `prashna_*` 目录（KP 追问只访问当前 `kp_horary_*`）。追问不改档；补限定语、换问法按
`qa_rules.md` §1、§4；跨栈比较只并列、不拼票。

---

## Tajika 可选副层

默认关闭。只有用户显式要求 Tajika／Itthasala／applying-separating 时才读取
`tajika-optional.md`。

先完成标准层 Phase 2，取得 Lagna lord 和唯一事项宫主，再运行独立
`scripts/build_tajika_overlay.py`。不得在标准 builder 上增加
`--enable-tajika`。查表题、不判题、描述型，以及问者星与事项星为同一颗（事项宫为 1 宫
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

---

## 本命交叉

本命交叉默认关闭。用户明确要求时读取 `cross-natal-policy.md`；当前版本因旧裁决规则未完成来源重审而失败关闭，不能调用不存在的 build 参数，
也不能用 SAV、本命 Dasha 或分盘升降 Prashna 结论。

---

## 最终自检

- [ ] 已完整读取六个默认资源？
- [ ] 取象单的关键词都有出处，每个子问题只有一个出口，别人的动作从那个人的宫起算？
- [ ] 判定由 `judge_prashna_standard.py` 生成，判读的倾向与内部档一致，没有手算或改档？
- [ ] 默认产物由专用 formatter 生成，未使用 Chara Karaka、SAV、完整分盘、本命 Dasha 或过运？
- [ ] 给用户看的部分没有判词、档名、`rule_id` 和输入精度，行动型问题两问分答？
- [ ] 偏成／持平才给时间，偏不成与盘面未给方向没给？
- [ ] 查表题只给查表结果、两说并列，没有出三档和时间？
- [ ] 情感类安抚只出现一次、有盘面依据、没有改结论？
- [ ] 提问时刻保留秒级，且没有用处理时刻替代用户提问时刻？
- [ ] 标准／Tajika 产物只写入当前 `prashna_*`，KP 只写入独立 `kp_horary_*`；标准 builder 与判定脚本未导入 Tajika／KP？
- [ ] 若启用 KP，是否由用户给了 1–249 数字，题型与用户确认的可观察结果一致，未把回暖／联系改写成关系落实？
- [ ] Tajika／KP 都有可读判读，且未进入标准账本？追问沿用当前盘，跨栈比较只并列、不拼票？
