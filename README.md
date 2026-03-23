# Codex-OS

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE) [![GitHub Repo](https://img.shields.io/badge/GitHub-rotsl%2Fcodex--os-181717?logo=github)](https://github.com/rotsl/codex-os) [![Node >=18](https://img.shields.io/badge/Node-%3E%3D18-339933?logo=node.js&logoColor=white)](./codexospackage/package.json) [![codexospackage 0.0.1](https://img.shields.io/badge/codexospackage-0.0.1-informational)](./codexospackage/package.json) [![npm version](https://img.shields.io/npm/v/codexospackage.svg)](https://www.npmjs.com/package/codexospackage) [![Live Demo](https://img.shields.io/badge/Live%20Demo-rotsl.github.io%2Fcodex--os-0aa?logo=githubpages&logoColor=white)](https://rotsl.github.io/codex-os/)

## Why This Exists
Most people end up repeating the same setup in every repo: prompts, memory notes, and run habits.
This project gives you one stable Codex workflow you can reuse across projects.
It keeps your local project state separate, supports optional cross-project context, and gives you a thin CLI so you can move faster without losing control.

## What This Repo Is
Codex-OS is a Codex-native operating layer made of markdown rules + a thin runner.
It does not replace Codex. It standardizes how Codex behaves in your repos.

Claude Code is also supported through a parallel thin runner and instruction layer, with a user-selectable memory mode.

## Hosted Frontend
- Live site: https://rotsl.github.io/codex-os/
- UI source: `docs/index.html`
- Output rendering is type-aware:
  - plain text renders directly
  - code, markdown, JSON, and table-like content render as labeled artifacts


## Custom GPT
- **Codex OS**: [https://chatgpt.com/g/g-69bb21d374f08191ba1f8211c950678a-codex-os](https://chatgpt.com/g/g-69bb21d374f08191ba1f8211c950678a-codex-os)
- A minimal, Codex-style engineering assistant with browsing, session context, and plugin-style roles. Based on Codex OS (minimal version of this repo).

## Before You Install (Important)
Back up your current Codex folder first.

```bash
cp -R ~/.codex ~/.codex.backup.$(date +%Y%m%d%H%M%S)
```

Why: install links your global loader and system path. Backup gives you a fast rollback.

## Install
From this repo root:

```bash
./install.sh
```

For Claude Code, use the separate installer:

```bash
./installclaude.sh
```

What install wires:
- `~/.codex/system -> <this repo>` (symlink)
- `~/.local/bin/ro -> ~/.codex/system/ro`
- `~/.local/bin/codex` shim when Codex binary is discoverable
- `~/.codex/AGENTS.md -> ~/.codex/system/AGENTS.md`
- creates missing `~/.codex/config.toml` (if absent)
- creates missing `~/.codex/system/plugins/`
- creates missing `~/.codex/system/plugin-registry.json`

What `installclaude.sh` wires:
- `~/.codex/system -> <this repo>` (shared system root)
- `~/.local/bin/ro-claude -> ~/.codex/system/ro-claude`
- `~/.claude/CLAUDE.md -> ~/.codex/system/claude/CLAUDE.md`
- `~/.claude/agents/*.md -> ~/.codex/system/claude/agents/*.md`

## How It Wires Into Codex
1. Codex loads `~/.codex/AGENTS.md` from your global config.
2. That file is symlinked to this repo’s `AGENTS.md`.
3. In any project, `AGENTS.md` can extend local rules.
4. `ro` runs `codex exec` with project-aware prompt shaping, memory handling, plugin loading, and bounded retries.
5. New repos auto-bootstrap on first `ro` run:
   - `AGENTS.md`
   - `memory/context.md`
   - `memory/decisions.md`

## How It Wires Into Claude Code
1. Claude Code loads `~/.claude/CLAUDE.md`.
2. That file is symlinked to this repo’s Claude layer at `claude/CLAUDE.md`.
3. Claude subagents are linked from `claude/agents/*.md` into `~/.claude/agents/`.
4. `ro-claude` runs `claude -p` with project-aware prompt shaping.
   - it uses the process working directory plus `--add-dir <project-root>` for workspace access
5. The user chooses memory mode:
   - `--memory-mode auto`: use `CLAUDE.md` and Claude Code auto-memory
   - `--memory-mode deterministic`: use `memory/context.md` and `memory/decisions.md` as the deterministic store
6. New repos auto-bootstrap on first `ro-claude` run:
   - `CLAUDE.md`
   - `memory/context.md` and `memory/decisions.md` only in deterministic mode

Claude CLI prerequisite:
- `ro-claude` assumes the local Claude CLI is already authenticated
- if not, the live invocation fails with `Not logged in · Please run /login`

## Usage Matrix

### 1. Plain Terminal
```bash
cd /path/to/project
ro "build login API"
```

Claude:

```bash
cd /path/to/project
ro-claude --memory-mode deterministic "build login API"
```

### 2. Terminal Inside a Python venv
```bash
cd /path/to/project
source .venv/bin/activate
ro "run tests and fix failures"
```

Notes:
- `ro` now resolves `codex` even when your venv PATH does not expose it.
- If needed, force binary path:
```bash
export RO_CODEX_BIN="/absolute/path/to/codex"
```

### 3. VS Code Terminal
```bash
cd /path/to/project
ro "refactor auth middleware"
```

### 4. VS Code Terminal + venv
```bash
cd /path/to/project
source .venv/bin/activate
ro "check no of files in data/raw/06-FEB_WT_PCBM_SUB"
```

### 5. VS Code Codex Chat Box (No Terminal Command)
In the chat box, write the task directly:

```text
check no of files in data/raw/06-FEB_WT_PCBM_SUB
```

You can also type command-style text:

```text
ro "check dataset counts"
```

In chat, that is treated as task intent, not a shell command call.

## Core Commands

```bash
ro "task"
ro build "task"
ro write "task"
ro analyze "task"
ro --plugin sql-helper "optimize query"
ro --context ../other-repo "reuse approach"
ro --share ../other-repo "reuse logic safely"
ro-claude --memory-mode auto "task"
ro-claude --memory-mode deterministic "task"
ro-claude build "task"
ro-claude write "task"
ro-claude analyze "task"
```

Interactive mode:

```bash
ro
# ro > build API
# ro > write client update
# ro > exit
```

## npm Package: codexospackage (v0.0.1)
A packaged wrapper is available in `codexospackage/`.

Global install with auto bootstrap:

```bash
npm install -g ./codexospackage
```

This install now auto-clones `https://github.com/rotsl/codex-os` to `~/.codex/codex-os` (if missing) and runs `install.sh`.

Use it:

```bash
codexos install
codexos install-claude
codexos ro "build login API"
codexos claude --memory-mode auto "review this project"
codexos doctor
```

Optional:
- skip auto bootstrap at install time with `CODEXOS_SKIP_POSTINSTALL=1`
- install from a specific local clone with `codexos install --repo /absolute/path/to/codex-os`

Package files:
- `codexospackage/package.json`
- `codexospackage/bin/codexos.js`
- `codexospackage/bin/postinstall.js`
- `codexospackage/README.md`
- `codexospackage/LICENSE`

## Plugin Commands

```bash
ro plugin install sql-helper
ro plugin install https://github.com/user/repo
ro plugin list
ro plugin remove sql-helper
```

Global registry:
- `~/.codex/system/plugin-registry.json`

Plugin contract:
- each plugin must provide `SKILL.md`
- plugin content is guidance only; no runtime code execution from plugin repos

## Memory and Isolation
Project-local by default:
- `.ro_history.json`
- `memory/context.md`
- `memory/decisions.md`

Claude memory mode choice:
- `auto`: rely on `CLAUDE.md` plus Claude Code auto-memory
- `deterministic`: rely on `memory/context.md` and `memory/decisions.md`, loaded explicitly by `ro-claude`
- set default with `RO_CLAUDE_MEMORY_MODE=auto` or `RO_CLAUDE_MEMORY_MODE=deterministic`

Optional shared context:
- `--context` reads summary from another local repo (on demand)
- `--share` writes isolated `memory/shared_<hash>.md` files
- no automatic cross-project memory merge

Optional global memory:
- `~/.codex/global_memory.md`
- loaded as small snippet, never overriding project memory

## Repository Map (What Each File Does)

### Root
- `AGENTS.md`: main orchestrator and mode contracts.
- `ro`: thin CLI wrapper around `codex exec`.
- `ro-claude`: thin CLI wrapper around `claude -p` with selectable memory mode.
- `install.sh`: global setup and wiring script.
- `installclaude.sh`: Claude-only setup and wiring script.
- `README.md`: user guide.
- `LICENSE`: license terms.
- `.gitignore`: repo hygiene.
- `docs/index.html`: GitHub Pages frontend UI.
- `docs/.nojekyll`: prevents Jekyll processing on Pages.
- `plugin-registry.json`: default plugin registry seed.
- `claude/`: Claude Code global instructions and subagents.

### agents/
- `planner.md`: compact planning behavior.
- `architect.md`: structure and tradeoff rules.
- `builder.md`: implementation behavior for coding tasks.
- `reviewer.md`: quality checks and risk review.
- `writer.md`: prose generation/editing behavior.

### skills/
- `reasoning.md`: deep reasoning when complexity justifies it.
- `structure.md`: compressed structure and decomposition.
- `completion.md`: finish-until-done behavior with safe stop conditions.
- `notai.md`: human prose cleanup rules; never applied to code outputs.

### rules/
- `workflow.md`: execution loop and mode-independent process rules.
- `token-efficiency.md`: compression and context minimization rules.
- `memory.md`: what to load, store, and prune in memory.

### contexts/
- `autoload.md`: autoload expectations.
- `loading.md`: context loading order.
- `repository-classification.md`: repo/task-type classification notes.
- `summarization.md`: summarization policy.

### memory/
- `context.md`: current project state only.
- `decisions.md`: durable decisions only.
- `shared_<hash>.md`: optional explicit shared-context snapshots.

### plugins/
- `plugins/<name>/SKILL.md`: optional project-local plugin skills.

## Safe Rollback
If you want to undo installation:

```bash
rm -f ~/.codex/system
rm -f ~/.codex/AGENTS.md
rm -f ~/.local/bin/ro
rm -f ~/.local/bin/codex
mv ~/.codex.backup.<timestamp> ~/.codex
```


## Changelog
### v0.0.1 — March 18, 2026
- Initial GitHub release: `v0.0.1`.
- Added Codex-OS orchestrator, agents, skills, rules, contexts, and memory system.
- Added `ro` CLI with project-aware routing, bounded recovery, context/share support, and plugin loading.
- Added `codexospackage` npm wrapper with install/bootstrap and doctor commands.

## Practical Tips
- Keep rules in rules/ and skills in skills/; avoid duplication.
- Keep memory short and current.
- Use `--context` and `--share` only when you need external project context.
- `ro-claude`: thin CLI wrapper around `claude -p` with selectable memory mode.
- live-tested against a local Claude CLI that supports `-p` and `--append-system-prompt` but not `--cwd`.
- Use chat for direct tasks; use `ro` when you want repeatable command workflows.

---

<div align="center">
  <h3>Codex-OS</h3>
  <p><code>autoload • memory • plugins • repeatable workflows</code></p>
  <p>
    <a href="https://rotsl.github.io/codex-os/">Live Site</a>
    ·
    <a href="https://github.com/rotsl/codex-os">GitHub</a>
    ·
    <a href="https://www.npmjs.com/package/codexospackage">npm</a>
  </p>
  <sub>Built for terminal, VS Code, and Codex chat.</sub>
</div>
