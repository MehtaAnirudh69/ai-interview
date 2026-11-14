
import faiss
from sentence_transformers import SentenceTransformer

from app.question_bank import QUESTION_BANK


# Load a pretrained model that converts sentences into embeddings.
# The first run may download the model.
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# Convert every question into a vector.
question_texts = [
    item["text"] for item in QUESTION_BANK
]

embeddings = embedding_model.encode(
    question_texts,
    convert_to_numpy=True,
    normalize_embeddings=True,
)

# Create a FAISS index for cosine-similarity search.
# Normalized vectors + inner product give cosine similarity.
vector_index = faiss.IndexFlatIP(embeddings.shape[1])
vector_index.add(embeddings)


def retrieve_relevant_questions(
    job_title: str,
    job_description: str,
    difficulty: str,
    top_k: int = 5,
) -> list[dict]:
    """Find question-bank entries relevant to an interview."""

    search_text = (
        f"Job title: {job_title}. "
        f"Job description: {job_description}. "
        f"Difficulty: {difficulty}."
    )

    query_embedding = embedding_model.encode(
        [search_text],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    number_to_retrieve = min(top_k, len(QUESTION_BANK))

    scores, indices = vector_index.search(
        query_embedding,
        number_to_retrieve,
    )

    results = []

    for score, index in zip(scores[0], indices[0]):
        if index == -1:
            continue

        item = QUESTION_BANK[int(index)]

        results.append({
            "topic": item["topic"],
            "difficulty": item["difficulty"],
            "text": item["text"],
            "similarity": round(float(score), 3),
        })

    return results
 