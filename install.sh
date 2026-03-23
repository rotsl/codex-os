#!/usr/bin/env bash

set -e

echo "Setting up Codex-OS..."

mkdir -p ~/.codex

# Link system
ln -sfn "$(pwd)" ~/.codex/system

# Expose ro globally (user-level)
mkdir -p ~/.local/bin
ln -sfn ~/.codex/system/ro ~/.local/bin/ro
chmod +x ~/.codex/system/ro

# Link codex binary into ~/.local/bin when discoverable
CODEX_BIN="$(command -v codex || true)"
if [ -z "$CODEX_BIN" ]; then
  CODEX_BIN="$(ls -1dt "$HOME"/.vscode/extensions/openai.chatgpt-*/bin/*/codex 2>/dev/null | head -n 1 || true)"
fi
if [ -n "$CODEX_BIN" ]; then
  ln -sfn "$CODEX_BIN" ~/.local/bin/codex
fi

# Also link into common global PATH bins when writable
for bin_dir in /usr/local/bin /opt/homebrew/bin; do
  if [ -d "$bin_dir" ] && [ -w "$bin_dir" ]; then
    ln -sfn ~/.codex/system/ro "$bin_dir/ro"
  fi
done

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

# Ensure global plugin directory exists
mkdir -p ~/.codex/system/plugins

# Create plugin registry if missing
REGISTRY=~/.codex/system/plugin-registry.json
if [ ! -f "$REGISTRY" ]; then
cat <<EOF > "$REGISTRY"
{
  "sql-helper": "https://github.com/example/sql-helper",
  "debug-helper": "https://github.com/example/debug-helper",
  "api-designer": "https://github.com/example/api-designer"
}
EOF
fi

# Link global AGENTS to system AGENTS (so VS Code chat uses the same rules)
GLOBAL_AGENTS="$HOME/.codex/AGENTS.md"
if [ -e "$GLOBAL_AGENTS" ] && [ ! -L "$GLOBAL_AGENTS" ]; then
  cp "$GLOBAL_AGENTS" "$GLOBAL_AGENTS.bak.$(date +%Y%m%d%H%M%S)"
fi
ln -sfn ~/.codex/system/AGENTS.md "$GLOBAL_AGENTS"

# Create config if missing
CONFIG=~/.codex/config.toml
if [ ! -f "$CONFIG" ]; then
cat <<EOF > "$CONFIG"
project_doc_fallback_filenames = ["AGENTS.md"]
project_doc_max_bytes = 65536

[tools]
web_search = true
shell = true

[agent]
max_steps = 30

model_instructions_file = "~/.codex/AGENTS.md"
EOF
fi

echo "Codex setup complete."

if command -v ro >/dev/null 2>&1; then
  echo "ro is available at: $(command -v ro)"
else
  echo "'ro' is not yet in this shell PATH. Restart terminal or run: source ~/.bash_profile"
fi
