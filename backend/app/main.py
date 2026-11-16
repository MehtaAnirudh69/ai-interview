from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.concurrency import run_in_threadpool

from app.resume_service import (
    extract_resume_text,
    analyze_resume,
)
from app.schemas import (
    InterviewCreate,
    InterviewResponse,
    QuestionListResponse,
    AnswerEvaluationRequest,
    AnswerEvaluationResponse,
)
from app.llm_service import generate_questions, evaluate_answer, LLMBusyError
from app.rag_service import retrieve_relevant_questions


app = FastAPI(
    title="InterviewIQ - AI Mock Interview Agent",
    description="API for generating and evaluating mock interviews",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Temporary storage for today's implementation.
# Day 4 will replace this with SQLite.
interview_sessions = {}


@app.get("/")
def home():
    return {"message": "InterviewIQ API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post(
    "/interviews",
    response_model=InterviewResponse,
    status_code=201,
)
def create_interview(data: InterviewCreate):
    session_id = str(uuid4())

    interview_sessions[session_id] = {
        "job_title": data.job_title,
        "job_description": data.job_description,
        "difficulty": data.difficulty,
        "num_questions": data.num_questions,
        "questions": [],
    }

    return InterviewResponse(
        session_id=session_id,
        job_title=data.job_title,
        difficulty=data.difficulty,
        num_questions=data.num_questions,
        status="in_progress",
        message="Interview session created successfully",
    )


@app.post("/interviews/start")
async def start_interview(
    job_title: str = Form(...),
    job_description: str = Form(...),
    difficulty: str = Form("beginner"),
    num_questions: int = Form(5),
    interview_mode: str = Form("no_resume"),
    file: UploadFile | None = File(None),
):
    # Step 1: Validate interview mode
    if interview_mode not in ["resume", "no_resume"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid interview mode.",
        )

    # Step 2: Validate other inputs
    if len(job_title.strip()) < 2:
        raise HTTPException(
            status_code=400,
            detail="Job title must contain at least 2 characters.",
        )

    if len(job_description.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="Job description must contain at least 10 characters.",
        )

    if difficulty not in ["beginner", "intermediate", "advanced"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid difficulty.",
        )

    if not 3 <= num_questions <= 10:
        raise HTTPException(
            status_code=400,
            detail="Number of questions must be between 3 and 10.",
        )

    resume_text = None
    analysis = None

    # Step 3: Process resume if resume mode is selected
    if interview_mode == "resume":
        if file is None:
            raise HTTPException(
                status_code=400,
                detail="Please upload a PDF resume.",
            )

        if not file.filename or not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported.",
            )

        pdf_bytes = await file.read()

        if not pdf_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty.",
            )

        if len(pdf_bytes) > 5 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="Resume must be smaller than 5 MB.",
            )

        try:
            # These are blocking calls (PDF parsing, possibly an LLM call),
            # so run them in a thread to keep the server responsive.
            resume_text = await run_in_threadpool(
                extract_resume_text, pdf_bytes
            )
            analysis = await run_in_threadpool(
                analyze_resume, resume_text, job_description
            )

        except LLMBusyError as exc:
            print(f"AI provider busy: {exc}")
            raise HTTPException(
                status_code=503,
                detail="The AI service is busy right now. Please try again in a few seconds.",
                headers={"Retry-After": "10"},
            ) from exc
        except Exception as exc:
            raise HTTPException(
                status_code=400,
                detail=str(exc),
            ) from exc

    # Step 4: Return the result
    return {
        "job_title": job_title,
        "difficulty": difficulty,
        "num_questions": num_questions,
        "interview_mode": interview_mode,
        "resume_provided": resume_text is not None,
        "resume_analysis": analysis,
        "message": (
            "Resume processed successfully."
            if resume_text
            else "Ready to start without a resume."
        ),
    }


@app.post(
    "/interviews/{session_id}/questions",
    response_model=QuestionListResponse,
)
def create_questions(session_id: str):
    session = interview_sessions.get(session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found",
        )

    # Retrieval is a bonus: if it fails, still generate questions
    # from the job description alone.
    try:
        retrieved_context = retrieve_relevant_questions(
            job_title=session["job_title"],
            job_description=session["job_description"],
            difficulty=session["difficulty"],
            top_k=5,
        )
    except Exception as exc:
        print(f"Question retrieval failed, continuing without context: {exc}")
        retrieved_context = []

    try:
        questions = generate_questions(
            job_title=session["job_title"],
            job_description=session["job_description"],
            difficulty=session["difficulty"],
            num_questions=session["num_questions"],
            retrieved_context=retrieved_context,
        )
    except LLMBusyError as exc:
        print(f"AI provider busy: {exc}")
        raise HTTPException(
            status_code=503,
            detail="The AI service is busy right now. Please try again in a few seconds.",
            headers={"Retry-After": "10"},
        ) from exc
    except Exception as exc:
        print(f"Question generation failed: {exc}")
        raise HTTPException(
            status_code=502,
            detail="Could not generate questions. Check the AI configuration and try again.",
        ) from exc

    session["questions"] = questions

    return QuestionListResponse(
        session_id=session_id,
        questions=questions,
    )


@app.post(
    "/interviews/{session_id}/evaluate",
    response_model=AnswerEvaluationResponse,
)
def evaluate_candidate_answer(
    session_id: str,
    data: AnswerEvaluationRequest,
):
    session = interview_sessions.get(session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found",
        )

    try:
        result = evaluate_answer(
            job_title=session["job_title"],
            question=data.question,
            answer=data.answer,
            difficulty=session["difficulty"],
        )

        return AnswerEvaluationResponse.model_validate(result)

    except LLMBusyError as exc:
        print(f"AI provider busy: {exc}")
        raise HTTPException(
            status_code=503,
            detail="The AI service is busy right now. Please try again in a few seconds.",
            headers={"Retry-After": "10"},
        ) from exc
    except Exception as exc:
        print(f"Answer evaluation failed: {exc}")
        raise HTTPException(
            status_code=502,
            detail="Could not evaluate the answer. Check the AI configuration and try again.",
        ) from exc