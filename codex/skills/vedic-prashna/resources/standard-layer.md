# Prashna 标准层：来源、准入与数据契约

> **用途**：约束默认主层。任何成败规则先在本文件取得来源标签、适用范围和
> 准入状态，才能进入 `SKILL.md`、判定 rubric 或代码。
>
> **标准层名称**：以 *Shatpanchasika* 为主文本、经 KN Rao／Bharatiya Vidya
> Bhavan 实践兼容性筛选的古典 Prashna，并有条件收入同一系、直接引用
> *Shatpanchasika* 的 *Prasna Marga*（合判权衡、婚姻卜问，见 §1）。不得简称为
> “KN Rao 自创 Prashna 体系”，也不得把 KN Rao 的本命盘工具自动迁入提问盘。

---

## 1. 来源标签与准入规则

| 标签 | 含义 | 主层权限 |
|---|---|---|
| `K` | KN Rao 本人直接表述或本人署名案例 | 可进入，但不得扩大原文适用范围 |
| `P` | *Shatpanchasika* 原文／可定位译文 | 可进入；专题规则只用于对应题型 |
| `B` | Bhavan／Journal of Astrology 实例 | 可作兼容性与用法证据，不冒充 KN Rao 原话 |
| `M` | *Prasna Marga*／Kerala 系（Raman 译注） | 有条件进入：逐偈核过原文并记 `M-章.偈`；只用 §4 白名单数据；专题条只用于对应题型；不收寿命、死亡、贞洁、子女夭折、相貌等 C 级内容。征兆、触碰部位、Arudha、Gulika、Thrisphuta、Yama Sukra、仪式补救不收。宫义、星义（XIV.3–14、20–22、31–37、44–48）不单独计分，用于取象、按需读、行动链与叙述（`house-meanings.md`）。时间模块见 `timing-layer.md` |
| `T` | Tajika | 仅 Tajika 沙箱 |
| `KP` | Krishnamurti Paddhati | 仅 KP 独立栈 |
| `E` | 工程／产品规则 | 可作输入、隔离和置信度门控，不冒充古典教义 |
| `U` | 未核证或只有泛化推断 | 禁止进入默认成败和择时 |

主层规则必须满足：

1. 至少有一个 `K`、`P`、`B` 或已准入的 `M` 来源；
2. 记录原始适用题型，禁止把专题规则泛化成全局规则；
3. 与更高优先级来源冲突时保留冲突，不静默调和；
4. `B` 单案例只能证明“该案例这样使用”，不能独立建立全局硬门；
5. `E` 只能管理工作流与不确定性，不能制造占星结论；
6. `U` 数据即使共享 engine 已计算，也不得出现在标准层评分契约。

---

## 2. 核证矩阵

