# Completion Skill

## Purpose
Prevent premature stopping and drive validated completion.

## Continue Signals
- output is progress-only
- work is incomplete
- fixable error path exists
- required validation is missing

## Stop Signals
- output is complete
- validation is complete
- no unresolved blockers remain
- next step does not meaningfully improve output

## Guardrails
- do not continue destructive actions without explicit confirmation
- do not invent missing input
- stop when blocked by permissions or required user input
- if the same failure repeats 3 times, report blocker + attempts and pause

## Loop
1. execute next step
2. check completion and value
3. continue only if meaningful
4. otherwise stop
