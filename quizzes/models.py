from sqlalchemy import Column, Integer, String, ARRAY
from sqlalchemy.orm import relationship

from db import Base


class Quizz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    tags = Column(ARRAY(String))

    questions = relationship("Question", back_populates="quiz")