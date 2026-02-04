#!/bin/bash

# ListenD 后台服务安装脚本

PLIST_FILE="com.listend.monitor.plist"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "📦 安装 ListenD 后台服务..."

# 创建 LaunchAgents 目录
mkdir -p "$LAUNCH_AGENTS_DIR"

# 复制 plist 文件
cp "$PROJECT_DIR/$PLIST_FILE" "$LAUNCH_AGENTS_DIR/"

# 加载服务
launchctl unload "$LAUNCH_AGENTS_DIR/$PLIST_FILE" 2>/dev/null
launchctl load "$LAUNCH_AGENTS_DIR/$PLIST_FILE"

echo ""
echo "✅ 安装完成！"
echo ""
echo "服务已在后台运行，开机自动启动。"
echo ""
echo "常用命令："
echo "  查看状态: launchctl list | grep listend"
echo "  查看日志: tail -f $PROJECT_DIR/logs/monitor.log"
echo "  停止服务: launchctl unload ~/Library/LaunchAgents/$PLIST_FILE"
echo "  启动服务: launchctl load ~/Library/LaunchAgents/$PLIST_FILE"
echo "  卸载服务: ./uninstall_service.sh"
