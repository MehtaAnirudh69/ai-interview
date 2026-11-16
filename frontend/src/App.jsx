import { useState } from "react";

import {
    createInterview,
    generateQuestions,
    evaluateAnswer,
    analyzeResume,
} from "./services/api";

import "./App.css";

function App() {
    const [mode, setMode] = useState("no_resume");

    const [jobTitle, setJobTitle] = useState("");
    const [jobDescription, setJobDescription] = useState("");
    const [difficulty, setDifficulty] = useState("beginner");
    const [numQuestions, setNumQuestions] = useState(5);
    const [file, setFile] = useState(null);

    const [sessionId, setSessionId] = useState("");
    const [questions, setQuestions] = useState([]);
    const [currentIndex, setCurrentIndex] = useState(0);
    const [answer, setAnswer] = useState("");

    const [result, setResult] = useState(null);
    const [resumeAnalysis, setResumeAnalysis] = useState(null);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    async function startInterview(event) {
        event.preventDefault();

        setLoading(true);
        setError("");
        setResult(null);
        setQuestions([]);
        setResumeAnalysis(null);
        setSessionId("");
        setCurrentIndex(0);
        setAnswer("");

        try {
            // Analyze resume if selected
            if (mode === "resume") {
                if (!file) {
                    throw new Error("Please upload your PDF resume.");
                }

                const analysis = await analyzeResume(
                    {
                        job_title: jobTitle,
                        job_description: jobDescription,
                        difficulty,
                        num_questions: numQuestions,
                    },
                    file
                );

                setResumeAnalysis(analysis.resume_analysis);
            }

            // Create interview session
            const session = await createInterview({
                job_title: jobTitle,
                job_description: jobDescription,
                difficulty,
                num_questions: Number(numQuestions),
            });

            setSessionId(session.session_id);

            // Generate questions
            const generated = await generateQuestions(
                session.session_id
            );

            setQuestions(generated.questions);

        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    async function submitAnswer(event) {
        event.preventDefault();

        if (!answer.trim()) {
            setError("Please enter your answer.");
            return;
        }

        setLoading(true);
        setError("");

        try {
            const evaluation = await evaluateAnswer(
                sessionId,
                questions[currentIndex].question,
                answer
            );

            setResult(evaluation);

        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    function nextQuestion() {
        setCurrentIndex((previous) => previous + 1);
        setAnswer("");
        setResult(null);
    }

    function restartInterview() {
        setSessionId("");
        setQuestions([]);
        setCurrentIndex(0);
        setAnswer("");
        setResult(null);
        setResumeAnalysis(null);
        setError("");
    }

    const interviewFinished =
        questions.length > 0 &&
        currentIndex >= questions.length;

    return (
        <div className="app">

            <header className="navbar">
                <h2>InterviewIQ</h2>
                <span>AI Mock Interview Agent</span>
            </header>

            <main className="container">

                {!sessionId && (
                    <section className="setup-card">

                        <h1>Prepare for your next interview</h1>

                        <p className="subtitle">
                            Practice with AI-generated,
                            role-specific interview questions.
                        </p>

                        <div className="mode-selector">

                            <button
                                type="button"
                                className={
                                    mode === "resume" ? "active" : ""
                                }
                                onClick={() => setMode("resume")}
                            >
                                With Resume
                            </button>

                            <button
                                type="button"
                                className={
                                    mode === "no_resume" ? "active" : ""
                                }
                                onClick={() => setMode("no_resume")}
                            >
                                Without Resume
                            </button>

                        </div>

                        <form onSubmit={startInterview}>

                            <label>Job Title</label>

                            <input
                                type="text"
                                placeholder="e.g. Python Developer"
                                value={jobTitle}
                                onChange={(e) =>
                                    setJobTitle(e.target.value)
                                }
                                required
                            />

                            <label>Job Description</label>

                            <textarea
                                placeholder="Enter the required skills and job responsibilities..."
                                value={jobDescription}
                                onChange={(e) =>
                                    setJobDescription(e.target.value)
                                }
                                required
                            />

                            {mode === "resume" && (
                                <>
                                    <label>Upload Resume (PDF)</label>

                                    <input
                                        type="file"
                                        accept=".pdf,application/pdf"
                                        onChange={(e) =>
                                            setFile(e.target.files[0])
                                        }
                                        required
                                    />
                                </>
                            )}

                            <label>Difficulty</label>

                            <select
                                value={difficulty}
                                onChange={(e) =>
                                    setDifficulty(e.target.value)
                                }
                            >
                                <option value="beginner">Beginner</option>
                                <option value="intermediate">Intermediate</option>
                                <option value="advanced">Advanced</option>
                            </select>

                            <label>Number of Questions</label>

                            <select
                                value={numQuestions}
                                onChange={(e) =>
                                    setNumQuestions(Number(e.target.value))
                                }
                            >
                                <option value={3}>3</option>
                                <option value={5}>5</option>
                                <option value={7}>7</option>
                                <option value={10}>10</option>
                            </select>

                            <button
                                className="primary-btn"
                                type="submit"
                                disabled={loading}
                            >
                                {loading
                                    ? "Preparing Interview..."
                                    : "Start Interview"}
                            </button>

                        </form>

                    </section>
                )}

                {error && (
                    <div className="error">
                        {error}
                    </div>
                )}

                {resumeAnalysis && (
                    <section className="result-card">
                        <h2>Resume Analysis</h2>

                        <p>
                            <strong>Matched skills:</strong>{" "}
                            {resumeAnalysis.matched_skills.join(", ") || "None identified"}
                        </p>

                        <p>
                            <strong>Potential skill gaps:</strong>{" "}
                            {resumeAnalysis.potential_gaps.join(", ") || "None identified"}
                        </p>
                    </section>
                )}

                {questions.length > 0 && !interviewFinished && (
                    <section className="interview-card">

                        <p className="progress">
                            Question {currentIndex + 1} of {questions.length}
                        </p>

                        <h2>
                            {questions[currentIndex].question}
                        </h2>

                        <p className="topic">
                            Topic: {questions[currentIndex].topic}
                        </p>

                        {!result && (
                            <form onSubmit={submitAnswer}>

                                <textarea
                                    placeholder="Write your answer here..."
                                    value={answer}
                                    onChange={(e) =>
                                        setAnswer(e.target.value)
                                    }
                                    required
                                />

                                <button
                                    className="primary-btn"
                                    type="submit"
                                    disabled={loading}
                                >
                                    {loading
                                        ? "Evaluating..."
                                        : "Submit Answer"}
                                </button>

                            </form>
                        )}

                        {result && (
                            <div className="evaluation">

                                <h3>
                                    Score: {result.score}/10
                                </h3>

                                <p>{result.feedback}</p>

                                <h4>Strengths</h4>

                                <ul>
                                    {result.strengths.map((item, index) => (
                                        <li key={index}>{item}</li>
                                    ))}
                                </ul>

                                <h4>Areas to Improve</h4>

                                <ul>
                                    {result.improvements.map((item, index) => (
                                        <li key={index}>{item}</li>
                                    ))}
                                </ul>

                                <h4>Sample Answer</h4>

                                <p>{result.sample_answer}</p>

                                {currentIndex + 1 < questions.length ? (
                                    <button
                                        className="primary-btn"
                                        onClick={nextQuestion}
                                    >
                                        Next Question
                                    </button>
                                ) : (
                                    <button
                                        className="primary-btn"
                                        onClick={nextQuestion}
                                    >
                                        Finish Interview
                                    </button>
                                )}

                            </div>
                        )}

                    </section>
                )}

                {interviewFinished && (
                    <section className="result-card">
                        <h1>Interview Completed!</h1>
                        <p>You have answered all the questions.</p>

                        <button
                            className="primary-btn"
                            onClick={restartInterview}
                        >
                            Start Another Interview
                        </button>
                    </section>
                )}

            </main>

        </div>
    );
}

export default App;