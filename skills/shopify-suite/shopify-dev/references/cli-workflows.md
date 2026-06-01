# CLI Workflows — shopify-dev Reference

Shopify CLI commands for theme and app development. Verified against CLI 3.x.

---

## Installation

```bash
npm install -g @shopify/cli@latest
shopify version
```

Requires Node 18+. Authentication is store-scoped (you authenticate per store).

---

## Theme Development

### Basic workflow

```bash
# Authenticate and pull from live theme
shopify theme dev --store your-store.myshopify.com

# Start dev server on specific theme
shopify theme dev --store your-store.myshopify.com --theme THEME_ID

# Check what themes exist
shopify theme list --store your-store.myshopify.com

# Pull theme files to local
shopify theme pull --store your-store.myshopify.com --theme THEME_ID

# Push to a specific theme (NOT live — always push to unpublished theme first)
shopify theme push --store your-store.myshopify.com --theme THEME_ID

# Push to new theme (creates it)
shopify theme push --unpublished --store your-store.myshopify.com

# Publish a theme (makes it live)
shopify theme publish --store your-store.myshopify.com --theme THEME_ID
```

### Targeting specific files

```bash
# Push only changed files
shopify theme push --only sections/header.liquid

# Ignore files during push/pull
shopify theme push --ignore "config/settings_data.json"
shopify theme pull --ignore "templates/*.json"
```

### Multiple environments

Define in `shopify.theme.toml`:

```toml
[environments.development]
store = "dev-store.myshopify.com"
theme = "123456789"
ignore = ["config/settings_data.json"]

[environments.staging]
store = "staging-store.myshopify.com"
theme = "987654321"

[environments.production]
store = "prod-store.myshopify.com"
theme = "111111111"
```

Then:
```bash
shopify theme dev --environment development
shopify theme push --environment staging
shopify theme push --environment production
```

### Check for errors

```bash
shopify theme check
shopify theme check --output json

# Check specific files
shopify theme check sections/product-form.liquid
```

`theme check` validates Liquid syntax, section schemas, deprecated filters, accessibility issues.

---

## App Development

### Scaffold a new app

```bash
npm init @shopify/app@latest
# Prompts: app name, template (Remix recommended), language (TypeScript or JS)
cd my-app
npm install
```

### Start dev server

```bash
shopify app dev
# Starts: local server + tunnel (Cloudflare ngrok) + updates app URLs in Dev Dashboard
```

Dev server requirements:
- Authenticated Shopify Partner/Dev Dashboard account
- App created in Dev Dashboard (first run prompts you to create)
- `.shopify/project.toml` created automatically on first `dev`

### Environment config

`.env` file (auto-created, never commit):
```
SHOPIFY_API_KEY=your-client-id
SHOPIFY_API_SECRET=your-client-secret
SCOPES=write_products,read_orders
```

### Deploy to production

```bash
shopify app deploy
# Builds, runs type check, deploys extensions to Shopify
# Does NOT deploy the web server — deploy that to Vercel/Railway/etc.
```

### Generate extension scaffold

```bash
# Checkout UI extension
shopify app generate extension --type checkout_ui_extension

# Product subscription
shopify app generate extension --type product_subscription

# Admin action
shopify app generate extension --type admin_action

# Web pixel
shopify app generate extension --type web_pixel_extension
```

### App info

```bash
shopify app info
# Shows: app name, client ID, extensions, deployment status
```

---

## Authentication

```bash
# Login to a store
shopify auth login --store your-store.myshopify.com

# Check current auth status
shopify auth status

# Logout
shopify auth logout
```

First `shopify app dev` or `shopify theme dev` on a new machine prompts for auth.

---

## Useful Flags

| Flag | Command | What it does |
|------|---------|-------------|
| `--store` | theme | Target store domain |
| `--theme THEME_ID` | theme | Target specific theme |
| `--environment` | theme | Use environment from .toml |
| `--only file.liquid` | theme push/pull | Scope to specific files |
| `--ignore "pattern"` | theme push/pull | Exclude files |
| `--unpublished` | theme push | Create new unpublished theme |
| `--live` | theme push | Push to currently active theme |
| `--json` | most commands | Machine-readable output |
| `--verbose` | most commands | Debug output |

---

## CI/CD Pattern

### GitHub Actions — theme deploy

```yaml
name: Deploy Theme

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: 18

      - name: Install Shopify CLI
        run: npm install -g @shopify/cli@latest

      - name: Deploy to staging
        env:
          SHOPIFY_CLI_THEME_TOKEN: ${{ secrets.SHOPIFY_CLI_THEME_TOKEN }}
        run: |
          shopify theme push \
            --store ${{ secrets.SHOPIFY_STORE }} \
            --theme ${{ secrets.STAGING_THEME_ID }} \
            --allow-live \
            --no-color
```

Generate `SHOPIFY_CLI_THEME_TOKEN`:
1. Shopify Admin → Settings → Apps and sales channels → Develop apps
2. Create app with `write_themes` scope
3. Get Admin API access token

### GitHub Actions — app deploy extensions

```yaml
- name: Deploy app extensions
  env:
    SHOPIFY_API_KEY: ${{ secrets.SHOPIFY_API_KEY }}
    SHOPIFY_API_SECRET: ${{ secrets.SHOPIFY_API_SECRET }}
  run: shopify app deploy --no-release
```

---

## Common Errors

**`Error: No store provided`** — add `--store` flag or set in `shopify.theme.toml`

**`Error: Theme not found`** — wrong THEME_ID. Run `shopify theme list` to get correct ID.

**`Error: Cannot push to live theme`** — use `--allow-live` flag explicitly, or push to unpublished theme first.

**`Error: SHOPIFY_CLI_THEME_TOKEN not set`** — CI/CD needs token. See token generation above.

**`Error: Extensions failed to deploy`** — check extension `shopify.extension.toml` for schema errors. Run `shopify app generate extension` again if structure is corrupted.
