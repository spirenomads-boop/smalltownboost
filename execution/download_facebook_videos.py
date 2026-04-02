#!/usr/bin/env python3
"""
Download Facebook videos using yt-dlp
Automates downloading all 8 performance videos for local hosting
"""

import subprocess
import os
from pathlib import Path

# Create videos directory
videos_dir = Path("docs/videos")
videos_dir.mkdir(exist_ok=True)

# Facebook video URLs
videos = {
    "01_build_process.mp4": "https://www.facebook.com/reel/26274358378891912/",
    "02_problem_solving.mp4": "https://www.facebook.com/reel/1319576770011268/",
    "03_travis_vision.mp4": "https://www.facebook.com/reel/1263774455719944/",
    "04_in_action.mp4": "https://www.facebook.com/reel/959585566642086/",
    "05_test_drive.mp4": "https://www.facebook.com/reel/1965359127382735/",
    "06_winter_testing.mp4": "https://www.facebook.com/reel/25783119921383937/",
    "07_snow_fun.mp4": "https://www.facebook.com/reel/1629349668200105/",
    "08_durability_test.mp4": "https://www.facebook.com/reel/1235720068730150/",
}

print("=" * 70)
print("FACEBOOK VIDEO DOWNLOADER - yt-dlp Automation")
print("=" * 70)
print(f"\n📁 Output directory: {videos_dir.absolute()}\n")

success_count = 0
failed_count = 0

for filename, url in videos.items():
    output_path = videos_dir / filename

    # Skip if already downloaded
    if output_path.exists():
        print(f"✓ {filename} (already exists)")
        success_count += 1
        continue

    print(f"⬇️  Downloading {filename}...", end=" ")

    try:
        # yt-dlp command with options optimized for Facebook
        cmd = [
            "yt-dlp",
            "-f", "best[ext=mp4]",  # Best quality MP4
            "-o", str(output_path),  # Output file
            "--no-warnings",  # Suppress warnings
            "-q",  # Quiet mode
            url
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        if result.returncode == 0 and output_path.exists():
            size_mb = output_path.stat().st_size / (1024 * 1024)
            print(f"✓ ({size_mb:.1f} MB)")
            success_count += 1
        else:
            print(f"✗ Failed")
            if result.stderr:
                print(f"  Error: {result.stderr[:100]}")
            failed_count += 1

    except subprocess.TimeoutExpired:
        print(f"✗ Timeout")
        failed_count += 1
    except Exception as e:
        print(f"✗ Error: {str(e)[:50]}")
        failed_count += 1

print("\n" + "=" * 70)
print(f"✓ Downloaded: {success_count}/{len(videos)}")
if failed_count > 0:
    print(f"✗ Failed: {failed_count}/{len(videos)}")
print("=" * 70)

# List downloaded files
print(f"\n📂 Files in {videos_dir}:")
for f in sorted(videos_dir.glob("*.mp4")):
    size_mb = f.stat().st_size / (1024 * 1024)
    print(f"  ✓ {f.name} ({size_mb:.1f} MB)")

print("\n✨ Next step: Update HTML to use local videos instead of Facebook embeds")
