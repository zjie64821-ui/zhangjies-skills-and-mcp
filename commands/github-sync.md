# GitHub 同步助手

在任意目录下通过自然语言与 GitHub 交互，支持大文件 LFS 和防超时。

## 工作流

### Step 1: 环境诊断
检查 `gh auth status`, `git lfs version`

### Step 2: 交互确认
确认：目标仓库（新建/现有）、名称、隐私、推送策略

### Step 3: 稳健配置
```bash
git config --global http.postBuffer 1048576000
git config --global lfs.dialtimeout 1800
git config --global lfs.activitytimeout 1800
git config --global lfs.concurrenttransfers 1
git lfs install
```

### Step 4: 分批推送
1. 动态生成 .gitignore 过滤大/无关文件
2. 先推送代码和文档（轻量文件）
3. 大型文件（CSV 等）逐个 add → commit → push

## 安全红线
- 绝不未经用户确认使用 `git push --force`
- 绝不推送 .env、API Key、密码文件

## 用户请求
$ARGUMENTS
