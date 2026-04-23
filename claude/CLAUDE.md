# Codex-OS for Claude Code

This file is the global Claude-facing orchestration layer for `codex-os`.

## Purpose
- keep Claude Code behavior aligned with the same repo conventions used by Codex-OS
- keep project-local state isolated by default
- allow either Claude-native memory or deterministic project memory

## Execution Model
- classify the task first: `coding`, `writing`, `mixed`, or `analysis/planning`
- load minimal context first
- execute directly when the path is obvious
- continue until the task is complete and validated

## Memory Modes
- `auto`: use `CLAUDE.md` and Claude Code's own memory behavior as the primary memory mechanism
- `deterministic`: use `memory/context.md` and `memory/decisions.md` as the primary memory mechanism when those summaries are explicitly provided by `ro-claude`

## Rules
- prefer minimal correct changes
- avoid redundant narration
- keep architecture proportional
- use deeper reasoning only when it improves execution
- separate prose cleanup rules from technical literal output

## Subagents
- project or user Claude subagents may mirror the roles from `codex-os`
- prefer planner, builder, architect, writer, and reviewer roles only when the task benefits from delegation
