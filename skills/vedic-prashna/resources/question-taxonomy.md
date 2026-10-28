# Prashna 问题门控 + 支持级 + 提问地推断

> **用途**：先把问题收敛为一个可观察结果，再判 A／B／C 支持级。禁止为了
> “一定能答”而把问题硬塞进最相似的宫。
>
> **调用时序**：输入检测 → 单问澄清 → 支持级 → 时间地点敏感性 → 起盘。

---

## 1. 问题分类与支持级

先看**动词**，再看对象：

```
问 "能不能" / "会不会" / "是否发生"
├─ `house-karaka-map.md §3` 有题目专属 P 规则 → A级
├─ 只有一般事项宫／宫主或 Bhavan 实例 → B级
└─ 事项宫或结果本身不可观察／未核证 → C级，停止硬套

问 "何时"
├─ 先判断对应结果题是否为 A/B级，并定出内部三档（偏成／持平／偏不成）
└─ 偏成或持平：加时间副层（`timing-layer.md`）；偏不成：不给时间

问 "选哪个"（AB 二选一）
└─ C级：不得在同一分钟机械起两张几乎相同的盘

问 "在哪／什么方向／多远／丢的是什么／是谁拿的"（失物、失踪者）
└─ 描述题：§2.10 查表，不出三档，不跑时间副层

问 "会不会下雨"（雨季）
└─ 天气题：§2.11 查表，不出三档，不跑时间副层

问 "生死、寿命、对方在想什么、对方私生活"
└─ C级：§2.13，不起盘
```

AB 选择先让用户选一个最想执行的方案，改问“执行 A 能否达到 `<可观察结果>`”。
若用户需要 A/B 同时比较，应走非 Prashna 的决策分析，不伪造两张独立心念盘。

---

## 2. 澄清话术（用户提问不合规时）

### 2.1 模糊问题（"帮我看看运势""感情怎么样"）

**触发**：问句没有明确动作或时间指向。
**响应模板**：

> "Prashna 卜卦要一个**具体、能判定"是/否/何时"**的问题。'看看运势' 这样的问法我起盘也答不了。
> 你现在最想知道的是哪一件事？举几个可判定的例子：
> - 「我接受这份 offer，能不能顺利入职?」（可观察结果）
> - 「我和 XX 的婚事能不能定下来?」（成败）
> - 「我这个官司会赢吗?」（吉凶结论）
> 你选一个方向告诉我，我先检查标准层是否有对应规则。时间只在盘面偏向推进或两边相当时
> 给一个大致范围，不承诺精确日期。"

### 2.2 多问题合并（"我想问事业和婚姻"）

**触发**：一句话里塞了 2 个及以上分类。
**响应模板**：

> "Prashna 一张盘只答一问——多问混判反而不清楚。
> 你现在想先问哪一个？另一个我们等下再起一张盘。"

**不合并起盘**：多问会使事项宫和适用专题规则不唯一，无法建立可审计规则账本。

### 2.3 假设性问题（"如果我 XX 会怎样"）

**触发**：句式带"如果/假设/万一"。
**响应模板**：

> "'如果……会怎样' 这种假设 Prashna 的判据不明确。我给你转成两种可判定的问法，你选一个：
> - 「我执行 XX，能不能达到 YY 结果?」（一般所谋之事）
> - 「XX 结果会不会发生?」（事项宫／专题规则）
> 选哪个?"

### 2.4 已发生事件（"上周面试怎么样"）

**触发**：问句时间已过 + 用户此刻起盘。
**判定**：只有结果仍未知或仍在发展时，才能改问“这件事最终会不会出现 `<可观察
结果>`”。若结果已经客观发生，不能用现在的盘反推当时过程；应复盘原提问盘或使用
事件资料。这里不使用“超过1年”等任意时间阈值。

### 2.5 反复起盘同一问题

**触发**：问题、目标和现实状态没有实质变化，却要求用新时刻反复测试。
**响应模板**：

> "这个问题和现实状态都没有变化，继续换时间起盘只会变成挑答案。我们沿用第一次
> 清晰提问的盘做追问。只有目标、对象、已发生事实或待决定行动发生实质变化，才建立
> 新问题；不能用固定小时／月份阈值代替这个判断。"

这是 `E` 工作流门控，不写成某条古典成败规则，也不把后起盘解释成“事情不成”。

