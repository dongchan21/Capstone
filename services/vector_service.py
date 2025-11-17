from sentence_transformers import SentenceTransformer
import faiss, numpy as np, json
import os, pickle

INDEX_PATH = "vector_db/deposit.index"
META_PATH = "vector_db/deposit_meta.pkl"
EMB_MODEL = "intfloat/multilingual-e5-base"

_emb_model = None
_index = None
_docs = None

def _lazy_load():
    """필요시 벡터 DB, 문서 메타데이터 로드"""
    global _emb_model, _index, _docs

    if _emb_model is None:
        _emb_model = SentenceTransformer(EMB_MODEL)
        print("🧠 임베딩 모델 로드 완료")

    if _index is None:
        if not os.path.exists(INDEX_PATH):
            raise FileNotFoundError(f"❌ {INDEX_PATH} not found.")
        _index = faiss.read_index(INDEX_PATH)
        print("📦 벡터 인덱스 로드 완료")

    if _docs is None:
        if os.path.exists(META_PATH):
            with open(META_PATH, "rb") as f:
                _docs = pickle.load(f)
            print(f"📚 {_docs and len(_docs)}개 문서 메타 로드됨 (from deposit_meta.pkl)")
        else:
            print("⚠️ 메타데이터 파일 없음. 빈 리스트로 초기화")
            _docs = []

def search_similar_docs(query, top_k=3):
    """쿼리에 가장 유사한 문서 반환"""
    _lazy_load()
    query_emb = _emb_model.encode([query])
    D, I = _index.search(query_emb, top_k)

    results = []
    for idx, score in zip(I[0], D[0]):
        if 0 <= idx < len(_docs):
            results.append(_docs[idx])
            print(f"📄 매칭 문서: {_docs[idx].get('meta', {})} | score={score:.4f}")

    return results


# return type: bool
def check_question_validity(question):
    results = search_similar_docs(question, top_k=1)
    return len(results) > 0