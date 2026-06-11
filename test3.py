import os
import yt_dlp

output_folder = "songs"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def progress_hook(d):
    if d['status'] == 'downloading':
        filename = os.path.basename(d.get('filename', 'Unknown'))
        percent = d.get('_percent_str', '?%').strip()
        print(f"\r  [{percent}] {filename[:60]}", end='', flush=True)
    elif d['status'] == 'finished':
        print(f"\n  ✔ Converted: {os.path.basename(d['filename'])}")

while True:
    url = input("\nEnter YouTube URL (video or playlist), or 'q' to quit: ").strip()

    if url.lower() == 'q':
        print("Exiting...")
        break

    start_input = input("Start from track number? (press Enter for 1): ").strip()
    start_index = int(start_input) if start_input.isdigit() else 1

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_folder, '%(playlist_index)s - %(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'noplaylist': False,
        'ignoreerrors': True,
        'progress_hooks': [progress_hook],
        'playliststart': start_index,
        # no playlistend — download everything from start_index to end
        'verbose': False,
        'quiet': False,
    }

    try:
        print(f"\nStarting download from track {start_index}...\n")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\nAll done!")
    except Exception as e:
        print(f"Error: {e}")