**同一段关系的不同问法算同一问题**：对同一个人问“会不会联系／回复我”“能不能
复合”“我挽回能不能成”，属于同一问题。沿用第一张盘和它的结论作答，不另起盘，
也不换一条规则重判出第二个结论。对方已经联系、已经复合或已经明确拒绝，才算现实
状态的实质变化。

**分类更正（唯一例外）**：若首次判读把问题归错了题型（例如"对方会不会主动约我见面"被归进
"合作、另一方会否配合"），追问时可在**同一张盘**上按正确题型重建一次账本，核对区标明"分类更正"
及原因。这是纠正门控错误，不是第二个结论；同一问题只允许更正一次。
问题后来补充的限定语（如"必须由对方发起"）不算分类错误，按 `judgment-rubric.md` §2.3 检验限定语，
不重建账本。

### 2.6 时间未定（“我以后能不能……”）

**触发**：完全无时间锚点。
**响应模板**：

> "我可以判断当前盘对这件事的支持方向。盘面偏向推进或两边相当时，可以附一个有原典
> 出处的大致时间；偏向难以推进时不给时间，但会说明什么变化之后可以再问。请把问题限定为
> 一个可观察结果。"

### 2.7 复合／联系专项

**适用**：分手后、冷战中或断联的关系。先按动词归到下表一行，一张盘只判一行。

| 问法 | 主规则 | 辅助规则 | 支持级 | 事项宫 |
|---|---|---|---|---:|
| 能不能复合／和好／复婚 | `P-III.3~4`（类比） | `P-I.3`（7 宫） | B | 7 |
| 喜欢的人能不能在一起；表白能不能成；能不能确立关系 | `P-I.4` | `P-I.3`（7 宫）；`M-XVII.5／15／16／17`（类比） | B | 7 |
| 对方会不会联系我／回复我 | `P-III.3~4`（类比） | `P-I.3`（7 宫） | B | 7 |
| 能不能见面、约会；对方会不会来、会不会主动约我 | `P-I.4`（一般所谋之事） | `P-I.3`（7 宫）；恋爱语境加 `M-XVII.5／15／16／17`（类比） | B | 7 |
| 我主动挽回能不能成 | `P-I.4` | — | A | 1 |
| 已搬走的伴侣会不会回来同住 | `P-I.2`；Chapter II／V | — | A | 按专题角色 |
| 能不能结婚 | `P-VII.2` | `P-VII.1`；`P-I.3`（7 宫）；`M-XVII.5／15／16／17` | A | 7 |
| 对方还爱不爱我；对方和现任会不会分手 | — | — | C | 不判 |
| 有没有缘分；能不能长久 | 先澄清，改成上面某一行 | — | — | — |

执行要点：

- `P-III.3~4` 原文是王者之间的和解；Ayer 注说它“can be used in all cases where
  settlement of scores is involved”。用于复合是类比，所以标 B级。
- 人形星座（human signs）：`P-III.3~4` 取 Gemini、Virgo、Libra、Aquarius，依据 III.3 的
  Ayer 注；`P-IV.2` 按本偈正文只取 Libra、Gemini、Aquarius，不加 Virgo。各用各的清单。
- III.3 的“凶星落变动座则冲突”属于和解规则本身，要用。`P-I.2`、`P-II.1~2` 的
  动座／固定座条件讲的是位置得失，不进复合主判。
- III.4 吉凶星混合落 kendra 或人形 Lagna 时，Ayer 注是“will tend to continue the
  tension without resolving it, a preponderance of benefic influence leading to
  prospective resolution”：按 `judgment-rubric.md` §4.1 数吉凶，吉占优记趋向和解
  （困难后成），凶占优记不利，持平记混合（0 分）。
- 能不能结婚：`P-VII.2` (a) Moon 落 3／5／7／11／6 宫且受 Jupiter、Sun、Mercury 照，或
  (b) 吉星落角宫／三方宫，则议婚能成。注：点名的是自然吉星，实指功能吉星；其余配置为否。
  按宫表标签读：(a) 看 Moon 所在宫行的“七曜照射本宫”，有吉标签照即记满足（原文点名
  三星，注只说改按功能取，未说须几颗，这是执行口径）；(b) 看 1／4／7／10／5／9 宫行的
  “七曜占据”。“Sun”不是自然吉星，疑为 Venus 误印，无梵文无法核实，照录。辅助
  `P-VII.1`：Saturn 落 Lagna 起奇数宫（不计 Lagna）兼示得新娘，否则兼示得新郎，问娶
  看前者、问嫁看后者；注列三问的次序（胎儿、新郎、新娘）与正文不一致，按正文。
  另加 *Prasna Marga* 第十七章四偈（核证矩阵 `M-XVII` 行）。
