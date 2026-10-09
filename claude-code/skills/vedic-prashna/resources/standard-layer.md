# Prashna 标准层：来源、准入与数据契约

> **用途**：约束默认主层。任何成败规则先在本文件取得来源标签、适用范围和
> 准入状态，才能进入 `SKILL.md`、判定 rubric 或代码。
>
> **标准层名称**：以 *Shatpanchasika* 为主文本、经 KN Rao／Bharatiya Vidya
> Bhavan 实践兼容性筛选的古典 Prashna。不得简称为“KN Rao 自创 Prashna
> 体系”，也不得把 KN Rao 的本命盘工具自动迁入提问盘。

---

## 1. 来源标签与准入规则

| 标签 | 含义 | 主层权限 |
|---|---|---|
| `K` | KN Rao 本人直接表述或本人署名案例 | 可进入，但不得扩大原文适用范围 |
| `P` | *Shatpanchasika* 原文／可定位译文 | 可进入；专题规则只用于对应题型 |
| `B` | Bhavan／Journal of Astrology 实例 | 可作兼容性与用法证据，不冒充 KN Rao 原话 |
| `M` | *Prasna Marga*／Kerala 系 | 默认不进入；只用于纠错边界或独立模块（时间副层见 `timing-layer.md`） |
| `T` | Tajika | 仅 Tajika 沙箱 |
| `KP` | Krishnamurti Paddhati | 仅 KP 独立栈 |
| `E` | 工程／产品规则 | 可作输入、隔离和置信度门控，不冒充古典教义 |
| `U` | 未核证或只有泛化推断 | 禁止进入默认成败和择时 |

主层规则必须满足：

