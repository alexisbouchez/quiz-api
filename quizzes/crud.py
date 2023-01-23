from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from quizzes import models, schemas
from quizzes.models import Quizz
from quizzes.schemas import Quiz, QuizInput

fake_quizzes: list[Quiz] = [
    Quiz(id=1, title="Top 10 Docker Interview Questions", tags=["docker", "interview"]),
    Quiz(id=2, title="Top Common Interview PHP Questions", tags=["php", "interview"]),
    Quiz(id=3, title="Common Docker Swarm Interview Questions", tags=["docker", "swarm", "interview"]),
]

quizzes_router = APIRouter()

@quizzes_router.get("/quizzes", response_model=list[schemas.Quiz])
def read_quizzes(db: Session = Depends(get_db)) -> list[Quiz]:
    return db.query(Quizz).all()


@quizzes_router.post("/quizzes")
def create_quiz(quiz_input: QuizInput, db: Session = Depends(get_db)) -> Quiz:
    quiz = Quiz(id=len(fake_quizzes) + 1, title=quiz_input.title, tags=quiz_input.tags)
    fake_quizzes.append(quiz)

    created_quiz = models.Quizz(title=quiz_input.title, tags=quiz_input.tags)
    db.add(created_quiz)
    db.commit()
    db.refresh(created_quiz)
    print(created_quiz)

    return quiz


def get_quiz_by_id(id: int) -> Quiz | None:
    for quiz in fake_quizzes:
        if quiz.id == id:
            return quiz
    return None


@quizzes_router.get("/quizzes/{id}")
def read_quiz(id: int) -> Quiz:
    quiz = get_quiz_by_id(id)
    if quiz is None:
        raise HTTPException(404, "Quiz not found")
    return quiz


@quizzes_router.patch("/quizzes/{id}")
def update_quiz(id: int, quiz_input: QuizInput) -> Quiz:
    quiz = get_quiz_by_id(id)
    if quiz is None:
        raise HTTPException(404, "Quiz not found")

    quiz.title = quiz_input.title
    quiz.tags = quiz_input.tags

    return quiz


@quizzes_router.delete("/quizzes/{id}")
def delete_quiz(id: int) -> str:
    quiz = get_quiz_by_id(id)
    if quiz is None:
        raise HTTPException(404, "Quiz not found")

    fake_quizzes.remove(quiz)
    return "Quiz deleted"