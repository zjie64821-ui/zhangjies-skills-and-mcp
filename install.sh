#!/bin/bash
# ============================================================
#  Claude Code 一键复刻安装脚本
#  将 Zhangjie 的 Skills + MCP + 配置安装到你的 Claude Code
# ============================================================

set -e

CLAUDE_DIR="$HOME/.claude"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "============================================"
echo "  Claude Code 配置一键安装"
echo "  Skills: 22 | MCP: 自定义GLM图像分析"
echo "============================================"
echo ""

# 0. 检查 Claude Code 是否已安装
if ! command -v claude &>/dev/null; then
    echo "⚠️  未检测到 Claude Code CLI，请先安装: https://docs.anthropic.com/en/docs/claude-code"
    echo "   macOS: npm install -g @anthropic-ai/claude-code"
    exit 1
fi
echo "✅ Claude Code 已安装"

# 1. 创建目标目录
echo ""
echo "📁 创建目录结构..."
mkdir -p "$CLAUDE_DIR/commands"
mkdir -p "$CLAUDE_DIR/skills"
mkdir -p "$CLAUDE_DIR/glm-mcp-server"
mkdir -p "$HOME/.gemini/chrome_hbw_profile"
mkdir -p "$HOME/writing/style-profiles"

# 2. 复制 Commands (Slash Commands)
echo "📋 安装 Slash Commands (20个)..."
cp -r "$SCRIPT_DIR/commands/"* "$CLAUDE_DIR/commands/" 2>/dev/null || true
CMD_COUNT=$(ls "$CLAUDE_DIR/commands/"*.md 2>/dev/null | wc -l | tr -d ' ')
echo "   ✅ 已安装 $CMD_COUNT 个命令"

# 3. 复制 Skills
echo "🛠️  安装 Skills (22个)..."
cp -r "$SCRIPT_DIR/skills/"* "$CLAUDE_DIR/skills/" 2>/dev/null || true
SKILL_COUNT=$(ls -d "$CLAUDE_DIR/skills/"*/ 2>/dev/null | wc -l | tr -d ' ')
echo "   ✅ 已安装 $SKILL_COUNT 个技能"

# 4. 复制 GLM MCP Server
echo "🤖 安装 GLM 图像分析 MCP Server..."
cp -r "$SCRIPT_DIR/glm-mcp-server/"* "$CLAUDE_DIR/glm-mcp-server/" 2>/dev/null || true
cd "$CLAUDE_DIR/glm-mcp-server" && pip3 install -r requirements.txt -q 2>/dev/null || echo "   ⚠️  pip install 失败，请手动运行: cd ~/.claude/glm-mcp-server && pip3 install -r requirements.txt"
echo "   ✅ GLM MCP Server 已安装"

# 5. 复制 HBW Launcher
echo "🌐 安装 Chrome DevTools 浏览器启动器..."
cp "$SCRIPT_DIR/scripts/hbw_launcher.sh" "$HOME/hbw_launcher.sh"
chmod +x "$HOME/hbw_launcher.sh"
echo "   ✅ hbw_launcher.sh 已安装到 ~/"

# 6. 安装配置文件（仅在文件不存在时，避免覆盖已有配置）
echo ""
echo "⚙️  配置文件安装..."

install_config() {
    local src="$1"
    local dest="$2"
    local desc="$3"

    if [ -f "$dest" ]; then
        echo "   ⚠️  $desc 已存在，跳过（避免覆盖你的配置）"
        echo "      如需使用，请手动复制: cp $src $dest"
        echo "      然后替换其中的 YOUR_* 占位符为你的实际 API Key"
    else
        cp "$src" "$dest"
        echo "   ✅ $desc 已安装（请替换 YOUR_* 占位符为你的 API Key）"
    fi
}

install_config "$SCRIPT_DIR/configs/settings.json" "$CLAUDE_DIR/settings.json" "settings.json (全局设置)"
install_config "$SCRIPT_DIR/configs/settings.local.json" "$CLAUDE_DIR/settings.local.json" "settings.local.json (权限设置)"
install_config "$SCRIPT_DIR/configs/mcp.json" "$CLAUDE_DIR/mcp.json" "mcp.json (MCP服务器配置)"

# 7. 安装 CLAUDE.md (项目级指令)
if [ -f "$HOME/CLAUDE.md" ]; then
    echo "   ⚠️  ~/CLAUDE.md 已存在，跳过"
    echo "      如需使用，请手动: cp $SCRIPT_DIR/configs/CLAUDE.md ~/CLAUDE.md"
else
    cp "$SCRIPT_DIR/configs/CLAUDE.md" "$HOME/CLAUDE.md"
    echo "   ✅ CLAUDE.md 已安装到 ~/"
fi

# 8. 配置 SessionStart Hook (自动启动 HBW 浏览器)
echo ""
echo "🪝 配置 SessionStart Hook..."
if [ -f "$CLAUDE_DIR/settings.json" ]; then
    # 用 python3 来安全地修改 JSON
    python3 -c "
import json, sys
try:
    with open('$CLAUDE_DIR/settings.json', 'r') as f:
        s = json.load(f)
    if 'hooks' not in s:
        s['hooks'] = {}
    if 'SessionStart' not in s['hooks']:
        s['hooks']['SessionStart'] = [{'type': 'command', 'command': 'bash ~/hbw_launcher.sh'}]
        with open('$CLAUDE_DIR/settings.json', 'w') as f:
            json.dump(s, f, indent=2)
        print('   ✅ SessionStart Hook 已配置（自动启动 Chrome DevTools 浏览器）')
    else:
        print('   ⚠️  SessionStart Hook 已存在，跳过')
except Exception as e:
    print(f'   ⚠️  Hook 配置失败: {e}')
" 2>/dev/null || echo "   ⚠️  Hook 配置失败，请手动添加"
fi

# 9. 完成
echo ""
echo "============================================"
echo "  ✅ 安装完成！"
echo "============================================"
echo ""
echo "📋 接下来你需要手动完成以下步骤："
echo ""
echo "1️⃣  替换 API Key（在 ~/.claude/settings.json 中）："
echo "   - ANTHROPIC_AUTH_TOKEN: 你的 API Key"
echo "   - ANTHROPIC_BASE_URL: 你的 API 代理地址（或删除此行使用官方API）"
echo ""
echo "2️⃣  替换 GLM API Key（在 ~/.claude/mcp.json 中）："
echo "   - GLM_API_KEY: 在 https://open.bigmodel.cn/ 申请"
echo ""
echo "3️⃣  安装其他 MCP Server（可选，但强烈推荐）："
echo "   - Chrome DevTools: npx @anthropic-ai/chrome-devtools-mcp@latest"
echo "   - Zotero: npx zotero-mcp@latest"
echo "   - ArXiv: pip install arxiv-mcp-server"
echo "   - Tavily: npx tavily-mcp@latest"
echo "   - Memory: npx @anthropic-ai/memory-mcp@latest"
echo "   - Sequential Thinking: npx @anthropic-ai/sequential-thinking-mcp@latest"
echo "   - OpenAlex: pip install openalex-mcp"
echo "   详细说明见 README.md"
echo ""
echo "4️⃣  重启 Claude Code 使配置生效"
echo ""
echo "🎉 享受你的增强版 Claude Code！"
