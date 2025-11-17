from fastapi import FastAPI
from agents.question_agent import suggest_questions
from agents.rag_agent import answer_question

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/suggest")
def suggest(data: dict):
    return suggest_questions(data["user_message"], data.get("user_profile", {}))

@app.post("/answer")
def answer(data: dict):
    return answer_question(data["selected_question"])
