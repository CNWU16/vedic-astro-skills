# KP Horary 独立栈（1–249）

## 定位

KP 是与 Parashari 标准层互斥的独立体系，不是副证据。只有用户明确要求 KP，
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

当前支持：

| topic | 判断 cusp | 正向宫 | 反向宫 | 来源范围 |
|---|---:|---|---|---|
| `love-materialization` | 5 | 7、11 | 6、12 | 恋情能否落实 |
| `business-partnership-continuity` | 7 | 5、11 | 6、12 | 合作关系能否延续 |

题型必须按唯一的可观察结果选择。同一问题同时命中多个 topic 时，返回输入门重新
澄清，不在一张 KP 盘中合并宫组。

当前不自动支持 `marital-reunion`。Reader IV／VI 至少保留三个不同语境：

- “重聚并恢复家庭生活”使用 2、7、11 的事件 significators；
- “丈夫是否回来同住”先检查 11 cusp，并分别列 11、7、6 与 12、7、6；
- 离婚章节另把 reunion 写为 1、5、7、11。

这些不能拼成“7 cusp；2/7/11 对 6/12”的统一 promise 公式。拆出单义题型并完成
出版例盘测试前，入口必须失败关闭。

进入下一阶段条件：号码、题型、时刻和地点完整。

---

## Phase KP-1：独立起盘

运行：

```bash
python scripts/build_kp_horary.py \
  --datetime "<YYYY-MM-DD HH:MM|now>" \
  --lat <lat> --lon <lon> --tz "<IANA>" \
  --number <1-249> \
  --topic "<supported-topic>" \
  --question "<single observable question>" \
  --label "<kebab-case>" \
  --out-parent "<parent>"
```

输出：

```text
kp_horary_<yyyymmdd_HHMM>_<label>/
├── structured_kp.md
└── structured_kp.json
```

不得运行标准 `build_prashna_data.py`，也不得读取 `structured_prashna.md`。
`structured_kp.md` 必须显示用户原问题、KP number 和 topic，防止号码盘脱离问题
语境后被误用。

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

再建立 Rahu／Ketu agent：

- 所处星座主；
- node 自身的 star-lord 链仍保留。
- 行星落在 node star 时，必须继续取得该 node 所代理行星的宫位结果，不能在 node
  自身占宫处截断。

Reader VI 例盘也使用 node 对合相／相位行星的代理，但本阶段尚未从原典建立可复核
的合相 orb 和相位政策。因此：

- 合相／相位 agent 暂停，不进入 significator chain；
- 旧版 `3°` proximity 是实现约定，不是已核证原典阈值，已从判定权中移除；
- 当前只把星座主 agency 标为 operative。

当前也不实现合相／相位对普通 significator 的第五级扩展；不得让模型凭印象补写。

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
5. 与题型专属正向／反向宫组比较；
6. 另列 cusp sub-lord、constellation lord、position sub-lord 的 temporary
   retrograde materialization gate。

禁止把 cusp sub-lord 自身的全部 A／B／C／D 宫位直接混成 promise 投票。Reader VI
的句式是“cusp sub-lord 落在某星宿，而该星宿主是目标宫 significator”。

机械状态：

| 命中 | 状态 |
|---|---|
| 只命中正向 | `promised_candidate` |
| 只命中反向 | `denied_candidate` |
| 正反同时 | `mixed` |
| 都未命中 | `unsupported` |

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
6. 代表上述星座主的 Rahu／Ketu。

Day lord 按当地**日出到次日日出**换日，不按民用午夜换日。

若 ruling planet 位于逆行星的 star，列入 rejected，不用于后续筛选。此规则只检查
Mars、Mercury、Jupiter、Venus、Saturn；Reader VI 明确说 Rahu／Ketu 不按
temporary retrograde 处理，因此不得因为 node 的正常逆向运动而剔除其 star 内的
ruling planet。

Ruling Planets 当前只输出筛选表，不承担日期预测。

---

## Phase KP-5：边界与 Timing

每个 cusp 和行星必须输出距最近：

- sign boundary；
- star boundary；
- sub boundary

的角分距离。5′ 内列入敏感点，但第一 cusp 的号码定义边界除外。

固定输出：

> KP timing 尚未启用。不得借用标准层 Moon ingress 或 natal Dasha。未来上线必须
> 同时实现 horary Moon 的 Vimshottari balance、事件 significator 的
> Dasha/Bhukti/Antara、Ruling Planets 筛选、快慢过运分层和出版例盘测试。

---

## 进入可用状态的门

标题在以下测试全部通过前必须保留“实验栈”：

- Reader VI 的 number 48 = Gemini 8°40′、Rahu star、Jupiter sub；
- number 74 = Cancer 14°53′20″、Saturn star、Jupiter sub；
- 249 个区间连续、无重叠、覆盖 360°；
- 1969／1970／2000 Krishnamurti ayanamsa 表；
- number Asc → Placidus cusp 已知例；
- A/B/C/D significator 强度；
- node sign-lord agent 正反例；
- node conjunction/aspect agent 的原典 orb、相位政策及正反例；
- 两个已实现题型的 promise／deny／mixed／unsupported；
- Reader VI number 156 的合作延续 known-answer；
- 婚姻重聚各语义的独立 cusp／宫组与出版例盘；
- Ruling Planets 顺序、日出换日与逆行过滤；
- star/sub/sign 边界两侧；
- Timing 独立套件。
