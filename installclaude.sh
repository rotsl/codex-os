#!/usr/bin/env bash

set -e

prompt_install_scope() {
  if [ -n "${CODEXOS_INSTALL_SCOPE:-}" ]; then
    case "$CODEXOS_INSTALL_SCOPE" in
      repo|systemwide)
        INSTALL_SCOPE="$CODEXOS_INSTALL_SCOPE"
        return
        ;;
      *)
        echo "Invalid CODEXOS_INSTALL_SCOPE: $CODEXOS_INSTALL_SCOPE"
        exit 1
        ;;
    esac
  fi

  while true; do
    cat <<'EOF'
Choose install scope for Codex-OS Claude support:
  1) this repo only
  2) systemwide
  3) decline
EOF
    read -r -p "Enter 1, 2, or 3: " scope_choice
    case "$scope_choice" in
      1) INSTALL_SCOPE="repo"; return ;;
      2) INSTALL_SCOPE="systemwide"; return ;;
      3)
        printf '^C\n'
        exit 130
        ;;
      *) echo "Invalid choice. Please enter 1, 2, or 3." ;;
    esac
  done
}

confirm_systemwide_install() {
  local backup_cmd='cp -R ~/.claude ~/.claude.backup.$(date +%Y%m%d%H%M%S)'
  local restore_cmd='mv ~/.claude.backup.<timestamp> ~/.claude'

  if [ "${CODEXOS_INSTALL_ACCEPT:-}" = "Accept" ]; then
    return
  fi

  cat <<EOF
Systemwide Claude install selected.

Backup your settings with:
  ${backup_cmd}

Retrieve them with:
  ${restore_cmd}
EOF

  read -r -p "Type Accept to proceed or Decline to cancel: " decision
  case "$decision" in
    Accept) ;;
    Decline)
      printf '^C\n'
      exit 130
      ;;
    *)
      echo "Install cancelled. Type Accept exactly to proceed."
      printf '^C\n'
      exit 130
      ;;
  esac
}

echo "Setting up Codex-OS for Claude Code..."

prompt_install_scope

if [ "$INSTALL_SCOPE" = "repo" ]; then
  chmod +x ./ro-claude
  echo "Repo-only Claude setup complete."
  echo "Use ./ro-claude from this repository. No global Claude settings were changed."
  exit 0
fi

confirm_systemwide_install

mkdir -p ~/.codex

# Link shared system root
ln -sfn "$(pwd)" ~/.codex/system

# Expose ro-claude globally (user-level)
mkdir -p ~/.local/bin
ln -sfn ~/.codex/system/ro-claude ~/.local/bin/ro-claude
chmod +x ~/.codex/system/ro-claude

# Ensure ~/.local/bin is on PATH for common shells
PATH_LINE='export PATH="$HOME/.local/bin:$PATH"'
ensure_path_line() {
  local file="$1"
  if [ ! -f "$file" ]; then
    touch "$file"
  fi
  if ! grep -Fq "$PATH_LINE" "$file"; then
    printf '\n%s\n' "$PATH_LINE" >> "$file"
  fi
}

ensure_path_line "$HOME/.bash_profile"
ensure_path_line "$HOME/.bashrc"
ensure_path_line "$HOME/.zshrc"

# Make available in current shell for immediate use
export PATH="$HOME/.local/bin:$PATH"

# Link global Claude instructions to system CLAUDE layer
mkdir -p ~/.claude
GLOBAL_CLAUDE="$HOME/.claude/CLAUDE.md"
if [ -e "$GLOBAL_CLAUDE" ] && [ ! -L "$GLOBAL_CLAUDE" ]; then
  cp "$GLOBAL_CLAUDE" "$GLOBAL_CLAUDE.bak.$(date +%Y%m%d%H%M%S)"
fi
ln -sfn ~/.codex/system/claude/CLAUDE.md "$GLOBAL_CLAUDE"

# Make Claude subagents available globally without copying them.
mkdir -p ~/.claude/agents
for agent_file in ~/.codex/system/claude/agents/*.md; do
  agent_name="$(basename "$agent_file")"
  ln -sfn "$agent_file" "$HOME/.claude/agents/$agent_name"
done

echo "Claude setup complete."

if command -v ro-claude >/dev/null 2>&1; then
  echo "ro-claude is available at: $(command -v ro-claude)"
else
  echo "'ro-claude' is not yet in this shell PATH. Restart terminal or run: source ~/.bash_profile"
fi
