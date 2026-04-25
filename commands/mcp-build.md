# MCP 服务器构建指南

创建高质量的 MCP (Model Context Protocol) 服务器，让 LLM 通过工具与外部服务交互。

## 四阶段流程

### Phase 1: 深度调研与规划
1. 理解 Agent-Centric 设计原则：
   - 为工作流构建，不只是包装 API
   - 优化有限上下文（高信号信息，非数据堆砌）
   - 设计可操作的错误消息（引导正确使用）
   - 按自然任务细分命名工具
2. 学习 MCP 协议: `https://modelcontextprotocol.io/llms-full.txt`
3. 学习框架文档:
   - Python SDK: `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
   - TypeScript SDK: `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
4. 研究目标 API 的所有文档
5. 创建实施计划（工具选择、输入输出设计、错误处理策略）

### Phase 2: 实现
1. 搭建项目结构
2. 先实现基础设施（API 请求、错误处理、响应格式、分页、认证）
3. 逐个实现工具：
   - Pydantic (Python) / Zod (TypeScript) 输入验证
   - 完整的 docstring/描述
   - 异步 I/O
   - 多响应格式（JSON/Markdown）
   - 工具注解（readOnlyHint, destructiveHint 等）

### Phase 3: 审查与优化
- DRY、可组合性、一致性、类型安全、文档完整
- Python: `python -m py_compile server.py`
- TypeScript: `npm run build`

### Phase 4: 创建评估
- 10 个独立、只读、复杂、真实、可验证的评估问题
- XML 格式输出

## 参考文档
- MCP Best Practices: `/Users/zhangjie/.gemini/skills/mcp-builder/reference/mcp_best_practices.md`
- Python Guide: `/Users/zhangjie/.gemini/skills/mcp-builder/reference/python_mcp_server.md`
- TypeScript Guide: `/Users/zhangjie/.gemini/skills/mcp-builder/reference/node_mcp_server.md`
- Evaluation Guide: `/Users/zhangjie/.gemini/skills/mcp-builder/reference/evaluation.md`

## 用户请求
$ARGUMENTS
