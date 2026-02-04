#!/bin/bash

# ListenD 后台服务卸载脚本

PLIST_FILE="com.listend.monitor.plist"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"

echo "🗑️  卸载 ListenD 后台服务..."

# 停止并卸载服务
launchctl unload "$LAUNCH_AGENTS_DIR/$PLIST_FILE" 2>/dev/null

# 删除 plist 文件
rm -f "$LAUNCH_AGENTS_DIR/$PLIST_FILE"

echo ""
echo "✅ 卸载完成！"
echo ""
echo "服务已停止，不再开机自动启动。"
echo "如需重新安装，运行: ./install_service.sh"
