---
name: docx
description: >
  Word document (.docx) processing toolkit with format cloning. TRIGGER when the user needs to:
  create, edit, analyze, or convert Word documents; clone formatting from a sample document;
  generate documents with exact same formatting as a reference; write academic papers matching
  a specific journal format (AER, etc.); produce government reports with precise formatting;
  replicate fonts, sizes, margins, spacing, indentation from any DOCX template or sample.
  Keywords: Word, docx, 文档, 格式, 排版, 模板, 字体, 字号, 行距, 页边距, 格式克隆,
  文档生成, 论文排版, 报告排版, format clone, replicate formatting, document formatting.
  DO NOT trigger for simple text files (.txt, .md).
---

# DOCX Toolkit V2.0 — 含格式克隆引擎

## 决策树（按场景选择方案）

| 场景 | 方案 | 工具 |
|------|------|------|
| **读/分析文档** | pandoc 转换 | `pandoc --track-changes=all file.docx -o output.md` |
| **从样本克隆格式写新文档** | 格式提取 + 渲染 | `format_extractor.py` + `format_cloner.py` |
| **有干净模板 + 动态内容** | docxtpl 模板渲染 | `DocxTemplate("template.docx").render(context)` |
| **从零创建新文档** | docx-js (JS) | Document, Paragraph, TextRun → Packer.toBuffer() |
| **编辑已有文档** | OOXML 操控 | unpack → edit XML → pack |
| **红线审阅/批注** | OOXML tracked changes | `<w:ins>`, `<w:del>` 标签 |

---

## 核心工作流：格式克隆（最常用场景）

### 场景说明
用户提供一篇**完整的样本文档**（如 AER 论文、政府报告），要求用完全相同的格式（字体、字号、行距、页边距、缩进）生成新内容。

### Step 1: 格式提取

```bash
python3 ~/.claude/skills/docx/format_extractor.py "样本文件.docx" "格式档案.json"
```

**输出**：完整的 JSON 格式档案，包含：
- 页面设置（纸张大小、四边距、页眉页脚距离）
- 所有样式定义（Heading 1/2/3、Normal、Title 等）
- 每个段落的格式（对齐、行距、段前段后间距、首行缩进）
- 每个 run 的字体信息（字体名、字号、加粗/斜体/颜色）
- 表格格式（样式、单元格格式、边框）

### Step 2: 格式档案分析

我（Claude）会：
1. 读取格式档案 JSON
2. 识别文档结构（标题层级、正文、脚注、参考文献等）
3. 为用户总结关键格式参数，如：
   - 标题：黑体 三号 加粗 居中
   - 正文：宋体 小四 两端对齐 首行缩进2字符 行距1.5倍
   - 页边距：上下2.54cm 左右3.17cm
4. 询问用户确认或微调

### Step 3: 内容构建 + 渲染

**方式 A：自动渲染（推荐）**
我直接用 python-docx 生成文档，精确应用格式档案中的每个参数：

```python
from docx import Document
from docx.shared import Pt, Cm
import json

# 加载格式档案
profile = json.load(open("格式档案.json"))

doc = Document()

# 应用页面设置
section = doc.sections[0]
section.top_margin = Cm(profile["page_setup"][0]["top_margin_cm"])
section.left_margin = Cm(profile["page_setup"][0]["left_margin_cm"])
# ... 其余页面参数

# 查找参考段落的格式
def get_ref_format(style_name):
    for p in profile["paragraphs"]:
        if p["style_name"] == style_name and p["text_preview"].strip():
            return p
    return None

# 添加标题
ref = get_ref_format("Heading 1")
para = doc.add_paragraph("新标题", style="Heading 1")
# 应用参考格式...
```

**方式 B：docxtpl 模板渲染（有干净模板时）**
```python
from docxtpl import DocxTemplate

tpl = DocxTemplate("template.docx")
context = {"title": "新标题", "content": "新内容..."}
tpl.render(context)
tpl.save("output.docx")
```

### Step 4: 验证
生成后我会用 pandoc 提取输出文档的格式，与样本对比关键参数是否一致。

---

## 关键格式参数速查

### 中文论文常用格式
| 元素 | 字体 | 字号 | 其他 |
|------|------|------|------|
| 论文标题 | 黑体 | 小二/三号 | 加粗 居中 |
| 作者 | 楷体/仿宋 | 小四 | 居中 |
| 摘要标题 | 黑体 | 小四 | 加粗 |
| 摘要正文 | 楷体 | 五号 | 首行缩进2字符 |
| 一级标题 | 黑体 | 四号 | 加粗 左对齐 |
| 二级标题 | 黑体 | 小四 | 加粗 |
| 三级标题 | 宋体 | 小四 | 加粗 |
| 正文 | 宋体 | 小四 | 首行缩进2字符 1.5倍行距 |
| 表格标题 | 黑体 | 五号 | 居中 |
| 图标题 | 黑体 | 五号 | 居中 |
| 参考文献 | 宋体 | 五号 | 悬挂缩进 |

### 英文期刊常用格式（AER 为例）
| 元素 | 字体 | 字号 | 其他 |
|------|------|------|------|
| 标题 | Times New Roman | 16pt | Bold Center |
| 作者 | TNR | 12pt | Center |
| Abstract | TNR | 10pt | Italic |
| Section Header | TNR | 12pt | Bold Center SMALL CAPS |
| Body | TNR | 11pt | Justified 1.15 spacing |
| Footnotes | TNR | 8pt | |

---

## format_extractor.py 完整用法

```bash
# 提取格式档案到 JSON
python3 ~/.claude/skills/docx/format_extractor.py "样本.docx" "格式档案.json"

# 输出到终端（用于快速检查）
python3 ~/.claude/skills/docx/format_extractor.py "样本.docx"
```

## format_cloner.py 完整用法

```bash
# 从指令文件生成（指令中包含内容和格式引用）
python3 ~/.claude/skills/docx/format_cloner.py "格式档案.json" "内容指令.json"

# 生成空白模板
python3 ~/.claude/skills/docx/format_cloner.py "格式档案.json" "空白模板.docx" --empty
```

---

## OOXML 编辑（高级场景）

1. Unpack: `python ooxml/scripts/unpack.py <file> <dir>`
2. Edit XML with Document library
3. Pack: `python ooxml/scripts/pack.py <dir> <file>`

## Convert to Images
```bash
soffice --headless --convert-to pdf document.docx && pdftoppm -jpeg -r 150 document.pdf page
```

## Dependencies
pandoc, docx (npm), LibreOffice, poppler-utils, defusedxml, docxtpl, python-docx

## User Request
$ARGUMENTS
