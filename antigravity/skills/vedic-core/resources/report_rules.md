# 报告打包规则

> 用途：当用户说"生成报告""打包""导出HTML"时执行

---

## 脚本位置

report_builder.py 在本skill的 `scripts/` 目录下。
**完整路径**：使用相对于SKILL.md的路径 `scripts/report_builder.py`。

如果执行时提示找不到脚本，按以下顺序查找：
1. 当前skill目录下的 `scripts/report_builder.py`
2. 工作目录下的 `report_builder.py`（用户可能手动复制过）
3. 如果都找不到 → 告诉用户脚本路径，让用户确认位置

## 打包命令

先根据当前 Skill 的 `client_language` 选择 `--lang`：

- English → `--lang en`
- 日本語 → `--lang ja`
- 中文 → `--lang cn`
- 其他语言 → 使用正文实际采用的语言；HTML 外壳暂选 `en`，不得因此把正文改回英文、日文或中文

```python
# 打包全部已有文件
python scripts/report_builder.py [工作目录] --lang [cn|en|ja]

# 只打包core
python scripts/report_builder.py [工作目录] --include core --lang [cn|en|ja]

# 只打包core + career
python scripts/report_builder.py [工作目录] --include core,career --lang [cn|en|ja]
```

report_builder自动检测目录中存在哪些MD文件，只打包存在的。
`--include`参数可选择只打包特定部分。
`--lang`只控制封面、目录、章节标题和页脚；正文语言来自已有 Markdown，禁止把
正文放入不匹配的中文、英文或日文外壳。

## ⚠️ 禁止行为

1. **禁止自动打开浏览器预览**：生成HTML后不要用 `open`/`start`/`xdg-open` 打开浏览器。只告诉用户文件路径，让用户自己决定是否打开。
2. **禁止在聊天框中输出HTML代码**：HTML文件由脚本生成，不要在对话中贴代码。
3. **生成完成后只报路径**：`"报告已生成：[完整文件路径]"`，不做其他操作。
