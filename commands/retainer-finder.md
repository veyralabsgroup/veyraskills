---
name: retainer-finder
description: Analyze a company and identify recurring service opportunities - what depreciates without maintenance, what creates dependency, and what justifies a monthly retainer.
---

Run the retainer-finder skill on the provided company.

Steps:
1. Load `skills/marketing-suite/retainer-finder/SKILL.md`
2. Scan for actively depreciating assets (ads, SEO, email, social, CMS)
3. Map high-dependency service opportunities
4. Generate retainer brief with MRR estimate and transition path

Input formats:
- URL: `/retainer-finder https://empresa.com`
- After audit: `/retainer-finder https://empresa.com - already audited, focus on recurring`
- With agency context: `/retainer-finder https://empresa.com - ofrecemos SEO, Ads y social`

Output: Depreciation scan, dependency map, retainer stack with MRR estimate, transition path from first project to monthly retainer, and renewal risk assessment.
