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
- proxies `ro-claude` command after setup
- provides `doctor` check for repo, `ro`, `ro-claude`, and `codex` shim

## Install
Global install (auto bootstrap):

```bash
npm install -g ./codexospackage
```

This postinstall path stays non-interactive and uses the systemwide install flow automatically so global npm installs do not hang on the new scope prompt.

If you want to skip auto bootstrap during install:

```bash
CODEXOS_SKIP_POSTINSTALL=1 npm install -g ./codexospackage
```

## Run
Install/repair wiring manually:

```bash
codexos install
```

The installer will ask whether the setup is for this repo only or systemwide.
If you choose systemwide, it will show backup and restore commands and proceed only after you type `Accept`.

Install/repair Claude wiring manually:

```bash
codexos install-claude
```

Use a specific local clone:

```bash
codexos install --repo /absolute/path/to/codex-os
```

Run a task:

```bash
codexos ro "build login API"
```

Run a Claude task:

```bash
codexos claude --memory-mode auto "review this project"
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
