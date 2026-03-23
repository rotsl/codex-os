#!/usr/bin/env bash

set -e

echo "Setting up Codex-OS for Claude Code..."

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
