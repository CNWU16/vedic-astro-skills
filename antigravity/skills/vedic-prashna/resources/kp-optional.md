# KP Horary 独立栈（1–249）

## 定位

KP 是与 Parashari 标准层在计算、文件和判读权上隔离的独立体系，不是副证据。
用户可以分别查看两套结果或在 Q&A 中并列比较，但不得拼票。只有用户明确要求 KP，
并亲自给出 `1–249` 数字时运行。

不得：

- 从提问文字、当前分钟或随机数替用户生成号码；
- 只用时刻上升点却称为经典 KP Horary；
- 把 KP 输出追加到 `structured_prashna.md`；
- 同时显示 KP 与 Parashari 两套主结论再“综合”；
- 使用 True Citra 代替 Krishnamurti ayanamsa；
- 使用标准层的 Moon ingress、Chandra Kriya 或 natal Dasha timing。

---

## 原生来源

本栈以 K.S. Krishnamurti Readers 为规则源：

- Reader I, *Casting the Horoscope*：Placidus／Raphael houses、
  Krishnamurti ayanamsa；
- Reader III, *Predictive Stellar Astrology*：Vimshottari 比例 sub、249 区；
- Reader IV, *Marriage, Married Life & Children*：婚姻、重聚语义的交叉核对；
- Reader VI, *Horary Astrology*：1–249 输入、significator 顺序、cusp
  sub-lord、当前已实现题型宫组、Ruling Planets。

扫描合集：
<https://archive.org/details/kp-readers>

---

## Phase KP-0：输入门

必收：

| 输入 | 要求 |
|---|---|
| 具体问题 | 一个可观察结果 |
| KP number | 用户给出的整数 `1–249` |
| 判盘时刻 | 开始判断问题的时刻 |
| 判盘地点 | 当时判断所在地；经纬和 IANA 时区 |
| 题型 | 必须命中已实现的题型规则 |
| 可观察结果范围 | 必须由用户确认，且与题型的来源范围完全一致 |

当前支持：

| topic | outcome scope | 判断 cusp | 正向条件 | 反向条件 | 来源范围 |
|---|---|---:|---|---|---|
| `love-materialization` | `explicit-mutual-relationship` | 5 | 7 与 11 必须同时关联 | 6 或 12 任一关联 | 双方是否建立明确确认并持续推进的恋爱关系 |
| `business-partnership-continuity` | `business-partnership-continuity` | 7 | 5 或 11 任一关联 | 6 或 12 任一关联 | 既有商业合作关系能否延续 |

题型必须按唯一的可观察结果选择。同一问题同时命中多个 topic 时，返回输入门重新
澄清，不在一张 KP 盘中合并宫组。

### 关系题范围门

先原样确认用户要观察的结果，禁止为了命中现有公式而提高问题门槛：

| 用户真正要观察的结果 | outcome scope | 当前处理 |
|---|---|---|
| 建立明确、双方确认并持续推进的恋爱关系 | `explicit-mutual-relationship` | 可进入 `love-materialization` |
| 仅恢复轻松、升温或暧昧互动 | `romantic-interaction-rewarming` | 失败关闭，不起 KP 盘 |
| 仅重新联系、回复或见面 | `romantic-contact-resumption` | 失败关闭，不起 KP 盘 |
| 对方的秘密感受、想法或行动意图 | `private-feelings-or-intent` | 失败关闭，不起 KP 盘 |

若“回暖／联系”和“落实明确关系”同时出现，先让用户选择一个可观察结果；不得把
前者当作后者的同义词，也不得因为用户已经给了号码就跳过范围门。失败关闭表示
当前来源没有对应公式，不表示现实事件不会发生。

当前不自动支持 `marital-reunion`。Reader IV／VI 至少保留三个不同语境：

- “重聚并恢复家庭生活”使用 2、7、11 的事件 significators；
- “丈夫是否回来同住”先检查 11 cusp，并分别列 11、7、6 与 12、7、6；
- 离婚章节另把 reunion 写为 1、5、7、11。

这些不能拼成“7 cusp；2/7/11 对 6/12”的统一 promise 公式。拆出单义题型并完成
出版例盘测试前，入口必须失败关闭。

Reader IV 的 1966-06-09 “reunion with husband and domestic facility”例确实使用
2、7、11，但它是提问时刻盘：原页没有 1–249 number，也没有单列地点，并以事件
significators 与 query-time periods 推到 1968-03-09～29。它可以验证该语境的宫组
与 period 叙述，不能伪装成当前 `1–249 + cusp sub-lord promise` 的端到端例盘。

进入下一阶段条件：号码、题型、用户确认的 outcome scope、时刻和地点完整，且
outcome scope 与题型的来源范围完全一致。

---

## Phase KP-1：独立起盘

运行：

```bash
python scripts/build_kp_horary.py \
  --datetime "<YYYY-MM-DD HH:MM[:SS[.ffffff]]|now>" \
  --lat <lat> --lon <lon> --tz "<IANA>" \
  --number <1-249> \
  --topic "<supported-topic>" \
  --outcome-scope "<user-confirmed-supported-scope>" \
  --question "<single observable question>" \
  --label "<kebab-case>" \
  --out-parent "<parent>"
```