| 规则 | 来源 | 范围 | 准入 |
|---|---|---|---|
| 以具体问题产生时刻和地点起盘 | `P/K/B` | 全部 | 核心 |
| Lagna／Lagna 主表示求问者和事情的当前状态 | `P-I.2~4/B` | 全部 | 核心 |
| 事项宫被其宫主或吉星占据／照射则增强，受凶星伤害则减损 | `P-I.3` | 全部宫位 | 核心；吉凶按 §2.1 |
| 一般所谋之事可检查 Lagna、Lagna 所落 varga、头升／背升及吉凶扶压 | `P-I.4` | 一般事业成败 | 条件适用 |
| “falls in a benefic's varga” 的 varga 指六分盘：Lagna、Hora、Drekkana、Navamsa、Dwadasamsa、Trimsamsa（注）；六个座主按 §2.1 功能吉凶计数，吉多算落吉 varga，凶多算反之，相等不计。数法出处：*Prasna Marga* 两偈用同类条件“has a number of benefic vargas”（`M-VIII.29` 说 Lagna，`M-XXIV.45` 说 ascendant，都与“吉星占 Lagna”并列），`M-VIII.29` 注“whether the Lagna has more benefic vargas or malefic ones”；`M-XVIII.148` 注按座主逐个数 varga。Hora 取传统 Sun／Moon Hora（`M-XVIII.148` 注 Virgo 30° 算例为证） | `P-I.4` 注；数法 `M-VIII.29` 注、`M-XXIV.45`、`M-XVIII.148` 注 | 一般事业成败 | 采纳（执行口径）；VIII.29 注称该偈 Lagna 指 Arudha，Arudha 不收，只借其数法；PM 注的七分盘多 Saptamsa，按 Ayer 注取六；数据见 §4 第 2 项 |
| 混合配置表示困难后成：(1)(2) 一合一不合、吉凶星同占头升 Lagna、Pisces 上升；由吉的影响是否占优定局（“preponderance of benefic influence will decide the issue”），不能由单一弱点判死 | `P-I.4` 及注 | 一般事业成败 | 核心；占优数法见 `judgment-rubric.md` §3 |
| Lagna、Sun、Moon 动／静星座“snapshot” | `K` | KN Rao 的有限快照法 | 只作有限辅证；本人明说并非总有效 |
| 1宫代表一方、7宫代表另一方 | `B-article-99` | 双方／谈判案例 | B级题型可用 |
| 用 Lagna、Lagna 主、Moon 及月宿核对盘是否反映问题 | `B-article-153` | 失踪者单案例 | 只作软验证候选 |
| Moon 为所有题型最高权重 | `U` | — | 禁入 |
| Moon 无同宫／Graha Drishti 即“空亡”或“不成” | 无支持 | — | 禁入 |
| Moon 月宿主是所有题型固定 significator | `B` 单案例 | — | 禁作全局硬门 |
| Chandra Kriya 是 60 种 lunar actions | `M-VIII.63~65` | Kerala 模块 | 仅纠错边界 |
| Moon ingress 等于 Dasha 切换 | `U` | — | 禁入 |
| Moon 下次进入事项宫主所在星座作为触发日 | `M-XIV.85` | 时间副层 | 只在 `timing-layer.md`，不进规则账本 |
| Chara Karaka、DK、UL、AL 用于默认 Prashna | `U` | — | 禁入 |
| SAV／BAV 用于默认 Prashna | `U` | — | 禁入 |
| 分盘只读取 Lagna 六分盘座主与 rising Navamsa；完整 D2／D3／D9／D12／D30 人生解读 | `P-I.4`、`P-I.7`、`P-VI.1~2`、`P-VI.4`、`P-VII.13`／`U` | 一般所谋之事、描述题／其余 | 只保留这两项 |
| D10／D4／D5 等本命分盘 | `U` | — | 禁入 |
| 提问盘生成的 120 年 Vimshottari／Chara Dasha | 与 `K/M` 边界冲突 | — | 禁入 |
| *Prasna Marga* 一年／一月 Prasna Dasa | `M-VI.39,65~67` | Kerala | 不收：答的是未来一年哪段顺逆，不是事件日期；需 Thrisphuta、Gulika；VI.67 三套 Dasa 由占星师择一，无确定选法 |
| 宫数／Navamsa 数换算应事时间 | `M-XIV.81~82,85`、`P-V.5` | 时间副层 | 只在 `timing-layer.md`；不改三档 |
| 固定座上升得位（Sthana labha），动座相反，变动座混合（注引 Bhattotpala *Prasnagyana*：上升点在变动座前半按固定座读，后半按动座读）；吉星照 Lagna 与 Moon-lagna 吉，凶星照则凶，吉凶同照为混合 | `P-II.1~2` 及注 | 位置得失；Ayer 注扩展到求职、住处、出行、失物、失踪者、疾病、名誉 | 求职、竞争性考试的主规则（见 `matter-rules.md` §4.2）；其余题型只取动／固座作辅助规则（`matter-rules.md` 登记表）；变动座前后半归属按所给时刻定，近 15° 时误差只记输入提示（`judgment-rubric.md` §13） |
| 吉星落 10／7 宫赐位置（position），落 2／5／1 宫得名利（fame and wealth）；凶星落 12／11 宫不吉；(Malefic) Moon 在 Lagna 不利，在 10 宫“even when malefic”有利 | `P-IV.3` | 位置；名利 | 求职题主规则；Lagna 条款只在亏月成立，10 宫条款不论盈亏；2／5／1 宫条款作名誉题辅助规则，求职题用来讲待遇与满意度（不计分） |
| 吉星落 10／1／7 宫则胜；Mars／Saturn 落 9 宫败，Mercury／Jupiter／Venus 落 9 宫胜 | `P-III.1` | 战事胜负；Ayer 注扩展到选举等 competitive efforts | 竞争性考试辅助规则，B级（主规则 `P-II.1~2`） |
| 人形星座（III.3 注：Gemini、Virgo、Libra、Aquarius）上升且有吉星、吉星落 12／11 宫、吉星落 kendra 或人形 Lagna 受吉星照则和解；凶星落变动座则冲突，凶星同样落位受凶星照则相反；吉凶混落则僵持，吉占优趋向解决（III.4 注） | `P-III.3~4` 及注 | 王者和解；Ayer 注扩展到 settlement of scores／negotiations | 谈判／和解A级；复合、恢复联系类比B级（见 `matter-rules.md` §4.1） |
| 吉凶按功能取：F1 本宫主对本宫恒吉；F2 同管本宫起 3、12 宫且落陷为凶；F3 同管本宫起角宫与三方宫且强（exalted／own_sign／moolatrikona）为吉；其余回落 Bhattotpala 自然吉凶 | `P-I.3` 注 Rule 1/2 及两例；Bhattotpala 见同注 | 全部 `P` 规则中的“吉星／凶星” | 采纳；正文点名行星且 Ayer 无注的偈按点名，不换标签（见 §2.1） |
| D1 尊贵度、受克和燃烧事实 | `P-I.3` 及注释 | 行星承事能力；F2／F3 的落陷与强 | 次级，不单项定档 |
| Chyuti 看 Lagna：动座且受本宫主或吉星占据／照射、无凶星则变动成立，固定座不变，变动座看吉凶多寡；Vriddhi 看 4 宫：受本宫主或吉星占据／照射且未受其他配置破坏（“unspoiled by other planetary dispositions”）则兴；Pravasa 看 10 宫：动座且受凶星照则成行，受本宫主或吉星照则否；Nivritti 看 7 宫：动座且受本宫主或吉星照则返回，受凶星照则否；在外者返回另看 4 宫，正文“with a planet's occupation of the fourth house”，注“contains its own lord or is aspected by it and not otherwise”，两说并列 | `P-I.2` 及注 | 换工作／裁员／调岗、房屋、出行、返回；注例扩展到诽谤 | 对应题型主规则，A级 |
| 满月（白半月第 10 至黑半月第 5 tithi）落 Lagna 受 Jupiter／Venus 照，或强吉星落 11 宫，失物速得 | `P-I.5` 及注 | 失物、走失者 | 只答找回快不快，不计分（原文只说“quickly recovered”，不满足推不出找不回）；能否找回走 `P-VI.3` |
| rising Navamsa 序号按奇偶座定 Dhatu／Moola／Jeeva | `P-I.7` 及注表 | 描述物品属性 | 描述题查表，不进三档 |
| 吉星落角宫、三方宫且凶星不落角宫和 8 宫则全面兴旺；配置相反（凶星落角宫和 8 宫、吉星落别处）则结果相反 | `P-IV.1` 及注 | 一般前景 | **通用环境规则**：Ayer 目录称"omnibus solution"，示范题"我现在前景如何？能不能开新事业？"；按 `judgment-rubric.md` §1 收入每个成败题的成事账（主、辅规则已含时不重复） |
| 吉星落 3／5／11／7 宫得益，凶星则损；吉星落人形座（本偈正文：Libra、Gemini、Aquarius）亦吉；照射等同占据 | `P-IV.2` 及注 | 示范题：投资 | 投资题，B级 |
| Moon 落 2／7／10／11／6／3 受 Jupiter 照，好处来自女性 | `P-IV.4` | 示范题：继承 | 本批不收 |
| 吉星落 Lagna／7／8／5 宫且彼此相照，Moon 落 3／6／10／11 宫，则病愈；凶星落这些宫且 Moon 落别处则相反；配置不全时看有利影响是否占优（注） | `P-IV.5` 及注 | 疾病康复 | 疾病题主规则，A级；“彼此相照”是 Bhattotpala 补充，“相反”“占优”是 Ayer 注 |
| 行星落 5／2／3 宫则离者返回；吉星落此则失物复得；Jupiter／Venus 落此则速 | `P-V.1` | 失踪者返回、失物；示范题含亏损补回 | 返回题 A级；失物题辅助规则；亏损补回 B级 |
| 7 或 6 宫有星、Jupiter 落角宫或 Mercury／Venus 落三方宫，离者返回；Moon 落 8 宫且角宫无凶星则平安返回，角宫有吉星则带利返回；注：Moon 与这些吉星都不可弱（“should not be weak”） | `P-V.2~3` 及注 | 远方之人返回 | 返回题辅助规则；“弱”按 D1 `debilitated` 算 |
| Jupiter 或 Venus 落 Lagna 起 2／3 宫，远方之人很快到来 | `P-III.5` 及注 | 示范题：儿子能否从海外返回 | 返回题辅助规则，按点名行星 |
| 动座上升且 Sun／Saturn／Mercury／Venus 之一占据则很快出发；该星逆行则否 | `P-II.9` 及注 | 示范题：早日出国 | 出行“会不会离开”问“能否早日出发”时的辅助规则，按点名行星 |
| Sun 与 Moon 落 4 宫则不来；Mercury、Jupiter 与 Venus 落 4 宫则很快来 | `P-II.11` 及注 | 示范题：官司会否很快开庭 | 开庭题，B级，按点名行星；两处原文都是“and”，按字面读作同落（三星同落 4 宫少见），不满足时本条不出方向 |
| 固定座／固定 Navamsa／vargottama 上升则亲属所盗、藏于屋内；Lagna 所在 drekkana 定藏处 | `P-VI.1~2` 及注 | 失物描述 | 描述题查表，不进三档 |
| 满月或吉星占 Lagna、头升座上升受吉星照、或强吉星落 11 宫则速得；皆无则渺茫 | `P-VI.3` 及注 | 失物能否找回（Bhattotpala 注：皆无则“chances of recovery are remote”） | 失物题主规则；Gemini 是否头升两说并列 |
| 角宫行星定方向，无则 Lagna 定方向；距离按 Navamsa 序号 | `P-VI.4` 及注 | 失物、失踪者方向距离 | 描述题查表；单星时正文与注两读并列 |
| Saturn 落 Lagna 起奇数宫（不计 Lagna）为男，否则为女；同偈：前者兼示得新娘，后者兼示得新郎 | `P-VII.1` 及注 | 胎儿性别；婚姻 | 胎儿性别 A级；婚姻题辅助规则（注：本偈也回答“eligible groom／bride”），按正文次序（注列三问的次序为胎儿、新郎、新娘，与正文不一致） |
| Moon 落 3／5／7／11／6 宫且受 Jupiter、Sun、Mercury 照，或吉星落角宫／三方宫，则议婚能成；注：点名的是自然吉星，实指功能吉星，其余配置为否 | `P-VII.2` 及注 | 能否成婚 | 婚姻题主规则，A级；走标签（§2.1）；“Sun”不是自然吉星，疑为 Venus 误印，无梵文无法核实，照录 |
| 雨季 Venus 与 Saturn 落 Moon 起 7 宫或 Lagna 起 2／3／4／8 宫；白半月吉星落水象座的 3／2／角宫，或 Moon 落水象 Lagna，则有雨 | `P-VII.3~4` 及注 | 雨季天气 | 天气查表；原文无反面判据，不判“不下雨”；水象座两说并列 |
| Lagna 落阳性 varga 受强阳性星照为男等 | `P-VII.5` 及注 | 胎儿性别 | 不收（创始人 2026-10-10 定）；六分盘座主表只供 `P-I.4` |
| Sun 带吉星落 8 宫受吉星照则父亲在外，否则在本地 | `P-VII.12` 及注 | 父亲下落；注称其他 karaka 同理，人与 karaka 取 `M-XIV.31` | 父亲 A级；其他亲属 B级 |
| Navamsa 定物、drekkana 定贼、星座定时间方向位置、Lagna 主定年龄 | `P-VII.13` 及注 | 失物描述 | 描述题查表；种姓、颜色、窃贼外貌、Navamsa 强弱不收 |
| I.6、VII.6~9 读所想之物／所问之人；VII.10 私生活；VII.11、V.4 生死安危 | `P` | 读心、隐私、生死 | 不收（C级） |
| II.8、II.10 敌军动向 | `P` | 示范题挂考试 | 已知未收：原文未写敌军来去如何对应考试成败 |
| 逆行统一等于失败 | `U` | — | 禁入；只在专题规则明示时使用 |
| 3／6／8／12 一律作为同级阻碍宫 | 与 `P` 题目语义冲突 | — | 禁入 |
| Lagna 主必须连接事项宫主 | 仅部分 `B/P` 专题 | — | 禁作全局硬门；连接按 `M-XIV.43` 连上记一条有利，没连上不记不利（`judgment-rubric.md` §1） |
| 事项宫主必须与自然 Karaka 闭环 | `U` | — | 禁入 |
| 内部三档“偏成／持平／偏不成”，账本按占优合判 | Ayer I.4／III.4／IV.5 注、`M-XIV.98`、`M-XVII` 注 + `E` 输出契约 | 全部 | 三档只写判读单核对区；给用户看的部分讲事情怎么走，不出现档名（`judgment-rubric.md` §2） |
| 24小时／3个月重复起盘阈值 | `U/E` | — | 删除数字阈值 |
| 时间地点误差下本题账本会不会变 | `E` | 全部 | 输入提示：只记核对区，不改档，不进给用户看的部分（`judgment-rubric.md` §13；创始人 2026-10-29 定） |
| 吉凶混合时按占优断：“If the influences are mixed, then prediction must be made according to the predominating factor”；Raman 判婚事例盘按多数（XVII.19 注“the majority of factors”）、按正负条数（XVII.32 注“minus points”） | `M-XIV.98`；`M-XVII` 注 | 全部题型的账本合判 | 采纳为合判原则；数法是执行口径（`judgment-rubric.md` §2.2） |
| Ayer 第 4 偈示范题挂“I am thinking of going abroad; will I succeed?”“I want to buy a property; will I succeed?” | `P-I.4` 示范题 | 出国、签证、留学、调动能否办成；买房 | 出行“能否办成”主规则；买房辅助规则 |
| 动座上升有吉星占据利行人，凶星占据则害；固定座上升有凶星占据，行人亦平安 | `P-II.5` 及注 | 示范题：路上顺不顺 | 出行“路上顺不顺”主规则；条件都不满足时本条不出方向 |
| 7 宫有吉星为好 | `M-XVII.5` | 婚姻；表白／确立关系类比 | 婚恋题辅助规则 |
| 受克的 Moon 落 Lagna 起偶数宫且亏月提问则不成；Moon 落 8 宫有阻 | `M-XVII.15` | 同上 | 婚恋题辅助规则；“受克”按 Moon 所在宫行有凶标签占据或照射（执行口径）；同偈 Arudha 起算不收 |
| Lagna 主与 7 宫主、或 Lagna 主与 Venus 互换、入旺、互照则成 | `M-XVII.16` | 同上 | 婚恋题辅助规则；“落友宫”语义不明不收；同偈触碰部位不收 |
| 8 宫凶星受凶星照且落陷或落敌座则不成；在 6 宫则因病或亲属争执告吹 | `M-XVII.17` 及注 | 同上 | 婚恋题辅助规则；落陷读 D1 尊贵度 `debilitated`，落敌座读 `enemy` 或 `great_enemy`（D1 尊贵度是五重合成值，最凶的 `great_enemy` 同属敌座） |
| 婚期早：Moon 受吉星照落 3／6／7／10／11 宫；或 Venus 与 Moon 落 Lagna／7 宫且 Lagna 为 Gemini、Virgo、Libra、Aquarius；或 Mercury、Venus、Jupiter 落角宫或 7 宫 | `M-XVII.31` | 婚恋题时间 | 只在 `timing-layer.md` 作“偏早”提示，不改日期、不计分 |
| 表白、确立关系等现代恋爱题 | `P-I.4`（一般所谋之事）+ `M-XVII.5／15／16／17` 类比 | 现代恋爱 | B级；婚姻专题只用于 `matter-rules.md` 登记表明列的类比行，类比偈过语境检验（`judgment-rubric.md` §1.3） |
| 寿命、贞洁、子女夭折、相貌、征兆、Yama Sukra | `M-XVII.18–26、33–37` 等 | — | 不收（C 级或不在数据契约） |
| 吉凶落宫换算应事时间 | `M-XIV.83,86,88` | 时间 | 不收：83 只讲忧患、多颗凶星取哪颗未写；86 Raman 自认“One has only to guess”；88 线索多而无排序 |
| 十二宫在即时盘里所管之事；宫的外名／内名（宫与本宫主相连时读内名）；上升＝提问人 | `M-XIV.3–14`、`M-XIV.20–21`、`M-XIV.24` | 判读单叙述 | 取象与叙述，不单独计分（`house-meanings.md` 第 2 节） |
| 七曜所主（Karaka）：Sun 父亲与精神、Moon 母亲与心意、Mars 手足地产勇气、Mercury 言语学识、Jupiter 智力子女智慧健康、Venus 车乘妻室感官之乐、Saturn 忧劳病苦仆从；Karaka 有力则所主显，无力则徒有其名，Saturn 相反 | `M-XIV.31–32` | 判读单叙述；按需读 | 叙述，以及能力层按需减项、行动链起意（Mars）的象义依据；不计分，不构成闭环；见 `house-meanings.md` 第 3 节；叙述不提死亡（`judgment-writing.md` §1） |
| 宫位受损（6／8／12 宫主连接、宫与 6／8／12 宫主相连） | `M-XIV.28–29` | — | 不收：Raman 注“not advisable to apply these combinations literally”；与 Ayer I.3 注“6／8／12 宫主入本宫反而减凶”相冲 |
| 宫、宫主、征象星受损诸项（弱、受凶星合照、无吉星合照等），“其中两三项同时出现，宫就毁坏”，Raman 注要求权衡 | `M-XIV.30` 及注 | 能力层 | **只取作用于事项宫主自身的几项**作折损项：落陷、受凶星占照而无吉星；加 XIV.39–40 的落 6／8／12 宫，及 rubric §9 的次级能力事实燃烧、逆行。三项及以上或两项无救应才算严重受损（`judgment-rubric.md` §5） |
| 宫主与征象星既弱又落 6／8／12 宫则结果为否；强而落凶位，事出现而不得享；弱而落吉位，多少能得。Raman 注：强＝本座、入旺、友座（天然友）；弱＝落陷；吉位＝角宫、三方宫、11 宫 | `M-XIV.39–40` 及注；`M-XIV.42` | 能力层 | 只做否决与叙述，不进账本合计（`judgment-rubric.md` §5）。征象星只在 `matter-rules.md` 的本事古法明确使用时检查。"弱而落吉位"＝宫主落陷而落吉位，记救应、落陷照记；落陷星落天然友座不算强。宫主坐本宫不记落 6／8／12 宫：`M-XIV.42` 宫主落本宫起算的吉位，该宫之事圆满（坐本宫＝本宫起算第 1 宫，执行口径） |
| 行星主典籍归给它的一切象义；卜卦时按所落吉凶宫筛去不合适的象义；落好宫、坏宫定吉凶 | `M-XIV.33`、`M-XIV.47`、`M-XIV.48` | 意愿层 | 取象叙述与限定语检验，不计分（`judgment-rubric.md` §6） |
| 与 Lagna 或 Lagna 主有照、合、角宫关系的宫必然应验；Lagna 主与 5 宫主同宫、互照、互换则得子 | `M-XIV.43`；`M-XVIII.30`（`M-XVII.16` 婚姻同理，已收） | 成事账；意愿层；行动链 | 连接口径：同宫、照射（单向即可）、互换、两星互为 4／10 宫（"角宫关系"的执行口径）；成事账一条，连上记有利、没连上不记不利（创始人 2026-10-29 定，D2）；另用于意愿层、限定语与行动链③（`house-meanings.md` 第 8 节）；婚恋题 `M-XVII.16` 的 Lagna 主–7 宫主互换、互照与之同源，归入连接一条 |
| 宫、宫主、征象星三者同判一宫；"这些原则也用于宫、宫主与征象星"，Raman 注示范从 7 宫起算第 2、第 12 宫，也可从 7 宫主或 Venus 起算 | `M-XIV.116` 及注；`M-XIV.28`、`M-XIV.30`、`M-XIV.39–41` | 转宫；征象星串联 | 执行口径，B 级：别人的动作以其宫为命宫转宫（`question-decomposition.md` 第 3 节）；所问动作的征象星与两端都同宫或由它照射，算串联（`house-meanings.md` 第 8 节）；116 本偈的疾病、死亡判语不收 |
| 婚姻卜问：新娘的一生看 Lagna，新郎的情况从 7 宫读 | `M-XVII.8–9` | 转宫 | 对方以 7 宫为命宫的依据；本章其余议婚细节不收 |
| 征象星强则所主显、弱则徒有其名；能吉能凶之星有力出吉、无力出凶；凶星无力凶全；凶星落 3、6、11 宫转吉；6 宫凶星给所主之物而宫受损，疾病题例外；吉星在 6 宫灭敌、凶星增敌；卜卦按所落之处筛象义 | `M-XIV.32`、`M-XIV.35`、`M-XIV.37`、`M-XIV.44–47` | 按需读 | 取象与按问题读（`house-meanings.md` 第 7 节）：能力层按需减项；`P-I.3` 不把取象单 `needed_planets` 按凶星计（创始人 2026-10-29 定，D3）；其余仍按宫表标签 |
| Moon 或 Venus 与凶星同落 7 宫或 4 宫，与女性起争执 | `M-XIV.117` | 按需读 | 描述型"相处会不会吵"的象义依据；不计分 |
| 10 宫主城镇、议事厅、路边客栈；可见半球主人多、公开，不可见半球主僻静、隐蔽，7 宫主为例 | `M-XIV.12`、`M-XIV.118–120` | 限定语检验 | 显隐判定的第 2、3 序位（`house-meanings.md` 第 9 节） |
| 12 宫主饭后歇息：吉星安眠、凶星不安；12 宫主入旺睡好床、落陷睡地上 | `M-XXVII.15–16` | 宫义 | 只作宫义（12 宫与睡眠、床榻），进 `house-meanings.md`；饮食问占本身不收 |
| 照 Lagna 之星落本座则事在自己家，落他星之座则在外；Moon 与 Saturn 相连、落 4 宫或水象座则在暗处，Sun 照或同 Moon 则不暗 | `M-XXVIII.5`、`M-XXVIII.19` | 限定语检验 | 在家在外、显隐判定的第 1 序位（两性、私会语境）；交合专章其余各偈不收 |

