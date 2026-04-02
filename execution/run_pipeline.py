#!/usr/bin/env python3
"""
Main pipeline: Scrape Facebook profile → Build website
"""

import sys
import subprocess
from pathlib import Path


def run_command(script, args=None):
    """Run a Python script and return success status"""
    cmd = [sys.executable, script]
    if args:
        cmd.extend(args)

    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script}: {e}", file=sys.stderr)
        return False


def main():
    print("\n" + "="*70)
    print("FACEBOOK PROFILE → BUSINESS WEBSITE PIPELINE")
    print("="*70)

    if len(sys.argv) < 2:
        print("\n📋 USAGE:")
        print(f"   python {sys.argv[0]} <facebook_profile_url>")
        print("\n📌 EXAMPLES:")
        print("   python execution/run_pipeline.py 'https://www.facebook.com/YourBusiness'")
        print("   python execution/run_pipeline.py 'YourBusiness'  (auto-prepends URL)")
        sys.exit(1)

    profile_url = sys.argv[1]

    print(f"\n🎯 Target: {profile_url}\n")

    # Step 1: Scrape Facebook profile
    print("="*70)
    print("STEP 1: SCRAPING FACEBOOK PROFILE")
    print("="*70)
    if not run_command('execution/scrape_facebook_profile.py', [profile_url]):
        print("\n❌ Scraping failed. Check the error above.")
        sys.exit(1)

    # Check if data was created
    if not Path('data/facebook_profile.json').exists():
        print("❌ No profile data generated")
        sys.exit(1)

    # Step 2: Build website
    print("\n" + "="*70)
    print("STEP 2: BUILDING WEBSITE")
    print("="*70)
    if not run_command('execution/build_website.py'):
        print("\n❌ Website generation failed.")
        sys.exit(1)

    # Success!
    print("\n" + "="*70)
    print("✅ PIPELINE COMPLETE!")
    print("="*70)
    print("\n📍 Output locations:")
    print("   Data: data/facebook_profile.json")
    print("   Website: .tmp/website/index.html")
    print("\n🚀 Next steps:")
    print("   1. Open .tmp/website/index.html in browser to preview")
    print("   2. Deploy to GitHub Pages, Netlify, or your server")
    print("   3. Share the live link with your client!")


if __name__ == "__main__":
    main()
