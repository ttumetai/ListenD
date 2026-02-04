from flask import Flask, jsonify, render_template
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
# 修改 Jinja2 分隔符，避免与 Vue 冲突
app.jinja_env.variable_start_string = '[['
app.jinja_env.variable_end_string = ']]'

DB_FILE = "./db/music_history.db"

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/.well-known/appspecific/com.chrome.devtools.json')
def chrome_devtools():
    return '', 204

@app.route('/api/stats/overview')
def stats_overview():
    from flask import request
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    conn = get_db()
    c = conn.cursor()
    
    date_filter = ''
    params = []
    if start_date and end_date:
        date_filter = 'WHERE DATE(started_at) BETWEEN ? AND ?'
        params = [start_date, end_date]
    
    # 总播放次数
    total_plays = c.execute(f'SELECT COUNT(*) FROM play_history {date_filter}', params).fetchone()[0]
    
    # 总播放时长（小时）
    total_duration = c.execute(f'SELECT SUM(played_duration) FROM play_history {date_filter} AND played_duration IS NOT NULL'.replace('WHERE AND', 'WHERE'), params).fetchone()[0] or 0
    total_hours = total_duration / 3600
    
    # 完成率
    completed = c.execute(f'SELECT COUNT(*) FROM play_history {date_filter} AND is_completed = 1'.replace('WHERE AND', 'WHERE'), params).fetchone()[0]
    completion_rate = (completed / total_plays * 100) if total_plays > 0 else 0
    
    # 单曲循环次数
    repeat_count = c.execute(f'SELECT COUNT(*) FROM play_history {date_filter} AND play_type = "repeat"'.replace('WHERE AND', 'WHERE'), params).fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'total_plays': total_plays,
        'total_hours': round(total_hours, 1),
        'completion_rate': round(completion_rate, 1),
        'repeat_count': repeat_count
    })

@app.route('/api/stats/top-tracks')
def top_tracks():
    from flask import request
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    conn = get_db()
    c = conn.cursor()
    
    date_filter = ''
    params = []
    if start_date and end_date:
        date_filter = 'WHERE DATE(started_at) BETWEEN ? AND ?'
        params = [start_date, end_date]
    
    tracks = c.execute(f'''
        SELECT track_name, artist_name, COUNT(*) as play_count,
               SUM(played_duration) as total_duration,
               AVG(completion_rate) as avg_completion
        FROM play_history
        {date_filter}
        GROUP BY track_name, artist_name
        ORDER BY play_count DESC
        LIMIT 10
    ''', params).fetchall()
    
    conn.close()
    
    return jsonify([{
        'track': row['track_name'],
        'artist': row['artist_name'],
        'play_count': row['play_count'],
        'total_duration': round(row['total_duration'] or 0, 1),
        'avg_completion': round((row['avg_completion'] or 0) * 100, 1)
    } for row in tracks])

@app.route('/api/stats/top-artists')
def top_artists():
    from flask import request
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    conn = get_db()
    c = conn.cursor()
    
    date_filter = ''
    params = []
    if start_date and end_date:
        date_filter = 'WHERE DATE(started_at) BETWEEN ? AND ?'
        params = [start_date, end_date]
    
    artists = c.execute(f'''
        SELECT artist_name, COUNT(*) as play_count,
               SUM(played_duration) as total_duration
        FROM play_history
        {date_filter}
        GROUP BY artist_name
        ORDER BY play_count DESC
        LIMIT 10
    ''', params).fetchall()
    
    conn.close()
    
    return jsonify([{
        'artist': row['artist_name'],
        'play_count': row['play_count'],
        'total_hours': round((row['total_duration'] or 0) / 3600, 1)
    } for row in artists])

@app.route('/api/stats/recent')
def recent_plays():
    from flask import request
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    conn = get_db()
    c = conn.cursor()
    
    date_filter = ''
    params = []
    if start_date and end_date:
        date_filter = 'WHERE DATE(started_at) BETWEEN ? AND ?'
        params = [start_date, end_date]
    
    recent = c.execute(f'''
        SELECT track_name, artist_name, started_at, played_duration, 
               completion_rate, play_type
        FROM play_history
        {date_filter}
        ORDER BY started_at DESC
        LIMIT 20
    ''', params).fetchall()
    
    conn.close()
    
    return jsonify([{
        'track': row['track_name'],
        'artist': row['artist_name'],
        'started_at': row['started_at'],
        'played_duration': round(row['played_duration'] or 0, 1),
        'completion_rate': round((row['completion_rate'] or 0) * 100, 1),
        'play_type': row['play_type']
    } for row in recent])

@app.route('/api/stats/hourly')
def hourly_stats():
    from flask import request
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    conn = get_db()
    c = conn.cursor()
    
    date_filter = ''
    params = []
    if start_date and end_date:
        date_filter = 'WHERE DATE(started_at) BETWEEN ? AND ?'
        params = [start_date, end_date]
    
    hourly = c.execute(f'''
        SELECT strftime('%H', started_at) as hour, COUNT(*) as count
        FROM play_history
        {date_filter} {'AND' if date_filter else 'WHERE'} started_at IS NOT NULL
        GROUP BY hour
        ORDER BY hour
    ''', params).fetchall()
    
    conn.close()
    
    # 填充所有小时
    result = {str(i).zfill(2): 0 for i in range(24)}
    for row in hourly:
        result[row['hour']] = row['count']
    
    return jsonify([{'hour': k, 'count': v} for k, v in result.items()])

@app.route('/api/stats/daily')
def daily_stats():
    from flask import request
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    conn = get_db()
    c = conn.cursor()
    
    date_filter = ''
    params = []
    if start_date and end_date:
        date_filter = 'AND started_at >= ? AND started_at <= ?'
        params = [start_date + ' 00:00:00', end_date + ' 23:59:59']
    else:
        date_filter = "AND started_at >= date('now', '-30 days')"
    
    daily = c.execute(f'''
        SELECT DATE(started_at) as date, COUNT(*) as count,
               SUM(played_duration) as duration
        FROM play_history
        WHERE started_at IS NOT NULL {date_filter}
        GROUP BY date
        ORDER BY date
    ''', params).fetchall()
    
    conn.close()
    
    return jsonify([{
        'date': row['date'],
        'count': row['count'],
        'duration': round((row['duration'] or 0) / 60, 1)  # 分钟
    } for row in daily])

if __name__ == '__main__':
    import os
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5999))
    debug = os.getenv('FLASK_ENV') != 'production'
    app.run(host=host, port=port, debug=debug)

