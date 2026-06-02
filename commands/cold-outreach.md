---
name: cold-outreach
description: Research a prospect and generate a personalized 4-message outreach sequence based on real signals from their website.
---

Run the cold-outreach skill on the provided prospect.

Steps:
1. Load `skills/marketing-suite/cold-outreach/SKILL.md`
2. Research the prospect website and company context
3. Identify the strongest personalization angle
4. Generate 4-message sequence: opener, follow-up 1, follow-up 2, break-up

Input formats:
- URL: `/cold-outreach https://empresa.com`
- URL + contact: `/cold-outreach https://empresa.com - Ana Lopez, directora de marketing`
- URL + LinkedIn: `/cold-outreach https://empresa.com - linkedin.com/in/analopez`

Output: 4 messages with subject lines, ready to customize. Every message based on specific research findings, not templates.
