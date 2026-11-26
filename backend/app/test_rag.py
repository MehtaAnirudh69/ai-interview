
from app.rag_service import retrieve_relevant_questions

results = retrieve_relevant_questions(
    job_title="Python Developer",
    job_description=(
        "Knowledge of Python, OOP, FastAPI, "
        "SQL and REST APIs."
    ),
    difficulty="Beginner",
    top_k=3
)

print("\nRetrieved Questions:\n")

for i, result in enumerate(results, start=1):

    print(f"\nQuestion {i}:")
    print("Topic:", result["topic"])
    print("Difficulty:", result["difficulty"])
    print("Question:", result["question"])
    print("Reference Answer:", result["reference_answer"])
    print("Concepts:", result["concepts"])
    print("Similarity:", result["similarity"])
