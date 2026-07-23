# Tajika sambandha/contact overlay

## 定位

本层是默认关闭的实验副层，只处理经来源核证的 Tajika 接触关系。它不是完整
16 yoga 引擎，不改变 Parashari 标准层的“成／悬／不成”，也不提供事件日期。

只在用户明确要求 Tajika、Itthasala、applying/separating 时读取并运行。必须先完成
标准层 Phase 2，选定：

- 问者星：Lagna lord；
- 事项星：唯一主事项宫之主。

不得固定加入自然 Karaka 或 Moon 作为第三主星。

---

## 来源边界

主要来源：

1. *Tajika Nilakanthi*, Samjnatantra, Sodasayogadhyaya 2.15–72：
   <https://archive.org/details/tajika_nilakanthi>
2. Martin Gansten and Ola Wikander, “Sahl and the Tājika Yogas: Indian
   Transformations of Arabic Astrology” (2011)：
   <https://doi.org/10.1080/00033790.2010.533349>

来源已经明确的计算：

| 名称 | 本层定义 |
|---|---|
| Itthasala / Muthashila | 同一 applying 关系，不是两个 yoga |
| Isharafa / Musharipha | 已过精确点的 separating 关系 |
| Nakta | 较快的第三星从一方分离并向另一方应用，传递光线 |
| Manau | Mars／Saturn 形成抢先接触而阻断主关系的候选 |
| Kamboola | 主星对 Itthasala，并由 Moon 与一方或双方形成 Itthasala |
| Khallasara | Moon 无 Itthasala／合相；只修正 Tajika 内的 Kamboola |
| Radda | 接收方因逆行、燃烧、落陷等不能接光 |

暂不实现：

- Ikkavala、Induvara；
- Yamaya、Gairikamboola；
- Duphalikuttha、Dutthotthadivira、Tambira；
- Kuttha、Durapha。

这些名称在 Nilakantha 与其阿拉伯来源之间存在传承、拆词或重释问题。没有独立
例盘与边界测试前，禁止模型凭名称补完。

---

## 计算契约

运行：

```bash
python scripts/build_tajika_overlay.py \
  --datetime "<YYYY-MM-DD HH:MM>" \
  --lat <lat> --lon <lon> --tz "<IANA>" \
  --querent-lord <planet> \
  --matter-lord <planet> \
  --out-dir "<existing prashna_* directory>"
```

输出固定为当前盘目录中的 `tajika_overlay.md`。标准
`build_prashna_data.py` 不导入本模块，也没有 `--enable-tajika`。

几何规则：

- 七曜参与；Rahu／Ketu 不参与；
- 相位为 0／60／90／120／180；
- 60／90／120 必须同时计算两侧分支；
- deeptamsha：Sun 15、Moon 12、Mars 8、Mercury 7、Jupiter 9、Venus 7、
  Saturn 9；
- 两星边界为 `(deeptamsha_A + deeptamsha_B) / 2`；
- 逆行不全局跳过；使用有符号相对速度判断 applying／separating，并交给 Radda
  等具体规则处理；
- 距精确小于 1°的刚分离状态单列，不直接冒充完整 Isharafa。
- 60／120 为友好相位；0／90／180 为敌意相位。Itthasala 只说明接触正在形成，
  敌意相位不能被翻译成“顺利成事”。

---

## 消费规则

只消费 `tajika_overlay.md` 中的主星对和已显示的第三星条件。

| 配置 | 可说 | 不可说 |
|---|---|---|
| 友好 Itthasala | 双方存在较顺畅的靠近／接通趋势 | 单凭它把标准层改判“成” |
| 敌意 Itthasala | 接触正在形成，但通过阻力、冲突或不协调发生 | 把“有接触”翻译成“顺利成” |
| Isharafa | 接触已经越过高点 | 自动等于永久不成 |
| Nakta | 主星无直接接触时，可能经中间人／中介完成连接 | 主星已有接触时重复叠加；写成 Moon 专属 |
| Manau | 有第三方／条件抢先阻断候选 | 未核时序就断言一定阻断 |
| Kamboola | Moon 对主接触有增强候选 | 不分尊贵等级就称“最强” |
| Khallasara | Tajika 内缺 Moon 接触 | 写成 Parashari 空亡或全局否决 |
| Radda | 接收能力受损 | 忽略具体退回原因 |

当前 Radda 只执行可明确回查的接收方逆行、燃烧、落陷。`enemy`／`great_enemy`
等一般敌友尊贵度不自动升级成 Radda；完整 Tajika strength 尚未实现。

若主星对无接触，只能写：

> 本 Tajika contact overlay 未检出 deeptamsha 内的主星接触；副层无明确补充。

不得把“未检出”写成标准层“不成”。

---

## 输出要求

判读单若引用，只能增加独立章节：

```markdown
## Tajika contact overlay（实验副层）

**主星对**：<Lagna lord> — <事项 lord>
**直接接触**：<Itthasala / Isharafa / 无>
**第三星条件**：<Nakta / Manau / 无>
**Moon 修正**：<Kamboola / Khallasara / 无>
**接收修正**：<Radda / 无>
**与标准层关系**：只作并列观察，不改标准结论。
**Timing**：未启用。
```

---

## 进入可用状态的门

在以下测试全部通过前，标题必须保留“实验副层”：

- 0／60／90／120／180 两侧分支；
- applying、exact、刚过 exact、Isharafa；
- direct／retrograde 的有符号速度；
- Nilakantha 的 Itthasala、Nakta、Manau 例盘；
- Kamboola、Khallasara、Radda 的正反例；
- 主星相同、Moon 为主星、边界等异常输入；
- 两张固定盘回归。
