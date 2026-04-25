#!/bin/bash

# GLM MCP Server 发布检查脚本

echo "🚀 GLM MCP Server 发布检查"
echo "================================"

# 检查必要文件
echo "📋 检查必要文件..."
required_files=(".gitignore" "LICENSE" "README.md" "CHANGELOG.md" "CONTRIBUTING.md" "PUBLISHING.md" "TESTING.md")
missing_files=()

for file in "${required_files[@]}"; do
    if [[ -f "$file" ]]; then
        echo "✅ $file"
    else
        echo "❌ $file 缺失"
        missing_files+=("$file")
    fi
done

# 检查脚本文件
echo
echo "📜 检查脚本文件..."
script_files=("install.bat" "install.sh" "test_install.bat" "test_install.sh" "verify_python_commands.sh")

for file in "${script_files[@]}"; do
    if [[ -f "$file" ]]; then
        if [[ "$file" == *.sh && -x "$file" ]]; then
            echo "✅ $file (有执行权限)"
        elif [[ "$file" == *.sh ]]; then
            echo "⚠️  $file (没有执行权限)"
        else
            echo "✅ $file"
        fi
    else
        echo "❌ $file 缺失"
        missing_files+=("$file")
    fi
done

# 检查Python文件
echo
echo "🐍 检查Python文件..."
python_files=("main.py" "config.py" "server.py" "image_processor.py" "logger.py" "utils.py")

for file in "${python_files[@]}"; do
    if [[ -f "$file" ]]; then
        echo "✅ $file"
    else
        echo "❌ $file 缺失"
        missing_files+=("$file")
    fi
done

# 检查其他文件
echo
echo "📦 检查其他文件..."
other_files=(".env.template" ".mcp.json" "requirements.txt")

for file in "${other_files[@]}"; do
    if [[ -f "$file" ]]; then
        echo "✅ $file"
    else
        echo "❌ $file 缺失"
        missing_files+=("$file")
    fi
done

# 检查敏感信息
echo
echo "🔒 检查敏感信息..."
if grep -r "GLM_API_KEY.*=[^[:space:]]" . --exclude-dir=.git --exclude="*.log" --exclude="temp_*" 2>/dev/null; then
    echo "⚠️  发现可能的敏感信息，请检查"
else
    echo "✅ 未发现敏感信息"
fi

# 检查Python命令使用
echo
echo "🐍 检查Python命令使用..."
if grep -q '"command": "python"' install.bat; then
    echo "✅ Windows使用python命令"
else
    echo "❌ Windows脚本python命令配置错误"
fi

if grep -q '"command": "python3"' install.sh; then
    echo "✅ Linux/Mac使用python3命令"
else
    echo "❌ Linux/Mac脚本python3命令配置错误"
fi

# 总结
echo
echo "================================"
if [[ ${#missing_files[@]} -eq 0 ]]; then
    echo "🎉 所有文件检查通过！准备发布！"
    echo
    echo "下一步："
    echo "1. 在GitHub创建新仓库：glm-mcp-server"
    echo "2. 运行: git init && git add . && git commit -m 'Initial release'"
    echo "3. 添加远程仓库并推送"
    echo "4. 创建GitHub Release v1.0.0"
else
    echo "❌ 以下文件缺失："
    for file in "${missing_files[@]}"; do
        echo "   - $file"
    done
    echo
    echo "请补充缺失的文件后再发布。"
fi

echo "================================"