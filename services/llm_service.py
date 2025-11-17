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
    base = [
        "예금과 적금의 차이가 뭐예요?",
        "단기 저축에 더 유리한 상품은 무엇인가요?",
        "적금이 예금보다 이자가 항상 높은가요?",
        "예금/적금 중도해지 시 불이익이 있나요?",
        "금리 비교 시 어떤 기준을 봐야 하나요?"
    ]
    return base

def _mock_answer(question: str, context: str) -> str:
    return f"모의응답: 질문 \"{question}\"에 대해 문서 내용을 바탕으로 요약하면 — {context[:120]}..."

def generate_questions(user_message: str, user_profile: Dict, restrict_topics: Optional[List[str]] = None) -> List[str]:
    if USE_MOCK:
        return _mock_questions(user_message, user_profile, restrict_topics)

    topics_line = f"\n참고 주제: {', '.join(restrict_topics)}" if restrict_topics else ""
    prompt = f"""
당신은 금융 챗봇의 '질문 추천' 역할입니다.
사용자 입력과 프로필을 참고하여 '예금/적금' 범위에서 후속 질문 5개를 제안하세요.
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

def generate_answer(question: str, context: str) -> str:
    if USE_MOCK:
        return _mock_answer(question, context)

    prompt = f"""
다음 문서 내용을 바탕으로 사용자의 질문에 정확하고 간결하게 답하세요.
가능하면 예금/적금의 차이, 금리, 유동성, 중도해지 등을 명확히 설명하세요.
[문서]
{context}

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
