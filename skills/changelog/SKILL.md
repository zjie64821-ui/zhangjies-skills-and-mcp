---
name: changelog
description: >
  Git commit to changelog generator. TRIGGER when the user wants to: generate release notes,
  create a changelog from git history, summarize commits into user-friendly updates, produce
  version documentation, or create update summaries.
  Keywords: changelog, release notes, 更新日志, 版本说明, commit history, 变更记录.
  DO NOT trigger for viewing git log without changelog intent.
---

# Changelog 生成器

## 工作流
1. **扫描 Git 历史**: 指定时间段/版本间的提交
2. **分类**: Features / Improvements / Bug Fixes / Breaking Changes / Security
3. **翻译**: 技术术语 → 用户语言
4. **格式化**: 干净 Markdown
5. **过滤**: 排除内部重构、测试更新

## 输出格式
```markdown
# [版本] - YYYY-MM-DD
## Features
- Added [功能] (#PR)
## Bug Fixes
- Fixed [问题] (#PR)
## Breaking Changes
- [变更描述]
```

## 常用: "上次发布以来的提交" / "过去一周" / "两版本之间"

## 用户请求
$ARGUMENTS
