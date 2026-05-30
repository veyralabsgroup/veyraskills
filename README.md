# VeyraLabs Skills

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Works with 35+ agents](https://img.shields.io/badge/works_with-35%2B_agents-brightgreen)](#supported-agents)

Reusable agent skills from [VeyraLabs](https://veyralabs.com). Install once, use everywhere — Claude Code, Cursor, Windsurf, Gemini CLI, GitHub Copilot, and 30+ more.

---

## Skills

### [domainforge](./skills/domainforge/SKILL.md) — AI Brand & Domain Intelligence

Not a domain generator. A naming strategist.

Most naming tools produce garbage: `SmartAIHub.com`, `NextGenApp.io`, `AIFlowPro.net`. DomainForge operates differently — it reasons about your project like a senior creative director, applies real scoring criteria, checks live domain availability, and explains *why* a name works.

**What it does:**

- Detects your project archetype (B2B SaaS, DevTool, Consumer AI, Fintech, Viral App, etc.) and adjusts naming style accordingly
- Generates 20+ name candidates using phonetic construction, Latin/Greek roots, semantic blending, and modified real words
- Scores every name across 8 factors: brandability, pronunciation, memorability, length, SEO potential, social availability, trademark risk, viral potential
- Checks real-time domain availability across registrars (Porkbun, Namecheap, Cloudflare)
- Checks social handle availability on X, GitHub, Instagram, LinkedIn
- Flags trademark conflicts before you fall in love with a name
- Writes a brand narrative for top candidates: *why* this name, *who* it speaks to, *where* it positions you
- Iterates automatically when preferred names are taken

**Search modes:** Unicorn · SEO · Viral · Premium · Indie Hacker · Futuristic

---

## Installation

### One-line (bash)

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/veyralabsgroup/veyraskills/main/install.sh)
```

Install a specific skill:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/veyralabsgroup/veyraskills/main/install.sh) --skill domainforge
```

Install globally (available across all projects):

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/veyralabsgroup/veyraskills/main/install.sh) --skill domainforge --global
```

### Manual

Copy the skill folder to your agent's skills directory:

| Agent | Project path | Global path |
|-------|-------------|-------------|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `.cursor/skills/` | `~/.cursor/skills/` |
| Windsurf | `.windsurf/skills/` | `~/.codeium/windsurf/skills/` |

Then restart your agent.

---

## Supported Agents

| Agent | Project path | Global path |
|-------|-------------|-------------|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `.cursor/skills/` | `~/.cursor/skills/` |
| Windsurf | `.windsurf/skills/` | `~/.codeium/windsurf/skills/` |
| Gemini CLI | `.gemini/skills/` | `~/.gemini/skills/` |
| GitHub Copilot | `.github/skills/` | `~/.copilot/skills/` |
| Codex | `.codex/skills/` | `~/.codex/skills/` |
| Cline | `.cline/skills/` | `~/.cline/skills/` |
| Goose | `.goose/skills/` | `~/.config/goose/skills/` |
| OpenHands | `.openhands/skills/` | `~/.openhands/skills/` |
| Roo Code | `.roo/skills/` | `~/.roo/skills/` |

---

## Usage

Once installed, just work normally. Skills activate contextually.

**Explicit triggers (DomainForge):**
```
Find a domain for my new SaaS
Name my CLI tool for environment variables
I need a brand identity for my agency
What should I call this project?
```

**Implicit triggers — no prompt needed:**
```
I'm building a project management app for design teams
[While writing SEO strategy] → adds keyword domain options
[While writing landing page copy] → suggests aligned domain
```

**Explicit mode selection:**
```
Domainforge unicorn mode: project management for remote teams
Domainforge SEO mode: find keyword domains for my travel startup
Domainforge viral mode: consumer app for splitting bills
```

---

## Example Output

```
## DomainForge Analysis — Design Team Project Management

Archetype: B2B SaaS / Design-adjacent
Mode: Unicorn

### Top Recommendations

1. florae.io — 91/100
   Latin roots for organic growth and living structure.
   Elegant without being literal. At home in Figma, Linear, or Notion's world.
   Domain: florae.io — available (~$38/yr Porkbun)
   Social: @florae available on X, GitHub, Instagram
   Trademark: Clean

2. tarka.app — 86/100
   Hard phonetics, two clean syllables, works across languages.
   Designed-product energy without trying too hard.
   Domain: tarka.app — available (~$14/yr)
   Social: @tarka — check availability
   Trademark: Clean
```

---

## Roadmap

- [x] `domainforge` — stable, available now
- [x] `brandaudit` — stable, available now
- [x] `competitornames` — stable, available now
- [ ] `namingguide` — generate a naming guide (style, dos/don'ts) for a company or product line

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on submitting new skills.

To validate your skill before opening a PR:

```bash
node validate.js
```

---

## License

MIT — use, fork, modify, distribute freely.

Built by [VeyraLabs](https://veyralabs.com).
