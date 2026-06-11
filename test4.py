
import os
import subprocess
from pathlib import Path

def convert_webm_to_mp3(folder_path):
    folder = Path(folder_path)

    if not folder.exists():
        print("Folder does not exist.")
        return

    webm_files = list(folder.rglob("*.webm"))

    if not webm_files:
        print("No .webm files found.")
        return

    print(f"Found {len(webm_files)} WebM files.\n")

    for index, webm_file in enumerate(webm_files, start=1):
        mp3_file = webm_file.with_suffix(".mp3")

        print(f"[{index}/{len(webm_files)}] Converting:")
        print(webm_file.name)

        command = [
            "ffmpeg",
            "-i", str(webm_file),
            "-vn",
            "-codec:a", "libmp3lame",
            "-b:a", "320k",
            "-y",
            str(mp3_file)
        ]

        try:
            subprocess.run(
                command,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"✓ Saved: {mp3_file.name}\n")

        except subprocess.CalledProcessError:
            print(f"✗ Failed: {webm_file.name}\n")

if __name__ == "__main__":
    folder = input("Enter folder path: ").strip()
    convert_webm_to_mp3(folder)