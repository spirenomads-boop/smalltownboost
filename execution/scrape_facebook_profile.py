#!/usr/bin/env python3
"""
Scrape Facebook business profile for photos and videos
Extracts metadata and media URLs for website generation
"""

import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

# Create output directories
Path(".tmp/media").mkdir(parents=True, exist_ok=True)
Path("data").mkdir(parents=True, exist_ok=True)


def scrape_facebook_profile(profile_url):
    """
    Scrape Facebook profile using requests + BeautifulSoup
    Works for public profiles
    """
    print(f"🔍 Scraping Facebook profile: {profile_url}")

    # Parse profile URL to get username/ID
    parsed = urlparse(profile_url)
    path_parts = parsed.path.strip('/').split('/')
    profile_id = path_parts[-1] if path_parts else None

    if not profile_id:
        print(f"❌ Invalid Facebook URL: {profile_url}", file=sys.stderr)
        return None

    # Set up session with headers to avoid being blocked
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    })

    try:
        # Fetch profile page
        print(f"📥 Fetching profile page...")
        response = session.get(profile_url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract profile info
        profile_info = extract_profile_info(soup, profile_id)

        # Extract photos and videos
        # Note: Facebook heavily relies on AJAX loading, so we get initial page content
        media_data = extract_media_from_page(soup, profile_url, session)

        print(f"✓ Found {len(media_data.get('photos', []))} photos")
        print(f"✓ Found {len(media_data.get('videos', []))} videos")

        return {
            'profile': profile_info,
            'media': media_data,
        }

    except requests.RequestException as e:
        print(f"❌ Error fetching profile: {e}", file=sys.stderr)
        return None


def extract_profile_info(soup, profile_id):
    """Extract basic profile information"""
    info = {
        'id': profile_id,
        'name': 'Unknown',
        'bio': '',
        'website': '',
        'scraped_at': datetime.now().isoformat(),
    }

    # Try to extract from page title
    title = soup.find('title')
    if title:
        info['name'] = title.string.split('|')[0].strip() if '|' in title.string else title.string

    # Try to extract from meta tags
    og_desc = soup.find('meta', {'property': 'og:description'})
    if og_desc:
        info['bio'] = og_desc.get('content', '')

    return info


def extract_media_from_page(soup, profile_url, session):
    """Extract media URLs from Facebook profile page"""
    media = {
        'photos': [],
        'videos': [],
    }

    # Facebook loads media via AJAX/lazy loading
    # On initial page load, we can find some images in various formats

    # Look for img tags with src
    images = soup.find_all('img', {'src': True})

    for img in images:
        src = img.get('src', '')

        # Filter out small/icon images
        if not src or 'icon' in src or 'avatar' in src or len(src) < 50:
            continue

        # Check if it's a scontent image (Facebook CDN)
        if 'scontent' in src or 'fbcdn' in src:
            media['photos'].append({
                'url': src,
                'title': img.get('alt', 'Untitled'),
                'scraped_at': datetime.now().isoformat(),
            })

    # Look for video elements
    videos = soup.find_all('video', {'src': True})
    for video in videos:
        src = video.get('src', '')
        if src:
            media['videos'].append({
                'url': src,
                'title': 'Video',
                'scraped_at': datetime.now().isoformat(),
            })

    # Alternative: look for video in iframe (embedded videos)
    iframes = soup.find_all('iframe')
    for iframe in iframes:
        src = iframe.get('src', '')
        if 'facebook.com' in src or 'fbcdn' in src:
            media['videos'].append({
                'url': src,
                'title': 'Embedded Video',
                'scraped_at': datetime.now().isoformat(),
            })

    return media


def save_results(data, output_file='data/facebook_profile.json'):
    """Save scraped data to JSON file"""
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Data saved to: {output_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python scrape_facebook_profile.py <facebook_profile_url>")
        print("Example: python scrape_facebook_profile.py https://www.facebook.com/YourBusinessPage")
        sys.exit(1)

    profile_url = sys.argv[1]

    # Ensure URL is properly formatted
    if not profile_url.startswith('http'):
        profile_url = f"https://www.facebook.com/{profile_url}"

    print("\n" + "="*60)
    print("Facebook Profile Scraper")
    print("="*60 + "\n")

    data = scrape_facebook_profile(profile_url)

    if data:
        save_results(data)
        print("\n✓ Scraping complete!")
        print(f"Profile: {data['profile']['name']}")
        print(f"Photos: {len(data['media']['photos'])}")
        print(f"Videos: {len(data['media']['videos'])}")
    else:
        print("\n❌ Scraping failed", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
