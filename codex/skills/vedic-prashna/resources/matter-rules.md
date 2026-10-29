# Prashna 事项登记：事项宫与本事古法

> **用途**：拆题之后（`question-decomposition.md`），"事情成不成"这个子问题查本表，取事项宫与本事古法，写进取象单的
> `matter`。本表与 `scripts/prashna_rules.py` 的 `MATTERS` 一一对应：**改一处必须同改另一处**。
>
> **权限**：本表只登记各类事自己的古法与执行要点。每个成败题都另加的三条通用规则（事项宫 `P-I.3`、`P-I.4`、
> `P-IV.1`）与连接（`M-XIV.43`）由判定脚本自动加，本表不重复列；同源不收的在"同源"列写明。
> 表外的问题不硬塞进最像的一行：取 `通用`，由模型按 `house-meanings.md` 的宫义与关键词选事项宫并写明出处（第 3 节）。
>
> **来源**：*Shatpanchasika*（Ayer 译注，`P`）各章正文与示范题；*Prasna Marga*（Raman 译注，`M`）第十七章；
> 挂靠依据是 Ayer 本人在各章示范题里给这种问法挂的偈，新增或调整挂靠须先核示范题。

---

## 1. 每题的默认角色

1. Lagna 与 Lagna 主：提问人与事情的当前状态；
2. 一个事项宫及其宫主（指标星）；
3. 本事古法明确使用的角色；
4. Moon 只在本事古法明确使用时作输入，否则只作背景（`moon-policy.md`）。

不固定加入 DK、AmK、PK、UL、AL 或其他 Chara Karaka；自然征象星只在本事古法明确使用时作辅证，不构成必须闭环的第二指标星。
一题需要两个完全不同的事项宫时，先拆成两个子问题，不把两宫堆进一个账本。

---

## 2. 登记表

"类比"＝原文是另一语境（议婚、王者和解），挂到现代问法，标 B；类比偈过语境检验（`judgment-rubric.md` §1.3）。

