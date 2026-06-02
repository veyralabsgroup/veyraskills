#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execFileSync } = require('child_process');

const SKILLS_DIR   = path.join(__dirname, '..', 'skills');
const COMMANDS_DIR = path.join(__dirname, '..', 'commands');

// pip packages required per skill
const SKILL_PIP_DEPS = {
  'shopify-store':    ['scrapling'],
  'webcloner':        ['scrapling'],
  'venture-analyst':  ['scrapling', 'ddgs', 'trendspyg', 'requests'],
  'agency-audit':     ['scrapling', 'requests', 'ddgs'],
  'cold-outreach':    ['scrapling', 'requests', 'ddgs'],
  'meeting-prep':     ['scrapling', 'requests', 'ddgs'],
  'ad-analyzer':      ['scrapling', 'requests'],
};

const AGENT_PATHS = {
  claude:    { local: '.claude/skills',             global: '.claude/skills' },
  cursor:    { local: '.cursor/skills',             global: '.cursor/skills' },
  windsurf:  { local: '.windsurf/skills',           global: '.codeium/windsurf/skills' },
  gemini:    { local: '.gemini/skills',             global: '.gemini/skills' },
  copilot:   { local: '.github/skills',             global: '.copilot/skills' },
  cline:     { local: '.cline/skills',              global: '.cline/skills' },
  goose:     { local: '.goose/skills',              global: '.config/goose/skills' },
  openhands: { local: '.openhands/skills',          global: '.openhands/skills' },
  roo:       { local: '.roo/skills',                global: '.roo/skills' },
};

// Auto-discover skills and packs from filesystem.
// Standalone skill: skills/<name>/SKILL.md
// Pack: skills/<pack>/<name>/SKILL.md (no SKILL.md at pack level)
function discover() {
  const skills = {};  // name → absolute path
  const packs = {};   // packName → [skillName, ...]

  if (!fs.existsSync(SKILLS_DIR)) return { skills, packs };

  for (const entry of fs.readdirSync(SKILLS_DIR, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    const entryPath = path.join(SKILLS_DIR, entry.name);

    if (fs.existsSync(path.join(entryPath, 'SKILL.md'))) {
      skills[entry.name] = entryPath;
    } else {
      const packSkills = [];
      for (const sub of fs.readdirSync(entryPath, { withFileTypes: true })) {
        if (!sub.isDirectory()) continue;
        const subPath = path.join(entryPath, sub.name);
        if (fs.existsSync(path.join(subPath, 'SKILL.md'))) {
          skills[sub.name] = subPath;
          packSkills.push(sub.name);
        }
      }
      if (packSkills.length > 0) packs[entry.name] = packSkills;
    }
  }

  return { skills, packs };
}

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
  return isGlobal ? path.join(os.homedir(), rel) : path.join(process.cwd(), rel);
}

function copySkill(name, skillPath, dest) {
  const target = path.join(dest, name);
  fs.mkdirSync(dest, { recursive: true });
  fs.cpSync(skillPath, target, { recursive: true });
  console.log(`  ✓ ${name}`);
}

function installPipDeps(skillNames) {
  const pkgs = [...new Set(skillNames.flatMap(n => SKILL_PIP_DEPS[n] || []))];
  if (pkgs.length === 0) return;

  let pip = null;
  for (const cmd of ['pip3', 'pip']) {
    try { execFileSync(cmd, ['--version'], { stdio: 'ignore' }); pip = cmd; break; } catch {}
  }

  if (!pip) {
    console.log(`  ⚠ Python pip not found. Install manually: pip install ${pkgs.join(' ')}`);
    return;
  }

  for (const pkg of pkgs) {
    try {
      console.log(`  Installing Python dependency: ${pkg}...`);
      execFileSync(pip, ['install', pkg, '-q'], { stdio: 'inherit' });
      console.log(`  ✓ ${pkg}`);
    } catch {
      console.log(`  ⚠ Failed to install ${pkg}. Run: ${pip} install ${pkg}`);
    }
  }
}

// Copy slash commands — Claude Code only (.claude/commands/)
function copyCommands(agent, isGlobal) {
  if (agent !== 'claude') return;
  if (!fs.existsSync(COMMANDS_DIR)) return;

  const cmdDest = isGlobal
    ? path.join(os.homedir(), '.claude', 'commands')
    : path.join(process.cwd(), '.claude', 'commands');

  fs.mkdirSync(cmdDest, { recursive: true });
  for (const f of fs.readdirSync(COMMANDS_DIR)) {
    if (!f.endsWith('.md')) continue;
    fs.copyFileSync(path.join(COMMANDS_DIR, f), path.join(cmdDest, f));
  }
  console.log(`  ✓ slash commands → ${cmdDest}`);
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
  npx @veyralabs/skills install webcloner --global
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

const { skills, packs } = discover();

if (command === 'list') {
  if (Object.keys(packs).length > 0) {
    console.log('\nPacks:');
    for (const [pack, members] of Object.entries(packs)) {
      console.log(`  ${pack}  →  ${members.join(', ')}`);
    }
  }
  console.log('\nSkills:');
  for (const name of Object.keys(skills).sort()) {
    console.log(`  ${name}`);
  }
  console.log();
  process.exit(0);
}

if (command === 'install') {
  const agent = agentArg || detectAgent();
  const dest = resolveDestination(agent, isGlobal);

  let toInstall = [];

  if (!target) {
    toInstall = Object.keys(skills);
  } else if (packs[target]) {
    toInstall = packs[target];
  } else if (skills[target]) {
    toInstall = [target];
  } else {
    console.error(`Not found: "${target}"`);
    console.error(`Available skills: ${Object.keys(skills).join(', ')}`);
    console.error(`Available packs:  ${Object.keys(packs).join(', ')}`);
    process.exit(1);
  }

  const scope = isGlobal ? 'global' : 'project';
  console.log(`\nInstalling into ${dest} [${agent}/${scope}]\n`);
  toInstall.forEach(name => copySkill(name, skills[name], dest));
  copyCommands(agent, isGlobal);
  installPipDeps(toInstall);
  console.log('\nDone. Restart your agent to activate skills.\n');
  process.exit(0);
}

console.error(`Unknown command: ${command}`);
printHelp();
process.exit(1);
