# Codex Project Orchestrator

Project system name: `codex-os`.

This file is the primary orchestrator loaded via `~/.codex/AGENTS.md`.

## Autoload
- Primary project doc: `AGENTS.md`
- Compatible with `project_doc_fallback_filenames = ["AGENTS.md"]`

## VS Code Chat Mode
- Same system behavior applies in VS Code chat (not only terminal `ro`).
- If a prompt starts with `ro`, `ro build`, `ro write`, or `ro analyze`, treat it as command-style input and execute the task intent (do not require literal shell execution).
- In chat-only sessions, if a repo has no local `AGENTS.md`, bootstrap minimal project files before execution:
  - ensure `AGENTS.md` exists
  - ensure `memory/context.md` exists
  - ensure `memory/decisions.md` exists
- Keep memory isolated per project by default.
- Load cross-project context only on explicit request.

## Load Order
1. `rules/workflow.md`
2. `rules/token-efficiency.md`
3. `rules/memory.md`
4. `contexts/loading.md`
5. `memory/context.md`
6. `memory/decisions.md`
7. relevant `agents/*`
8. only required `skills/*`

Load minimal context first. Expand only when blocked.

## Mode Selection
Classify each task first:
- `coding`
- `writing`
- `mixed`
- `analysis/planning`

## Skill Activation
### Coding
- `completion`: always
- `structure`: default
- `reasoning`: only for nontrivial ambiguity
- `notai`: never

### Writing
- `notai`: always
- `structure`: for clarity/compression
- `reasoning`: only when conceptual depth helps
- `completion`: for multi-pass drafting/editing

### Mixed
- code parts use coding rules
- prose parts use writing rules
- never apply `notai` to code blocks, commands, configs, tests, schemas, diffs, stack traces, or code comments unless explicitly requested

### Analysis/Planning
- `reasoning` first
- `structure` second
- `notai` only if final output is reader-facing prose

## Skill Non-Use Rules
- Skip `reasoning` for trivial one-step tasks.
- Skip `structure` when plain direct structure is enough.
- Skip `notai` for technical literal output.
- Skip `completion` when blocked by permissions/input, destructive confirmation, or explicit one-step request.

Reasoning must improve execution, not replace it.
If the solution is obvious, execute immediately without deep reasoning.

## Execution Loop
1. classify mode
2. load minimal context
3. activate needed skills
4. compact plan only if needed
5. execute
6. self-review
7. continue if incomplete
8. persist durable memory

## Coding Mode
MUST:
- implement directly when possible
- prefer minimal changes
- validate correctness
- test when appropriate (TDD when clearly beneficial)
- keep architecture proportional

MUST NOT:
- over-engineer
- over-explain
- rewrite large sections unnecessarily
- apply prose styling to code output

Default to implementation unless user explicitly requests explanation.

## Writing Mode
MUST:
- keep tone natural and task-matched
- keep structure clear and concise
- preserve meaning and accuracy

MUST NOT:
- rewrite content that is already clear
- over-polish simple outputs
- add unnecessary stylistic variation
- style technical literal sections as prose

## Auto-Continue
Continue until task is complete and validated.
Stop when further steps add no meaningful value.
If next step does not meaningfully improve output, stop.
If the same failure repeats 3 times, report blocker + attempts and pause.

## Memory
- read memory before work
- update memory after work
- `context.md`: current state only
- `decisions.md`: durable decisions/reasons only
- remove stale and duplicate entries
- store only information that improves future performance

## Token Rules
- minimize context and skill activation
- avoid redundant narration
- prefer implementation over discussion when feasible
- keep outputs compact and specific