### 2.1 吉凶口径（Ayer 功能吉凶）

Ayer 在 I.3 注中主张按 functional character 取吉凶，并给出 Rule 1（本宫主对本宫
恒吉）、Rule 2 及两个例子；没写到的情况，回落他在同注引用的 Bhattotpala 自然吉凶。
标准层按此执行，不另引入 Laghu Parashari 全表，也不复用 engine 的 functional P1。

| 顺序 | 条件（从被占据／照射的星座 S 起数宫） | 标签 | 出处 |
|---:|---|---|---|
| F1 | 行星是 S 的座主 | 吉(宫主) | I.3 正文 + 注 Rule 1；凶星、6／8／12 宫主同样适用（注称这些宫主“strong and declared for that reason functional benefics”，入本宫减凶；F1 不另加“强”条件） |
| F2 | 行星同管 S 起第 3、12 宫，且落陷 | 凶(注例一) | 注例一：Jupiter 对 Capricorn |
| F3 | 行星同管 S 起一个角宫（4／7／10）和一个三方宫（5／9），且强（D1 `exalted`／`own_sign`／`moolatrikona`） | 吉(注例二) | 注例二：Mars 对 Leo，“provided he is strong” |
| 回落 | 其余 | 自然吉凶 + “(回落)” | 同注：Bhattotpala 取自然吉凶 |

