# Verdict Template

Final output of venture-analyst. Complete all sections. No section is optional.
The goal is a decision, not a report.

---

## [Idea Name] - Venture Verdict

**Date:** [YYYY-MM-DD]
**Evidence Score:** [0-100]
**Evidence Quality:** [A/B/C/D/F]
**Recommendation:** BUILD / VALIDATE FIRST / AVOID

---

## Evidence Summary

### Source breakdown

| Source | Count | Quality | Strongest signal |
|--------|-------|---------|-----------------|
| HN discussions | [n] | [H/M/L] | "[quote or title]" |
| Reddit posts | [n] | [H/M/L] | "[quote or title]" |
| GitHub issues | [n] | [H/M/L] | "[repo - issue title - reactions]" |
| Market trend | [rising/stable/declining] | - | [avg interest + period] |

**Spending signals found:** [Yes - describe / No]
**Willingness-to-pay evidence:** [Yes - describe / No]

### Competitor landscape

| Name | Pricing | Users/Stars | Main weakness |
|------|---------|-------------|---------------|
| [A] | [price] | [n] | [gap] |
| [B] | [price] | [n] | [gap] |

**Market gap identified:** [Yes - describe / No]
**Dominant player (>50% share):** [Yes - name / No]

**Opportunity Score:** [0-100] - [how strong is the market?]
**Startup Score:** [0-100] - [how viable as a startup to execute?]

---

## Confidence Engine

```
Confidence: [0-100]

High confidence because:
+ [specific signal - e.g. "312 Reddit mentions across 8 subreddits"]
+ [specific signal - e.g. "84 GitHub issues with 50+ reactions"]
+ [specific signal - e.g. "14 paying competitors validated"]
+ [specific signal - e.g. "trend rising 40% over 12 months"]

Confidence reduced because:
- [specific gap - e.g. "no direct willingness-to-pay signals found"]
- [specific gap - e.g. "search volume low, problem may not be searched"]
- [specific gap - e.g. "fragmented ICP - different pain in different segments"]
```

---

## Bull Case

*Arguments for building this.*

**Strongest evidence:**
[2-3 specific data points with sources. Quotes, numbers, URLs.]

**Market timing:**
[Why now? What changed recently?]

**Competitive angle:**
[What can this do that incumbents can't or won't?]

**Best-case scenario:**
In 18 months: [specific outcome] if [specific condition] holds.

---

## Bear Case

*Steelman the opposition. Give it everything.*

**Strongest evidence against:**
[2-3 specific counterarguments with data.]

**Why existing solutions might be good enough:**
[What do incumbents have that would be hard to beat?]

**Key risks:**
- Market: [specific]
- Timing: [specific]
- Execution: [specific]

---

## Judge Verdict

### Score

| Signal | Present | Points |
|--------|---------|--------|
| Evidence score > 60 | [Y/N] | +2 / 0 |
| Evidence quality A or B | [Y/N] | +1 / 0 |
| Trend rising | [Y/N] | +1 / 0 |
| Clear competitor weakness | [Y/N] | +1 / 0 |
| No dominant player >50% | [Y/N] | +1 / 0 |
| B2B willingness-to-pay signals | [Y/N] | +1 / 0 |
| Price ceiling gap | [Y/N] | +1 / 0 |
| Evidence score < 30 | [Y/N] | 0 / -3 |
| Evidence quality D or F | [Y/N] | 0 / -2 |
| Trend declining | [Y/N] | 0 / -2 |
| Dominant player + free tier | [Y/N] | 0 / -2 |
| Niche < 10k users | [Y/N] | 0 / -1 |
| High-priority founder trap | [Y/N] | 0 / -2 |
| Reality check failed | [Y/N] | 0 / -2 |
| **Total** | | **[sum]** |

### Recommendation

**[BUILD / VALIDATE FIRST / AVOID]**
**Confidence:** [0-100]

*Reasoning (2-3 sentences. Direct. Reference specific evidence):*
[What tipped the scale. What the judge weighed most heavily.]

---

## Decision Intelligence

### Contradictions

[If none: "No significant contradictions detected."]

[If found:]
```
Contradiction: [name]

[source A] shows: [signal]
[source B] shows: [signal]

Interpretation: [explanation]
What to verify: [specific test that resolves this]
```

### Founder Traps

[If none detected: "No founder traps detected."]

[If found:]
```
Trap: [trap name]
Evidence: [which signals matched]
Risk level: [high/medium]
```

### Reality Check

[If execution path is clear: "No significant execution barriers identified."]

[If barriers found:]
```
Execution risk: [high/medium]

Requires: [list constraints]

Alternative path: [reduced scope or different entry point]
```

### Distribution Plan

**Top 3 acquisition channels for this idea:**

1. **[channel]** - [why, based on where the evidence was actually found]
   - Test: [how to test this in 2 weeks with minimal budget]

2. **[channel]** - [why]
   - Test: [how to test]

3. **[channel]** - [why]
   - Test: [how to test]

**Avoid:**
- [channel] - [specific reason for this market]

### Time-To-First-Dollar

**Estimate:** [X-Y weeks]

| Week | Action |
|------|--------|
| 1-2 | [specific action] |
| 3-4 | [specific action] |
| 5-8 | [specific action] |

**What would accelerate this:** [factor]
**What would delay this:** [risk]

---

## Next Steps

### If BUILD

**Start here (this week):**
[One specific action. Not "do customer research." Something like: "Post in r/[subreddit] describing the problem and ask how people handle it - aim for 10 DMs this week."]

**MVP type:** [Concierge / Wizard of Oz / Fake door / Single feature]
**v0.1 scope:** [What it does. What it explicitly does NOT do.]
**First 10 customers:** [Where exactly. Who exactly.]

---

### If VALIDATE FIRST

**Critical unknown:**
[The one thing that must be proven before building. One sentence.]

**Run this experiment:**
[Name from experiments.py] - [duration] - success = [metric >= threshold]

**Decision point:**
If [metric] >= [threshold] in [X weeks]: proceed to build.
If not: [specific pivot or kill condition].

---

### If AVOID

**Core problem:**
[One clear reason. Not a list.]

**What would have to change:**
[Specific signal that would make this worth revisiting. Or: "nothing changes this - the structural problem is permanent."]

**Adjacent opportunity (if found):**
[Related problem the research surfaced that IS worth pursuing.]