- 表白／确立关系：没有专属偈，按一般所谋之事走 `P-I.4`，再按 *Prasna Marga* 第十七章婚姻
  卜问类比加四偈，标 B 级。PM 原文是议婚语境，Lagna 读女方、7 宫读男方（XVII.8–9）；这里
  沿用 Lagna＝提问人、7 宫＝对方。
- 见面、约会、对方会不会来或主动约：属"某个人会不会做一件具体的事"。没有专属偈，按一般所谋之事走
  `P-I.4`，事项宫取行动者的宫（`house-meanings.md` 第 3 节：对方 7、上级 10、母亲 4……），加该宫 `P-I.3`；
  B 级。问题里的"主动""私下""在家"等是限定语，按 `judgment-rubric.md` §2.3 检验，不另立题型。
  Ch.2 到达诸偈（敌军来不来，`P-II.6~8`、`P-II.11`、`P-II.13`，*Prasna Marga* XXIV.68 注明可用于人会不会来）
  尚未逐偈审定，暂不进账本。
- 对方会不会联系：没有示范题。断联、冷战后恢复联系是双方关系的缓和，按 III.3 注“all cases where
  settlement of scores is involved”类比收 `P-III.3~4`，与复合同标 B 级（10-21 创始人定）。

**操控／打听类不判**：打听对方行踪、新伴侣信息或隐私；问“怎么让他回来”“怎么让他
离开现任”。用一句话说明为什么不判（这类问题要的是控制或窥探另一个人，卜卦不做），
再给替代问法，例如“我主动挽回能不能成”。不说教。

### 2.8 求职／考试专项

| 问法 | 主规则 | 辅助规则 | 支持级 | 事项宫 |
|---|---|---|---|---:|
| 能不能找到工作；能不能拿到（满意的）offer；面试能不能过；能不能升职 | `P-IV.3`；`P-II.1`（星座类型）；`P-II.2`（照射） | `P-I.3`（10 宫） | A | 10 |
| 会不会被裁／调岗／换工作；能不能保住工作 | `P-I.2` Chyuti | `P-II.1` 动／固座（Chyuti 读的正是 Lagna 的占据与照射，与 1 宫 `P-I.3` 同源，不另计） | A | 1 |
| 竞争性考试（按排名录取：考研、考公、选拔） | `P-II.1~2` | `P-III.1` | B | 1 |
| 达标性考试（过线即过：驾照、资格证） | `P-I.4` | — | A | 1 |
| 面试表现如何；面试官怎么看我 | — | — | C | 改问“能不能拿到这个 offer” |

执行要点：

- `P-IV.3`：吉星落 10 宫和 7 宫赐位置；凶星落 12、11 宫不吉。原文是“(Malefic) Moon
  in lagna will not give favourable results, while in the tenth (even when malefic) it
  will”：Moon 落 Lagna 只在亏月时记不利；落 10 宫不论盈亏都有利。`P-II.1~2`：固定座
  上升主得位，动座相反（注“he will not get the position”）；变动座混合，Ayer 注引
  Bhattotpala *Prasnagyana*：上升点在前半按固定座读，后半按动座读，离 15° 很近时算输入
  敏感。吉星照 Lagna 与 Moon-lagna 吉，凶星照则凶，吉凶同照为混合。Ayer 在 II.1 注里
  把“landing a job”列为得位的一种。
- `P-II.1~2` 在账本里记两条：星座类型一条（II.1，含 II.2 首句“动座相反、变动座混合”），
  照射一条（II.2 后句）。两偈；Ayer 注只说合起来列表，没说捆成一条。
- 问“满意的 offer”：账本同上；`P-IV.3` 后半句“吉星落 2、5、1 宫得名与财”用来讲待遇和
  满意度，不计分。
- 裁员／调岗／换工作走 `P-I.2` Chyuti（Ch.1 示范题“Is a change of job imminent? Will
  I lose my job? Will I be transferred?”）。Ayer 注：Lagna 动座，且受本宫主或吉星占据／
  照射、没有凶星占据／照射，则变动成立；固定座即使无凶星也不变；变动座看吉凶影响
  孰多（按 `judgment-rubric.md` §4.1 第 1 条数）。问“会不会被裁／调走”时，变动成立＝会；问“能不能保住”时方向相反。辅助只用
  `P-II.1` 的动／固座；`P-II.2` 的“吉星照 Lagna 吉”在 Chyuti 里反而促成变动，不用。
