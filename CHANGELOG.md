# 📋 Changelog

All notable changes to this project will be documented in this file.

---

## [v5.0.1] - 2026-05-24

> **社区反馈修复** — BOM修复 + Nakshatra校验 + Ayanamsa检测

### 🔧 Reader (vedic-reader)

#### Fixed
- **UTF-8 BOM移除**：SKILL.md开头的BOM导致Claude Code frontmatter解析失败（skill描述显示为`---`）

#### Added
- **Ayanamsa被动提醒**：Step 0数据需求清单中明确标注"本系统基于Lahiri设计"，警告非Lahiri岁差的影响
- **Ayanamsa主动检测**：校验7增强为主动检测——在PDF/文本数据源中搜索Ayanamsa关键词（Lahiri/KP/Raman/Pushya），检测到非Lahiri时标注风险并提醒用户，不强制阻塞

### 🔧 Rectifier (vedic-rectifier)

#### Added
- **Step 3d Nakshatra边界校验**：D9精调后检查Lagna是否在Nakshatra边界±2°内，如果命中则展示两个候选Nakshatra的核心特质供用户确认，辅助验证时间偏向

---

## [v5.0] - 2026-05-22

> **开源最终版** — 执行阶段化重构 + 性能优化 + 报告系统升级

### 🔧 Reader (vedic-reader)

#### Changed
- **执行阶段化重构**：连续Steps 0-9拆分为3个独立执行阶段，每阶段独立思考链
  - 阶段1: 数据提取+校验 → WRITE 1
  - 阶段2: 预分析(8项) → WRITE 2
  - 阶段3: 验前事+收尾 → WRITE 3
- **渐进写入**：structured_data.md分3次写入（每次≤200行），防止单次output超限崩溃
- **强制断点**：每次写入后必须输出进度消息，自然打断过长思考链
- **SAV铁规强化**：SAV/BAV数据只接受用户主动粘贴（门控路径B），绝不从PDF自行提取

#### Fixed
- 修复模型自行合并多次写入导致agent terminated
- 修复思考链400-600秒撞output limit问题

### 📦 Report Builder

#### Changed
- **动态文件发现**：find_files 3轮扫描（精确匹配→前缀动态分组→QA glob）
- 不再需要穷举文件名，p2/p3/p4/p5任意后缀自动识别分组
- SECTION_REGISTRY扩展：支持p2d, p3a/p3b, p4a/p4b等分段文件

---

## [v4.9] - 2026-05-14

> **验前事话术定版** — 信号驱动 + minicore工具箱

### 🔧 Reader (vedic-reader)

#### Changed
- **SAV映射铁规**：明确SAV→Bhava映射公式，Lagna对齐规则，杜绝2宫位偏移
- **验前事SOP定版**：候选池A-H多维评估 → P1/P1.3/P5工具箱 → 3-5条输出
- **验前事复盘**：core分析完成后自动回溯未命中项，验证是否为时间偏差

#### Added
- 分盘提取门控(Path B)：SAV/D10/D4/D5必须用户截屏确认，不从PDF自动提取
- 校验规则扩展至16条（新增D5同宫检验）

---

## [v4.8] - 2026-05-13

> **分盘提取工程化** — 多通道交叉验证 + 校验强化

### 🔧 Reader (vedic-reader)

#### Changed
- D9改三轨交叉验证（文本层+视觉+公式计算）
- D10/D4/D5无条件截屏请求，去掉PDF自动提取路径
- 分盘视觉提取改整页300DPI，禁止auto-crop
- Ra-Ke对冲失败时用户截屏兜底

#### Added
- 验前事复盘自动触发（core分析完成后回溯）
- 校验11-12（分盘一致性）强制执行

---

## [v4.7] - 2026-05-12

> **验前事话术重构** — 时间验证定位 + 砍R2

### 🔧 Reader (vedic-reader)

#### Changed
- **话术重构**：从"占星师验身"改为"时间验证定位"
- 砍掉R2（二次验前事），改为评分触发rectifier
- 命中率根据时间来源分支评估

#### Fixed
- 清理R2残留引用（校准后重验+修正日志）

---

## [v4.6] - 2026-05-12

> **Rectifier对接优化** — Step 6精简 + 双盘对比

### 🔧 Reader (vedic-reader)

