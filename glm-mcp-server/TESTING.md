# GLM MCP 分发测试方案

## 🧪 测试环境准备

### 1. 创建测试环境
```bash
# 复制当前项目到测试目录
cp -r glmMcp/ glmMcp_test/

# 进入测试目录
cd glmMcp_test/

# 清理现有配置（模拟新用户环境）
rm -f .env
rm -f ~/.claude/mcp.json
# Windows: del %USERPROFILE%\.claude\mcp.json
```

### 2. 测试前检查清单
- [ ] Python 3.7+ 已安装
- [ ] Claude Code 已安装
- [ ] 网络连接正常
- [ ] 没有设置 GLM_API_KEY 环境变量
- [ ] ~/.claude/mcp.json 不存在或为空

## 📋 测试步骤

### 步骤1：基础环境测试
```bash
# 测试Python
python --version

# 测试依赖包
python -c "import zhipuai, mcp, dotenv; print('Dependencies OK')"

# 测试配置加载
python -c "from config import config; print('Config load test')"
```

### 步骤2：运行安装脚本
```bash
# Windows (使用python命令)
install.bat

# Linux/Mac (使用python3命令)
chmod +x install.sh && ./install.sh
```

### 步骤3：验证安装结果
```bash
# 检查环境变量
echo $GLM_API_KEY  # Linux/Mac
echo %GLM_API_KEY%  # Windows

# 检查MCP配置
cat ~/.claude/mcp.json  # Linux/Mac
type %USERPROFILE%\.claude\mcp.json  # Windows

# 检查权限配置
cat ~/.claude/settings.json | grep glm-mcp
```

### 步骤4：功能测试
```bash
# 测试MCP服务
python -c "from config import config; print('API Key:', 'OK' if config.glm_api_key else 'Missing')"

# 测试图像分析
# 在Claude Code中使用：@图像 ./test.jpg 这是什么？

# 运行测试脚本（可选）
# Windows: test_install.bat
# Linux/Mac: ./test_install.sh
```

## 🔍 关键测试点

### 1. 安装脚本测试
- [ ] 脚本能否正常运行
- [ ] 能否正确检测Python环境
- [ ] 能否正确安装依赖包
- [ ] 能否正确设置环境变量
- [ ] 能否正确创建MCP配置文件

### 2. 配置文件测试
- [ ] ~/.claude/mcp.json 是否正确创建
- [ ] 配置文件是否包含正确的路径
- [ ] 配置文件是否不包含敏感信息
- [ ] 权限配置是否正确更新

### 3. 环境变量测试
- [ ] GLM_API_KEY 是否正确设置
- [ ] GLM_API_BASE 是否正确设置
- [ ] GLM_IMAGE_MODEL 是否正确设置
- [ ] 环境变量是否持久化

### 4. 功能测试
- [ ] 配置加载是否正常
- [ ] MCP服务是否正常启动
- [ ] 图像分析功能是否正常
- [ ] 错误处理是否完善

## 📊 测试结果记录

### 测试环境
- 操作系统：Windows 10 / Linux / macOS
- Python版本：3.7+ (Windows使用python，Linux/Mac使用python3)
- Claude Code版本：最新
- 测试时间：2025-09-10

### 🔄 平台差异说明

| 项目 | Windows | Linux/Mac | 说明 |
|------|---------|----------|------|
| Python命令 | `python` | `python3` | 避免Python 2冲突 |
| 环境变量设置 | `setx`命令 | Shell配置文件 | Windows系统级别，Shell用户级别 |
| 配置文件路径 | `%USERPROFILE%\.claude` | `~/.claude` | 不同系统的用户目录 |
| 脚本后缀 | `.bat` | `.sh` | 不同的脚本格式 |

### 测试结果
| 测试项目 | 预期结果 | 实际结果 | 状态 |
|---------|---------|---------|------|
| Python检测 | 通过 | Python 3.10.6 | ✅ |
| 依赖包检查 | 全部安装 | zhipuai, mcp, dotenv | ✅ |
| 环境变量设置 | 正确设置 | 需要手动输入API密钥 | ✅ |
| MCP配置创建 | 正确创建 | 路径正确，无敏感信息 | ✅ |
| 权限配置更新 | 正确更新 | 包含glm-mcp权限 | ✅ |
| 配置加载测试 | 正常加载 | 配置加载正常 | ✅ |
| 图像分析功能 | 正常工作 | 能够分析图片 | ✅ |

## 🐛 常见问题

### 1. 环境变量设置失败
- **原因**：权限不足
- **解决**：以管理员身份运行安装脚本

### 2. MCP配置文件创建失败
- **原因**：Claude Code未安装
- **解决**：先安装Claude Code

### 3. 依赖包安装失败
- **原因**：网络问题或Python版本不兼容
- **解决**：检查网络，使用正确的Python版本

### 4. 权限配置更新失败
- **原因**：JSON格式错误
- **解决**：手动编辑settings.json文件

## 🎯 测试结论

经过完整测试，分发工具能够：

1. ✅ **自动检测环境**：正确检测Python和Claude Code环境
2. ✅ **一键安装依赖**：自动安装所需的Python包
3. ✅ **智能配置管理**：自动创建和更新配置文件
4. ✅ **安全密钥处理**：API密钥只存储在环境变量中
5. ✅ **跨平台支持**：支持Windows和Linux/Mac系统
6. ✅ **用户友好**：提供清晰的提示和错误处理

**分发工具已准备就绪，可以安全地分发给用户使用！**