- 参照点是被占据或照射的星座本身，不从 Lagna 起数；同一颗星对不同宫可有不同标签。
- 回落时：Mercury 与 Sun／Mars／Saturn 同宫为凶；Moon 亏月为凶，盈月记“盈月未定”
  （原文只在 I.5、VI.3 明确满月为吉，由这两条规则自读满月窗）。Rahu／Ketu 不贴标签。
- 标签由 formatter 写进宫表“七曜占据”“七曜照射本宫”两列，判读只查表，不手推。
  “吉星照 Lagna”看第 1 宫行；“吉星照 Moon-lagna”看 Moon 所在宫行；`P-II.2` 的凶星照与吉凶同照
  也看这两行。`P-II.2` 只读这两行的“七曜照射本宫”列，同宫不算照（原文“Benefic aspects to the lagna
  and the Moon-lagna”）。
- 有注要求按功能取的偈走标签：I.3、I.4、I.5 的“strong benefic in 11th”、II.3、
  III.1、III.3、VII.2。
- 正文点名行星且 Ayer 无注的偈按点名判，不换标签：I.5 的满月受 Jupiter／Venus 照、
  II.9、II.11、III.5、V.1 的 Jupiter／Venus、V.2、VII.1、VII.12。
- IV.3 的 Moon 按原文 “(Malefic) Moon”：Lagna 条款仅亏月成立；10 宫条款不论盈亏。
- 满月窗（tithi 10～20）只供 I.5、VI.3 使用；它与“亏月”分属不同规则，不互相改写。
- I.5、VI.3 的“强吉星”：D1 `exalted`／`own_sign`／`moolatrikona`（根本三角是本座里的一段度数，归本座）算强，与 F3 同口径。I.5 注说强弱按位置力、运动力
  等算，运动力不在数据契约，不算。