#### Changed
- Step 6精简为跳转rectifier（不再自行校准）
- 双盘对比融入rectifier的Step 3c

### 🔬 Rectifier (vedic-rectifier)

#### Added
- P1角色匹配验证
- 盘外验证使用工具箱

---

## [v4.5] - 2026-05-11

> **Mini-core引擎** — 行星快照 + SOP多维评估 + 工具箱体系

### 🔧 Reader (vedic-reader)

#### Added
- **Step 4.5 (后融入Step 4)**：mini-core预分析，8项计算为验前事准备
- **SOP多维评估**：验前事候选从直觉改为结构化评估
- **P1/P5/纹理工具箱**：作为Step 5分析辅助，不再依赖快照中间层

#### Changed
- Step 4.5融入Step 4（第7-9项），消除冗余
- 删除快照中间层，P1角色判定+P5落宫效率改为内联计算

---

## [v4.2-v4.4] - 2026-05-10

> **验前事迭代期** — 用户驱动验证 + 防锚定 + 排版规范

### 🔧 Reader (vedic-reader)

#### Added
- 验前事输出强制附带推导来源标注
- 修正日志（记录验前事反馈对信号的调整）
- 校准后重验流程

#### Changed
- 验前事框架从"考试检验"改为"校准+建信任+补充信息"
- 禁止假设标准年龄 + 推断具体性引导
- 排版硬规则：推导标注独占一段 + 条目间空行
- Step 6触发条件改用综合评分（含二次验前事）

#### Fixed
- 回滚v4.2.5过度设计（三重防污染体系→保持自然客观）

---

## [v4.0] - 2026-05-10

> **工程化重构** — 以实测反馈驱动的全面体验升级

### 🔧 Reader (vedic-reader)

#### Added
- **强制双通道PDF提取**：PyMuPDF文本层 + AI视觉识别同时执行，交叉验证
- **智能引导开场白**：三种输入方式按推荐程度排序（文字粘贴→PDF→截图）
- **JH导出指南**：5步表格复制操作指引 + South Indian (Regular) 设置建议
- **陈述式验前事**：从提问式改为占星师"验身"式陈述（"您应该是..."）
- **时间精度→分盘启用矩阵**：精度不够直接禁用高敏感分盘
- **校准推荐决策树**：精度不足时完整的推荐→接受/拒绝→后续处理流程
- **南/北印盘识别指引**：快速识别方法 + 推荐南印度盘 (Regular)

#### Changed
- **验前事阈值收紧**：3/5命中不再被视为"可接受"，≤3/5=低→推荐校准
- **校验规则**：12条→16条（新增燃烧、行星战争、Sandhi/Gandanta、盈月亏月）
- **措辞统一**：全部"盘面初验"→"验前事"

### 🔬 Rectifier (vedic-rectifier)

#### Added
- 改时间硬性条件：必须同时满足3条才能修改出生时间
- 防过度校准规则：5/5匹配绝对禁止进入扫描

---

## [v3.2] - 2026-05-08

### Added
- Reader通用提取架构：从JH专用→任意占星软件
- 引导开场白（初版）
- 三级数据清单（🔴关键/🟡重要/🟢可选）
- 触发词扩展

---

## [v3.1] - 2026-05-07

### Added
- Chehil独立审计对比合入
- 燃烧 (Combustion) 检测
- 行星战争 (Planetary War) 检测
- Dig Bala 方位力量

### Fixed
- 移除150行硬限制（导致内容压缩）

---

## [v3.0] - 2026-05-06

### Added
- **五Skill架构**：reader / core / career / love / rectifier
- vedic-rectifier 上线（5事件逆推出生时间，精度±5分钟）
- 正反双审 (Double Blind Audit) 机制
- D9身份继承矩阵五维分析
- Badhaka/Maraka审计模块

---

## [v2.x] - 2026-05-05

### Added
- Q&A规则外置 (qa_rules.md)
- HTML报告生成脚本 (report_builder.py)
- 报告打包规则 (report_rules.md)
- 语言风格规范同步至career/love

---

## [v1.x] - 2026-05-04

### Added
- 初始三Skill架构（core/career/love）
- 验前事反转：AI先预测，用户确认
- 十大板块白话文总结模板
- Claude Code命令支持
