# Directive: Build Business Website from Facebook Data

## Goal
Generate a responsive business website showcasing photos and videos scraped from Facebook profile.

## Inputs
- `data/facebook_profile.json` - Profile info and media URLs from scraper
- Client branding (optional: colors, logo, custom text)

## Process
1. Parse Facebook profile data
2. Generate HTML/CSS website with:
   - Hero section with business name and bio
   - Photo gallery (grid layout, lightbox)
   - Video section
   - Business info
   - Contact/social links
3. Deploy to `.tmp/website/` for testing
4. Ready for deployment to hosting (Netlify, Vercel, or custom server)

## Tools/Scripts
- `execution/build_website.py` - Generate HTML from template
- Uses: Jinja2 for templating

## Outputs
- `website/` directory with complete website files:
  - `index.html`
  - `styles.css`
  - `script.js`
  - `/assets/` - Images/videos

## Template Features
- Mobile responsive (CSS Grid/Flexbox)
- Gallery with lightbox
- Lazy loading for images
- Video embeds
- SEO-friendly
- Modern design

## Edge Cases
- Large number of images (100+) → paginate or lazy load
- Mixed media (some images, some videos)
- Missing metadata

## Next Steps
After generation, deploy via:
1. GitHub Pages (free)
2. Netlify (drag & drop)
3. Custom hosting

## Notes
Updated: 2026-04-01 - Static HTML generation. Can be enhanced with CMS later if needed.
