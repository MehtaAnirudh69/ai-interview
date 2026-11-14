
from typing import Literal

from pydantic import BaseModel, Field


class InterviewCreate(BaseModel):
    job_title: str = Field(min_length=2, max_length=100)
    job_description: str = Field(min_length=10)
    difficulty: Literal[
        "beginner", "intermediate", "advanced"
    ] = "beginner"
    num_questions: int = Field(default=5, ge=3, le=10)


class InterviewResponse(BaseModel):
    session_id: str
    job_title: str
    difficulty: str
    num_questions: int
    status: str
    message: str


class QuestionItem(BaseModel):
    question: str
    topic: str


class QuestionListResponse(BaseModel):
    session_id: str
    questions: list[QuestionItem]


class AnswerEvaluationRequest(BaseModel):
    question: str = Field(min_length=5)
    answer: str = Field(min_length=2, max_length=10000)


class AnswerEvaluationResponse(BaseModel):
    score: float = Field(ge=0, le=10)
    strengths: list[str]
    improvements: list[str]
    feedback: str
    sample_answer: str
