from dataclasses import dataclass


STATES = ("IDEA", "PLAN", "SPEC", "TASKS", "EXEC", "ANALYZE")


@dataclass(frozen=True)
class Transition:
    allowed_from: set[str]


RULES = {
    "/co-plan": Transition({"IDEA"}),
    "/co-create-spec": Transition({"PLAN"}),
    "/co-exec-tasks": Transition({"SPEC", "TASKS"}),
    "/co-analyze": Transition({"EXEC"}),
}


def next_state(current_state: str, command: str) -> str:
    if command not in RULES:
        raise ValueError("Unsupported command")

    rule = RULES[command]
    if current_state not in rule.allowed_from:
        raise ValueError(f"Invalid transition: {current_state} -> {command}")

    if command == "/co-plan":
        return "PLAN"
    if command == "/co-create-spec":
        return "SPEC"
    if command == "/co-exec-tasks":
        return "TASKS" if current_state == "SPEC" else "EXEC"
    if command == "/co-analyze":
        return "ANALYZE"

    raise ValueError("Unhandled workflow command")
