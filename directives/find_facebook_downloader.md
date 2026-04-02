# Directive: Find Facebook Video/Photo Downloader on GitHub

## Goal
Identify and evaluate existing Facebook downloader tools on GitHub that can extract videos and photos from profiles.

## Inputs
- GitHub search queries
- Criteria for evaluation (language, stars, maintenance status, capability)

## Process
1. Search GitHub for Facebook downloader tools using multiple queries:
   - "facebook video downloader"
   - "facebook photo scraper"
   - "facebook profile downloader"
   - "instagram facebook downloader"
2. Filter results by:
   - Stars/popularity (100+ preferred)
   - Recent activity (updated in last 12 months)
   - Language (Python preferred for ease of integration)
   - License (permissive licenses preferred)
3. Clone/analyze top candidates
4. Evaluate API/capabilities:
   - Can it download videos? Photos? Both?
   - Does it need authentication?
   - Rate limiting?
   - Output format?

## Tools/Scripts
- `execution/search_github.py` - Search GitHub API for projects

## Outputs
- Report with top 5 candidates
- Each with:
  - Repository link
  - Stars/forks
  - Last updated date
  - Language
  - Key capabilities
  - Setup requirements

## Edge Cases
- Some tools may require API keys (Facebook Graph API)
- Some may violate Facebook ToS (legal risk to note)
- Maintenance status varies widely
- Facebook actively restricts scraping and changes API

## Notes
Updated: 2026-04-01 - Initial setup. Facebook scraping is in legal gray area; recommend checking ToS compliance with client before implementation.
