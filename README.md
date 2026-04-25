# Zhangjie's Skills & MCP for Claude Code

一键复刻 Zhangjie 的 Claude Code 全套配置：22个自定义技能、20个 Slash Commands、MCP 服务器、自动触发规则、写作风格学习系统等。

## 一键安装

```bash
git clone https://github.com/zjie64821-ui/zhangjies-skills-and-mcp.git
cd zhangjies-skills-and-mcp
chmod +x install.sh
./install.sh
```

安装脚本会自动复制所有文件到 `~/.claude/`，并在首次安装时（不覆盖已有配置）放置配置文件。

## 安装后必做

### 1. 替换 API Key

编辑 `~/.claude/settings.json`：
```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "你的API Key",
    "ANTHROPIC_BASE_URL": "你的API代理地址（或删除此行用官方API）"
  }
}
```

编辑 `~/.claude/mcp.json`：
```json
{
  "GLM_API_KEY": "在 https://open.bigmodel.cn/ 申请"
}
```

### 2. 安装其他 MCP Server（强烈推荐）

这些 MCP 服务端提供了核心功能，需单独安装：

| MCP Server | 安装命令 | 用途 |
|---|---|---|
| **Chrome DevTools** | `npx @anthropic-ai/chrome-devtools-mcp@latest` | 浏览器控制、外部大脑搜索 |
| **Zotero** | `npx zotero-mcp@latest` | 文献管理 |
| **ArXiv** | `pip install arxiv-mcp-server` | 论文搜索 |
| **Tavily** | `npx tavily-mcp@latest` | 深度网络搜索 |
| **Memory** | `npx @anthropic-ai/memory-mcp@latest` | 知识图谱记忆 |
| **Sequential Thinking** | `npx @anthropic-ai/sequential-thinking-mcp@latest` | 结构化推理 |
| **OpenAlex** | `pip install openalex-mcp` | 学术搜索 |
| **Synapse (Obsidian)** | `npx synapse-mcp@latest` | Obsidian 知识库 |

安装后在 Claude Code 中运行 `/mcp` 来添加服务器。

### 3. 重启 Claude Code

## 包含内容

### Slash Commands (20个)

| 命令 | 功能 |
|---|---|
| `/xlsx` | Excel 电子表格处理 |
| `/research-master` | PDF 文献深度解析 (V4.5) |
| `/content-writer` | 内容研究与写作助手 |
| `/changelog` | Git 提交转 Changelog |
| `/pptx` | PowerPoint 演示文稿处理 |
| `/style-learn` | 写作风格学习引擎 |
| `/obsidian` | Obsidian 笔记库控制 |
| `/mcp-build` | MCP 服务器构建指南 |
| `/research-agent` | 学术科研全自动生产线 (V4.0) |
| `/zotero` | Zotero 文献管理 |
| `/docx` | Word 文档处理（含格式克隆） |
| `/plan` | 文件式规划 |
| `/file-organize` | 文件整理助手 |
| `/pdf` | PDF 处理（合并、拆分、提取、OCR） |
| `/cnki-search` | CNKI 知网搜索 |
| `/youtube-dl` | YouTube 视频下载 |
| `/style-write` | 风格驱动写作引擎 |
| `/github-sync` | GitHub 同步（LFS 支持） |
| `/gs-search` | Google Scholar 搜索 |
| `/webapp-test` | Web 应用测试 (Playwright) |

### Skills (22个)

在以上20个命令基础上额外包含：
- **Data Pipeline**: Python 数据处理管道引擎
- **Stata**: 计量经济学分析引擎
- **Policy Eval**: LLM 政策文本评估引擎
- **Lit Download**: 学术文献批量下载与解析引擎

### MCP Server

- **GLM-4V 图像分析**: 自定义 MCP Server，调用智谱 GLM-4V-Flash 模型分析本地图像

### 核心规则 (CLAUDE.md)

- **图像自动分析**: 检测到图片立即分析，无需用户请求
- **写作风格学习**: 写作任务前自动检查/学习风格，去AI味规则
- **MCP 自动触发**: ArXiv、Memory、Tavily 等按关键词自动激活
- **技能自动触发**: Stata、DataPipeline、PolicyEval 按语义触发
- **外部大脑搜索**: 指定用 Grok/Gemini/小红书/B站 时自动打开
- **Chrome DevTools 专属浏览器**: HBW Launcher 管理，Google Scholar 镜像

### 其他组件

- **HBW Browser Launcher** (`~/hbw_launcher.sh`): Chrome DevTools 专属浏览器启动器
- **SessionStart Hook**: 自动启动浏览器
- **权限白名单**: 预配置常用工具权限，减少权限弹窗

## 目录结构

```
zhangjies-skills-and-mcp/
├── commands/          # 20个 Slash Commands
├── skills/            # 22个 Skills（含Python脚本）
├── glm-mcp-server/    # GLM-4V 图像分析 MCP Server
├── scripts/           # HBW Launcher 等辅助脚本
├── configs/           # 配置文件模板（需替换API Key）
│   ├── settings.json
│   ├── settings.local.json
│   ├── mcp.json
│   └── CLAUDE.md
├── install.sh         # 一键安装脚本
└── README.md
```

## 自定义模型配置

默认配置使用火山引擎(Volces/Ark) API 代理，映射如下：
- Opus → kimi-k2.6
- Sonnet → minimax-m2.7
- Haiku → glm-5.1

如使用 Anthropic 官方 API，删除 `ANTHROPIC_BASE_URL` 和 `ANTHROPIC_AUTH_TOKEN` 即可。

## License

MIT
