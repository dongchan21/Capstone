from services.vector_service import search_similar_docs
from services.llm_service import generate_answer

def answer_question(question):
    # 1️⃣ Vector DB에서 관련 문서 검색
    docs = search_similar_docs(question, top_k=3)
    if not docs:
        return {"answer": "현재 관련 정보가 부족합니다. 다른 질문을 해보시겠어요?"}

    # 2️⃣ 문맥 기반 답변 생성
    context = "\n".join([d["content"] for d in docs])
    answer = generate_answer(question, context)
    
    return {
        "answer": answer,
        "source_docs": [d["source"] for d in docs]
    }

def detect_intent(question):
    if any(word in question for word in ["높", "낮", "비교", "많", "적"]):
        return "numeric_query"
    else:
        return "semantic_query"