| matter | 问法 | 事项宫 | 本事古法（主；辅） | 支持级 | 同源不收 | 时间 |
|---|---|---:|---|---|---|---|
| 复合 | 能不能复合、和好、复婚 | 7 | `P-III.3~4`（类比） | B | — | general |
| 表白 | 喜欢的人能不能在一起；表白能不能成；能不能确立关系 | 7 | `P-I.4`；`M-XVII.5／15／16／17`（类比） | B | — | general |
| 恢复往来 | 断联后能不能恢复往来、关系能不能缓和 | 7 | `P-III.3~4`（类比） | B | — | general |
| 见面 | 能不能见面、约会，见不见得成 | 行动者的宫 | `P-I.4`；恋爱语境加 `M-XVII` 四偈（类比） | B | — | general |
| 挽回 | 我主动挽回能不能成 | 1 | `P-I.4` | A | — | general |
| 同住归来 | 已搬走的伴侣会不会回来同住 | 7 | `P-I.2` Nivritti 与归来 4 宫；`P-V.1~3`、`P-III.5`、`P-II.1~2` | A | — | return |
| 结婚 | 能不能结婚 | 7 | `P-VII.2`；`P-VII.1`、`M-XVII` 四偈 | A | — | general |
| 求职 | 能不能找到工作、拿到（满意的）offer、面试能不能过、能不能升职 | 10 | `P-IV.3`、`P-II.1`（星座类型）、`P-II.2`（照射） | A | — | general |
| 裁员 | 会不会被裁、调岗、换工作；能不能保住工作 | 1 | `P-I.2` Chyuti；`P-II.1` 动／固座 | A | 1 宫 `P-I.3`（Chyuti 读的就是 Lagna 的占据与照射） | general |
| 竞争考试 | 按排名录取：考研、考公、选拔 | 1 | `P-II.1~2`；`P-III.1` | B | — | general |
| 达标考试 | 过线即过：驾照、资格证 | 1 | `P-I.4` | A | — | general |
| 失物 | 失物、被盗物能不能找回 | 11 | `P-VI.3`；`P-V.1`、`P-II.1~2` 动／固座 | A | — | general |
| 走失宠物 | 走失的宠物能不能找回 | 11 | 同失物（Ayer 示范题"My cattle have strayed away"） | B | — | general |
| 买房 | 能不能买房、置产；住处问题能不能解决 | 4 | `P-I.2` Vriddhi；`P-II.1~2` 动／固座、`P-I.4`（第 4 偈示范题） | A | 4 宫 `P-I.3`（与 Vriddhi 读同一组占照） | general |
| 出行办成 | 出国、签证、留学、调动能不能办成 | 1 | `P-I.4`（第 4 偈示范题） | A | — | general |
| 路上顺不顺 | 路上顺不顺 | 1 | `P-II.5` | A | 1 宫 `P-I.3`（与 II.5 同读 Lagna 占据） | 不运行 |
| 离开 | 会不会离开、搬走；能否早日出发 | 10 | `P-I.2` Pravasa；`P-II.1~2` 动／固座；问"早日出发"加 `P-II.9` | A | 10 宫 `P-I.3`（反向同源：Pravasa 以凶星照为成行） | general |
| 归来 | 在外的人或失踪者会不会回来 | 7 | `P-V.1`；`P-V.2~3`、`P-III.5`、`P-I.2` Nivritti 与归来 4 宫、`P-II.1~2` 动／固座 | A | — | return |
| 疾病 | 病能不能好（含代他人问） | 1 | `P-IV.5`；`P-II.1~2` 动／固座 | A | — | general |
| 名誉 | 被诬陷、名誉能不能保住 | 4 | `P-I.2` Vriddhi；`P-II.1~2` 动／固座、`P-IV.3` 2／5／1 宫 | A | 4 宫 `P-I.3` | general |
| 谈判 | 谈判、和解能不能达成 | 7 | `P-III.3~4`（原文覆盖） | A | — | general |
| 投资 | 该不该投资某标的；会不会亏 | 11 | `P-IV.2`（Ch.4 示范题挂靠） | B | — | general |
| 亏损补回 | 生意亏损能不能补回 | 11 | `P-V.1`（Ch.5 示范题挂靠） | B | — | general |
| 开庭 | 官司会不会很快开庭 | 4 | `P-II.11`（Ch.2 示范题挂靠） | B | — | general |
| 合作 | 合作、另一方会否配合 | 7 | `B-article-99` 1／7 双方（实例，不计分） | B | — | general |
| 财富 | 财富能不能取得 | 2 或 11（按问题动词，取象单给） | — | B | — | general |
| 子女行动 | 子女相关的一个具体行动 | 5 | — | B | — | general |
| 通用 | 表外问题 | 模型按宫义选（第 3 节） | — | B | — | general |
| 描述 | 描述型：相处得怎样、氛围、局面（如某职位竞争激不激烈） | 模型按宫义选 | —（只出事实：指标星能力与连接、影响者逐颗、关键词落点、`M-XIV.117`；不建账、不定档，`judgment-rubric.md` §15） | B | — | 不运行 |

取象单另需：结婚题 `asker`（男／女，`P-VII.1` 问娶看新娘、问嫁看新郎）；裁员题 `direction`（会不会被裁＝发生；能不能保住＝避免，
方向相反）；离开题问"能否早日出发"时 `early_departure`；见面题 `context`（"恋爱"时加四偈）与 `matter_house`（行动者的宫）。

---

## 3. 表外问题（`通用`）

先按 `question-decomposition.md` 拆题。"事情成不成"那个子问题落在哪一宫，按 `house-meanings.md` 第 2 节宫义与第 6 节关键词库选，
在取象单的 `keywords` 里写明"关键词 → 宫 → 出处"，`matter` 取 `通用`、`matter_house` 填所选宫。这是 B 级通用古典规则判读。

只有拆题后连一个有出处的宫义都对不上，才停在不判（第 6 节）；按宫义选宫并写明出处，不算"找最像的宫硬套"。

常见的去处：继承、遗产 → `通用`，事项宫 8（亡者之财，BPHS 11.9；`P-IV.4` 原文未逐偈审，不收）；选举 → `竞争考试`（`P-III.1` Ayer 注含
"elections"，4.2）；某职位竞争激不激烈 → `描述`（6 宫争斗、敌）；天气 → 第 5 节，非雨季不判（第 6 节）。

---

## 4. 执行要点

### 4.1 关系类

