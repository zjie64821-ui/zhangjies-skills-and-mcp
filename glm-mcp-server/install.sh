#!/bin/bash

# GLM MCP Server 一键安装脚本
# 适用于 Linux 和 macOS

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================"
echo -e "     GLM MCP Server 一键安装工具"
echo -e "========================================${NC}"
echo

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查Python环境
echo -e "${YELLOW}[1/6] 检查Python环境...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[错误] 未检测到Python3，请先安装Python3${NC}"
    echo "Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip"
    echo "CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "macOS: brew install python3"
    exit 1
fi
echo -e "${GREEN}[✓] Python3环境正常${NC}"

# 检查pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}[警告] 未检测到pip3，尝试安装...${NC}"
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install python3-pip -y
    elif command -v yum &> /dev/null; then
        sudo yum install python3-pip -y
    elif command -v brew &> /dev/null; then
        brew install python3
    fi
fi

# 检查Claude Code配置
echo
echo -e "${YELLOW}[2/6] 检查Claude Code配置...${NC}"
CLAUDE_CONFIG_DIR="$HOME/.claude"
if [[ ! -d "$CLAUDE_CONFIG_DIR" ]]; then
    echo -e "${RED}[错误] 未检测到Claude Code配置目录${NC}"
    echo "请确保已安装Claude Code"
    exit 1
fi
echo -e "${GREEN}[✓] Claude Code配置目录存在${NC}"

# 安装Python依赖包
echo
echo -e "${YELLOW}[3/6] 安装Python依赖包...${NC}"
echo "正在安装：zhipuai mcp python-dotenv"
pip3 install --user zhipuai mcp python-dotenv
if [[ $? -ne 0 ]]; then
    echo -e "${YELLOW}[警告] 部分依赖包安装失败，请检查网络连接${NC}"
    echo "可以手动运行：pip3 install --user zhipuai mcp python-dotenv"
fi
echo -e "${GREEN}[✓] 依赖包安装完成${NC}"

# 配置GLM API密钥
echo
echo -e "${YELLOW}[4/6] 配置GLM API密钥...${NC}"
echo
echo "请从智谱AI控制台获取您的API密钥：https://open.bigmodel.cn/console"
echo

# 检查是否已配置API密钥
if [[ -n "${GLM_API_KEY}" ]]; then
    echo -e "${GREEN}[信息] 检测到已配置的GLM_API_KEY：${GLM_API_KEY:0:10}...${NC}"
    API_KEY_CONFIGURED=1
else
    API_KEY_CONFIGURED=0
fi

if [[ $API_KEY_CONFIGURED -eq 0 ]]; then
    read -p "请输入您的GLM API密钥: " GLM_API_KEY_INPUT
    
    if [[ -z "$GLM_API_KEY_INPUT" ]]; then
        echo -e "${RED}[错误] API密钥不能为空${NC}"
        exit 1
    fi
    
    # 根据操作系统设置环境变量
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        SHELL_CONFIG="$HOME/.zshrc"
        if [[ ! -f "$SHELL_CONFIG" ]]; then
            SHELL_CONFIG="$HOME/.bashrc"
        fi
        
        echo "export GLM_API_KEY=\"$GLM_API_KEY_INPUT\"" >> "$SHELL_CONFIG"
        echo "export GLM_API_BASE=\"https://open.bigmodel.cn/api/paas/v4/\"" >> "$SHELL_CONFIG"
        echo "export GLM_IMAGE_MODEL=\"glm-4.6v\"" >> "$SHELL_CONFIG"
        
        echo -e "${GREEN}[✓] API密钥已保存到 $SHELL_CONFIG${NC}"
        echo "请运行以下命令使配置生效："
        echo "source $SHELL_CONFIG"
        
    else
        # Linux
        SHELL_CONFIG="$HOME/.bashrc"
        if [[ ! -f "$SHELL_CONFIG" ]]; then
            SHELL_CONFIG="$HOME/.profile"
        fi
        
        echo "export GLM_API_KEY=\"$GLM_API_KEY_INPUT\"" >> "$SHELL_CONFIG"
        echo "export GLM_API_BASE=\"https://open.bigmodel.cn/api/paas/v4/\"" >> "$SHELL_CONFIG"
        echo "export GLM_IMAGE_MODEL=\"glm-4.6v\"" >> "$SHELL_CONFIG"
        
        echo -e "${GREEN}[✓] API密钥已保存到 $SHELL_CONFIG${NC}"
        echo "请运行以下命令使配置生效："
        echo "source $SHELL_CONFIG"
    fi
    
    # 立即设置当前会话的环境变量
    export GLM_API_KEY="$GLM_API_KEY_INPUT"
    export GLM_API_BASE="https://open.bigmodel.cn/api/paas/v4/"
    export GLM_IMAGE_MODEL="glm-4.6v"
    
