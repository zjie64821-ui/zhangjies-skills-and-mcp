---
name: github-sync
description: >
  GitHub repository synchronization with LFS support. TRIGGER when the user wants to: push a local
  project/folder to GitHub; backup files to a GitHub repository; sync large files with Git LFS;
  create a new GitHub repo from local directory; push with timeout prevention for large files.
  Keywords: 推送到GitHub, 备份到github, github同步, push to github, git push, LFS,
  上传到github, 同步仓库.
  DO NOT trigger for normal git operations (commit, pull) without GitHub push intent.
---

# GitHub 同步助手

## 工作流

### 1. 环境诊断
`gh auth status`, `git lfs version`

### 2. 确认
目标仓库（新建/现有）、名称、隐私、策略

### 3. 稳健配置
```bash
git config --global http.postBuffer 1048576000
git config --global lfs.dialtimeout 1800
git config --global lfs.activitytimeout 1800
git config --global lfs.concurrenttransfers 1
git lfs install
```

### 4. 分批推送
1. 生成 .gitignore
2. 先推代码/文档
3. 大文件(CSV等)逐个 push

## 安全红线
- 不未确认 `--force`
- 不推 .env/API Key

## 用户请求
$ARGUMENTS
