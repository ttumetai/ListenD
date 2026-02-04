from utils.db_utils import init_db, start_play_record, end_play_record
from utils.music_utils import get_music_info
from utils.notification import send_notification
import time

POLL_INTERVAL = 1  # 轮询间隔 (秒)

def main():
    init_db()
    
    last_track_signature = None
    last_position = 0
    current_record_id = None
    play_start_time = None
    
    print("🚀 监听服务已启动，按 Ctrl+C 停止...")
    print("💡 提示：如果通知不显示，请检查系统偏好设置 -> 通知 -> terminal-notifier")

    try:
        while True:
            current_info = get_music_info()
            
            if current_info:
                current_signature = f"{current_info['track']}-{current_info['artist']}-{current_info['album']}"
                
                if current_signature != last_track_signature:
                    # 结束上一首歌的记录
                    if current_record_id is not None and play_start_time is not None:
                        played_duration = time.time() - play_start_time
                        end_play_record(current_record_id, played_duration, last_duration, 'normal')
                    
                    print(f"\n🎵 切歌检测: {current_info['track']} - {current_info['artist']}")
                    
                    send_notification(
                        current_info['track'], 
                        current_info['artist'],
                        current_info['album']
                    )
                    
                    # 开始新的播放记录
                    current_record_id = start_play_record(current_info)
                    play_start_time = time.time()
                    last_duration = current_info['duration']
                    
                    last_track_signature = current_signature
                    last_position = current_info['position']
                else:
                    # 同一首歌，检测是否单曲循环
                    if current_info['position'] < last_position - 5:
                        # 结束上一次循环的记录
                        if current_record_id is not None and play_start_time is not None:
                            played_duration = time.time() - play_start_time
                            end_play_record(current_record_id, played_duration, current_info['duration'], 'repeat')
                        
                        print(f"\n🔁 单曲循环检测: {current_info['track']} - {current_info['artist']}")
                        
                        # 开始新的循环记录
                        current_record_id = start_play_record(current_info)
                        play_start_time = time.time()
                    
                    last_position = current_info['position']
            else:
                # 暂停或停止
                if last_track_signature is not None:
                    # 结束当前播放记录
                    if current_record_id is not None and play_start_time is not None:
                        played_duration = time.time() - play_start_time
                        end_play_record(current_record_id, played_duration, last_duration, 'skip')
                    
                    print("⏸️ 播放已停止或暂停")
                    last_track_signature = None
                    last_position = 0
                    current_record_id = None
                    play_start_time = None
            
            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        # 退出时结束当前记录
        if current_record_id is not None and play_start_time is not None:
            played_duration = time.time() - play_start_time
            end_play_record(current_record_id, played_duration, last_duration, 'skip')
        print("\n👋 服务已停止")


if __name__ == "__main__":
    main()