# Founder Trap Patterns

Common patterns where founders convince themselves they have a good idea when the evidence says otherwise. Detect these from the research data - not from what the founder says, but from what the data shows.

## How to detect traps

These are signal patterns, not opinions. Each trap has specific evidence criteria. If the criteria match, flag it. If they don't, don't flag it.

---

## Trap 1: Solution Looking for a Problem

**What it looks like:**
Founder describes a sophisticated technical solution. When asked about the problem, they describe the solution again in different words.

**Evidence signals:**
- High feature complexity in the idea description
- Low Reddit/HN pain evidence (people aren't complaining about this)
- GitHub issues about the problem: near zero
- Trend data: flat or no data
- When searching for the problem, results are mostly product announcements, not complaints

**Example:**
"An AI-powered semantic graph database for distributed knowledge management" - but nobody is searching for this, and no Reddit threads show people struggling with their current knowledge management.

**Output flag:**
```
Founder Trap: Solution looking for a problem
Signal: High technical complexity, low organic pain evidence
Evidence score on the problem: [X] -- below threshold for this complexity level
```

---

## Trap 2: Building for Yourself

**What it looks like:**
The founder is the only person in the world with this exact problem configuration. The idea solves a very specific workflow that only power users in one niche experience.

**Evidence signals:**
- The subreddits where this pain appears have under 10k subscribers
- HN discussions exist but are 5+ years old and never got traction
- GitHub issues exist in one very specific repo from one very specific maintainer
- No mainstream discussion anywhere
- Trend data: zero or declining

**Output flag:**
```
Founder Trap: Building for yourself
Signal: Pain exists but only in a very narrow segment
Estimated addressable users: [small] -- may not support a business
```

---

## Trap 3: Vitamin, Not Painkiller

**What it looks like:**
The problem exists. People acknowledge it. But nobody is urgently trying to solve it right now. It's a "nice to have."

**Evidence signals:**
- Reddit posts about the problem get upvotes but few comments
- No "is there a tool that does X" posts
- Competitors exist but have low engagement / slow growth
- People describe the problem but their current workaround is "good enough"
- No one is spending money on bad solutions currently

**Output flag:**
```
Founder Trap: Vitamin, not painkiller
Signal: Problem acknowledged, urgency low
No evidence of active spending on imperfect solutions
```

---

## Trap 4: Red Ocean Obsession

**What it looks like:**
Founder wants to compete directly with a dominant player using the same positioning and features. "We're like X but better."

**Evidence signals:**
- 1+ competitor with over 100k users
- Competitor has a free tier
- No clear positioning gap in the competitor map
- Founder's description relies on feature parity + marginal improvements
- No ERRC analysis shows a meaningfully different value curve

**Output flag:**
```
Founder Trap: Red ocean entry
Signal: Dominant player exists with free tier and no clear structural weakness
"Better" is not a strategy
```

---

## Trap 5: Market Timing Mismatch

**What it looks like:**
The idea was good 3-5 years ago (or will be good in 3-5 years) but is poorly timed for now.

**Evidence signals:**
- Trend data: declining
- Related GitHub repos: abandoned or archived
- HN discussions: lots of interest 3+ years ago, silence now
- OR: Trend rising fast but infrastructure/regulation not ready yet (too early)

**Output flag:**
```
Founder Trap: Market timing mismatch
Signal: [declining interest over X period] or [infrastructure gap for early timing]
```

---

## Trap 6: Complexity Moat Illusion

**What it looks like:**
Founder believes the product's complexity is the moat. "Nobody else will build this because it's hard." This is almost never true.

**Evidence signals:**
- The problem space has well-funded competitors (they can hire the engineers)
- The technical complexity doesn't translate to switching costs for users
- No network effects in the model
- No proprietary data advantage

**Output flag:**
```
Founder Trap: Complexity moat illusion
Signal: Technical difficulty does not equal defensibility
Better-resourced competitors can and will replicate
```

---

## Trap 7: Proxy Metric Validation

**What it looks like:**
Founder validated the wrong thing. Got 500 waitlist signups but none converted. Got 50 "great idea" replies to a cold email but nobody booked a call.

**Evidence signals (use when reviewing experiment design):**
- Success criteria were defined by vanity metrics
- No willingness-to-pay experiment was ever run
- Conversion from interest to commitment was never tested

**Output flag:**
```
Founder Trap: Proxy metric validation
Signal: Interest validated, commitment not validated
Waitlist signups are not customers
```

---

## Trap 8: ICP Drift

**What it looks like:**
Founder started with one customer type, got rejected, and gradually expanded their ICP until "everyone" is the customer.

**Evidence signals:**
- Target customer description is vague ("any business", "any developer")
- Multiple contradictory customer types mentioned in the idea description
- Pain signals come from very different subreddits with no overlap

**Output flag:**
```
Founder Trap: ICP drift
Signal: Expanding ICP is a sign of failed validation, not a bigger market
Narrow the target before expanding
```

---

## How to apply in analysis

During Phase 5 (Decision Intelligence):

1. Match evidence patterns against each trap above
2. Flag any trap where at least 3 of the listed signals are present
3. Never flag based on one signal alone
4. If a trap is flagged, it does NOT automatically change the verdict - it goes into Decision Intelligence for the judge to weigh
5. A BUILD verdict can coexist with a detected trap if the other evidence is strong enough

Priority order (most damaging first):
1. Solution looking for problem
2. Red ocean obsession
3. Vitamin not painkiller
4. Building for yourself
5. Market timing mismatch
6. All others
