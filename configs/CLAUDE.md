# Project Rules

## Image Auto-Analysis

When the user uploads, pastes, or references an image file (PNG, JPG, JPEG, GIF, WebP, BMP, etc.), you MUST proactively analyze the image BEFORE responding to anything else.

Rules:
- Do NOT wait for the user to explicitly ask you to analyze the image.
- As soon as you detect an image in the conversation, immediately analyze it.
- If the active model supports image input (e.g., kimi-k2.6), use native vision capabilities.
- If the active model does NOT support image input (e.g., GLM-5.1), invoke `mcp__glm-mcp__analyze_image` to analyze the image.
- Provide a comprehensive analysis including: visual content description, text/OCR extraction, key elements, data/charts interpretation, and relevant insights.
- If the image contains code, diagrams, charts, documents, or screenshots, extract and interpret all meaningful information from it.
- After analyzing, naturally continue with whatever task the user requested.

## Auto Style Learning for Writing Tasks

When the user requests ANY writing task, you MUST automatically check and activate the style learning system BEFORE generating writing content.

### What counts as a writing task (auto-detection triggers)
- Academic writing: paper drafting, research background, literature review, methodology, results discussion
- Thesis or dissertation sections
- Policy reports, government documents
- Research proposals, grant applications
- Any request containing keywords like: "写一段", "帮我写", "draft", "write", "撰写", "拟写", "写作", "论文", "报告"

### Auto-trigger workflow (MANDATORY - execute before writing)

**Step 1: Check for existing style profile**
1. Look for `.claude/style-profile.md` in the current working directory
2. Look for files in `~/writing/style-profiles/`
3. Check if `/style-learn` was already run in this session

**Step 2: If NO style profile found → Auto-prompt**
Before generating any writing content, ask the user:
> "检测到写作任务。是否需要先从参考文献库学习写作风格？
> - 指定一个本地文件夹路径，我会分析里面所有文章的风格
> - 或者指定 Zotero 集合名称，我从 Zotero 中提取
> - 回复「跳过」则使用通用学术风格（含去AI味规则）"

**Step 3: If user provides reference source → Auto-execute style-learn**
Automatically run the full style learning workflow:
1. Read all documents from the specified source (folder or Zotero collection)
2. Deep-analyze writing patterns (sentence structure, vocabulary, paragraph organization, argumentation flow)
3. Generate a style profile and save to `.claude/style-profile.md` in the current project
4. Briefly summarize the key style findings to the user

**Step 4: Write with style profile**
After loading (or creating) the style profile, write following ALL rules in the profile:
- Use ONLY vocabulary from the whitelist, NEVER use blacklist words
- Match sentence length distribution from the profile
- Follow paragraph templates and transition patterns
- Apply the "de-AI-flavor" checklist before delivering
- Give a style match score (1-10) after writing

### Style profile location convention
- Per-project: `{project_root}/.claude/style-profile.md`
- Global profiles: `~/writing/style-profiles/{name}.md`
- When in a git repo, store in the project's `.claude/` directory

### Session memory
- If the user already provided a style source in the current session, do NOT ask again
- If the user said "skip" in the current session, do NOT ask again for the same writing task
- If the user switches to a different writing topic/genre, re-prompt

### De-AI-flavor universal rules (always apply, even without style profile)
Chinese banned phrases: "值得注意的是", "总的来说", "综上所述", "不可忽视", "至关重要", "毋庸置疑", "近年来", "随着...的发展", "扮演着重要角色", "发挥着不可或缺的作用", "具有重要意义", "深入探讨"
English banned phrases: "It is worth noting that", "In conclusion", "plays a crucial/vital role", "It is important to note", "In today's world", "delve into", "tapestry", "landscape", "realm", "beacon", "navigating the complexities", "pivotal", "multifaceted", "underscores", "underscores the importance"

## MCP Auto-Trigger Rules (MCP 自动触发规则)

