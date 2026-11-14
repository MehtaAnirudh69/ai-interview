
from io import BytesIO

from pypdf import PdfReader


COMMON_SKILLS = [
    "python",
    "c++",
    "java",
    "sql",
    "fastapi",
    "django",
    "flask",
    "rest api",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "langchain",
    "rag",
    "faiss",
    "git",
    "docker",
    "aws",
    "azure",
    "react",
    "javascript",
    "authentication",
]


def extract_resume_text(pdf_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(pdf_bytes))

    if reader.is_encrypted:
        raise ValueError(
            "Password-protected PDFs are not supported."
        )

    pages = []

    for page in reader.pages:
        pages.append(page.extract_text() or "")

    text = "\n".join(pages).strip()

    if not text:
        raise ValueError(
            "No readable text found. The PDF may be scanned."
        )

    return text


def find_skills(text: str) -> list[str]:
    normalized_text = text.lower()

    return [
        skill
        for skill in COMMON_SKILLS
        if skill in normalized_text
    ]


def analyze_resume(
    resume_text: str,
    job_description: str,
) -> dict:
    resume_skills = find_skills(resume_text)
    required_skills = find_skills(job_description)

    matched_skills = [
        skill
        for skill in required_skills
        if skill in resume_skills
    ]

    missing_skills = [
        skill
        for skill in required_skills
        if skill not in resume_skills
    ]

    return {
        "resume_skills": resume_skills,
        "job_skills": required_skills,
        "matched_skills": matched_skills,
        "potential_gaps": missing_skills,
    }
