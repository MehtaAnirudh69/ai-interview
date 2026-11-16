import time
from google import genai
from google.genai import types
from app.llm_service import API_KEY

client = genai.Client(
    api_key=API_KEY,
    http_options=types.HttpOptions(timeout=15_000),  # 15s per model
)

MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.6-flash",
    "gemini-3.7-flash",
    "gemini-3.8-flash",
]

for model in MODELS:
    t = time.time()
    try:
        r = client.models.generate_content(model=model, contents="Say hi")
        print(f"{model}: OK in {time.time()-t:.1f}s")
    except Exception as e:
        print(f"{model}: FAILED in {time.time()-t:.1f}s -> {str(e)[:80]}")