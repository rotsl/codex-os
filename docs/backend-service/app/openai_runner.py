from openai import OpenAI


def run_openai(prompt: str, api_key: str, model: str, retries: int = 2) -> str:
    client = OpenAI(api_key=api_key)
    last_err = None

    for _ in range(retries + 1):
        try:
            resp = client.responses.create(model=model, input=prompt)
            text = getattr(resp, "output_text", "")
            if text:
                return text.strip()

            # fallback for older shapes
            return str(resp)
        except Exception as exc:
            last_err = exc

    raise RuntimeError(f"OpenAI request failed after retries: {last_err}")
