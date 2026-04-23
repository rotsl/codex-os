# Codex-OS

Sprachen: [English](./README.md) | [中文](./README.zh-CN.md) | [Français](./README.fr.md) | [Deutsch](./README.de.md)

Dieses Dokument ist eine deutsche Fassung von `README.md`. Die englische Version bleibt die maßgebliche und aktuellste Quelle.

## Überblick

Codex-OS ist eine Codex-native Betriebsschicht aus Markdown-Regeln, Speicherdateien und einem schlanken Runner.
Es ersetzt Codex nicht, sondern standardisiert dessen Verhalten über verschiedene Repositories hinweg.

Das Projekt hilft dabei:
- wiederholte Prompt- und Memory-Setups in jedem Repo zu vermeiden
- lokalen Kontext sauber und isoliert zu halten
- einen stabilen, wiederverwendbaren Workflow bereitzustellen

Claude Code wird ebenfalls unterstützt, über `ro-claude` und eine eigene Claude-Instruktionsschicht.

## Gehostetes Frontend

- Live-Seite: https://rotsl.github.io/codex-os/
- UI-Quelle: `docs/index.html`
- GitHub-Pages-Workflow: `.github/workflows/pages.yml`
- Ausgaben werden typbewusst gerendert:
  - Klartext
  - Code
  - Markdown
  - JSON
  - tabellarische Inhalte

## Vor der Installation

Sichere zuerst deinen aktuellen Codex-Ordner:

```bash
cp -R ~/.codex ~/.codex.backup.$(date +%Y%m%d%H%M%S)
```

Warum:
- die Installation verbindet globalen Loader und PATH
- das Backup ermöglicht ein schnelles Rollback

## Installation

Im Repository-Stamm ausführen:

```bash
./install.sh
```

Für Claude Code:

```bash
./installclaude.sh
```

Die Installer fragen jetzt nach dem Installationsumfang:
- `this repo only`
- `systemwide`

### Nur dieses Repo

- Nutzung bleibt lokal in diesem Checkout
- ändert weder `~/.codex`, `~/.claude` noch den PATH
- `./ro` und `./ro-claude` können direkt verwendet werden

### Systemweit

- zeigt zuerst Backup- und Restore-Befehle
- läuft nur weiter, wenn du `Accept` eingibst
- bricht bei `Decline` ab

## Was die Installation verdrahtet

### `install.sh`

- `~/.codex/system -> <this repo>`
- `~/.local/bin/ro -> ~/.codex/system/ro`
- optionaler `codex`-Shim, wenn das Binary gefunden wird
- `~/.codex/AGENTS.md -> ~/.codex/system/AGENTS.md`
- erstellt fehlende Dateien/Ordner:
  - `~/.codex/config.toml`
  - `~/.codex/system/plugins/`
  - `~/.codex/system/plugin-registry.json`

### `installclaude.sh`

- `~/.codex/system -> <this repo>`
- `~/.local/bin/ro-claude -> ~/.codex/system/ro-claude`
- `~/.claude/CLAUDE.md -> ~/.codex/system/claude/CLAUDE.md`
- `~/.claude/agents/*.md -> ~/.codex/system/claude/agents/*.md`

## Einbindung in Codex und Claude Code

### Codex

1. Codex lädt `~/.codex/AGENTS.md`
2. diese Datei verweist auf `AGENTS.md` in diesem Repo
3. jedes Projekt kann lokale Regeln über eigenes `AGENTS.md` ergänzen
4. `ro` erweitert `codex exec` um:
   - Projektkontext
   - Memory-Verwaltung
   - Plugins
   - begrenzte Wiederholungen
5. neue Repos bekommen beim ersten `ro`-Lauf automatisch:
   - `AGENTS.md`
   - `memory/context.md`
   - `memory/decisions.md`

### Claude Code

1. Claude Code lädt `~/.claude/CLAUDE.md`
2. diese Datei verweist auf `claude/CLAUDE.md`
3. Unteragenten stammen aus `claude/agents/*.md`
4. `ro-claude` führt `claude -p` aus
5. zwei Speicher-Modi sind verfügbar:
   - `auto`
   - `deterministic`

