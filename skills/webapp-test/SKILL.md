---
name: webapp-test
description: >
  Web application testing with Playwright. TRIGGER when the user wants to: test a web application's
  UI functionality; automate browser interactions for testing; capture screenshots of web pages;
  verify frontend behavior; debug UI issues; test local dev servers.
  Keywords: test web app, UI testing, Playwright, browser testing, webapp test, 前端测试,
  浏览器测试, 截图测试.
  DO NOT trigger for unit tests, API tests, or non-browser testing.
---

# Web 应用测试 (Playwright)

## 决策树
- 静态 HTML → 直接读 HTML 识别选择器
- 动态应用、服务器未运行 → `python scripts/with_server.py --server "cmd" --port N -- python test.py`
- 动态应用、服务器已运行 → 先侦察再行动

## 服务器管理
```bash
# 单服务器
python scripts/with_server.py --server "npm run dev" --port 5173 -- python test.py
# 多服务器
python scripts/with_server.py --server "cd backend && python server.py" --port 3000 --server "cd frontend && npm run dev" --port 5173 -- python test.py
```

## 脚本模板
```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:5173')
    page.wait_for_load_state('networkidle')  # 关键
    # ... 测试逻辑
    browser.close()
```

## 关键: 动态应用必须 `networkidle` 后再检查 DOM

## 用户请求
$ARGUMENTS
