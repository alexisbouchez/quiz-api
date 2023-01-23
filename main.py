from fastapi import FastAPI

import questions.crud
import quizzes.crud
from db import engine
from questions import models

# En production, on utiliserait des migrations.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(quizzes.crud.quizzes_router)
app.include_router(questions.crud.questions_router)