1. 至少有一个 `K`、`P` 或 `B` 来源；
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
| 一般所谋之事可检查 Lagna、rising Navamsa、头升／背升及吉凶扶压 | `P-I.4` | 一般事业成败 | 条件适用 |
| 混合配置表示困难后成，不能由单一弱点判死 | `P-I.4` | 一般事业成败 | 核心 |
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
| D9 只读取 rising Navamsa；完整 D9 人生解读 | `P-I.4`／`U` | 一般所谋之事／其余 | 只保留 rising Navamsa |
| D10／D4／D5 等本命分盘 | `U` | — | 禁入 |
| 提问盘生成的 120 年 Vimshottari／Chara Dasha | 与 `K/M` 边界冲突 | — | 禁入 |
| *Prasna Marga* 一年／一月 Prasna Dasa | `M-VI.39,65~67` | Kerala | 不自动进入 K/P/B 主层 |
| 宫数／Navamsa 数换算应事时间 | `M-XIV.81~82,85`、`P-V.5` | 时间副层 | 只在 `timing-layer.md`；不改三档 |
| 固定座上升得位（Sthana labha），动座相反，变动座混合；吉星照 Lagna 与 Moon-lagna 吉 | `P-II.1~2` | 位置得失；Ayer 注扩展到求职 | 求职／保工作题主规则（见 `question-taxonomy.md` §2.8） |
| 吉星落 10／7 宫赐位置（position）；凶星落 12／11 宫不吉；(Malefic) Moon 在 Lagna 不利，在 10 宫“even when malefic”有利 | `P-IV.3` | 位置 | 求职题主规则；Lagna 条款只在亏月成立，10 宫条款不论盈亏 |
| 吉星落 10／1／7 宫则胜；Mars／Saturn 落 9 宫败，Mercury／Jupiter／Venus 落 9 宫胜 | `P-III.1` | 战事胜负；Ayer 注扩展到选举等 competitive efforts | 竞争性考试同向检查，B级（主规则 `P-II.1~2`） |
| 人形星座上升且有吉星、吉星落 12／11 宫、吉星落 kendra 或人形 Lagna 受吉星照则和解；凶星落变动座则冲突，凶星同样落位受凶星照则相反 | `P-III.3~4` | 王者和解；Ayer 注扩展到 settlement of scores／negotiations | 谈判／和解A级；复合类比B级（见 `question-taxonomy.md` §2.7） |
| 吉凶按功能取：F1 本宫主对本宫恒吉；F2 同管本宫起 3、12 宫且落陷为凶；F3 同管本宫起角宫与三方宫且强（exalted／own_sign）为吉；其余回落 Bhattotpala 自然吉凶 | `P-I.3` 注 Rule 1/2 及两例；Bhattotpala 见同注 | 全部 `P` 规则中的“吉星／凶星” | 采纳；正文点名行星且 Ayer 无注的偈按点名，不换标签（见 §2.1） |
| D1 尊贵度、受克和燃烧事实 | `P-I.3` 及注释 | 行星承事能力；F2／F3 的落陷与强 | 次级，不单项定档 |
| Chyuti 看 Lagna：动座且受本宫主或吉星占据／照射、无凶星则变动成立，固定座不变，变动座看吉凶多寡；Vriddhi 看 4 宫：受本宫主或吉星占据／照射则兴；Pravasa 看 10 宫：动座且受凶星照则成行，受本宫主或吉星照则否；Nivritti 看 7 宫：动座且受本宫主或吉星照则返回，受凶星照则否 | `P-I.2` 及注 | 换工作／裁员／调岗、房屋、出行、返回；注例扩展到诽谤 | 对应题型主规则，A级 |
| 满月（白半月第 10 至黑半月第 5 tithi）落 Lagna 受 Jupiter／Venus 照，或强吉星落 11 宫，失物速得 | `P-I.5` 及注 | 失物、走失者 | 失物题主规则 |
| rising Navamsa 序号按奇偶座定 Dhatu／Moola／Jeeva | `P-I.7` 及注表 | 描述物品属性 | 描述题查表，不进三档 |
| 吉星落角宫、三方宫且凶星不落角宫和 8 宫则全面兴旺 | `P-IV.1` | 一般前景 | 不单立题型；一般所谋之事仍走 `P-I.4` |
| 吉星落 3／5／11／7 宫得益，凶星则损；吉星落人形座亦吉；照射等同占据 | `P-IV.2` 及注 | 示范题：投资 | 投资题，B级 |
| Moon 落 2／7／10／11／6／3 受 Jupiter 照，好处来自女性 | `P-IV.4` | 示范题：继承 | 本批不收 |
| 吉星落 Lagna／7／8／5 宫且彼此相照，Moon 落 3／6／10／11 宫，则病愈 | `P-IV.5` 及注 | 疾病康复 | 疾病题主规则，A级 |
| 行星落 5／2／3 宫则离者返回；吉星落此则失物复得；Jupiter／Venus 落此则速 | `P-V.1` | 失踪者返回、失物；示范题含亏损补回 | 返回题 A级；失物题同向检查；亏损补回 B级 |
| 7 或 6 宫有星、Jupiter 落角宫或 Mercury／Venus 落三方宫，离者返回；Moon 落 8 宫且角宫无凶星则平安返回，角宫有吉星则带利返回 | `P-V.2~3` 及注 | 远方之人返回 | 返回题同向检查 |
| Jupiter 或 Venus 落 Lagna 起 2／3 宫，远方之人很快到来 | `P-III.5` 及注 | 示范题：儿子能否从海外返回 | 返回题同向检查，按点名行星 |
| 动座上升且 Sun／Saturn／Mercury／Venus 之一占据则很快出发；该星逆行则否 | `P-II.9` 及注 | 示范题：早日出国 | 出行题“能否早日出发”同向检查，按点名行星 |
| Sun 与 Moon 落 4 宫则不来；Mercury／Jupiter／Venus 落 4 宫则很快来 | `P-II.11` 及注 | 示范题：官司会否很快开庭 | 开庭题，B级，按点名行星 |
| 固定座／固定 Navamsa／vargottama 上升则亲属所盗、藏于屋内；Lagna 所在 drekkana 定藏处 | `P-VI.1~2` 及注 | 失物描述 | 描述题查表，不进三档 |
| 满月或吉星占 Lagna、头升座上升受吉星照、或强吉星落 11 宫则速得；皆无则渺茫 | `P-VI.3` 及注 | 失物找回快慢 | 失物题同向检查；Gemini 是否头升两说并列 |
| 角宫行星定方向，无则 Lagna 定方向；距离按 Navamsa 序号 | `P-VI.4` 及注 | 失物、失踪者方向距离 | 描述题查表；单星时正文与注两读并列 |
| Saturn 落 Lagna 起奇数宫（不计 Lagna）为男，否则为女 | `P-VII.1` 及注 | 胎儿性别；婚姻 | A级 |
| 雨季 Venus 与 Saturn 落 Moon 起 7 宫或 Lagna 起 2／3／4／8 宫；白半月吉星落水象座的 3／2／角宫，或 Moon 落水象 Lagna，则有雨 | `P-VII.3~4` 及注 | 雨季天气 | 天气查表；原文无反面判据，不判“不下雨”；水象座两说并列 |
| Lagna 落阳性 varga 受强阳性星照为男等 | `P-VII.5` 及注 | 胎儿性别 | 本批不收：需六分盘 varga，Hora 分盘口径与精度未核 |
| Sun 带吉星落 8 宫受吉星照则父亲在外，否则在本地 | `P-VII.12` 及注 | 父亲下落；注称其他 karaka 同理 | 父亲 A级；其他亲属 B级 |
| Navamsa 定物、drekkana 定贼、星座定时间方向位置、Lagna 主定年龄 | `P-VII.13` 及注 | 失物描述 | 描述题查表；种姓、颜色、窃贼外貌、Navamsa 强弱不收 |
| I.6、VII.6~9 读所想之物／所问之人；VII.10 私生活；VII.11、V.4 生死安危 | `P` | 读心、隐私、生死 | 不收（C级） |
| II.8、II.10 敌军动向 | `P` | 示范题挂考试 | 已知未收：原文未写敌军来去如何对应考试成败 |
| 逆行统一等于失败 | `U` | — | 禁入；只在专题规则明示时使用 |
| 3／6／8／12 一律作为同级阻碍宫 | 与 `P` 题目语义冲突 | — | 禁入 |
| Lagna 主必须连接事项宫主 | 仅部分 `B/P` 专题 | — | 禁作全局硬门 |
| 事项宫主必须与自然 Karaka 闭环 | `U` | — | 禁入 |
| 三档“成／悬／不成” | `P-I.4` 的成功／失败／困难后成 + `E` 输出契约 | 全部 | 可保留，但不冒充所有题型原文措辞 |
| 24小时／3个月重复起盘阈值 | `U/E` | — | 删除数字阈值 |
| 时间地点粗略时检查 Lagna／Navamsa 边界敏感性 | `E` | 全部 | 输入稳定性门控 |

