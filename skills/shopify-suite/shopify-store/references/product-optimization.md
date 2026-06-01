# Product Optimization — shopify-store Reference

Title formulas, description frameworks, and image standards for Shopify product pages.

---

## Title Formulas

### Formula by product type

**Apparel:**
```
[Product Name] — [Key Attribute] | [Brand]
Blue Linen Shirt — Relaxed Fit | Studio Name
Oversized Hoodie — 400gsm Cotton | Brand
```

**Electronics / tech:**
```
[Brand] [Product Name] [Model/Key Spec]
Brand Wireless Headphones ANC Pro 45hr
```

**Home goods / furniture:**
```
[Product Name] — [Material/Style] — [Size if relevant]
Oak Dining Table — Solid Wood — 160cm
Linen Throw Pillow — Natural — 45x45cm
```

**Beauty / skincare:**
```
[Product Name] — [Key Ingredient/Benefit] | [Brand]
Vitamin C Serum — Brightening 20% | Brand
```

**Food / consumables:**
```
[Product Name] — [Size/Format/Origin]
Organic Olive Oil — 500ml Cold Press
Colombian Coffee — Medium Roast 250g
```

### Title rules
- 50-70 characters (shows fully in Google SERP and Shopify search)
- Lead with product name, not brand (unless brand is the purchase driver)
- Include the one attribute buyers filter by most (color, size, material)
- No: "NEW", "SALE", "BEST SELLER", "!", "100% authentic"
- No: all caps
- No: variant info in title (size S/M/L goes in variants, not title)

---

## Meta Title Formulas

The meta title is separate from the product title in Shopify (Admin → SEO section).

```
[Product Name] [Key Attribute] — Buy Online | [Brand]
[Primary Keyword] — [Secondary Keyword] | [Brand]
```

Examples:
```
Linen Relaxed Shirt — Men's Summer Fashion | Studio Name
Wireless Noise Cancelling Headphones | Brand
Organic Olive Oil 500ml — Cold Pressed | Store Name
```

