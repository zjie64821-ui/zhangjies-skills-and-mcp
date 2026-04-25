---
name: file-organize
description: >
  Intelligent file and folder organization. TRIGGER when the user wants to: organize messy folders,
  clean up downloads, find and remove duplicate files, restructure project directories, sort files
  by type/date/purpose, archive old files, or establish better file organization.
  Keywords: 整理文件, 文件整理, 清理下载, 重复文件, 文件夹整理, organize files, cleanup,
  duplicates, sort files, archive.
  DO NOT trigger for file reading or single-file operations.
---

# 文件整理助手

## 工作流
1. **了解范围**: 目标目录、主要问题、整理力度
2. **分析**: `ls`, `du`, `find` 统计类型/大小/日期
3. **找重复**: `md5` 精确匹配 / 同名检测
4. **提出方案**: 当前状态 → 新结构 → 变更列表 → 等待确认
5. **执行**: 创建文件夹 → 移动 → 重命名 → 删除(需确认)

## 整理维度
- 按类型: 文档/图片/视频/压缩包/代码/表格
- 按用途: 工作/个人、活跃/归档
- 按时间: 当前/往年/归档

## 命名: `YYYY-MM-DD - 描述.ext`

## 安全: 删除前确认、记录移动、保留日期

## 用户请求
$ARGUMENTS
