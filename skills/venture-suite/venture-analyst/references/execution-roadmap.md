# Execution Roadmap Framework

The analysis means nothing if the founder doesn't know what to do on Monday morning.

This framework converts a venture-analyst verdict into a concrete 30-day action plan. The output is not generic advice - it is specific actions based on the evidence collected in Phases 1-5.

---

## The core principle

Most validators end with BUILD or AVOID. That is not enough.

The right output is:
- What to do this week (not "validate the idea" - specific tasks)
- What NOT to build yet (and why)
- When to stop and reassess (specific trigger conditions)

The roadmap changes based on the verdict:
- **BUILD** → 30-day sprint to first paying customer
- **VALIDATE FIRST** → 30-day experiment plan
- **AVOID** → pivot path or stop criteria

---

## BUILD path - 30-day roadmap

The goal is one paying customer in 30 days. Not an MVP. Not a waitlist. One customer who pays.

### Week 1 - Find the customer before building

Actions:
1. Identify 50 people who have the problem (from the research: which subreddits, which GitHub repos, which communities had the most signal?)
2. Reach out to 20 with a Mom Test message - not a pitch, a question about their current workflow
3. Book 5 discovery calls
4. Run all 5 calls using Mom Test structure from `references/mom-test.md`
5. By end of week: can you describe the customer's pain in their exact words?

Do NOT build anything this week.

Decision gate: if you cannot find 5 people willing to talk, the ICP is wrong. Stop and reassess before continuing.

### Week 2 - Build only what closes the first sale

Based on the 5 conversations:
1. Identify the one outcome the customer cares most about
2. Can you deliver that outcome manually? (Concierge MVP)
3. If yes: offer to do it for free or at a steep discount for 2-3 people
4. If the outcome requires software: build only the path from input to that outcome. Nothing else.

Scope rule: if it takes more than 5 days to build, you are building too much.

Decision gate: if you cannot articulate what the customer is paying for in one sentence, do not build yet.

### Week 3 - Deliver and charge

1. Deliver the concierge MVP or minimal software to the 2-3 people from Week 2
2. At delivery: ask "would you pay [price] per month for this if it continued?"
3. If yes: send them a payment link (Stripe, Gumroad, bank transfer - whatever works)
4. If no: ask what would have to be different for them to pay

First payment is the signal. Not a letter of intent. Not "I would pay". An actual transaction.

Decision gate: if nobody pays after Week 3, you have a problem with price, value, or ICP. Identify which one before continuing.

### Week 4 - Stabilize and find customer 2-3

1. Deliver reliably to paying customer 1
2. Ask for referral: "who else do you know with this problem?"
3. Run outreach to 10 more people from the original 50 list
4. Goal: 2-3 paying customers by end of month

---

## VALIDATE FIRST path - 30-day experiment plan

The goal is to answer the one critical unknown identified in Phase 5.

### Week 1 - Define the question precisely

Write this sentence: "We do not know if [specific assumption]. If we knew [assumption] is true, we would build. If false, we would not build."

Examples:
- "We do not know if freelancers will pay for automated invoicing when free tools exist."
- "We do not know if HR teams have budget for this outside their annual planning cycle."

Everything in the next 3 weeks answers this one question.

### Week 2 - Run the cheapest test that could falsify it

Based on the assumption type:

| Assumption type | Best test | Cost | Time |
|----------------|-----------|------|------|
| Does the problem exist? | 10 Mom Test interviews | 0 | 1 week |
| Will they pay? | Concierge MVP with payment ask | 0 | 2 weeks |
| Does the message resonate? | Fake door landing page | 0-30€ | 1 week |
| Is the ICP right? | Cold outreach to 3 different segments | 0 | 1 week |

Do not run more than one test at a time. You need clean signal.

### Week 3 - Collect and evaluate data

By end of week 3 you need a number against a threshold:
- Interviews: at least 7 out of 10 describe the same problem unprompted
- Payment ask: at least 2 out of 5 say yes and follow through
- Fake door: CTR above 5% from cold traffic
- ICP test: one segment responds 3x better than others

### Week 4 - Decision

Three possible outcomes:

**Assumption confirmed:** move to BUILD path. Start Week 1 of the BUILD roadmap.

**Assumption partially confirmed:** the test worked but raised a new question. Run a second 2-week experiment targeting the new unknown.

**Assumption falsified:** the critical assumption is wrong. Before stopping:
- Is there a pivot? (different customer, different problem, different solution)
- If yes: restart from Phase 1 with the new hypothesis
- If no: stop. Time is the most valuable resource.

---

## AVOID path - what to do instead

If the verdict is AVOID, the roadmap is not "do nothing." It is:

### Option A - Pivot investigation (2 weeks)

The research surfaced something. What was the most interesting unexpected signal?
- A different customer segment with stronger pain
- A related problem that nobody is solving
- A gap in the competitor landscape that the original idea missed

Spend 2 weeks doing Phase 1 research on the pivot hypothesis before committing.

### Option B - Clean stop criteria

If no pivot is visible, document:
- What was learned (specific, honest)
- What would have to change in the market for this to be worth revisiting
- Time horizon: reassess in [6/12/24] months if [specific trigger] occurs

This is not failure. It is validated learning. The next idea starts from a better place.

---

## Roadmap anti-patterns

**Anti-pattern 1: Building before selling**
The roadmap assumes zero code until someone has committed to paying. Build only what closes the next sale.

**Anti-pattern 2: Optimizing before validating**
Do not improve the landing page conversion rate before you have 100 cold visitors. Do not A/B test before you have a working baseline.

**Anti-pattern 3: Scaling before repeating**
Do not invest in marketing before you have 3 customers who came through the same process. One customer is an anecdote. Three is a pattern.

**Anti-pattern 4: Measuring vanity metrics**
The only metric that matters in week 1-4 is: did someone pay? Every other metric is a proxy.

**Anti-pattern 5: Moving the goalposts**
Define success criteria before starting each week. Do not redefine "success" after seeing results.

---

## Output format for roadmap

```
## 30-Day Execution Roadmap

Path: [BUILD / VALIDATE FIRST / AVOID]

Critical constraint: [the one thing that must be true for this plan to work]

Week 1: [specific tasks + decision gate]
Week 2: [specific tasks + decision gate]
Week 3: [specific tasks + decision gate]
Week 4: [goal + decision]

Do NOT build yet:
- [specific feature or system to avoid]
- [reason]

Reassess if:
- [specific trigger that means the plan is failing]
```
