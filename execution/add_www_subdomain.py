#!/usr/bin/env python3
"""
Add www subdomain CNAME record to Cloudflare
"""

import json
import urllib.request
import urllib.error
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

def cloudflare_request(method, endpoint, token, data=None):
    """Make a Cloudflare API request"""
    url = f"https://api.cloudflare.com/client/v4{endpoint}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    req_data = None
    if data:
        req_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_data = json.loads(e.read().decode('utf-8'))
        return {'success': False, 'errors': error_data.get('errors', [str(e)])}

def main():
    print("\n" + "=" * 70)
    print("ADDING WWW SUBDOMAIN - www.smalltownboost.com")
    print("=" * 70)

    env = load_env()
    token = env.get('CLOUDFLARE_API_TOKEN')
    zone_id = env.get('CLOUDFLARE_ZONE_ID')

    if not token or not zone_id:
        print("❌ Error: CLOUDFLARE_API_TOKEN or CLOUDFLARE_ZONE_ID not configured")
        return False

    # Create CNAME record for www
    print("\n🔗 Creating CNAME record for www...")
    data = {
        'type': 'CNAME',
        'name': 'www',
        'content': 'smalltownboost.com',
        'ttl': 3600,
        'proxied': False
    }

    result = cloudflare_request('POST', f'/zones/{zone_id}/dns_records', token, data)

    if result['success']:
        record = result['result']
        print(f"✅ CNAME record created:")
        print(f"   Name: {record['name']}")
        print(f"   Content: {record['content']}")
        print(f"   TTL: {record['ttl']}")
    else:
        print(f"❌ Failed to create CNAME record: {result['errors']}")
        return False

    print("\n" + "=" * 70)
    print("✅ WWW SUBDOMAIN CONFIGURED!")
    print("=" * 70)
    print(f"\nDomain: https://www.smalltownboost.com")
    print(f"Status: CNAME → smalltownboost.com → GitHub Pages")
    print(f"\nBoth www and non-www versions should now work!")

    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
