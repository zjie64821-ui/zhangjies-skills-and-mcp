# 贡献指南

感谢您对 GLM MCP Server 项目的关注！我们欢迎任何形式的贡献。

## 🤝 如何贡献

### 报告问题

如果您发现了问题或有改进建议，请：

1. 先检查 [Issues](https://github.com/your-username/glm-mcp-server/issues) 确认问题是否已被报告
2. 如果是新的问题，请创建新的 Issue，包含：
   - 清晰的标题
   - 问题描述
   - 复现步骤
   - 期望行为
   - 实际行为
   - 相关日志或错误信息
   - 运行环境信息

### 提交代码

#### 开发环境设置

1. Fork 项目
2. Clone 到本地：
   ```bash
   git clone https://github.com/your-username/glm-mcp-server.git
   cd glm-mcp-server
   ```

3. 设置上游仓库：
   ```bash
   git remote add upstream https://github.com/your-username/glm-mcp-server.git
   ```

4. 创建开发环境：
   ```bash
   # 创建虚拟环境
   python -m venv venv
   
   # 激活虚拟环境
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   
   # 安装依赖
   pip install -r requirements.txt
   ```

#### 代码规范

- 使用 4 个空格缩进
- 遵循 PEP 8 代码风格
- 添加适当的注释和文档字符串
- 确保代码在所有支持的平台上都能正常工作

#### 提交规范

1. 创建功能分支：
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. 提交更改：
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

3. 推送到您的 fork：
   ```bash
   git push origin feature/your-feature-name
   ```

4. 创建 Pull Request

#### 提交消息格式

使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

- `feat:` 新功能
- `fix:` 修复问题
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建或辅助工具变动

示例：
```
feat: add support for additional image formats

fix: resolve memory leak in image processing

docs: update installation instructions
```

### 测试

在提交之前，请确保：

1. 所有测试通过
2. 代码符合项目规范
3. 新功能有相应的测试
4. 文档已更新

### 文档贡献

- 改进 README.md
- 添加或更新文档
- 修复拼写错误
- 翻译文档

## 📋 发布流程

### 版本号规范

使用 [语义化版本](https://semver.org/)：
- `MAJOR.MINOR.PATCH`
- `1.0.0` 初始版本
- `1.0.1` 修复版本
- `1.1.0` 功能版本
- `2.0.0` 重大变更

### 发布步骤

1. 更新版本号
2. 更新 CHANGELOG.md
3. 创建发布标签
4. 创建 GitHub Release
5. 更新文档

## 📞 联系方式

- GitHub Issues: [报告问题](https://github.com/your-username/glm-mcp-server/issues)
- GitHub Discussions: [讨论区](https://github.com/your-username/glm-mcp-server/discussions)
- Email: [your-email@example.com](mailto:your-email@example.com)

## 📄 许可证

通过贡献代码，您同意您的贡献将在 [MIT License](LICENSE) 下发布。

---

感谢您的贡献！🎉