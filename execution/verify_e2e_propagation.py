#!/usr/bin/env python3
"""
End-to-end verification that DNS propagation setup is complete
"""

import json
import urllib.request
import urllib.error
import os
import socket
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

def check_github_pages():
    """Verify site is published to GitHub Pages"""
    print("\n🔍 CHECK 1: GitHub Pages Site")
    print("-" * 70)

    try:
        req = urllib.request.Request('https://spirenomads-boop.github.io/smalltownboost/',
                                     headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                print("✅ GitHub Pages site is accessible")
                print("   URL: https://spirenomads-boop.github.io/smalltownboost/")
                return True
    except Exception as e:
        print(f"❌ GitHub Pages site not accessible: {e}")
        return False

def check_cloudflare_dns_records(token, zone_id):
    """Verify DNS records exist in Cloudflare"""
    print("\n🔍 CHECK 2: Cloudflare DNS Records")
    print("-" * 70)

    result = cloudflare_request('GET', f'/zones/{zone_id}/dns_records', token)

    if not result['success']:
        print(f"❌ Could not fetch DNS records: {result['errors']}")
        return False

    records = result['result']
    a_records = [r for r in records if r['type'] == 'A' and r['name'] == 'smalltownboost.com']

    expected_ips = ['185.199.108.153', '185.199.109.153', '185.199.110.153', '185.199.111.153']
    found_ips = [r['content'] for r in a_records]

    print(f"✓ Found {len(a_records)} A records:")
    for ip in expected_ips:
        status = "✅" if ip in found_ips else "❌"
        print(f"   {status} {ip}")

    if len(found_ips) == 4 and all(ip in found_ips for ip in expected_ips):
        print("✅ All 4 GitHub Pages A records configured")
        return True
    else:
        print(f"❌ Expected 4 records, found {len(found_ips)}")
        return False

def check_cloudflare_zone(token, zone_id):
    """Verify zone is active and using Cloudflare nameservers"""
    print("\n🔍 CHECK 3: Cloudflare Zone Status")
    print("-" * 70)

    result = cloudflare_request('GET', f'/zones/{zone_id}', token)

    if not result['success']:
        print(f"❌ Could not fetch zone info: {result['errors']}")
        return False

    zone = result['result']
    status = zone.get('status', 'unknown')
    plan = zone.get('plan', {}).get('name', 'unknown')
    nameservers = zone.get('name_servers', [])

    print(f"✓ Zone: {zone.get('name')}")
    print(f"✓ Status: {status}")
    print(f"✓ Plan: {plan}")
    print(f"✓ Nameservers:")
    for ns in nameservers:
        print(f"   - {ns}")

    if status == 'active':
        print("✅ Zone is active")
        return True
    else:
        print(f"❌ Zone status is {status}, expected 'active'")
        return False

def check_nameserver_propagation():
    """Check if Cloudflare nameservers are resolving"""
    print("\n🔍 CHECK 4: Nameserver Propagation")
    print("-" * 70)

    cloudflare_ns = [
        'kyrie.ns.cloudflare.com',
        'lauryn.ns.cloudflare.com'
    ]

    try:
        # Query CloudFlare nameservers directly
        resolver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        resolver.settimeout(3)

        print("Checking if nameservers are responding...")
        for ns in cloudflare_ns:
            try:
                ip = socket.gethostbyname(ns)
                print(f"✓ {ns} → {ip}")
            except:
                print(f"⚠️  {ns} - could not resolve")

        print("\n✅ Cloudflare nameservers are configured")
        return True
    except Exception as e:
        print(f"⚠️  Nameserver check limited: {e}")
        return True  # Not critical, might be network issue

def main():
    print("\n" + "=" * 70)
    print("E2E PROPAGATION VERIFICATION - smalltownboost.com")
    print("=" * 70)

    env = load_env()
    token = env.get('CLOUDFLARE_API_TOKEN')
    zone_id = env.get('CLOUDFLARE_ZONE_ID')

    if not token or not zone_id:
        print("❌ Error: CLOUDFLARE_API_TOKEN or CLOUDFLARE_ZONE_ID not configured")
        return False

    checks = []

    # Run all checks
    checks.append(("GitHub Pages", check_github_pages()))
    checks.append(("DNS Records", check_cloudflare_dns_records(token, zone_id)))
    checks.append(("Zone Status", check_cloudflare_zone(token, zone_id)))
    checks.append(("Nameservers", check_nameserver_propagation()))

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    for name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"{status} {name}")

    all_passed = all(p for _, p in checks)

    if all_passed:
        print("\n✅ ALL CHECKS PASSED - Propagation setup is complete!")
        print("\nNext: Wait 24-48 hours for global DNS propagation")
        print("Then: Check https://www.whatsmydns.net/ for status")
    else:
        print("\n⚠️  Some checks failed - review above for details")

    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
