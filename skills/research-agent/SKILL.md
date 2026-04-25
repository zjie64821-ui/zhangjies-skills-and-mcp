---
name: research-agent
description: >
  学术科研全流程自动编排引擎. TRIGGER when the user wants to: conduct a comprehensive academic
  literature search; find papers on a research topic across multiple databases (CNKI, Google Scholar,
  ScienceDirect, Web of Science); perform systematic literature review; collect high-quality academic
  references for a research project; search for Chinese or English academic papers.
  Keywords that should trigger: 文献搜索, 论文搜索, 科研, 学术研究, literature review,
  find papers, academic search, 系统综述.
  DO NOT trigger for simple web searches or non-academic research.
---

# Research-Agent V4.0: 学术科研全自动生产线

## 全流程

### 1. 深度对齐与拆解
严禁直接搜索，先进行 X/Y 轴逻辑拆解 → 3x3 关键词检索矩阵 → 提交检索方案待确认

### 2. 高通量精准发现
- 并行搜索: CNKI, ScienceDirect, Google Scholar, Web of Science
- 时间锁定 [2023-2026]，优先顶刊和高被引

### 3. 自动化摘要评估
批量读取摘要 → AI 评估实证价值和逻辑匹配度 → 锁定 20中+20英种子文献

### 4. Zotero 推送与下载
导出 zotero 模式 → PDF 下载挂载 → 元数据同步

### 5. 科研成果管理
维护 `文献下载进度表.xlsx` → 自动触发 research-master 深度解析

## 执行原则
1. 宁缺毋滥：只收录高质量顶刊
2. 眼见为实：PDF 验证后才标记"已获取"
3. 内存友好：每 5 篇清理 Chrome 标签

## 资源路径
- 源码: `/Users/zhangjie/Research-Skills-Source/`
- 归档: `/Users/zhangjie/Desktop/研究/`

## 研究主题
$ARGUMENTS
