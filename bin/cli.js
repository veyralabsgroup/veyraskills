#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');

const SKILLS_DIR = path.join(__dirname, '..', 'skills');

const PACKS = {
  'naming-suite': ['domainforge', 'brandaudit', 'competitornames', 'namingguide'],
};

const AGENT_PATHS = {
  claude:    { local: '.claude/skills',                  global: '.claude/skills' },
  cursor:    { local: '.cursor/skills',                  global: '.cursor/skills' },
  windsurf:  { local: '.windsurf/skills',                global: '.codeium/windsurf/skills' },
  gemini:    { local: '.gemini/skills',                  global: '.gemini/skills' },
  copilot:   { local: '.github/skills',                  global: '.copilot/skills' },
  cline:     { local: '.cline/skills',                   global: '.cline/skills' },
  goose:     { local: '.goose/skills',                   global: '.config/goose/skills' },
  openhands: { local: '.openhands/skills',               global: '.openhands/skills' },
  roo:       { local: '.roo/skills',                     global: '.roo/skills' },
};

function detectAgent() {
  const cwd = process.cwd();
  for (const agent of Object.keys(AGENT_PATHS)) {
    const dir = agent === 'copilot' ? '.github' : `.${agent}`;
    if (fs.existsSync(path.join(cwd, dir))) return agent;
  }
  return 'claude';
}

function resolveDestination(agent, isGlobal) {
  const entry = AGENT_PATHS[agent];
  if (!entry) {
    console.error(`Unknown agent: ${agent}. Options: ${Object.keys(AGENT_PATHS).join(', ')}`);
    process.exit(1);
  }
  const rel = isGlobal ? entry.global : entry.local;
  return isGlobal
    ? path.join(os.homedir(), rel)
    : path.join(process.cwd(), rel);
}

function copySkill(name, dest) {
  const src = path.join(SKILLS_DIR, name);
  if (!fs.existsSync(src)) {
    console.error(`Skill not found: ${name}`);
    console.error(`Available: ${availableSkills().join(', ')}`);
    process.exit(1);
  }
  const target = path.join(dest, name);
  fs.mkdirSync(dest, { recursive: true });
  fs.cpSync(src, target, { recursive: true });
  console.log(`  ✓ ${name}`);
}

function availableSkills() {
  return fs.readdirSync(SKILLS_DIR).filter(
    f => fs.statSync(path.join(SKILLS_DIR, f)).isDirectory()
  );
}

function printHelp() {
  console.log(`
Usage:
  npx @veyralabs/skills install                     Install all skills
  npx @veyralabs/skills install <skill|pack>        Install a skill or pack
  npx @veyralabs/skills list                        List available skills and packs

Options:
  --global              Install globally (all projects)
  --agent <name>        Target agent (auto-detected if omitted)
                        Options: ${Object.keys(AGENT_PATHS).join(', ')}

Examples:
  npx @veyralabs/skills install naming-suite
  npx @veyralabs/skills install domainforge --global
  npx @veyralabs/skills install domainforge --agent cursor
`);
}

// --- Parse args ---

const rawArgs = process.argv.slice(2);
const command = rawArgs[0];
const target = rawArgs[1] && !rawArgs[1].startsWith('--') ? rawArgs[1] : undefined;
const isGlobal = rawArgs.includes('--global');
const agentIdx = rawArgs.indexOf('--agent');
const agentArg = agentIdx !== -1 ? rawArgs[agentIdx + 1] : null;

// --- Commands ---

if (!command || command === 'help' || command === '--help' || command === '-h') {
  printHelp();
  process.exit(0);
}

if (command === 'list') {
  console.log('\nSkills:');
  availableSkills().forEach(s => console.log(`  ${s}`));
  console.log('\nPacks:');
  Object.entries(PACKS).forEach(([pack, skills]) =>
    console.log(`  ${pack}  →  ${skills.join(', ')}`)
  );
  console.log();
  process.exit(0);
}

if (command === 'install') {
  const agent = agentArg || detectAgent();
  const dest = resolveDestination(agent, isGlobal);

  let toInstall = [];

  if (!target) {
    toInstall = availableSkills();
  } else if (PACKS[target]) {
    toInstall = PACKS[target];
  } else {
    toInstall = [target];
  }

  const scope = isGlobal ? 'global' : 'project';
  console.log(`\nInstalling into ${dest} [${agent}/${scope}]\n`);
  toInstall.forEach(s => copySkill(s, dest));
  console.log('\nDone. Restart your agent to activate skills.\n');
  process.exit(0);
}

console.error(`Unknown command: ${command}`);
printHelp();
process.exit(1);