输出：

```text
kp_horary_<yyyymmdd_HHMMSS>_<label>/
├── structured_kp.md
├── structured_kp.json
└── kp_judgment_<label>.md
```

不得运行标准 `build_prashna_data.py`，也不得读取 `structured_prashna.md`。
`structured_kp.md` 必须显示用户原问题、KP number 和 topic，防止号码盘脱离问题
语境后被误用；同时显示 outcome scope 的白话定义和明确排除的低门槛结果。
判盘时刻必须保留秒和可用的小数秒；不得把 `now` 截断为整分钟。

技术口径：

1. 用 Vimshottari 比例把每个 nakshatra 分九 sub；
2. 在 sign 边界进一步切分，得到 249 个 sign/star/sub 区；
3. 用户号码取对应区间起点为 Nirayana Ascendant；
4. 用 Krishnamurti ayanamsa 转为 tropical Ascendant；
5. 按判盘地纬度求 Placidus cusps，再扣回 Krishnamurti ayanamsa；
6. 行星取判盘时刻；Rahu／Ketu 使用 Mean Node；
7. 第一 cusp 位于号码区间精确起点是定义，不判输入敏感。

进入下一阶段条件：249 表已知边界、Asc 求解、12 cusps 和 ayanamsa 自检通过。

---

## Phase KP-2：Significator chain

对每颗行星完整建立：

| 强度 | 规则 |
|---|---|
| A | 行星位于某宫 occupant 的 star |
| B | 行星自身占据该宫 |
| C | 行星位于该宫 owner 的 star |
| D | 行星自身为该宫 owner |

Node 代理按 Reader VI 的原文次序维护：

1. 合相行星；
2. node 所在 constellation 的 lord；
3. 照射 node 的行星；
4. node 所在 sign 的 lord。

当前可确定地启用第 2、4 项。Reader I 的 applying／separating 表只笼统写
“other planets”，没有明确把无实体的 Rahu／Ketu 包含进去；Reader VI 的逐星数值
表同样没有 Rahu／Ketu。出版例盘又证明旧版固定 `3°` 会漏掉明确写作合相的
Sun–Rahu。因此第 1、3 项继续失败关闭，不能把“other planets”推断成 node 数值，
也不能用自造 orb 解除。

Node 自身的 star-lord 链与第 2 项的完整代理结果都保留；第 4 项随后加入。行星落在
node star 时，必须继续取得该 node 已启用代理行星的宫位结果，不能在 node 自身占宫
处截断。

当前不实现合相／相位对普通 significator 的第五级扩展；不得让模型凭印象补写。

`NODE_AGENT` 是代理来源标签，不是虚构的“第五强度”。输出排序继承被代理证据的
A／B／C／D 等级；当前不对“node 比星座主更强”的原文另造数值倍数。

进入下一阶段条件：每颗星的 occupancy、ownership、star-lord occupancy／ownership
和 node agent 都可回查。

---

## Phase KP-3：Cusp sub-lord promise

1. 读取题型的判断 cusp；
2. 取得该 cusp 的 sub-lord；
3. 取得该 sub-lord 所落 constellation 的 lord；
4. 读取该 constellation lord 的完整 significator houses；
5. 按题型分别执行正向／反向宫组的 `all`／`any` 条件，不得把“同时关联”降成
   “命中任一”；
6. 另列 cusp sub-lord、constellation lord、position sub-lord 的 temporary
   retrograde materialization gate。

禁止把 cusp sub-lord 自身的全部 A／B／C／D 宫位直接混成 promise 投票。Reader VI
的句式是“cusp sub-lord 落在某星宿，而该星宿主是目标宫 significator”。

机械状态：

| 完整条件 | 状态 |
|---|---|
| 正向完整成立、反向不成立 | `promised_candidate` |
| 正向不成立、反向成立 | `denied_candidate` |
| 正反完整条件同时成立 | `mixed` |
| 正反完整条件都未成立 | `unsupported` |

若相关 temporary-retrograde gate 阻塞，保留方向但输出
`positive_indication_blocked`、`negative_indication_blocked` 或
`mixed_with_retrograde_block`，不得把“负向事件未能落实”偷换成正向 promise。

若 operative promise 路径的 constellation／star／agent 任一环穿过 Rahu／Ketu，
当前因 node 合相／相位代理尚未完成，输出 `incomplete_node_agency`，不得用不完整
代理链宣布 promise 或 denial。

这些状态在例盘验证完成前仍是实验结果，不得改写成宿命式断语。

禁止使用统一的“相关宫＝成、6/8/12＝不成”。例如房产投资的原生规则可能把
12宫列为正向输入，证明 blanket dushtana 规则不成立。

---

## Phase KP-4：Ruling Planets

按顺序取：