- `P-III.3~4` 原文是王者之间的和解；Ayer 注"can be used in all cases where settlement of scores is involved"。复合、恢复往来是类比，标 B；
  谈判、和解原文覆盖（注"… negotiations"），标 A。
- 人形星座：`P-III.3~4` 取 Gemini、Virgo、Libra、Aquarius（III.3 Ayer 注）；`P-IV.2` 按本偈正文只取 Libra、Gemini、Aquarius。各用各的清单。
- III.3 的"凶星落变动座则冲突"属和解规则本身，要用；`P-I.2`、`P-II.1~2` 的动／固座讲位置得失，不进复合主判。
- III.4 吉凶星混落角宫或人形 Lagna：注"will tend to continue the tension without resolving it, a preponderance of benefic influence leading to
  prospective resolution"，按 `judgment-rubric.md` §3 偈内占优数，吉占优记趋向和解（困难后成）。
- 结婚：`P-VII.2` (a) Moon 落 3／5／7／11／6 宫且受吉星照，或 (b) 吉星落角宫、三方宫，则议婚能成；注：点名的是自然吉星，实指功能吉星，
  其余配置为否。(a) 看 Moon 所在宫行"七曜照射本宫"有吉标签即满足（原文点名三星，注只说改按功能取，未说须几颗，执行口径）；
  (b) 看 1／4／7／10／5／9 宫"七曜占据"。"Sun"不是自然吉星，疑为 Venus 误印，无梵文可核，照录。`P-VII.1`：Saturn 落 Lagna 起奇数宫
  （不计 Lagna）兼示得新娘，否则得新郎；注列三问次序与正文不一致，按正文。另加 *Prasna Marga* 第十七章四偈。
- 表白、确立关系：没有专属偈，按一般所谋之事走 `P-I.4`，按 *Prasna Marga* 第十七章婚姻卜问类比加四偈，标 B。原文议婚语境 Lagna 读女方、
  7 宫读男方（`M-XVII.8–9`）；这里沿用 Lagna＝提问人、7 宫＝对方。
- 见面、约会：答"见不见得成"。没有专属偈，按一般所谋之事走 `P-I.4`，事项宫取行动者的宫（`house-meanings.md` 第 5 节：对方 7、上级 10、
  母亲 4……）；恋爱语境加四偈。Ch.2 到达诸偈（敌军来不来，`P-II.6~8`、`P-II.11`、`P-II.13`，*Prasna Marga* XXIV.68 注明可用于人会不会来）
  尚未逐偈审定，不进账本；将来收入也须先定它答哪个子问题，不与行动链在同一子问题上各出结论。
- 恢复往来、关系缓和：没有示范题；断联、冷战后恢复联系是双方关系的缓和，按 III.3 注类比收 `P-III.3~4`（10-21 创始人定）。
- "他会不会主动约、联系、表白、来"都是行动子问题，读行动链，本表各行只答结果（`question-decomposition.md` 第 2 节）。

### 4.2 求职、考试

- `P-IV.3`：吉星落 10、7 宫赐位置；凶星落 12、11 宫不吉。原文"(Malefic) Moon in lagna will not give favourable results, while in the tenth (even
  when malefic) it will"：Moon 落 Lagna 只在亏月记不利；落 10 宫不论盈亏都有利。
- `P-II.1~2`：固定座上升主得位，动座相反（注"he will not get the position"）；变动座混合，Ayer 注引 Bhattotpala *Prasnagyana*：上升点在前半按
  固定座读，后半按动座读。吉星照 Lagna 与 Moon-lagna 吉，凶星照则凶，吉凶同照为混合。Ayer 在 II.1 注里把"landing a job"列为得位的一种。
  账本记两条：星座类型一条（II.1，含 II.2 首句），照射一条（II.2 后句）；Ayer 注只说合起来列表，没说捆成一条。
- 问"满意的 offer"：账本同上；`P-IV.3` 后半句"吉星落 2、5、1 宫得名与财"用来讲待遇和满意度，不计分。
- 裁员、调岗、换工作走 `P-I.2` Chyuti（Ch.1 示范题"Is a change of job imminent? Will I lose my job? Will I be transferred?"）：Lagna 动座且受本宫主或
  吉星占据／照射、没有凶星占照，则变动成立；固定座即使无凶星也不变；变动座看吉凶影响孰多（§3 偈内占优）。辅助只用 `P-II.1` 动／固座；
  `P-II.2`"吉星照 Lagna 吉"在 Chyuti 里反而促成变动，不用。
