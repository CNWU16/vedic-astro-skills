# Tajika 十六 Yoga overlay

## 定位

本层是默认关闭、与 Parashari 标准层隔离的 Tajika 副层。它按
*Tajika Nilakanthi* 的十六 Yoga 次序分类接触、传光、集光、阻断、接收与强弱修正。
它不改变标准层的“成／悬／不成”，也不与 KP 拼票。

只在用户明确要求 Tajika、Itthasala、applying/separating 或十六 Yoga 时运行。
必须先完成标准层 Phase 2，取得：

- 问者星：Lagna lord；
- 事项星：唯一主事项宫之主。

不得固定加入自然 Karaka；Moon 只按 Kamboola／Khallasara 等原规则进入。

---

## 来源边界

主要来源：

1. *Tajika Nilakanthi*, Samjnatantra, Sodasayogadhyaya 2.3–59：
   <https://archive.org/details/tajika_nilakanthi>
2. Martin Gansten and Ola Wikander, “Sahl and the Tājika Yogas: Indian
   Transformations of Arabic Astrology” (2011)：
   <https://doi.org/10.1080/00033790.2010.533349>

实现顺序固定为：

| # | Yoga | 本层判据 |
|---:|---|---|
| 1 | Ikkavala | 七曜均不在 cadent houses |
| 2 | Induvara | 七曜均在 cadent houses |
| 3 | Itthasala / Muthashila | deeptamsha 内正在应用或精确成相 |
| 4 | Isharafa / Musharipha | 已越过精确点并继续分离 |
| 5 | Nakta | 主星无直接接触；更快第三星从一方分离并向另一方应用 |
| 6 | Yamaya | 主星无直接接触；更慢第三星同时接收双方应用 |
| 7 | Manau | Mars／Saturn 在主 Itthasala 前抢先接触或形成原典包围条件 |
| 8 | Kamboola | 主星有 Itthasala，Moon 再向一方或双方应用 |
| 9 | Gairikamboola | Moon 处 Shunyamarga，但换座后向强星形成未来接触 |
| 10 | Khallasara | Moon 同时为 Shunyamarga，且与两主星都无 Itthasala／合相 |
| 11 | Radda | 接收方因逆行、停滞、失光、落陷、敌座等退回接触 |
| 12 | Duphalikuttha | 较快星弱、较慢星强的主 Itthasala |
| 13 | Dutthotthadivira | 弱主星由强第三星接援 |
| 14 | Tambira | 主星当前无接触，但换座后向强星形成未来接触 |
| 15 | Kuttha | Itthasala 参与星具原典强势条件 |
| 16 | Durapha | Itthasala 参与星具原典失能条件 |

这些分类是 Tajika 内部语义，不能迁入 KN Rao 兼容标准层。

---

## 计算契约

运行：

```bash
python scripts/build_tajika_overlay.py \
  --datetime "<YYYY-MM-DD HH:MM[:SS[.ffffff]]>" \
  --lat <lat> --lon <lon> --tz "<IANA>" \
  --querent-lord <planet> \
  --matter-lord <planet> \
  --out-dir "<existing prashna_* directory>"
```

只在当前标准盘目录增加 `tajika_overlay.md`。标准
`build_prashna_data.py` 不导入本模块，也没有 `--enable-tajika`。
overlay 必须沿用标准盘的原始秒级时刻和实际地点，不能用开始计算 Tajika 的时间。

几何与权限：

- 七曜参与；Rahu／Ketu 不参与；
- 相位为 0／60／90／120／180；
- 60／90／120 计算两侧分支；
- deeptamsha：Sun 15、Moon 12、Mars 8、Mercury 7、Jupiter 9、Venus 7、
  Saturn 9；
- 两星边界为 `(deeptamsha_A + deeptamsha_B) / 2`；
- 逆行保留在有符号相对速度中，再由 Radda／Durapha 等具体 Yoga 处理；
- 60／120 为友好相位；0／90／180 为敌意相位；
- Itthasala 只说明接触正在形成，敌意相位不得翻译成“顺利成事”；
- Kamboola 权限使用 Uttama／Madhyama／Sama／Adhama 四级交叉的 16 档；
- 权限输入限 D1 sign dignity、TNK Hadda、Drekkana、Navamsa 和相关 house；
- Khallasara 必须满足完整 Shunyamarga 条件，不是普通 Moon 无接触。

