import faiss
from sentence_transformers import SentenceTransformer

from app.question_bank import QUESTION_BANK


def chunk_text(
    text: str,
    chunk_size: int = 100,
    overlap: int = 20
) -> list[str]:
    """
    Split reference text into smaller overlapping chunks (measured in words).
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be non-negative and smaller than chunk_size")

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        # Stop once the last words are covered. Without this, a short
        # redundant tail chunk (entirely inside the previous chunk's
        # overlap) would be added.
        if end >= len(words):
            break

        start += chunk_size - overlap

    return chunks

# --------------------------------------------------
# 1. Load pretrained embedding model
# --------------------------------------------------

# Converts text into numerical embeddings.
# all-MiniLM-L6-v2 generates 384-dimensional vectors.

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# --------------------------------------------------
# 2. Prepare searchable text from question bank
# --------------------------------------------------

question_texts = []

for item in QUESTION_BANK:

    searchable_text = (
        f"Topic: {item['topic']}. "
        f"Question: {item['text']}. "
        f"Concepts: {', '.join(item['concepts'])}."
    )

    question_texts.append(searchable_text)


# --------------------------------------------------
# 3. Generate embeddings
# --------------------------------------------------

embeddings = embedding_model.encode(
    question_texts,
    convert_to_numpy=True,
    normalize_embeddings=True,
)


# --------------------------------------------------
# 4. Create FAISS vector index
# --------------------------------------------------

# IndexFlatIP performs inner-product similarity search.
# Normalized embeddings make this equivalent to cosine similarity.

vector_index = faiss.IndexFlatIP(
    embeddings.shape[1]
)

# Store all question embeddings in FAISS.
vector_index.add(embeddings)


# --------------------------------------------------
# 5. Retrieve relevant questions
# --------------------------------------------------


def retrieve_relevant_questions(
    job_title: str,
    job_description: str,
    difficulty: str,
    top_k: int = 5,
) -> list[dict]:

    search_text = (
        f"Job title: {job_title}. "
        f"Job description: {job_description}."
    )

    query_embedding = embedding_model.encode(
        [search_text],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    if top_k <= 0 or len(QUESTION_BANK) == 0:
        return []

    # Retrieve all entries so difficulty filtering
    # does not accidentally remove relevant candidates.
    scores, indices = vector_index.search(
        query_embedding,
        len(QUESTION_BANK),
    )

    results = []

    for score, index in zip(scores[0], indices[0]):

        if index == -1:
            continue

        item = QUESTION_BANK[int(index)]

        # Filter by requested difficulty.
        if item["difficulty"].lower() != difficulty.lower():
            continue

        results.append({
            "topic": item["topic"],
            "difficulty": item["difficulty"],
            "question": item["text"],
            "reference_answer": item["reference_answer"],
            "concepts": item["concepts"],
            "similarity": round(float(score), 3),
        })

        if len(results) == top_k:
            break

    return results


# ==================================================
# ANSWER-CHUNK INDEX (used for RAG-based evaluation)
# ==================================================

# Reference answers are split into chunks and stored in a SEPARATE FAISS
# index. At grading time the candidate's question is used to retrieve the
# most relevant reference chunks.

ANSWER_CHUNK_SIZE = 40   # words per chunk
ANSWER_CHUNK_OVERLAP = 8

# Minimum cosine similarity for a chunk to be trusted as grading material.
# Tune this by printing scores for real questions (see test script).
ANSWER_MATCH_THRESHOLD = 0.45


# --------------------------------------------------
# 6. Chunk every reference answer, keeping metadata
# --------------------------------------------------

answer_records = []

for item in QUESTION_BANK:

    chunks = chunk_text(
        item["reference_answer"],
        chunk_size=ANSWER_CHUNK_SIZE,
        overlap=ANSWER_CHUNK_OVERLAP,
    )

    for chunk_number, chunk in enumerate(chunks):
        answer_records.append({
            "text": chunk,
            "chunk_number": chunk_number,
            "question": item["text"],
            "topic": item["topic"],
            "concepts": item["concepts"],
        })


# --------------------------------------------------
# 7. Embed chunks and build the separate FAISS index
# --------------------------------------------------

# Prefixing topic and question keeps each chunk's meaning clear even
# when it is only part of a longer answer.
answer_chunk_texts = [
    f"Topic: {record['topic']}. "
    f"Question: {record['question']}. "
    f"Answer: {record['text']}"
    for record in answer_records
]

answer_embeddings = embedding_model.encode(
    answer_chunk_texts,
    convert_to_numpy=True,
    normalize_embeddings=True,
)

answer_index = faiss.IndexFlatIP(
    answer_embeddings.shape[1]
)

answer_index.add(answer_embeddings)


# --------------------------------------------------
# 8. Retrieve reference chunks for a question
# --------------------------------------------------


def retrieve_answer_chunks(
    question: str,
    top_k: int = 3,
    min_score: float = ANSWER_MATCH_THRESHOLD,
) -> list[dict]:
    """
    Return up to top_k reference-answer chunks most similar to `question`,
    keeping only those whose similarity is at least `min_score`.
    An empty list means nothing in the bank was relevant enough.
    """

    if top_k <= 0 or not answer_records:
        return []

    query_embedding = embedding_model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    scores, indices = answer_index.search(
        query_embedding,
        min(top_k, len(answer_records)),
    )

    results = []

    for score, index in zip(scores[0], indices[0]):

        if index == -1 or float(score) < min_score:
            continue

        record = answer_records[int(index)]

        results.append({
            **record,
            "similarity": round(float(score), 3),
        })

    return results
