# Directive: Scrape Facebook Messenger Conversations

## Goal
Extract messages, attachments, and metadata from Facebook Messenger conversations.

## Inputs
- Facebook account credentials (or authorized access)
- Chat ID or conversation URL
- Date range or specific conversation

## Technical Options

### Option A: Facebook Graph API (Official, Limited)
**Pros:** Safest, official, reliable
**Cons:** Very limited access, requires app review, may not include messages
**Use case:** Business accounts, official integrations
**Implementation:** Use `facebook-sdk`

### Option B: Selenium + Browser Automation (Hacks)
**Pros:** Full access, works on personal accounts
**Cons:** Fragile (Facebook changes HTML), easily detected as bot, violates ToS
**Use case:** Personal use, one-time exports
**Implementation:** Selenium with headless browser + CAPTCHA handling

### Option C: Official Facebook Data Export
**Pros:** Legitimate, no coding needed
**Cons:** Manual, large archives, slow processing
**Use case:** Data privacy requests
**Implementation:** User manual export via settings → Download Your Information

### Option D: Manual Screenshot + OCR (Extreme Fallback)
**Pros:** Always works
**Cons:** Slow, error-prone, limited data
**Use case:** Small conversations only

## Legal/Compliance Notes
⚠️ **IMPORTANT:**
- Scraping Messenger violates Facebook ToS
- Selenium automation is considered bot activity
- Only scrape your own account or with explicit written consent from message recipients
- Check privacy laws (GDPR, CCPA, etc.)
- Better option: Recommend client use official Facebook export

## Recommended Approach
1. **First option:** Ask client to use official Data Export (Settings → Download Your Information)
2. **If automation needed:** Use Selenium with rate limiting, user-agent rotation, and session persistence
3. **If API only:** Implement Graph API (limited but compliant)

## Edge Cases
- CAPTCHA challenges (requires manual intervention or CAPTCHA solving service)
- Two-factor authentication
- Checkpoints/security challenges from Facebook
- Deleted messages/conversations
- Large conversation histories (100k+ messages = slow)

## Notes
Updated: 2026-04-01 - This is technically and legally complex. Recommend starting with client's official export before attempting automated scraping.
