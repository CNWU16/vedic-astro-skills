# Prashna 时间副层（timing layer）

> **用途**：标准层定档后，给“成”和“悬”两档补一个有原典出处的时间候选。
> 时间副层不进规则账本，不改三档结论，也不因时间远近升降档。
>
> **先读**：`standard-layer.md`、`judgment-rubric.md`。本文件只管时间。

---

## 1. 定位与准入

- 来源只有两类：*Prasna Marga* XIV.81／82／85（Raman 译注，标签 `M`）和
  *Shatpanchasika* V.5（Ayer 译本，标签 `P`）。`M` 在这里只是一个独立的时间模块，
  不进入成败判读。
- `standard-layer.md` 要求时间模块具备来源范围、完整算法、例盘和边界测试四项。
  本模块对应：§2 的来源和算法；Raman 注的两个算例和 Moon 入座搜索已写进
  `tests/test_prashna_isolation.py`。
- 按结论档呈现：
  - **成**：给时间，写“约……”；
  - **悬**：写“如果能成，大约……”；
  - **不成**：不给时间，不运行脚本。

---

## 2. 四个时间候选

| 代号 | rule_id | 算法 | 角色 |
|---|---|---|---|
| T1 | `P-V.5` | 从 Lagna 顺数到第一个有七曜的宫，宫数 × 12 天 | 归来／到达题的主时间 |
| T2 | `M-XIV.85` | 从事项宫数到其宫主所在宫（含首尾）；宫主在 7–12 宫按天，在 1–6 宫按月 | 其余题型的主时间 |
| T3 | `M-XIV.85` | Moon 下次进入事项宫主所在的星座 | 最近的触发日 |
| T4 | `M-XIV.82` | 上升 Navamsa 主星的时间单位 × 该星在本座第几个 Navamsa | 只作参考 |

**T1（P-V.5）**
- 原文：“Count the number of rasis from the lagna to the house first occupied by a
  planet; multiply the number by twelve… days for the person to arrive.”
- Lagna 本身有星算 1。只数七曜，Rahu／Ketu 不计。原文“若逆行”后半句不用。
- 只用于人的归来／到达题。

**T2（M-XIV.85）**
- 宫数 = `((宫主落宫 − 事项宫) mod 12) + 1`，含首尾。
- 原文只说宫主在可见半球应事快、在不可见半球应事慢。“7–12 宫按天、1–6 宫按月”
  是 Raman 注的假设（“It is to be assumed…”），输出时要注明。
- Raman 算例：7 宫主 Sun 在 6 宫（不可见半球），含首尾相隔 12 个星座，所以婚事
  约在 12 个月内。

**T3（M-XIV.85）**
- 原文：“when the Moon next transits the sign occupied by the lord of the
  concerned Bhava”。Raman 算例中 Moon 约 24 天后进入该星座。
- 提问时 Moon 已在该星座：取下一次重新进入，并注明“提问时已在该座”。
- 事项宫主就是 Moon：这一条是自指，不适用，不能硬算。

**T4（M-XIV.82，单位来自 XIV.81）**
- 时间单位（Raman 注，引 *Brihat Jataka*）：Sun 6 个月（Ayana）、Moon 48 分钟
  （Kshana）、Mars 1 周（Vasara）、Mercury 2 个月（Rithu）、Jupiter 1 个月
  （Masa）、Venus 半个月（Ardha）、Saturn 1 年（Sama）。
- 第几个 Navamsa 取 1–9。Raman 算例：上升 Navamsa 为 Leo，主星 Sun 在第 5 个
  Navamsa，结果是 5 × 6 = 30 个月。
- 主星为 Moon 时照实输出，并注明“对需要过程的事项通常过短”。
- 只作参考，不能和主时间折中。

---

## 3. 定序与呈现

1. 归来／到达题以 T1 为主时间，其余题型以 T2 为主时间。
2. T3 给出具体日期，作为最近的触发日。XIV.85 的 Raman 注引 Bhattotpala：原文的
   “或”表示先看宫数、再看 Moon 过境的次序。
3. T4 只作参考。
4. 几个候选结果不同时并列呈现，不平均、不投票、不折中。

---

## 4. 各题型的事项宫

`--matter-house` 默认取 Phase 2 已选的主事项宫。下列题型按本表：

| 题型 | `--matter-house` | `--mode` |
|---|---:|---|
| 能否复合／和好／复婚；对方会否联系／回复 | 7 | `general` |
| 我主动挽回能否成 | 1 | `general` |
| 在外的人或失踪者会否回来 | 7 | `return`（T1 为主） |
| 已搬走的伴侣会否回来同住 | Phase 2 主事项宫 | `return`（T1 为主） |
| 找工作／offer／面试／升职 | 10 | `general` |
| 会否被裁／调岗／换工作；能否保住工作 | 1 | `general` |
| 失物；走失宠物能否找回 | 11 | `general` |
| 买房／置产；名誉能否保住；官司会否很快开庭 | 4 | `general` |
| 出行／出国 | 10 | `general` |
| 病能否好 | 1 | `general` |
| 谈判／和解 | 7 | `general` |
| 投资；生意亏损能否补回 | 11 | `general` |
| 考试 | 官方已公布出结果日程：不运行，写“以官方公布为准”；未公布：1 | `general` |
| 描述题、天气、胎儿性别、父亲下落 | 不运行 | — |

---

## 5. 运行

```bash
python scripts/build_timing_overlay.py \
  --datetime "<与标准 builder 完全相同>" \
  --lat <lat> --lon <lon> --tz "<IANA>" \
  --matter-house <1-12> --mode general|return \
  --verdict favorable|pending \
  --out-dir "<当前 prashna_* 目录>"
```

- `--datetime/--lat/--lon/--tz` 必须与标准 builder 完全一致，不能另取处理时刻。
- `--verdict`：`favorable` 对应“成”，`pending` 对应“悬”。“不成”不运行。
- 产物是当前 `prashna_*` 目录下的 `timing_overlay.md`，不改 `structured_prashna.md`。

---

## 6. 不收与禁止

- 不收：*Prasna Marga* XIV.83／86／88、一年／一月 Prasna Dasa；*Shatpanchasika*
  II.14–17。
- 不使用提问盘生成的 120 年 Vimshottari、Chara Dasha、过运或 Sade Sati。
- 不导入 Tajika 的“度差 × 12 日”，也不导入 KP 的时间。不同体系的时间不互相
  校正；用户开了 Tajika 时，主答案以判读单 §四 为准。
- 不把时间写进规则账本，不因时间远近改档。

---

## 7. 自检

- [ ] 结论是成或悬？不成档没有给时间？
- [ ] 主时间按题型选对了 T1 或 T2？
- [ ] T2 注明了天／月分法是 Raman 的假设？
- [ ] T3 处理了“提问时已在该座”和“宫主即 Moon”两种情况？
- [ ] T4 只作参考，没有和主时间折中？
- [ ] 几个候选结果不同时是并列呈现的？
- [ ] 没有混入 Dasha、过运、Tajika 或 KP 的时间？
- [ ] 描述题、天气、胎儿性别、父亲下落没有运行时间副层？