### ArXiv MCP
- When the user asks about a specific paper by title, DOI, or arXiv ID → search ArXiv first
- When the user mentions "arxiv", "论文预印本", "working paper" → use ArXiv MCP
- When doing literature review, supplement with ArXiv search for recent preprints

### Sequential Thinking MCP
- When the user asks complex multi-step reasoning questions → use sequential thinking for structured analysis
- When the task involves debugging complex logic, architectural decisions, or trade-off analysis → chain thoughts explicitly
- NOT needed for simple Q&A or straightforward tasks

### Memory MCP
- When the user says "记住", "remember", "save this", "记下来" → store to Memory MCP as structured knowledge graph
- When the user asks "你还记得", "之前我们", "上次" → search Memory MCP for related entities
- Memory MCP stores entities and relations as a knowledge graph, complementing file-based memory

### Tavily Search
- When web search is needed → prefer Tavily MCP (search, extract, map, crawl tools)
- For deep research on a topic → use Tavily extract to get full page content
- For site-level discovery → use Tavily map to list URLs
- For bulk content collection → use Tavily crawl

## Skill Auto-Trigger Rules (技能自动触发规则)

### Stata 计量分析 (`/stata`)
- Keywords: 回归, DID, SDM, 面板数据, 固定效应, 工具变量, PSM, 稳健性检验, 计量, 实证
- When the user asks about econometric methods or needs Stata code → auto-trigger `/stata`
- When user shares regression results asking for interpretation → trigger for context

### Data Pipeline (`/datapipeline`)
- Keywords: 数据处理, 清洗, 合并, 去重, 面板构建, 特征工程, 批量处理, pandas
- When the user needs to clean/transform/process datasets → auto-trigger `/datapipeline`
- When user asks to build panel data or merge multiple CSVs → trigger

### Policy Evaluation (`/policy-eval`)
- Keywords: 政策评估, 政策强度, LLM评估, 政策文本分析, 政策打分, OIST
- When the user needs to evaluate policy documents → auto-trigger `/policy-eval`
- When user discusses policy intensity measurement or LLM-based assessment → trigger

## External Brain Search (外部大脑搜索)

When the user **explicitly specifies** to search using an external brain (e.g., "用Grok搜一下", "去小红书查", "用外部大脑搜"), use Chrome DevTools MCP to open and search the specified site.

### External Brain Options

| External Brain | Best for | URL Pattern |
|---------------|----------|-------------|
| **Grok** (x.com/xai) | Technical experience, real-time info, high accuracy | grok.com or x.com |
| **Gemini** (gemini.google.com) | Deep reasoning, professional knowledge | gemini.google.com |
| **小红书** (xiaohongshu.com) | Chinese experience sharing, lifestyle, tips | xiaohongshu.com |
| **哔哩哔哩** (bilibili.com) | Video tutorials, hands-on demos | bilibili.com |

### Rules
- **Default**: Use built-in WebSearch for normal searches. No need to open external brains.
- **Triggered only when user specifies**: e.g., "用Grok搜", "去小红书查一下", "让Gemini帮我看看", "外部大脑搜"
- User picks which brain to use → open it via Chrome DevTools and execute the search there.
- These sites are already logged in on the user's browser.

## Chrome DevTools 专属浏览器规则 (全局强制)

### 启动规则
- **唯一启动方式**: `bash ~/hbw_launcher.sh`（HBW Browser Launcher v3.1）
- **禁止手动启动**: 绝不使用 `open -na "Google Chrome" --args --remote-debugging-port=...` 手动启动
- **端口**: 9222
- **配置文件**: `~/.gemini/chrome_hbw_profile`（持久化登录状态）
- **已配置 Hook**: SessionStart 自动执行 `bash ~/hbw_launcher.sh`

