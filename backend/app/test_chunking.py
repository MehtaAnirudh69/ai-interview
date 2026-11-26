
from app.question_bank import QUESTION_BANK
from app.rag_service import chunk_text

# Find the SQL question
sql_question = next(
    item for item in QUESTION_BANK
    if item["topic"] == "SQL"
)

# Extract its reference answer
reference_answer = sql_question["reference_answer"]

# Split into chunks
chunks = chunk_text(
    reference_answer,
    chunk_size=15,
    overlap=3
)

# Display results
for i, chunk in enumerate(chunks, start=1):
    print(f"\nChunk {i}:")
    print(chunk)
