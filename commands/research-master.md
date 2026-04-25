# Research Master: PDF 深度解析引擎 (V4.5)

将指定目录中的 PDF 文献转化为高保真结构化研究资产。

## 核心原则
1. **自动化全闭环**: 给定 PDF 目录，自动完成文本提取、深度分析、Markdown 笔记、Obsidian Canvas、Excel 汇总
2. **极度详尽**: 笔记可替代原文阅读，机制分析和实证设计各至少 500 字
3. **构建透明**: 详细说明数据来源、核心变量(X/Y)、公式、IV 选择逻辑
4. **实时进度**: 终端输出 `[1/40] Processing...`

## 使用方法

执行 Python 管道脚本：
```bash
/opt/anaconda3/bin/python "/Users/zhangjie/.gemini/skills/research-master/research_master_pipeline.py" "<PDF目录绝对路径>"
```

示例：
```bash
/opt/anaconda3/bin/python "/Users/zhangjie/.gemini/skills/research-master/research_master_pipeline.py" "/Users/zhangjie/Desktop/研究/能源转型政策/原始文献"
```

## 产出
- `{Author} - {Title}_笔记.md`: 超详细 Markdown 笔记
- `{Author} - {Title}_画布.canvas`: Obsidian Canvas 表示
- `文献资产登记表_精简摘要版.xlsx`: 汇总 Excel

产出位于输入目录的父目录下的 `文献笔记` 文件夹中。

## 目标目录
$ARGUMENTS
