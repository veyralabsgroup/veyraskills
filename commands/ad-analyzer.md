---
name: ad-analyzer
description: Analyze competitor ads from Meta Ad Library or pasted copy, extract creative patterns, and generate test variants.
---

Run the ad-analyzer skill on the provided brand or ad copy.

Steps:
1. Load `skills/marketing-suite/ad-analyzer/SKILL.md`
2. Collect ads via Meta Ad Library scraping or analyze provided copy
3. Extract hook types, offer patterns, emotional triggers, CTA patterns
4. Generate variants based on what is working

Input formats:
- Brand name: `/ad-analyzer Empresa SA`
- Brand + country: `/ad-analyzer Empresa SA country:US`
- Pasted copy: `/ad-analyzer [paste ad copy here]`
- Library URL: `/ad-analyzer https://www.facebook.com/ads/library/?search_terms=empresa`

Output: Pattern analysis per ad, summary of what works, and 3-5 variants to test with hypotheses.
