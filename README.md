# VeyraSkills

![7 skills](https://img.shields.io/badge/skills-7-blue) ![npm](https://img.shields.io/npm/v/@veyralabs/skills) ![license](https://img.shields.io/badge/license-MIT-green)

Skills for Claude Code and other AI coding agents. Each skill is a plain text file that teaches your agent a specialized workflow — naming, branding, website cloning, Shopify development, and more.

```bash
npx @veyralabs/skills install naming-suite
npx @veyralabs/skills install webcloner
npx @veyralabs/skills install shopify-suite
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

### webcloner

Clone any landing page, marketing site, portfolio, or ecommerce storefront into a pixel-accurate Next.js replica.

| Skill | What it does |
|-------|-------------|
| [webcloner](./skills/webcloner/SKILL.md) | Six-phase visual cloning: recon with Scrapling, foundation setup, spec generation per section, parallel component build with git worktrees, assembly, and visual QA |

Includes three scripts: a Scrapling-based extractor (`extract.py`), an asset downloader with WebP conversion (`download-assets.mjs`), and a side-by-side screenshot comparison tool (`compare.mjs`).

Works for landings, marketing sites, portfolios, and ecommerce product pages. Not designed for SaaS dashboards, auth flows, or real-time data apps.

---

## Install

### A specific pack or skill

```bash
npx @veyralabs/skills install naming-suite
npx @veyralabs/skills install webcloner
npx @veyralabs/skills install shopify-suite
npx @veyralabs/skills install shopify-dev
npx @veyralabs/skills install shopify-store
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
- `brandvoice` — tone of voice guide generator
- `brandpositioning` — positioning statement and competitive differentiation
- `taglineforge` — tagline generation with scoring

**gtm-suite**
- `icp` — Ideal Customer Profile builder
- `pricingstrategy` — pricing model analysis
- `gtmplan` — go-to-market plan generator

---

## Individual packages

Each skill is also published as a standalone npm package if you only want one:

- `@veyralabs/naming-suite`
- `@veyralabs/webcloner`
- `@veyralabs/shopify-suite`
- `@veyralabs/shopify-dev`
- `@veyralabs/shopify-store`

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