- V.3 注“the Moon should not be weak, even as the benefics”：D1 `debilitated` 算弱。
- I.3 注所引 Laghu Jataka（8、12 宫无吉）不收：Ayer 引后改用自己的 Rule 1／2，并论证 6／8／12
  宫主入本宫反而减凶。

---

## 3. 问题支持级

### A级：有题目专属 `P` 规则

只有在 `matter-rules.md` 登记为 A 级、能定位到具体章／节／sloka 时使用专题规则。有专题规则时先查专题规则
并入账，与通用规则同账等权、按占优断（`judgment-rubric.md` §2.2）；专题规则不单独否决，也不外推到别的题型。

### B级：只有一般宫／宫主规则或 Bhavan 实例

允许使用：

- Lagna／Lagna 主；
- 一个主事项宫及其宫主；
- `P-I.3` 的宫位扶压；
- 通用环境规则 `P-I.4`（所问之事能否达成）与 `P-IV.1`（Ayer 目录的"omnibus solution"），按 `judgment-rubric.md` §1 收入每个成败题；
- 连接（`M-XIV.43`），成事账一条；
- 能力层与意愿层（`judgment-rubric.md` §5、§6），读"宫主能力与连接"表；
- 与题型吻合的 `B` 实例只作兼容性辅证。

