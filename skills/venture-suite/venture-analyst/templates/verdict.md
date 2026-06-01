# Verdict Template

The final output of venture-analyst. Complete all sections. No section is optional.

---

## [Idea Name] — Venture Verdict

**Date:** [YYYY-MM-DD]
**Evidence Score:** [0-100] (from calculate_evidence_score())
**Recommendation:** BUILD / VALIDATE FIRST / AVOID

---

## Evidence Summary

### Problem signals found

| Source | Count | Strongest signal |
|--------|-------|-----------------|
| HN discussions | [n] | "[quote]" |
| Reddit mentions | [n] | "[quote]" |
| GitHub issues | [n] | "[repo/issue]" |
| Market trend | [rising/stable/declining] | [data point] |

**Evidence quality:** [Strong / Moderate / Thin / Weak]

### Competitor landscape

| Name | Pricing | Users/Stars | Main weakness |
|------|---------|-------------|---------------|
| [A] | [price] | [n] | [gap] |
| [B] | [price] | [n] | [gap] |

**Market gap identified:** [Yes/No — describe if yes]
**Dominant player:** [Yes/No — name if yes]

---

## Bull Case

*Arguments for building this.*

**Strongest evidence:**
[2-3 specific data points — quotes, numbers, sources. Not opinions.]

**Market timing:**
[Why now? What changed recently that makes this viable?]

**Competitive angle:**
[What can this do that incumbents can't or won't?]

**Best-case scenario:**
In 18 months, [specific outcome] if [specific condition] holds. Revenue path: [rough numbers].

---

## Bear Case

*Steel man the opposition. Give it everything.*

**Strongest evidence against:**
[2-3 specific counterarguments — facts, not opinions.]

**Why existing solutions might be good enough:**
[What do incumbents have that would be hard to beat?]

**Risk factors:**
- Market risk: [specific]
- Timing risk: [specific]
- Execution risk: [specific]

**Worst-case scenario:**
[What happens if the problem isn't as painful as signals suggest? Or if incumbents copy the positioning?]

---

## Judge Verdict

*Read both cases above before scoring.*

### Score

| Signal | Present? | Points |
|--------|----------|--------|
| Evidence score > 60 | [Y/N] | +2 / 0 |
| Trend = rising | [Y/N] | +1 / 0 |
| Competitor has clear weakness | [Y/N] | +1 / 0 |
| No dominant player >50% share | [Y/N] | +1 / 0 |
| B2B with willingness-to-pay signals | [Y/N] | +1 / 0 |
| Price ceiling gap exists | [Y/N] | +1 / 0 |
| Evidence score < 30 | [Y/N] | 0 / -3 |
| Trend = declining | [Y/N] | 0 / -2 |
| Competitor with >100k users + free tier | [Y/N] | 0 / -2 |
| Niche < 10k potential users | [Y/N] | 0 / -1 |
| **Total** | | **[sum]** |

### Recommendation

**[BUILD / VALIDATE FIRST / AVOID]**

**Confidence:** High / Medium / Low

*Reasoning (2-3 sentences max. Direct. No hedging):*
[Judge's reasoning here. Reference specific evidence from both cases. State what tipped the scale.]

---

## Next Steps

### If BUILD

**Start here:**
[One specific, concrete first action. Not "do customer research." "Post in r/[subreddit] asking about [specific problem] — aim for 10 direct messages this week."]

**Recommended MVP type:** [Concierge / Wizard of Oz / Fake door / Single feature]
**First version scope:** [What does v0.1 do? What does it explicitly NOT do?]
**Target for first 10 customers:** [Where specifically. Who exactly.]

---

### If VALIDATE FIRST

**Critical unknown:**
[The one thing that must be true for this to work, that is not yet proven.]

**Experiment to run:**
[Specific experiment from experiments.py — name, duration, success metric]

**Decision point:**
Run [experiment] for [X weeks]. If [metric] >= [threshold], proceed to build. If not, [pivot or kill].

---

### If AVOID

**Core problem:**
[Why specifically this fails. One clear reason, not a list.]

**What would have to change:**
[What signal would need to appear for this to be worth revisiting? If nothing could change it, say so.]

**Adjacent opportunity (if any):**
[Sometimes the research reveals a related problem that IS worth pursuing. If found, name it.]

---

## Appendix — Raw Data

### Top HN threads
[list with URLs and point counts]

### Top Reddit posts
[list with URLs and upvote counts]

### Competitor data
[scraped pricing, feature lists, tech stack if available]

### Trend data
[keyword, avg interest, trend direction, related queries]