### 使用前检查
每次需要使用 Chrome DevTools MCP 时，必须先确认专属浏览器是否在运行：
1. 检查 `curl -s http://127.0.0.1:9222/json/version` 是否响应
2. 如果无响应 → 运行 `bash ~/hbw_launcher.sh`
3. 如果仍然失败 → `pkill -9 -f "Google Chrome"` → 清理 `~/.gemini/chrome_hbw_profile/Singleton*` → 再运行 `bash ~/hbw_launcher.sh`

### Google Scholar 镜像网站
官方 `scholar.google.com` 可能无法访问，按以下顺序使用镜像：
1. **推荐**: `https://xs.gupiaoq.com/`（最佳兼容性，支持BibTeX）
2. **优先**: `https://scholar.lanfanshu.cn/`（稳定，引用弹窗需口令）
3. **备选**: `https://so.6465.net/` / `https://so.673.org/` / `https://sci.673.org/`
4. **备选**: `https://scholar.aigrogu.com/` / `https://www.defineabc.com/`

### Chrome DevTools 文件上传工作流

向外部大脑（Gemini/Grok等）上传本地文件时，按以下优先级选择方法：

**方法1：`upload_file` 直接上传（适用于标准网站）**
```
1. take_snapshot → 找到文件上传按钮的 uid
2. upload_file(uid="...", filePath="/absolute/path/to/file")
3. 如果成功 → 完成
4. 如果失败（"could not accept file directly"）→ 进入方法2
```

**方法2：暴露隐藏 input 后 `upload_file`（适用于隐藏 file input 的网站）**
```
1. evaluate_script: 找到并暴露隐藏的 <input type="file">
   () => {
     const input = document.querySelector('input[type="file"]');
     if (!input) return 'No file input found';
     input.style.cssText = 'position:fixed; left:10px; top:10px; width:200px; height:30px; display:block !important; opacity:1; z-index:99999;';
     input.removeAttribute('hidden');
     return 'File input exposed';
   }
2. take_snapshot → 获取暴露后的 input uid
3. upload_file(uid="新uid", filePath="...")
```

**方法3：DataTransfer API + click拦截（适用于 Gemini 等动态创建 file input 的网站）**
```
1. 用 Bash 读取文件为 base64: base64 -i /path/to/file | tr -d '\n'
2. evaluate_script 执行以下逻辑:
   async () => {
     const base64Content = "上一步获取的base64字符串";
     const mimeType = "application/pdf";  // 按需调整
     const fileName = "document.pdf";      // 按需调整
     const byteCharacters = atob(base64Content);
     const byteArray = new Uint8Array(byteCharacters.length);
     for (let i = 0; i < byteCharacters.length; i++) byteArray[i] = byteCharacters.charCodeAt(i);
     const file = new File([byteArray], fileName, { type: mimeType });
     // 拦截 input.click() 阻止 OS 文件选择器
     const origClick = HTMLInputElement.prototype.click;
     HTMLInputElement.prototype.click = function() {
       if (this.type === 'file') {
         const dt = new DataTransfer(); dt.items.add(file); this.files = dt.files;
         this.dispatchEvent(new Event('change', { bubbles: true }));
         HTMLInputElement.prototype.click = origClick;
         return;
       }
       return origClick.call(this);
     };
     // 点击上传按钮触发拦截
     const btn = document.querySelector('[aria-label*="Upload"]') || document.querySelector('[aria-label*="file"]');
     if (btn) { btn.click(); return 'File injected via interceptor'; }
     HTMLInputElement.prototype.click = origClick;
     return 'Upload button not found';
   }
```

**方法4：剪贴板粘贴（适用于支持粘贴上传的聊天界面，如 Gemini）**
```
1. 读取文件为 base64
2. evaluate_script: 构造 File → DataTransfer → ClipboardEvent('paste') → dispatch 到 textarea
```

**选择规则**:
- 有明确 `<input type="file">` → 方法1或2
- Gemini 等动态上传 → 方法3（最可靠）
- 图片粘贴 → 方法4
- 大文件(>10MB) → 不建议上传，改用文字描述
