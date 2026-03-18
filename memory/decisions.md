# Persistent Decision Log

## Durable Decisions
- `AGENTS.md` stays orchestration-only; details live in `agents/`, `skills/`, `rules/`, `contexts/`, and `memory/`.
- mode classification is mandatory before execution.
- notai is prose-only and excluded from technical literal output.
- continuation is required for multi-step tasks, bounded by validation and value checks.
- memory remains two-file primary state: current state (`context.md`) and durable reasoning (`decisions.md`).

## Reusable Patterns
- execute immediately when the solution is obvious.
- use reasoning only when depth improves execution quality.
- use structure to compress ambiguity into atomic actions.

## Persistent Constraints
- no raw logs in memory
- no duplicated rules across files
- no plan-only stop when implementation is feasible