- 竞争性考试：Ch.2 示范题 1&2“Will I succeed in the competitive examination?”挂
  `P-II.1~2`；`P-III.1` 原文是战事胜负，Ayer 注扩到“elections and such other
  competitive efforts”，作辅助规则。示范题只挂靠、正文未覆盖，所以标 B级。
- `P-II.8`、`P-II.10` 的示范题也挂了考试，但正文是敌军动向，原文没写敌军来去如何
  对应考试成败，已知未收。
- 多环节考试（初试、复试、面试）：只问最近一个还没出结果的环节。
- 面试卡点按账本条目讲成条件：Lagna 一侧的条目讲“你这边的准备和时机”，10 宫一侧讲
  “职位和流程那边”；必须对应规则账本里的具体条目，不评判人，不从盘里读性格、口才等特质。
- 吉星／凶星一律读宫表的 Ayer 功能吉凶标签（`standard-layer.md` §2.1）。`P-III.1`
  注明说“mention of planets by name is only symbolic; their functional character
  should be taken”，所以 9 宫的 Mars／Saturn 与 Mercury／Jupiter／Venus 也按 9 宫行的
  标签读，不按名字读。

### 2.9 情绪与安全

问题里出现自伤或极端语句时，先回应安全，不起盘。安抚的写法见 `SKILL.md`
Phase 6。

### 2.10 描述题（失物、失踪者）

**适用**：问东西或人在哪、什么方向、多远、丢的是什么、是谁拿的。“能不能找回、
快不快”是成败题，走 §2.12 失物行。
只给 `structured_prashna.md`“描述题与天气查表事实”一节的查表结果，不建规则账本、
不出三档、不跑时间副层（`standard-layer.md` §5.1）。

| 问法 | 规则 | 查表依据 |
|---|---|---|
| 是不是家里人拿的；还在屋里吗 | `P-VI.1` | 固定座、固定 Navamsa 或 vargottama 上升：亲属所拿、藏在屋内；Bhattotpala：否则外人拿走 |
| 藏在屋里哪个部位 | `P-VI.2` | Lagna 所在 drekkana：门槛／中间部分／后院；只在 VI.1 读作“屋内”时用 |
| 往哪个方向、多远 | `P-VI.4` | 角宫行星定方向，无则 Lagna 星座；距离按 rising Navamsa 序号，只报相对远近 |
| 丢的是什么类东西 | `P-I.7`；`P-VII.13` | rising Navamsa 序号定 Dhatu／Moola／Jeeva；大小 |
| 何时丢的、去向、放在什么地方、拿的人多大 | `P-VII.13` | 星座定时段、方向、藏放处；Lagna 主定年龄 |

执行要点：

- `P-VI.4` 恰有一颗角宫行星时，正文“by the planets occupying kendras”与注“Two or
  more planets”读法不一，两说并列。距离原文单位是 yojana，注称按现代条件另定尺度，
  所以只报相对读数。
- `P-I.7` 注中 Mesha 举例（第二 Navamsa 为 Jeeva）与注表（2／5／8 为 Moola）矛盾，
  以译文和注表为准。
- `P-VII.13` 不收：颜色与窃贼外貌（注指向 Brihad Jataka／Saravali，本地无原文）；
  种姓；“Relation by karaka”、Navamsa 强弱、“concerned planet”落陷燃烧（原文未给判据
  或未指明是哪颗星）。
- `P-I.6`（所想之物）、`P-VII.6~9`（所问何人）属读心，不收。
- 同时问“能不能找回”时，成败部分另走失物题账本（§2.12 失物行），两部分
  分开写。

### 2.11 天气（雨季会不会下雨）

**适用**：用户所在地正值雨季，问今天或近期会不会下雨。非雨季不适用；雨季与否由
用户提供，不从盘里推。只给查表结果，不出三档，不跑时间副层。

| 规则 | 有雨条件 |
|---|---|
| `P-VII.3` | Venus 与 Saturn 落 (a) Moon 起 7 宫（注：Venus 不可能落 Sun 起 7 宫），或 (b) Lagna 起 2／3／4／8 宫 |
| `P-VII.4` | (a) 白半月，吉星落水象座的 3、2 宫或角宫；或 (b) Moon 落水象 Lagna |