B级输出必须标“通用古典规则判读”；这是来源覆盖等级，不是准确率或概率。
B级照常计分，不得把 B 自动记持平。自然 Karaka 只能作有来源的次级说明，不构成必须闭环。

### C级：拆题后连一个有出处的宫义都对不上

停止成败判定；澄清问题或明确告知当前标准层不支持。按 `house-meanings.md` 宫义与关键词选事项宫并写明出处的，是 B 级通用判读（`matter-rules.md` 第 3 节），不算"找最像的宫"硬套。

---

## 4. 标准层数据白名单

`structured_prashna.md` 默认主层只允许：

1. D1 Lagna、Lagna 度数、星座性质和边界距离；
2. rising Navamsa 的星座与本座第几个 Navamsa，不输出完整 D9；Lagna 六分盘座主表
   （`P-I.4` 注：Lagna、传统 Sun／Moon Hora、Drekkana、Navamsa、Dwadasamsa、Trimsamsa 各一
   行：星座、座主、座主对 Lagna 星座的功能吉凶、距本分盘座内分界），附吉凶合计、多数与
   多数临界距离；不输出任何分盘的其余行星；
3. D1 七曜位置；Rahu／Ketu 只列位置事实；
4. 12宫、宫主、宫主落宫、宫内行星；
5. 七曜的整宫 Graha Drishti；宫表中七曜占据与照射附 §2.1 的功能吉凶标签；
6. D1 尊贵度、engine 的行星特定燃烧结果、逆行事实；
7. Moon 月相、tithi、是否在 `P-I.5` 满月窗、位置、当前整宫接触；月宿只作描述或
   题目软验证；
