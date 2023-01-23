from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from db import get_db
from questions import models
from questions.schemas import Question, QuestionInput
from quizzes.crud import get_quiz_by_id

questions_router = APIRouter()


@questions_router.post("/quizzes/{quiz_id}/questions")
def create_question(quiz_id: int, create_question_input: QuestionInput, db: Session = Depends(get_db)) -> Question:
    quiz = get_quiz_by_id(quiz_id, db)
    if quiz is None:
        raise HTTPException(404, "Quiz not found")

    question = Question(
        **create_question_input.dict(),
        id=len(quiz.questions) + 1
    )

    created_question = models.Question(
        quiz_id=quiz_id,
        text=create_question_input.text,
    )
    db.add(created_question)
    db.commit()
    db.refresh(created_question)

    answers = []
    for answer_input in question.answers:
        answers.append(
            models.Answer(question_id=created_question.id, **answer_input.dict())
        )
    db.add_all(answers)
    db.commit()

    return created_question


@questions_router.get("/quizzes/{quiz_id}/questions")
def get_questions(quiz_id: int):
    quiz = get_quiz_by_id(quiz_id)
    if quiz is None:
        raise HTTPException(404, "Quiz not found")
    return quiz.questions


def get_question_by_id_with_quiz(quiz_id: int, question_id: int) -> Question | None:
    quiz = get_quiz_by_id(quiz_id)
    if quiz is None:
        return None
    for question in quiz.questions:
        if question.id == question_id:
            return question
    return None


@questions_router.get("/quizzes/{quiz_id}/questions/{question_id}")
def get_question(quiz_id: int, question_id: int) -> Question:
    question = get_question_by_id_with_quiz(quiz_id, question_id)
    if question is None:
        raise HTTPException(404, "Question not found")
    return question


@questions_router.patch("/quizzes/{quiz_id}/questions/{question_id}")
def update_question(quiz_id: int, question_id: int, update_question_input: QuestionInput) -> Question:
    question = get_question_by_id_with_quiz(quiz_id, question_id)
    if question is None:
        raise HTTPException(404, "Question not found")

    quiz = get_quiz_by_id(quiz_id)
    quiz.questions[question_id - 1].text = update_question_input.text
    quiz.questions[question_id - 1].answers = update_question_input.answers

    return quiz.questions[question_id - 1]


@questions_router.delete("/quizzes/{quiz_id}/questions/{question_id}")
def delete_question(quiz_id: int, question_id: int):
    quiz = get_quiz_by_id(quiz_id)
    if quiz is None:
        return
    question = get_question_by_id_with_quiz(quiz_id, question_id)
    if question is None:
        return
    quiz.questions.remove(question)
