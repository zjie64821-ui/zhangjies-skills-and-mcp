#!/bin/bash

# GLM MCP Server 安装测试脚本
# 适用于 Linux 和 macOS

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================"
echo -e "     GLM MCP Server 安装测试工具"
echo -e "========================================${NC}"
echo

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${YELLOW}[测试1] 检查Python环境...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo -e "${GREEN}[成功] Python3已安装: $(python3 --version)${NC}"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    echo -e "${GREEN}[成功] Python已安装: $(python --version)${NC}"
else
    echo -e "${RED}[失败] Python未安装${NC}"
    exit 1
fi

echo
echo -e "${YELLOW}[测试2] 检查依赖包...${NC}"

# 检查zhipuai
if $PYTHON_CMD -c "import zhipuai" 2>/dev/null; then
    echo -e "${GREEN}[成功] zhipuai已安装${NC}"
else
    echo -e "${YELLOW}[警告] zhipuai未安装${NC}"
fi

# 检查mcp
if $PYTHON_CMD -c "import mcp" 2>/dev/null; then
    echo -e "${GREEN}[成功] mcp已安装${NC}"
else
    echo -e "${YELLOW}[警告] mcp未安装${NC}"
fi

# 检查dotenv
if $PYTHON_CMD -c "import dotenv" 2>/dev/null; then
    echo -e "${GREEN}[成功] dotenv已安装${NC}"
else
    echo -e "${YELLOW}[警告] dotenv未安装${NC}"
fi

echo
echo -e "${YELLOW}[测试3] 检查配置文件...${NC}"
if [[ -f ".env" ]]; then
    echo -e "${GREEN}[信息] .env文件存在${NC}"
    echo "GLM_API_KEY配置: $(grep GLM_API_KEY .env || echo '未设置')"
else
    echo -e "${YELLOW}[信息] .env文件不存在${NC}"
fi

echo
echo -e "${YELLOW}[测试4] 检查MCP配置...${NC}"
CLAUDE_CONFIG_DIR="$HOME/.claude"
if [[ -f "$CLAUDE_CONFIG_DIR/mcp.json" ]]; then
    echo -e "${GREEN}[信息] MCP配置文件存在${NC}"
    if grep -q "glm-mcp" "$CLAUDE_CONFIG_DIR/mcp.json"; then
        echo -e "${GREEN}[成功] glm-mcp配置已找到${NC}"
        echo "配置路径: $(grep -A 1 '"args"' "$CLAUDE_CONFIG_DIR/mcp.json" | head -1)"
    else
        echo -e "${YELLOW}[警告] glm-mcp配置未找到${NC}"
    fi
else
    echo -e "${YELLOW}[信息] MCP配置文件不存在${NC}"
fi

echo
echo -e "${YELLOW}[测试5] 检查环境变量...${NC}"
echo "GLM_API_KEY: ${GLM_API_KEY:+已设置}"
echo "GLM_API_BASE: ${GLM_API_BASE:-未设置}"
echo "GLM_IMAGE_MODEL: ${GLM_IMAGE_MODEL:-未设置}"

echo
echo -e "${YELLOW}[测试6] 测试配置加载...${NC}"
if $PYTHON_CMD -c "from config import config; print('配置加载测试通过'); print('API Key:', '设置' if config.glm_api_key else '未设置'); print('API Base:', config.glm_api_base); print('Model:', config.glm_image_model)" 2>/dev/null; then
    echo -e "${GREEN}[成功] 配置加载测试通过${NC}"
else
    echo -e "${RED}[失败] 配置加载测试失败${NC}"
fi

echo
echo -e "${YELLOW}[测试7] 检查文件权限...${NC}"
if [[ -x "install.sh" ]]; then
    echo -e "${GREEN}[成功] install.sh有执行权限${NC}"
else
    echo -e "${YELLOW}[警告] install.sh没有执行权限${NC}"
    echo "运行: chmod +x install.sh"
fi

if [[ -x "main.py" ]]; then
    echo -e "${GREEN}[成功] main.py有执行权限${NC}"
else
    echo -e "${YELLOW}[信息] main.py没有执行权限（可选）${NC}"
fi

echo
echo -e "${BLUE}========================================"
echo -e "             测试完成！"
echo -e "========================================${NC}"
echo

# 提供后续步骤建议
echo -e "${YELLOW}后续步骤建议：${NC}"
echo "1. 如果所有依赖都已安装，可以直接运行: ./install.sh"
echo "2. 如果有缺失的依赖，请先安装: pip install zhipuai mcp python-dotenv"
echo "3. 确保 Claude Code 已安装并正常运行"
echo "4. 安装完成后，重启 Claude Code 使配置生效"

echo
echo -e "${GREEN}测试脚本执行完成！${NC}"