执行要点：

- 原文只写有雨条件，没有反面判据。条件不满足时写“原文无反面判据”，不判“不下雨”。
- 水象座两说并列：Horasara 取 Cancer、Capricorn、Scorpio、Pisces；Mantreswara 取
  Cancer、Capricorn 后半、Pisces。
- `P-VII.3` 只有一颗星满足条件时，正文“Venus and Saturn”是否要求两星同时满足未明，
  两读并列。
- `P-VII.4`(a) 的吉星读宫表标签。

### 2.12 其他专项

| 问法 | 主规则 | 辅助规则 | 支持级 | 事项宫 |
|---|---|---|---|---:|
| 失物能不能找回 | `P-VI.3` | `P-V.1`、`P-II.1~2` 动／固座；快不快另看 `P-I.5`（不计分） | A | 11 |
| 能不能买房／置产；住处问题能不能解决 | `P-I.2` Vriddhi | `P-II.1~2` 动／固座；`P-I.4`（第 4 偈示范题“I want to buy a property; will I succeed?”）（Vriddhi 与 4 宫 `P-I.3` 同源，不另计） | A | 4 |
| 出国、签证、留学、调动能不能办成 | `P-I.4` | `P-I.3`（1 宫） | A | 1 |
| 路上顺不顺 | `P-II.5` | — | A | 1 |
| 会不会离开、搬走；能否早日出发 | `P-I.2` Pravasa | `P-II.1~2` 动／固座；问“能否早日出发”时加 `P-II.9`（不收 10 宫 `P-I.3`，反向同源） | A | 10 |
| 在外的人或失踪者会不会回来 | `P-V.1`；失踪者寻得快不快另看 `P-I.5`（不计分，同失物） | `P-V.2~3`、`P-III.5`、`P-I.2` Nivritti 与 4 宫、`P-II.1~2` 动／固座 | A | 7 |
| 病能不能好（含代他人问） | `P-IV.5` | `P-II.1~2` 动／固座 | A | 1 |
| 被诬陷／名誉能不能保住 | `P-I.2` Vriddhi | `P-I.2` Nivritti；`P-II.1~2` 动／固座；`P-IV.3` 2／5／1 宫 | A | 4 |
| 谈判／和解能不能达成 | `P-III.3~4` | `P-I.3`（7 宫） | A | 7 |
| 该不该投资某标的；会不会亏 | `P-IV.2` | `P-I.3`（11 宫） | B | 11 |
| 生意亏损能不能补回 | `P-V.1` | `P-I.3`（11 宫） | B | 11 |
| 官司会不会很快开庭 | `P-II.11` | — | B | 4 |
| 胎儿是男是女 | `P-VII.1` | — | A | 查表输出男／女 |
| 父亲是否在外地 | `P-VII.12` | — | A | 查表输出在外／在本地 |

执行要点：

- 失物：`P-I.5` 满月落 Lagna 受 Jupiter 或 Venus 照（按点名），或强吉星落 11 宫，则
  速得；满月按注取满月窗（白半月第 10 至黑半月第 5 tithi），读 Moon 节的
  `full_moon_window`。I.5 只答快不快，不计分：原文只说“quickly recovered”，不满足推不出
  找不回。`P-VI.3` 是能否找回的主规则：满月或吉星占 Lagna、头升座上升受吉星照、强吉星
  落 11 宫则速得，Bhattotpala：皆无则渺茫（“chances of recovery are remote”）。头升座 Ayer 注列 Leo、Virgo、Libra、
  Scorpio、Aquarius，没有 Gemini；Lagna 为 Gemini 时两说并列（计分见 rubric §2.4）。`P-V.1` 吉星落 5／2／3
  宫则失物复得。I.5、VI.3 的强吉星按 D1 `exalted`／`own_sign` 算（`standard-layer.md`
  §2.1）。`P-II.1~2` 注：固定座“hidden from view, possibly misplaced inadvertently”，
  没丢、一时找不到；动座“object lost is irrecoverable”；变动座前半按固定座、后半按动座。
- `P-I.2` 四问的方向各不相同：Vriddhi 是 4 宫受本宫主或吉星占据／照射、且“unspoiled by
  other planetary dispositions”则兴（4 宫同时有凶标签占据／照射时记混合，执行口径）；Pravasa
  是 10 宫动座且受凶星照才成行，受本宫主或吉星照反而不成；Nivritti 是 7 宫动座且受
  本宫主或吉星照则返回，受凶星照则否。不能互相套用。
