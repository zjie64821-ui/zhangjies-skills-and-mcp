---
name: plan
description: >
  Manus-style file-based planning for complex tasks. TRIGGER when the user wants to: plan a complex
  multi-step task; organize work into phases with tracking; create a structured project plan;
  break down a large task into manageable steps; track progress across sessions.
  Keywords: 规划, 计划, 任务分解, 项目规划, plan, organize, break down, task plan, 进度追踪.
  DO NOT trigger for simple tasks with fewer than 3 steps.
---

# 文件式规划

核心: Context Window = RAM (易失) | Filesystem = Disk (持久) → 重要信息写入磁盘

## 三个规划文件 (在项目目录下创建)

### task_plan.md
```markdown
# 任务计划
## 目标
## 阶段
### Phase 1: [名称] - status: pending
- [ ] 子任务
## 错误记录
| Error | Attempt | Resolution |
```

### findings.md — 调研发现
### progress.md — 进度日志

## 关键规则
1. **先建计划再动手**
2. **2-Action 规则**: 每 2 次操作后立即写文件
3. **决策前重读计划**
4. **行动后更新状态**
5. **记录所有错误**
6. **3-Strike 协议**: 诊断→换方法→重新审视→上报

## 用户请求
$ARGUMENTS
