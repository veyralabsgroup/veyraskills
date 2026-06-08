# VeyraSkills

![skills](https://img.shields.io/badge/skills-13-blue) ![npm](https://img.shields.io/npm/v/@veyralabs/skills) ![license](https://img.shields.io/badge/license-MIT-green)

Skills for Claude Code and other AI coding agents. Each skill is a plain text file that teaches your agent a specialized workflow — naming, branding, website cloning, Shopify development, marketing intelligence, idea validation, and more.

```bash
npx @veyralabs/skills install naming-suite
npx @veyralabs/skills install webcloner
npx @veyralabs/skills install shopify-suite
npx @veyralabs/skills install venture-suite
npx @veyralabs/skills install marketing-suite
```

Or install everything at once:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/veyralabsgroup/veyraskills/main/install.sh)
```

---

## Available Skills

### naming-suite

Four skills for naming products, auditing brands, mapping competitors, and building naming systems.

| Skill | What it does |
|-------|-------------|
| [domainforge](./skills/naming-suite/domainforge/SKILL.md) | Generate startup name candidates. Scores each on 8 factors: memorability, distinctiveness, domain availability, trademark risk, pronunciation, spelling, brandability, market fit |
| [brandaudit](./skills/naming-suite/brandaudit/SKILL.md) | Audit an existing brand name. Returns severity scores across 8 dimensions and a rebrand verdict |
| [competitornames](./skills/naming-suite/competitornames/SKILL.md) | Map how competitors in a market are named. Identifies saturation, naming clusters, and open whitespace |
| [namingguide](./skills/naming-suite/namingguide/SKILL.md) | Build a naming system for a company or product line. Covers principles, naming patterns, approval criteria, and anti-patterns |

Works best in sequence: run `competitornames` to understand the landscape, then `domainforge` to generate names that stand out from it.

### shopify-suite

Two skills covering the full Shopify stack — one for developers building themes and apps, one for merchants auditing and optimizing stores.

| Skill | What it does |
|-------|-------------|
| [shopify-dev](./skills/shopify-suite/shopify-dev/SKILL.md) | Shopify development across all layers: Liquid themes, JSON templates, app development with Remix, Storefront and Admin API, CLI workflows, checkout extensions, Hydrogen. Fetches live Shopify documentation via Context7 before answering version-sensitive questions |
| [shopify-store](./skills/shopify-suite/shopify-store/SKILL.md) | Store audit and optimization. Works in two modes: Mode A uses shopify-mcp to read real store data (products, orders, apps, metafields); Mode B uses public extraction when MCP is not available. Audits 6 dimensions: catalog health, collection architecture, navigation, SEO, app stack, conversion signals |

### venture-suite

Research a startup or SaaS idea before building. Collects evidence from HN, Reddit, GitHub, and web searches — no API keys required.

| Skill | What it does |
|-------|-------------|
| [venture-analyst](./skills/venture-suite/venture-analyst/SKILL.md) | Four-phase idea validation: problem discovery (evidence from real sources), competitor intelligence (pricing, gaps, weaknesses), validation experiments (Mom Test, fake door, concierge MVP), and a Bull/Bear/Judge verdict with confidence score |

Includes Python scripts for zero-key data collection and auto-detection of available enhancements (SearXNG via Docker, optional API keys). All methodology references included: Lean Startup, Customer Development, Mom Test, Blue Ocean Strategy, Traction.

### webcloner

Clone any landing page, marketing site, portfolio, or ecommerce storefront into a pixel-accurate Next.js replica.

| Skill | What it does |
|-------|-------------|
| [webcloner](./skills/webcloner/SKILL.md) | Seven-phase visual cloning: recon + computed styles extraction, foundation setup, parallel 5-agent spec (layout/typography/color/spacing/component), parallel component build, assembly, pixel-accurate QA, automated visual feedback loop |

Includes five scripts: `extract.py` (Scrapling DOM/CSS/asset extractor), `extract-styles.mjs` (exact computed styles via Playwright injection), `download-assets.mjs` (asset downloader with WebP conversion), `compare.mjs` (pixelmatch pixel diff with PASS/WARN/FAIL verdict and red diff image), `visual-loop.mjs` (automated N-iteration loop — Claude Vision reads the diff, patches code, repeats until PASS).

Works for landings, marketing sites, portfolios, and ecommerce product pages. Not designed for SaaS dashboards, auth flows, or real-time data apps.

### marketing-suite

Five skills for marketing agencies and sales teams — from prospect research to retainer strategy.

| Skill | What it does |
|-------|-------------|
| [agency-audit](./skills/marketing-suite/agency-audit/SKILL.md) | Audit any company website. Extracts SEO, tech stack, copy signals, competitor comparison. Generates a pitch-ready proposal with opportunity score, close probability, entry door service, and revenue projection |
| [retainer-finder](./skills/marketing-suite/retainer-finder/SKILL.md) | Analyze what depreciates without maintenance, map high-dependency services, generate a retainer brief with MRR estimate and transition path from first project to monthly contract |
| [meeting-prep](./skills/marketing-suite/meeting-prep/SKILL.md) | Research a prospect and generate a 5-minute sales brief with evidence-based pain points, research-specific questions, and one insight that builds rapport |
| [cold-outreach](./skills/marketing-suite/cold-outreach/SKILL.md) | Research a prospect and write a personalized 4-message sequence (opener, two follow-ups, break-up) based on real signals from their website — not templates |
| [ad-analyzer](./skills/marketing-suite/ad-analyzer/SKILL.md) | Analyze competitor ads from Meta Ad Library or pasted copy. Extract hook patterns, offer structures, emotional triggers, and generate test variants with hypotheses |

---

## Install

### A specific pack or skill

```bash
npx @veyralabs/skills install naming-suite
npx @veyralabs/skills install webcloner
npx @veyralabs/skills install shopify-suite
npx @veyralabs/skills install shopify-dev
npx @veyralabs/skills install shopify-store
npx @veyralabs/skills install venture-suite
npx @veyralabs/skills install venture-analyst
npx @veyralabs/skills install marketing-suite
npx @veyralabs/skills install agency-audit
npx @veyralabs/skills install domainforge
```

### All skills

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/veyralabsgroup/veyraskills/main/install.sh)
```

