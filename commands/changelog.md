# Changelog 生成器

将 git 提交历史转换为用户友好的更新日志。

## 工作流
1. **扫描 Git 历史**: 分析指定时间段或版本间的提交
2. **分类变更**: 按逻辑分组
   - Features (新功能)
   - Improvements (改进)
   - Bug Fixes (修复)
   - Breaking Changes (破坏性变更)
   - Security (安全)
3. **翻译**: 将技术术语转换为用户语言
4. **格式化**: 干净的 Markdown 输出
5. **过滤噪声**: 排除内部重构、测试更新等

## 常用方式
- "从上次发布以来的所有提交生成 changelog"
- "过去一周的提交"
- "两个版本之间的变更"
- "指定日期范围的变更"

## 输出格式
```markdown
# [版本号] - YYYY-MM-DD

## Features
- Added [功能描述] (#PR)

## Bug Fixes
- Fixed [问题描述] (#PR)

## Breaking Changes
- [破坏性变更描述]
```

## 用户请求
$ARGUMENTS
