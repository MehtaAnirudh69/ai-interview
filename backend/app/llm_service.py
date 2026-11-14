import os
import json
import time
import random

import httpx
from dotenv import load_dotenv
from google import genai
from google.genai import errors, types


# Load environment variables from backend/.env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

# Optional comma-separated fallbacks, e.g.
# GEMINI_FALLBACK_MODELS=gemini-2.5-flash,gemini-2.5-flash-lite
FALLBACK_MODELS = [
    m.strip()
    for m in os.getenv("GEMINI_FALLBACK_MODELS", "").split(",")
    if m.strip()
]
MODELS_TO_TRY = [MODEL_NAME, *FALLBACK_MODELS]

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Add it to backend/.env"
    )

client = genai.Client(
    api_key=API_KEY,
    http_options=types.HttpOptions(timeout=60_000),  # 20s per call (ms)
)

# HTTP status codes worth retrying (temporary problems)
TRANSIENT_CODES = {429, 500, 503, 504}
MAX_ATTEMPTS_PER_MODEL = 1
MAX_OUTPUT_ATTEMPTS = 1  # retries for bad JSON / failed validation


class LLMBusyError(Exception):
    """Raised when the AI provider stays unavailable after all retries."""


def _call_gemini(prompt: str) -> str:
    """
    Call Gemini, retrying transient errors with exponential backoff and
    falling back to other models if the primary one stays unavailable.
    """
    last_exc = None

    for model in MODELS_TO_TRY:
        for attempt in range(MAX_ATTEMPTS_PER_MODEL):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config={"response_mime_type": "application/json"},
                )
                return response.text

            except errors.APIError as exc:
                last_exc = exc

                if exc.code not in TRANSIENT_CODES:
                    # Bad key, bad request, unknown model, etc.
                    # Retrying won't help, so fail immediately.
                    raise

                if attempt < MAX_ATTEMPTS_PER_MODEL - 1:
                    time.sleep(2 ** attempt + random.random())

            except (httpx.TimeoutException, httpx.TransportError) as exc:
                last_exc = exc
                print(f"Timeout/network error on '{model}': {exc}")

                if attempt < MAX_ATTEMPTS_PER_MODEL - 1:
                    time.sleep(2 ** attempt + random.random())

        print(f"Model '{model}' still unavailable, trying next fallback...")

    raise LLMBusyError(str(last_exc)) from last_exc


def _generate_json(prompt: str, validate):
    """
    Call Gemini and parse/validate the JSON result. If the model returns
    malformed JSON or output that fails validation, try again.
    `validate` receives the parsed dict, may raise ValueError, and
    returns the value to hand back.
    """
    last_exc = None

    for _ in range(MAX_OUTPUT_ATTEMPTS):
        text = _call_gemini(prompt)
        try:
            result = json.loads(text)
            return validate(result)
        except (json.JSONDecodeError, ValueError) as exc:
            last_exc = exc
            print(f"Bad model output, retrying: {exc}")

    raise ValueError(f"Model returned invalid output: {last_exc}")


def generate_questions(
    job_title: str,
    job_description: str,
    difficulty: str,
    num_questions: int,
    retrieved_context: list[dict] | None = None,
) -> list[dict]:
    context_text = "\n".join(
        f"- Topic: {item['topic']}; "
        f"Difficulty: {item['difficulty']}; "
        f"Question: {item['text']}"
        for item in (retrieved_context or [])
    )

    if not context_text:
        context_text = "No relevant question-bank context was found."

    prompt = f"""
    You are an experienced technical interviewer.

    Generate exactly {num_questions} interview questions for this role.

    Job title: {job_title}
    Job description: {job_description}
    Difficulty: {difficulty}

    Relevant question-bank context:
    {context_text}

    Use this context to understand which topics matter for this role.
    Create new, role-specific questions inspired by the relevant topics.
    Do not simply copy every retrieved question.
    If the context is not relevant, prioritize the job description.

    Requirements:
    - Questions must be relevant to the job description.
    - Use clear, professional language.
    - Avoid duplicate questions.
    - Include a mixture of conceptual and practical questions.
    - Do not provide the answers.

    Return valid JSON in this exact format:
    {{
        "questions": [
            {{
                "question": "The interview question",
                "topic": "The topic being tested"
            }}
        ]
    }}
    """

    def validate(result: dict) -> list[dict]:
        questions = result.get("questions", [])
        if len(questions) != num_questions:
            raise ValueError(
                f"Expected {num_questions} questions, "
                f"but received {len(questions)}."
            )
        return questions

    return _generate_json(prompt, validate)


def evaluate_answer(
    job_title: str,
    question: str,
    answer: str,
    difficulty: str,
) -> dict:
    prompt = f"""
    You are a fair and constructive interview evaluator.

    Job title: {job_title}
    Difficulty: {difficulty}
    Interview question: {question}
    Candidate answer: {answer}

    Evaluate only the answer provided. Do not assume experience
    or knowledge that the candidate has not demonstrated.

    Score the answer from 0 to 10 using:
    - Technical correctness: 0 to 4 points
    - Explanation and clarity: 0 to 3 points
    - Relevance and completeness: 0 to 3 points

    Return valid JSON in this exact format:
    {{
        "score": 0,
        "strengths": ["A strength"],
        "improvements": ["An improvement"],
        "feedback": "Constructive feedback",
        "sample_answer": "A concise example of a strong answer"
    }}

    The score must be a number between 0 and 10.
    Keep feedback specific to the question and answer.
    """

    def validate(result: dict) -> dict:
        score = result.get("score")
        if (
            isinstance(score, bool)
            or not isinstance(score, (int, float))
            or not 0 <= score <= 10
        ):
            raise ValueError("Gemini returned an invalid score.")
        return result

    return _generate_json(prompt, validate)