import sys
import re
import subprocess

def srt_timestamp_to_seconds(srt_time):
    time_part = srt_time.split(',')[0]
    h, m, s = map(int, time_part.split(':'))
    return h * 3600 + m * 60 + s

def main():
    if len(sys.argv) < 3:
        return

    srt_path = sys.argv[1]
    # MPV passes the total seconds as an integer string
    target_seconds = int(sys.argv[2])
    
    try:
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return

    blocks = content.strip().split('\n\n')
    
    for block in blocks:
        lines = block.split('\n')
        if len(lines) >= 3:
            time_match = re.match(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})', lines[1])
            if time_match:
                start_sec = srt_timestamp_to_seconds(time_match.group(1))
                end_sec = srt_timestamp_to_seconds(time_match.group(2))
                
                # Check if current playback time falls in this window
                if start_sec <= target_seconds <= end_sec:
                    sub_text = " ".join(lines[2:])
                    # Strip formatting tags
                    sub_text = re.sub(r'<[^>]*>', '', sub_text)
                    
                    # Send to Wayland clipboard
                    process = subprocess.Popen(['wl-copy'], stdin=subprocess.PIPE, text=True)
                    process.communicate(input=sub_text)
                    return

if __name__ == "__main__":
    main()
