"""
Validation experiment generator.
Based on Lean Startup + Mom Test methodology.
Outputs concrete, actionable experiments — not analysis.
"""

EXPERIMENTS = {
    "cold_outreach": {
        "name": "Cold Outreach Test",
        "type": "discovery",
        "cost": "0€",
        "duration": "5-7 days",
        "effort": "medium",
        "goal": "Validate problem exists and find early adopters",
        "process": [
            "Identify 50 potential customers on LinkedIn, Reddit, or niche communities",
            "Send short message: 'I'm researching [problem area] — would you spare 15 min?'",
            "Do NOT pitch. Ask about their current process and pain.",
            "Apply Mom Test: ask about past behavior, not future intentions",
        ],
        "metric": "Response rate + calls booked",
        "success_criteria": "≥10% response rate, ≥3 discovery calls completed",
        "red_flags": [
            "Everyone says 'great idea' but nobody wants a call",
            "People say they'd pay but won't commit to a free beta",
            "You have to explain the problem before they understand it",
        ],
        "mom_test_questions": [
            "Tell me how you currently handle [problem]. Walk me through your last time.",
            "What's the most frustrating part of that process?",
            "Have you tried other solutions? What happened?",
            "How much time/money does this cost you per month right now?",
            "What would you do if this problem disappeared tomorrow?",
        ],
        "bad_questions_to_avoid": [
            "Would you use a tool that does X?",
            "Do you think this is a good idea?",
            "Would you pay $X for this?",
            "How much would you pay for this?",
        ],
    },

    "fake_door": {
        "name": "Fake Door Test",
        "type": "demand_signal",
        "cost": "0-30€",
        "duration": "7-14 days",
        "effort": "low",
        "goal": "Measure real demand before building anything",
        "process": [
            "Build a landing page (Carrd.co free, 30 min)",
            "Describe the value proposition clearly — no features, only outcome",
            "Add a CTA button: 'Join Waitlist' or 'Get Early Access'",
            "When clicked: show 'Thanks, we'll notify you' — collect email",
            "Drive traffic: 2-3 Reddit posts in relevant communities + LinkedIn",
            "Track: page visits, CTA clicks, emails collected",
        ],
        "metric": "CTA click-through rate (CTR)",
        "success_criteria": "≥5% CTR from cold traffic, ≥50 emails in 14 days",
        "tools": [
            "Carrd.co — free landing pages",
            "Tally.so — free forms with email collection",
            "Google Analytics (free) — traffic tracking",
            "Plausible.io — privacy-friendly alternative",
        ],
        "headline_formula": "[Outcome they want] without [current pain]",
        "subheadline_formula": "[Product name] helps [target customer] [achieve outcome] by [key mechanism]",
        "red_flags": [
            "CTR below 2% consistently",
            "High visits but nobody clicks CTA",
            "Traffic only from your own network — zero cold traffic",
        ],
    },

    "waitlist": {
        "name": "Waitlist Campaign",
        "type": "demand_signal",
        "cost": "0€",
        "duration": "14-30 days",
        "effort": "medium",
        "goal": "Build an audience before building the product",
        "process": [
            "Build landing with value proposition + email signup",
            "Write 3-5 posts for relevant communities (Reddit, LinkedIn, Twitter)",
            "Frame as 'I'm building X because Y — who's interested?'",
            "Respond to every comment — this is customer research",
            "Track: emails per day, most common questions, what resonates",
        ],
        "metric": "Email signups per week",
        "success_criteria": "100 organic signups in 30 days without paid ads",
        "tools": [
            "Beehiiv (free for <2500 subs) — email list",
            "Carrd.co — landing",
            "Reddit (organic, zero cost)",
            "LinkedIn (organic, zero cost)",
        ],
        "red_flags": [
            "Only your friends/connections sign up",
            "High unsubscribe rate on first email",
            "Nobody shares it organically",
        ],
    },

    "concierge_mvp": {
        "name": "Concierge MVP",
        "type": "value_validation",
        "cost": "0€",
        "duration": "2-4 weeks",
        "effort": "high",
        "goal": "Deliver the core value manually to 3-5 real users",
        "process": [
            "Find 3-5 people with the problem (from outreach or waitlist)",
            "Offer to do the service manually for free",
            "Do it by hand: spreadsheets, email, calls, manual research",
            "Observe where they get value, where they get frustrated",
            "At the end: 'Would you pay X/month for this if it was automated?'",
        ],
        "metric": "Willingness to pay (real commitment, not hypothetical)",
        "success_criteria": "≥3/5 users say yes to paying target price, 1+ pre-orders",
        "key_question": "If this service disappeared tomorrow, what would you do?",
        "what_to_track": [
            "Which parts of the manual process they value most",
            "Which parts they don't care about",
            "How often they'd use it",
            "What would make them stop using it",
            "Who else they'd recommend it to",
        ],
        "red_flags": [
            "'I'd use it but can't commit right now'",
            "They use it but never refer anyone",
            "The manual process takes so long it's not viable to automate",
        ],
    },

    "smoke_test_ads": {
        "name": "Paid Smoke Test",
        "type": "demand_signal",
        "cost": "30-100€",
        "duration": "7 days",
        "effort": "medium",
        "goal": "Measure demand with cold paid traffic — no bias from network",
        "process": [
            "Set up landing page with single CTA",
            "Run €30-50 in Meta or Google Ads to target audience",
            "B2C: Facebook/Instagram interest targeting",
            "B2B: LinkedIn job title targeting (more expensive, ~€5-10/click)",
            "Measure CPL (cost per lead) — this is your true demand signal",
        ],
        "metric": "Cost Per Lead (CPL)",
        "success_criteria": "B2C CPL < 5€, B2B CPL < 40€",
        "tools": [
            "Meta Ads Manager (€30 minimum budget)",
            "Google Ads (€10/day minimum)",
            "LinkedIn Ads (most expensive — B2B only, €15-50/click)",
        ],
        "red_flags": [
            "CPL 5x higher than benchmark — market doesn't respond to messaging",
            "Clicks but no conversions — landing page or offer problem",
            "Can't target audience precisely — unclear ICP",
        ],
    },
}