- 竞争性考试：Ch.2 示范题"Will I succeed in the competitive examination?"挂 `P-II.1~2`；`P-III.1` 原文是战事胜负，Ayer 注扩到"elections and
  such other competitive efforts"，作辅助。示范题只挂靠、正文未覆盖，标 B。`P-III.1` 注"mention of planets by name is only symbolic; their functional
  character should be taken"，9 宫按宫表标签读。`P-II.8`、`P-II.10` 示范题也挂考试，但正文是敌军动向，已知未收。
- 多环节考试只问最近一个还没出结果的环节。面试卡点按账本条目讲成条件，不评判人，不从盘里读性格、口才。

### 4.3 其他

- 失物：`P-VI.3` 是能否找回的主规则：满月或吉星占 Lagna、头升座上升受吉星照、强吉星落 11 宫则速得；Bhattotpala：皆无则渺茫（"chances of recovery
  are remote"）。头升座 Ayer 注列 Leo、Virgo、Libra、Scorpio、Aquarius，没有 Gemini；Lagna 为 Gemini 时两说。`P-V.1` 吉星落 5／2／3 宫则失物复得。
  强吉星按 D1 `exalted`／`own_sign`／`moolatrikona`。`P-II.1~2` 注：固定座"hidden from view, possibly misplaced inadvertently"（未丢、一时找不到），动座"object lost is
  irrecoverable"。`P-I.5`（满月落 Lagna 受 Jupiter 或 Venus 照，或强吉星落 11 宫则速得）只答快不快、不计分：原文只说"quickly recovered"，不满足推不出
  找不回；满月取注的满月窗（白半月第 10 至黑半月第 5 tithi）。
- `P-I.2` 四问方向各不相同，不能互相套用：Vriddhi 是 4 宫受本宫主或吉星占照、且"unspoiled by other planetary dispositions"则兴（4 宫同时有凶标签
  占照记混合，执行口径）；Pravasa 是 10 宫动座且受凶星照才成行，受本宫主或吉星照反而不成；Nivritti 是 7 宫动座且受本宫主或吉星照则返回，
  受凶星照则否；Chyuti 见 4.2。
- 买房：Vriddhi 定结果；`P-II.1~2` 注：固定座得住处（"acquisition of a dwelling place"），动座"he will not get the position or home desired"；另收
  `P-I.4`（第 4 偈示范题"I want to buy a property; will I succeed?"）。
- 出行按问法分三行（Ayer 示范题分挂三处，执行口径）：能不能办成走 `P-I.4`（第 4 偈"I am thinking of going abroad; will I succeed?"）；会不会离开走
  Pravasa（第 2 偈"Will my contemplated journey materialise?""Can I leave this city for good?"，原文"only when"，满足的盘很少，照实说）；路上顺不顺走
  `P-II.5`（Ch.2 示范题"bon voyage or meet with trouble on the way?"：动座上升有吉星占据利行人，凶星占据害；固定座上升有凶星占据行人亦平安；
  都不满足不出方向）。现代人问"能不能出国"多半是问办不办得成，先按此澄清。
- 能否早日出发：`P-II.9` 按点名——动座上升且 Sun／Saturn／Mercury／Venus 之一占据则很快出发，该星逆行则否。Ayer 注称日月无逆行、"should be kept
  out of reckoning in this context"：Sun 只免逆行判断、还是整体不计入，两说。`P-II.1~2` 注：固定座"neither departure nor arrival"。
- 归来：`P-V.1` 行星落 5／2／3 宫则返回；`P-V.2` 7 或 6 宫有星、Jupiter 落角宫或 Mercury／Venus 落三方宫（且／或两说）；`P-V.3` Moon 落 8 宫且角宫无
  凶星则平安返回（注：Moon 与角宫吉星都不可弱，D1 `debilitated` 算弱）；`P-III.5` Jupiter 或 Venus 落 2／3 宫则很快到来。点名行星的按点名读。
  归来 4 宫两说：正文"One returns from abroad, with a planet's occupation of the fourth house"；注"the person from abroad has come home when the fourth house
  contains its own lord or is aspected by it and not otherwise"。`P-II.1~2` 注：固定座不来；动座注"he has not arrived; he is moving"，在途、尚未到达，
  记有利（执行口径）；失踪者固定座注"not gone abroad or far away, nor dead"只取"没走远"。失踪者寻得快慢另看 `P-I.5`，不计分。方向距离走查表
  （第 5 节 `P-VI.4`）；"是否平安、是否还活着"不判。
