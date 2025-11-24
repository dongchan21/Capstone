from services.llm_service import generate_questions_from_context
from services.vector_service import search_similar_docs

# return type: dict
# example output: {"category": "상품 추천 / 비교", "suggested_questions": ["ISA 계좌는 개인종합자산관리계좌로, ...", ..., "..."]}
def suggest_questions(user_message, user_profile):
    print(f"\n🔍 질문 추천 시작: '{user_message}'")
    
    # 1️⃣ 벡터 DB에서 유사 문서 검색
    similar_docs = search_similar_docs(user_message, top_k=5)
    print(f"📚 벡터 DB에서 {len(similar_docs)}개 유사 문서 검색")
    
    if not similar_docs:
        print("⚠️ 벡터 DB에서 관련 문서를 찾을 수 없음")
        return {
            "category": "일반",
            "suggested_questions": [
                "죄송합니다. 해당 주제에 대한 정보가 부족합니다.",
                "다른 금융 관련 주제로 질문해주세요."
            ]
        }
    
    # 2️⃣ 검색된 문서 내용을 기반으로 LLM이 질문 생성
    suggested_questions = generate_questions_from_context(
        user_message, 
        user_profile, 
        similar_docs
    )
    print(f"✨ 벡터 DB 기반 질문 {len(suggested_questions)}개 생성")
    for i, q in enumerate(suggested_questions, 1):
        print(f"  ✅ [{i}] {q}")

    return {
        "category": "상품 추천 / 비교",
        "suggested_questions": suggested_questions[:3]
    }
