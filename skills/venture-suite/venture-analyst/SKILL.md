---
name: venture-analyst
description: Startup and SaaS idea validation. Researches market evidence, maps competitors, scores viability, and generates concrete validation experiments. Zero API keys required.
---

# Venture Analyst

Research a startup or SaaS idea and determine if it's worth building. No fluff — real evidence from real sources.

## What this does

Four phases, each producing structured output:

1. **Problem Discovery** - Find evidence the problem actually exists (Reddit, HN, GitHub issues)
2. **Competitor Intelligence** - Map the landscape, find gaps, extract pricing signals
3. **Validation Experiments** - Generate 3 prioritized experiments to test demand before building
4. **Verdict** - Bull/Bear/Judge debate producing a final recommendation with confidence score

## How to use

Describe your idea. Include:
- What it does (one sentence)
- Who it's for (target customer)
- What problem it solves

Optional: budget for experiments, market type (B2C/B2B), known competitors.

## Phase 1 — Problem Discovery

**Goal:** Find evidence the problem is real and people talk about it unprompted.

Use `scripts/sources.py` to collect evidence:

```python
from scripts.sources import search_hn, search_hn_comments, search_reddit, search_github_issues, get_trends

# HN: find discussions, Show HN, Ask HN about the problem space
hn_stories = search_hn(query, limit=20)
hn_comments = search_hn_comments(query, min_points=3, limit=30)

# Reddit: find complaints, questions, "is there a tool for X" posts
reddit_posts = search_reddit(query, limit=25, timeframe="year")

# GitHub: find feature requests and pain in related tools
gh_issues = search_github_issues(query, limit=20)

# Trends: is interest rising or declining?
trend_data = get_trends(keyword)
```

**Synthesize findings:**

Look for these signals (strongest first):
- People spending money on bad solutions (evidence of willingness to pay)
- Recurring complaints with no good answer
- "Is there a tool that does X?" posts with many upvotes
- GitHub issues with many reactions and no resolution
- Rising trend line

Red flags:
- Zero discussion anywhere — not even a complaint
- Problem exists but nobody's tried to solve it (often means it's not painful enough)
- Only a few power users care, not a broad market

**Output format:**
```
## Problem Evidence

**Evidence Score:** [0-100] (use calculate_evidence_score())
**Trend:** [rising/stable/declining/no_data]

### What people say (direct quotes preferred)
- [Source] "[quote or paraphrase]" — [upvotes/reactions]

### Pain signals
- [description of signal + source count]

### Gaps found
- [what existing solutions miss]
```

## Phase 2 — Competitor Intelligence

**Goal:** Map who's already solving this. Find pricing, positioning gaps, weak points.

```python
from scripts.scraper import scrape_competitor
from scripts.sources import search_github_repos, search_web

# Find competitors via web and GitHub
repos = search_github_repos(f"{idea} tool", limit=8)
web_results = search_web(f"{idea} software alternatives", limit=8)

# Scrape each competitor's pricing + positioning
for url in competitor_urls:
    data = scrape_competitor(url)
    # data has: title, tagline, description, pricing, features, tech_stack
```

**Competitive map structure:**
```
| Name | Pricing | Target | Weakness | Stars |
|------|---------|--------|----------|-------|
| X    | $49/mo  | SMBs   | No API   | 2.1k  |
```

**Gaps to look for:**
- Price ceiling: is there a tier missing?
- Audience gap: power users vs beginners vs enterprise
- Feature gap: what do G2/Reddit reviews complain about?
- Distribution gap: who's not in a specific channel?

**G2 reviews (when Playwright available):**
```python
from scripts.scraper import scrape_g2_reviews
reviews = scrape_g2_reviews("https://www.g2.com/products/[product]/reviews")
# Check for recurring "cons" patterns
```

**Output format:**
```
## Competitor Map

### Direct competitors
[table]

### Indirect / adjacent
[list with one-line descriptions]

### Market gaps
- Gap 1: [description + evidence]
- Gap 2: [description + evidence]

### Pricing landscape
- Range: [$X - $Y/month]
- Free tier pattern: [present/absent]
- Typical model: [seat/flat/usage]
```

## Phase 3 — Validation Experiments

**Goal:** Before writing code, find out if people will actually pay.

```python
from scripts.experiments import generate_experiments, format_experiment_output

experiments = generate_experiments(
    idea=idea,
    target_customer=target,
    market_type="b2b",  # or "b2c"
    competition_level="medium",  # low/medium/high
    budget="zero",  # zero / low / medium
)

print(format_experiment_output(experiments, idea))
```

Always present experiments in priority order. Cheapest + highest-signal first.

**Mom Test enforcement** — when helping design interviews or outreach:
- See `references/mom-test.md` for good vs bad questions
- Detect and flag future-hypothetical questions ("would you use X?")
- Replace with past-behavior questions ("how do you currently handle X?")

## Phase 4 — Verdict

**Goal:** Simulate a debate between Bull, Bear, and Judge. Reach a conclusion.

### Bull case (write this first)
- Strongest evidence for building it
- Market timing arguments
- Why this team / why now
- Best-case scenario with numbers

### Bear case (steelman the opposition)
- Strongest evidence AGAINST
- Why existing solutions might be good enough
- Market risks, timing risks, competition risks
- Why it might fail even if the problem is real

### Judge verdict
Read both cases. Apply these criteria:

| Signal | Weight |
|--------|--------|
| Evidence score > 60 | +2 |
| Trend = rising | +1 |
| Competitors have clear weakness | +1 |
| No dominant player (>50% market) | +1 |
| B2B with willingness-to-pay signals | +1 |
| Price ceiling exists | +1 |
| Evidence score < 30 | -3 |
| Trend = declining | -2 |
| 1+ competitor with >100k users + free tier | -2 |
| Problem is niche (<10k potential users) | -1 |

**Verdict output:**
```
## Verdict

**Recommendation:** [BUILD / VALIDATE FIRST / AVOID]
**Confidence:** [High / Medium / Low]
**Score:** [+N or -N]

### Judge's reasoning
[2-3 sentences. Direct. No hedging.]

### If BUILD: suggested starting point
[Specific first step. Not generic advice.]

### If VALIDATE FIRST: critical unknown
[The one thing that must be proven before spending time.]

### If AVOID: core problem
[Why specifically this fails. What would have to change.]
```

## Enhancement detection

Run at session start to unlock better sources:

```python
from scripts.enhance_detect import detect_level, ensure_searxng, best_search

env = detect_level()
# Returns: docker, searxng, veyrascrape_mcp, github_token, exa_key, tavily_key, groq_key

# If Docker available, auto-launch SearXNG for better web search
if env["docker"] and not env["searxng"]:
    ensure_searxng()  # silent, no user prompt

# Use best available search
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

## Output principles

1. Lead with evidence, not opinions
2. Quote real sources (HN post, Reddit thread, GitHub issue)
3. Be specific about numbers (upvotes, stars, $prices)
4. Separate fact from inference clearly
5. Bull/Bear before Verdict — don't skip the debate
6. Verdict must commit to a recommendation — no "it depends" without specifics
