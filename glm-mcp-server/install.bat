@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

title GLM MCP Server 一键安装
color 0A

echo.
echo ========================================
echo      GLM MCP Server 一键安装工具
echo ========================================
echo.

cd /d "%~dp0"

echo [1/5] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.10+
    echo 下载地址：https://www.python.org/downloads/
    echo 请确保安装时勾选"Add Python to PATH"
    pause
    exit /b 1
)
for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PY_VER=%%v
echo [OK] Python %PY_VER%

echo.
echo [2/5] 安装Python依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo [警告] 部分依赖包安装失败，请检查网络连接
    echo 可以手动运行：pip install -r requirements.txt
    pause
)

echo.
echo [3/5] 配置GLM API密钥...
if not exist .env (
    echo.
    echo 请从智谱AI控制台获取您的API密钥：https://open.bigmodel.cn/console
    echo.
    set /p GLM_API_KEY=请输入您的GLM API密钥：

    if "!GLM_API_KEY!"=="" (
        echo [错误] API密钥不能为空
        pause
        exit /b 1
    )

    (
        echo # GLM MCP Server Configuration
        echo GLM_API_KEY=!GLM_API_KEY!
        echo GLM_API_BASE=https://open.bigmodel.cn/api/paas/v4/
        echo GLM_IMAGE_MODEL=glm-4.6v
    ) > .env
    echo [OK] .env 配置文件已创建
) else (
    echo [OK] .env 配置文件已存在
)

echo.
echo [4/5] 配置Claude Code MCP服务器...
set CLAUDE_CONFIG_DIR=%USERPROFILE%\.claude
if not exist "%CLAUDE_CONFIG_DIR%" (
    echo [错误] 未检测到Claude Code配置目录
    echo 请确保已安装 Claude Code
    pause
    exit /b 1
)

:: 使用Python生成.mcp.json（确保JSON格式正确）
python -c "
import json, os
script_dir = r'%~dp0'.replace('\\\\', '/')
script_dir = script_dir.rstrip('/')
mcp_config = {
    'mcpServers': {
        'glm-mcp': {
            'command': 'python',
            'args': [script_dir + '/glm_fastmcp_server.py'],
            'env': {
                'GLM_API_BASE': 'https://open.bigmodel.cn/api/paas/v4/',
                'GLM_IMAGE_MODEL': 'glm-4.6v'
            }
        }
    }
}
with open('.mcp.json', 'w', encoding='utf-8') as f:
    json.dump(mcp_config, f, indent=2, ensure_ascii=False)
print('OK')
"
if errorlevel 1 (
    echo [错误] MCP配置文件创建失败
    pause
    exit /b 1
)
echo [OK] .mcp.json 配置文件已创建

echo.
echo [5/5] 配置Claude Code权限...
set SETTINGS_FILE=.claude\settings.json

if not exist ".claude" mkdir .claude

python -c "
import json, os
settings_file = r'.claude\settings.json'

try:
    with open(settings_file, 'r', encoding='utf-8') as f:
        settings = json.load(f)
except:
    settings = {}

if 'permissions' not in settings:
    settings['permissions'] = {'allow': [], 'deny': []}

tool_name = 'mcp__glm-mcp__analyze_image'
if tool_name not in settings['permissions'].get('allow', []):
    if 'allow' not in settings['permissions']:
        settings['permissions']['allow'] = []
    settings['permissions']['allow'].append(tool_name)

with open(settings_file, 'w', encoding='utf-8') as f:
    json.dump(settings, f, indent=2, ensure_ascii=False)
print('OK')
"
echo [OK] 权限配置已更新

echo.
echo ========================================
echo             安装完成！
echo ========================================
echo.
echo 后续步骤：
echo 1. 在 Claude Code 中打开此项目目录
echo 2. 输入"分析 ./03.jpg" 测试图像分析功能
echo 3. 日志文件位置：%~dp0mcpserver.log
echo.
echo 如需更新API密钥，编辑项目根目录的 .env 文件
echo.
pause
