# App Stack — shopify-store Reference

App impact scoring, recommendations, and common app combinations for Shopify stores.

---

## Load Impact by Category

Each installed app runs JavaScript on storefront pages. Impact ranges from negligible to store-breaking.

| Category | Typical load impact | Notes |
|----------|--------------------| ------|
| Page builders (PageFly, GemPages, Shogun) | 400-800ms | Worst offenders — use only for specific pages |
| Upsell popups (Honeycomb, CartHook) | 300-500ms | Heavy cart manipulation |
| Live chat (Tidio, Gorgias, Intercom) | 200-400ms | Loads on every page |
| Loyalty / rewards (Yotpo, Smile.io) | 200-400ms | Loads even for non-members |
| Review apps (Judge.me, Loox, Yotpo) | 100-300ms | Load review widget on product pages |
| Email popups (Privy, OptiMonk, Wisepops) | 100-200ms | Often loads before first paint |
| Subscription (ReCharge, Bold) | 100-200ms | Modifies product page JS |
| Analytics (GA4, Klaviyo, Triple Whale) | 50-150ms | Pixels — minimize but unavoidable |
| SEO apps (SEO Manager, Plug in SEO) | 10-50ms | Mostly server-side |
| Inventory / shipping (ShipStation) | 0-50ms | Server-side only |

Rule: every app after the first 8 adds compounding load. With 15+ apps, mobile PageSpeed often drops below 30.

---

## Must-Have vs Nice-to-Have

### Must-have (most stores need these)

| Function | Recommended app | Free tier? |
|----------|----------------|-----------|
| Reviews | Judge.me | Yes — generous free plan |
| Email marketing | Klaviyo | Yes — up to 500 contacts |
| Live chat / support | Gorgias | No — starts ~€10/month |
| Abandoned cart recovery | Built into Klaviyo | — |
| Analytics | GA4 (native) | Free |

### Situational (only if you need the function)

| Function | App | When to use |
|----------|-----|------------|
| Subscriptions | ReCharge or Bold | Only if you sell subscription products |
| Loyalty program | Smile.io | Only if repeat purchase rate > 30% |
| Upsells in cart | CartHook or Rebuy | Only if AOV is a primary focus |
| Bundles | Bundler or Bold Bundles | Only if bundles are a core strategy |
| Wishlists | Wishlist Plus | Only if you have returning customers |
| Size guide | Kiwi Size Chart | Only if apparel with complex sizing |

### Avoid (or replace)

| Category | Problem | Alternative |
|----------|---------|------------|
| Page builders for all pages | Destroys performance, hard to maintain | Use only for landing pages |
| Multiple review apps | Duplicate reviews, social proof split | Pick one |
| Multiple email apps | Contacts split, conflicting automations | Pick one |
| SEO apps that modify canonicals | Can break Shopify's canonical logic | Remove — Shopify handles this |
| Instagram feed apps | Embed kills performance | Use manual or theme built-in |

---

## Common App Stack Profiles

### Small direct-to-consumer (< 500 orders/month)

```
Reviews:        Judge.me (free)
Email:          Klaviyo (free up to 500 contacts)
Analytics:      GA4 (free)
Shipping label: ShipStation or Sendcloud
Total apps: 4
Monthly cost: ~€0-50
```

### Growing DTC (500-5000 orders/month)

```
Reviews:        Judge.me (paid) or Okendo
Email/SMS:      Klaviyo
Support:        Gorgias
Subscriptions:  ReCharge (if applicable)
Upsell:         Rebuy or CartHook (one only)
Analytics:      GA4 + Triple Whale
Shipping:       ShipStation or EasyShip
Total apps: 6-8
Monthly cost: ~€200-500
```

### High-volume (5000+ orders/month)

```
Reviews:        Okendo or Stamped
Email:          Klaviyo
SMS:            Attentive or Postscript (dedicated — not Klaviyo SMS)
Support:        Gorgias (full team)
Loyalty:        Yotpo or Smile.io (if retention strategy active)
Subscriptions:  ReCharge or Skio
Analytics:      Triple Whale + GA4
Upsell:         Rebuy (full suite)
Returns:        Loop Returns
Total apps: 9-11
Monthly cost: ~€1000-3000
```

---

## App Conflict Patterns

### Review app conflicts

Having both Judge.me and Yotpo (or any two review apps) causes:
- Schema structured data duplication (two `aggregateRating` blocks)
- Review import/sync conflicts
- Double review request emails to customers

Fix: pick one, import reviews from the other, uninstall duplicate.

### Page builder + theme editor conflict

PageFly / GemPages build pages using their own block structure. If the same page also has sections in theme editor, conflicts occur:
- Duplicate content sections
- Theme editor shows blank preview
- Inconsistent rendering on mobile

Fix: page builder pages should be built entirely in the builder. Don't mix.

### Email platform conflicts

Klaviyo + Omnisend on the same store = contacts getting double emails, confusing data.
Fix: pick one, migrate flows, uninstall the other.

### Multiple pixel apps

GA4 + Klaviyo + Triple Whale + Facebook Pixel all loading independently vs using a centralized pixel manager:
- Duplicate pageview/purchase events
- Attribution data conflicts

Fix: use one source of truth for attribution (Triple Whale or Northbeam for paid), let GA4 be independent.

---

## App Audit Output Format

When reporting app stack findings:

```markdown
## App Stack Audit

Total apps installed: X
Estimated total load impact: ~XXXms

### High Impact (remove or investigate)
| App | Impact | Recommendation |
|-----|--------|---------------|
| PageFly | ~600ms | Remove from non-landing pages. Keep for campaign pages only |
| Tidio | ~350ms | Replace with Gorgias if support volume justifies cost, else remove |

### Redundant Apps
- Judge.me + Loox: both review apps. Remove Loox, consolidate on Judge.me.

### Low Usage / Abandoned
- [App Name]: last updated 2022, no recent activity in Shopify App Store

### Keep
| App | Impact | Why |
|-----|--------|-----|
| Klaviyo | ~100ms | Core email marketing — high ROI |
| GA4 | ~50ms | Essential analytics |
| Judge.me | ~150ms | Reviews driving conversion |

### Estimated savings if recommendations applied
Load time reduction: ~850ms
Monthly cost reduction: ~€XX
```
