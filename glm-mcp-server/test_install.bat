@echo off
chcp 65001 >nul
echo ========================================
echo      GLM MCP Server 安装验证
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] 检查Python依赖...
python -c "import zhipuai; print('[OK] zhipuai ' + zhipuai.__version__)" 2>nul || echo [FAIL] zhipuai 未安装
python -c "import mcp; print('[OK] mcp')" 2>nul || echo [FAIL] mcp 未安装
python -c "import dotenv; print('[OK] python-dotenv')" 2>nul || echo [FAIL] python-dotenv 未安装

echo.
echo [2/4] 检查配置文件...
if exist .env (
    echo [OK] .env 文件存在
    python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('  API Key:', '已设置' if os.getenv('GLM_API_KEY') else '未设置'); print('  API Base:', os.getenv('GLM_API_BASE', '默认值')); print('  Model:', os.getenv('GLM_IMAGE_MODEL', '默认值'))"
) else (
    echo [FAIL] .env 文件不存在，请运行 install.bat
)

echo.
if exist .mcp.json (
    echo [OK] .mcp.json 文件存在
) else (
    echo [FAIL] .mcp.json 文件不存在
)

echo.
echo [3/4] 检查MCP服务器模块...
python -c "from mcp.server.fastmcp import FastMCP; print('[OK] FastMCP 可用')" 2>nul || echo [FAIL] FastMCP 不可用
python -c "import glm_fastmcp_server; print('[OK] glm_fastmcp_server 模块可加载')" 2>nul || echo [FAIL] glm_fastmcp_server 模块加载失败

echo.
echo [4/4] 测试API连接...
python -c "
from dotenv import load_dotenv
load_dotenv()
import os
from zhipuai import ZhipuAI
client = ZhipuAI(api_key=os.getenv('GLM_API_KEY'), base_url=os.getenv('GLM_API_BASE', 'https://open.bigmodel.cn/api/paas/v4/'))
resp = client.chat.completions.create(model='glm-4-flash', messages=[{'role':'user','content':'hi'}], max_tokens=10)
print('[OK] API连接正常，模型响应:', resp.choices[0].message.content)
" 2>nul || echo [FAIL] API连接失败，请检查API密钥

echo.
echo ========================================
echo        验证完成
echo ========================================
pause
