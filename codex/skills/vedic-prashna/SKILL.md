---
name: vedic-prashna
description: 吠陀占星提问盘/时盘(Prashna)分析引擎。接收一个具体问题、提问时刻和地点，以 Shatpanchasika 为主文本并经 KN Rao/Bharatiya Vidya Bhavan 兼容性筛选的古典 Prashna 标准层回答当前成败倾向。Tajika contact overlay 与 KP 1–249 Horary 是默认关闭、互相隔离的实验沙箱。当用户提到“卜卦”“即时盘”“时盘”“Prashna”“起一卦”“我现在想问”等具体占问时触发；不用于本命盘人生趋势。
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
4. 标准产物只写入 `prashna_<yyyymmdd_HHMM>_<label>/`，文件名
   `structured_prashna.md` 和 `prashna_judgment_<label>.md`。显式 Tajika overlay
   只在该目录增加 `tajika_overlay.md`。KP 只写入独立
   `kp_horary_<yyyymmdd_HHMM>_<label>/`，文件名 `structured_kp.md`、
   `structured_kp.json` 和未来的 `kp_judgment_<label>.md`。
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
| 提问时刻 | 显式时刻，或用户说“现在” |
| 提问地点 | 城市或经纬；必须能确定 IANA 时区 |

执行：

1. 用 `question-taxonomy.md` 澄清单问；
2. 判 A／B／C 支持级；
3. C级停止，不硬套宫位；
4. “现在”必须在提问地时区捕获；
5. 地点／时区未知时澄清，不用机器时区代替；
6. A/B 二选一不得机械起两张同刻盘；
7. 同一问题和现实状态未变化时沿用第一次清晰提问盘，不使用24小时／3个月阈值。

进入下一阶段条件：问题唯一、支持级为A或B、时间地点完整。

---

## Phase 1：起盘与输入敏感性

运行：

```bash
python scripts/build_prashna_data.py \
  --datetime "<YYYY-MM-DD HH:MM|now>" \
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
不能声称城市中心近似必然不影响结论。

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

**提问时刻／地点**：
**支持级**：[A/B]
**输入敏感性**：[稳定/敏感及原因]

## 一、当前结论
**成败**：[成/悬/不成]
**置信度边界**：<来源级与输入边界>
**一句话理由**：<可回查 rule_id>

## 二、现实条件
**利好**：
**阻力**：
**建议**：

## 三、Timing 状态
当前标准层未启用生产级 Prashna timing。

## 四、适用规则账本
| rule_id | 支持级 | 适用理由 | 原始证据 | 方向 | 权重 | 冲突 |

## 五、Moon 当前事实
<专题输入或背景；说明 rule_id>

## 六、体系边界
默认层不含 natal Dasha/Chara Karaka/SAV/完整分盘/Transit/Tajika/KP。
```

语言要求：先说人话，再列证据；术语出现即翻译；不使用极端或宿命化措辞。

---

## Tajika 可选副层

默认关闭。只有用户显式要求 Tajika／Itthasala／applying-separating 时才读取
`tajika-optional.md`。

先完成标准层 Phase 2，取得 Lagna lord 和唯一事项宫主，再运行独立
`scripts/build_tajika_overlay.py`。不得在标准 builder 上增加
`--enable-tajika`。

当前实现明确限定为 Tajika sambandha/contact subset，不冒充完整 16 yoga。
它仍是实验候选，不能进入默认主结论或提供 timing；只有
Itthasala/Muthashila、Isharafa、Nakta、Manau、Kamboola、Khallasara、Radda
的出版例盘与边界测试完成后，才能解除该子集的实验标签。

---

## KP 独立栈

默认关闭。只有用户明确要求 KP／sub-lord 时才读取 `kp-optional.md`。经典 KP
Horary 必须由用户给出 `1–249` 数字；不得从时刻、文字或随机数代取。

KP 与 Tajika 互斥；KP 是独立判读栈，不运行标准 builder，也不与默认层拼票。
使用 `scripts/build_kp_horary.py` 生成独立 `kp_horary_*` 目录。当前已实现
Krishnamurti ayanamsa、number-derived Placidus cusps、A/B/C/D significator
chain、node 星座主 agent、Reader VI 已锁定的恋情落实／商业合作题型宫组、
Ruling Planets 和边界距离；婚姻重聚因原文存在多个不同语境而失败关闭。node 的
conjunction/aspect agency 与独立 timing 仍关闭，整栈不能标“生产级”。

---

## 本命交叉与追问

本命交叉默认关闭；用户明确要求且有可靠本命盘时才读取
`cross-natal-policy.md`。本命只读，不能把提问盘生成的本命式 Dasha 当作 Prashna。

已有盘追问不重起，读取 `qa_rules.md`，且只访问当前 `prashna_*` 目录。
若追问对象是 KP，则只访问当前 `kp_horary_*` 目录，不读取或拼接
`prashna_*`。

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
- [ ] 标准／Tajika 产物是否只写入当前 `prashna_*`，KP 是否只写入独立
      `kp_horary_*`？
- [ ] 标准 builder 是否完全未导入 Tajika／KP？
- [ ] 若启用 KP，是否由用户给了 1–249 数字并使用独立 `kp_horary_*` 目录？
