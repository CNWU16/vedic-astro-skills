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
| `M` | *Prasna Marga*／Kerala 系 | 默认不进入；只用于纠错边界或独立模块 |
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
| 事项宫被其宫主或吉星占据／照射则增强，受凶星伤害则减损 | `P-I.3` | 全部宫位 | 核心 |
| 一般所谋之事可检查 Lagna、rising Navamsa、头升／背升及吉凶扶压 | `P-I.4` | 一般事业成败 | 条件适用 |
| 混合配置表示困难后成，不能由单一弱点判死 | `P-I.4` | 一般事业成败 | 核心 |
| Lagna、Sun、Moon 动／静星座“snapshot” | `K` | KN Rao 的有限快照法 | 只作有限辅证；本人明说并非总有效 |
| 1宫代表一方、7宫代表另一方 | `B-article-99` | 双方／谈判案例 | B级题型可用 |
| 用 Lagna、Lagna 主、Moon 及月宿核对盘是否反映问题 | `B-article-153` | 失踪者单案例 | 只作软验证候选 |
| Moon 为所有题型最高权重 | `U` | — | 禁入 |
| Moon 无同宫／Graha Drishti 即“空亡”或“不成” | 无支持 | — | 禁入 |
| Moon 月宿主是所有题型固定 significator | `B` 单案例 | — | 禁作全局硬门 |
| Chandra Kriya 是 60 种 lunar actions | `M-VIII.63~65` | Kerala 模块 | 仅纠错边界 |
| Moon ingress 等于 Dasha 切换或事件应期 | `U` | — | 禁入 |
| Chara Karaka、DK、UL、AL 用于默认 Prashna | `U` | — | 禁入 |
| SAV／BAV 用于默认 Prashna | `U` | — | 禁入 |
| D9 只读取 rising Navamsa；完整 D9 人生解读 | `P-I.4`／`U` | 一般所谋之事／其余 | 只保留 rising Navamsa |
| D10／D4／D5 等本命分盘 | `U` | — | 禁入 |
| 提问盘生成的 120 年 Vimshottari／Chara Dasha | 与 `K/M` 边界冲突 | — | 禁入 |
| *Prasna Marga* 一年／一月 Prasna Dasa | `M-VI.39,65~67` | Kerala | 不自动进入 K/P/B 主层 |
| D1 尊贵度、自然吉凶、受克和燃烧事实 | `P-I.3` 及注释 | 行星承事能力 | 次级，不单项定档 |
| 逆行统一等于失败 | `U` | — | 禁入；只在专题规则明示时使用 |
| 3／6／8／12 一律作为同级阻碍宫 | 与 `P` 题目语义冲突 | — | 禁入 |
| Lagna 主必须连接事项宫主 | 仅部分 `B/P` 专题 | — | 禁作全局硬门 |
| 事项宫主必须与自然 Karaka 闭环 | `U` | — | 禁入 |
| 三档“成／悬／不成” | `P-I.4` 的成功／失败／困难后成 + `E` 输出契约 | 全部 | 可保留，但不冒充所有题型原文措辞 |
| 24小时／3个月重复起盘阈值 | `U/E` | — | 删除数字阈值 |
| 时间地点粗略时检查 Lagna／Navamsa 边界敏感性 | `E` | 全部 | 输入稳定性门控 |

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
2. rising Navamsa 的星座与座主，不输出完整 D9；
3. D1 七曜位置；Rahu／Ketu 只列位置事实；
4. 12宫、宫主、宫主落宫、宫内行星；
5. 七曜的整宫 Graha Drishti；
6. D1 尊贵度、engine 的行星特定燃烧结果、逆行事实；
7. Moon 月相、位置、当前整宫接触；月宿只作描述或题目软验证；
8. 简单互视与宫主交换的结构事实，不自动附带 natal yoga 分类；
9. 明确的择时禁用说明。

默认产物禁止出现：

- Chara Karaka、DK、UL、AL；
- SAV／BAV、Shadbala、Bhava Bala；
- 完整 D9、D10、D4、D5 或其他本命分盘；
- natal yoga prescan、functional P1 身份；
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

成败档次与 timing 状态分开；缺少 timing 模块本身不改变成败档次。
若临界字段未被本题适用规则消费，只报告该字段敏感，不得因此自动降档。

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
  VI.39、65–67；VIII.63–65 及 Appendix IV。
