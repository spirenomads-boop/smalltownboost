#!/usr/bin/env python3
"""
Generate a responsive business website from Facebook profile data
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def load_profile_data(json_file='data/facebook_profile.json'):
    """Load scraped Facebook profile data"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Profile data not found: {json_file}", file=sys.stderr)
        print("Run scrape_facebook_profile.py first", file=sys.stderr)
        sys.exit(1)


def generate_html(data):
    """Generate HTML for business website"""
    profile = data.get('profile', {})
    media = data.get('media', {})
    photos = media.get('photos', [])
    videos = media.get('videos', [])

    business_name = profile.get('name', 'Business')
    bio = profile.get('bio', '')

    # Generate photo gallery HTML
    photo_gallery = ""
    for i, photo in enumerate(photos[:50]):  # Limit to 50 for MVP
        photo_url = photo.get('url', '')
        title = photo.get('title', 'Photo')
        photo_gallery += f'''
    <div class="gallery-item">
        <img src="{photo_url}" alt="{title}" loading="lazy">
        <div class="overlay">
            <p>{title}</p>
        </div>
    </div>'''

    # Generate video section HTML
    video_section = ""
    if videos:
        video_section = "<section class='videos'><h2>Videos</h2><div class='video-grid'>"
        for video in videos[:10]:  # Limit to 10
            video_url = video.get('url', '')
            title = video.get('title', 'Video')
            if 'iframe' in str(video_url).lower():
                video_section += f'''
    <div class="video-item">
        <iframe src="{video_url}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
    </div>'''
            else:
                video_section += f'''
    <div class="video-item">
        <video controls>
            <source src="{video_url}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </div>'''
        video_section += "</div></section>"

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{business_name} - Business Website</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --primary-color: #1877f2;
            --secondary-color: #e4e6eb;
            --text-color: #050505;
            --light-bg: #f0f2f5;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            color: var(--text-color);
            line-height: 1.6;
        }}

        header {{
            background: linear-gradient(135deg, var(--primary-color), #0a66c2);
            color: white;
            padding: 60px 20px;
            text-align: center;
        }}

        header h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}

        header p {{
            font-size: 1.2em;
            opacity: 0.9;
            max-width: 600px;
            margin: 0 auto;
        }}

        nav {{
            background: white;
            padding: 15px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 100;
        }}

        nav ul {{
            list-style: none;
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
        }}

        nav a {{
            color: var(--text-color);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }}

        nav a:hover {{
            color: var(--primary-color);
        }}

        section {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 60px 20px;
        }}

        h2 {{
            font-size: 2em;
            margin-bottom: 30px;
            color: var(--primary-color);
            text-align: center;
        }}

        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }}

        .gallery-item {{
            position: relative;
            overflow: hidden;
            aspect-ratio: 1;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            cursor: pointer;
            transition: transform 0.3s;
        }}

        .gallery-item:hover {{
            transform: scale(1.05);
        }}

        .gallery-item img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}

        .gallery-item .overlay {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
            color: white;
            padding: 20px;
            transform: translateY(100%);
            transition: transform 0.3s;
        }}

        .gallery-item:hover .overlay {{
            transform: translateY(0);
        }}

        .video-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 30px;
        }}

        .video-item {{
            position: relative;
            width: 100%;
            padding-bottom: 56.25%;
            height: 0;
            overflow: hidden;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}

        .video-item video,
        .video-item iframe {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
        }}

        footer {{
            background: #f0f2f5;
            padding: 30px 20px;
            text-align: center;
            color: #65676b;
            margin-top: 60px;
        }}

        footer p {{
            margin: 5px 0;
        }}

        @media (max-width: 768px) {{
            header h1 {{
                font-size: 2em;
            }}

            .gallery {{
                grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            }}

            .video-grid {{
                grid-template-columns: 1fr;
            }}

            nav ul {{
                gap: 15px;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>{business_name}</h1>
        <p>{bio if bio else 'Welcome to our business website'}</p>
    </header>

    <nav>
        <ul>
            <li><a href="#photos">📸 Photos</a></li>
            <li><a href="#videos">🎥 Videos</a></li>
            <li><a href="#contact">📧 Contact</a></li>
        </ul>
    </nav>

    <section id="photos">
        <h2>Photo Gallery</h2>
        <div class="gallery">
{photo_gallery}
        </div>
    </section>

{video_section}

    <section id="contact">
        <h2>Get in Touch</h2>
        <p style="text-align: center; font-size: 1.1em; color: #65676b;">
            Visit our Facebook page or contact us through the form below.
        </p>
    </section>

    <footer>
        <p>&copy; {datetime.now().year} {business_name}. All rights reserved.</p>
        <p>Website generated from Facebook profile • {datetime.now().strftime('%Y-%m-%d')}</p>
    </footer>
</body>
</html>'''

    return html


def save_website(html_content, output_dir='.tmp/website'):
    """Save generated HTML to file"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    html_file = output_path / 'index.html'
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✓ Website generated: {html_file}")
    return output_path


def main():
    print("\n" + "="*60)
    print("Business Website Generator")
    print("="*60 + "\n")

    # Load profile data
    print("📂 Loading profile data...")
    data = load_profile_data()

    # Generate HTML
    print("🔨 Generating website...")
    html = generate_html(data)

    # Save website
    output_dir = save_website(html)

    print(f"\n✓ Website ready!")
    print(f"📁 Location: {output_dir.absolute()}")
    print(f"📖 Open: {output_dir.absolute()}/index.html")
    print("\n✨ Next steps:")
    print("   1. Review the website locally")
    print("   2. Deploy to hosting (GitHub Pages, Netlify, etc)")
    print("   3. Share with client")


if __name__ == "__main__":
    main()
