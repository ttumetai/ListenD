import subprocess

# --- AppleScript 获取信息 ---
def get_music_info():
    """
    获取 macOS Music App 的当前播放信息
    """
    script = '''
    tell application "Music"
        if it is running then
            if player state is playing then
                try
                    set tName to name of current track
                    set tArtist to artist of current track
                    set tAlbum to album of current track
                    set tDuration to duration of current track
                    set tPosition to player position
                    
                    if tArtist is missing value then set tArtist to "Unknown"
                    if tAlbum is missing value then set tAlbum to "Unknown"
                    
                    return tName & "|||" & tArtist & "|||" & tAlbum & "|||" & tDuration & "|||" & tPosition
                on error
                    return "error"
                end try
            else
                return "paused"
            end if
        else
            return "stopped"
        end if
    end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        output = result.stdout.strip()
        
        if output in ["stopped", "paused", "error", ""]:
            return None
            
        if "|||" in output:
            parts = output.split("|||")
            if len(parts) >= 5:
                return {
                    "track": parts[0],
                    "artist": parts[1],
                    "album": parts[2],
                    "duration": float(parts[3].replace(',', '.')),
                    "position": float(parts[4].replace(',', '.'))
                }
    except Exception as e:
        print(f"⚠️ 获取信息出错: {e}")
        return None
    return None