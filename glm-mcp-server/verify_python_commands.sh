#!/bin/bash

# 验证Python命令使用的正确性

echo "🔍 验证GLM MCP分发工具的Python命令使用"
echo

# 检查install.sh
echo "📋 检查 install.sh:"
if grep -q '"command": "python3"' install.sh; then
    echo "✅ MCP配置使用python3命令"
else
    echo "❌ MCP配置未使用python3命令"
fi

if grep -q 'python3 -c' install.sh; then
    echo "✅ Python脚本调用使用python3命令"
else
    echo "❌ Python脚本调用未使用python3命令"
fi

# 检查install.bat
echo
echo "📋 检查 install.bat:"
if grep -q '"command": "python"' install.bat; then
    echo "✅ MCP配置使用python命令"
else
    echo "❌ MCP配置未使用python命令"
fi

# 检查测试脚本
echo
echo "📋 检查测试脚本:"
if [[ -f test_install.sh ]]; then
    if grep -q 'python3\|python' test_install.sh; then
        echo "✅ test_install.sh包含Python检测逻辑"
    else
        echo "❌ test_install.sh缺少Python检测"
    fi
fi

# 检查文档
echo
echo "📋 检查文档:"
if grep -q 'python3' README.md; then
    echo "✅ README.md包含python3说明"
else
    echo "❌ README.md缺少python3说明"
fi

if grep -q 'python3' TESTING.md; then
    echo "✅ TESTING.md包含python3说明"
else
    echo "❌ TESTING.md缺少python3说明"
fi

echo
echo "✅ 验证完成！"