Rules:
- 50-60 characters (Google truncates at ~60)
- Include primary keyword near the front
- Include brand at end (recognition, not keyword — separator `|` or `—`)
- Different from the product title (if they're identical, one is wasted)

---

## Description Framework

### SPECS → STORY → SOCIAL PROOF structure

```
[Opening line: main benefit or use case — 1 sentence]

[Specs block: what it's made of, dimensions, key features — short bullets]

[Story paragraph: who it's for, when to use it, why it matters — 2-3 sentences]

[Trust closer: shipping, returns, sizing guide link — 1 sentence]
```

### Example (apparel)

```html
<p>A linen shirt built for warm weather — breathable, lightweight, and gets better with every wash.</p>

<ul>
  <li>100% European linen</li>
  <li>Relaxed fit, fits true to size</li>
  <li>Available in 8 colors</li>
  <li>Machine washable at 30°C</li>
</ul>

<p>Designed for easy summer days — works equally well with shorts or tailored trousers. 
The fabric softens naturally over time without losing its shape.</p>

<p>Free shipping on orders over €50. 30-day free returns. <a href="/pages/size-guide">Size guide</a>.</p>
```

### Example (electronics)

```html
<p>45 hours of active noise cancellation, zero compromise on sound quality.</p>

<ul>
  <li>ANC: -35dB noise reduction</li>
  <li>Battery: 45hr ANC on, 60hr ANC off</li>
  <li>Charging: USB-C, 15min = 5hr playback</li>
  <li>Connectivity: Bluetooth 5.3, multipoint (2 devices simultaneously)</li>
  <li>Weight: 248g</li>
</ul>

<p>Designed for long work sessions and travel. The over-ear cushions are memory foam — 
they seal out noise without pressure points after hours of wear.</p>

<p>2-year warranty. Free returns within 30 days. Ships in 1-2 business days.</p>
```

### Description rules
- Minimum 150 characters, aim for 300-500 characters
- First 160 characters become the meta description fallback — make them strong
- Lead with benefit, not feature ("stays cool" not "made of linen")
- Bullets for specs, prose for story — mix formats
- Include dimensions/weight for anything where size matters
- No fluff: "quality product", "you'll love it", "great for everyone"
- No generic manufacturer text — rewrite it

---

## Meta Description Formulas

```
[Main benefit]. [Key specs/features]. [Trust signal or CTA].
```

Examples:
```
Breathable linen shirt perfect for summer. Available in 8 colors, sizes XS-XXL. Free shipping over €50.
(134 chars)

Noise cancelling headphones with 45hr battery. Bluetooth 5.3, USB-C fast charge. 2-year warranty included.
(106 chars)

Cold-pressed organic olive oil from Spanish groves. 500ml bottle, harvested November 2024. Free delivery over €30.
(113 chars)
```

Rules:
- 120-160 characters
- Unique per product (not the same as title)
- Include a purchase-trigger: price signal, shipping benefit, time signal, social proof
- No clickbait ("You won't believe...")
- Ends with implicit CTA or benefit

---

## Image Standards

### Required images per product

| # | Image type | Purpose |
|---|-----------|---------|
| 1 | Hero / packshot | Main listing image — product centered, clean background |
| 2 | Lifestyle in context | Shows scale, use, aspiration |
| 3 | Detail / texture | Close-up of key material or feature |
| 4+ | Variant images | One per color/style variant |

### Technical specs

| Spec | Recommended | Minimum |
|------|-------------|---------|
| Dimensions | 2048×2048px | 800×800px |
| Format | JPEG (80-85% quality) | — |
| Aspect ratio | 1:1 (square) | Consistent per product |
| Background (main image) | White #FFFFFF or very light gray | Clean neutral |
| File size | < 500KB after optimization | < 1MB |

### Alt text formulas

```
Main image: [Brand] [Product Name] [Key Attribute]
"Studio Name Blue Linen Shirt Relaxed Fit"

Lifestyle: [Product Name] [Context]
"Linen Shirt worn at outdoor dinner"

Detail: [Product Name] [What the detail shows]
"Linen Shirt fabric texture close-up"
```

Rules:
- Describe what's in the image, not the product name repeated
- Don't start with "Image of" or "Photo of" — Google already knows it's an image
- Include color for variant images
- Max 125 characters

### Variant images

Every color variant needs its own image — minimum the hero shot on the correct color.
Shopify auto-switches image when customer selects a color variant if images are tagged with variant.

In Shopify admin: product images → click image → assign to variant.

---

## Collection Descriptions

Short, keyword-rich, benefit-first:

```
[What's in the collection — 1 sentence]. [Count or variety signal]. [Differentiator].
```

Examples:
```
Men's shirts in linen, cotton, and blends for every season. 40+ styles, new arrivals weekly. 
Free shipping on orders over €50.
```

```
Wireless headphones from entry-level to professional grade. Tested and reviewed by our audio team.
30-day trial period on every model.
```

Rules:
- 2-4 sentences
- Include primary keyword naturally
- Avoid "our collection of" or "we offer" — lead with what's in it
- Update seasonally for campaign collections

---

## Variant Naming

### Color naming

Use recognizable color names, not marketing names:
- "Navy Blue" not "Ocean Depths"
- "Forest Green" not "Emerald Whisper"
- "Off-White" not "Morning Mist"

Exception: luxury or high-differentiation brands where color naming IS part of the brand language.

### Size naming

Consistent across catalog:
- Apparel: XS, S, M, L, XL, XXL (not Extra Small, Small, etc.)
- Shoes: numeric EU sizing (42, 43...) not US mixed
- Home: dimensions in cm or specific names ("Small / 45×45cm")

### Option order

Color before size (most common filter order):
- Option 1: Color
- Option 2: Size
- Option 3: Material (if needed)
