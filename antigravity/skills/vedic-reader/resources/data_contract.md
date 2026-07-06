# structured_data.md 数据契约

> 本文档定义了 structured_data.md 的数据标准。
> 数据由 vedic-calculator 或 vedic-reader 生成，由 core/career/love 消费。

## 数据源优先级

> **主数据规则：calculator > PDF/截图/文本提取。**
>
> 只要出生日期、时间、地点完整，`vedic-calculator` 生成的数据就是
> `structured_data.md` 的 canonical source。PDF、截图和文本提取用于交叉验证，
> 不覆盖行星位置、分盘、Dasha、SAV/BAV、宫主、尊贵度、相位、特殊点或过运。
>
> **唯一例外是 Shadbala：**
> - 始终先计算并保留calculator基准值；
> - PDF无Shadbala或提取失败时，直接写入calculator值；
> - 同一出生时间生成的PDF含有效Shadbala时，逐行与calculator对照，最终展示PDF值；
> - 两者不一致时，必须向用户提示，并标注“calc与PDF不一致；当前采用PDF”；
> - 两者一致时标注“PDF校验一致”，PDF缺失行继续使用calculator值；
> - 出生时间校准后，旧PDF Shadbala无效，只有新时间重排的PDF可覆盖。
> 所有字段为必须，除非标注[可选]。

---

## 元信息

```
出生日期: YYYY-MM-DD
出生时间: HH:MM
出生地点: [城市] ([经度], [纬度])
时间精度: [精确到分钟 / ±15分钟 / ±1小时 / 不确定]
时间来源: [出生证/医院记录 / 家人明确记忆 / 家人大概回忆 / 未追问]
夏令时: [⚠️ 出生时刻处于当地夏令时，报时已按"墙上钟时间"处理（实际UTC偏移+N:00）/ 否]（calc自动标注）
有效精度: [±分钟级 / ±5分钟 / ±15分钟 / ±1小时 / 不确定]（经来源修正后）
验证轨道: [轨道1-标准 / 轨道2-严格 / 轨道3-双Lagna]
读盘方式: [calc engine / JH表格 / 文本度数 / 视觉识别+用户确认]
Ayanamsa: [True Chitra / 其他]
Node模式: [Mean Node / True Node]
```

## 用户信息

```
性别: [男 / 女]
感情状态: [单身 / 恋爱中 / 已婚]
```

> ⚠️ 以下字段**不写入**structured_data.md，**必须写入 user_context.md**（不存在则创建；写入机制见 vedic-reader「user_context.md 使用限制 + 增量回写规则」）：
> - 职业状态
> - 核心关切/具体问题
> - 用户补充的人生事件
> - 特质类（配偶/职业/专业/家庭氛围/性格等校准证据）

## D1基础数据

### 行星位置
| 行星 | 星座 | 宫位 | 度数 | 逆行 |
|------|------|------|------|------|
| Lagna | [sign] | 1 | [deg]°[min]' | — |
| Sun | [sign] | [house] | [deg]°[min]' | [D/R] |
| Moon | [sign] | [house] | [deg]°[min]' | [D/R] |
| Mars | [sign] | [house] | [deg]°[min]' | [D/R] |
| Mercury | [sign] | [house] | [deg]°[min]' | [D/R] |
| Jupiter | [sign] | [house] | [deg]°[min]' | [D/R] |
| Venus | [sign] | [house] | [deg]°[min]' | [D/R] |
| Saturn | [sign] | [house] | [deg]°[min]' | [D/R] |
| Rahu | [sign] | [house] | [deg]°[min]' | R |
| Ketu | [sign] | [house] | [deg]°[min]' | R |

