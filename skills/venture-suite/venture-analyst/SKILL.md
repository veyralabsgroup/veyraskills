---
name: venture-analyst
description: Startup and SaaS idea validation. Researches market evidence, maps competitors, scores viability, and generates concrete validation experiments. Zero API keys required.
---

# Venture Analyst

Research a startup or SaaS idea and determine if it's worth building. No fluff - real evidence from real sources, structured reasoning, and a committed decision.

## What this does

Five phases, each producing structured output:

1. **Problem Discovery** - Find evidence the problem actually exists (Reddit, HN, GitHub issues, trends)
2. **Competitor Intelligence** - Map the landscape, find gaps, extract pricing signals
3. **Validation Experiments** - Generate 3 prioritized experiments to test demand before building
4. **Verdict** - Bull/Bear/Judge debate with Confidence Engine and scored recommendation
5. **Decision Intelligence** - Contradiction detection, founder trap check, reality check, distribution plan, time-to-first-dollar

## How to use

Describe your idea. Include:
- What it does (one sentence)
- Who it's for (target customer)
- What problem it solves

Optional: budget for experiments, market type (B2C/B2B), known competitors, founder background.

## Phase 1 - Problem Discovery

**Goal:** Find evidence the problem is real and people talk about it unprompted.

Use `scripts/sources.py` to collect evidence:

```python
from scripts.sources import search_hn, search_hn_comments, search_reddit, search_github_issues, get_trends, calculate_evidence_score

hn_stories   = search_hn(query, limit=20)
hn_comments  = search_hn_comments(query, min_points=3, limit=30)
reddit_posts = search_reddit(query, limit=25, timeframe="year")
gh_issues    = search_github_issues(query, limit=20)
trend_data   = get_trends(keyword)
```

**Evidence Quality (not just quantity):**

Evaluate source mix and signal strength, not just raw counts.

| Source | Quality signal | Weight |
|--------|---------------|--------|
| HN Ask/Show with 50+ points | People actively seeking solutions | High |
| Reddit complaints with 100+ upvotes | Widespread frustration | High |
| GitHub issues with many reactions | Developers hitting the same wall | High |
| HN/Reddit mentions of spending money | Willingness to pay | Very high |
| Rising trend | Growing problem | High |
| Trend flat | Established problem | Medium |
| Trend declining | Dying problem | Negative |
| Generic blog posts | Low signal noise | Low |

Evidence Quality grades:
- **A** - Multiple high-quality sources, direct pain quotes, spending signals
- **B** - Good source mix, clear pain but limited spending signals
- **C** - Some signal but concentrated in one source
- **D** - Thin signal, only indirect evidence
- **F** - Essentially no evidence

**Synthesize findings:**

Strongest pain signals (prioritize):
- People actively spending money on imperfect solutions
- Recurring complaints with no satisfying answer
- "Is there a tool that does X?" posts with many upvotes
- GitHub issues with many reactions, still open

Red flags:
- Zero discussion anywhere (even if search terms varied)
- Problem exists but everyone's workaround is "good enough"
- Only a few power users care, no broad market
- Discussion peaked years ago (dying category)

**Output format:**
```
## Problem Evidence

Evidence Score: [0-100]
Evidence Quality: [A/B/C/D/F]

Source breakdown:
- HN: [n] discussions, strongest: "[quote]"
- Reddit: [n] posts, strongest: "[quote]"
- GitHub: [n] issues, strongest reaction count: [n]
- Trend: [rising/stable/declining], avg interest: [n]

Quality notes:
- [what makes this evidence strong]
- [what's missing]
```

## Phase 2 - Competitor Intelligence

**Goal:** Map who's already solving this. Find pricing, positioning gaps, weak points.

```python
from scripts.scraper import scrape_competitor
from scripts.sources import search_github_repos, search_web

repos       = search_github_repos(f"{idea} tool", limit=8)
web_results = search_web(f"{idea} software alternatives", limit=8)

for url in competitor_urls:
    data = scrape_competitor(url)
    # data: title, tagline, description, pricing, features, tech_stack
```

**Competitive map:**
```
| Name | Pricing | Target | Weakness | Stars/Users |
|------|---------|--------|----------|-------------|
```

**Gaps to identify:**
- Price ceiling: tier missing between free and enterprise?
- Audience gap: power users vs beginners vs enterprise underserved?
- Feature gap: what do reviews complain about repeatedly?
- Distribution gap: channel nobody is using?

**Opportunity Score vs Startup Score:**

These are two different things. Conflating them is a common mistake.

- **Opportunity Score** = how good is the market? (demand, size, willingness to pay)
- **Startup Score** = how viable is this as a startup? (scalability, defensibility, execution path)

A market can be huge (high opportunity) but impossible to win as a bootstrapped startup (low startup score). Example: "A better Stripe" - huge opportunity, near-zero startup score for most founders.

