---
name: agency-audit
description: Audit a company website and generate a pitch-ready report with problems, quick wins, and recommended services.
---

Run the agency-audit skill on the provided URL or company.

Steps:
1. Load `skills/marketing-suite/agency-audit/SKILL.md`
2. If a URL is provided, run `scripts/web_inspector.py` to extract technical data
3. Find competitors using `scripts/competitor_finder.py`
4. Build the Problem Map and Opportunity Map using references
5. Generate the full audit report using `templates/audit-report.md`

Input formats accepted:
- URL: `/agency-audit https://empresa.com`
- URL + context: `/agency-audit https://empresa.com - somos agencia de performance, ofrecemos SEO y Ads`
- Company name: `/agency-audit Empresa SA marketing agency`

Output: Full audit report ready to customize and send. Includes critical issues, competitor comparison, quick wins, recommended services, and next steps.