---

## 消费规则

| 配置 | 可说 | 不可说 |
|---|---|---|
| 友好 Itthasala | 双方存在较顺畅的靠近／接通趋势 | 单凭它把标准层改判“成” |
| 敌意 Itthasala | 接触正在形成，但伴随冲突或不协调 | 把“有接触”翻译成“顺利成” |
| Isharafa | 接触已经越过高点 | 自动等于永久不成 |
| Nakta／Yamaya | 可能经中间人传递或由第三方收集双方力量 | 主星已有直接接触时重复叠加 |
| Manau | Mars／Saturn 的抢先阻断候选 | 未核先后次序就断言一定阻断 |
| Kamboola | Moon 对主接触的分级增强候选 | 不显示 16 档权限就称“最强” |
| Gairikamboola／Tambira | 换座后的未来接触候选 | 当成已经发生的接触 |
| Khallasara | Tajika 内对 Kamboola 的缺失修正 | 写成 Parashari 空亡或全局否决 |
| Radda | 接收方退回，并保留先成后坏／先坏后成次序 | 把所有弱势都压成同一句失败 |
| Duphalikuttha／Dutthotthadivira | 主接触中的强弱不对称或第三星援助 | 覆盖更具体的 Radda 结果 |
| Kuttha／Durapha | Itthasala 参与星的承事能力或失能 | 当作独立于接触的全盘吉凶 |

若主星对无接触，只能写：

> 本 Tajika overlay 未检出 deeptamsha 内的主星直接接触；继续检查
> Nakta／Yamaya／Tambira 等原典条件。副层不改变标准结论。

`tajika_overlay.md` 是本副层的人类可读判读单，固定先显示：

1. 原始时刻和地点；
2. 一段无需术语即可理解的过程结论；
3. 直接接触、间接帮助或阻力的白话含义；
4. timing 是否可用及原因；
5. 十六 Yoga 完整表及可回查明细。

不得只输出布尔表，不得让 Yoga 名称先于其白话翻译，也不得生成标准层
“成／悬／不成”。“先说人话”一节不得出现 deeptamsha、Yoga 名称、英文状态码
或只写行星／相位而不解释现实意义；这些全部移入可跳过的技术核对区。

---

## Timing

只有主星对形成直接 Itthasala 时，允许显示
`度差 × 12 日` 的 *Tajika Nilakanthi* 原典比例候选。必须同时写：

- 这是原典比例候选，不是天文保证；
- 只属于 Tajika 副层；
- 不进入 Parashari 标准层；
- 无直接主星 Itthasala 时，timing 为 `unavailable`。

---

## 进入可用状态的门

当前实现覆盖十六 Yoga，但在出版例盘套件全部完成前仍标
`experimental_pending_published_example_suite`。至少验证：

- 0／60／90／120／180 两侧分支；
- applying、exact、刚过 exact、Isharafa；
- direct／retrograde 的有符号速度；
- Ikkavala／Induvara 的完整与缺输入边界；
- Nakta／Yamaya／Manau 的正反例与先后顺序；
- Kamboola 16 档、Shunyamarga、Gairikamboola、Khallasara；
- Radda 与 Durapha 的优先级及先成后坏／先坏后成；
- Duphalikuttha／Dutthotthadivira／Tambira／Kuttha；
- 主星相同、Moon 为主星、sign／Hadda／Drekkana／Navamsa 边界；
- 两张固定出版盘回归；
- `度差 × 12 日` 的正反例与禁用条件。

当前已锁定一张出版接触几何回归：Journal of Astrology article 153
（1994-06-11 18:45 IST），可复算公开盘的 Scorpio 20°08′ 上升、Mars Aries
20°02′ 与 Saturn Aquarius 18°30′，并复现原文所称 Mars–Saturn Tajik sextile。
原页面没有单列 Prashna place；Delhi 坐标虽可复现公开 Lagna，仍不能把这个推断
冒充完整出版输入。因此它只闭合接触几何，不独立满足“两张完整固定出版盘”或出版
timing 正反例门。
