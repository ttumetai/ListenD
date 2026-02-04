import sqlite3
import datetime

DB_FILE = "./db/music_history.db"

# --- 数据库初始化 ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS play_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            track_name TEXT,
            artist_name TEXT,
            album_name TEXT,
            duration REAL,
            started_at DATETIME,
            ended_at DATETIME,
            played_duration REAL,
            completion_rate REAL,
            is_completed BOOLEAN,
            play_type TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print(f"✅ 数据库已就绪: {DB_FILE}")

# --- 开始播放记录 ---
def start_play_record(info):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        c.execute('''
            INSERT INTO play_history (track_name, artist_name, album_name, duration, started_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (info['track'], info['artist'], info['album'], info['duration'], current_time))
        
        record_id = c.lastrowid
        conn.commit()
        conn.close()
        print(f"💾 [开始记录] {current_time} | {info['track']}")
        return record_id
    except Exception as e:
        print(f"❌ 数据库写入失败: {e}")
        return None

# --- 结束播放记录 ---
def end_play_record(record_id, played_duration, total_duration, play_type):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        completion_rate = min(played_duration / total_duration, 1.0) if total_duration > 0 else 0
        is_completed = completion_rate >= 0.8  # 听完80%算完成
        
        c.execute('''
            UPDATE play_history 
            SET ended_at = ?, played_duration = ?, completion_rate = ?, is_completed = ?, play_type = ?
            WHERE id = ?
        ''', (current_time, played_duration, completion_rate, is_completed, play_type, record_id))
        
        conn.commit()
        conn.close()
        print(f"✅ [记录完成] 播放时长: {played_duration:.1f}s | 完成度: {completion_rate*100:.1f}% | 类型: {play_type}")
    except Exception as e:
        print(f"❌ 更新记录失败: {e}")