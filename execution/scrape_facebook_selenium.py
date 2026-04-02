#!/usr/bin/env python3
"""
Scrape Facebook profile using Selenium
Handles JavaScript rendering and lazy-loading
"""

import json
import sys
import time
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def setup_driver():
    """Set up Selenium Chrome driver with headless options"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def scrape_facebook_profile_selenium(profile_url):
    """Scrape Facebook profile using Selenium"""
    print(f"🔍 Scraping with Selenium: {profile_url}")

    driver = None
    try:
        driver = setup_driver()

        print("📥 Loading profile page...")
        driver.get(profile_url)

        # Wait for page to load
        time.sleep(3)

        # Extract profile name
        try:
            name_element = driver.find_element(By.XPATH, "//h1")
            profile_name = name_element.text
        except:
            profile_name = "Unknown"

        print(f"✓ Profile: {profile_name}")

        # Extract bio/about
        bio = ""
        try:
            bio_element = driver.find_element(By.XPATH, "//div[@data-testid='profile_bio']")
            bio = bio_element.text
        except:
            pass

        # Scroll to load lazy images
        print("📸 Loading images (scrolling)...")
        last_height = driver.execute_script("return document.body.scrollHeight")

        scroll_count = 0
        max_scrolls = 20  # Limit scrolls to avoid infinite loops

        while scroll_count < max_scrolls:
            # Scroll down
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # Calculate new height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break

            last_height = new_height
            scroll_count += 1

        print(f"✓ Scrolled {scroll_count} times")

        # Extract images
        print("🖼️  Extracting images...")
        photos = extract_images_from_page(driver)

        # Extract videos
        print("🎬 Extracting videos...")
        videos = extract_videos_from_page(driver)

        profile_info = {
            'name': profile_name,
            'bio': bio,
            'scraped_at': datetime.now().isoformat(),
            'method': 'selenium',
        }

        print(f"✓ Found {len(photos)} photos")
        print(f"✓ Found {len(videos)} videos")

        return {
            'profile': profile_info,
            'media': {
                'photos': photos,
                'videos': videos,
            }
        }

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return None

    finally:
        if driver:
            driver.quit()


def extract_images_from_page(driver):
    """Extract image URLs from loaded page"""
    photos = []

    # Find all img elements
    img_elements = driver.find_elements(By.TAG_NAME, "img")

    for img in img_elements:
        try:
            src = img.get_attribute("src")
            alt = img.get_attribute("alt")

            # Filter valid image URLs
            if not src or len(src) < 50:
                continue

            # Check if it's from Facebook CDN
            if "scontent" in src or "fbcdn" in src or "facebook" in src:
                if src not in [p['url'] for p in photos]:  # Avoid duplicates
                    photos.append({
                        'url': src,
                        'title': alt or 'Photo',
                        'scraped_at': datetime.now().isoformat(),
                    })
        except:
            continue

    return photos


def extract_videos_from_page(driver):
    """Extract video URLs from loaded page"""
    videos = []

    # Find all video elements
    video_elements = driver.find_elements(By.TAG_NAME, "video")
    for video in video_elements:
        try:
            src = video.get_attribute("src")
            if src:
                videos.append({
                    'url': src,
                    'title': 'Video',
                    'type': 'video',
                    'scraped_at': datetime.now().isoformat(),
                })
        except:
            continue

    # Find video sources inside video tags
    video_sources = driver.find_elements(By.TAG_NAME, "source")
    for source in video_sources:
        try:
            src = source.get_attribute("src")
            if src and "video" in src:
                if src not in [v['url'] for v in videos]:
                    videos.append({
                        'url': src,
                        'title': 'Video',
                        'type': 'video',
                        'scraped_at': datetime.now().isoformat(),
                    })
        except:
            continue

    return videos


def save_results(data, output_file='data/facebook_profile.json'):
    """Save scraped data to JSON file"""
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Data saved to: {output_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python scrape_facebook_selenium.py <facebook_profile_url>")
        print("Example: python scrape_facebook_selenium.py https://www.facebook.com/travis.watkins.940")
        sys.exit(1)

    profile_url = sys.argv[1]

    # Ensure URL is properly formatted
    if not profile_url.startswith('http'):
        profile_url = f"https://www.facebook.com/{profile_url}"

    print("\n" + "="*60)
    print("Facebook Profile Scraper (Selenium)")
    print("="*60 + "\n")

    data = scrape_facebook_profile_selenium(profile_url)

    if data and (len(data['media']['photos']) > 0 or len(data['media']['videos']) > 0):
        save_results(data)
        print("\n✓ Scraping complete!")
        print(f"Profile: {data['profile']['name']}")
        print(f"Photos: {len(data['media']['photos'])}")
        print(f"Videos: {len(data['media']['videos'])}")
    elif data:
        print("\n⚠️  Scraping completed but no media found.")
        print("This could mean:")
        print("  • Profile is private or restricted")
        print("  • No photos/videos on public section")
        print("  • Page structure changed")
        save_results(data)
    else:
        print("\n❌ Scraping failed", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
