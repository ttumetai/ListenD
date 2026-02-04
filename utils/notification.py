import pync

def send_notification(track, artist, album):
    """
    使用 pync 发送 macOS 通知
    """

    ICON_PATH = './2705.png'
    try:
        # 使用 pync.notify() 发送通知
        pync.notify(
            f"🎵 {track}\n🎤 {artist}\n💿 {album}",
            title=f"Now Playing",
            sound='default',
            # appIcon 决定左侧小图标
            appIcon=ICON_PATH,
        )
        print("✅ 通知已发送")
    except Exception as e:
        print(f"❌ 通知发送失败: {e}")
        print("💡 提示：请确保已安装 pync (pip install pync)")