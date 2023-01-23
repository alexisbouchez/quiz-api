from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from quizzes import models, schemas
from quizzes.models import Quizz
from quizzes.schemas import Quiz, QuizInput

quizzes_router = APIRouter()


@quizzes_router.get("/quizzes", response_model=list[schemas.Quiz])
def read_quizzes(db: Session = Depends(get_db)) -> list[Quiz]:
    return db.query(Quizz).all()


@quizzes_router.post("/quizzes")
def create_quiz(quiz_input: QuizInput, db: Session = Depends(get_db)) -> Quiz:
    created_quiz = models.Quizz(title=quiz_input.title, tags=quiz_input.tags)
    db.add(created_quiz)
    db.commit()
    db.refresh(created_quiz)

    return created_quiz


def get_quiz_by_id(id: int, db: Session) -> Quiz | None:
    return db.query(models.Quizz).filter(
        models.Quizz.id == id
    ).first()


@quizzes_router.get("/quizzes/{id}")
def read_quiz(id: int, db: Session = Depends(get_db)) -> Quiz:
    quiz = get_quiz_by_id(id, db)
    if quiz is None:
        raise HTTPException(404, "Quiz not found")
    return quiz


@quizzes_router.patch("/quizzes/{id}")
def update_quiz(id: int, quiz_input: QuizInput, db: Session = Depends(get_db)) -> Quiz:
    quiz = get_quiz_by_id(id, db)
    if quiz is None:
        raise HTTPException(404, "Quiz not found")

    quiz.title = quiz_input.title
    quiz.tags = quiz_input.tags
    db.commit()

    return quiz


@quizzes_router.delete("/quizzes/{id}")
def delete_quiz(id: int, db: Session = Depends(get_db)) -> str:
    quiz = get_quiz_by_id(id, db)
    if quiz is None:
        raise HTTPException(404, "Quiz not found")

    db.delete(quiz)
    db.commit()

    return "Quiz deleted"
