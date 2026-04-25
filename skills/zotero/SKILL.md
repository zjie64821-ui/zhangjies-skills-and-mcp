---
name: zotero
description: >
  Zotero reference management via MCP and CLI. TRIGGER when the user wants to: search their Zotero
  library, manage references, add notes to papers, organize collections, export citations, find similar
  papers, manage tags, or perform any bibliographic management task.
  Keywords: Zotero, 文献管理, 参考文献, citation, reference, bibliography, 我的文献库.
  DO NOT trigger for searching external databases (use cnki-search or gs-search).
---

# Zotero 控制

## MCP 工具 (zotero-mcp, 直接可用)
| 操作 | 工具 |
|------|------|
| 搜索文献 | `mcp__zotero-mcp__search_library` |
| 条目详情 | `mcp__zotero-mcp__get_item_details` |
| 全文内容 | `mcp__zotero-mcp__get_content` |
| 高亮笔记 | `mcp__zotero-mcp__get_annotations` |
| 全文搜索 | `mcp__zotero-mcp__search_fulltext` |
| 语义搜索 | `mcp__zotero-mcp__semantic_search` |
| 集合管理 | `mcp__zotero-mcp__get_collections` |
| 创建条目 | `mcp__zotero-mcp__write_item` |
| 创建笔记 | `mcp__zotero-mcp__write_note` |
| 更新元数据 | `mcp__zotero-mcp__write_metadata` |
| 管理标签 | `mcp__zotero-mcp__write_tag` |
| 相似文献 | `mcp__zotero-mcp__find_similar` |

## CLI 工具 (需 Local API 启用)
```bash
cli-anything-zotero app status --json
cli-anything-zotero item citation <key> --style apa --json
cli-anything-zotero note add <key> --text "要点" --json
cli-anything-zotero item context <key> --include-notes --json
```

## 前置: Zotero 桌面端运行 + MCP 127.0.0.1:23120

## 用户请求
$ARGUMENTS
