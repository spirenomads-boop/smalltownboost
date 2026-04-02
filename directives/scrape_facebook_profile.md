# Directive: Scrape Facebook Business Profile

## Goal
Extract photos and videos from a public Facebook business profile to populate a website.

## Inputs
- Facebook profile URL (public business page)
- Output format preference (JSON with media URLs)

## Process
1. Evaluate scraping approach:
   - Option A: Facebook Graph API (official, requires app approval)
   - Option B: HTML scraping + Selenium (works on public profiles, simpler setup)
2. Extract all photos:
   - Download metadata (URL, caption, date, likes)
   - Group by album if available
3. Extract all videos:
   - Metadata (URL, title, date, views)
4. Save to JSON structure for website generation
5. Download media files to `.tmp/media/`

## Tools/Scripts
- `execution/scrape_facebook_profile.py` - Main scraping script
- Uses: requests, BeautifulSoup (or Selenium if needed)

## Outputs
- `data/profile_data.json` - Photos and videos metadata
- `data/profile_info.json` - Profile info (name, bio, website, etc.)
- Media files cached in `.tmp/media/`

## Edge Cases
- Facebook blocks aggressive scraping (rate limiting, bot detection)
- Some media may require authentication even on "public" pages
- Facebook changes page structure frequently (may break scraper)
- Solution: Add delays between requests, rotate user agents, use Selenium for JavaScript-rendered content

## Legal/Compliance
- Only scrape profiles owned by/authorized by client
- Respect Facebook ToS
- Verify client owns the profile before proceeding

## Notes
Updated: 2026-04-01 - Using HTML scraping approach for MVP. If needed, can pivot to Graph API later.
