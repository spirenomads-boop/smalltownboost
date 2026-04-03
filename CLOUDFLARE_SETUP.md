# Cloudflare Setup for smalltownboost.com

## Domain Registration
- Domain: **smalltownboost.com**
- Registrar: **Cloudflare**

## API Token Setup

To manage DNS records and deploy the website via Cloudflare, you'll need to create an API token with appropriate permissions.

### Creating a Cloudflare API Token

1. **Login to Cloudflare Dashboard**: https://dash.cloudflare.com/
2. **Navigate to Settings** → **API Tokens**
3. **Create Token** with these permissions:
   - Zone / DNS / Edit
   - Zone / Page Rules / Manage
   - Account / Workers R2 Storage / Edit (if using Workers/R2)

### Required Tokens

Add to `.env`:

```env
CLOUDFLARE_API_TOKEN=your_token_here
CLOUDFLARE_ACCOUNT_ID=your_account_id_here
CLOUDFLARE_ZONE_ID=your_zone_id_here
```

#### How to find these values:

- **CLOUDFLARE_API_TOKEN**: Generate in API Tokens section
- **CLOUDFLARE_ACCOUNT_ID**: Account Settings → API → Zone ID (under your profile)
- **CLOUDFLARE_ZONE_ID**: Domain overview → Copy Zone ID

## DNS Records

Point **smalltownboost.com** to GitHub Pages:

```
Type: CNAME
Name: @
Content: spirenomads-boop.github.io
```

Or for apex domain routing:
```
Type: A
Name: @
Content: 185.199.108.153
       185.199.109.153
       185.199.110.153
       185.199.111.153
```

## Deploying to smalltownboost.com

### Option 1: GitHub Pages + Cloudflare DNS (Free)
- Already configured
- Uses Cloudflare DNS to point to GitHub Pages

### Option 2: Cloudflare Pages (Recommended)
- Direct integration with GitHub
- Auto-deploy on push
- Better performance

### Option 3: Workers (Advanced)
- Full serverless deployment
- Maximum control

## Next Steps

1. Update `.env` with Cloudflare credentials
2. Set DNS records in Cloudflare dashboard
3. Verify domain points to GitHub Pages
4. Test at https://smalltownboost.com

