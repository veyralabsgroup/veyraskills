# Lean Startup Reference

Core methodology for venture-analyst. Eric Ries, 2011. Still the most cited startup framework.

## Build-Measure-Learn loop

Not a sequential process — a loop. Start from Learn and work backwards:

1. **Learn** - What do we need to know? (Define the riskiest assumption)
2. **Build** - Build the minimum thing to test that assumption
3. **Measure** - Collect data on whether assumption is true

Speed through the loop beats quality of any single cycle.

**Key insight:** Most startups fail not because they can't build, but because they build something nobody wants. The loop's purpose is to surface that failure cheaply and early.

## Validated learning

Not all learning is equal. Vanity metrics (page views, registered users) feel good and mean nothing.

**Vanity metric examples:**
- Total signups (meaningless without activation rate)
- Page views (meaningless without behavior)
- Press mentions (zero correlation with revenue)
- Lines of code shipped

**Actionable metrics (validated learning):**
- Activation rate: % of signups who complete key action
- Retention cohorts: do users come back week 2, week 4?
- Willingness to pay: who actually pays vs who says they would
- NPS with follow-up: would you be disappointed if gone?

**Test:** "If this metric doubled, would we change what we build next?" If no - it's vanity.

## Minimum Viable Product (MVP) types

### Concierge MVP
Do the service manually for 3-5 users. No automation.
- When: early problem validation, B2B, high-value customers
- Cost: time only
- What you learn: is the outcome valuable? What parts matter?
- Example: Airbnb founders photographed first listings themselves

### Wizard of Oz MVP
System looks automated but humans do the work behind the scenes.
- When: you want to simulate the product without building it
- Cost: time + some frontend work
- What you learn: do users engage with the interface? Is the outcome valuable?
- Example: Zappos CEO manually bought shoes from stores to test demand

### Landing Page / Fake Door
Page describes product, collects signups or clicks before product exists.
- When: demand signal, product not built
- Cost: hours (Carrd.co is free)
- What you learn: does the message resonate? Will people take action?
- Caution: doesn't test willingness to pay - only interest

### Piecemeal MVP
Assemble from existing tools. Don't build infrastructure.
- When: proving the workflow works before custom tech
- Cost: subscription fees for tools used
- Example: use Airtable + Zapier + Stripe before building SaaS

### Single-Feature MVP
Ship one core feature only. Cut everything else.
- When: you know the problem, testing one solution
- Risk: might ship the wrong feature
- Rule: what is the single thing that makes this valuable? Ship only that.

## Pivot types

When data says current direction is wrong, pivot — don't persevere blindly.

| Pivot type | What changes | Example |
|-----------|--------------|---------|
| Zoom-in | Narrow one feature into whole product | Instagram pivoted from Burbn |
| Zoom-out | Widen — current product becomes one feature | - |
| Customer segment | Same product, different customer | B2C → B2B |
| Customer need | Same customer, different problem | - |
| Platform | App → platform or vice versa | - |
| Business architecture | High margin/low volume ↔ low margin/high volume | - |
| Value capture | How you charge (not what you sell) | Per seat → flat rate |
| Engine of growth | Viral → sticky → paid acquisition | - |
| Channel | Direct → partner → marketplace | - |
| Technology | Same problem, completely different tech | - |

**When to pivot vs persevere:**
- Experiments consistently failing over multiple cycles = pivot signal
- One experiment failing = not enough data
- Team excited about pivot because it's easier = wrong reason, investigate

## Innovation accounting

3 milestones before declaring pivot/persevere:

1. Establish baseline (where are we now? honest numbers)
2. Tune the engine (optimize toward ideal, eliminate waste)
3. Decide pivot or persevere (did tuning move numbers? if no, pivot)

## Engines of growth

**Sticky engine:** Retention is the driver. Churn rate < growth rate.
- Metric: customer lifetime value vs churn rate
- Strategy: improve activation and retention before acquisition

**Viral engine:** Users recruit users.
- Metric: viral coefficient (K-factor). K > 1 = exponential growth
- K = (invites sent per user) × (conversion rate of invites)
- Strategy: build referral loop into core product

**Paid engine:** Buy customers profitably.
- Metric: LTV > CAC (lifetime value > customer acquisition cost)
- Rule of thumb: LTV should be 3x CAC minimum
- Strategy: find one channel that scales before optimizing others

## Signals this framework applies

Use lean startup when:
- Building a new product in uncertain market
- Validating a problem before heavy investment
- Deciding between multiple possible solutions

Don't use it to justify shipping forever-incomplete products. "Lean" = eliminate waste, not "don't finish things."
