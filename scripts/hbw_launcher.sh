#!/bin/bash

# HBW Browser Launcher v3.1 - 持久化登录 + 永不死锁 + 已运行跳过
PORT=9222
# 核心变化：使用用户目录下的持久化文件夹，确保登录状态不丢失
USER_DATA_DIR=”/Users/zhangjie/.gemini/chrome_hbw_profile”

# 创建目录（如果不存在）
mkdir -p “$USER_DATA_DIR”

# 0. 如果专用浏览器已经在运行且端口就绪，直接跳过
if curl -s -o /dev/null -w '' http://127.0.0.1:$PORT/json/version 2>/dev/null; then
    echo “HBW Engine 已在运行，调试端口 $PORT 就绪，跳过启动。”
    exit 0
fi

# 1. 强制清理 9222 端口上的残留死锁（如果有的话）
PID=$(lsof -ti :$PORT)
if [ ! -z “$PID” ]; then
    kill -9 $PID
    sleep 1
fi

# 2. 启动”AI 特攻版”Chrome
# -n: 强制开启新实例
# --user-data-dir: 锁定持久化配置文件夹
open -na "Google Chrome" --args \
    --remote-debugging-port=$PORT \
    --user-data-dir="$USER_DATA_DIR" \
    --no-first-run \
    --no-default-browser-check \
    "$@"

# 3. 校验启动结果
for i in {1..5}; do
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null; then
        echo "HBW Engine 启动成功，调试端口 $PORT 已就绪。"
        exit 0
    fi
    sleep 1
done

echo "错误：浏览器启动超时或端口无法响应。"
exit 1