- 买房／置产：`P-I.2` Vriddhi 定结果。`P-II.1~2` 辅助：固定座得住处（注“acquisition of a
  dwelling place”），动座“he will not get the position or home desired”，变动座前半按固定座、
  后半按动座。Vriddhi 与 4 宫 `P-I.3` 读同一组占据／照射，只计 Vriddhi。另收 `P-I.4`：Ayer 在第 4 偈
  示范题挂“I want to buy a property; will I succeed?”。
- 出行按问法分三行（执行口径；Ayer 示范题分挂三处）：问能不能办成走 `P-I.4`（第 4 偈
  “I am thinking of going abroad; will I succeed?”）；问会不会离开走 Pravasa（第 2 偈“Will my
  contemplated journey materialise?”“Can I leave this city for good?”），原文“only when”，满足的
  盘很少，照实说；问路上顺不顺走 `P-II.5`（Ch.2 示范题 5“bon voyage or meet with trouble on
  the way?”）：动座上升有吉星占据则利行人，凶星占据则害，固定座上升有凶星占据行人亦平安，
  条件都不满足时本条不出方向。现代人问“能不能出国”多半是问办不办得成，先按此澄清。
- 出行（会不会离开）：`P-II.9` 按点名行星——动座上升且 Sun／Saturn／Mercury／Venus 之一占据则很快
  出发，该星逆行则否。Ayer 注称日月无逆行、“should be kept out of reckoning in this
  context”：Sun 只免逆行判断、还是整体不计入，两读并列（计分见 rubric §2.4）。`P-II.1~2` 注：固定座“neither
  departure nor arrival”，不成行；动座相反；变动座前半按固定座、后半按动座。
- 返回：`P-V.1` 行星落 5／2／3 宫则返回，Jupiter／Venus 落此则快；`P-V.2` 7 或 6 宫有
  星、Jupiter 落角宫或 Mercury／Venus 落三方宫；`P-V.3` Moon 落 8 宫且角宫无凶星则平安
  返回；`P-III.5` Jupiter 或 Venus 落 2／3 宫则很快到来。点名行星的按点名读。
  `P-V.3` 注：Moon 与角宫吉星都不可弱（“should not be weak”），D1 `debilitated` 算弱。
  `P-I.2` 4 宫两说并列（计分见 rubric §2.4；`P-V.2` 的且／或同样按两说算）：正文“One returns from abroad, with a planet's occupation of the
  fourth house”，有行星落 4 宫则回；注“the person from abroad has come home when the fourth
  house contains its own lord or is aspected by it and not otherwise”，4 宫主占据或照 4 宫
  才回。`P-II.1~2` 注：固定座“neither departure nor arrival”，不来；动座正文“相反”，注
  “he has not arrived; he is moving”，在途、尚未到达，记有利（执行口径）；失踪者固定座注
  “not gone abroad or far away, nor dead”，只取“没走远”，生死按 §2.13 不判。
  方向距离走 §2.10 `P-VI.4`。“是否平安、是否还活着”不判（§2.13）。
- 疾病：`P-IV.5` 吉星落 Lagna／7／8／5 宫且彼此相照，Moon 落 3／6／10／11 宫则康复；
  Bhattotpala 只补“落这些宫的吉星（Moon 除外）须彼此相照”。Ayer 注：凶星落这些宫且 Moon
  落别处则相反；配置不全时看有利影响是否占优（按 `judgment-rubric.md` §4.1 数，吉占优记
  终可康复）。`P-II.1~2` 注：固定座“cure is doubtful”，动座“chances of recovery are good”，
  与求职方向相反。“彼此相照”按标准层“派生结构事实”的“七曜互视”行判（执行口径）：同宫
  不算互照，只有一颗吉星不算满足；正反配置任一完整成立、且不混对方成分时直接定方向，
  其余都按 §4.1 数。代他人问病同样读 1 宫：Ch.4 示范题 5“My brother is seriously ill;
  will he recover completely?”挂本偈。只答能否康复，不作医疗诊断，不替代就医。
- 名誉：依据 `P-I.2` 注的诽谤例——先看 Vriddhi（4 宫）定结果，再看 Nivritti（7 宫）
  定对方能否得逞；`P-II.1~2` 注辅助：固定座“honour and reputation … fixed signs rising
  ensure safety”，动座“humiliation is certain”，变动座前半按固定座、后半按动座。`P-IV.3`
  吉星落 2／5／1 宫得名利（fame and wealth），作辅助规则。
