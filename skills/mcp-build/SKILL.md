---
name: mcp-build
description: >
  MCP (Model Context Protocol) server development guide. TRIGGER when the user wants to: create or
  build an MCP server; integrate an external API or service with MCP; develop tools for LLM interaction
  with external services; design MCP tool interfaces; implement MCP servers in Python (FastMCP) or
  TypeScript (MCP SDK).
  Keywords: MCP server, build MCP, create MCP, MCP开发, FastMCP, MCP SDK, tool integration.
  DO NOT trigger for using existing MCP tools or general API development.
---

# MCP 服务器构建指南

## 四阶段流程

### Phase 1: 深度调研
- Agent-Centric 设计（工作流 > API包装，优化上下文，可操作错误）
- MCP 协议: `https://modelcontextprotocol.io/llms-full.txt`
- SDK: Python (`python-sdk README`) 或 TypeScript (`typescript-sdk README`)
- 研究 API 文档 → 创建实施计划

### Phase 2: 实现
- 搭建项目 → 先基础设施（API请求/错误/响应/分页/认证）
- 逐工具实现: Pydantic/Zod 验证 + 完整 docstring + 异步 + 多格式
- 工具注解: readOnlyHint, destructiveHint, idempotentHint

### Phase 3: 审查
- DRY, 可组合性, 一致性, 类型安全
- Python: `python -m py_compile` | TS: `npm run build`

### Phase 4: 评估
- 10 个独立/只读/复杂/真实/可验证的评估问题 (XML)

## 参考文档 (in Gemini skills dir)
- `/Users/zhangjie/.gemini/skills/mcp-builder/reference/` 下的 best practices, python/node guides

## 用户请求
$ARGUMENTS