### Global (available across all projects)

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/veyralabsgroup/veyraskills/main/install.sh) --global
```

### Manual

Copy the skill folder into your agent's skills directory and restart the agent.

| Agent | Project skills | Global skills |
|-------|---------------|--------------|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `.cursor/skills/` | `~/.cursor/skills/` |
| Windsurf | `.windsurf/skills/` | `~/.codeium/windsurf/skills/` |
| Gemini CLI | `.gemini/skills/` | `~/.gemini/skills/` |
| GitHub Copilot | `.github/skills/` | `~/.copilot/skills/` |

---

## How it works

Skills are Markdown files with a small YAML header. Claude Code reads them at startup and knows when to activate them based on what you type. No configuration, no plugins, no API keys.

```
Find a name for my new developer tool
```

That's enough to activate `domainforge`. The skill takes over from there.

---

## Packs vs individual skills

A pack is a folder of related skills that work together. Install a pack and you get all the skills inside it.

```bash
# Install the full naming-suite pack (4 skills)
npx @veyralabs/skills install naming-suite

# Install just one skill from the pack
npx @veyralabs/skills install domainforge
```

---

## Coming soon

**brand-suite**
- `brandvoice` - tone of voice guide generator
- `brandpositioning` - positioning statement and competitive differentiation
- `taglineforge` - tagline generation with scoring

**gtm-suite**
- `icp` - Ideal Customer Profile builder
- `pricingstrategy` - pricing model analysis
- `gtmplan` - go-to-market plan generator

---

## Individual packages

Each skill is also published as a standalone npm package if you only want one:

- `@veyralabs/naming-suite`
- `@veyralabs/webcloner`
- `@veyralabs/shopify-suite`
- `@veyralabs/shopify-dev`
- `@veyralabs/shopify-store`
- `@veyralabs/venture-suite`
- `@veyralabs/venture-analyst`
- `@veyralabs/marketing-suite`
- `@veyralabs/agency-audit`

---

## Contributing

Validate your skill before opening a PR:

```bash
node validate.js
```

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the full guide.

---

## License

MIT. Built by [VeyraLabs](https://veyralabs.com).