### 2.1 吉凶口径（Ayer 功能吉凶）

Ayer 在 I.3 注中主张按 functional character 取吉凶，并给出 Rule 1（本宫主对本宫
恒吉）、Rule 2 及两个例子；没写到的情况，回落他在同注引用的 Bhattotpala 自然吉凶。
标准层按此执行，不另引入 Laghu Parashari 全表，也不复用 engine 的 functional P1。

| 顺序 | 条件（从被占据／照射的星座 S 起数宫） | 标签 | 出处 |
|---:|---|---|---|
| F1 | 行星是 S 的座主 | 吉(宫主) | I.3 正文 + 注 Rule 1；凶星、6／8／12 宫主同样适用 |
| F2 | 行星同管 S 起第 3、12 宫，且落陷 | 凶(注例一) | 注例一：Jupiter 对 Capricorn |
| F3 | 行星同管 S 起一个角宫（4／7／10）和一个三方宫（5／9），且强（D1 `exalted`／`own_sign`） | 吉(注例二) | 注例二：Mars 对 Leo，“provided he is strong” |
| 回落 | 其余 | 自然吉凶 + “(回落)” | 同注：Bhattotpala 取自然吉凶 |

- 参照点是被占据或照射的星座本身，不从 Lagna 起数；同一颗星对不同宫可有不同标签。
- 回落时：Mercury 与 Sun／Mars／Saturn 同宫为凶；Moon 亏月为凶，盈月记“盈月未定”
  （原文只在 I.5、VI.3 明确满月为吉，由这两条规则自读满月窗）。Rahu／Ketu 不贴标签。
- 标签由 formatter 写进宫表“七曜占据”“七曜照射本宫”两列，判读只查表，不手推。
  “吉星照 Lagna”看第 1 宫行；“吉星照 Moon-lagna”看 Moon 所在宫行。
- 有注要求按功能取的偈走标签：I.3、I.4、I.5 的“strong benefic in 11th”、II.3、
  III.1、III.3、VII.2。
- 正文点名行星且 Ayer 无注的偈按点名判，不换标签：I.5 的满月受 Jupiter／Venus 照、
  II.9、II.11、III.5、V.1 的 Jupiter／Venus、V.2、VII.1、VII.12。
- IV.3 的 Moon 按原文 “(Malefic) Moon”：Lagna 条款仅亏月成立；10 宫条款不论盈亏。
- 满月窗（tithi 10～20）只供 I.5、VI.3 使用；它与“亏月”分属不同规则，不互相改写。

---

## 3. 问题支持级

### A级：有题目专属 `P` 规则

只有在 `question-taxonomy.md` 能定位到具体章／节／sloka 时使用专题规则。专题
证据优先于一般规则，但不得外推到别的题型。

