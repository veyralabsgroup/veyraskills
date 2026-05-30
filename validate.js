#!/usr/bin/env node

'use strict';

const fs = require('fs');
const path = require('path');

const REQUIRED_FIELDS = ['name', 'description'];
const NAME_PATTERN = /^[a-z][a-z0-9-]*$/;
const SKILLS_DIR = path.join(__dirname, 'skills');

function findSkillFiles(dir) {
  const results = [];

  if (!fs.existsSync(dir)) return results;

  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    const candidate = path.join(dir, entry.name, 'SKILL.md');
    if (fs.existsSync(candidate)) results.push(candidate);
  }

  return results;
}

function parseFrontmatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return { error: 'No YAML frontmatter found. File must start with a --- block.' };

  const fields = {};
  const lines = match[1].split('\n');
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];
    const trimmed = line.trim();

    if (!trimmed || trimmed.startsWith('#')) { i++; continue; }

    const colon = trimmed.indexOf(':');
    if (colon === -1) { i++; continue; }

    const key = trimmed.slice(0, colon).trim();
    const rawValue = trimmed.slice(colon + 1).trim();

    if (!key || key.includes(' ')) { i++; continue; }

    // Handle block scalars (> and |)
    if (rawValue === '>' || rawValue === '|') {
      const blockLines = [];
      i++;
      while (i < lines.length && (lines[i].startsWith('  ') || lines[i].trim() === '')) {
        blockLines.push(lines[i].trim());
        i++;
      }
      fields[key] = blockLines.join(' ').trim();
    } else {
      fields[key] = rawValue.replace(/^['"]|['"]$/g, '');
      i++;
    }
  }

  return { fields };
}

function validate(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const relative = path.relative(__dirname, filePath);
  const errors = [];
  const warnings = [];

  const { error, fields } = parseFrontmatter(content);

  if (error) {
    return { file: relative, errors: [error], warnings, valid: false };
  }

  for (const field of REQUIRED_FIELDS) {
    if (!fields[field] || !fields[field].trim()) {
      errors.push(`Missing required field: "${field}"`);
    }
  }

  if (fields.name && !NAME_PATTERN.test(fields.name)) {
    errors.push(`"name" must be lowercase alphanumeric with hyphens only (got: "${fields.name}")`);
  }

  if (fields.description && fields.description.length < 20) {
    warnings.push(`"description" is very short (${fields.description.length} chars) — be more specific`);
  }

  const wordCount = content.split(/\s+/).filter(Boolean).length;
  if (wordCount < 100) {
    warnings.push(`SKILL.md has only ${wordCount} words — skills typically need more instructions`);
  }

  return { file: relative, errors, warnings, valid: errors.length === 0 };
}

function main() {
  const files = findSkillFiles(SKILLS_DIR);

  if (files.length === 0) {
    console.log('No SKILL.md files found in skills/');
    process.exit(0);
  }

  console.log(`Validating ${files.length} skill(s)...\n`);

  let allValid = true;

  for (const filePath of files) {
    const result = validate(filePath);
    const icon = result.valid ? '✓' : '✗';

    console.log(`${icon}  ${result.file}`);

    for (const err of result.errors) {
      console.log(`   ERROR  ${err}`);
      allValid = false;
    }

    for (const warn of result.warnings) {
      console.log(`   WARN   ${warn}`);
    }

    if (result.errors.length === 0 && result.warnings.length === 0) {
      console.log('   All checks passed');
    }

    console.log('');
  }

  if (!allValid) {
    console.error('Validation failed. Fix the errors above before merging.');
    process.exit(1);
  }

  console.log('All skills valid.');
}

main();
