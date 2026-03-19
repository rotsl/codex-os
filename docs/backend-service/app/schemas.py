from datetime import datetime
from pydantic import BaseModel, Field


class SessionOut(BaseModel):
    token: str


class UpsertProjectIn(BaseModel):
    projectId: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=200)


class ProjectOut(BaseModel):
    id: str
    name: str
    state: str
    updatedAt: datetime


class ApiKeyIn(BaseModel):
    apiKey: str = Field(min_length=20, max_length=300)


class ExecuteIn(BaseModel):
    projectId: str = Field(min_length=1, max_length=64)
    command: str = Field(pattern=r"^/co-(plan|create-spec|exec-tasks|analyze)$")
    input: str = Field(min_length=1, max_length=20000)


class ExecuteOut(BaseModel):
    projectId: str
    command: str
    previousState: str
    newState: str
    output: str


class CommandItem(BaseModel):
    command: str
    fromState: str
    toState: str
    createdAt: datetime
    output: str


class CommandsOut(BaseModel):
    items: list[CommandItem]
