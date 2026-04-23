# Codex Autoload Compatibility

Repository system name: `codex-os`.

Codex should autoload this repository via project docs.

## Expected config
In `~/.codex/config.toml`:

```toml
project_doc_fallback_filenames = ["AGENTS.md"]
```

## Behavior
- load `AGENTS.md` at session start
- let `AGENTS.md` orchestrate rules, memory, agents, and skills
