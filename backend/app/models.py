
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.database import Base


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    session_id = Column(String, primary_key=True, index=True)
    job_title = Column(String(100), nullable=False)
    job_description = Column(Text, nullable=False)
    difficulty = Column(String(20), nullable=False)
    num_questions = Column(Integer, nullable=False)
    status = Column(String(30), default="in_progress")

    questions = relationship(
        "InterviewQuestion",
        back_populates="interview",
        cascade="all, delete-orphan",
    )


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(
        String,
        ForeignKey("interview_sessions.session_id"),
        nullable=False,
    )
    question = Column(Text, nullable=False)
    topic = Column(String(100), nullable=False)

    interview = relationship(
        "InterviewSession",
        back_populates="questions",
    )
    evaluations = relationship(
        "AnswerEvaluation",
        back_populates="question_record",
        cascade="all, delete-orphan",
    )


class AnswerEvaluation(Base):
    __tablename__ = "answer_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(
        Integer,
        ForeignKey("interview_questions.id"),
        nullable=False,
    )
    answer = Column(Text, nullable=False)
    score = Column(Float, nullable=False)
    strengths = Column(Text, nullable=False)
    improvements = Column(Text, nullable=False)
    feedback = Column(Text, nullable=False)
    sample_answer = Column(Text, nullable=False)

    question_record = relationship(
        "InterviewQuestion",
        back_populates="evaluations",
    )
