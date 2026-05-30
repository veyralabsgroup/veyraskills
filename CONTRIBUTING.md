# Contributing

## Adding a new skill

1. Copy `skill-template/` to `skills/<your-skill-name>/`
2. Fill in `SKILL.md` — see the template for required frontmatter fields
3. Add reference files to `references/` if needed
4. Run `node validate.js` — must pass before opening a PR
5. Update the skills table in `README.md`
6. Add a `CHANGELOG.md` entry

## Skill quality bar

Skills in this repo are expected to:

- Have a clear, specific trigger condition (when should the skill activate?)
- Produce consistent, structured output
- Work with at least Claude Code and Cursor
- Not leak implementation details into user-facing output

## Frontmatter requirements

Every `SKILL.md` must start with a valid YAML block:

```yaml
---
name: your-skill-name
description: >
  One paragraph explaining what this skill does and when to activate it.
  Be specific — agents use this to decide whether to load the skill.
---
```

`name` must be lowercase alphanumeric with hyphens only. No spaces.

## Pull request checklist

- [ ] `node validate.js` passes
- [ ] Skill tested with at least one agent
- [ ] README updated
- [ ] CHANGELOG entry added

## Questions

Open an issue or reach out at [veyralabs.com](https://veyralabs.com).
