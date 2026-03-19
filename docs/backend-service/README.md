# Codex-OS Backend Service (External)

This is a reference backend for Codex-OS frontend (`/docs/index.html`).

## Features
- BYOK with AES-256 encryption at rest
- Server-side workflow enforcement: `IDEA -> PLAN -> SPEC -> TASKS -> EXEC -> ANALYZE`
- Persistent projects and command history
- `/execute` endpoint with OpenAI call using user key
- Simple anonymous session token authentication

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

## Required env
- `MASTER_KEY_B64`: URL-safe base64-encoded 32-byte key for AES-256 (`AESGCM`)
- `DATABASE_URL`: e.g. `sqlite:///./codex_os.db` or PostgreSQL URL

Generate key:
```bash
python - <<'PY'
import base64, os
print(base64.urlsafe_b64encode(os.urandom(32)).decode())
PY
```
