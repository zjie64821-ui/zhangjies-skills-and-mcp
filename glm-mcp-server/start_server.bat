@echo off
title GLM MCP Server Launcher
color 0A

echo.
echo ========================================
echo    GLM MCP Server Launcher
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] Checking Python environment...
python --version
if errorlevel 1 (
    echo [ERROR] Python not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python environment is normal

echo.
echo [2/4] Installing dependencies...
echo Installing required packages: zhipuai, mcp, python-dotenv
pip install -r requirements.txt
if errorlevel 1 (
    echo [WARNING] Some packages may have failed to install
    echo Please check the error messages above
    echo You can try manual installation: pip install zhipuai mcp python-dotenv
)

echo.
echo [3/4] Checking configuration file...
if not exist .env (
    echo [INFO] Configuration file not found, creating...
    if exist .env.template (
        copy .env.template .env
        echo.
        echo [IMPORTANT] Please edit .env file to set your GLM API key
        echo.
        notepad .env
        echo.
        echo Please run this script again after configuration
        pause
        exit /b 1
    ) else (
        echo [ERROR] .env.template file not found
        pause
        exit /b 1
    )
)
echo [OK] Configuration file exists

echo.
echo [3.5/4] Validating API key configuration...
python -c "from config import config; print('API Key:', '✓ Set' if config.glm_api_key else '✗ Missing'); print('API Base:', config.glm_api_base); print('Model:', config.glm_image_model)"
if errorlevel 1 (
    echo [WARNING] Configuration validation failed
    echo Please check your .env file and ensure GLM_API_KEY is set
    echo Current configuration:
    type .env
    echo.
    echo Would you like to edit the configuration now? (Y/N)
    set /p choice=
    if /i "%choice%"=="Y" (
        notepad .env
        echo Please run this script again after configuration
        pause
        exit /b 1
    )
)

echo.
echo [4/4] Starting server...
echo.
echo ========================================
echo    Server is starting, please wait...
echo    Press Ctrl+C to stop server
echo ========================================
echo.

python main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Server exited abnormally
    echo Please check console output for error information
) else (
    echo.
    echo Server stopped normally
)

pause