### Chara Karakas
| 排名 | Karaka | 行星 | 有效度数 | 说明 |
|------|--------|------|---------|------|
| 1 | AK | [planet] | [deg] | 灵魂指示星（core板块1/9, career Phase3引用） |
| 2 | AmK | [planet] | [deg] | 事业指示星（career Phase2引用） |
| 3 | BK | [planet] | [deg] | 兄弟指示星 |
| 4 | MK | [planet] | [deg] | 母亲指示星 |
| 5 | PK | [planet] | [deg] | 子女/恋爱指示星（love引用） |
| 6 | GK | [planet] | [deg] | 障碍指示星 |
| 7 | DK | [planet] | [deg] | 配偶指示星（love引用） |
| (8K参考) | — | Rahu | [30°-原始度数] | 仅8K体系参与，非主表 |

> **7K体系（主表 / KN Rao）**：Sun~Saturn 共 7 颗，按宫内度数降序
> 8K体系（参考 / Sanjay Rath）：加入Rahu（度数=30°-原始度数），产生 PiK
> DK以7K为准，8K仅标注参考

### DK (配偶指示星)
```
DK = [planet]（7K主用）
8K参考 DK = [planet]
```
> 下游消费：vedic-love 直接使用7K DK进行配偶画像分析
> 8K DK仅在婚姻专题中作为补充参考

### Jaimini 特殊点
| 点位 | 星座 | 宫位(从Lagna数) | 说明 |
|------|------|-----------------|------|
| AL (Arudha Lagna) | [sign] | [house] | 社会人设/外界形象（core板块8引用） |
| UL (Upapada Lagna) | [sign] | [house] | 婚姻/配偶来源（love引用） |

> 计算规则 (BPHS标准)：
> AL = 1宫主从1宫数X宫，再从1宫主数X宫（X=1宫主距Lagna的距离）
> UL = 12宫主从12宫数X宫，再从12宫主数X宫
> 例外：Arudha不可落在本宫(→取第10宫) 或对宫(→取第4宫)
> 数据来源：calc engine `special_points['AL'/'UL']` 或 JHora 图中 AL/UL 标记

### Nakshatra
| 行星 | Nakshatra | Pada | Nakshatra主 |
|------|-----------|------|-------------|
| Lagna | [name] | [1-4] | [planet] |
| Sun | [name] | [1-4] | [planet] |
| ... | ... | ... | ... |

## 量化数据

### Shadbala
| 行星 | Rupas | 百分比 | 排名 | 强弱 | IshtaPhala | KashtaPhala | calc基准 | 数据来源/校验 |
|------|-------|--------|------|------|-------------|--------------|----------|---------------|
| [planet] | [展示值] | [展示值]% | [rank] | [强/中/弱] | [val] | [val] | [calc rupas / pct] | [calc / PDF校验一致 / calc与PDF不一致；当前采用PDF] |

> 强: ≥150% | 中: 100-149% | 弱: <100%

> **⚠️ 数据来源优先级**：
> 1. **calc engine先行** → 始终先生成Shadbala基准；没有PDF时直接展示
> 2. **JHora PDF对照** → 同一出生时间下逐行比较；有PDF时展示PDF值
> 3. **差异可见** → 不一致必须提示用户，并保留calc基准供审计
> 4. PyJHora 底层 Shadbala 算法与 JHora 存在系统性偏差（分盘蝴蝶效应、aspect插值公式、日出折射等），
>    平均每颗行星偏差 1-2 rupas，个别可达 4 rupas。**排序基本正确，数值不精确。**
> 5. 下游（core/love/career）引用时，以**排序和强弱分级**为准，避免引用具体数值

### SAV (Sarvashtakavarga)

#### 原始值（按星座，用于校验）
| Ar | Ta | Ge | Cn | Le | Vi | Li | Sc | Sg | Cp | Aq | Pi | 总计 |
|----|----|----|----|----|----|----|----|----|----|----|----|----| 
| [n] | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | [n] | 337 |

#### 宫位映射（按宫位，供core/career/love直接使用）
> 映射公式: 第N宫 = 星座编号((Lagna星座编号 + N - 2) % 12 + 1)的SAV值
> Lagna星座: [sign]

| 1宫 | 2宫 | 3宫 | 4宫 | 5宫 | 6宫 | 7宫 | 8宫 | 9宫 | 10宫 | 11宫 | 12宫 |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|------|------|------|
| [n] | ... | ... | ... | ... | ... | ... | ... | ... | ...  | ...  | [n]  |

