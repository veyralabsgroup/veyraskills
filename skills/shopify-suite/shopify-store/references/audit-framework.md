# Audit Framework — shopify-store Reference

Full checklists per audit dimension. Use in Phase A2 (MCP mode) or as guided questions in Mode B.

---

## Dimension 1: Product Catalog Health

### Title quality
- [ ] Formula: `[Brand] [Product Name] [Key Attribute]` or `[Product Name] — [Key Attribute] | [Brand]`
- [ ] Length: 50-70 characters (optimal for search and Shopify search)
- [ ] No ALL CAPS titles
- [ ] Consistent naming convention across catalog
- [ ] Variant info NOT in title (use variant options instead)

### Description quality
- [ ] Minimum 100 characters (short = thin content signal)
- [ ] First 160 chars sellable (meta description often auto-pulled from here)
- [ ] Includes: material, dimensions/sizing, use case, care instructions
- [ ] No copy-paste manufacturer descriptions (duplicate content)
- [ ] HTML formatting: `<p>`, `<ul>`, `<strong>` — no inline styles

### Images
- [ ] At least 3 images per product (main, lifestyle, detail)
- [ ] Alt texts filled on all images
- [ ] Consistent aspect ratio across catalog (1:1 or 4:3 recommended)
- [ ] Main image: pure product on white/neutral background
- [ ] File names: descriptive, not `IMG_00123.jpg`

### Variants
- [ ] No "Default Title" variants (indicates single-variant product with unfilled options)
- [ ] Consistent option naming: "Color" not "Colour"/"color"
- [ ] All variants have prices set
- [ ] SKUs filled (important for inventory tracking + ads)
- [ ] Compare-at price set for discounted items

### Scoring guide
- 9-10: All titles/descriptions/images consistent, no gaps
- 7-8: Minor gaps (< 10% products missing something)
- 5-6: Noticeable gaps (10-30% products incomplete)
- 3-4: Systematic gaps (> 30% products missing descriptions or images)
- 1-2: Most products have placeholder titles/descriptions/no images

---

## Dimension 2: Collection Architecture

### Structure
- [ ] Maximum 2 levels deep (Collections → Sub-collections)
- [ ] Every product assigned to at least 1 collection
- [ ] No duplicate collections (e.g., "Shirts" and "All Shirts" serving same purpose)
- [ ] Clear naming: user should understand what's in collection from name alone

### Smart vs manual collections
- Smart collection: rule-based (product type, tag, vendor)
- Manual collection: hand-curated

Recommendation:
- Use smart for ongoing catalogs (auto-adds new products)
- Use manual for editorial/campaign collections (Homepage Feature, Seasonal Sale)

### Overlap check
- Product in > 3 collections = potential confusion
- Products in 0 collections = invisible from navigation (check orphans)

### Collection quality
- [ ] Each collection has description (good for SEO + context)
- [ ] Collection images set
- [ ] Sort order intentional (Best Selling or Manual, not default alphabetical)
- [ ] Smart collection rules actually filtering correctly (check product count vs expectation)

### Scoring guide
- 9-10: Clean 2-level hierarchy, all products assigned, no orphans
- 7-8: Minor orphans or 1-2 redundant collections
- 5-6: Flat or too-deep structure, some orphans
- 3-4: Poor structure, many orphans, confusing naming
- 1-2: No meaningful collection structure

---

## Dimension 3: Navigation

### Header navigation
- [ ] Max 7 primary navigation items (cognitive overload above 7)
- [ ] Max 2 levels deep in dropdown
- [ ] Hierarchy matches collection architecture
- [ ] All collections reachable from header or footer
- [ ] Search visible and functional (header placement preferred)
- [ ] Cart icon visible with item count

### Footer navigation
- [ ] Customer service links: Contact, Returns, FAQ, Shipping Policy
- [ ] Legal: Privacy Policy, Terms of Service, Cookie Policy
- [ ] Social media links (if active)
- [ ] Newsletter signup (if applicable)

