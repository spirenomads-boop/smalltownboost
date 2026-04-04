#!/usr/bin/env python3
"""
SEO Optimization for Jimny M65 Supercharger Kit Website
- Adds comprehensive meta tags
- Adds schema.org structured data
- Creates sitemap.xml
- Creates robots.txt
- Optimizes image alt text
"""

import json
from pathlib import Path

def optimize_html():
    """Add SEO meta tags and structured data to index.html"""

    html_file = Path('docs/index.html')
    content = html_file.read_text()

    # Enhanced meta tags with keywords, OG tags, etc.
    seo_meta_tags = '''    <meta name="keywords" content="Jimny M65 supercharger, Suzuki Jimny performance, M13A turbo, supercharger kit, bolt-on supercharger, Jimny upgrade">
    <meta name="author" content="Smalltownboost">
    <meta name="robots" content="index, follow">
    <meta name="language" content="English">

    <!-- Open Graph Meta Tags -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="Jimny M65 Supercharger Kit - Smalltownboost">
    <meta property="og:description" content="Eaton M65 Supercharger Kit for Suzuki Jimny M13A - Premium performance upgrade with instant torque and no turbo lag">
    <meta property="og:url" content="https://smalltownboost.com">
    <meta property="og:image" content="https://smalltownboost.com/hero.jpg">
    <meta property="og:site_name" content="Smalltownboost">
    <meta property="og:locale" content="en_CA">

    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Jimny M65 Supercharger Kit - Smalltownboost">
    <meta name="twitter:description" content="Transform your Suzuki Jimny with an Eaton M65 Supercharger. Instant power, massive torque, 1-day installation.">
    <meta name="twitter:image" content="https://smalltownboost.com/hero.jpg">

    <!-- Additional SEO Tags -->
    <meta name="canonical" content="https://smalltownboost.com">
    <link rel="alternate" hreflang="en-ca" href="https://smalltownboost.com">
    <link rel="icon" type="image/x-icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90' font-weight='bold' fill='%23d32f2f'>M65</text></svg>">'''

    # Schema.org Product markup
    product_schema = {
        "@context": "https://schema.org/",
        "@type": "Product",
        "name": "Jimny M65 Supercharger Kit",
        "description": "Eaton M65 Supercharger Kit for Suzuki Jimny M13A - Complete bolt-on performance upgrade with instant torque and no turbo lag",
        "brand": {
            "@type": "Brand",
            "name": "Smalltownboost"
        },
        "image": [
            "https://smalltownboost.com/hero.jpg",
            "https://smalltownboost.com/m65-turbo.jpg",
            "https://smalltownboost.com/logo.jpg"
        ],
        "offers": [
            {
                "@type": "Offer",
                "name": "Complete Kit",
                "price": "1840",
                "priceCurrency": "CAD",
                "description": "Complete Eaton M65 Supercharger Kit with bracket, piping, intercooler, and all hardware"
            },
            {
                "@type": "Offer",
                "name": "Bracket Kit Only",
                "price": "450",
                "priceCurrency": "CAD",
                "description": "Custom-fabricated steel bracket kit for Suzuki Jimny M13A"
            }
        ],
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "5",
            "reviewCount": "12"
        }
    }

    # Schema.org LocalBusiness markup
    localbusiness_schema = {
        "@context": "https://schema.org/",
        "@type": "LocalBusiness",
        "name": "Smalltownboost",
        "description": "Premium Suzuki Jimny Performance Upgrades - Specializing in the Eaton M65 Supercharger Kit",
        "url": "https://smalltownboost.com",
        "telephone": "+1-709-216-9055",
        "email": "709traviswatkins@gmail.com",
        "address": {
            "@type": "PostalAddress",
            "addressCountry": "CA"
        },
        "sameAs": [
            "https://www.facebook.com/travis.watkins.940"
        ]
    }

    # Schema.org FAQPage markup
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "How long does it take to install?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Roughly 1 day if you're prepared. Professional installation recommended."
                }
            },
            {
                "@type": "Question",
                "name": "Will it fit my Jimny?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Yes. Designed specifically for M13A (2007+). Perfect fit, proven."
                }
            },
            {
                "@type": "Question",
                "name": "Do I need tuning?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "YES. ECU calibration is critical. Works with 91 octane + professional tuning."
                }
            },
            {
                "@type": "Question",
                "name": "Why the M65?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Perfect balance of power, reliability, and drivability for the M13A. Proven OEM unit."
                }
            },
            {
                "@type": "Question",
                "name": "Is it reliable?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Eaton M65 is built to last. Used in Mercedes Kompressor for decades. Rebuild kits readily available."
                }
            },
            {
                "@type": "Question",
                "name": "Can I see it working?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Watch the videos above. Real prototype on Travis's personal Jimny. This is exactly what you get."
                }
            }
        ]
    }

    # Insert meta tags after <title>
    title_end = content.find('</title>')
    insert_pos = content.find('\n', title_end) + 1
    content = content[:insert_pos] + seo_meta_tags + '\n' + content[insert_pos:]

    # Find closing </head> tag and insert schema scripts before it
    schema_scripts = f'''    <!-- Schema.org Structured Data -->
    <script type="application/ld+json">
{json.dumps(product_schema, indent=2)}
    </script>
    <script type="application/ld+json">
{json.dumps(localbusiness_schema, indent=2)}
    </script>
    <script type="application/ld+json">
{json.dumps(faq_schema, indent=2)}
    </script>
'''

    head_close = content.find('</head>')
    content = content[:head_close] + schema_scripts + '\n    ' + content[head_close:]

    # Improve image alt text
    alt_improvements = [
        ('alt="Installation"', 'alt="Jimny M65 Supercharger Kit Installation - Custom bracket mounting on M13A engine"'),
        ('alt="Details"', 'alt="Supercharger Kit Components - Eaton M65 intercooler piping and bracket assembly"'),
        ('alt="Final"', 'alt="Completed M65 Supercharger Installation - Bolt-on kit fully integrated on Suzuki Jimny"'),
    ]

    for old, new in alt_improvements:
        content = content.replace(old, new)

    # Save optimized HTML
    html_file.write_text(content)
    print("✅ HTML optimized with SEO meta tags and structured data")

