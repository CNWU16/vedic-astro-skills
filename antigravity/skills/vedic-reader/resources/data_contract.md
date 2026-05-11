# structured_data.md 数据契约

> 本文档定义了reader输出、core/career/love消费的数据标准。
> 所有字段为必须，除非标注[可选]。

---

## 元信息

```
出生日期: YYYY-MM-DD
出生时间: HH:MM
出生地点: [城市] ([经度], [纬度])
时间精度: [精确到分钟 / ±15分钟 / ±1小时 / 不确定]
读盘方式: [JH表格 / 文本度数 / 视觉识别+用户确认]
Ayanamsa: [Lahiri / 其他]
Node模式: [Mean Node / True Node]
```

## 用户信息

```
性别: [男 / 女]
感情状态: [单身 / 恋爱中 / 已婚]
```

> ⚠️ 以下字段**不写入**structured_data.md，写入user_context.md：
> - 职业状态
> - 核心关切/具体问题
> - 用户补充的人生事件

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
| 1 | AK | [planet] | [deg] | 灵魂指示星 |
| 2 | AmK | [planet] | [deg] | 事业指示星 |
| 3 | BK | [planet] | [deg] | 兄弟指示星 |
| 4 | MK | [planet] | [deg] | 母亲指示星 |
| 5 | PK | [planet] | [deg] | 子女指示星 |
| 6 | GK | [planet] | [deg] | 障碍指示星 |
| 7 | DK | [planet] | [deg] | 配偶指示星 |

> Rahu参与8K时度数 = 30° - 原始度数

### DK争议
```
7K体系 DK = [planet]
8K体系 DK = [planet]
状态: [一致 / 不一致 → 分析时弱化DK，以宫位结构为主]
```

### Nakshatra
| 行星 | Nakshatra | Pada | Nakshatra主 |
|------|-----------|------|-------------|
| Lagna | [name] | [1-4] | [planet] |
| Sun | [name] | [1-4] | [planet] |
| ... | ... | ... | ... |

## 量化数据

### Shadbala
| 行星 | Rupas | 百分比 | 排名 | 强弱 |
|------|-------|--------|------|------|
| [planet] | [val] | [pct]% | [rank] | [强/中/弱] |

> 强: ≥150% | 中: 100-149% | 弱: <100%

### SAV (Sarvashtakavarga)
| Ar | Ta | Ge | Cn | Le | Vi | Li | Sc | Sg | Cp | Aq | Pi | 总计 |
|----|----|----|----|----|----|----|----|----|----|----|----|----|
| [n] | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | [n] | 337 |

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

当前状态:
```
Mahadasha: [planet] (YYYY-MM ~ YYYY-MM)
Antardasha: [planet] (YYYY-MM ~ YYYY-MM)
```

## 预分析（reader计算，core直接引用）

### 行星尊贵度
| 行星 | 落座 | 尊贵度 | 说明 |
|------|------|--------|------|
| [planet] | [sign] | [旺/入庙/友方/中性/敌方/陷] | [一句话] |

### 主要相位关系
| 行星A | 行星B | 关系 | 度数差 | 影响 |
|-------|-------|------|--------|------|
| [p1] | [p2] | [合相/对冲/三合] | [deg] | [一句话] |

> 只记录5-8组最重要的关系

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
| 行星 | D9星座 | D9宫位 | Vargottama |
|------|--------|--------|-----------|
| Lagna | [sign] | 1 | — |
| [planet] | [sign] | [house] | [是/否] |

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
```

## 盘面初验结果

| # | 验证内容 | 用户反馈 |
|---|---------|---------|
| 1 | [描述] | [✅命中 / ❌不命中] |
| ... | ... | ... |

命中率: [X]/[Y] → 时间可信度: [高/中/低]

## 生时矫正记录

```
Lagna度数: [deg]° [sign]
D1边界: [远离/接近]
D9边界: [远离/接近]
ABC执行: [未执行 / 已执行 → 结果]
```
