---
name: research-master
description: >
  PDF 文献深度解析引擎. TRIGGER when the user wants to: batch-process PDF files into structured
  research notes; extract and analyze academic papers in a directory; generate literature notes,
  Obsidian canvases, or Excel summaries from PDFs; perform deep reading analysis of academic papers.
  Keywords that should trigger: 文献解析, 论文笔记, PDF分析, research notes, literature analysis,
  文献笔记, 解析文献, 批量处理PDF.
  DO NOT trigger for single PDF reading (use Read tool) or non-academic PDF processing.
---

# Research-Master V4.5: PDF 深度解析引擎

## 核心原则
1. **自动化全闭环**: 给定 PDF 目录 → 文本提取 → LLM 分析 → Markdown 笔记 → Canvas → Excel
2. **极度详尽**: 机制分析和实证设计各至少 500 字
3. **构建透明**: 数据来源、核心变量(X/Y)、公式、IV 逻辑完整

## 使用方法
```bash
/opt/anaconda3/bin/python "/Users/zhangjie/.gemini/skills/research-master/research_master_pipeline.py" "<PDF目录绝对路径>"
```

## 产出（在输入目录的父目录下）
- `{Author} - {Title}_笔记.md` — 超详细笔记
- `{Author} - {Title}_画布.canvas` — Obsidian Canvas
- `文献资产登记表_精简摘要版.xlsx` — 汇总 Excel

## 目标目录
$ARGUMENTS
