#!/usr/bin/env python3
"""
Cloudflare Domain Setup Automation
Sets up smalltownboost.com with DNS records pointing to GitHub Pages
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
    print("CLOUDFLARE DOMAIN SETUP - smalltownboost.com")
    print("=" * 70)

    # Load environment
    env = load_env()
    token = env.get('CLOUDFLARE_API_TOKEN')

    if not token:
        print("❌ Error: CLOUDFLARE_API_TOKEN not found in .env")
        print("Please add your token to .env first")
        return False

    print("\n🔐 Testing API token...")

    # Get account info
    result = cloudflare_request('GET', '/accounts', token)
    if not result['success']:
        print(f"❌ Token error: {result['errors']}")
        return False

    if len(result['result']) == 0:
        print("❌ No accounts found")
        return False

    account_id = result['result'][0]['id']
    account_name = result['result'][0]['name']
    print(f"✓ Account: {account_name}")
    print(f"✓ Account ID: {account_id}")

    # Get zone info for smalltownboost.com
    print("\n🌐 Looking up zone for smalltownboost.com...")
    result = cloudflare_request('GET', '/zones?name=smalltownboost.com', token)

    if not result['success']:
        print(f"❌ Error: {result['errors']}")
        print("\n⚠️  Domain not added to Cloudflare account yet")
        print("\nSteps to add domain:")
        print("1. Go to https://dash.cloudflare.com/")
        print("2. Add Site → smalltownboost.com")
        print("3. Update nameservers at registrar")
        print("4. Wait 5-48 hours for propagation")
        print("5. Run this script again")
        return False

    if len(result['result']) == 0:
        print("⚠️  smalltownboost.com not found in your account")
        print("Please add it first via https://dash.cloudflare.com/")
        return False

    zone = result['result'][0]
    zone_id = zone['id']
    zone_name = zone['name']
    zone_status = zone['status']

    print(f"✓ Zone: {zone_name}")
    print(f"✓ Zone ID: {zone_id}")
    print(f"✓ Status: {zone_status}")

    # Get existing DNS records
    print("\n📋 Checking DNS records...")
    result = cloudflare_request('GET', f'/zones/{zone_id}/dns_records', token)

    if result['success']:
        records = result['result']
        print(f"✓ Found {len(records)} existing DNS records")
    else:
        print(f"⚠️  Could not fetch DNS records: {result['errors']}")

    # Create/update CNAME record for apex domain
    print("\n🔗 Setting up DNS record for GitHub Pages...")
    print("Creating CNAME record:")
    print("  Name: smalltownboost.com")
    print("  Target: spirenomads-boop.github.io")

    # Check if record exists
    cname_exists = False
    for record in records:
        if record['name'] == 'smalltownboost.com' and record['type'] in ['CNAME', 'A']:
            cname_exists = True
            print(f"✓ Record already exists: {record['type']} → {record['content']}")
            break

    if not cname_exists:
        # For apex domain, use A records (GitHub Pages IPs)
        github_ips = [
            '185.199.108.153',
            '185.199.109.153',
            '185.199.110.153',
            '185.199.111.153'
        ]

        print(f"\n✓ Creating A records pointing to GitHub Pages...")
        for ip in github_ips:
            data = {
                'type': 'A',
                'name': '@',
                'content': ip,
                'ttl': 3600,
                'proxied': False
            }
            result = cloudflare_request('POST', f'/zones/{zone_id}/dns_records', token, data)
            if result['success']:
                print(f"  ✓ A record created: {ip}")
            else:
                print(f"  ⚠️  Failed to create A record: {result['errors']}")

    # Update .env with credentials
    print("\n💾 Updating .env file...")

    with open('.env', 'r') as f:
        env_content = f.read()

    # Replace placeholders
    env_content = env_content.replace(
        'CLOUDFLARE_ACCOUNT_ID=your_cloudflare_account_id_here',
        f'CLOUDFLARE_ACCOUNT_ID={account_id}'
    )
    env_content = env_content.replace(
        'CLOUDFLARE_ZONE_ID=your_cloudflare_zone_id_here',
        f'CLOUDFLARE_ZONE_ID={zone_id}'
    )

    with open('.env', 'w') as f:
        f.write(env_content)

    print("✓ .env updated successfully")

    # Summary
    print("\n" + "=" * 70)
    print("✅ CLOUDFLARE SETUP COMPLETE!")
    print("=" * 70)
    print(f"\n📊 Configuration Summary:")
    print(f"   Domain: smalltownboost.com")
    print(f"   Account: {account_name}")
    print(f"   Zone ID: {zone_id}")
    print(f"   DNS Records: GitHub Pages A records")
    print(f"   Status: {zone_status}")

    print(f"\n🚀 Your site is now configured!")
    print(f"   Site URL: https://smalltownboost.com")
    print(f"   Git Repo: https://github.com/spirenomads-boop/smalltownboost")

    print(f"\n⏱️  DNS Propagation:")
    print(f"   Global propagation: 24-48 hours")
    print(f"   Check status: https://www.whatsmydns.net/")

    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
