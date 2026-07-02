# Changelog

All notable changes to this project will be documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.8.0] — 2026-07-02

### Added

- `codegraph-usage` skill — field guide for [CodeGraph](https://github.com/colbymchenry/codegraph)
  - When to reach for CodeGraph and when not (structural vs semantic search)
  - Tool selection table: `explore`, `node`, `query`, `callers`, `callees`, `impact`, `affected`
  - Community-reported gotchas: impact vs callers, staleness banners, monorepo `projectPath`, CLI-without-MCP for containers
  - Contributed upstream in [codegraph#1117](https://github.com/colbymchenry/codegraph/pull/1117)

---

## [0.1.0] — 2025-05-30

### Added

- `domainforge` skill — AI brand & domain intelligence system
  - 8-factor name scoring rubric
  - 6 generation techniques (phonetic, Latin/Greek roots, semantic blending, etc.)
  - Brand archetype detection (10 archetypes)
  - TLD strategy guide with registrar recommendations
  - Example outputs reference
- `install.sh` — single-command installer for 10+ agents
- `validate.js` — frontmatter validator for CI and local development
- GitHub Actions workflow for skill validation on PRs
- `skill-template/` — starter template for new skill contributions
