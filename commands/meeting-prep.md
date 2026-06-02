---
name: meeting-prep
description: Research a prospect and generate a 5-minute sales meeting brief with pain points, questions, and service fit.
---

Run the meeting-prep skill on the provided company.

Steps:
1. Load `skills/marketing-suite/meeting-prep/SKILL.md`
2. Research the company using available web tools
3. Identify pain points based on what is missing or underperforming
4. Generate the meeting brief with questions and talking points

Input formats:
- URL: `/meeting-prep https://empresa.com`
- URL + contact: `/meeting-prep https://empresa.com - contacto: Ana Lopez, CMO`
- Company name: `/meeting-prep Empresa SA`

Output: Meeting brief readable in under 5 minutes. Includes company snapshot, pain points with evidence, research-based questions, service fit analysis, and the one thing to remember.