### BAV (Bhinnashtakavarga)
| 行星 | Ar | Ta | Ge | Cn | Le | Vi | Li | Sc | Sg | Cp | Aq | Pi | 行和 |
|------|----|----|----|----|----|----|----|----|----|----|----|----|------|
| Sun | | | | | | | | | | | | | 48 |
| Moon | | | | | | | | | | | | | 49 |
| Mars | | | | | | | | | | | | | 39 |
| Mercury | | | | | | | | | | | | | 54 |
| Jupiter | | | | | | | | | | | | | 56 |
| Venus | | | | | | | | | | | | | 52 |
| Saturn | | | | | | | | | | | | | 39 |

### Vimsottari Dasha
| 大运 | 行星 | 起始 | 结束 | 年数 |
|------|------|------|------|------|
| [当前标记→] | [planet] | YYYY-MM | YYYY-MM | [n] |
| ... | ... | ... | ... | ... |

### 各大运Antardasha表（全部MD，必须）

每个大运一节（calc路径由formatter自动输出）：

```
### [MD planet]大运 Antardasha（当前/下一/空）
| 小运 | 起始 | 结束 |
|------|------|------|
| [MD]-[AD planet] | YYYY-MM | YYYY-MM | [← 当前标记]
```

> 降级规则：非calc路径（PDF/截图/文本提取）提取不到AD时，
> 本节标注"AD未提取"——此时下游（验前事窄窗口、core子运表、QA时机类回答）
> 禁止输出年月级时间窗口，只允许到大运级；禁止按Vimsottari比例心算AD日期。

当前状态:
```
Mahadasha: [planet] (YYYY-MM ~ YYYY-MM)
Antardasha: [planet] (YYYY-MM ~ YYYY-MM)
```

### Chara Dasha 时间线（K.N. Rao，calc路径必须）
> 第二时间系统（Jaimini 星座大运，KN Rao 变体），由 calc chara_dasha.py 生成
> （实现经 JHora 双盘金标准 24/24 对照验证）。用途：时间窗口的双系统交叉验证。

```
### Chara Dasha 时间线（K.N. Rao，[顺行/逆行]）
| 大运座 | 起始 | 结束 | 年数 |
| [sign] | YYYY-MM-DD | YYYY-MM-DD | [N] |  [← 当前标记]
```

> 降级规则：非 calc 路径无此表时，下游禁止做"双系统确认"表述（只按单系统 Vimsottari 出，
> 措辞维持单系统档）；禁止凭通识心算 Chara Dasha。

## 预分析（calculator计算，core直接引用）

### 行星尊贵度（Compound Dignity / Panchadha Maitri）
| 行星 | 落座 | 座主 | 自然关系 | 临时关系 | 复合尊贵度 | 说明 |
|------|------|------|---------|---------|-----------|------|
| [planet] | [sign] | [lord] | [友/中性/敌] | [临时友/临时敌/—] | [旺/入庙/至友/友方/中性/敌方/死敌/陷] | [一句话] |

> 旺(Exalted)/入庙(Own)/陷(Debilitated)：直接确定，不需要算compound，"临时关系"列填"—"
> 其余情况：自然关系 + 临时关系 → 查Panchadha合成表得出复合尊贵度
> Rahu/Ketu：不参与临时关系，"临时关系"列填"—"，用先天状态

### 主要相位关系（西占度数相位·orb 制）
| 行星A | 行星B | 关系 | 度数差 | 影响 |
|-------|-------|------|--------|------|
| [p1] | [p2] | [合相/对冲/三合] | [deg] | [一句话] |

> 只记录5-8组最重要的关系

### Graha Drishti（吠陀行星相位·宫位照射）
| 行星 | 落宫 | 照射宫位 | 照到的行星 |
|------|------|---------|-----------|
| [planet] | [house] | [houses] | [planets] |

