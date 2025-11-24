import os
from typing import List, Dict, Optional
from openai import OpenAI

USE_MOCK = os.getenv("USE_MOCK_LLM", "0") == "1"
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

_client = None
# Lazy initialization of OpenAI client
def _client_lazy():
    global _client
    if _client is None:
        _client = OpenAI()  # 환경변수 OPENAI_API_KEY 필요
    return _client

# Mock functions for testing without actual LLM calls
def _mock_questions(user_message: str, user_profile: Dict, restrict_topics: Optional[List[str]] = None) -> List[str]:
    # 사용자 메시지 기반으로 다양한 mock 질문 생성
    if "대출" in user_message:
        return ["대출 금리는 어떻게 결정되나요?", "신용대출과 담보대출의 차이는?", "대출 한도는 어떻게 산정되나요?"]
    elif "펀드" in user_message or "투자" in user_message:
        return ["펀드와 주식 투자의 차이는?", "안정적인 펀드 상품 추천해주세요", "펀드 수익률은 어떻게 확인하나요?"]
    else:
        return [
            "예금과 적금의 차이가 뭐예요?",
            "단기 저축에 더 유리한 상품은 무엇인가요?",
            "적금이 예금보다 이자가 항상 높은가요?",
            "예금/적금 중도해지 시 불이익이 있나요?",
            "금리 비교 시 어떤 기준을 봐야 하나요?"
        ]
    return base if 'base' in locals() else []

def _mock_answer(question: str, context: str) -> str:
    return f"모의응답: 질문 \"{question}\"에 대해 문서 내용을 바탕으로 요약하면 — {context[:120]}..."

def generate_questions_from_context(user_message: str, user_profile: Dict, similar_docs: List[Dict]) -> List[str]:
    """벡터 DB에서 검색된 문서 내용을 기반으로 질문 생성"""
    if USE_MOCK:
        return _mock_questions(user_message, user_profile, None)
    
    # 문서 내용 추출 및 포맷팅
    context_parts = []
    for i, doc in enumerate(similar_docs[:5], 1):
        doc_content = doc.get('content', '') or doc.get('text', '')
        doc_meta = doc.get('meta', {})
        context_parts.append(f"[문서 {i}] {doc_meta}\n내용: {doc_content[:200]}...")
    
    context = "\n\n".join(context_parts)
    
    prompt = f"""
당신은 금융 챗봇의 '질문 추천' 역할입니다.
사용자의 질문과 관련된 문서 내용을 참고하여, 사용자가 추가로 궁금해할 만한 질문 5개를 제안하세요.

**중요**: 아래 검색된 문서 내용에 기반하여 답변 가능한 질문만 생성하세요.
질문은 짧고 클릭하기 쉽게 만드세요.

사용자 질문: "{user_message}"
사용자 프로필: {user_profile}

[검색된 관련 문서]
{context}

출력은 각 질문을 한 줄씩 나열만 하세요.
"""
    
    client = _client_lazy()
    resp = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    content = resp.choices[0].message.content.strip()
    lines = [l.strip("- ").strip() for l in content.split("\n") if l.strip()]
    return lines[:5]

def generate_questions(user_message: str, user_profile: Dict, restrict_topics: Optional[List[str]] = None) -> List[str]:
    if USE_MOCK:
        return _mock_questions(user_message, user_profile, restrict_topics)

    topics_line = f"\n참고 주제: {', '.join(restrict_topics)}" if restrict_topics else ""
    prompt = f"""
당신은 금융 챗봇의 '질문 추천' 역할입니다.
사용자 입력과 프로필을 참고하여 금융 관련(예금/적금, 대출, 펀드, 보험, 카드 등) 후속 질문 5개를 제안하세요.
사용자의 질문 의도를 정확히 파악하여 관련성 높은 질문을 생성하세요.
질문은 짧고 클릭하기 쉽게 만드세요.
사용자 입력: "{user_message}"
사용자 프로필: {user_profile}{topics_line}
출력은 각 질문을 한 줄씩 나열만 하세요.
"""
    client = _client_lazy()
    resp = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    content = resp.choices[0].message.content.strip()
    lines = [l.strip("- ").strip() for l in content.split("\n") if l.strip()]
    return lines[:5]

def generate_answer(question: str, context: str, user_profile: Optional[Dict] = None) -> str:
    if USE_MOCK:
        return _mock_answer(question, context)

    profile_text = f"\n[사용자 프로필]\n{user_profile}\n" if user_profile else ""

    prompt = f"""
다음 문서 내용을 바탕으로 사용자의 질문에 정확하고 간결하게 답하세요.
금융 상품(예금/적금, 대출, 펀드, 보험, 카드 등)의 특징, 조건, 금리, 혜택 등을 명확히 설명하세요.
사용자 프로필이 제공된 경우, 해당 정보를 고려하여 맞춤형 답변을 제공하세요.

[문서]
{context}
{profile_text}
[질문]
{question}
"""
    client = _client_lazy()
    resp = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()
