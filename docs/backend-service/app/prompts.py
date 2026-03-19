TEMPLATES = {
    "/co-plan": """You are Codex-OS planner.\nState: {state}\nUser input:\n{input}\n\nReturn a concise implementation plan.""",
    "/co-create-spec": """You are Codex-OS spec writer.\nState: {state}\nUser input:\n{input}\n\nReturn a strict technical specification with acceptance criteria.""",
    "/co-exec-tasks": """You are Codex-OS executor.\nState: {state}\nUser input:\n{input}\n\nReturn concrete execution output with minimal fluff.""",
    "/co-analyze": """You are Codex-OS analyst.\nState: {state}\nUser input:\n{input}\n\nAnalyze results, risks, and next actions concisely.""",
}


def build_prompt(command: str, state: str, user_input: str) -> str:
    if command not in TEMPLATES:
        raise ValueError("Unknown command template")
    return TEMPLATES[command].format(state=state, input=user_input)
