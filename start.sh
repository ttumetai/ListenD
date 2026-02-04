#!/bin/bash

# ListenD 启动脚本

# ASCII Art
echo ""
echo "  _     _     _             ____  "
echo " | |   (_)___| |_ ___ _ __ |  _ \ "
echo " | |   | / __| __/ _ \ '_ \| | | |"
echo " | |___| \__ \ ||  __/ | | | |_| |"
echo " |_____|_|___/\__\___|_| |_|____/ "
echo ""
echo "  🎵 Music Analytics Dashboard"
echo ""

echo "🚀 启动 ListenD..."

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "❌ 虚拟环境不存在，请先运行: uv sync"
    exit 1
fi

# 使用虚拟环境的 Python
PYTHON=".venv/bin/python"

# 启动监听服务（后台运行）
echo "📡 启动音乐监听服务..."
$PYTHON main.py &
MAIN_PID=$!

# 等待1秒
sleep 1

# 启动 Web 服务（后台运行）
echo "🌐 启动 Web 服务..."
$PYTHON web_server.py &
WEB_PID=$!

echo ""
echo "✅ 服务已启动！"
echo "   - 监听服务 PID: $MAIN_PID"
echo "   - Web 服务 PID: $WEB_PID"
echo "   - Web 地址: http://localhost:5999"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 捕获 Ctrl+C 信号
trap "echo ''; echo '🛑 正在停止服务...'; kill $MAIN_PID $WEB_PID 2>/dev/null; echo '👋 服务已停止'; exit" INT

# 保持脚本运行
wait