- 谈判／和解：`P-III.3` 注“all cases where settlement of scores is involved …
  negotiations”，原文覆盖，标 A；复合仍按 §2.7 类比标 B。
- 投资：`P-IV.2` 吉星落 3／5／11／7 宫得益、凶星则损，照射等同占据（注）；Ch.4 示范题
  “Should I invest in this particular scrip or will it ruin me?”只挂靠，标 B。吉星落人形座
  亦吉，人形座按本偈正文取 Libra、Gemini、Aquarius，不加 Virgo（§2.7）。
- 亏损补回：`P-V.1` 吉星落 5／2／3 宫则失物复得；Ch.5 示范题“I have incurred a loss in
  my business; can I expect to make it good soon?”，标 B。
- 开庭：`P-II.11` Sun 与 Moon 落 4 宫则不来，Mercury、Jupiter 与 Venus 落 4 宫则很快来，
  按点名读。两处原文都是“and”，按字面读作同落；三星同落 4 宫少见，两组都不满足时本条
  不出方向。Ch.2 示范题“Will the suit against me come up for hearing soon?”，标 B。
  “官司能不能赢”不在此行。
- 胎儿性别：`P-VII.1` Saturn 落 Lagna 起奇数宫为男，否则为女；注：按 Varahamihira，
  Lagna 本身不计入奇数宫。只用于已怀孕的提问，不作医学判断。`P-VII.5` 需要六分盘
  varga，本批不收。
- 父亲下落：`P-VII.12` Sun 带吉星落 8 宫且受吉星照则在外，否则在本地。注称其他
  karaka 可同法处理，但原文未列 karaka 对应表，其他亲属本批不收。
- 胎儿性别与父亲下落输出查表结果，不出三档，不跑时间副层。

### 2.13 不判（C级）

- 生死、寿命、“还活着吗”：Ch.2、Ch.5 示范题与 `P-V.4`、`P-VII.11` 有此类问法，标准层
  不判。用一句话说明不判，必要时建议联系当事人或相关机构。
- 读心与隐私：所想之物（`P-I.6`）、所问何人（`P-VII.6~9`）、他人私生活（`P-VII.10`）、
  对方心理。
- 继承（`P-IV.4`）、选举、某职位竞争大不大（`P-II.6`）、“我的困境能不能解决”：
  本批未单列题型。困境类按 §2.3 改为一个可观察行动结果，走 `P-I.4`。

---

## 3. 提问地 → 时区详表

补 SKILL.md 前置门控里"高频案例"未覆盖的完整表。

### 3.1 亚洲

| 地区 | IANA tz |
|---|---|
| 中国大陆(全境同 tz) | Asia/Shanghai |
| 中国台湾 | Asia/Taipei |
| 中国香港 | Asia/Hong_Kong |
| 中国澳门 | Asia/Macau |
| 日本 | Asia/Tokyo |
| 韩国 | Asia/Seoul |
| 朝鲜 | Asia/Pyongyang |
| 蒙古 | Asia/Ulaanbaatar |
| 新加坡 | Asia/Singapore |
| 马来西亚 | Asia/Kuala_Lumpur |
| 印尼西部(雅加达) | Asia/Jakarta |
| 印尼东部(巴厘岛/望加锡) | Asia/Makassar |
| 泰国 | Asia/Bangkok |
| 越南 | Asia/Ho_Chi_Minh |
| 菲律宾 | Asia/Manila |
| 印度 | Asia/Kolkata |
| 巴基斯坦 | Asia/Karachi |
| 阿联酋(迪拜) | Asia/Dubai |
| 沙特 | Asia/Riyadh |
| 以色列 | Asia/Jerusalem |
| 土耳其 | Europe/Istanbul |

### 3.2 欧洲

| 地区 | IANA tz |
|---|---|
| 英国 | Europe/London |
| 爱尔兰 | Europe/Dublin |
| 法国/德国/意大利/西班牙/荷兰 | Europe/Paris / Berlin / Rome / Madrid / Amsterdam |
| 俄罗斯莫斯科 | Europe/Moscow |
| 瑞士 | Europe/Zurich |
| 北欧(挪威/瑞典/丹麦/芬兰) | Europe/Oslo / Stockholm / Copenhagen / Helsinki |
| 希腊 | Europe/Athens |
| 波兰 | Europe/Warsaw |
| 乌克兰 | Europe/Kyiv |

