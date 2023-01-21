from fastapi import FastAPI

import questions.crud
import quizzes.crud

app = FastAPI()
app.include_router(quizzes.crud.quizzes_router)
app.include_router(questions.crud.questions_router)