1. 判盘时刻 Asc star lord；
2. Asc sign lord；
3. Moon star lord；
4. Moon sign lord；
5. day lord；
6. 通过当前可核证代理代表上述基础 RP 的 Rahu／Ketu。

Day lord 按当地**日出到次日日出**换日，不按民用午夜换日。

若 ruling planet 位于逆行星的 star，列入 rejected，不用于后续筛选。此规则只检查
Mars、Mercury、Jupiter、Venus、Saturn；Reader VI 明确说 Rahu／Ketu 不按
temporary retrograde 处理，因此不得因为 node 的正常逆向运动而剔除其 star 内的
ruling planet。

Ruling Planets 既输出筛选表，也只在 KP-5 内与事件 significators 取交集。Node
只有在当前可核证的 constellation／sign-lord 代理能代表基础 RP 时加入；不得使用
尚未闭合的 node 合相／相位槽扩张 RP。

---

## Phase KP-5：边界与 Timing

每个 cusp 和行星必须输出距最近：

- sign boundary；
- star boundary；
- sub boundary

的角分距离。5′ 内列入敏感点，但第一 cusp 的号码定义边界除外。

Timing 只在 `directional_status` 为 `positive_only`、temporary-retrograde gate 清空且 operative
路径不穿过未闭合的 node contact agency 时运行：

1. 以判盘时刻 Moon 在当前 nakshatra 已行比例计算 Mahadasha balance；
2. 同一 Vimshottari 比例递归取得 Bhukti／Antara／Shookshma；
3. 事件宫 significators 与已接受 Ruling Planets 取交集；
4. 搜索四级 period lord 均来自该交集的候选窗口；
5. 一月内用 Moon、超过一月用 Sun、以年计用 Jupiter；
6. 过运行星须进入 Ruling Planets 共同控制的 sign／star／sub 区间。

状态必须显式区分：

- `candidate`：四级 period 与过运候选同时成立；
- `blocked_node_agency`：promise 路径穿过未闭合的 node contact 槽；
- `blocked_temporary_retrograde`：方向保留，但暂不落实；
- `not_authorized_without_positive_promise`：没有正向 promise，不硬给日期；
- `no_rp_significator_intersection`：RP 与事件 significator 无交集；
- `no_four_level_period_within_horizon`：12 年搜索内无四级共同 period；
- `period_candidate_without_transit_entry`：有 period，无对应过运入口。

这是 KP 独立 timing。不得借用标准层 Moon ingress、提问盘之外的 natal Dasha，或
把它写入 Parashari 判读单。

---

## Phase KP-6：人类可读判读单

每次运行同时生成 `kp_judgment_<label>.md`，固定包含：

1. 问题、KP number、topic、秒级判盘时刻和地点；
2. 无需理解 KP 术语即可看懂的结论、主要支持、主要阻力和 timing 权限；
3. 先把正反宫命中翻译为该题型的现实支持／阻力，再在技术附录列判断
   cusp、sub-lord、star-lord 和原始宫位；
4. temporary retrograde 与 node agency 门控；
5. Ruling Planets／period／transit timing 状态；
6. 实验状态与“不换算为标准层三档”的边界。

`mixed` 必须写成正反完整条件同时成立、当前题型又没有来源支持的优先裁决规则，
不能压缩成“有机会也有阻力”或含糊的“可能”；失败关闭状态不能被模型补全。
“先说人话”一节固定先写“当前偏向／关键理由／现实含义／能否给时间”，不得出现
cusp、sub-lord、RP、period、宫位号、机械状态码或生产状态；这些全部放进可跳过
的技术附录。机械状态码、英文缩写和生产状态不得代替开头的人话回答。进入完成
条件：判读单每一项都能回查 `structured_kp.json`。

---

## 进入可用状态的门

标题在以下测试全部通过前必须保留“实验栈”：

- Reader VI 的 number 48 = Gemini 8°40′、Rahu star、Jupiter sub；
- number 74 = Cancer 14°53′20″、Saturn star、Jupiter sub；
- 249 个区间连续、无重叠、覆盖 360°；
- 1969／1970／2000 Krishnamurti ayanamsa 表；
- number Asc → Placidus cusp 已知例；
- A/B/C/D significator 强度；
- node constellation／sign-lord agent 正反例与顺序；
- node conjunction/aspect agent 的原典 orb、相位政策及正反例；
- 两个已实现题型的 promise／deny／mixed／unsupported；
- Reader VI number 156 的合作延续 known-answer；
- 婚姻重聚各语义的独立方法路由；若进入本 1–249 栈，必须取得含用户 number、
  判盘时刻、地点、cusp promise 与 known answer 的出版例盘；
- Ruling Planets 顺序、日出换日与逆行过滤；
- star/sub/sign 边界两侧；
- Horary Moon balance、Bhukti／Antara／Shookshma 边界；
- Reader VI p.134 的 Jupiter sub／Venus sub-sub 边界敏感例；
- RP ∩ event significators、四级 period、Moon／Sun／Jupiter 过运；
- Timing 的 promise、node、逆行与无交集失败关闭。
