from services.llm_service import generate_questions
from services.vector_service import check_question_validity

# return type: dict
# example output: {"category": "상품 추천 / 비교", "suggested_questions": ["ISA 계좌는 개인종합자산관리계좌로, ...", ..., "..."]}
def suggest_questions(user_message, user_profile):
    # 1️⃣ LLM으로 후보 질문 생성
    raw_questions = generate_questions(user_message, user_profile)

    # 2️⃣ Vector DB로 검증 (RAG가 답변 가능한가?)
    valid_questions = []
    for q in raw_questions:
        if check_question_validity(q):
            valid_questions.append(q)

    # 3️⃣ 실패 시 Fallback
    if not valid_questions:
        valid_questions = generate_questions(
            user_message,
            user_profile,
            restrict_topics=["예금", "적금", "금리", "단기 저축"]
        )

    return {
        "category": "상품 추천 / 비교",
        "suggested_questions": valid_questions[:3]
    }
