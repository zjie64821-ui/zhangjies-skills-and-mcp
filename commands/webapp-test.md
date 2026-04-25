# Web 应用测试 (Playwright)

使用 Playwright 测试本地 Web 应用。

## 决策树
```
是静态 HTML？→ 直接读 HTML 识别选择器 → 写 Playwright 脚本
是动态应用？→ 服务器已运行？
  否 → 用 with_server.py 辅助启动
  是 → 先侦察再行动：navigate → screenshot → 识别选择器 → 执行
```

## 启动服务器
```bash
# 单服务器
python scripts/with_server.py --server "npm run dev" --port 5173 -- python test.py

# 多服务器（前后端）
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python test.py
```

## 测试脚本模板
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:5173')
    page.wait_for_load_state('networkidle')  # 关键：等 JS 执行完
    # ... 测试逻辑
    browser.close()
```

## 侦察-行动模式
1. 截图/检查 DOM: `page.screenshot()`, `page.content()`
2. 从结果中识别选择器
3. 用发现的选择器执行操作

## 最佳实践
- 动态应用必须 `wait_for_load_state('networkidle')` 后再检查 DOM
- 使用描述性选择器: `text=`, `role=`, CSS, ID
- 始终关闭浏览器

## 用户请求
$ARGUMENTS
