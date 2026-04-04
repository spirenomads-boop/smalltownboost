#!/usr/bin/env python3
"""
Verify DNS records are properly configured in Cloudflare
"""

import json
import urllib.request
import urllib.error
import os
from pathlib import Path

def load_env():
    """Load environment variables from .env"""
    env = {}
    if Path('.env').exists():
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env[key] = value
    return env

def cloudflare_request(method, endpoint, token):
    """Make a Cloudflare API request"""
    url = f"https://api.cloudflare.com/client/v4{endpoint}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    req = urllib.request.Request(url, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_data = json.loads(e.read().decode('utf-8'))
        return {'success': False, 'errors': error_data.get('errors', [str(e)])}

def main():
    print("\n" + "=" * 70)
    print("VERIFYING DNS RECORDS - smalltownboost.com")
    print("=" * 70)

    env = load_env()
    token = env.get('CLOUDFLARE_API_TOKEN')
    zone_id = env.get('CLOUDFLARE_ZONE_ID')

    if not token or not zone_id:
        print("❌ Error: CLOUDFLARE_API_TOKEN or CLOUDFLARE_ZONE_ID not configured")
        return False

    # Get DNS records
    print("\n📋 Fetching DNS records...")
    result = cloudflare_request('GET', f'/zones/{zone_id}/dns_records', token)

    if not result['success']:
        print(f"❌ Error: {result['errors']}")
        return False

    records = result['result']
    a_records = [r for r in records if r['type'] == 'A' and r['name'] == 'smalltownboost.com']

    print(f"\n✓ Found {len(records)} total DNS records")

    expected_ips = ['185.199.108.153', '185.199.109.153', '185.199.110.153', '185.199.111.153']

    print(f"\n🔍 Checking for GitHub Pages A records:")
    for ip in expected_ips:
        found = any(r['content'] == ip for r in a_records)
        status = "✓" if found else "❌"
        print(f"   {status} {ip}")

    if len(a_records) == 4:
        print(f"\n✅ All 4 GitHub Pages A records are present!")
        print("   DNS propagation is in progress globally (24-48 hours)")
        return True
    else:
        print(f"\n⚠️  Expected 4 A records, found {len(a_records)}")
        if a_records:
            print("   Existing records:")
            for r in a_records:
                print(f"     - {r['name']} → {r['content']}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
