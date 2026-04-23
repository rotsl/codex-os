# Context Loading Rules

## Purpose
Load only what is necessary for the active mode.

## Order
1. `AGENTS.md`
2. `rules/*`
3. `memory/context.md`
4. `memory/decisions.md`
5. relevant `agents/*`
6. required `skills/*`
7. additional `contexts/*` only when blocked

## Policy
- start minimal
- expand only when required for correctness