def generate_experiments(
    idea: str,
    target_customer: str,
    market_type: str = "b2c",
    competition_level: str = "medium",
    budget: str = "zero",
) -> list[dict]:
    """
    Generate 3 prioritized validation experiments.
    Always starts with the cheapest, highest-signal experiments first.
    """
    selected = []

    # Always: Cold outreach first (zero cost, real signal)
    exp = EXPERIMENTS["cold_outreach"].copy()
    exp["priority"] = 1
    exp["customized_for"] = idea
    exp["target"] = target_customer
    selected.append(exp)

    # Always: Fake door (low cost, measurable)
    exp = EXPERIMENTS["fake_door"].copy()
    exp["priority"] = 2
    exp["customized_for"] = idea
    selected.append(exp)

    # B2B with budget: concierge MVP
    # B2C with budget: waitlist
    if market_type.lower() == "b2b" or competition_level == "high":
        exp = EXPERIMENTS["concierge_mvp"].copy()
        exp["priority"] = 3
        exp["customized_for"] = idea
        exp["target"] = target_customer
        selected.append(exp)
    else:
        exp = EXPERIMENTS["waitlist"].copy()
        exp["priority"] = 3
        exp["customized_for"] = idea
        selected.append(exp)

    return selected


def format_experiment_output(experiments: list[dict], idea: str) -> str:
    """Format experiments as markdown output."""
    lines = [f"# Validation Experiments — {idea}\n"]
    lines.append("Start with Experiment 1. Only move to the next if the previous fails.\n")

    for exp in experiments:
        lines.append(f"## Experiment {exp['priority']}: {exp['name']}")
        lines.append(f"**Cost:** {exp['cost']} | **Duration:** {exp['duration']} | **Effort:** {exp['effort']}")
        lines.append(f"\n**Goal:** {exp['goal']}\n")
        lines.append("**Process:**")
        for step in exp.get("process", []):
            lines.append(f"- {step}")
        lines.append(f"\n**Metric:** {exp['metric']}")
        lines.append(f"**Success:** {exp['success_criteria']}")
        if exp.get("red_flags"):
            lines.append("\n**Red flags to watch:**")
            for flag in exp["red_flags"]:
                lines.append(f"- {flag}")
        lines.append("")

    return "\n".join(lines)
