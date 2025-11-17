import os, json, pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

# 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "deposit_docs.json")
VEC_DIR = os.path.join(BASE_DIR, "vector_db")
os.makedirs(VEC_DIR, exist_ok=True)

INDEX_PATH = os.path.join(VEC_DIR, "deposit.index")
META_PATH  = os.path.join(VEC_DIR, "deposit_meta.pkl")

# 임베딩 모델
MODEL_NAME = "intfloat/multilingual-e5-base"

# 한 번에 임베딩할 배치 크기
BATCH_SIZE = 100

def main():
    # 새 데이터 불러오기
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        new_docs = json.load(f)

    # 모델 로드
    model = SentenceTransformer(MODEL_NAME)

    # 기존 인덱스 및 메타데이터 로드
    if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
        print("📦 기존 인덱스 및 메타데이터 로드 중 ...")
        index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, "rb") as f:
            old_meta = pickle.load(f)
    else:
        print("🆕 새 인덱스 생성 중 ...")
        index = None
        old_meta = []

    # 기존 텍스트 중복 방지
    existing_texts = set(d["content"] for d in old_meta)
    filtered_docs = [d for d in new_docs if d["content"] not in existing_texts]

    if not filtered_docs:
        print("⚠️ 추가할 새로운 문서가 없습니다. 인덱싱을 건너뜁니다.")
        return

    total = len(filtered_docs)
    print(f"➕ {total}개의 새 문서 추가 중 ...")

    # 배치 단위로 임베딩 생성 및 로그 출력
    all_embs = []
    for i in range(0, total, BATCH_SIZE):
        batch_docs = filtered_docs[i:i + BATCH_SIZE]
        texts = [d["content"] for d in batch_docs]
        emb = model.encode(texts, normalize_embeddings=True).astype(np.float32)
        all_embs.append(emb)

        # ✅ 100개 단위 로그 출력
        print(f"[INFO] {min(i + BATCH_SIZE, total)}/{total} rows processed...")

    # 전체 병합
    all_embs = np.vstack(all_embs)
    dim = all_embs.shape[1]

    # 인덱스 초기화 또는 기존 이어쓰기
    if index is None:
        index = faiss.IndexFlatIP(dim)
    index.add(all_embs)

    updated_meta = old_meta + filtered_docs

    # 저장
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(updated_meta, f)

    print(f"✅ 인덱싱 완료 (총 {len(updated_meta)}개 문서)")
    print(f"- index: {INDEX_PATH}")
    print(f"- meta : {META_PATH}")

if __name__ == "__main__":
    main()
