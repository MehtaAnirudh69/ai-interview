const API_URL = "http://127.0.0.1:8000";

async function handleResponse(response) {
    const data = await response.json();

    if (!response.ok) {
        const message =
            typeof data.detail === "string"
                ? data.detail
                : JSON.stringify(data.detail || data);

        throw new Error(message);
    }

    return data;
}

// Create interview session
export async function createInterview(details) {
    const response = await fetch(`${API_URL}/interviews`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(details),
    });

    return handleResponse(response);
}

// Generate questions
export async function generateQuestions(sessionId) {
    const response = await fetch(
        `${API_URL}/interviews/${sessionId}/questions`,
        {
            method: "POST",
        }
    );

    return handleResponse(response);
}

// Evaluate answer
export async function evaluateAnswer(sessionId, question, answer) {
    const response = await fetch(
        `${API_URL}/interviews/${sessionId}/evaluate`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                question,
                answer,
            }),
        }
    );

    return handleResponse(response);
}

// Analyze uploaded resume
export async function analyzeResume(details, file) {
    const formData = new FormData();

    formData.append("job_title", details.job_title);
    formData.append("job_description", details.job_description);
    formData.append("difficulty", details.difficulty);
    formData.append("num_questions", details.num_questions);
    formData.append("interview_mode", "resume");
    formData.append("file", file);

    const response = await fetch(`${API_URL}/interviews/start`, {
        method: "POST",
        body: formData,
    });

    return handleResponse(response);
}