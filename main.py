from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agents.question_agent import suggest_questions
from agents.rag_agent import answer_question

app = FastAPI()

# --- CORS 설정 추가 ---
origins = [
    "http://localhost:5173",  # Vite 기본 포트
    "http://127.0.0.1:5173",
    "*",                      # 개발 단계에서는 전체 허용 가능
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ------------------------


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/suggest")
def suggest(data: dict):
    print(f"📥 [POST /suggest] Request Body: {data}")
    return suggest_questions(data["user_message"], data.get("user_profile", {}))

@app.post("/answer")
def answer(data: dict):
    print(f"📥 [POST /answer] Request Body: {data}")
    return answer_question(data["selected_question"], data.get("user_profile", {}))
