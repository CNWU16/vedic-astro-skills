# 16条数学校验规则

> 用途：reader在Step 2执行，确保提取数据的数学一致性
> 所有校验不通过 → 标注问题 → 仅对低信心数据要求用户确认

---

## D1基础校验

### 校验1: SAV总分 = 337
如果有SAV数据，12宫SAV总和必须等于337。

### 校验2: BAV行常量
每颗星BAV行总和 = 固定值：
```
Sun=48, Moon=49, Mars=39, Mercury=54,
Jupiter=56, Venus=52, Saturn=39, Lagna=49
```

### 校验3: 行星完整性
9颗行星 + Lagna都已识别（不多不少）

### 校验4: 度数唯一性
没有两颗行星度数完全相同（除非合相，需标注）

### 校验5: Ra-Ke对冲
D1中Rahu和Ketu相差约180°（±1°容差）

### 校验6: 逆行标记
- Sun和Moon永远不逆行
- Rahu和Ketu通常永远逆行
- 所有逆行行星都已标注(R)

### 校验6b: 燃烧检测(Combustion)
检测每颗行星与Sun的度数差，按以下临界值判定燃烧：
```
Moon    < 12°  → 燃烧
Mars    < 17°  → 燃烧
Mercury < 14°  → 燃烧（逆行时 < 12°）
Jupiter < 11°  → 燃烧
Venus   < 10°  → 燃烧（逆行时 < 8°）
Saturn  < 15°  → 燃烧
```
- 距离 = 两星绝对经度差的最短弧（取min(差, 360-差)）
- 燃烧行星 → 在structured_data预分析中标注`[燃烧，距Sun X°]`
- **延迟补偿标注**：Venus和Saturn燃烧后解除（大运切换时），标注`[延迟补偿潜力]`

### 校验6c: 行星战争检测(Graha Yuddha)
检测任意两颗行星（Sun/Moon/Rahu/Ketu除外）是否距离 < 1°：
```
距离 < 1° → 行星战争
胜者 = 经度较小者（差 < 0.1° 时比较Shadbala）
败者 → 职能封锁/内耗
```
- 在structured_data预分析中标注`[战争，与X星距Y°，胜/败]`

### 校验7: Ayanamsa一致性
与用户声明一致

### 校验7b: Lagna敏感度数检查
```
Sandhi检查：
  Lagna度数在0°-1° 或 29°-30° → 标注[Sandhi-身份模糊]
  含义：上升点在星座边界，身份表达不稳定

Gandanta检查：
  Lagna在以下交界0°附近（水象→火象）：
    Cancer 29°~30° / Leo 0°~1°
    Scorpio 29°~30° / Sagittarius 0°~1°
    Pisces 29°~30° / Aries 0°~1°
  → 标注[Gandanta-业力结节]
  含义：出生时Lagna在"灵魂搅拌区"，人生有深层重塑主题
```
- 在structured_data预分析中标注

### 校验7c: 盈月/亏月判定
```
计算：Moon绝对经度 - Sun绝对经度（负数加360°）
  差值 0°~180° = 盈月(Shukla Paksha) → Moon为天然吉星
  差值 180°~360° = 亏月(Krishna Paksha) → Moon为天然凶星

进一步细分：
  差值 > 150° = 接近满月，Moon最强
  差值 < 30° = 接近新月，Moon最弱(暗月)
```
- 在structured_data预分析中标注`[盈月/亏月，距Sun X°]`
- 此标注直接影响core P1审计中Moon的天然属性判定

### 校验7d: 分盘输入稳定性（与直接计算正确性分开）

按Step 3确定的“有效精度”对报时前后区间逐分钟重算D1、D9、D10、D4、D5
Lagna；calculator路径直接读取其`divisional_boundary_audit`。逐项记录：

- 审计区间内Lagna不变 → `✅ 稳定`；
- 任一换座 → `⚠️ 边界敏感`，列出两侧候选与首次换座偏移；
- 旧数据或非calc路径无法扫描 → `⚠️ 未审计`，不得写成稳定；
- 出生证/医院记录只影响来源可靠度，不替代本项；
- D1远离0°/30°也不替代本项，因为D9等分盘可以在D1星座内部换座。

边界敏感时，分盘行星星座/尊贵度若在候选间未变可继续引用；以分盘Lagna为起点的
落宫、内部宫主、房东、承载与事件形态全部必须按候选分支或降级。校验结果写入
structured_data的“分盘可信度声明”和校验7d。

---

## Nakshatra校验

