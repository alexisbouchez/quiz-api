from pydantic import BaseModel


class Answer(BaseModel):
    text: str
    is_correct: bool

    class Config:
        orm_mode = True


class Question(BaseModel):
    id: int
    text: str
    answers: list[Answer] = []

    class Config:
        orm_mode = True


class QuestionInput(BaseModel):
    text: str
    answers: list[Answer] = []