- 疾病：`P-IV.5` 吉星落 Lagna／7／8／5 宫且彼此相照、Moon 落 3／6／10／11 宫则康复；Bhattotpala 只补"落这些宫的吉星（Moon 除外）须彼此相照"。Ayer 注：
  凶星落这些宫且 Moon 落别处则相反；配置不全时看有利影响是否占优（§3，吉占优记终可康复）。"彼此相照"按"七曜互视"判：同宫不算互照，只有一颗
  吉星不算满足。`P-II.1~2` 注：固定座"cure is doubtful"，动座"chances of recovery are good"，与求职方向相反。代他人问同样读 1 宫（Ch.4 示范题"My
  brother is seriously ill; will he recover completely?"）。只答能否康复，不作医疗诊断，不替代就医。
- 名誉：依据 `P-I.2` 注的诽谤例——先看 Vriddhi 定结果；`P-II.1~2` 注：固定座"honour and reputation … fixed signs rising ensure safety"，动座"humiliation
  is certain"；`P-IV.3` 吉星落 2／5／1 宫得名利，作辅助。注例"再看 Nivritti（7 宫）定对方能否得逞"：原文未写对方得逞对提问人记有利还是不利，
  **只进叙述、不计分**，待对原文。
- 投资：`P-IV.2` 吉星落 3／5／11／7 宫得益、凶星则损，照射等同占据（注）；吉星落人形座亦吉。Ch.4 示范题"Should I invest in this particular scrip or
  will it ruin me?"只挂靠，标 B；不判具体价格。
- 亏损补回：`P-V.1` 吉星落 5／2／3 宫则失物复得；Ch.5 示范题"I have incurred a loss in my business; can I expect to make it good soon?"，标 B。
- 开庭：`P-II.11` Sun 与 Moon 落 4 宫则不来，Mercury、Jupiter 与 Venus 落 4 宫则很快来，按点名、按字面同落；两组都不满足本条不出方向。
  "官司能不能赢"不在此行。
- 合作：`B-article-99` 只证明"1 宫代表一方、7 宫代表另一方"的用法，不计分；不自动加入 Mercury、DK。
- 财富：2 宫（财）或 11 宫（收益），按问题动词二选一；不自动加入 Jupiter、SAV。
- 子女相关行动：5 宫；不自动加入 PK、Jupiter。

---

## 5. 查表题（不建账本、不出三档、不跑时间副层）

只给 `structured_prashna.md`"描述题与天气查表事实"的查表结果，原文歧义两说并列（`standard-layer.md` §5.1）。

| 问法 | 规则 | 查表依据 |
|---|---|---|
| 是不是家里人拿的；还在屋里吗 | `P-VI.1` | 固定座、固定 Navamsa 或 vargottama 上升：亲属所拿、藏在屋内；Bhattotpala：否则外人拿走 |
| 藏在屋里哪个部位 | `P-VI.2` | Lagna 所在 drekkana：门槛／中间部分／后院；只在 VI.1 读作"屋内"时用 |
| 往哪个方向、多远（失物、失踪者） | `P-VI.4` | 角宫行星定方向，无则 Lagna 星座；距离按 rising Navamsa 序号，只报相对远近 |
| 丢的是什么类东西 | `P-I.7`；`P-VII.13` | rising Navamsa 序号定 Dhatu／Moola／Jeeva；大小 |
| 何时丢的、去向、放在什么地方、拿的人多大 | `P-VII.13` | 星座定时段、方向、藏放处；Lagna 主定年龄 |
| 雨季今天或近期会不会下雨 | `P-VII.3~4` | VII.3：Venus 与 Saturn 落 Moon 起 7 宫（注：Venus 不可能落 Sun 起 7 宫）或 Lagna 起 2／3／4／8 宫；VII.4：白半月吉星落水象座的 3、2 宫或角宫，或 Moon 落水象 Lagna |
| 胎儿是男是女（已怀孕） | `P-VII.1` | Saturn 落 Lagna 起奇数宫为男，否则为女（按 Varahamihira，Lagna 不计入）；不作医学判断 |
| 亲属是否在外地（父亲、母亲、手足、子女、妻子、仆从） | `P-VII.12`；人与 karaka 依 `M-XIV.31` | 该 karaka（Sun 父亲、Moon 母亲、Mars 手足、Jupiter 子女、Venus 妻子、Saturn 仆从）带吉星落 8 宫且受吉星照则在外，否则在本地；吉星按 8 宫星座的吉凶标签；父亲 A 级，其余 B 级 |