8. 简单互视与宫主交换的结构事实，不自动附带 natal yoga 分类；
9. 描述题与天气查表事实（`P-VI.1~2`、`P-VI.4`、`P-I.7`、`P-VII.13`、`P-VII.12`、`P-VII.3~4`），只给
   原文查表结果，歧义两说并列；
10. 时间副层的指针说明（时间本身只写在 `timing_overlay.md`）；
11. 由第 4–6 项派生、只列事实的三张表：宫主能力与连接（能力层、意愿层）；行动者视角（转宫）与行动链
    （行动型问题，`judgment-rubric.md` §8）；征象星串联。不进账本合计。

判定产物 `prashna_verdict.json`／`prashna_verdict.md` 由判定脚本只读本白名单字段与取象单生成。

默认产物禁止出现：

- Chara Karaka、DK、UL、AL；
- SAV／BAV、Shadbala、Bhava Bala；
- 完整 D9、D10、D4、D5 或其他本命分盘；
- natal yoga prescan、engine functional P1 身份（宫表的 Ayer 吉凶标签是 `P-I.3`
  注规则，按被占据／照射的星座起算，不是 P1）；
- 120 年 Vimshottari、Chara Dasha；
- transit、Sade Sati、double transit；
- Tajika／KP 字段（除非用户显式切换对应沙箱）。

