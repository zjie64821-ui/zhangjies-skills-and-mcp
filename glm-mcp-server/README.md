# General Read Image For Claude Code - 通用大模型接入Claude Code读图分析助手

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Claude](https://img.shields.io/badge/Claude%20Code-compatible-green.svg)

**一个用于在 Claude Code 中集成智谱 AI GLM-4.6V 图像分析功能的 MCP 服务器**

[功能特性](#-功能特性) • [快速开始](#-快速开始) • [手动安装](#-手动安装可选) • [配置说明](#-配置说明) • [故障排除](#-故障排除)

</div>


![pj](https://github.com/user-attachments/assets/b93ce6a6-4629-49c4-b5a1-a86666cdf474)


## ⚡ 快速开始

### 📥 下载项目

```bash
git clone https://github.com/ifolin/glm-mcp-server.git
cd glm-mcp-server
```

### 🚀 一键安装

<details>
<summary><strong>Windows 用户</strong></summary>

1. 双击运行 `install.bat`
2. 按照提示输入您的 GLM API 密钥
3. 在 Claude Code 中打开此项目目录即可使用

</details>

<details>
<summary><strong>Linux/Mac 用户</strong></summary>

1. 在终端中运行：`chmod +x install.sh && ./install.sh`
2. 按照提示输入您的 GLM API 密钥
3. 在 Claude Code 中打开此项目目录即可使用

</details>

### 🎯 验证安装

安装完成后，在 Claude Code 中输入：
```
分析 ./03.jpg 这张图片的内容
```

如果看到图像分析结果，说明安装成功！

**注意**：Claude Code 会自动调用 `mcp__glm-mcp__analyze_image` 工具来处理图像分析请求。

## ✨ 功能特性

- **一键安装**：跨平台自动化安装脚本
- **安全配置**：API 密钥存储在项目 `.env` 文件中，不暴露在代码仓库
- **多格式支持**：JPG、PNG、GIF、BMP 等常见图片格式
- **跨平台**：Windows、Linux、macOS 全支持
- **智能分析**：基于 GLM-4.6V 模型的强大图像理解能力
- **FastMCP 驱动**：基于 MCP 官方 FastMCP 框架，轻量高效

## 🔧 手动安装（可选）

如果您需要手动配置，请按照以下步骤：

### 1. 获取 API 密钥
- 访问 [智谱AI控制台](https://open.bigmodel.cn/console)
- 注册并获取您的 API 密钥

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

依赖包含：
- `zhipuai` — 智谱 AI SDK
- `mcp` — MCP 官方包（含 FastMCP 框架）
- `python-dotenv` — 环境变量管理

### 3. 创建 `.env` 文件

在项目根目录创建 `.env` 文件：
```
GLM_API_KEY=your_api_key_here
GLM_API_BASE=https://open.bigmodel.cn/api/paas/v4/
GLM_IMAGE_MODEL=glm-4.6v
```

### 4. 创建 `.mcp.json` 文件

在项目根目录创建 `.mcp.json`（告诉 Claude Code 如何启动 MCP 服务器）：
```json
{
  "mcpServers": {
    "glm-mcp": {
      "command": "python",
      "args": ["/替换为你的实际路径/GLM-MCP/glm_fastmcp_server.py"],
      "env": {
        "GLM_API_BASE": "https://open.bigmodel.cn/api/paas/v4/",
        "GLM_IMAGE_MODEL": "glm-4.6v"
      }
    }
  }
}
```

> **说明**：
> - `command` — Python 可执行文件路径（建议使用绝对路径，如 conda 环境的 `E:\miniconda3\envs\py310\python.exe`）
> - `args` — MCP 服务器入口文件 `glm_fastmcp_server.py` 的绝对路径
> - `env` — 额外环境变量（`GLM_API_KEY` 通过 `.env` 文件提供，不需要写在这里）
> - `.mcp.json` 已加入 `.gitignore`，不会被提交到代码仓库

### 5. 配置权限（可选）

如果 Claude Code 每次调用都要求确认，可在 `.claude/settings.json` 中添加：
```json
{
  "permissions": {
    "allow": [
      "mcp__glm-mcp__analyze_image"
    ]
  }
}
```

## ⚙️ 配置说明

### MCP 配置层级

Claude Code 的 MCP 配置支持三个层级：

| 层级 | 文件位置 | 用途 |
|------|----------|------|
| **项目级** | 项目根目录 `.mcp.json` | 团队共享，可提交到 git |
| **本地级** | 项目 `.claude/settings.local.json` | 个人私有配置 |
| **用户级** | `~/.claude/settings.json` | 跨项目全局生效 |

本项目使用 **项目级** `.mcp.json` 配置。

### API 密钥管理

| 方式 | 安全性 | 说明 |
|------|--------|------|
| `.env` 文件（推荐） | 高 | 已加入 `.gitignore`，不进入代码仓库 |
| `.mcp.json` 的 `env` 字段 | 低 | 明文存储，不适合存放密钥 |
| 系统环境变量 | 中 | 所有项目可用，但需手动配置 |

本项目推荐使用 `.env` 文件方式，服务器代码通过 `python-dotenv` 自动加载。

### 跨项目全局使用（所有项目可用）

默认情况下 MCP 服务器仅在当前项目目录生效。如需在所有项目中使用 GLM 图像分析：

```bash
# 方法一：通过 CLI 注册到用户级（推荐）
claude mcp add glm-mcp -s user \
  -e GLM_API_KEY=your_api_key \
  -e GLM_API_BASE=https://open.bigmodel.cn/api/paas/v4/ \
  -e GLM_IMAGE_MODEL=glm-4.6v \
  -- /path/to/python /path/to/GLM-MCP/glm_fastmcp_server.py
```

Windows 用户：
```cmd
claude mcp add glm-mcp -s user -e GLM_API_KEY=your_api_key -e GLM_API_BASE=https://open.bigmodel.cn/api/paas/v4/ -e GLM_IMAGE_MODEL=glm-4.6v -- "E:\miniconda3\envs\py310\python.exe" "E:\claude-code\GLM-MCP\glm_fastmcp_server.py"
```

注册后，在**任何项目**中都可以直接使用 `mcp__glm-mcp__analyze_image` 分析图片。

### 切换本地/云端图片分析工具

Claude Code 可能内置了云端图片分析 MCP（如 `4_5v_mcp`）。可通过 `switch_mcp.bat` 脚本切换：

```
双击运行 switch_mcp.bat
```

提供三种模式：

| 选项 | 说明 | 适用场景 |
|------|------|----------|
| 1. glm-mcp（本地） | 禁用云端，只用本地 GLM | 日常使用（推荐） |
| 2. 云端模型 | 禁用本地，只用云端 | 需要云端模型时 |
| 3. 两者都允许 | Claude 自动选择 | 灵活使用 |

切换后需**重启 Claude Code** 生效。

手动切换（编辑 `~/.claude/settings.json`）：
```json
{
  "permissions": {
    "allow": ["mcp__glm-mcp__analyze_image"],
    "deny": ["mcp__4_5v_mcp__*"]
  }
}
```

### 环境变量说明

| 变量名 | 必需 | 默认值 | 说明 |
|--------|------|--------|------|
| `GLM_API_KEY` | 是 | 无 | 智谱 AI API 密钥 |
| `GLM_API_BASE` | 否 | `https://open.bigmodel.cn/api/paas/v4/` | API 基础地址 |
| `GLM_IMAGE_MODEL` | 否 | `glm-4.6v` | 使用的视觉模型 |

### Windows 特别说明

本项目针对 Windows 平台做了以下适配：
- **事件循环策略**：自动设置 `WindowsSelectorEventLoopPolicy`，解决 Windows 上 MCP stdio 通信兼容性问题
- **编码处理**：建议在 `.mcp.json` 的 `env` 中添加 `"PYTHONIOENCODING": "utf-8"` 和 `"PYTHONUTF8": "1"`
- **路径格式**：`.mcp.json` 中 Windows 路径使用双反斜杠 `\\` 或正斜杠 `/`

## 📖 使用方法

安装完成后，在 Claude Code 中自然地描述您的需求：

**示例用法**：
- "分析 ./test.jpg 这张图片的内容"
- "请帮我看看 ./photos/image1.png 里面有什么"
- "使用GLM-4.6V模型分析 /path/to/image.jpg，描述这张图片"

**工作原理**：
- Claude Code 会自动识别图像分析需求
- 自动调用 `mcp__glm-mcp__analyze_image` 工具
- 使用智谱 GLM-4.6V 模型进行图像理解

**支持的图片格式**：
JPG、PNG、GIF、BMP 等常见图片格式

## 🛠️ 故障排除

### 1. MCP 服务器无法启动
- 确保 Python 3.10+ 已安装且 `command` 路径正确
- 检查 `glm_fastmcp_server.py` 文件路径是否正确
- Windows 用户确保使用绝对路径指向 Python 可执行文件
- 运行 `test_install.bat` 进行诊断

### 2. API 密钥问题
- 确认 `.env` 文件中 `GLM_API_KEY` 已正确设置
- `.env` 文件应位于项目根目录
- 验证 API 密钥是否有效：访问 [智谱AI控制台](https://open.bigmodel.cn/console)

### 3. Claude Code 无法识别工具
- 确保在 Claude Code 中**打开此项目目录**（`.mcp.json` 所在目录）
- 检查 `.mcp.json` 文件格式是否正确（JSON 语法）
- 确认权限配置中包含 `mcp__glm-mcp__analyze_image`
- 重启 Claude Code

### 4. 图像分析失败
- 检查图片路径是否使用绝对路径
- 确认图片格式是否支持
- 查看日志文件：`mcpserver.log`

### 5. Windows 上服务器卡死/无响应
这是 Windows 上 Python 事件循环与 MCP stdio 传输不兼容导致的。本项目已在 `glm_fastmcp_server.py` 中自动处理，如果仍出现问题：
- 确认使用的是 `glm_fastmcp_server.py` 而非 `server.py` 或 `main.py`
- 检查是否有其他代码向 stdout 输出内容（会干扰 MCP 协议通信）

## 📝 更新配置

### 更新 API 密钥
1. 编辑项目根目录的 `.env` 文件
2. 重启 Claude Code

### 更新模型版本
修改 `.env` 或 `.mcp.json` 中的 `GLM_IMAGE_MODEL`，支持的模型：
- `glm-4.6v`（推荐）
- `glm-4v`

## 📋 文件结构

```
GLM-MCP/
├── glm_fastmcp_server.py    # MCP 服务器核心（基于 FastMCP 框架）
├── main.py                  # 原始主程序入口
├── config.py                # 配置管理模块
├── server.py                # 原始 MCP 服务器（低级 API 实现）
├── image_processor.py       # 图像处理模块
├── logger.py                # 日志系统（MCP 模式自动禁用控制台输出）
├── utils.py                 # 工具函数
├── .mcp.json                # MCP 服务器声明（项目级配置）
├── .env                     # API 密钥等敏感配置（不提交到 git）
├── .gitignore               # Git 忽略规则
├── .claude/
│   ├── settings.json        # 项目级权限配置
│   └── settings.local.json  # 本地权限配置（不提交到 git）
├── install.bat              # Windows 一键安装
├── switch_mcp.bat           # 本地/云端 MCP 切换
├── test_install.bat         # Windows 安装验证
├── start_server.bat         # Windows 手动启动（调试用）
├── requirements.txt         # Python 依赖
├── README.md                # 本文档
└── CHANGELOG.md             # 更新日志
```

## 🤝 贡献

我们欢迎任何形式的贡献！请查看 [贡献指南](CONTRIBUTING.md) 了解如何参与项目开发。

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [智谱AI](https://open.bigmodel.cn/) - 提供强大的GLM-4.6V模型
- [Claude Code](https://claude.ai/code) - 优秀的AI编程助手
- [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) - 标准化的AI服务接口

## 📞 支持

<img width="477" height="477" alt="林枫_qrcode" src="https://github.com/user-attachments/assets/14bae59a-3e7d-4843-9e72-6744b1d5b636" />

- **问题反馈**：[GitHub Issues](https://github.com/ifolin/glm-mcp-server/issues)

---

<div align="center">

**如果这个项目对您有帮助，请给我们一个 ⭐️ Star**

</div>
