@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set SETTINGS=%USERPROFILE%\.claude\settings.json

echo.
echo ========================================
echo    图片分析 MCP 切换工具
echo ========================================
echo.
echo 当前状态：

:: 检查 deny 中是否有 4_5v 规则
findstr /c:"4_5v" "%SETTINGS%" >nul 2>&1
if !errorlevel! equ 0 (
    echo   [√] glm-mcp 本地版 - 已启用
    echo   [×] 云端 4_5v_mcp - 已禁用
) else (
    echo   [×] glm-mcp 本地版 - 可用
    echo   [√] 云端 4_5v_mcp - 可用
)

echo.
echo 请选择：
echo   1. 使用 glm-mcp（本地模型，推荐）
echo   2. 使用云端 4_5v_mcp（云端模型）
echo   3. 两者都允许（Claude 自动选择）
echo   4. 退出
echo.

set /p choice=请输入选项 (1-4):

if "%choice%"=="1" goto :use_glm
if "%choice%"=="2" goto :use_builtin
if "%choice%"=="3" goto :use_both
if "%choice%"=="4" exit /b 0
echo 无效选项
pause
exit /b 1

:use_glm
echo.
echo 正在切换到 glm-mcp（本地模型）...
python -c "
import json
with open(r'%SETTINGS%', 'r', encoding='utf-8') as f:
    data = json.load(f)
perms = data.setdefault('permissions', {})
deny = perms.setdefault('deny', [])
to_add = ['mcp__4_5v_mcp__analyze_image', 'mcp__4_5v_mcp__*']
for item in to_add:
    if item not in deny:
        deny.append(item)
# 确保 glm-mcp 不在 deny 中
allow = perms.get('allow', [])
if 'mcp__glm-mcp__analyze_image' not in allow:
    allow.append('mcp__glm-mcp__analyze_image')
with open(r'%SETTINGS%', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print('[OK] 已切换到 glm-mcp（本地模型）')
print('  - glm-mcp: 已启用')
print('  - 云端 4_5v_mcp: 已禁用')
"
echo.
echo 请重启 Claude Code 使配置生效
pause
exit /b 0

:use_builtin
echo.
echo 正在切换到云端 4_5v_mcp（云端模型）...
python -c "
import json
with open(r'%SETTINGS%', 'r', encoding='utf-8') as f:
    data = json.load(f)
perms = data.setdefault('permissions', {})
deny = perms.setdefault('deny', [])
# 禁用 glm-mcp
to_add = ['mcp__glm-mcp__analyze_image', 'mcp__glm-mcp__*']
for item in to_add:
    if item not in deny:
        deny.append(item)
# 移除 4_5v 的 deny 规则
deny[:] = [x for x in deny if '4_5v' not in x and '4.5v' not in x]
with open(r'%SETTINGS%', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print('[OK] 已切换到云端 4_5v_mcp（云端模型）')
print('  - glm-mcp: 已禁用')
print('  - 云端 4_5v_mcp: 已启用')
"
echo.
echo 请重启 Claude Code 使配置生效
pause
exit /b 0

:use_both
echo.
echo 正在设置为两者都允许...
python -c "
import json
with open(r'%SETTINGS%', 'r', encoding='utf-8') as f:
    data = json.load(f)
perms = data.setdefault('permissions', {})
deny = perms.setdefault('deny', [])
# 移除所有图片分析相关的 deny 规则
deny[:] = [x for x in deny if '4_5v' not in x and '4.5v' not in x and 'glm-mcp' not in x and 'analyze_image' not in x]
# 确保 allow 中都有
allow = perms.get('allow', [])
for item in ['mcp__glm-mcp__analyze_image']:
    if item not in allow:
        allow.append(item)
with open(r'%SETTINGS%', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print('[OK] 两者都允许')
print('  - glm-mcp: 已启用')
print('  - 云端 4_5v_mcp: 已启用')
print('  Claude 将根据上下文自动选择')
"
echo.
echo 请重启 Claude Code 使配置生效
pause
exit /b 0