def create_sitemap():
    """Create sitemap.xml for search engines"""

    sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://smalltownboost.com/</loc>
        <lastmod>2026-04-03</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://www.smalltownboost.com/</loc>
        <lastmod>2026-04-03</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>'''

    sitemap_file = Path('docs/sitemap.xml')
    sitemap_file.write_text(sitemap)
    print("✅ Created sitemap.xml")

def create_robots():
    """Create robots.txt for search engine crawlers"""

    robots = '''# Robots.txt for smalltownboost.com
User-agent: *
Allow: /
Allow: /index.html
Allow: /videos/
Allow: /*.jpg
Allow: /*.css
Allow: /*.js

# Prevent indexing of private/temporary files
Disallow: /.env
Disallow: /.git
Disallow: /.github
Disallow: /.tmp

# Sitemap
Sitemap: https://smalltownboost.com/sitemap.xml
Sitemap: https://www.smalltownboost.com/sitemap.xml

# Crawl delay (optional - be respectful)
Crawl-delay: 1
'''

    robots_file = Path('docs/robots.txt')
    robots_file.write_text(robots)
    print("✅ Created robots.txt")

def main():
    print("\n" + "=" * 70)
    print("SEO OPTIMIZATION - smalltownboost.com")
    print("=" * 70)

    try:
        optimize_html()
        create_sitemap()
        create_robots()

        print("\n" + "=" * 70)
        print("✅ SEO OPTIMIZATION COMPLETE!")
        print("=" * 70)
        print("\nOptimizations Applied:")
        print("  ✓ Meta tags (keywords, author, robots)")
        print("  ✓ Open Graph tags (Facebook, LinkedIn)")
        print("  ✓ Twitter Card tags")
        print("  ✓ Canonical URL tag")
        print("  ✓ Language alternates")
        print("  ✓ Schema.org Product markup")
        print("  ✓ Schema.org LocalBusiness markup")
        print("  ✓ Schema.org FAQPage markup")
        print("  ✓ Improved image alt text")
        print("  ✓ Created sitemap.xml")
        print("  ✓ Created robots.txt")

        print("\nNext Steps:")
        print("  1. Commit and push changes")
        print("  2. Submit sitemap to Google Search Console")
        print("  3. Monitor indexing progress")
        print("  4. Check Search Console for any crawl errors")

        return True
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
