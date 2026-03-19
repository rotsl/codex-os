from collections import defaultdict, deque
from datetime import datetime

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from .config import settings
from .db import Base, engine, get_db
from .models import CommandLog, Project, SessionToken, StateEvent
from .openai_runner import run_openai
from .prompts import build_prompt
from .schemas import (
    ApiKeyIn,
    CommandsOut,
    CommandItem,
    ExecuteIn,
    ExecuteOut,
    ProjectOut,
    SessionOut,
    UpsertProjectIn,
)
from .security import contains_injection, decrypt_key, encrypt_key, hash_token, issue_token
from .workflow import next_state


app = FastAPI(title="Codex-OS Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
rate_bucket: dict[str, deque[datetime]] = defaultdict(deque)


def _require_session(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization format")

    token = authorization.removeprefix("Bearer ").strip()
    token_hash = hash_token(token)

    session = db.scalar(select(SessionToken).where(SessionToken.token_hash == token_hash))
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session token")

    now = datetime.utcnow()
    bucket = rate_bucket[token_hash]
    while bucket and (now - bucket[0]).total_seconds() > 60:
        bucket.popleft()

    if len(bucket) >= settings.rate_limit_per_minute:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    bucket.append(now)
    return token_hash


@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}


@app.post("/session/anonymous", response_model=SessionOut)
def create_session(db: Session = Depends(get_db)):
    token = issue_token()
    session = SessionToken(token_hash=hash_token(token))
    db.add(session)
    db.commit()
    return SessionOut(token=token)


@app.post("/projects/upsert", response_model=ProjectOut)
def upsert_project(payload: UpsertProjectIn, db: Session = Depends(get_db), owner: str = Depends(_require_session)):
    project = db.get(Project, payload.projectId)
    if project is None:
        project = Project(id=payload.projectId, name=payload.name, state="IDEA", owner_token_hash=owner)
        db.add(project)
    else:
        if project.owner_token_hash != owner:
            raise HTTPException(status_code=403, detail="Project belongs to different session")
        project.name = payload.name

    db.commit()
    db.refresh(project)
    return ProjectOut(id=project.id, name=project.name, state=project.state, updatedAt=project.updated_at)


@app.get("/projects/{project_id}", response_model=ProjectOut)
def get_project(project_id: str, db: Session = Depends(get_db), owner: str = Depends(_require_session)):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_token_hash != owner:
        raise HTTPException(status_code=403, detail="Project belongs to different session")

    return ProjectOut(id=project.id, name=project.name, state=project.state, updatedAt=project.updated_at)


@app.post("/projects/{project_id}/api-key")
def set_api_key(project_id: str, payload: ApiKeyIn, db: Session = Depends(get_db), owner: str = Depends(_require_session)):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_token_hash != owner:
        raise HTTPException(status_code=403, detail="Project belongs to different session")

    project.api_key_encrypted = encrypt_key(payload.apiKey)
    db.commit()

    return {"status": "ok", "projectId": project_id}


@app.get("/projects/{project_id}/commands", response_model=CommandsOut)
def list_commands(
    project_id: str,
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    owner: str = Depends(_require_session),
):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_token_hash != owner:
        raise HTTPException(status_code=403, detail="Project belongs to different session")

    rows = db.scalars(
        select(CommandLog)
        .where(CommandLog.project_id == project_id)
        .order_by(CommandLog.created_at.desc())
        .limit(limit)
    ).all()

    items = [
        CommandItem(
            command=row.command,
            fromState=row.from_state,
            toState=row.to_state,
            createdAt=row.created_at,
            output=row.output_text,
        )
        for row in rows
    ]

    return CommandsOut(items=items)


@app.post("/execute", response_model=ExecuteOut)
def execute(payload: ExecuteIn, db: Session = Depends(get_db), owner: str = Depends(_require_session)):
    project = db.get(Project, payload.projectId)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_token_hash != owner:
        raise HTTPException(status_code=403, detail="Project belongs to different session")

    if not project.api_key_encrypted:
        raise HTTPException(status_code=400, detail="API key not configured for project")

    if contains_injection(payload.input):
        raise HTTPException(status_code=400, detail="Input rejected by prompt injection filter")

    previous = project.state
    try:
        new_state = next_state(previous, payload.command)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))

    prompt = build_prompt(payload.command, previous, payload.input)
    api_key = decrypt_key(project.api_key_encrypted)

    output = run_openai(prompt=prompt, api_key=api_key, model=settings.openai_model, retries=2)

    if not output or len(output.strip()) < 2:
        raise HTTPException(status_code=500, detail="Model returned empty output")

    project.state = new_state
    db.add(
        CommandLog(
            project_id=project.id,
            command=payload.command,
            input_text=payload.input,
            output_text=output,
            from_state=previous,
            to_state=new_state,
        )
    )
    db.add(
        StateEvent(
            project_id=project.id,
            command=payload.command,
            from_state=previous,
            to_state=new_state,
        )
    )
    db.commit()

    return ExecuteOut(
        projectId=project.id,
        command=payload.command,
        previousState=previous,
        newState=new_state,
        output=output,
    )
