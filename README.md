InterviewIQ – AI Mock Interview Agent

An AI-powered mock interview platform that simulates technical interviews based on a Job Description (JD). It generates role-specific interview questions, evaluates candidate responses using an LLM, and provides structured feedback to help candidates improve their interview performance.

Features

JD-Based Interview Generation: Generates relevant technical interview questions based on the job description, role, and difficulty level.

AI-Powered Answer Evaluation: Evaluates candidate answers using an LLM and a structured evaluation rubric.

RAG-Based Question Retrieval: Uses Retrieval-Augmented Generation (RAG) to retrieve relevant questions and reference answers from a curated question bank.

Semantic Search: Uses Sentence-Transformers embeddings and FAISS to retrieve semantically relevant information.

Structured Feedback: Provides evaluation results and improvement suggestions in a structured format.

Interview Session Management: Maintains interview sessions and stores interview history using SQLite.

REST API Backend: Provides API endpoints through FastAPI for communication between the frontend and backend.
