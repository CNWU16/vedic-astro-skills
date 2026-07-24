---
name: vedic-prashna
description: 吠陀占星提问盘/时盘(Prashna)分析与追问引擎。接收一个具体问题、秒级提问时刻和地点，以 Shatpanchasika 为主文本并经 KN Rao/Bharatiya Vidya Bhavan 兼容性筛选的古典 Prashna 标准层回答当前成败倾向；也处理既有即时盘的澄清、细化和跨栈追问。Tajika contact overlay 与 KP 1–249 Horary 默认关闭，计算与结论互相隔离。当用户提到“卜卦”“即时盘”“时盘”“Prashna”“起一卦”“我现在想问”“这个盘为什么”“继续看这个盘”等具体占问或追问时触发；不用于本命盘人生趋势。
---

# Vedic Prashna

## 定位

用一个具体问题产生时的时间和地点建立独立提问盘。默认层是：

> *Shatpanchasika*-rooted classical Prashna，经 KN Rao／Bharatiya Vidya Bhavan
> 实践兼容性筛选。

不要把它写成“KN Rao 自创的完整 Prashna 体系”。KN Rao 的公开材料支持谨慎使用
Prashna、有限 snapshot 实例及其对 *Shatpanchasika* 的认可，但不支持把他的本命
Jaimini、Dasha、分盘或 SAV 工具自动迁入提问盘。

默认层回答：

- 当前证据支持“成／悬／不成”哪一档；
- 吉凶条件和现实建议；
- timing 模块是否可用。

当前默认层**不提供生产级事件日期**。

---

## 每次执行必须读取

按顺序完整读取：

1. `resources/standard-layer.md`：来源标签、准入、白名单；
2. `resources/question-taxonomy.md`：单问与 A／B／C 支持级；
3. `resources/house-karaka-map.md`：一个主事项宫和专题入口；
4. `resources/judgment-rubric.md`：适用规则账本和三档组合；
5. `resources/moon-policy.md`：Moon 当前事实的使用边界。

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
   `structured_prashna.md` 和 `prashna_judgment_<label>.md`。显式 Tajika overlay
   只在该目录增加 `tajika_overlay.md`。KP 只写入独立
   `kp_horary_<yyyymmdd_HHMMSS>_<label>/`，文件名 `structured_kp.md`、
   `structured_kp.json` 和 `kp_judgment_<label>.md`。
5. 不读取或写入 `user_context.md`。
6. Tajika／KP 计算只存在本 skill；标准 builder 不导入两者，也不接受 optional
   flag。
7. 不读取其他 `prashna_*` 目录；追问只沿用当前盘。

---

## 默认层禁入项

不得消费或输出：

- Chara Karaka、DK、UL、AL；
- SAV／BAV、Shadbala、Bhava Bala；
- 完整 D9、D10、D4、D5 等本命分盘；
- functional P1 身份、natal yoga prescan；
- 120年 Vimshottari、Chara Dasha；
- transit、Sade Sati、double transit；
- Tajika orb／applying／separating；
- KP cusp／sub-lord。

只允许 rising Navamsa 这一项有限数据，因为 `P-I.4` 明确使用 rising Navamsa；
禁止由此展开完整 D9 解读。

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
7. 同一问题和现实状态未变化时沿用第一次清晰提问盘，不使用24小时／3个月阈值。

进入下一阶段条件：问题唯一、支持级为A或B、时间地点完整。

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
- 时间／地点是否只是近似。

若输入误差可能改变 Lagna 或 rising Navamsa，标记 `输入敏感` 并取得更准确输入；
不能声称城市中心近似必然不影响结论。输入敏感性只影响实际消费该字段的规则；
若本题账本不使用 rising Navamsa，须分别写“该字段敏感”和“主结论所用 D1 结构
是否稳定”，不得把两者合成一个模糊置信度。

进入下一阶段条件：产物存在、默认白名单无越权字段、敏感性已处理或明确降置信度。

---

## Phase 2：主事项宫与适用规则

1. 从 `house-karaka-map.md` 选择一个主事项宫；
2. A级定位题目专属 `P` rule_id；
3. B级只使用通用宫／宫主规则和明确匹配的 Bhavan 辅证；
4. 始终保留 Lagna 与 Lagna 主；
5. Moon 只在专题规则明确需要时成为主输入；
6. 不固定加入自然 Karaka、Moon 月宿主或 Chara Karaka。

建立并在聊天和判读单中完整显示：

| rule_id | 支持级 | 适用理由 | 原始证据 | 方向 | 权重 | 冲突 |
|---|---|---|---|---|---|---|

规则账本只消费 `structured_prashna.md` 白名单。没有 rule_id 的解释不能进入结论。

进入下一阶段条件：至少一条适用主规则，所有规则有范围和原始字段，没有 `U/M/T/KP`
混入默认账本。

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
- Moon ingress 承担 Dasha 或事件 timing。

进入下一阶段条件：Moon 每条判断都说明适用 rule_id，或明确标为背景。

---

## Phase 4：三档结论

严格按 `judgment-rubric.md`：

- **成**：适用主规则有利，一般宫／宫主规则同向或仅轻度混合；
- **悬**：混合配置、来源级不足或输入敏感；
- **不成**：至少两条独立适用主规则偏不利，其中至少一条来自 `P`，且无同级救援。

