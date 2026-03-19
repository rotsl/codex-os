from dataclasses import dataclass
import os


@dataclass
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./codex_os.db")
    master_key_b64: str = os.getenv("MASTER_KEY_B64", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-5-mini")
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "30"))


settings = Settings()