Voraussetzung:
- die lokale Claude-CLI muss bereits angemeldet sein

## Nutzung

### Terminal

```bash
ro "build login API"
ro build "task"
ro write "task"
ro analyze "task"
```

Claude:

```bash
ro-claude --memory-mode auto "task"
ro-claude --memory-mode deterministic "task"
```

### In einer Python-venv

```bash
source .venv/bin/activate
ro "run tests and fix failures"
```

Falls nötig, kann der Codex-Pfad erzwungen werden:

```bash
export RO_CODEX_BIN="/absolute/path/to/codex"
```

### Codex-Chat in VS Code

Du kannst die Aufgabe direkt schreiben:

```text
refactor auth middleware
```

Oder im Kommandostil:

```text
ro "check dataset counts"
```

Im Chat wird das als Aufgabenabsicht behandelt, nicht als Shell-Befehl.

## npm-Paket

Das Repo enthält `codexospackage/`.

Globale Installation:

```bash
npm install -g ./codexospackage
```

Danach:

```bash
codexos install
codexos install-claude
codexos ro "build login API"
codexos claude --memory-mode auto "review this project"
codexos doctor
```

Optionen:
- `CODEXOS_SKIP_POSTINSTALL=1`
- `codexos install --repo /absolute/path/to/codex-os`

## Plugins

```bash
ro plugin install sql-helper
ro plugin install https://github.com/user/repo
ro plugin list
ro plugin remove sql-helper
```

Plugin-Vertrag:
- jedes Plugin muss ein `SKILL.md` bereitstellen
- Plugins liefern nur Anleitungen, keinen Remote-Runtime-Code

## Memory und Isolation

Projektlokale Dateien:
- `.ro_history.json`
- `memory/context.md`
- `memory/decisions.md`

Claude-Memory-Modi:
- `auto`
- `deterministic`

Optionaler geteilter Kontext:
- `--context`
- `--share`
- keine automatische Zusammenführung zwischen Projekten

Optionaler globaler Speicher:
- `~/.codex/global_memory.md`

## Repository-Struktur

### Root

- `AGENTS.md`: Hauptorchestrator
- `ro`: Codex-CLI-Wrapper
- `ro-claude`: Claude-CLI-Wrapper
- `install.sh`: Codex-Installation
- `installclaude.sh`: Claude-Installation
- `docs/index.html`: GitHub-Pages-Frontend
- `.github/workflows/pages.yml`: Pages-Deployment
- `plugin-registry.json`: Plugin-Registry

### Wichtige Verzeichnisse

- `agents/`: Planung, Architektur, Build, Review, Schreiben
- `skills/`: reasoning, structure, completion, notai
- `rules/`: workflow, token-efficiency, memory
- `contexts/`: autoload, loading, repository-classification, summarization
- `memory/`: aktueller Zustand und dauerhafte Entscheidungen
- `plugins/`: optionale Plugins
- `claude/`: Claude-Anweisungen und Unteragenten

## Rollback

```bash
rm -f ~/.codex/system
rm -f ~/.codex/AGENTS.md
rm -f ~/.local/bin/ro
rm -f ~/.local/bin/codex
mv ~/.codex.backup.<timestamp> ~/.codex
```

## Changelog

### v0.0.2 — 24. März 2026
- `codexospackage` auf `v0.0.2` erhöht
- Claude-Code-Unterstützung hinzugefügt
- Auswahl für repo-lokale oder systemweite Installation hinzugefügt
- Docs-Site aktualisiert

### v0.0.1 — 18. März 2026
- erste öffentliche Version
- Codex-OS-Orchestrator, Agents, Skills, Rules, Contexts und Memory hinzugefügt
- CLI-Wrapper `ro` und npm-Paket hinzugefügt

## Praktische Tipps

- Regeln in `rules/`, Skills in `skills/` halten
- Memory kurz und aktuell halten
- `--context` und `--share` nur bei Bedarf verwenden
- `ro-claude` ist ein schlanker Wrapper um `claude -p`

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
  <sub>Gebaut für Terminal, VS Code und Codex-Chat.</sub>
</div>
