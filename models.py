from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class SuggestRequest(BaseModel):
    user_message: str
    user_profile: Dict = Field(default_factory=dict)

class SuggestResponse(BaseModel):
    category: str = "상품 추천 / 비교"
    suggested_questions: List[str]

class AnswerRequest(BaseModel):
    selected_question: str

class AnswerResponse(BaseModel):
    answer: str
    source_docs: List[str] = []