### 3.3 美洲

| 地区 | IANA tz |
|---|---|
| 美东(纽约/波士顿/迈阿密/华盛顿) | America/New_York |
| 美中(芝加哥/达拉斯/休斯顿) | America/Chicago |
| 美西山地(丹佛) | America/Denver |
| 美西太平洋(旧金山/西雅图/洛杉矶) | America/Los_Angeles |
| 阿拉斯加 | America/Anchorage |
| 夏威夷 | Pacific/Honolulu |
| 加拿大多伦多 | America/Toronto |
| 加拿大温哥华 | America/Vancouver |
| 墨西哥城 | America/Mexico_City |
| 巴西圣保罗 | America/Sao_Paulo |
| 阿根廷 | America/Argentina/Buenos_Aires |
| 智利 | America/Santiago |

### 3.4 大洋洲 / 非洲

| 地区 | IANA tz |
|---|---|
| 澳东(悉尼/墨尔本) | Australia/Sydney |
| 澳中(阿德莱德) | Australia/Adelaide |
| 澳西(珀斯) | Australia/Perth |
| 新西兰 | Pacific/Auckland |
| 南非(约翰内斯堡/开普敦) | Africa/Johannesburg |
| 埃及 | Africa/Cairo |
| 尼日利亚 | Africa/Lagos |

**默认策略**：地点或时区无法确定时停止起盘并澄清。不得用机器时区冒充提问地时区。
用户说“现在”时，必须在提问地 IANA 时区于用户提出问题时捕获当前墙上钟时间，
保留秒和可用的小数秒；禁止等到处理或排盘开始后另取整分钟。

---

## 4. 提问地 → (lat, lon) 高频城市

以下坐标只用于用户仅报城市名时的中心点近似。不能预先声称这种误差必然不影响
Lagna；必须在排盘后报告 Lagna 距 sign／Navamsa 边界的距离。

| 城市 | (lat, lon) |
|---|---|
| 北京 | (39.90, 116.41) |
| 上海 | (31.23, 121.47) |
| 广州 | (23.13, 113.26) |
| 深圳 | (22.54, 114.06) |
| 成都 | (30.67, 104.07) |
| 杭州 | (30.27, 120.15) |
| 南京 | (32.06, 118.80) |
| 武汉 | (30.60, 114.30) |
| 重庆 | (29.56, 106.55) |
| 西安 | (34.34, 108.94) |
| 香港 | (22.30, 114.17) |
| 台北 | (25.03, 121.57) |
| 东京 | (35.68, 139.65) |
| 大阪 | (34.69, 135.50) |
| 首尔 | (37.57, 126.98) |
| 新加坡 | (1.35, 103.82) |
| 曼谷 | (13.76, 100.50) |
| 吉隆坡 | (3.14, 101.69) |
| 雅加达 | (-6.21, 106.85) |
| 德里 | (28.61, 77.21) |
| 孟买 | (19.08, 72.88) |
| 迪拜 | (25.20, 55.27) |
| 伦敦 | (51.51, -0.13) |
| 巴黎 | (48.86, 2.35) |
| 柏林 | (52.52, 13.40) |
| 罗马 | (41.90, 12.50) |
| 莫斯科 | (55.75, 37.62) |
| 纽约 | (40.71, -74.01) |
| 洛杉矶 | (34.05, -118.24) |
| 旧金山 | (37.77, -122.42) |
| 芝加哥 | (41.88, -87.63) |
| 多伦多 | (43.65, -79.38) |
| 温哥华 | (49.28, -123.12) |
| 悉尼 | (-33.87, 151.21) |
| 墨尔本 | (-37.81, 144.96) |
| 奥克兰 | (-36.85, 174.76) |

**未收录城市**：优先取得实际城市或经纬度。使用最近城市近似时必须显式标记；
若本题实际使用的 Lagna、六分盘多数或 rising Navamsa 临界，停止确定性判读并要求更准确地点／时间。

---

## 5. 分类不明确时的兜底

若澄清后仍是 C级：

> "这个问法目前找不到有来源支持的事项宫或专题规则。我可以帮你把它改成一个
> 可观察的行动结果；如果你问的是性格、长期趋势或人生方向，应走本命盘入口。"

**不硬拗**——归不了类的问题直接告知用户走别的入口，比强行起盘给敷衍结论更负责。
