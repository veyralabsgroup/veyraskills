#!/usr/bin/env bash
# VeyraLabs Skills installer
# https://github.com/veyralabsgroup/veyraskills

set -euo pipefail

REPO="veyralabsgroup/veyraskills"
GITHUB="https://github.com/${REPO}.git"

SKILL_NAME=""
GLOBAL=false
AGENT=""
LIST_ONLY=false

# ── argument parsing ─────────────────────────────────────────────────────────

usage() {
  cat <<EOF
VeyraLabs Skills — installer

Usage:
  bash install.sh [options]

Options:
  --skill <name>    Install a specific skill (default: all)
  --global          Install globally instead of project-local
  --agent <name>    Target agent (auto-detected if omitted)
  --list            List available skills
  -h, --help        Show this help

Supported agents:
  claude, cursor, windsurf, gemini, copilot, cline, goose, openhands, roo

Examples:
  # Auto-detect agent, install all skills to current project
  bash install.sh

  # Install domainforge globally for Claude Code
  bash install.sh --skill domainforge --global --agent claude

  # List available skills
  bash install.sh --list
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skill)   SKILL_NAME="$2"; shift 2 ;;
    --global)  GLOBAL=true; shift ;;
    --agent)   AGENT="$2"; shift 2 ;;
    --list)    LIST_ONLY=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *)         echo "Unknown option: $1"; usage; exit 1 ;;
  esac
done

# ── agent detection ──────────────────────────────────────────────────────────

detect_agent() {
  [[ -f ".claude/settings.json" ]] || [[ -d ".claude" ]]   && echo "claude"   && return
  [[ -d ".cursor" ]]                                        && echo "cursor"   && return
  [[ -d ".windsurf" ]]                                      && echo "windsurf" && return
  [[ -d ".gemini" ]]                                        && echo "gemini"   && return
  [[ -d ".github/copilot" ]]                                && echo "copilot"  && return
  [[ -d ".cline" ]]                                         && echo "cline"    && return
  [[ -d ".goose" ]]                                         && echo "goose"    && return
  [[ -d ".openhands" ]]                                     && echo "openhands"&& return
  [[ -d ".roo" ]]                                           && echo "roo"      && return
  echo ""
}

skills_dir() {
  local agent="$1"

  if [[ "$GLOBAL" == "true" ]]; then
    case "$agent" in
      claude)    echo "$HOME/.claude/skills"                   ;;
      cursor)    echo "$HOME/.cursor/skills"                   ;;
      windsurf)  echo "$HOME/.codeium/windsurf/skills"         ;;
      gemini)    echo "$HOME/.gemini/skills"                   ;;
      copilot)   echo "$HOME/.copilot/skills"                  ;;
      cline)     echo "$HOME/.cline/skills"                    ;;
      goose)     echo "$HOME/.config/goose/skills"             ;;
      openhands) echo "$HOME/.openhands/skills"                ;;
      roo)       echo "$HOME/.roo/skills"                      ;;
      *)         echo "$HOME/.skills"                          ;;
    esac
  else
    case "$agent" in
      claude)    echo ".claude/skills"   ;;
      cursor)    echo ".cursor/skills"   ;;
      windsurf)  echo ".windsurf/skills" ;;
      gemini)    echo ".gemini/skills"   ;;
      copilot)   echo ".github/skills"   ;;
      cline)     echo ".cline/skills"    ;;
      goose)     echo ".goose/skills"    ;;
      openhands) echo ".openhands/skills";;
      roo)       echo ".roo/skills"      ;;
      *)         echo ".skills"          ;;
    esac
  fi
}

# ── install logic ────────────────────────────────────────────────────────────