单一行星、单一宫位、单一缺失或单一强弱因素不得全局否决。

输入敏感只有在可能改变本题账本实际使用的 Lagna、rising Navamsa、事项宫或宫主
结构时才能影响档次。未被本题规则消费的临界字段只报告，不改票。

成败档次与 timing 状态分开。没有 timing 模块不自动把“成”降为“悬”。

进入下一阶段条件：结论可从已显示账本逐条复核。

---

## Phase 5：Timing

默认固定输出：

> 当前标准层未启用生产级 Prashna timing。本盘只回答当前支持方向，不使用提问盘
> 生成的120年本命 Dasha、Moon ingress 或今日过运硬给日期。

*Prasna Marga* 的一年／一月 Prasna Dasa 属 `M` 来源，不因能纠正旧错误就自动并入
K/P/B 默认层。未来模块上线必须同时具备来源范围、完整算法、例盘和边界测试。

---

## Phase 6：输出

写入 `prashna_judgment_<label>.md`，并在聊天中显示支持级、规则账本、结论和
timing 状态。固定结构：

```markdown
# Prashna 判读单：<问题>

## 一、先说人话
**结论**：[成/悬/不成；紧跟普通语言解释]
**更可能发生什么**：<可观察结果，不写术语>
**主要阻力**：<现实含义，不写宫位或行星名称代替解释>
**现在能做什么**：<可执行建议>
**能不能给时间**：<可用/不可用及白话原因>

## 二、这张盘的范围
**提问时刻／地点**：
**来源支持级**：[A/B；说明这是来源覆盖，不是概率]
**输入稳定性**：[本题实际消费字段稳定/敏感及原因]
**体系状态**：[标准层/实验候选]

## 三、现实条件
**利好**：
**阻力**：
**建议**：

## 四、Timing 状态
当前标准层未启用生产级 Prashna timing。

## 五、适用规则账本
| rule_id | 支持级 | 适用理由 | 原始证据 | 方向 | 权重 | 冲突 |

## 六、Moon 当前事实
<专题输入或背景；说明 rule_id>

## 七、体系边界
默认层不含 natal Dasha/Chara Karaka/SAV/完整分盘/Transit/Tajika/KP。
```

语言要求：先说人话，再列证据；术语出现即翻译；不使用极端或宿命化措辞。判读单
开头必须让不懂占星的用户直接看懂“更可能发生什么、主要阻力是什么、现在能做什么、
能不能给时间”。“先说人话”一节禁止出现未经翻译的行星名、宫位号、`rule_id`、
Yoga 名称、`mixed`、`promise`、`cusp`、`sub-lord`、`Itthasala` 或生产状态码；
这些只能放在白话结论之后的核对区。不能用“混合配置”“支持级 B”或“实验候选”
代替事件结论，必须先说明它们在现实中意味着什么。

---

## Tajika 可选副层

默认关闭。只有用户显式要求 Tajika／Itthasala／applying-separating 时才读取
`tajika-optional.md`。

先完成标准层 Phase 2，取得 Lagna lord 和唯一事项宫主，再运行独立
`scripts/build_tajika_overlay.py`。不得在标准 builder 上增加
`--enable-tajika`。

当前实现按 *Tajika Nilakanthi* 2.3–59 输出十六 Yoga 分类，并保留
Uttama／Madhyama／Sama／Adhama 的 Kamboola 16 档、严格 Shunyamarga、
Radda／Durapha 优先级及换座候选。它仍是实验候选，不能进入默认主结论。
只有主星直接 Itthasala 才可显示原典“度差 × 12 日”比例候选；这不是天文保证，
也不得进入标准层。全部出版例盘与边界测试完成前不得解除实验标签。
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
标准层的“成／悬／不成”。判读单必须先回答“当前偏向什么、为什么、能否给时间”，
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
   时才回 Phase 0。

进入完成条件：每条回答能回查对应栈文件，未跨目录偷读，未用追问补造禁用 timing，
也未把跨栈比较写成一个新的混合占星结论。

---

## 最终自检

- [ ] 已完整读取五个默认资源？
- [ ] 支持级为A或B，且只选一个主事项宫？
- [ ] 默认产物由专用 formatter 生成？
- [ ] 规则账本完整可见，且没有 `U/M/T/KP` 越界？
- [ ] 未使用 Chara Karaka、SAV、完整分盘、本命 Dasha 或过运？
- [ ] Moon 无接触未被写成空亡或全局负分？
- [ ] 成败与 timing 状态分开？
- [ ] 输入敏感性已处理？
- [ ] 提问时刻是否保留秒级，且没有用处理时刻替代用户提问时刻？
- [ ] 标准／Tajika 产物是否只写入当前 `prashna_*`，KP 是否只写入独立
      `kp_horary_*`？
- [ ] 标准 builder 是否完全未导入 Tajika／KP？
- [ ] 若启用 KP，是否由用户给了 1–249 数字并使用独立 `kp_horary_*` 目录？
- [ ] KP 题型是否与用户确认的可观察结果一致，且未把回暖／联系改写成关系落实？
- [ ] Tajika／KP 是否都有可读判读，且未进入标准账本？
- [ ] 追问是否沿用当前盘；跨栈比较是否只并列、不拼票？