### B级：只有一般宫／宫主规则或 Bhavan 实例

允许使用：

- Lagna／Lagna 主；
- 一个主事项宫及其宫主；
- `P-I.3` 的宫位扶压；
- 若确实属于“一般所谋之事”，使用 `P-I.4`；
- 与题型吻合的 `B` 实例只作兼容性辅证。

B级输出必须标“通用古典规则判读”；这是来源覆盖等级，不是准确率或概率。
不得把 B 自动翻译成“悬”。自然 Karaka 只能作有来源的次级说明，不构成必须闭环。

### C级：事项宫本身也缺少可靠映射

停止成败判定；澄清问题或明确告知当前标准层不支持。禁止“找最像的宫”硬套。

---

## 4. 标准层数据白名单

`structured_prashna.md` 默认主层只允许：

1. D1 Lagna、Lagna 度数、星座性质和边界距离；
2. rising Navamsa 的星座、本座第几个 Navamsa、座主及座主对 Lagna 星座的功能吉凶
   标签，不输出完整 D9；
3. D1 七曜位置；Rahu／Ketu 只列位置事实；
4. 12宫、宫主、宫主落宫、宫内行星；
5. 七曜的整宫 Graha Drishti；宫表中七曜占据与照射附 §2.1 的功能吉凶标签；
6. D1 尊贵度、engine 的行星特定燃烧结果、逆行事实；
7. Moon 月相、tithi、是否在 `P-I.5` 满月窗、位置、当前整宫接触；月宿只作描述或
   题目软验证；
8. 简单互视与宫主交换的结构事实，不自动附带 natal yoga 分类；
9. 描述题与天气查表事实（`P-VI.1~2`、`P-VI.4`、`P-I.7`、`P-VII.13`、`P-VII.3~4`），只给
   原文查表结果，歧义两说并列；
10. 时间副层的指针说明（时间本身只写在 `timing_overlay.md`）。

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

标准层不再运行固定“五轴全部打分”。每张盘先建立**适用规则账本**：

| 字段 | 要求 |
|---|---|
| rule_id | 如 `P-I.3`、`P-I.4`、`B-article-99` |
| support_level | A／B |
| scope_match | 为什么该规则适用于本题 |
| raw_evidence | 只引用白名单字段 |
| direction | 有利／不利／混合 |
| weight | 主规则／辅证 |
| conflict | 与哪条同级或更高来源冲突 |

输出必须分开记录：

1. `source_support`：A／B，表示规则来源对题型的覆盖程度，不是概率；
2. `input_stability`：本题实际消费字段是否可能随时间／地点误差改变；
3. `system_status`：标准层或尚待例盘验证的实验栈状态。

结论：

- **成**：适用的题目主规则与一般规则共同偏有利，没有同级强反证；
- **悬**：规则混合、只有B级通用规则且方向不集中，或输入边界敏感；
- **不成**：至少两条相互独立的适用主规则偏不利，且没有同级救援；
- 单一 Moon、单一宫位、单一尊贵度或单一缺失不能独立判“不成”。

成败档次与时间副层分开：时间只在成／悬档给出，不因时间远近改档（见 `timing-layer.md`）。
若临界字段未被本题适用规则消费，只报告该字段敏感，不得因此自动降档。

### 5.1 描述输出契约

描述题（失物性质、藏处、方向距离等）与天气题不建规则账本、不出三档、
不跑时间副层，只输出：

| 字段 | 要求 |
|---|---|
| rule_id | 如 `P-VI.4`、`P-VII.4` |
| 查表结果 | 原样引用 `structured_prashna.md` 描述节，不改写、不合并 |
| 两说 | 原文与注、或注内两种口径不一致时并列，不择一 |
| 适用条件 | 天气只限雨季；条件不满足时写“原文无反面判据”，不判“不下雨” |

描述题若同时问“能不能找回”，成败部分另走失物题账本（`P-I.5`；`P-VI.3`、`P-V.1` 同向），两部分分开写。

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
  VI.39、65–67；VIII.63–65；XIV.81–82、85 及 Appendix IV。
- *Shatpanchasika*, V. A. K. Ayer 译本（*Indian Horary*）：I.2–5、I.7、II.1–2、II.9、
  II.11、III.1、III.3–5、IV.1–5、V.1–3、V.5、VI.1–4、VII.1、VII.3–4、VII.12–13，
  各章示范题及译者注（I.3 注 Rule 1/2 及两例为功能吉凶依据）。
