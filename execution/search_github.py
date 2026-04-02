#!/usr/bin/env python3
"""
Search GitHub for Facebook downloader projects
"""

import requests
import json
from datetime import datetime
from pathlib import Path
import sys

# GitHub API endpoint
GITHUB_API = "https://api.github.com/search/repositories"

# Search queries
SEARCH_QUERIES = [
    "facebook video downloader",
    "facebook photo scraper",
    "facebook profile downloader",
    "facebook media downloader",
]

def search_github(query, per_page=10):
    """Search GitHub for repositories matching query"""
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": per_page,
    }

    try:
        response = requests.get(GITHUB_API, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get("items", [])
    except requests.RequestException as e:
        print(f"Error searching GitHub for '{query}': {e}", file=sys.stderr)
        return []

def filter_results(repos, min_stars=50):
    """Filter repositories by criteria"""
    filtered = []

    for repo in repos:
        # Skip if not enough stars
        if repo["stargazers_count"] < min_stars:
            continue

        # Skip if last update is too old (>24 months)
        updated_date = datetime.fromisoformat(repo["updated_at"].replace("Z", "+00:00"))
        months_since_update = (datetime.now(updated_date.tzinfo) - updated_date).days / 30
        if months_since_update > 24:
            continue

        license_info = repo.get("license")
        license_name = license_info.get("name") if license_info else "No license specified"

        filtered.append({
            "name": repo["full_name"],
            "url": repo["html_url"],
            "description": repo["description"],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "language": repo["language"],
            "last_updated": repo["updated_at"],
            "license": license_name,
        })

    return filtered

def main():
    print("Searching GitHub for Facebook downloader projects...\n")

    all_results = []

    # Search using multiple queries
    for query in SEARCH_QUERIES:
        print(f"Searching: {query}")
        results = search_github(query, per_page=15)
        filtered = filter_results(results, min_stars=50)
        all_results.extend(filtered)

    # Remove duplicates (same repo found in multiple searches)
    seen = set()
    unique_results = []
    for repo in all_results:
        if repo["url"] not in seen:
            seen.add(repo["url"])
            unique_results.append(repo)

    # Sort by stars
    unique_results.sort(key=lambda x: x["stars"], reverse=True)

    # Take top 10
    top_results = unique_results[:10]

    # Save to .tmp/
    output_path = Path(".tmp/facebook_downloader_candidates.json")
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(top_results, f, indent=2)

    print(f"\n✓ Found {len(top_results)} candidates")
    print(f"Results saved to: {output_path}\n")

    # Print summary
    for i, repo in enumerate(top_results, 1):
        print(f"{i}. {repo['name']}")
        print(f"   ⭐ {repo['stars']} stars | 🍴 {repo['forks']} forks")
        print(f"   📝 {repo['language'] or 'Unknown language'}")
        print(f"   📅 {repo['last_updated'][:10]}")
        print(f"   📜 {repo['license']}")
        print(f"   🔗 {repo['url']}")
        if repo["description"]:
            print(f"   {repo['description']}")
        print()

if __name__ == "__main__":
    main()