Score both separately in the competitor output section.

## Phase 3 - Validation Experiments

**Goal:** Before writing code, find out if people will actually pay.

```python
from scripts.experiments import generate_experiments, format_experiment_output

experiments = generate_experiments(
    idea=idea,
    target_customer=target,
    market_type="b2b",      # or "b2c"
    competition_level="medium",
    budget="zero",
)
print(format_experiment_output(experiments, idea))
```

Present experiments in priority order. Cheapest + highest-signal first.

**Mom Test enforcement** - when helping design interviews or outreach:
- See `references/mom-test.md` for good vs bad questions
- Flag any future-hypothetical question ("would you use X?")
- Replace with past-behavior questions ("how do you currently handle X?")

**Time-To-First-Dollar estimate:**

For each experiment path, estimate realistic time to first revenue:

| Market type | Typical range | What accelerates it |
|------------|--------------|---------------------|
| B2C consumer SaaS | 30-90 days | Viral loop, strong landing page CTR |
| B2B SMB | 30-60 days | Warm outreach, concierge MVP |
| B2B mid-market | 60-180 days | Champion inside company, ROI clear |
| B2B enterprise | 6-18 months | Do not start here without traction |
| Developer tool (paid) | 14-45 days | Show HN, Product Hunt, X/Twitter post |
| Marketplace | 90-180+ days | Cold start problem, both sides |
| Content-led SaaS | 60-120 days | SEO takes time, need existing audience |

This is not the time to build - it's the time from starting experiments to first paying customer.

## Phase 4 - Verdict

**Goal:** Simulate a debate between Bull, Bear, and Judge. Reach a committed conclusion.

### Confidence Engine

The confidence score must explain itself. Not "Confidence: High" alone. Show the reasoning.

```
Confidence: [0-100]

High confidence because:
+ [n] Reddit mentions across [n] subreddits
+ [n] GitHub issues with [n]+ reactions
+ [n] competitors validated with real pricing
+ Rising trend over [period]
+ [specific spending signal found]

Confidence reduced because:
- [specific gap, e.g. weak monetization signals]
- [e.g. no willingness-to-pay evidence found]
- [e.g. fragmented ICP - different pain in different segments]
- [e.g. limited search volume data]
```

This matters because users need to see the reasoning is transparent, not magic.

### Bull case (write this first)
- Strongest evidence for building it
- Market timing arguments
- Why this team / why now
- Best-case scenario with numbers

### Bear case (steelman the opposition)
- Strongest evidence AGAINST building it
- Why existing solutions might be good enough
- Market risks, timing risks, competition risks
- Why it might fail even if the problem is real

### Judge verdict

Apply these criteria:

| Signal | Weight |
|--------|--------|
| Evidence score > 60 | +2 |
| Evidence quality A or B | +1 |
| Trend = rising | +1 |
| Competitors have clear weakness | +1 |
| No dominant player (>50% market) | +1 |
| B2B with willingness-to-pay signals | +1 |
| Price ceiling exists | +1 |
| Evidence score < 30 | -3 |
| Evidence quality D or F | -2 |
| Trend = declining | -2 |
| 1+ competitor with >100k users + free tier | -2 |
| Problem is niche (<10k potential users) | -1 |
| Founder trap detected (high priority) | -2 |
| Reality check failed | -2 |

**Verdict:**
```
Recommendation: BUILD / VALIDATE FIRST / AVOID
Confidence: [0-100]
Score: [+N or -N]

Judge's reasoning:
[2-3 sentences. Direct. No hedging. Reference the specific evidence that tipped the scale.]
```

## Phase 5 - Decision Intelligence

Run this after the Verdict. It does not change the verdict score - it adds context that makes the decision actionable.

### Contradiction Detector

Look for contradictions between sources. The most valuable insight is often in the gap between what people say and what the market shows.

Common contradiction patterns:

**Pain high, market growing:**
```
Reddit: strong complaints about current solutions
Competitors: growing, raising funding

Interpretation: users hate existing tools but still pay.
This is an improvement opportunity, not a replacement play.
Consider: better UX, better pricing, better ICP focus.
```

**Pain high, no competitors:**
```
Evidence of real pain.
Zero viable competitors found.

Two interpretations:
1. Blue ocean - opportunity exists
2. Graveyard - others tried and died

Check: search for failed startups in this space. If multiple failed,
investigate why before treating this as opportunity.
```

**Trend rising, community silent:**
```
Google Trends shows growing interest.
Reddit/HN have minimal discussion.

Possible: problem is new, community hasn't formed yet (early).
Risk: trend is noise, not genuine demand.
```

**Competition dense, pain still high:**
```
Multiple established competitors.
Pain signals still strong and recent.

Interpretation: nobody has actually solved it.
Look for the structural reason: price, UX, missing feature, wrong ICP.
```

