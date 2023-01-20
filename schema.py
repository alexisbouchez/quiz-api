from typing import Optional

from pydantic import BaseModel


class Quiz(BaseModel):
    id: int
    title: str
    tags: list[str] = []


class QuizInput(BaseModel):
    title: str
    tags: list[str] = []