> ⚠️ 这是 graha drishti（星→宫照射，P10/格局互视/rectifier 第3层读本表、禁手推）；与上面「主要相位关系」(西占度数相位)是两套体系、别混。calc 已算(engine graha_drishti 字段)，此段缺失则降级禁手推。
> 口径：所有星→第7；Mars +4/8；Jupiter +5/9；Saturn +3/10；Rahu/Ketu 仅第7（无特殊相位，对齐底层 jhora）。Rahu 行带「（放大）」标记 = 相位放大/膨胀迷惑。

### 宫主表
| 宫位 | 领域 | 宫主 | 宫主落宫 |
|------|------|------|---------|
| 1 | 自我 | [planet] | [house] |
| 2 | 财富 | [planet] | [house] |
| ... | ... | ... | ... |
| 12 | 损耗 | [planet] | [house] |

## 分盘数据

### 分盘可信度声明
```
D1  ✅ 可信
D9  [✅/⚠️] [说明]
D10 [✅/⚠️] [说明]
D4  [✅/⚠️] [说明]
D5  [✅/⚠️] [说明]
```

### D9 Navamsha
| 行星 | D9星座 | D9宫位 | Vargottama | D9尊贵 | D9房东 |
|------|--------|--------|-----------|--------|--------|
| Lagna | [sign] | 1 | — | — | — |
| [planet] | [sign] | [house] | [是/否] | [旺/自庙/陷/友/敌/中性] | [座主] |

> D9尊贵(自然尊贵：旺/自庙/陷/友/敌/中性)与D9房东(座主)由 calculator 查表确定；
> D9 审计直接读此两列，禁止自行判读入旺/落陷/座主链。Rahu/Ketu 不出此两列(留"—")。

Pushkara Navamsa（滋养保护区）: [星名列表 / 无]
Pushkara Bhaga（精确滋养度）: [星名列表 / 无]
（calc 计算输出；D9 审计"落陷检查Pushkara补丁"直接读此两行，定义见 p1_p12 P7）

### D10 Dasamsha
| 行星 | D10星座 | D10宫位 |
|------|---------|---------|
| Lagna | [sign] | 1 |
| [planet] | [sign] | [house] |

### D4 Chaturthamsha
| 行星 | D4星座 | D4宫位 |
|------|--------|--------|
| Lagna | [sign] | 1 |
| [planet] | [sign] | [house] |

### D5 Panchamsha
| 行星 | D5星座 | D5宫位 |
|------|--------|--------|
| Lagna | [sign] | 1 |
| [planet] | [sign] | [house] |

### 分盘内部宫主表 + 尊贵度（线A · calc 查表，禁自推）
> 线A=用分盘自身 Lagna 推出的分盘宫主(D*-L*)，读此段；线B=本命宫主职落分盘(见上各分盘落宫表)。两线禁混用，断语须标是哪个盘。
**D[9/10/4/5]** Lagna=[sign]（D*-Lagna主=[行星]）
  宫主(线A): D*-L1=[行星]@H* D*-L2=[行星]@H* …（12宫，以分盘自身 Lagna 起宫；@H*=该座主在本分盘落宫）
  分盘尊贵: [星]=[旺/自庙/陷/友/敌/中]/座主[行星] …（7曜，calc 查表的分盘内部自然尊贵）
> ❌ 禁止自推 D*-L*；引用分盘宫主职时必须写"D10-L10=Saturn"而非裸"10宫主"，遵循 SKILL 分盘视角分离铁律。

## 校验结果

```
 1. SAV=337          [✅/❌]
 2. BAV行常量        [✅/❌] [细节]
 3. 行星完整性(10)   [✅/❌]
 4. 度数唯一性        [✅/❌]
 5. Ra-Ke差180°      [✅/❌]
 6. 逆行标记完整      [✅/❌]
 6b. 燃烧检测        [✅/❌] [燃烧行星列表]
 6c. 行星战争检测    [✅/❌] [战争行星对]
 7. Ayanamsa一致     [✅/❌]
 7b. Lagna敏感度     [✅/❌] [Sandhi/Gandanta标注]
 7c. 盈月/亏月       [盈月/亏月] [距Sun X°]
 8. Nakshatra↔度数   [✅/❌]
 9. Chara Karaka排序 [✅/❌]
 10. Dasha时长常数    [✅/❌]
 11. D9公式交叉       [✅/❌]
 12. Ra-Ke分盘校验    [✅/❌] [各分盘结果]
 13. AL/UL位置        [✅/❌/未提取] [AL=sign/house, UL=sign/house]
```

