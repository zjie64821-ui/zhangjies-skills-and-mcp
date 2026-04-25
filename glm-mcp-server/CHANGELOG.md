# 更新日志

本项目的重要变更记录。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
本项目遵循 [语义化版本](https://semver.org/spec/v2.0.0.html)。

## [1.1.0] - 2026-03-28

### 新增
- 基于 FastMCP 框架的轻量 MCP 服务器 `glm_fastmcp_server.py`
- `switch_mcp.bat` 本地/云端图片分析工具切换脚本
- `.gitignore` 敏感配置保护（.env、.mcp.json 等）
- 跨项目全局使用说明（`claude mcp add -s user`）
- 模型默认值升级为 `glm-4.6v`

### 变更
- MCP 服务器入口从 `server.py` 切换为 `glm_fastmcp_server.py`（FastMCP 封装，72 行代码）
- 移除 `config.py`、`logger.py`、`server.py` 中所有 `print()` 输出，避免干扰 MCP stdio 通信
- `logger.py` 控制台日志默认禁用，通过 `MCP_DISABLE_CONSOLE_LOG` 环境变量控制
- 工具名从 `read_image` 改为 `analyze_image`
- `install.bat` 重写，使用 `.env` 文件管理 API 密钥
- `test_install.bat` 重写，新增 FastMCP 和 API 连通性检测
- 全面更新 `README.md` 文档，新增配置说明和故障排除

### 修复
- Windows 上 `ProactorEventLoop` 与 MCP stdio 传输不兼容导致服务器无响应
- 日志输出写入 stdout 导致 JSON-RPC 协议帧被破坏

## [1.0.0] - 2025-09-10

### 新增
- 一键安装功能（Windows/Linux/Mac）
- 安全的 API 密钥管理（环境变量存储）
- 多格式图像支持（JPG、PNG、GIF、BMP）
- 跨平台支持（Windows、Linux、macOS）
- 基于 GLM-4.6V 的智能图像分析
- 完整的日志系统和错误处理
- 详细的使用文档和故障排除指南
- MCP (Model Context Protocol) 服务器实现
- 自动环境检测和依赖安装
- Claude Code 集成

---

## 版本说明

- **主版本号**：不兼容的 API 变更
- **次版本号**：向下兼容的功能新增
- **修订号**：向下兼容的问题修复
