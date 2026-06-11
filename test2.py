import os
import yt_dlp

output_folder = "songs"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def get_playlist_info(url):
    """Fetch playlist/video info without downloading."""
    with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True}) as ydl:
        return ydl.extract_info(url, download=False)

def download_url(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_folder, '%(playlist_index)s - %(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'noplaylist': False,          # Allow playlist downloads
        'ignoreerrors': True,         # Skip unavailable videos instead of crashing
        'progress_hooks': [progress_hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def progress_hook(d):
    if d['status'] == 'downloading':
        filename = os.path.basename(d.get('filename', 'Unknown'))
        percent = d.get('_percent_str', '?%').strip()
        print(f"\r  Downloading: {filename[:50]} — {percent}", end='', flush=True)
    elif d['status'] == 'finished':
        print(f"\n  ✔ Done: {os.path.basename(d['filename'])}")

while True:
    url = input("\nEnter YouTube URL (video or playlist), or 'q' to quit: ").strip()

    if url.lower() == 'q':
        print("Exiting...")
        break

    try:
        print("Fetching info...")
        info = get_playlist_info(url)

        # Detect if it's a playlist
        if info.get('_type') == 'playlist':
            entries = info.get('entries', [])
            total = len(entries)
            print(f"Playlist detected: '{info.get('title', 'Unknown')}' — {total} tracks")
            print("Starting download one by one...\n")

            for i, entry in enumerate(entries, start=1):
                if entry is None:
                    print(f"  [{i}/{total}] Skipping unavailable track.")
                    continue
                track_url = entry.get('url') or f"https://www.youtube.com/watch?v={entry['id']}"
                print(f"[{i}/{total}] {entry.get('title', 'Unknown title')}")
                try:
                    download_url(track_url)
                except Exception as e:
                    print(f"  ✘ Failed: {e}")
        else:
            # Single video
            print(f"Single video: '{info.get('title', 'Unknown')}'")
            download_url(url)

        print("\nAll done!")

    except Exception as e:
        print(f"Error: {e}")