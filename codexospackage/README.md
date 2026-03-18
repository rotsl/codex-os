# codexospackage

npm package wrapper for installing and running Codex-OS.

## Keywords
codex, codex-os, ai-workflow, cli, developer-tools, agentic

## License
MIT

## What This Package Does
- exposes `codexos` command
- on `npm install -g`, auto-bootstraps by cloning `https://github.com/rotsl/codex-os` to `~/.codex/codex-os` (if missing)
- runs Codex-OS `install.sh` automatically during package postinstall
- proxies `ro` command after setup
- provides `doctor` check for repo, `ro`, and `codex` shim

## Install
Global install (auto bootstrap):

```bash
npm install -g ./codexospackage
```

If you want to skip auto bootstrap during install:

```bash
CODEXOS_SKIP_POSTINSTALL=1 npm install -g ./codexospackage
```

## Run
Install/repair wiring manually:

```bash
codexos install
```

Use a specific local clone:

```bash
codexos install --repo /absolute/path/to/codex-os
```

Run a task:

```bash
codexos ro "build login API"
```

Check setup:

```bash
codexos doctor
```

## Equivalent Coverage
After bootstrap, behavior matches the main repository workflow:
- terminal usage
- terminal with venv
- VS Code terminal
- VS Code terminal with venv
- Codex chat-mode wiring through AGENTS autoload