check_deps() {
  local missing=()
  command -v git &>/dev/null || missing+=("git")

  if [[ ${#missing[@]} -gt 0 ]]; then
    echo "Error: required tools missing: ${missing[*]}"
    echo "Install git and try again."
    exit 1
  fi
}

# Skills that require Python packages: skill_name -> pip packages (space-separated)
declare -A SKILL_PIP_DEPS=(
  ["shopify-store"]="scrapling"
  ["webcloner"]="scrapling"
  ["venture-analyst"]="scrapling ddgs trendspyg requests"
  ["agency-audit"]="scrapling requests ddgs"
  ["cold-outreach"]="scrapling requests ddgs"
  ["meeting-prep"]="scrapling requests ddgs"
  ["ad-analyzer"]="scrapling requests"
)

install_pip_deps() {
  local skill="$1"
  local pkgs="${SKILL_PIP_DEPS[$skill]:-}"
  [[ -z "$pkgs" ]] && return

  local pip=""
  for cmd in pip3 pip; do
    command -v "$cmd" &>/dev/null && pip="$cmd" && break
  done

  if [[ -z "$pip" ]]; then
    echo "  Warning: pip not found. Install manually: pip install $pkgs"
    return
  fi

  for pkg in $pkgs; do
    echo "  Installing Python dependency: $pkg..."
    if "$pip" install "$pkg" -q; then
      echo "  ✓ $pkg"
    else
      echo "  Warning: failed to install $pkg. Run: $pip install $pkg"
    fi
  done
}

install_skill() {
  local skill="$1"
  local dest_dir="$2"
  local tmp

  tmp=$(mktemp -d)
  # shellcheck disable=SC2064
  trap "rm -rf '$tmp'" EXIT

  echo "  Cloning veyralabsgroup/veyraskills..."
  git clone --depth=1 --filter=blob:none --sparse "$GITHUB" "$tmp" -q

  (cd "$tmp" && git sparse-checkout set "skills/${skill}")

  if [[ ! -d "$tmp/skills/${skill}" ]]; then
    echo "  Error: skill '${skill}' not found in the repository."
    exit 1
  fi

  mkdir -p "$dest_dir"
  cp -r "$tmp/skills/${skill}" "$dest_dir/"

  trap - EXIT
  rm -rf "$tmp"
}

install_commands() {
  local agent="$1"
  local is_global="$2"
  local tmp="$3"

  # Slash commands are only supported by Claude Code
  [[ "$agent" != "claude" ]] && return

  local cmd_dir
  if [[ "$is_global" == "true" ]]; then
    cmd_dir="$HOME/.claude/commands"
  else
    cmd_dir=".claude/commands"
  fi

  if [[ -d "$tmp/commands" ]]; then
    mkdir -p "$cmd_dir"
    cp "$tmp/commands/"*.md "$cmd_dir/" 2>/dev/null || true
    echo "  Slash commands → ${cmd_dir}/"
  fi
}

install_all() {
  local dest_dir="$1"
  local tmp

  tmp=$(mktemp -d)
  # shellcheck disable=SC2064
  trap "rm -rf '$tmp'" EXIT

  echo "  Cloning veyralabsgroup/veyraskills..."
  git clone --depth=1 --filter=blob:none --sparse "$GITHUB" "$tmp" -q
  (cd "$tmp" && git sparse-checkout set "skills" "commands")

  if [[ ! -d "$tmp/skills" ]]; then
    echo "  Error: could not retrieve skills from repository."
    exit 1
  fi

  mkdir -p "$dest_dir"
  cp -r "$tmp/skills/." "$dest_dir/"
  install_commands "$AGENT" "$GLOBAL" "$tmp"

  trap - EXIT
  rm -rf "$tmp"
}

list_skills() {
  local tmp
  tmp=$(mktemp -d)
  trap "rm -rf '$tmp'" EXIT

  git clone --depth=1 --filter=blob:none --sparse "$GITHUB" "$tmp" -q
  (cd "$tmp" && git sparse-checkout set "skills")

  echo "Available skills:"
  echo ""
  for d in "$tmp/skills"/*/; do
    local name
    name=$(basename "$d")
    echo "  • $name"
  done
  echo ""
  echo "Install:  bash install.sh --skill <name>"
  echo "All:      bash install.sh"

  trap - EXIT
  rm -rf "$tmp"
}

# ── main ─────────────────────────────────────────────────────────────────────

main() {
  check_deps

  if [[ "$LIST_ONLY" == "true" ]]; then
    list_skills
    exit 0
  fi

  if [[ -z "$AGENT" ]]; then
    AGENT=$(detect_agent)
    if [[ -z "$AGENT" ]]; then
      echo "Could not detect an agent in the current directory."
      echo "Specify one with --agent <name> (claude, cursor, windsurf, gemini, copilot, cline, goose)"
      exit 1
    fi
    echo "Detected agent: $AGENT"
  fi

  local dest
  dest=$(skills_dir "$AGENT")

  if [[ -n "$SKILL_NAME" ]]; then
    echo "Installing '$SKILL_NAME' → $dest/"
    install_skill "$SKILL_NAME" "$dest"
    install_pip_deps "$SKILL_NAME"
    echo ""
    echo "Done. ${dest}/${SKILL_NAME}/ is ready."
  else
    echo "Installing all skills → $dest/"
    install_all "$dest"
    for skill in "${!SKILL_PIP_DEPS[@]}"; do
      install_pip_deps "$skill"
    done
    echo ""
    echo "Done. All skills installed to ${dest}/"
  fi
}

main
