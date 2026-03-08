# Created the Pydantic request/response models

from pydantic import BaseModel
from typing import Optional


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteUpdate(BaseModel):
    new_title: Optional[str]  = None
    new_content: Optional[str] = None


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str