### 校验8: Nakshatra↔度数一致
每个Nakshatra跨13°20'(13.333°)，从Ashwini(0°Aries)开始。

公式：`绝对经度 ÷ 13.333 = Nakshatra编号(从0开始)`

27 Nakshatras顺序：
```
0.Ashwini  1.Bharani  2.Krittika  3.Rohini  4.Mrigashira
5.Ardra  6.Punarvasu  7.Pushya  8.Ashlesha  9.Magha
10.P.Phalguni  11.U.Phalguni  12.Hasta  13.Chitra  14.Swati
15.Vishakha  16.Anuradha  17.Jyeshtha  18.Moola  19.P.Ashadha
20.U.Ashadha  21.Shravana  22.Dhanishta  23.Shatabhisha
24.P.Bhadrapada  25.U.Bhadrapada  26.Revati
```

Pada = `(度数在Nakshatra内的位置) ÷ 3.333 + 1` (结果1-4)

---

## Chara Karaka校验

### 校验9: Chara Karaka度数排序
必须按度数从高到低排列：
`AK(最高) > AmK > BK > MK > PK > GK > DK(最低)`

注：只看度数在星座内的位置(0-30°)，不看绝对经度
注：Rahu用30°减去度数（反向计算），仅8K体系参考时参与排序

> 以上为7K体系排序（KN Rao）。8K体系加入Rahu仅作参考。

---

## Dasha层级与连续性校验

### 校验10: MD/AD/PD完整性 + 大运时长常数
```
Sun=6年, Moon=10年, Mars=7年, Rahu=18年, Jupiter=16年,
Saturn=19年, Mercury=17年, Ketu=7年, Venus=20年
总计=120年
```

相邻大运日期间隔必须等于对应行星的固定年数。
注：第一个和最后一个大运可能不完整（出生时已过一部分）

calc路径另必须同时满足：
```
MD段数 = 9
AD段数 = 81
PD段数 = 729
每层相邻区间均按 [start,end) 无缝连续，无断裂、无重叠
每个MD下有9段AD；每个AD下有9段PD
```

任一不通过 → 标注`Dasha层级校验失败`，停止所有PD月级判定。
非calc兜底路径按实际提取到的层级校验并明示降级；禁止用比例或365.25天补齐缺失层。

---

## D9校验

### 校验11: D9公式交叉验证
D9落宫必须与D1度数的Pada映射一致。
→ D9公式实测10/10准确，可作为可靠校验手段

---

## 分盘Ra-Ke校验

### 校验12: Ra-Ke分盘校验总表

```
★ = 必须读取   ○ = 可选

分盘    Ra-Ke规则            用途            读取          实测验证
────────────────────────────────────────────────────────────────────
D1  ★  必须对宫              基础盘           文本层(100%)  16/16
D9  ★  必须对宫              婚姻/灵魂        公式校验(100%) 16/16
D10 ★  必须对宫              事业/成就         calc engine   11/11*
D4  ★  必须对宫              财产/资产/舒适    calc engine   9/9*
D5  ★  必须同宫(⚠️!)        权力/创造力       calc engine   13/13
D2  ○  必须同宫†             财富(Hora)       calc/截屏     40/40(calc)
D3  ○  必须对宫              兄弟/勇气        calc/截屏     -
D7  ○  必须对宫              子女             calc/截屏     -
D12 ○  必须对宫              父母             calc/截屏     -
D30 ○  待验证                困苦/业障        calc/截屏     -
D60 ○  待验证                前世业力         calc/截屏     -

* D10/D4的"实测验证"排除了AI视觉读错的异常样本
† D2 按 JHora 打印的 "D-2 (US)"（Uma Shambhu Hora，与 calculator 同口径）：Ra-Ke 同宫，但可落任一星座。
  只有传统 Sun／Moon Hora 才只落 Cn 或 Le；截屏上的 D2 口径不明时不做本项校验。
```

**⚠️ D5同宫规则特别说明**：
D5(Panchamsha)中Ra和Ke在同一个星座，不是对宫。
这不是错误——D5的5分割法导致180°对冲的行星映射到同一分区。
已用13个JHora实盘全部确认。**不要"纠正"为对宫！**

通用读法：找到As(Lagna)→确定固定星座位置→逐格读行星
通用过滤：忽略A2-A12, AL, UL, GL, HL, SL, PP, BB, Md, Gk
通用纠错：边界行星倾向归入左侧格子

⚠️ 基于Mean Node校验。True Node极罕见弧秒级抖动时，
如度数在区间边界±0.01°内，标记"边界待确认"。