共享 engine 可以为其他 skill 继续计算这些字段；Prashna 专用 formatter 不消费、
不输出，也不允许判读层引用。

---

## 5. 判定契约

标准层不运行固定"五轴全部打分"。判定由脚本执行（`judgment-rubric.md`；实现 `scripts/prashna_rules.py`），每个成败题输出**成事账**：

| 字段 | 要求 |
|---|---|
| rule_id | 如 `P-I.3`、`P-I.4`、`M-XIV.43` |
| level | A／B／B（类比）／B（通用环境） |
| reason | 为什么该规则适用于本题 |
| evidence | 只引用白名单字段 |
| direction | 有利／不利／混合／无方向；两说给第二读法 |
| score | +1／−1／0（`B` 实例不计分；语境不合的类比偈不入账） |

输出另分开记录：`source_support`（A／B，规则来源对题型的覆盖程度，不是概率）、`system_status`（标准层或实验栈）、输入提示（不改档，
`judgment-rubric.md` §13）。内部三档按 `judgment-rubric.md` §2–§4，只写判读单核对区；给用户看的部分讲事情怎么走（`judgment-writing.md`）。
成败档次与时间副层分开：时间只在偏成／持平档给出，不因时间远近改档（`timing-layer.md`）。

### 5.1 描述输出契约

描述题（失物性质、藏处、方向距离等）与天气题不建规则账本、不出三档、
不跑时间副层，只输出：

| 字段 | 要求 |
|---|---|
| rule_id | 如 `P-VI.4`、`P-VII.4` |
| 查表结果 | 原样引用 `structured_prashna.md` 描述节，不改写、不合并 |
| 两说 | 原文与注、或注内两种口径不一致时并列，不择一 |
| 适用条件 | 天气只限雨季；条件不满足时写“原文无反面判据”，不判“不下雨” |

描述题若同时问“能不能找回”，成败部分另走失物题账本（`P-VI.3` 主；`P-V.1`、`P-II.1~2` 动／固座、11 宫 `P-I.3` 辅助；`P-I.5` 只讲快慢），两部分分开写。

---

## 6. 来源锚点

- [*Shatpanchasika*, V. Subrahmanya Sastri 译本](https://archive.org/details/dli.ministry.22678)：
  I.2–5，及各专题章。
- KN Rao, [“The Case of Sanjay Dutt and Punishment”](https://www.journalofastrology.com/article.php?article_id=60)：
  snapshot 有限性及避免滥用 Prashna。
- KN Rao, [“Eternal India 17”](https://www.journalofastrology.com/article.php?article_id=150)：
  有可靠本命盘时直接使用本命 Dasha。
- KN Rao, [“Precarious Prediction: World Cup Football Final 2014”](https://www.journalofastrology.com/article.php?article_id=476)：
  再次说明其谨慎立场。
- Journal of Astrology, [“Nuke Deal: Governments Meeting with the Left”](https://www.journalofastrology.com/article.php?article_id=99)：
  1宫／7宫双方实例。
- G. N. Saxena, [“Case Study of a Prediction – Missing Persons”](https://www.journalofastrology.com/article.php?article_id=153)：
  Bhavan 实例；含 Tajika，不可整体搬入标准层。
- [*Prasna Marga*, B. V. Raman 译本](https://archive.org/details/PrasnaMargaBVR)：
  VI.39、65–67；VIII.29、63–65；XIV.3–14、20–48、81–83、85–86、88、90、98、115–120；XVII.5、8–9、11–19、31 及注；XVIII.30、148 注；
  XXIV.45、68；XXVII.15–16；XXVIII.1–6、19；Appendix IV。
- *Shatpanchasika*, V. A. K. Ayer 译本（*Indian Horary*）：I.2–5、I.7、II.1–2、II.5、II.9、
  II.11、III.1、III.3–5、IV.1–5、V.1–3、V.5、VI.1–4、VII.1–4、VII.12–13，
  各章示范题及译者注（I.3 注 Rule 1/2 及两例为功能吉凶依据）。
