# VeyraLabs Skills

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Skills](https://img.shields.io/badge/skills-5_available-brightgreen)](#packs)
[![Works with 30+ agents](https://img.shields.io/badge/works_with-30%2B_agents-blue)](#supported-agents)

A curated collection of agent skills for founders, developers, and builders. Claude Code, Cursor, Windsurf, Gemini CLI, GitHub Copilot, and 30+ more.

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/veyralabsgroup/veyraskills/main/install.sh)
```

---

## Packs

### `naming-suite` — Brand & Naming Intelligence

Four skills that work together. Find names, audit brands, map competitors, generate naming guides.

| Skill | What it does |
|-------|-------------|
| [`domainforge`](./skills/domainforge/SKILL.md) | Generate and score startup names. Domain availability, social handles, trademark check, brand narrative |
| [`brandaudit`](./skills/brandaudit/SKILL.md) | Audit an existing brand name across 8 dimensions. Severity scoring, rebrand verdict |
| [`competitornames`](./skills/competitornames/SKILL.md) | Map the naming landscape in your market. Saturation levels, whitespace, naming brief for DomainForge |
| [`namingguide`](./skills/namingguide/SKILL.md) | Generate a complete naming guide for a company or product line. Principles, system, dos/don'ts, approval checklist |

**Recommended flow:**

```
competitornames → domainforge
brandaudit      → namingguide
```

Run `competitornames` first to map the competitive landscape, then `domainforge` to generate names that stand out from it. Run `brandaudit` on an existing name, `namingguide` to lock in what works.

---

### `webcloner` — Website Visual Cloning

Clone any landing page, marketing site, portfolio, or ecommerce storefront into a pixel-accurate Next.js replica. Structured 6-phase process: extract → spec → build → QA.

| Skill | What it does |
|-------|-------------|
| [`webcloner`](./skills/webcloner/SKILL.md) | Clone any website's visual design. Scrapling extraction, spec-driven parallel build with git worktrees, visual regression QA |

**Included scripts:**

| Script | Purpose |
|--------|---------|
| `scripts/extract.py` | Scrapling-based extractor — DOM, computed CSS, assets, animations, tech stack |
| `scripts/download-assets.mjs` | Download all images/videos/fonts with WebP conversion |
| `scripts/compare.mjs` | Screenshot original vs clone at desktop + mobile |

**Usage:**
```
Clone this landing page: https://example.com
Replicate this design in Next.js: https://example.com
I want my site to look like this: https://example.com
```

**In scope:** landings, marketing sites, portfolios, ecommerce storefronts
**Not for:** SaaS dashboards, auth flows, real-time data apps

**Prerequisites:** Python 3.10+ with Scrapling, Node 18+

```bash
npx @veyralabs/skills install webcloner
```

Also available as a standalone repo: [veyralabsgroup/webcloner](https://github.com/veyralabsgroup/webcloner)

---

## Installation

### One-line

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/veyralabsgroup/veyraskills/main/install.sh)
```

Installs all available skills into your current project.

### Specific skill

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/veyralabsgroup/veyraskills/main/install.sh) --skill domainforge
```

### Global install (available across all projects)

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/veyralabsgroup/veyraskills/main/install.sh) --global
```

### Manual

Copy the skill folder to your agent's skills directory and restart the agent.

| Agent | Project | Global |
|-------|---------|--------|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `.cursor/skills/` | `~/.cursor/skills/` |
| Windsurf | `.windsurf/skills/` | `~/.codeium/windsurf/skills/` |
| Gemini CLI | `.gemini/skills/` | `~/.gemini/skills/` |
| GitHub Copilot | `.github/skills/` | `~/.copilot/skills/` |

---

## Usage

Once installed, skills activate contextually — no configuration needed.

**DomainForge:**
```
Find a domain for my new SaaS
Name my CLI tool for environment variables
What should I call this project?
```

**BrandAudit:**
```
Audit the brand name "Acme" for a B2B SaaS
Is our brand name working? Company is called Vercel for analytics tools
```

**CompetitorNames:**
```
Map the naming landscape for developer config tools
Who are my competitors and how are they named?
```

**NamingGuide:**
```
Create a naming guide for our company
We're building a product line and need naming conventions
Our feature naming is inconsistent — generate a guide
```

---

## Example Output — DomainForge

```
DomainForge Analysis — Developer Config Management

Archetype: DevTool / Infrastructure
Mode: Indie Hacker

Top Recommendations

1. krev.dev — 93/100
   Hard consonant, 4 chars, terminal-native in lowercase.
   Zero overlap with Vault/dotenv cluster. Premium DevTool energy.
   Domain: krev.dev — available (~$12/yr Porkbun)
   Social: @krev — available on X, GitHub
   Trademark: Clean

2. onyx.sh — 89/100
   Single hard word, immediate memorability, shell-adjacent TLD.
   Domain: onyx.sh — available (~$18/yr)
   Social: @onyxdev — available
   Trademark: Check in software category
```

---

## Supported Agents

| Agent | Supported |
|-------|-----------|
| Claude Code | ✅ |
| Cursor | ✅ |
| Windsurf | ✅ |
| Gemini CLI | ✅ |
| GitHub Copilot | ✅ |
| Codex | ✅ |
| Cline | ✅ |
| Goose | ✅ |
| OpenHands | ✅ |
| Roo Code | ✅ |

---

## Roadmap

**naming-suite** — stable, all 4 skills available now

**webcloner** — stable, available now

**brand-suite** *(coming soon)*
- `brandvoice` — tone of voice guide generator
- `brandpositioning` — positioning statement + competitive differentiation
- `taglineforge` — tagline generation with scoring

**gtm-suite** *(coming soon)*
- `icp` — Ideal Customer Profile builder
- `pricingstrategy` — pricing model analysis
- `gtmplan` — go-to-market plan generator

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on submitting new skills.

Validate before opening a PR:

```bash
node validate.js
```

---

## License

MIT — use, fork, modify, distribute freely.

Built by [VeyraLabs](https://veyralabs.com).