else
    echo -e "${GREEN}[✓] API密钥已配置，跳过设置步骤${NC}"
fi

# 配置Claude MCP服务器
echo
echo -e "${YELLOW}[5/6] 配置Claude MCP服务器...${NC}"
MCP_CONFIG_FILE="$CLAUDE_CONFIG_DIR/mcp.json"

# 创建MCP配置文件
cat > "$MCP_CONFIG_FILE" << EOF
{
  "mcpServers": {
    "glm-mcp": {
      "command": "python3",
      "args": ["$SCRIPT_DIR/main.py"],
      "env": {
        "GLM_API_BASE": "https://open.bigmodel.cn/api/paas/v4/",
        "GLM_IMAGE_MODEL": "glm-4.6v"
      }
    }
  }
}
EOF

echo -e "${GREEN}[✓] MCP配置文件已创建：$MCP_CONFIG_FILE${NC}"

# 更新Claude Code权限配置
echo
echo -e "${YELLOW}[6/6] 更新Claude Code权限配置...${NC}"
SETTINGS_FILE="$CLAUDE_CONFIG_DIR/settings.json"

# 检查settings.json是否存在，不存在则创建
if [[ ! -f "$SETTINGS_FILE" ]]; then
    cat > "$SETTINGS_FILE" << EOF
{
  "\$schema": "https://json.schemastore.org/claude-code-settings.json",
  "env": {},
  "includeCoAuthoredBy": false,
  "permissions": {
    "allow": [],
    "deny": []
  },
  "hooks": {}
}
EOF
fi

# 备份原文件
cp "$SETTINGS_FILE" "$SETTINGS_FILE.backup" 2>/dev/null || true

# 使用Python来正确处理JSON
python3 -c "
import json
import os

settings_file = '$SETTINGS_FILE'

# 读取现有配置
try:
    with open(settings_file, 'r', encoding='utf-8') as f:
        settings = json.load(f)
except:
    settings = {}

# 确保permissions结构存在
if 'permissions' not in settings:
    settings['permissions'] = {'allow': [], 'deny': []}

# 添加glm-mcp权限
if 'mcp__glm-mcp__read_image' not in settings['permissions']['allow']:
    settings['permissions']['allow'].append('mcp__glm-mcp__read_image')

# 写入文件
with open(settings_file, 'w', encoding='utf-8') as f:
    json.dump(settings, f, indent=2, ensure_ascii=False)

print('Settings updated successfully')
"

echo -e "${GREEN}[✓] Claude Code权限配置已更新${NC}"

# 完成提示
echo
echo -e "${BLUE}========================================"
echo -e "             安装完成！"
echo -e "========================================${NC}"
echo
echo -e "${YELLOW}重要提示：${NC}"
echo "1. 请重新启动Claude Code以使配置生效"
echo "2. 重启后，您可以在任何项目中使用 @图像 来分析图片"
echo "3. 如需更新API密钥，请修改环境变量 GLM_API_KEY"
echo "4. 日志文件位置：$SCRIPT_DIR/mcpserver.log"
echo
if [[ $API_KEY_CONFIGURED -eq 0 ]]; then
    echo -e "${YELLOW}请重新打开终端或运行 source $SHELL_CONFIG 使环境变量生效${NC}"
fi
echo
echo -e "${GREEN}安装完成！感谢使用 GLM MCP Server！${NC}"