> ⚠️ 迁移保留规则：以下四节（盘面初验结果 / 验前事校准率 / 生时矫正记录 / 信号修正日志）
> 由 reader 验前事阶段产出（第3次写入），calc/formatter 不生成。
> rectifier 校准后用 calc engine 重算 structured_data 时，必须将这些节原样保留/迁移到新文件，
> 不得因重算而静默丢失。

## 盘面初验结果

| # | 验证内容 | 用户反馈 |
|---|---------|---------|
| 1 | [描述] | [✅命中 / ❌不命中] |
| ... | ... | ... |

命中率: [X]/[Y] → 时间可信度: [高/中/低]

## 验前事校准率

```
校准率: [总命中]/[总推断]
```

## 生时矫正记录

```
Lagna度数: [deg]° [sign]
D1边界: [远离/接近]
D9边界: [远离/接近]
```

## 信号修正日志

| 轮次 | AI预测 | 信号调整 |
|------|--------|--------|
| R1 | [信号逻辑] | [信号方向调整 / 未命中，记录偏差] |

解读总结（给core的一句话概括）: [信号方向概括]

> ⚠️ 信息隔离铁规（同 reader SKILL Step 8）："AI预测"列只写信号逻辑、
> "信号调整"列与解读总结只写信号方向，禁止包含用户原话与经历细节。

## 当前过运位置（Transit Data）

> 数据来源：calc engine 自动计算（当前日期）
> 用途：core动态预测（大运×过运交叉分析、Sade Sati检查）
> 提取时间点：读盘当日日期

### 慢行星过运
| 行星 | 过运星座 | 过运宫位(从Lagna数) | 说明 |
|------|---------|-------------------|------|
| Saturn | [sign] | [house] | 过运周期~2.5年/星座 |
| Jupiter | [sign] | [house] | 过运周期~1年/星座 |
| Rahu | [sign] | [house] | 过运周期~1.5年/星座 |
| Ketu | [sign(Rahu对冲)] | [house] | 自动取Rahu对冲 |

### Sade Sati初判
```
Moon本命星座: [sign]
Saturn过运星座: [sign]
相对位置: [Moon前1宫 / Moon本宫 / Moon后1宫 / 非Sade Sati]
Sade Sati状态: [第一阶段(升起) / 第二阶段(顶峰) / 第三阶段(消退) / 未激活]
```

### 双过运触发检查（Saturn-Jupiter Double Transit）
```
Saturn过运相位覆盖宫位: [列出Saturn合相/3rd/7th/10th相位覆盖的宫位]
Jupiter过运相位覆盖宫位: [列出Jupiter合相/5th/7th/9th相位覆盖的宫位]
双过运激活宫位: [两者交集的宫位] → 这些宫位的事务在当前时期被"触发"
```

### 未来过运换座时间表（真实天文计算，未来5年，必须）
> 用途：报告/QA 中一切未来过运窗口（"YYYY年 Saturn 进X座"类）**必须引用本表日期**，
> 禁止模型凭记忆推算换座时间（LLM 心算恒星黄道换座常错数月到一年）。
> 由 calc（transit.py future_ingress_table）生成；逆行回跨如实列出（同一边界可能 进→退→再进）。

| 日期 | 行星 | 换座 |
|------|------|------|
| [YYYY-MM-DD] | [Saturn/Jupiter/Rahu] | [from_sign] → [to_sign] |

降级规则：非 calc 路径无此表时，下游禁止给出带年月的未来过运表述，只允许"需实算确认"。
