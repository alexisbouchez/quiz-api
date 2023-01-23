from pydantic import BaseModel

from questions.schemas import Question


class QuizBase(BaseModel):
    id: int


class Quiz(QuizBase):
    title: str
    tags: list[str] = []
    questions: list[Question] = []

    class Config:
        orm_mode = True


class QuizInput(BaseModel):
    title: str
    tags: list[str] = []
