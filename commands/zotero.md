# Zotero CLI 控制

通过 Zotero MCP 和 cli-anything-zotero 管理桌面端 Zotero。

## MCP 工具 (zotero-mcp)
直接可用的 Zotero 操作：
- `mcp__zotero-mcp__search_library` - 搜索文献库
- `mcp__zotero-mcp__get_item_details` - 获取条目详情
- `mcp__zotero-mcp__get_content` - 获取全文内容
- `mcp__zotero-mcp__get_annotations` - 获取高亮和笔记
- `mcp__zotero-mcp__search_fulltext` - 全文搜索
- `mcp__zotero-mcp__semantic_search` - 语义搜索
- `mcp__zotero-mcp__get_collections` - 获取集合
- `mcp__zotero-mcp__write_item` - 创建新条目
- `mcp__zotero-mcp__write_note` - 创建/修改笔记
- `mcp__zotero-mcp__write_metadata` - 更新元数据
- `mcp__zotero-mcp__write_tag` - 管理标签
- `mcp__zotero-mcp__find_similar` - 查找相似文献

## CLI 工具 (cli-anything-zotero)
需要 Zotero Local API 启用：
```bash
# 状态检查
cli-anything-zotero app status --json

# 使用当前选中的集合
cli-anything-zotero collection use-selected --json

# 渲染引用
cli-anything-zotero item citation <key> --style apa --locale en-US --json

# 添加子笔记
cli-anything-zotero note add <key> --text "要点" --json

# 构建 LLM 上下文
cli-anything-zotero item context <key> --include-notes --include-links --json
```

## 前置条件
- Zotero 桌面端运行中
- MCP 服务器: http://127.0.0.1:23120/mcp
- Local API 需在 Zotero 设置中启用

## 用户请求
$ARGUMENTS
