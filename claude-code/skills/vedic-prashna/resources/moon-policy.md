# Moon 当前事实：标准层消费边界

> **用途**：消费 `calc_moon_vedic.py` 输出的 Moon 位置、月相和当前整宫接触。
> Moon 数据不生成“成／不成”，也不承担生产级事件择时。

---

## 1. 来源位置

Moon 在不同 Prashna 专题中有具体用途，但当前来源集不支持以下全局断言：

- “Moon 是所有问题权重最高的 significator”；
- “Moon 必须连接事项宫主，否则事情不成”；
- “Moon 月宿主是每题固定的第四 significator”；
- “无同宫、无 Graha Drishti 就是空亡”。

`B-article-153` 曾用 Lagna、Lagna 主、Moon 及月宿检查一张失踪者盘是否反映
问题；这是一个 Bhavan 单案例，只能作为**软验证候选**，不能扩展成全局硬门。

---

## 2. 数据契约

默认 `structured_prashna.md` 只含三组 Moon 数据：

### `moon_position`

| 字段 | 用途 |
|---|---|
| moon_sign / moon_house | 当前 D1 落点 |
| moon_nakshatra / moon_pada | 描述；专题规则或软验证明确需要时才消费 |
| moon_nakshatra_lord | 描述；不是固定 significator |

### `moon_contacts`

| 字段 | 用途 |
|---|---|
| conjunctions | 与 Moon 同整宫／同 sign 的行星 |
| graha_drishti_planets | 通过七曜整宫 Graha Drishti 照 Moon 的行星 |
| graha_drishti_details | 来源宫与照射类型 |

### `moon_strength_factors`

| 字段 | 用途 |
|---|---|
| paksha | 盈亏及 Sun–Moon 距离事实 |
| dignity | D1 尊贵度事实 |
| house | Moon 所在宫 |

这些字段只在适用规则账本中有明确 `rule_id` 和 `scope_match` 时产生方向。

---

## 3. 消费顺序

1. 先从 `question-taxonomy.md` 取得 A／B／C 支持级；
2. 读取该题型明确适用的 `P` 专题规则；
3. 专题规则明确使用 Moon 时，按原规则使用；
4. 只有 `B-article-153` 类型的题意验证需要时，才把月宿作为软验证；
5. 其余情况下只把 Moon 作为当前心理／状态背景，不加入主规则权重。

Moon 有接触也不自动有利；必须说明它接触了谁、为什么该行星在本题适用规则中
有意义。Moon 无接触只是一项事实，不自动记负分。

---

## 4. Chandra Kriya 纠错边界

*Prasna Marga* VIII.63–65 及 Appendix IV 的 Chandra Kriya 是按 Moon 在月宿内
已行弧度计算的 60 种 lunar actions，不是“Moon 无接触”。

当前默认层：

- 不计算 Chandra Kriya；
- 不借用 Tajika Khallāsara 或西方 Void of Course；
- 不把该 Kerala 技法并入 K/P/B 标准层；
- 只保留这段说明，防止再次制造假“空亡”字段。

---

## 5. Timing 边界

默认层不计算 Moon ingress。即使另行计算天文换宿／换座时刻，也不得：

- 写成 Vimshottari Dasha／Antardasha 切换；
- 单独写成事件发生日期；
- 用来替代尚未核证的 Prashna timing 模块。

---

## 6. 判读单写法

有专题意义：

> `[rule_id]` 明确使用 Moon；本盘 Moon 的 `<位置／接触／月相>` 对该规则构成
> `<有利／不利／混合>` 证据。

只有背景意义：

> Moon 当前位于 `<sign/house>`，与 `<planet>` 有／无整宫接触。当前没有来源允许
> 把这一事实单独升级为成败规则，因此只列背景。

---

## 7. 自检

- [ ] 是否先取得题型支持级和适用 `rule_id`？
- [ ] Moon 的每条判断是否说明原规则为何需要它？
- [ ] 是否没有把月宿主固定加入所有题型？
- [ ] 是否没有把“无接触”记为全局负分或盘无效？
- [ ] 是否没有输出 Moon ingress 事件应期？
- [ ] 是否没有混入 Chandra Kriya、Tajika 或西方 Void 语义？
