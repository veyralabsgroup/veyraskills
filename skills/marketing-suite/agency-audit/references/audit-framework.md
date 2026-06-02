# Audit Framework

Severity criteria and evaluation standards for agency-audit. Applied in Phase 3 to prioritize findings.

---

## Severity Levels

### Critical
Fix before anything else. Likely costing leads, revenue, or search visibility right now.

Criteria - any of:
- No value proposition visible above the fold
- No CTA on homepage
- Website not indexed (robots.txt blocks all)
- No HTTPS
- Page loads completely broken on mobile
- 0 social proof elements on a service business site
- Contact form broken

### Important
Real impact, but not emergency. Should be in first 60 days of any engagement.

Criteria - any of:
- Title tag missing or using "Home | Company Name" with no keywords
- H1 missing or generic ("Welcome to our website")
- No Google Analytics or tracking installed
- No Meta Pixel despite running or wanting to run paid ads
- Pricing completely hidden when competitors show it
- Copy is feature-first with no mention of customer problems
- No blog or content section (for SEO-dependent businesses)

### Quick Win
Low effort, visible improvement. Good for early trust-building with client.

Criteria - all of:
- Fix takes under 1 working day
- Result is immediately visible (rankings, UX, or analytics)
- No design or development risk

Examples:
- Add/fix meta description
- Change CTA from "Submit" to action-based text
- Add alt text to hero image
- Install Google Tag Manager
- Add a testimonial section with 2-3 real quotes
- Add phone number to header
- Fix broken links

### Minor
Real but low priority. Include in full report, not in executive summary.

Criteria:
- Cosmetic or edge case
- Impact is marginal
- Only relevant after more important issues are fixed

---

## Audit Dimensions

### 1. Value Proposition (weight: very high)

The single most important element. If a visitor cannot answer "what does this company do and for whom?" in 3 seconds, everything else is a rounding error.

Check:
- Headline: specific or generic?
- Sub-headline: expands on headline or repeats it?
- First-screen CTA: present? action verb? benefit-clear?
- Who it's for: stated explicitly?

Score:
- 3/3: Clear headline + clear audience + visible CTA
- 2/3: Two elements present
- 1/3: One element present
- 0/3: None clear

### 2. SEO Fundamentals (weight: high)

Not deep SEO - the basics that affect whether Google can find, understand, and display the page.

Check:
- Title tag: present, under 60 chars, includes primary keyword
- Meta description: present, 120-160 chars, has CTA or benefit
- H1: present, single, matches page intent
- H2-H6: logical hierarchy
- Image alt text: present on decorative + informational images
- Internal links: at least some to key pages
- Canonical tag: present if needed
- Sitemap: findable at /sitemap.xml or linked in robots.txt

### 3. Conversion Signals (weight: high)

Visitors arrive. Are they converting? What stops them?

Check:
- Number of CTAs on homepage (0 = problem, 1-3 = good, 5+ = cluttered)
- CTA language quality (action verb + benefit vs. generic)
- Lead capture: form present? friction level?
- Pricing transparency: visible / hidden / on request
- Social proof: logos, testimonials, case studies, numbers, awards
- Trust signals: team photos, physical address, phone number, certifications

### 4. Technical Health (weight: medium)

Not a full technical audit - just the signals visible from HTML.

Check:
- HTTPS: yes/no
- Redirect: www/non-www consistent
- Platform: WordPress / Webflow / Wix / Squarespace / Shopify / Custom
- Analytics: GA4 / UA / GTM / Pixel / nothing
- Render-blocking: scripts in <head> without defer/async
- Image optimization: webp format, lazy loading attributes
- Mobile: viewport meta tag present

### 5. Content Quality (weight: medium)

Check:
- Homepage copy: pain-first or feature-first?
- Does copy speak to customer outcomes or company features?
- Are there specific numbers/results or only vague claims?
- Blog/resources: present? recent? (last post date matters)
- Case studies: present? specific results?

### 6. Competitive Position (weight: medium)

Evaluated in Phase 2 separately. Summary here:
- Does the site differentiate from competitors or look identical?
- Is there a positioning statement that competitors could not copy word-for-word?
- Are there elements competitors have that this site lacks?

---

## Common Critical Findings by Business Type

### Service businesses (agencies, consultants, freelancers)
Most critical: social proof, specific outcomes, contact clarity, pricing transparency signal

### eCommerce
Most critical: product photography, trust signals, return policy visibility, checkout friction

### SaaS / Software
Most critical: clear problem statement, demo/trial CTA, pricing page, integration list

### Local business (restaurants, clinics, tradesman)
Most critical: address + phone above fold, Google Maps embed, opening hours, reviews widget

### B2B companies
Most critical: case studies with named clients and specific results, decision-maker-targeted copy, clear process/how-it-works section

---

## What NOT to flag

- Minor style preferences ("I would use a different font")
- Industry-standard UX choices that work even if unconventional
- Features the company may have intentionally omitted
- Problems that exist in all competitors equally (not a differentiator)
- Theoretical SEO improvements with no evidence of impact

If the evidence is not there, say "not assessed" - not "this is a problem."
