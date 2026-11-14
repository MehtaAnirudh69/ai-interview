from app.llm_service import client

SKIP = ("tts", "image", "live", "audio", "robotics", "computer-use", "lyria")

for m in client.models.list():
    name = m.name.replace("models/", "")
    actions = m.supported_actions or []
    if "generateContent" in actions and "gemini" in name and not any(s in name for s in SKIP):
        print(name)