When a contradiction is found, output:
```
Contradiction detected: [name]

[source A] shows: [signal]
[source B] shows: [signal]

Most likely interpretation: [explanation]
What to verify: [specific experiment or question that resolves this]
```

### Founder Trap Detector

Check `references/founder-traps.md` for full criteria.

Evaluate the evidence against each trap pattern. Flag any trap where 3+ signals match.

Output when trap found:
```
Founder Trap: [trap name]
Evidence: [which signals matched]
Risk level: [high/medium]
Does not invalidate the opportunity, but changes the execution approach.
```

### Reality Check

This is not about the market - it's about whether this founder can execute this idea.

Gather context:
- What is the founder's background? (from idea description if mentioned)
- What does the idea require to work? (regulatory, infrastructure, capital, technical depth)

Questions to answer:
1. Does this require compliance, licensing, or regulatory approval?
2. Does this require partnerships before it can function? (e.g. bank partners, data licenses)
3. Does this require enterprise sales from day one?
4. Does this require a team of 10+ to build the MVP?
5. Is the technical complexity beyond a solo founder?

If 2+ of these are true:
```
Reality check: Execution path is high-risk for early-stage founders

Requires: [list what it requires]

This does not mean the opportunity is bad.
It means: do not start building until these constraints are addressed.

Alternative paths:
- [reduced scope version that avoids the constraint]
- [validate the demand first, then find the right co-founder/partner]
```

### Distribution Plan

Based on the research, recommend 3 specific acquisition channels.

Use `references/traction.md` for channel criteria. Apply to this specific market:

```
Top channels for this idea:

1. [channel] - because [specific evidence from research]
   Test: [how to run a cheap test in 2 weeks]
   
2. [channel] - because [specific evidence]
   Test: [how to test]
   
3. [channel] - because [specific evidence]
   Test: [how to test]

Avoid:
- SEO - [reason, e.g. "competitive market, 6+ months to rank"]
- Paid social - [reason, e.g. "B2B ICP hard to target on Meta"]
```

Do not recommend generic channels. Base it on where the pain evidence was actually found.

Example: if most Reddit signal came from r/smallbusiness, recommend Reddit community strategy specifically.

### Time-To-First-Dollar

Based on the market type, competition, and experiment plan:

```
Time-To-First-Dollar estimate: [X-Y weeks/months]

Path:
Week 1-2: [specific action, e.g. "cold outreach to 50 Reddit users who posted about problem"]
Week 3-4: [specific action]
Week 5-8: [specific action]
Target: first paying customer by [date estimate]

What would accelerate this: [specific factor]
What would delay this: [specific risk]
```

## Enhancement detection

Run at session start to unlock better sources:

```python
from scripts.enhance_detect import detect_level, ensure_searxng, best_search

env = detect_level()
# Returns: docker, searxng, veyrascrape_mcp, github_token, exa_key, tavily_key, groq_key

if env["docker"] and not env["searxng"]:
    ensure_searxng()  # silent, no user prompt

results = best_search(query, env, limit=10)
```

**Level 1 (always works):** HN + Reddit + GitHub + ddgs + trendspyg
**Level 2 (auto, no keys):** + SearXNG via Docker (if Docker installed)
**Level 3 (optional keys):** + Exa, Tavily, GitHub authenticated, VeyraScrape MCP

Never ask the user to set up API keys. Auto-detect and use what's available.

## Evidence Score interpretation

From `calculate_evidence_score()` in `sources.py`:

| Score | Meaning |
|-------|---------|
| 0-20  | Weak - barely any signal. Rethink or pivot problem framing |
| 21-40 | Thin - some signal but not convincing |
| 41-60 | Moderate - proceed to competitor research |
| 61-80 | Strong - real problem, real people care |
| 81-100 | Very strong - validated pain, move to experiments immediately |

## Methodology references

- `references/lean-startup.md` - validated learning, MVP types, pivot signals
- `references/customer-dev.md` - Steve Blank's 4 steps, problem interview structure
- `references/mom-test.md` - good vs bad interview questions
- `references/blue-ocean.md` - Value Curve, ERRC Grid, finding uncontested space
- `references/traction.md` - 19 acquisition channels, Bullseye framework
- `references/founder-traps.md` - 8 trap patterns with evidence criteria

## Output principles

1. Lead with evidence, not opinions
2. Quote real sources (HN post, Reddit thread, GitHub issue) with specifics
3. Separate fact from inference - never present interpretation as data
4. Show the Confidence Engine reasoning - never just state "High confidence"
5. Run the contradiction check - the most valuable insight is often in the gaps
6. Check for founder traps before finalizing verdict
7. Verdict must commit - no "it depends" without specifics and a path forward
8. Distinguish Opportunity Score from Startup Score
