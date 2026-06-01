# SEO — Shopify-Specific Issues

Shopify has structural SEO issues that generic SEO guides miss. This covers the ones that actually matter.

---

## Duplicate Content (Shopify's biggest SEO problem)

### The /products/ vs /collections/*/products/ problem

Shopify serves every product at two URLs:
- `https://store.com/products/blue-shirt`
- `https://store.com/collections/shirts/products/blue-shirt`

Shopify auto-canonicalizes collection-path URLs to the `/products/` URL. This is correct behavior — do not override it. But verify it's working:

```html
<!-- Should appear on /collections/shirts/products/blue-shirt -->
<link rel="canonical" href="https://store.com/products/blue-shirt">
```

If a custom theme or app overrides this, you get duplicate content penalties.

### Tag pages getting indexed

Shopify creates URLs for every tag: `/collections/shirts/t-shirts`, `/collections/shirts/blue`.
These are thin pages with subset content — they dilute link equity and create duplicates.

Fix: add to `robots.txt` (Shopify 2.0 allows custom robots.txt):
```
Disallow: /collections/*+*
```
Or noindex via theme liquid:
```liquid
{% if current_tags %}
  <meta name="robots" content="noindex, follow">
{% endif %}
```

### Variant URLs

`/products/blue-shirt?variant=123456` creates near-duplicate pages per variant.
Shopify canonicalizes these to the main product URL automatically. Do not disable this.

### Pagination

`/collections/shirts?page=2` — Shopify removed `rel="next"/"prev"` pagination support in 2019. Google handles these via `?page=N` parameters. Do not noindex paginated pages — you'll lose product indexing.

---

## Structured Data

### Product schema (must-have)

Shopify themes should output this on every product page. Check if yours does:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{{ product.title }}",
  "description": "{{ product.description | strip_html | escape }}",
  "image": "{{ product.featured_image | img_url: '800x' }}",
  "sku": "{{ product.selected_or_first_available_variant.sku }}",
  "brand": {
    "@type": "Brand",
    "name": "{{ product.vendor }}"
  },
  "offers": {
    "@type": "Offer",
    "priceCurrency": "{{ cart.currency.iso_code }}",
    "price": "{{ product.selected_or_first_available_variant.price | divided_by: 100.0 }}",
    "availability": "{% if product.available %}https://schema.org/InStock{% else %}https://schema.org/OutOfStock{% endif %}",
    "url": "{{ shop.url }}{{ product.url }}"
  }
  {% if product.metafields.reviews.rating %}
  ,"aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "{{ product.metafields.reviews.rating.value }}",
    "reviewCount": "{{ product.metafields.reviews.rating_count }}"
  }
  {% endif %}
}
</script>
```

### BreadcrumbList (improves SERP appearance)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "{{ shop.url }}" },
    { "@type": "ListItem", "position": 2, "name": "{{ collection.title }}", "item": "{{ shop.url }}{{ collection.url }}" },
    { "@type": "ListItem", "position": 3, "name": "{{ product.title }}" }
  ]
}
</script>
```

---

## Title and Meta Description Formulas

### Product pages
```
Title (50-60 chars): [Product Name] — [Key Attribute] | [Brand]
Example: "Blue Linen Shirt — Relaxed Fit | Mariano Studio"

Meta description (120-160 chars): [Benefit]. [Key features]. [CTA with differentiator].
Example: "Breathable linen shirt perfect for summer. Available in 8 colors, sizes XS-XXL. Free shipping over €50."
```

### Collection pages
```
Title: [Collection Name] — [Category] | [Brand]
Example: "Men's Shirts — Linen & Cotton | Mariano Studio"

Meta description: [What's in the collection]. [Count/variety]. [Differentiator].
Example: "Browse our collection of 40+ men's shirts in linen, cotton, and blends. New arrivals weekly. Free returns."
```

### Homepage
```
Title: [Brand] — [One-line value proposition]
Example: "Mariano Studio — Sustainable Linen Clothing for Men"
```

---

## Technical SEO Checklist

| Issue | Check | Fix |
|-------|-------|-----|
| Canonical tags | View source on product + collection URL | Should point to /products/ URL |
| Tag page indexation | Search site:store.com/collections inurl:t- | Add noindex or robots.txt disallow |
| Duplicate H1 | Check if theme puts product title in H1 twice | One H1 per page |
| Image alt texts | Inspect img tags on product pages | Fill via Shopify admin or bulk with metafields |
| Page speed | PageSpeed Insights on 3 pages | Remove heavy apps, optimize images |
| Sitemap | yourdomain.com/sitemap.xml | Should exist and include products + collections |
| robots.txt | yourdomain.com/robots.txt | Should not block /products/ or /collections/ |
| 404 errors | Google Search Console > Coverage | 301 redirect old URLs |

---

## Common Shopify SEO Mistakes

**Mistake: Disabling the Shopify sitemap**
The auto-generated sitemap at `/sitemap.xml` is good. Don't replace it with a custom one unless you have a specific reason. Many apps do this and break indexation.

**Mistake: Using a page builder for all pages**
Page builders like PageFly output custom HTML structures that often miss semantic tags (H1, structured data, canonical). Check that builder-created pages still have proper SEO markup.

**Mistake: Changing product handles**
`/products/old-handle` → `/products/new-handle` without a redirect = 404 = lost rankings.
Shopify doesn't auto-redirect when you change a handle. Add a URL redirect in admin: Settings → Policies → URL Redirects.

**Mistake: Publishing all variants as separate products**
One product with 5 color variants is better than 5 separate products. Consolidates link equity, avoids duplicate content.

**Mistake: Keeping "/a/collections/" filtering in index**
Some filter apps create `/collections/shirts?filter.p.product_type=Formal` URLs. These should be noindexed or disallowed.
