# Codex-OS

Langues : [English](./README.md) | [中文](./README.zh-CN.md) | [Français](./README.fr.md) | [Deutsch](./README.de.md)

Ce document est une version française du `README.md`. La version anglaise reste la source canonique et la plus à jour.

## Présentation

Codex-OS est une couche d’exploitation native pour Codex, composée de règles Markdown, de fichiers mémoire et d’un exécuteur léger.
Le but n’est pas de remplacer Codex, mais de standardiser son comportement dans vos dépôts.

Le projet aide à :
- éviter de répéter les mêmes prompts et habitudes dans chaque repo
- garder un contexte local propre et isolé
- réutiliser un workflow stable entre plusieurs projets

Claude Code est aussi pris en charge via `ro-claude` et une couche d’instructions dédiée.

## Frontend hébergé

- Site live : https://rotsl.github.io/codex-os/
- Source UI : `docs/index.html`
- Workflow GitHub Pages : `.github/workflows/pages.yml`
- Le rendu de sortie gère :
  - texte brut
  - code
  - Markdown
  - JSON
  - tableaux

## Avant installation

Sauvegardez d’abord votre dossier Codex :

```bash
cp -R ~/.codex ~/.codex.backup.$(date +%Y%m%d%H%M%S)
```

Pourquoi :
- l’installation relie le chargeur global et le PATH
- la sauvegarde permet un retour arrière rapide

## Installation

Depuis la racine du dépôt :

```bash
./install.sh
```

Pour Claude Code :

```bash
./installclaude.sh
```

Les installateurs demandent maintenant si l’installation est :
- `this repo only`
- `systemwide`

### Mode dépôt uniquement

- usage limité à ce dépôt
- ne modifie pas `~/.codex`, `~/.claude` ni le PATH
- permet d’exécuter directement `./ro` ou `./ro-claude`

### Mode global

- affiche d’abord les commandes de sauvegarde et de restauration
- continue uniquement si vous tapez `Accept`
- annule si vous choisissez `Decline`

## Ce que l’installation configure

### `install.sh`

- `~/.codex/system -> <this repo>`
- `~/.local/bin/ro -> ~/.codex/system/ro`
- shim `codex` si le binaire est détecté
- `~/.codex/AGENTS.md -> ~/.codex/system/AGENTS.md`
- création des fichiers/répertoires manquants :
  - `~/.codex/config.toml`
  - `~/.codex/system/plugins/`
  - `~/.codex/system/plugin-registry.json`

### `installclaude.sh`

- `~/.codex/system -> <this repo>`
- `~/.local/bin/ro-claude -> ~/.codex/system/ro-claude`
- `~/.claude/CLAUDE.md -> ~/.codex/system/claude/CLAUDE.md`
- `~/.claude/agents/*.md -> ~/.codex/system/claude/agents/*.md`

## Intégration avec Codex et Claude Code

### Codex

1. Codex charge `~/.codex/AGENTS.md`
2. ce fichier est lié à `AGENTS.md` dans ce dépôt
3. chaque projet peut étendre les règles avec son propre `AGENTS.md`
4. `ro` enveloppe `codex exec` avec :
   - contexte projet
   - mémoire
   - plugins
   - reprises bornées
5. au premier usage, de nouveaux projets reçoivent :
   - `AGENTS.md`
   - `memory/context.md`
   - `memory/decisions.md`

### Claude Code

1. Claude Code charge `~/.claude/CLAUDE.md`
2. ce fichier pointe vers `claude/CLAUDE.md`
3. les sous-agents sont fournis par `claude/agents/*.md`
4. `ro-claude` exécute `claude -p`
5. deux modes mémoire sont disponibles :
   - `auto`
   - `deterministic`

Prérequis Claude :
- la CLI Claude locale doit déjà être connectée

## Utilisation

### Terminal

```bash
ro "build login API"
ro build "task"
ro write "task"
ro analyze "task"
```

Claude :

```bash
ro-claude --memory-mode auto "task"
ro-claude --memory-mode deterministic "task"
```

### Dans un venv Python

```bash
source .venv/bin/activate
ro "run tests and fix failures"
```

Forcer le chemin du binaire Codex si nécessaire :

```bash
export RO_CODEX_BIN="/absolute/path/to/codex"
```

### Chat Codex dans VS Code

Vous pouvez écrire directement la tâche :

```text
refactor auth middleware
```

Ou une forme commande :

```text
ro "check dataset counts"
```

Dans le chat, cela reste une intention de tâche, pas une commande shell réelle.

## Paquet npm

Le dépôt inclut `codexospackage/`.

Installation globale :

```bash
npm install -g ./codexospackage
```

Ensuite :

```bash
codexos install
codexos install-claude
codexos ro "build login API"
codexos claude --memory-mode auto "review this project"
codexos doctor
```

Options :
- `CODEXOS_SKIP_POSTINSTALL=1`
- `codexos install --repo /absolute/path/to/codex-os`

## Plugins

```bash
ro plugin install sql-helper
ro plugin install https://github.com/user/repo
ro plugin list
ro plugin remove sql-helper
```

Contrat plugin :
- chaque plugin doit inclure `SKILL.md`
- les plugins fournissent de la guidance, pas d’exécution de code distant

## Mémoire et isolation

Fichiers locaux par projet :
- `.ro_history.json`
- `memory/context.md`
- `memory/decisions.md`

Mémoire Claude :
- `auto`
- `deterministic`

Contexte partagé optionnel :
- `--context`
- `--share`
- pas de fusion automatique entre projets

Mémoire globale optionnelle :
- `~/.codex/global_memory.md`

## Carte du dépôt

### Racine

- `AGENTS.md` : orchestrateur principal
- `ro` : wrapper CLI Codex
- `ro-claude` : wrapper CLI Claude
- `install.sh` : installation globale Codex
- `installclaude.sh` : installation Claude
- `docs/index.html` : UI GitHub Pages
- `.github/workflows/pages.yml` : déploiement Pages
- `plugin-registry.json` : registre de plugins

### Dossiers principaux

- `agents/` : planification, architecture, build, revue, écriture
- `skills/` : reasoning, structure, completion, notai
- `rules/` : workflow, token-efficiency, memory
- `contexts/` : autoload, loading, repository-classification, summarization
- `memory/` : mémoire courante et décisions durables
- `plugins/` : plugins optionnels
- `claude/` : instructions et sous-agents Claude

## Retour arrière

```bash
rm -f ~/.codex/system
rm -f ~/.codex/AGENTS.md
rm -f ~/.local/bin/ro
rm -f ~/.local/bin/codex
mv ~/.codex.backup.<timestamp> ~/.codex
```

## Changelog

### v0.0.2 — 24 mars 2026
- passage de `codexospackage` à `v0.0.2`
- ajout du support Claude Code
- ajout du choix du périmètre d’installation
- mise à jour du site docs

### v0.0.1 — 18 mars 2026
- première version publique
- ajout de l’orchestrateur Codex-OS, des agents, skills, rules, contexts et mémoire
- ajout du wrapper CLI `ro` et du paquet npm

## Conseils pratiques

- gardez les règles dans `rules/` et les skills dans `skills/`
- gardez la mémoire courte et actuelle
- utilisez `--context` et `--share` seulement si nécessaire
- `ro-claude` est un wrapper léger autour de `claude -p`

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
  <sub>Conçu pour le terminal, VS Code et le chat Codex.</sub>
</div>
