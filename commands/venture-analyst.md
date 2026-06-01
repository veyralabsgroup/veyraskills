Activate the venture-analyst skill. Task: $ARGUMENTS

Read the full skill at skills/venture-suite/venture-analyst/SKILL.md before doing anything else.

Then run the 4 phases in order:

1. Problem Discovery - collect evidence from HN, Reddit, GitHub, trends using scripts/sources.py
2. Competitor Intelligence - map the landscape using scripts/scraper.py and sources
3. Validation Experiments - generate prioritized experiments using scripts/experiments.py
4. Verdict - Bull case, Bear case, Judge verdict using the scoring system in SKILL.md

Start by detecting environment enhancements silently (scripts/enhance_detect.py) and use the best available search method without asking the user for any API keys.

If the user did not specify the idea clearly, ask one question: "What's the idea, and who is it for?"

Output the full verdict using templates/verdict.md as structure.
