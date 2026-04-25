---
name: obsidian
description: >
  Obsidian vault control via Local REST API. TRIGGER when the user wants to: search, create, update,
  read, or append to notes in their Obsidian vault; interact with Obsidian daily notes; manage
  Obsidian knowledge base; add content to currently open Obsidian note.
  Keywords: Obsidian, 笔记库, 我的笔记, daily note, 知识库, vault.
  DO NOT trigger for general note-taking without Obsidian context.
---

# Obsidian 笔记库控制

通过 Obsidian Local REST API 插件直接控制。

## 功能
- **搜索**: 按关键词搜索笔记
- **创建/更新**: 新建或覆盖笔记
- **追加**: 在笔记末尾添加内容
- **读取**: 获取指定笔记内容
- **当前笔记**: 读取/更新当前打开的笔记
- **命令**: 触发 Obsidian 命令

## 使用方式
- "在 Obsidian 中搜索 '项目计划'"
- "在每日笔记中添加任务"
- "读取 '研究笔记.md'"
- "在当前笔记追加摘要"

## 前置: Obsidian Local REST API 插件

## 用户请求
$ARGUMENTS
