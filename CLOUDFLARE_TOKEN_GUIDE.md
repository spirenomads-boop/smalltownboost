# Cloudflare API Token Setup Guide

## Create a Comprehensive Token

To automate domain setup and deployment for smalltownboost.com, create a token with these exact permissions:

### Step-by-Step Token Creation

1. **Go to**: https://dash.cloudflare.com/profile/api-tokens
2. **Click**: "Create Token"
3. **Select**: "Custom token" (don't use templates)
4. **Token Name**: `smalltownboost-deploy`

### Required Permissions

Add these permissions to your token:

#### Zone Permissions:
- ✅ **Zone** → **Zone Settings** → **Read**
- ✅ **Zone** → **DNS** → **Edit**
- ✅ **Zone** → **Zone** → **Read**
- ✅ **Zone** → **Nameserver** → **Manage**
- ✅ **Zone** → **Page Rules** → **Manage**
- ✅ **Zone** → **Workers Routes** → **Write** (optional, for Workers)

#### Account Permissions:
- ✅ **Account** → **Account Settings** → **Read**
- ✅ **Account** → **Workers Routes** → **Write** (optional, for Workers)

#### Zone Resources:
- ✅ Include → **Specific zone** → `smalltownboost.com` (once added to account)

### Token Summary

When created, your token should have:
- **Account**: Ian@puresouls.ca's Account
- **Permissions**: All DNS, Zone, and Nameserver management
- **Zone Resources**: smalltownboost.com

## Scopes for Automation

Your token needs these scopes to:
- **Add/Update DNS records** → `Zone:DNS:Edit`
- **Manage nameservers** → `Zone:Nameserver:Manage`
- **Read zone info** → `Zone:Zone:Read`
- **Access account info** → `Account:Account Settings:Read`

## Testing the Token

Once created, copy the token and update `.env`:
```
CLOUDFLARE_API_TOKEN=your_new_token_here
```

Then run:
```bash
python3 execution/cloudflare_setup.py
```

This will:
1. Verify token access
2. Find your Account ID
3. Find your Zone ID for smalltownboost.com
4. Update `.env` automatically
5. Configure DNS records pointing to GitHub Pages
6. Verify everything is set up correctly

## What the Script Does

- ✅ Fetches account information
- ✅ Lists available zones
- ✅ Retrieves Zone ID for smalltownboost.com
- ✅ Creates CNAME record (@ → spirenomads-boop.github.io)
- ✅ Updates `.env` with all credentials
- ✅ Verifies DNS propagation

## Security Notes

- **Never commit** `.env` to git (it's in `.gitignore`)
- **Keep token private** - regenerate if compromised
- Token expires in 1 year by default
- Can set custom expiration (recommended: 90 days)

## Troubleshooting

**Zone not found?**
- Domain must be added to Cloudflare account first
- Wait for nameserver propagation (5-48 hours)
- Verify domain is active in Cloudflare dashboard

**Permission denied?**
- Ensure token has all required scopes
- Create new token with correct permissions
- Don't reuse old/limited tokens

**DNS not resolving?**
- Wait 24-48 hours for full propagation
- Check nameserver update at registrar
- Verify CNAME record in Cloudflare dashboard