执行要点：
- `P-VI.4` 恰有一颗角宫行星时，正文"by the planets occupying kendras"与注"Two or more planets"读法不一，两说。距离单位原文是 yojana，注称按现代条件另定
  尺度，只报相对读数。
- `P-I.7` 注中 Mesha 举例（第二 Navamsa 为 Jeeva）与注表（2／5／8 为 Moola）矛盾，以译文和注表为准。
- `P-VII.13` 不收：颜色与窃贼外貌（注指向 Brihad Jataka／Saravali，本地无原文）；种姓；"Relation by karaka"、Navamsa 强弱、"concerned planet"落陷燃烧
  （原文未给判据或未指明是哪颗星）。
- 天气：雨季与否由用户提供，不从盘里推；原文只写有雨条件，条件不满足写"原文无反面判据"，不判"不下雨"。水象座两说：Horasara 取 Cancer、Capricorn、
  Scorpio、Pisces；Mantreswara 取 Cancer、Capricorn 后半、Pisces。`P-VII.3` 只有一颗星满足时，正文"Venus and Saturn"是否要求两星同时满足未明，两读并列。
  `P-VII.4`(a) 的吉星读宫表标签。
- 父亲以外的亲属：`P-VII.12` 注"other karakas too can be handled in an identical manner"，人与 karaka 取 `M-XIV.31`（B 级）；XIV.31 没列的人
  （丈夫、朋友、同事）不收。问"会不会回来"走登记表 `归来`。
- 同时问"能不能找回"时，成败部分另走失物行，两部分分开写。

---

## 6. 不判

用一句话说明不判，必要时给替代问法或建议联系当事人、相关机构；不说教。

- 生死、寿命、"还活着吗"、在外者是否平安（`P-V.4`、`P-VII.11`；Ch.2、Ch.5 示范题有此类问法）；
- 读心与隐私：所想之物（`P-I.6`）、所问何人（`P-VII.6~9`）、他人私生活（`P-VII.10`）、对方心理、对方还爱不爱我、对方和现任会不会分手、
  第三方是什么性格（改问"我们相处会怎样"，走 `描述`）；
- 操控、打听：打听对方行踪、新伴侣信息或隐私；"怎么让他回来""怎么让他离开现任"。说明这类问题要的是控制或窥探另一个人，卜卦不做，
  替代问法如"我主动挽回能不能成"；
- 同一张盘比较 A／B 两个互斥选项（先让用户选一个最想执行的方案，改问"执行 A 能否达到某结果"）；
- 面试表现如何、面试官怎么看我（改问"能不能拿到这个 offer"）；
- 非雨季的天气（晴不晴、冷不冷、雨季以外会不会下雨）：宫义里没有天气，拆题投不上，原文只有雨季的有雨条件（第 5 节）；背后若是一件人事，
  改问那件事（出门办事 → "路上顺不顺"或"这件事办不办得成"；怕下雨误了婚礼 → "婚礼能不能顺利办成"）；
- 拆题后连一个有出处的宫义都对不上的对象（第 3 节）。

---

## 7. 已知未收

`P-II.8`、`P-II.10`（敌军动向，示范题挂考试，原文未写如何对应考试成败）；`P-IV.4`（继承，好处来自女性；继承题走第 3 节 `通用`）；`M-XIV.31` 未列之人（丈夫、朋友、同事）的下落；`P-VII.5`（Lagna 落阳性 varga 定胎儿
性别，创始人 2026-10-10 定不收）；Ch.2 到达诸偈（见 4.1）；`P-I.6`、`P-VII.6~11`（读心、隐私、生死）。