### Mobile navigation
- [ ] Hamburger menu or equivalent
- [ ] Touch targets: minimum 44×44px
- [ ] No hover-dependent menus (hover doesn't exist on mobile)

### Scoring guide
- 9-10: Logical, complete, mobile-friendly
- 7-8: Minor gaps (missing footer link, one level too deep somewhere)
- 5-6: Navigation functional but confusing structure
- 3-4: Missing important links, mobile navigation broken
- 1-2: Navigation actively misleading or broken

---

## Dimension 4: SEO

Full Shopify-specific SEO checklist in `references/seo-shopify.md`.

Quick scoring checklist:
- [ ] Meta titles: 50-60 chars, primary keyword included
- [ ] Meta descriptions: 120-160 chars, every product + collection has one
- [ ] No duplicate content from `/collections/*/products/` — canonicals correct
- [ ] Tag pages handled (noindex or robots.txt)
- [ ] Structured data present on product pages (Product schema)
- [ ] Sitemap accessible at `/sitemap.xml`
- [ ] robots.txt not blocking product/collection pages
- [ ] Google Search Console connected and no coverage errors

### Scoring guide
- 9-10: All meta filled, no canonical issues, structured data present
- 7-8: Small gaps (< 20% products missing meta description)
- 5-6: Systematic gaps or known duplicate content issues
- 3-4: Most products missing SEO meta, or active duplicate content
- 1-2: robots.txt blocking index, or no meta data across site

---

## Dimension 5: App Stack

Full app scoring in `references/app-stack.md`.

Quick check:
- [ ] Total apps installed: < 8 (each adds load time)
- [ ] No duplicate functionality (2 review apps, 2 email platforms)
- [ ] No abandoned apps (last updated > 18 months)
- [ ] Page builder: max 1, and not used on all pages
- [ ] Apps with monthly cost vs actual usage ratio

### Load impact tiers
- High impact (400-800ms): page builders, upsell popups, loyalty widgets
- Medium impact (100-300ms): review apps, email popups, live chat
- Low impact (< 100ms): analytics pixels, metafield apps

### Scoring guide
- 9-10: Lean stack (< 6 apps), no redundancy, all actively used
- 7-8: 6-9 apps, minor redundancy or one unused
- 5-6: 10-14 apps, some redundancy
- 3-4: 15+ apps, multiple redundant apps, page builder on all pages
- 1-2: Severely bloated (20+ apps), duplicate core functions, confirmed speed impact

---

## Dimension 6: Conversion Signals

### Product page trust
- [ ] Reviews visible above the fold on desktop
- [ ] Reviews visible before "Add to Cart" on mobile
- [ ] Review count shown (social proof — "1,243 reviews" beats 5 stars alone)
- [ ] Shipping estimate visible on product page
- [ ] Return policy visible (or link to it)
- [ ] Secure payment icons visible

### Urgency / scarcity
- [ ] Low stock counter shown when < 5 units (optional but high impact)
- [ ] Restock notification option if out of stock
- [ ] Sale badge on discounted items

### Add to cart
- [ ] CTA button above the fold on desktop
- [ ] CTA sticky or fixed on mobile scroll
- [ ] Size/color selector intuitive (swatches preferred over dropdown for color)
- [ ] Variant images update when switching color

### Cart / Checkout
- [ ] Upsell or cross-sell in cart (optional but measurable)
- [ ] Shipping threshold visible ("Add €X for free shipping")
- [ ] Checkout trust elements: SSL, accepted payment methods
- [ ] No forced account creation before checkout

### Scoring guide
- 9-10: Reviews prominent, trust signals complete, CTA optimized for mobile
- 7-8: Minor gaps (no shipping estimate on product page, reviews below fold)
- 5-6: Functional but missing key trust signals
- 3-4: No reviews visible, poor mobile CTA, no trust elements
- 1-2: Active friction (forced account, no payment icons, reviews hidden)

---

## Priority Matrix

| Score | Dimension | Recommended Action |
|-------|-----------|-------------------|
| 1-4 | Any | Immediate fix — blocking sales |
| 5-6 | Catalog/SEO | High priority — compound impact |
| 5-6 | Conversion | High priority — direct revenue impact |
| 5-6 | Navigation | Medium priority — UX issue |
| 7-8 | Any | Optimize when above issues resolved |
| 9-10 | Any | Maintain — no action needed |

Start with lowest-scoring dimensions that have the highest traffic.
